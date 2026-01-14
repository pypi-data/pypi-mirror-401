import numpy as np
import pandas as pd
from sklearn.metrics import auc, roc_curve, roc_auc_score, precision_recall_curve
from scipy.stats import ks_2samp
from concurrent import futures
from tqdm import tqdm
from .utils import check_memory

@check_memory()
def describe_col(col: pd.Series) -> pd.Series:
    '''Describe a feature.
    '''
    des = col.describe(percentiles = [.1, .25, .5, .75, .9])
    des['Dtype'] = col.dtype.name
    des['Missing'] = col.isna().sum()
    des['Missing_Rate'] = des['Missing'] / col.size
    
    if 'unique' not in des.index:
        des['unique'] = col.nunique()
    des.index = des.index.map(str.title)
    return des

def divergence(p1: np.ndarray, p2: np.ndarray) -> np.float64:
    dvg = np.sum((p1 - p2) * np.log(p1 / p2))
    return dvg

def _iv(g: np.ndarray) -> np.float64:
    '''Calculate IV based on the binary classification count matrix.
    
    Args:
        g: Grouped count matrix containing only two columns (binary classification).
    
    Returns:
        numpy.float64.
    '''
    if not isinstance(g, np.ndarray):
        g = np.array(g)
    gsum = g.sum(axis = 0)
    gsize = gsum.size
    if gsize == 1 or np.any(gsize == 0):
        return 0
    elif gsize == 2:
        p = g / gsum
        iv = divergence(p[:,0], p[:,1])
        return iv
    else:
        raise ValueError('g is not a binary class count.')

@check_memory()
def iv(cut: pd.Series, flag: pd.Series, group: np.ndarray | pd.Series | None = None) -> np.float64 | pd.Series:
    '''Calculates the Information Value (IV) of a feature. Any count of zero will be replaced with 0.5.
    
    Args:
        cut: A binned feature.
        flag: Binary classification labels.
        group: (Optional) Groups the feature and calculates IV for each group.
    
    Returns:
        A numpy.float64 or a pandas.Series.
    '''
    if group is not None:
        if not isinstance(group, np.ndarray):
            group = np.array(group)
        group = flag.groupby([group, cut.to_numpy(), flag.to_numpy()], sort = False, dropna = False)
        count = group.size().unstack(fill_value = 0.5)
        iv = count.groupby(level = 0).apply(_iv)
        iv.name = cut.name
    else:
        group = flag.groupby(by = [cut.to_numpy(), flag.to_numpy()], sort = False, dropna = False)
        count = group.size().unstack(fill_value = 0.5).to_numpy()
        iv = _iv(count)
    return iv
    
def psi(tcut: pd.Series, bcut: pd.Series) -> np.float64:
    '''Calculate the PSI between the test group and the base group. Proportions of zero will be replaced with 1e-8.
    
    Args:
        tcut: Test group.
        bcut: Base group.
    
    Returns:
        A numpy.float64.
    '''
    fillzero = 1e-8
    basecnt = bcut.value_counts(sort = False, dropna = False)
    baseprop = basecnt / basecnt.sum()
    testcnt = tcut.value_counts(sort = False, dropna = False)
    testprop = testcnt / testcnt.sum()
    baseprop, testprop = baseprop.align(testprop, fill_value = fillzero)
    baseprop.replace(0, fillzero, inplace = True)
    testprop.replace(0, fillzero, inplace = True)
    psi = divergence(baseprop, testprop)
    return psi

@check_memory()
def psi_roll(cuts: list[pd.Series]) -> np.ndarray:
    '''Calculating PSI with a sliding window on list element pairs.
    '''
    psis = []
    for g1, g2 in zip(cuts[:-1], cuts[1:]):
        psis.append(psi(g1, g2))
    psis = np.array(psis)
    return psis

