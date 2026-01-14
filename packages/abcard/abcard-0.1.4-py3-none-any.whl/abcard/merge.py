import numpy as np
import pandas as pd
from functools import reduce
import os, platform
from ctypes import CDLL, c_double, c_int, c_uint, Structure, POINTER, pointer, sizeof, addressof, byref

from .stats import bins_cnt, group_agg
from .utils import check_memory

script_dir = os.path.dirname(os.path.abspath(__file__))
system = platform.system()
if system == "Windows":
    lib_path = os.path.join(script_dir, "libs", "split.dll")
elif system == "Linux":
    lib_path = os.path.join(script_dir, "libs", "split.so")
elif system == "Darwin":
    lib_path = os.path.join(script_dir, "libs", "split.dylib")
else:
    raise OSError(f"Unsupported platform: {system}")

calc = CDLL(lib_path)

class FtFgNum(Structure):
    _fields_ = [('value', c_double), ('flag', c_int)]
class CountsNum(Structure):
    _fields_ = [('value', c_double), ('count', c_int * 3)]
class ChiValue(Structure):
    _fields_ = [('chisquare', c_double), ('pvalue', c_double)]
class GroupsNum(Structure):
    _fields_ = [('groups', POINTER(CountsNum)), ('len', c_int)]
class ChainNum(Structure):
    pass
ChainNum._fields_ = [('link', CountsNum), ('chi', c_double), ('prev', POINTER(ChainNum)), 
                     ('next', POINTER(ChainNum))]

calc.chi2.argtypes = [c_int * 2 * 2, c_int, c_int, c_int]
calc.chi2.restype = ChiValue
calc.groupbinNum.argtypes = [POINTER(FtFgNum), c_uint, c_int]
calc.groupbinNum.restype = GroupsNum
calc.chi_splitNum.argtypes = [POINTER(FtFgNum), c_uint, c_double, c_int, c_double, c_int, c_double, c_int]
calc.chi_splitNum.restype = POINTER(ChainNum)
calc.freeCN.argtypes = [POINTER(ChainNum)]
calc.freeCN.restype = None
calc.freeP.argtypes = [POINTER(CountsNum)]
calc.freeP.restype = None


def chi2(bins: np.ndarray, forced_correction: int, chi_inv: int, call_p: int) -> list[float, float]:
    '''Fourfold Chi-Square Test, also known as the 2×2 Contingency Table Chi-Square Test.
    
    Args:
        forced_correction: A non-zero value forces the use of the chi-square correction formula. A value of 0 determines the calculation method based on the following conditions:
            1. If the total number is < 40 or any expected frequency is < 1, use Fisher's exact test.
            2. If the total number is > 40 and any expected frequency is < 5, use the chi-square correction formula.
            3. If the total number is > 40 and all expected frequencies are >= 5, use the standard chi-square formula.
        chi_inv: When Fisher's exact test is used, this parameter determines whether to inversely approximate the chi-square value (a simple approximation with some loss of precision). 
            A non-zero value triggers the approximate calculation; otherwise, the chi-square value is returned as -1.
        call_p: When the chi-square correction formula is used, this parameter indicates whether to calculate the p-value (to avoid redundant calculations). 
            A non-zero value calculates the p-value; otherwise, it is not calculated.
    
    Returns:
        [chi-square value, P-value]
    '''
    if not isinstance(bins, np.ndarray):
        bins = np.array(bins)
    if bins.shape != (2,2) or np.isnan(bins).any():
        return np.nan
    
    grid = (c_int * 2 * 2)()
    grid[0][0] = c_int(int(bins[0,0]))
    grid[0][1] = c_int(int(bins[0,1]))
    grid[1][0] = c_int(int(bins[1,0]))
    grid[1][1] = c_int(int(bins[1,1]))
    respt = calc.chi2(grid, forced_correction, chi_inv, call_p)
    return [respt.chisquare, respt.pvalue]