def group_agg(group: np.ndarray) -> dict:
    '''Calculate group-wise metrics from a binary classification count matrix.
    
    Args:
        group: Grouped count matrix containing the count of negatives (0), positives (1), and the total sample size for each group.
    
    Returns:
        A dict.
    '''
    if group.shape[1] != 3:
        raise ValueError(f"Must have exactly three columns.")
    group[np.isnan(group)] = 0
    binscnt = group[:,2]
    flagcnt = group.sum(axis = 0)
    badcnt = group[:,1]
    goodcnt = group[:,0]
    count = flagcnt[2]
    cum_badcnt = badcnt.cumsum()
    cum_goodcnt = goodcnt.cumsum()
    cum_binscnt = binscnt.cumsum()
    
    badprop = np.divide(badcnt, flagcnt[1], out = np.full(badcnt.shape, np.nan, dtype = float), where = flagcnt[1] != 0)
    goodprop = np.divide(goodcnt, flagcnt[0], out = np.full(goodcnt.shape, np.nan, dtype = float), where = flagcnt[0] != 0)
    binsprop = binscnt / count
    cum_badprop = badprop.cumsum()
    cum_goodprop = goodprop.cumsum()
    cum_binsprop = binsprop.cumsum()
    
    badrate = np.divide(badcnt, binscnt, out = np.full(binscnt.shape, np.nan, dtype = float), where = binscnt != 0)
    goodrate = np.divide(goodcnt, binscnt, out = np.full(binscnt.shape, np.nan, dtype = float), where = binscnt != 0)
    cum_badrate = np.divide(cum_badcnt, cum_binscnt, out = np.full(cum_binscnt.shape, np.nan, dtype = float), where = cum_binscnt != 0)
    cum_goodrate = np.divide(cum_goodcnt, cum_binscnt, out = np.full(cum_binscnt.shape, np.nan, dtype = float), where = cum_binscnt != 0)
    
    tot_badrate = flagcnt[1] / count

    lift = np.divide(badrate, tot_badrate, out =  np.full(badrate.shape, np.nan, dtype = float), where = tot_badrate != 0)
    cum_lift = np.divide(cum_badrate, tot_badrate, out = np.full(cum_badrate.shape, np.nan, dtype = float), where = tot_badrate != 0)

    ks_bin = np.abs(cum_badprop - cum_goodprop)
    ks = ks_bin.max()
    
    group_woe = np.where(group[:,:2] == 0, 0.5, group[:,:2])
    flagrat = group_woe / group_woe.sum(axis = 0)
    woe_bin = np.log(flagrat[:,0] / flagrat[:,1])
    iv_bin = (flagrat[:,0] - flagrat[:,1]) * woe_bin
    iv = iv_bin.sum()
    
    res = {'binscnt': binscnt, 'flagcnt': flagcnt[:2], 'badcnt': badcnt, 'goodcnt': goodcnt, 'count': count, 
        'cum_badcnt': cum_badcnt, 'cum_goodcnt': cum_goodcnt, 'cum_binscnt': cum_binscnt, 
        'badprop': badprop, 'goodprop': goodprop, 'binsprop': binsprop, 
        'cum_badprop': cum_badprop, 'cum_goodprop': cum_goodprop, 'cum_binsprop': cum_binsprop, 
        'badrate': badrate, 'goodrate': goodrate, 'cum_badrate': cum_badrate, 'cum_goodrate': cum_goodrate, 'tot_badrate': tot_badrate, 
        'woe_bin': woe_bin, 'iv_bin': iv_bin, 'iv': iv, 'lift': lift, 'cum_lift': cum_lift, 'ks_bin': ks_bin, 'ks': ks}
    return res

@check_memory()
def bins_cnt(cut: pd.Series, flag: pd.Series) -> pd.DataFrame:
    '''Groups and counts the categoryDtype object cut by flag labels. 
    Ordering follows cut; the NaN group is always in the first row.
    
    Args:
        cut: A binned feature.
        flag: Binary classification labels.
    
    Returns:
        A pandas.DataFrame.
    '''
    group = flag.groupby(by = [cut.to_numpy(), flag.to_numpy()], sort = False, dropna = False).size().unstack(fill_value = 0)
    if np.nan in group.index:
        group = group.reindex(cut.cat.categories.insert(0, np.nan))
    else:
        group = group.reindex(cut.cat.categories)
    group = group.reindex([0,1], axis = 1, fill_value = 0)
    group['sum'] = group.sum(axis = 1)
    return group

def bin_agg(cut: pd.Series, flag: pd.Series, init_bin: dict = {}) -> dict:
    '''Count the labels for the grouped features and calculate the metrics for each group.
    
    Args:
        cut: A binned feature.
        flag: Binary classification labels.
        init_bin: The initial statistical information of feature bins in the training set.
    
    Returns:
        A dict.
    '''
    binscnt = bins_cnt(cut, flag)
    bin = init_bin.copy()
    init_split = init_bin.get('split')
    if init_split:
        index = pd.Index(init_split).union(binscnt.index, sort = False)
        binscnt = binscnt.reindex(index, fill_value = 0)
    split = binscnt.index.to_list()
    bin.update({'split': split, 'bin': list(range(len(split)))})
    bin.update(group_agg(binscnt.to_numpy()))
    return bin

def prob2score(prob: float | pd.Series, base_odds: float = 1/35, base_score: float = 1000, pdo: float = 80) -> float | pd.Series:
    '''Convert probabilities to scores based on the specified parameters.
    
    Args:
        prob: Probability values, accepting either a scalar or a Series.
        base_odds: Baseline odds ratio.
        base_score: Score at the baseline odds.
        pdo: Points to Double Odds - score decrease when odds double.

    Returns:
        Same type as the input.
    '''
    factor = -pdo / np.log(2)
    offset = base_score - factor * np.log(base_odds)
    logodds =  np.log(prob / (1 - prob))
    score = offset + factor * logodds
    return score

def score2prob(score: float | pd.Series, base_odds: float = 1/35, base_score: float = 1000, pdo: float = 80) -> float | pd.Series:
    '''Convert scores to probabilities based on the specified parameters.
    
    Args:
        score: Score values, accepting either a scalar or a Series.
        base_odds: Baseline odds ratio.
        base_score: Score at the baseline odds.
        pdo: Points to Double Odds - score decrease when odds double.
    
    Returns:
        Same type as the input.
    '''
    factor = -pdo / np.log(2)
    offset = base_score - factor * np.log(base_odds)
    odds = np.exp((score - offset) / factor)
    prop = odds / (1 + odds)
    return prop