def cutcat(srs: pd.Series, split: list) -> pd.Series:
    '''Regroups ordered categorical objects and returns new ordered categorical objects; NaN values do not participate in the regrouping.

    Args:
        srs: A pandas Series, an ordered categorical object with dtype CategoricalDtype.
        split: A list of split points constructed from the 'cat.codes' attribute of `srs` (left-open, right-closed interval).

    Returns:
        If the elements in `srs` are pd.Interval objects, the element type of the returned object remains unchanged; 
        otherwise, the element type of the returned object is tuple.
    '''
    
    scut = pd.cut(srs.cat.codes, [-1] + split, duplicates = 'drop')
    newcat = []
    cat = srs.cat.categories
    if isinstance(cat[0], pd.Interval):
        right = [cat[0].left] + [i.right for i in cat[split]]
        for l,r in zip(right[:-1],  right[1:]):
            newcat.append(pd.Interval(left = l, right = r))
    else:
        tup = [i if isinstance(i, tuple) else (i,) for i in cat]
        right = [int(i + 1) for i in split]
        for l,r in zip([0] + right[:-1],  right):
            newcat.append(reduce(tuple.__add__, tup[l:r]))
    new = scut.cat.codes.map({k: v for k, v in enumerate(newcat)})
    cut = new.astype(pd.CategoricalDtype(categories = newcat, ordered = True))
    cut.name = srs.name
    return cut, newcat

def _chi_split(feature: pd.Series, flag: pd.Series, chi2value: float = 3.841, pvalue: float = 0.05, forced_correction: bool = False, 
    minbin: float | int = 0.05, maxbins: None | int = None, woediff: float = 0.05, prebins: int = 1000, precision: int = 8, 
    retbins: bool = False, retcnt: bool = False) -> pd.Series | list:
    '''Chi-square binning. NaN values do not participate in binning.
    
    Args:
        feature: Supports float and category types.
        flag: For binary classification only.
        chi2value: Chi-square test threshold. The default is 3.841.
        pvalue: Significance threshold corresponding to the chi-square test threshold. The default is 0.05.
        forced_correction: Whether to force the use of the chi-square correction formula. 
            When forced correction is applied, binning is based on `chi2value`; otherwise, it is based on `pvalue`. The default is False.
        minbin: Minimum sample size per bin. If a decimal between 0 and 1, it represents the proportion of the sample size that is non-NaN values. The default is 0.05.
        maxbins: Maximum number of bins (excluding the NaN bin). The default is None.
        woediff: Merge adjacent bins if the absolute difference in WOE is less than this value after chi-square binning. The default is 0.05.
        prebins: Number of pre-bins. If the number of distinct values exceeds this, pre-binning will be performed based on percentiles of distinct values, 
            which can improve binning speed for variables with many distinct values. The default is 1000.
        precision: Display precision. For detailed explanation, refer to the pandas.cut method.
        retbins: Whether to return a list of feature binning results. If the feature is of float type, elements in bins are numerical values representing 
            the split points of left-open, right-closed intervals; if the feature is of category type, elements in bins are string tuples. The default is False.
        retcnt: Whether to return counts for each bin along with the total count.
    
    Returns:
        Returns a pandas.Series or a list composed of pandas.Series, list of bins, and numpy.array of counts.
    '''
    
    iscat = isinstance(feature.dtype, pd.CategoricalDtype)
    if maxbins is None:
        maxbins = 0
    notna = feature.notna().to_numpy()
    real_ft = feature[notna]
    real_fg = flag[notna]
    
    if iscat:
        if not feature.cat.ordered:
            count = real_fg.groupby(by = [real_ft.to_numpy(), real_fg.to_numpy()], sort = False, dropna = False).size().unstack(fill_value = 0)
            if 1 not in count: count[1] = 0
            ratio = count[1] / count.sum(axis = 1)
            feature = feature.cat.set_categories(new_categories = ratio.sort_values(ascending = False).index.to_list(), ordered = True)
            values = feature[notna].cat.codes
        else:
            values = real_ft.cat.codes
    elif pd.api.types.is_numeric_dtype(feature.dtype):
        values = real_ft
    else:
        raise TypeError('Supports only CategoricalDtype and numeric dtypes in pandas.')

    length = values.size
    if length == 0:
        feature = feature.astype('category')
        if retbins or retcnt:
            retn = [feature]
            if retbins:
                retn.append([])
            if retcnt:
                retn.append(np.array([[]]))
            return retn
        return feature
    
    ftfgnum = (FtFgNum * length)()
    for i, v in enumerate(zip(values, real_fg)):
        ftfgnum[i] = FtFgNum(c_double(v[0]), c_int(v[1]))
    chi_threshold = chi2value if forced_correction else pvalue
    res = calc.chi_splitNum(pointer(ftfgnum[0]), length, chi_threshold, c_int(forced_correction), minbin, maxbins, woediff, prebins)
    
    split = list()
    binscnt = list()
    p = res
    while p:
        split.append(p[0].link.value)
        binscnt.append([p[0].link.count[0], p[0].link.count[1], p[0].link.count[2]])
        p = p[0].next
    
    if iscat:
        ft_cut, split = cutcat(feature, [int(i) for i in split])
    else:
        split = [-np.inf] + split[:-1] + [np.inf]
        ft_cut = pd.cut(feature, bins = split, include_lowest= True, precision = precision)
        split = list(ft_cut.cat.categories)
    
    calc.freeCN(res)
    
    if retbins or retcnt:
        retn = [ft_cut]
        if retbins:
            retn.append(split)
        if retcnt:
            retn.append(np.array(binscnt))
        return retn
    return ft_cut

@check_memory()
def chi2_split(feature: pd.Series, flag: pd.Series, chi2value: float = 3.841, pvalue: float = 0.05, forced_correction: bool = False, 
        minbin: float | int = 0.05, maxbins: None | int = None, woediff: float = 0.05, prebins: int = 1000, mergena: bool = False) -> tuple[pd.Series, dict]:
    '''Chi-square binning. NaN values may participate in binning.
    
    Args:
        feature: Supports float and category types.
        flag: For binary classification only.
        chi2value: Chi-square test threshold. The default is 3.841.
        pvalue: Significance threshold corresponding to the chi-square test threshold. The default is 0.05.
        forced_correction: Whether to force the use of the chi-square correction formula. 
            When forced correction is applied, binning is based on `chi2value`; otherwise, it is based on `pvalue`. The default is False.
        minbin: Minimum sample size per bin. If a decimal between 0 and 1, it represents the proportion of the sample size that is non-NaN values. The default is 0.05.
        maxbins: Maximum number of bins (excluding the NaN bin). The default is None.
        woediff: Merge adjacent bins if the absolute difference in WOE is less than this value after chi-square binning. The default is 0.05.
        prebins: Number of pre-bins. If the number of distinct values exceeds this, pre-binning will be performed based on percentiles of distinct values, 
            which can improve binning speed for variables with many distinct values. The default is 1000.
        mergena: Whether NaN values can be merged for binning.
    
    Returns:
        Returns a pandas.Series or a tuple composed of pandas.Series, dict of binning-related statistical data.
        If NaN values are placed in a separate bin, the index of the statistical data for the NaN bin is always 0.
    '''
    
    if feature.empty:
        raise ValueError('`feature` is empty.')
    if feature.size != flag.size:
        raise ValueError("`feature` length and `flag` length do not match.")
    
    cut, split, binscnt = _chi_split(feature, flag, chi2value = chi2value, pvalue = pvalue, forced_correction = forced_correction, 
                minbin = minbin, maxbins = maxbins, woediff = woediff, prebins = prebins, retbins = True, retcnt = True)
    if binscnt.size == 0:
        binscnt = flag.value_counts().to_numpy()
        binscnt = np.append(binscnt, binscnt.sum()).reshape(1,-1)
        bins = {'split': [np.nan], 'bin': [0]}
        bins.update(group_agg(binscnt))
        return cut, bins

    mergeinx = -1
    fillnan = None
    isna = feature.isna()
    nancbad = flag[isna].sum()
    countnan = isna.sum()
    nanc = np.array([countnan - nancbad, nancbad])

    if mergena and isna.any():
        reac = binscnt[:,:2]
        chiv = []
        for i in reac:
            grid = np.array([i, nanc])
            tempchi = chi2(grid, forced_correction, 0, 0)
            chiv.append(tempchi[0] if forced_correction else tempchi[1])
        chiv = np.array(chiv)

        if forced_correction and chiv.min() < chi2value:
            mergeinx = chiv.argmin()
        elif not forced_correction and chiv.max() > pvalue:
            mergeinx = chiv.argmax()
        
        if mergeinx >= 0:
            fillnan = split[mergeinx]
            if isinstance(fillnan, tuple):
                newcat = {-1: fillnan}
                newcat.update({k:v for k,v in enumerate(split)})
                cut = cut.cat.codes.map(newcat).astype(pd.CategoricalDtype(categories = split, ordered = True))
                cut.name = feature.name
            else:
                cut.fillna(fillnan, inplace = True)
            cut, split, binscnt = _chi_split(cut, flag, chi2value = chi2value, pvalue = pvalue, forced_correction = forced_correction, 
                minbin = minbin, maxbins = maxbins, woediff = woediff, prebins = prebins, retbins = True, retcnt = True)
    
    bins = {}
    if mergeinx >= 0:
        for s in split:
            if (isinstance(fillnan, pd.Interval) and fillnan.left >= s.left and fillnan.right >= s.right) or (isinstance(fillnan, tuple) and set(fillnan).issubset(set(s))):
                fillnan = s
        bins.update({'fillnan': fillnan, 'fillnum': countnan})
    elif isna.any():
        split = [np.nan] + split
        binscnt = np.insert(binscnt, 0, np.append(nanc, countnan), axis = 0)
    
    bins.update({'split': split, 'bin': list(range(len(binscnt)))})
    bins.update(group_agg(binscnt))
    
    return cut, bins