def ks(y_ture: np.ndarray | pd.Series, y_prob: np.ndarray | pd.Series) -> float:
    '''Calculate the KS statistic.

    Args:
        y_true: The true labels of y.
        y_prob: The predicted probability values of y.
    
    Returns:
        A float.
    '''
    ks = ks_2samp(y_prob[y_ture == 1], y_prob[y_ture == 0])
    return float(ks.statistic)

def mod_eva(y_true: np.ndarray | pd.Series, y_pred: np.ndarray | pd.Series, beta: float) -> dict:
    '''Calculate model evaluation metrics for plotting.

    Args:
        y_true: The true labels of y.
        y_prob: The predicted probability values of y.
        beta: Required to calculate the F-statistic.

    Returns:
        A dict.
    '''
    fpr, tpr, p_ks = roc_curve(y_true, y_pred)
    auc_value = auc(fpr, tpr)
    ks = tpr - fpr
    ind_ks_max = np.argmax(ks)
    p_ks_max = p_ks[ind_ks_max]
    ks_max = ks[ind_ks_max]
    beta2 = beta**2
    precision, recall, p_f = precision_recall_curve(y_true, y_pred)
    pmulr = (1 + beta2) * precision * recall 
    paddr = np.ma.masked_values(beta2 * precision + recall, 0)
    f = pmulr / paddr
    ind_f_max = np.argmax(f)
    p_f_max = p_f[ind_f_max]
    f_max = f[ind_f_max]
    return {'auc': auc_value, 'ind_ks_max': ind_ks_max, 'p_ks': p_ks, 'fpr': fpr, 'tpr': tpr, 'ks':ks, 'p_ks_max': p_ks_max, 
            'ks_max': ks_max, 'ind_f_max': ind_f_max, 'p_f': p_f, 'f': f, 'p_f_max': p_f_max, 'f_max': f_max,
            'precision': precision, 'recall': recall}

def eva_metric(y_true: np.ndarray | pd.Series, y_score: np.ndarray | pd.Series, metric: str | list = ['ks', 'auc'], time = None) -> pd.DataFrame:
    '''Calculate model evaluation metrics.

    Args:
        y_true: The true labels of y.
        y_score: Probabilities or scores.
        metric: 'ks' and 'auc' is supported
        time: Group by time and calculate.

    Returns:
        A pandas.DataFrame.
    '''
    if not isinstance(y_true, np.ndarray):
        y_true = np.array(y_true)
    if not isinstance(y_score, np.ndarray):
        y_score = np.array(y_score)
    if not isinstance(metric, list):
        metric = [metric]
    if time is not None and not isinstance(time, np.ndarray):
        time = np.array(time)
    
    res = pd.DataFrame()
    if time is None:
        res.loc[0, 'count'] = y_true.size
        res.loc[0, 'badrate'] = y_true.mean()
        if 'ks' in metric:
            res.loc[0, 'ks'] = ks(y_true, y_score)
        if 'auc' in metric:
            res.loc[0, 'auc'] = roc_auc_score(y_true, y_score)
        res.loc[0, 'score_min'] = y_score.min()
        res.loc[0, 'score_max'] = y_score.max()
        res.loc[0, 'score_mean'] = y_score.mean()
    else:
        for n,d in pd.DataFrame({'y_true': y_true, 'y_score': y_score}).groupby(time):
            res.loc[n, 'count'] = d['y_true'].size
            res.loc[n, 'badrate'] = d['y_true'].mean()
            if 'ks' in metric:
                res.loc[n, 'ks'] = ks(d['y_true'], d['y_score'])
            if 'auc' in metric:
                res.loc[n, 'auc'] = roc_auc_score(d['y_true'], d['y_score'])
            res.loc[n, 'score_min'] = d['y_score'].min()
            res.loc[n, 'score_max'] = d['y_score'].max()
            res.loc[n, 'score_mean'] = d['y_score'].mean()
    res['count'] = res['count'].astype(int)
    return res


def eval_ks(y_true: np.ndarray | pd.Series, y_prob: np.ndarray | pd.Series) -> tuple:
    '''The KS statistic for LightGBM's early stopping function.

    Args:
        y_true: The true labels of y.
        y_prob: The predicted probability values of y.
    
    Returns:
        A tuple. 
    '''
    return 'ks', ks(y_true, y_prob), True

def eval_extreme(y_true: np.ndarray | pd.Series, y_prob: np.ndarray | pd.Series) -> tuple:
    '''The difference in bad rate between the top 20% and bottom 20% of samples for LightGBM's early stopping function.
    
    Args:
        y_true: The true labels of y.
        y_prob: The predicted probability values of y.
    
    Returns:
        A tuple. 
    '''
    ext = 0.2
    obslen = int(y_prob.size * ext)
    if obslen < 1:
        obslen = 1
    ind = np.argsort(y_prob)
    best = y_true[ind[:obslen]].mean()
    worst = y_true[ind[-obslen:]].mean()
    diff = np.abs(worst - best)
    return 'extreme', diff, True