@check_memory()
def dt_split(feature: pd.Series, flag: pd.Series, minbin: float | int = 0.05, maxbins: None | int = None, precision: int = 8) -> pd.Series | tuple:
    '''Decision tree binning, NaN values do not participate in binning.

    Args:
        feature: Supports float and category types.
        flag: For binary classification only.
        minbin: Minimum sample size per bin. If a decimal between 0 and 1, it represents the proportion of the sample size that is non-NaN values. The default is 0.05.
        maxbins: Maximum number of bins (excluding the NaN bin). The default is None.
        precision: Display precision. For detailed explanation, refer to the pandas.cut method.
        
    Returns:
        Returns a pandas.Series or a tuple composed of pandas.Series, dict of binning-related statistical data.
        If NaN values are placed in a separate bin, the index of the statistical data for the NaN bin is always 0.
    '''
    from sklearn.tree import DecisionTreeClassifier, _tree

        
    iscat = isinstance(feature.dtype, pd.CategoricalDtype)
    isnum = pd.api.types.is_numeric_dtype(feature.dtype)
    notna = feature.notna()
    real_ft = feature[notna]
    real_fg = flag[notna]
    if minbin > 0 and minbin < 1:
        minbin = max(int(minbin * len(feature)), 1)
    elif not isinstance(minbin, int) or minbin <= 0:
        raise ValueError('`minbin` is a floating-point number between (0, 1) or an integer greater than or equal to 1.')
    tr = DecisionTreeClassifier(min_samples_leaf = minbin, max_leaf_nodes = maxbins)

    if iscat:
        if not feature.cat.ordered:
            count = real_fg.groupby(by = [real_ft.to_numpy(), real_fg.to_numpy()], sort = False, dropna = False).size().unstack(fill_value = 0)
            if 1 not in count: count[1] = 0
            ratio = count[1] / count.sum(axis = 1)
            ratio.sort_values(ascending = False, inplace = True)
            feature = feature.cat.set_categories(new_categories = ratio.index, ordered = True)
            real_ft = feature[notna]
        feature = pd.Series(feature.cat.codes, name = feature.name, index = feature.index)
        feature[feature == -1] = np.nan
        tr.fit(real_ft.cat.codes.to_numpy().reshape((-1,1)), real_fg)
    elif isnum:
        real_ft = real_ft.to_numpy().reshape((-1,1))
        real_ft = np.where(np.isneginf(real_ft), np.finfo(np.float32).min, real_ft)
        real_ft = np.where(np.isposinf(real_ft), np.finfo(np.float32).max, real_ft)
        tr.fit(real_ft, real_fg)
    else:
        raise TypeError('Supports only CategoricalDtype and numeric dtypes in pandas.')

    thresholds = tr.tree_.threshold[tr.tree_.feature != _tree.TREE_UNDEFINED]
    if iscat:
        thresholds = np.hstack([-1, thresholds, real_ft.nunique() - 1])
    else:
        thresholds = np.hstack([-np.inf, thresholds, np.inf])
    thresholds.sort()

    ft_cut = pd.cut(feature, thresholds, include_lowest = True, precision = precision)

    if iscat:
        cat_cut = pd.cut(range(len(real_ft.cat.categories)), ft_cut.cat.categories, precision = precision)
        new_cat = real_ft.cat.categories.groupby(cat_cut)
        new_cat = {k: tuple(v) for k,v in new_cat.items()}
        ft_cut = ft_cut.cat.rename_categories(new_cat)
    
    split = ft_cut.cat.categories.to_list()
    if not notna.all():
        split = [np.nan] + split
    binscnt = bins_cnt(ft_cut, flag).to_numpy()
    
    bins = {'split': split, 'bin': list(range(len(binscnt)))}
    bins.update(group_agg(binscnt))
    return ft_cut, bins


