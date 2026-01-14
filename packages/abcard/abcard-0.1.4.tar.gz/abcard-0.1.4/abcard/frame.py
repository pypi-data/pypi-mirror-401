
from io import StringIO
from concurrent import futures
from functools import reduce
from time import perf_counter

import numpy as np
import pandas as pd
import logging
from tqdm import tqdm
from statsmodels.api import OLS, Logit, add_constant
from sklearn.metrics import roc_auc_score

from .stats import describe_col, bins_cnt, group_agg, bin_agg, divergence, psi_roll, iv, ks, eva_metric, prob2score
from .merge import _chi_split, chi2_split, dt_split
from .utils import missdict, TextObjectHandler, tabs_writer

class Frame:
    def __init__(self, flag: str | None = None, time: str | None  = None, exclude: str | list[str] | None = None, catvars: str | list[str] | None = None) -> None:
        """Initial sample set field configuration.
        
        Args:
            flag: Flag for sample category.
            time: Specify the time column for the sample.
            exclude: Exclude non-feature columns.
            catvars: Manually assign categorical features. If None, first tries to convert to float, then to category on failure.
        """
        logFormat = "%(levelname)s %(asctime)s %(name)s: %(message)s"
        logging.basicConfig(level = logging.INFO, format= logFormat)
        self.logger = logging.getLogger(self.__class__.__name__)
        
        self.loginfo = StringIO()
        text_handler = TextObjectHandler(self.loginfo)
        text_handler.setLevel(logging.INFO)
        # text_handler.addFilter(lambda record: record.levelno == logging.INFO)
        text_handler.setFormatter(logging.Formatter(logFormat))
        self.logger.addHandler(text_handler)
        
        self._flag = flag
        self._time = time

        self._exclude = [] if exclude is None else exclude
        if not isinstance(self._exclude, list):
            self._exclude = [self._exclude]
        self._catvars = [] if catvars is None else catvars
        if not isinstance(self._catvars, list):
            self._catvars = [self._catvars]
        
        self._samp_labels = []
        self._drop = {}
        self._config = {}
    
    @property 
    def select(self) -> list[str]:
        '''Returns the remaining features after the drop operation.
        If no features are selected, issue a warning.
        '''
        names = self.feature_names
        select = [i for i in names if i not in self._drop]
        if select == []:
            self.logger.warning('No features selected.')
        return select
    
    @property
    def train_label(self) -> str:
        '''Get first sample set label (training set).
        If no dataset has been set, an error will be thrown.
        '''
        if self._samp_labels:
            return self._samp_labels[0]
        else:
            raise ValueError('Please set the first sample set.')

    @property
    def feature_names(self) -> list[str]:
        '''Get all feature names.
        '''
        names = getattr(self, 'x_' + self.train_label).columns.to_list()
        return names
    
    def check_data(self, data: pd.DataFrame) -> None:
        '''Check the sample set for compliance with the sample setup requirements.
        '''
        if not isinstance(self._flag, str):
            raise TypeError('`flag` must be a string.')
        if self._time is not None and not isinstance(self._time, str):
            raise TypeError('`time` must be a string.')
        if not isinstance(data, pd.DataFrame):
            raise TypeError('`data` must be a pandas DataFrame.')
        if data.shape[0] < 1 or data.shape[1] < 2:
            raise ValueError('`data` shape must be at least (1, 2).')
        if self._flag not in data:
            raise ValueError(f"`data` must contain column {repr(self._flag)}.")
        if set(data[self._flag]) > {0,1}:
            raise ValueError(f"Column {repr(self._flag)} in the `data` must be binary.")
        if self._time is not None and self._time not in data:
            raise ValueError(f"`data` must contain column {repr(self._time)}.")
        if self._samp_labels:
            for i in self.feature_names:
                if i not in data:
                    raise ValueError(f'`data` must contain column {i}.')
    
    def initialize(self, data: pd.DataFrame, label: str, warn: bool = True) -> dict[str, pd.DataFrame | pd.Series]:
        '''Initialize the dataset.
        Feature order aligns with the training set (if exists). 
        
        Args:
            data: Sample dataset.
            label: The label of sample dataset.
            warn: A warning is raised if any training set feature is missing from the dataset.
        
        Returns:
            dict: A dict containing key 'x', along with 'y' and 'time' (if available).
        '''
        self.logger.info(f"Initializing {label} dataset...")

        if self._samp_labels:
            xdata = []
            for i in self.feature_names: # keep features order
                if i in data:
                    if i in self._floatvars:
                        xdata.append(pd.to_numeric(data[i], downcast = 'float'))
                    elif i in self._catvars:
                        xdata.append(data[i].astype('category'))
                elif warn:
                    self.logger.warning(f"Column {i} is not in the `data`.")
            xdata = pd.concat(xdata, axis = 1)
        else:
            floatvars = []
            catvars = []
            xdata = []
            exclude = self._exclude + [self._flag, self._time] if self._time else self._exclude + [self._flag]
            columns = [i for i in data if i not in exclude]
            for c in columns:
                if c in self._catvars:
                    xdata.append(data[c].astype('category'))
                    catvars.append(c)
                else:
                    try:
                        xdata.append(pd.to_numeric(data[c], downcast = 'float'))
                        floatvars.append(c)
                    except:
                        xdata.append(data[c].astype('category'))
                        catvars.append(c)
            xdata = pd.concat(xdata, axis = 1)
            self._floatvars = floatvars
            self._catvars = catvars
        
        res = {'x': xdata}
        if self._flag in data:
            res.update({'y': pd.to_numeric(data[self._flag], downcast = 'signed')})
        if self._time in data:
            res.update({'time': data[self._time].astype('string')})
        return res
    
    def set_samp(self, samp: pd.DataFrame, label: str) -> None:
        '''Set the sample dataset.
        The dataset will be saved in the instance attributes 'x_{samp}', 'y_{samp}' and 'time_{samp}'(if '_time' exists).
        
        Args:
            samp: Sample dataset.
            label: The label of sample dataset.
        '''
        self.check_data(samp)
        data = self.initialize(samp, label = label)
        setattr(self, 'x_' + label, data['x'])
        setattr(self, 'y_' + label, data['y'])
        if self._time:
            setattr(self, 'time_' + label, data['time'])
        self._samp_labels.append(label)

    def del_samp(self, label: str) -> None:
        '''Delete the sample dataset.
        Instance attributes 'x_{samp}', 'y_{samp}' and 'time_{samp}'(if '_time' exists) will be deleted.
        
        Args:
            label: The label of sample dataset.
        '''
        delattr(self, 'x_' + label)
        delattr(self, 'y_' + label)
        if self._time:
            delattr(self, 'time_' + label)
        self._samp_labels.remove(label)
    
    def get_samp(self, label: str) -> dict[str, pd.DataFrame | pd.Series]:
        '''Get the sample dataset.
        If the specified sample set does not exist, it returns None.
        
        Args:
            label: The label of sample dataset.
        
        Returns:
            dict: A dict containing key 'x', along with 'y' and 'time' (if available).
        '''
        res = {}
        if label in self._samp_labels:
            res.update({'x': getattr(self, 'x_' + label)})
            res.update({'y': getattr(self, 'y_' + label)})
            if self._time:
                res.update({'time': getattr(self, 'time_' + label)})
            return res
    
    def describe_sample(self) -> pd.DataFrame | dict[str, pd.DataFrame]:
        '''Descriptive analysis of samples.
        The result will be saved in the instance attribute '_describe_sample'.

        Returns:
            A dict if a time column is present; otherwise, a pandas DataFrame.
        '''
        if self._time:
            table = {}
            for label in self._samp_labels:
                flag = getattr(self, 'y_' + label)
                tim = getattr(self, 'time_' + label).to_numpy()
                tab = flag.groupby(tim).agg(['size', 'sum', 'mean'])
                tot = pd.DataFrame([flag.agg(['size', 'sum', 'mean'])], index = ['total'])
                if len(set(tim)) > 1:
                    tab = pd.concat([tab, tot])
                tab.columns = ['count', 'badcnt', 'badrate']
                tab.insert(1, 'goodcnt', tab['count'] - tab['badcnt'])
                tab[['count', 'goodcnt', 'badcnt']] = tab[['count', 'goodcnt', 'badcnt']].astype(int)
                tab.index.name = label
                table[label] = tab
        else:
            table = []
            for label in self._samp_labels:
                flag = getattr(self, 'y_' + label)
                table.append(pd.DataFrame([flag.agg(['size', 'sum', 'mean'])], index = [label]))
            if len(table) > 1:
                table = pd.concat(table)
                table.iloc['total', 'size'] = table['size'].sum()
                table.iloc['total', 'sum'] = table['sum'].sum()
                table.iloc['total', 'mean'] = table.iloc['total', 'sum'] / table.iloc['total', 'size']
            elif len(table) == 1:
                table = table[0]
            table.columns = ['count', 'badcnt', 'badrate']
            table.insert(1, 'goodcnt', table['count'] - table['badcnt'])
            table[['count', 'goodcnt', 'badcnt']]= table[['count', 'goodcnt', 'badcnt']].astype(int)
        self._describe_sample = table
        return table
        
    def describe_feature(self) -> pd.DataFrame:
        '''Descriptive analysis of fearures.
        The result will be saved in the instance attribute '_describe_feature'.

        Returns:
            A pandas DataFrame indexed by feature names.
        '''
        self.logger.info("Describing features...")
        res = []
        index = ['Dtype', 'Count', 'Missing', 'Missing_Rate', 'Unique']
        
        if len(self._floatvars) > 0:
            index += ['Mean', 'Std', 'Min', '10%', '25%', '50%', '75%', '90%', 'Max']
        if len(self._catvars) > 0:
            index += ['Top', 'Freq']
        x_train = getattr(self, 'x_' + self.train_label)
        for c,s in tqdm(x_train.items(), total = x_train.shape[1]):
            res.append(describe_col(s))
        result = pd.DataFrame(res).reindex(columns = index)
        result.index.name = 'Features'
        result.reset_index(inplace = True)
        result.index.name = 'Ind'
        self._describe_feature = result
        return result
    
    def chi2_split(self, chi2value: float = 3.841, pvalue: float = 0.05, forced_correction: bool = False, minbin: float | int = 0.05, 
                maxbins: None | int = None, woediff: float = 0.05, prebins: int = 1000, mergena: bool = False, cores = 1) -> None:
        '''Perform chi-square binning on all features.
        The result will be saved in the instance attribute '_cuts' and '_bins'. 
            '_cuts' is a DataFrame composed of binned categories for all features. 
            '_bins' is a dict consisting of feature names and their related binning statistics.
        
        Args:
            chi2value: Chi-square test threshold. The default is 3.841.
            pvalue: Significance threshold corresponding to the chi-square test threshold. The default is 0.05.
            forced_correction: Whether to force the use of the chi-square correction formula. 
                When forced correction is applied, binning is based on chi2value; otherwise, it is based on pvalue. The default is False.
            minbin: Minimum sample size per bin. If a decimal between 0 and 1, it represents the proportion of the sample size that is non-NaN values. The default is 0.05.
            maxbins: Maximum number of bins (excluding the NaN bin). The default is None.
            woediff: Merge adjacent bins if the absolute difference in WOE is less than this value after chi-square binning. The default is 0.05.
            prebins: Number of pre-bins. If the number of distinct values exceeds this, pre-binning will be performed based on percentiles of distinct values, 
                which can improve binning speed for variables with many distinct values. The default is 1000.
            mergena: If True, NaN bins will be automatically merged with other bins when merging conditions are satisfied.
            cores: Number of CPU cores to use.
        '''
        split_config = {'chi2value':chi2value, 'pvalue':pvalue, 'forced_correction':forced_correction, 'minbin':minbin, 
                        'maxbins':maxbins, 'woediff':woediff, 'prebins':prebins, 'mergena':mergena}
        text_config = ', '.join([f"{k}={v}" for k,v in split_config.items()])
        self.logger.info(f"Features binning using chi2_split({text_config})...")
        self._config.update({'split':{'method':'chi2', **split_config}})
        cuts = []
        self._bins = dict()
        x_train = getattr(self, 'x_' + self.train_label)
        y_train = getattr(self, 'y_' + self.train_label)
        if cores > 1:
            with futures.ProcessPoolExecutor(max_workers= cores) as executor:
                to_do = []
                for c,s in x_train.items():
                    future = executor.submit(chi2_split, feature = s, flag = y_train, chi2value = chi2value, pvalue = pvalue, 
                            forced_correction = forced_correction, minbin = minbin, maxbins = maxbins, woediff = woediff, 
                            prebins = prebins, mergena = mergena)
                    to_do.append(future)
                for f in tqdm(futures.as_completed(to_do), total = len(to_do)):
                    cut, bins = f.result()
                    cuts.append(cut)
                    self._bins.update({cut.name: bins})
        else:
            for c,s in tqdm(x_train.items(), total = x_train.shape[1]):
                cut, bins = chi2_split(s, y_train, chi2value = chi2value, pvalue = pvalue, forced_correction = forced_correction, 
                    minbin = minbin, maxbins = maxbins, woediff = woediff, prebins = prebins, mergena = mergena)
                cuts.append(cut)
                self._bins.update({c: bins})
        
        self._cuts = pd.concat(cuts, axis = 1).reindex(columns = x_train.columns)

    def dt_split(self, minbin: float | int = 0.05, maxbins: None | int = None, cores = 1) -> None:
        '''Perform decision tree binning on all features.
        The result will be saved in the instance attribute '_cuts' and '_bins'. 
            '_cuts' is a DataFrame composed of binned categories for all features. 
            '_bins' is a dict consisting of feature names and their related binning statistics.
        
        Args:
            minbin: Minimum sample size per bin. If a decimal between 0 and 1, it represents the proportion of the sample size that is non-NaN values. The default is 0.05.
            maxbins: Maximum number of bins (excluding the NaN bin). The default is None.
            cores: Number of CPU cores to use.
        '''
        split_config = {'minbin':minbin, 'maxbins':maxbins}
        text_config = ', '.join([f"{k}={v}" for k,v in split_config.items()])
        self.logger.info(f"Features binning using dt_split({text_config})...")
        self._config.update({'split':{'method':'dt', **split_config}})
        cuts = []
        self._bins = dict()
        x_train = getattr(self, 'x_' + self.train_label)
        y_train = getattr(self, 'y_' + self.train_label)
        if cores > 1:
            with futures.ProcessPoolExecutor(max_workers= cores) as executor:
                to_do = []
                for c,s in x_train.items():
                    future = executor.submit(dt_split, feature = s, flag = y_train, minbin = minbin, maxbins = maxbins)
                    to_do.append(future)
                for f in tqdm(futures.as_completed(to_do), total = len(to_do)):
                    cut, bins = f.result()
                    cuts.append(cut)
                    self._bins.update({cut.name: bins})
        else:
            for c,s in tqdm(x_train.items(), total = x_train.shape[1]):
                cut, bins = dt_split(s, y_train, minbin = minbin, maxbins = maxbins)
                cuts.append(cut)
                self._bins.update({c: bins})
        
        self._cuts = pd.concat(cuts, axis = 1).reindex(columns = x_train.columns)

    def nan_by_time(self) -> pd.DataFrame:
        '''Calculate the missing rate of features by time.

        Returns:
            A pandas DataFrame.
        '''
        self.logger.info("Calculating the missing rate of features by time...")
        x_train = getattr(self, 'x_' + self.train_label)
        time_train = getattr(self, 'time_' + self.train_label)
        group = x_train.groupby(by = time_train.to_numpy())

        nan_rat = {}
        for c in x_train.columns:
            rats = {}
            for t, v in group[c]:
                rats[t] = v.isna().sum() / v.size
            nan_rat[c] = rats
        res = pd.DataFrame.from_dict(nan_rat, orient = 'index').sort_index(axis = 1)
        res.index.name = 'nan_by_time'
        return res
        
    def iv(self, samp: str, cores: int = 1) -> None:
        '''Calculate IV (Information Value) for all features in samp.
        The result will be saved in the instance attribute '_iv_{samp}', a pandas Series.
        
        Args:
            samp: Sample label.
            cores: Number of CPU cores to use.
        '''
        train_label = self.train_label
        ivs = {}
        if samp == train_label:
            for k,v in self._bins.items():
                ivs[k] = v['iv']
        else:
            cuts = self.transform(samp)
            self.logger.info(f"Calculating the IV for features in {samp}...")
            flag = getattr(self, 'y_' + samp)
            if cores > 1:
                with futures.ProcessPoolExecutor(max_workers = cores) as executor:
                    to_do = {}
                    for k,v in cuts.items():
                        future = executor.submit(iv, v, flag)
                        to_do[future] = k
                    for f in tqdm(futures.as_completed(to_do), total = len(to_do)):
                        ivs[to_do[f]] = f.result()
            else:
                for k,v in tqdm(cuts.items(), total = cuts.shape[1]):
                    ivs[k] = iv(v, flag)
        ivs = pd.Series(ivs).sort_values(ascending = False)
        setattr(self, f"_iv_{samp}", ivs)
    
    def iv_by_time(self, cores: int = 1) -> None:
        '''Calculate IV (Information Value) for all features grouped by time.
        The result will be saved in the instance attribute '_iv_by_time', a pandas DataFrame.
        
        Args:
            cores: Number of CPU cores to use.
        '''
        train_label = self.train_label
        flag_train = getattr(self, 'y_' + train_label)
        time_train = getattr(self, 'time_' + train_label)
        if time_train.nunique() < 2:
            raise ValueError('All values of time in the {train_label} are the same.')

        self.logger.info("Calculating the IV for features by time...")
        
        res = []
        if cores > 1:
            time_train = time_train.to_numpy()
            with futures.ProcessPoolExecutor(max_workers= cores) as executor:
                to_do = []
                for k,v in self._cuts.items():
                    future = executor.submit(iv, cut = v, flag = flag_train, group = time_train)
                    to_do.append(future)
                for f in tqdm(futures.as_completed(to_do), total = len(to_do)):
                    res.append(f.result())
        else:
            for k,v in tqdm(self._cuts.items(), total = self._cuts.shape[1]):
                t_iv = iv(cut = v, flag = flag_train, group = time_train)
                res.append(t_iv)
        res = pd.DataFrame(res).sort_index(axis = 1)
        res.index.name = 'iv_by_time'
        setattr(self, '_iv_by_time', res)
    
    def psi(self, tcut: pd.Series, bcut: None | pd.Series = None) -> np.float64:
        '''Calculate population stability index for a feature.
        If bcut is specified, calculate PSI between tcut and bcut; if not specified, calculate PSI between tcut and the binned training feature with the same name."
        
        Args:
            tcut: The binned category series of test.
            bcut: The binned category series of base.
        
        Returns:
            A numpy.float64.
        '''
        if not isinstance(tcut.dtype, pd.CategoricalDtype) or (bcut is not None and not isinstance(bcut.dtype, pd.CategoricalDtype)):
            raise TypeError('Both `tcut` and `bcut` must be pandas Series of categorical dtype.')
        if bcut is None:
            bins = self._bins.get(tcut.name)
            baseprop = pd.Series(bins['binsprop'], index = bins['split'])
        else:
            basecnt = bcut.value_counts(sort = False, dropna = False)
            baseprop = basecnt / basecnt.sum()
        testcnt = tcut.value_counts(sort = False, dropna = False)
        testprop = testcnt / testcnt.sum()
        baseprop, testprop = baseprop.align(testprop, fill_value = 1e-8)
        baseprop.replace(0, 1e-8, inplace = True)
        testprop.replace(0, 1e-8, inplace = True)
        psi = divergence(baseprop, testprop)
        return psi
    
    def psi_with_samp(self, samp: str | pd.DataFrame) -> None:
        '''Calculate the PSI (Population Stability Index) between training set features and other dataset features.
        The result will be saved in the instance attribute '_psi_with_{samp}', a pandas DataFrame.
        
        Args:
            samp: Sample label or pandas DataFrame.
        '''
        trans = self.transform(samp = samp, woe = False)
        label = samp if isinstance(samp, str) else 'specified'
        self.logger.info(f"Calculating the PSI for features between sample {self.train_label} and {label}...")
        res = trans.apply(self.psi)
        res.name = 'psi_with_' + label
        setattr(self, '_' + res.name, res)
    
    def psi_by_time(self, cores: int = 1):
        '''Calculate the PSI (Population Stability Index) for all features grouped by time.
        The result will be saved in the instance attribute '_psi_by_time', a pandas DataFrame.
        
        Args:
            cores: Number of CPU cores to use.
        '''
        train_label = self.train_label
        time_train = getattr(self, 'time_' + train_label)
        if time_train.nunique() < 2:
            raise ValueError('All values of time in the {train_label} are the same.')
        
        self.logger.info("Calculating the PSI for features by time...")
        group = self._cuts.groupby(by = time_train.to_numpy(), sort = True)
        res = {}
        if cores > 1:
            with futures.ProcessPoolExecutor(max_workers= cores) as executor:
                to_do = {}
                for c in self._cuts.columns:
                    s_list = [g for _, g in group[c]]
                    future = executor.submit(psi_roll, cuts = s_list)
                    to_do[future] = c
                for f in tqdm(futures.as_completed(to_do), total = len(to_do)):
                    res[to_do[f]] = f.result()
        else:
            for c in tqdm(self._cuts.columns, total = self._cuts.shape[1]):
                s_list = [g for _, g in group[c]]
                res[c] = psi_roll(s_list)
        res = pd.DataFrame.from_dict(res, orient = 'index')
        res.index.name = 'psi_by_time'
        setattr(self, '_psi_by_time', res)
    
    def vif(self, data: pd.DataFrame) -> None:
        '''Calculate VIF (Variance Inflation Factor) for each feature in the dataset. 
        Uses the OLS class from statsmodels.api to build multiple linear regression models (including intercept term).
        The result will be saved in the instance attribute '_vif', a pandas Series.
        '''
        colnames = data.columns.to_list()
        data = data.to_numpy()
        self.logger.info("Calculating the VIF for the dataset...")
        val = []
        for i in tqdm(range(data.shape[1])):
            X = np.delete(data, i, axis = 1)
            X = add_constant(X)
            y = data[:, i]
            vifname = colnames[i]
            if np.all(y == 0):
                self.logger.warning(f"All values in {colnames[i]} is zero, VIF will be set to np.inf.")
                self._bins[vifname].update({'vif': np.inf})
                continue
            mod = OLS(y, X)
            res = mod.fit()
            val.append(1/(1-res.rsquared))
        res = pd.Series(val, index = colnames, name = 'vif')
        setattr(self, '_vif', res)
    
    def mergebins(self, var: str, start: int, end: int, woe: None | pd.DataFrame = None) -> None:
        '''Merge bins manually.
        The feature's results in instance attributes '_cuts' and '_bins' will be updated. 
        If the instance already has '_psi_with_{samp}', '_psi_by_time', or '_vif', these will also be updated. 
        
        Args:
            var: Feature name. 
            start: Starting index of bins to merge (0-based).
            end: Ending index of bins to merge.
            woe: Training set WOE for updating the feature's VIF.
        '''
        train_label = self.train_label
        if var not in getattr(self, 'x_' + train_label):
            raise ValueError(f"Column {var} must be present in the {train_label} dataset.")
        if start < 0 or end - start < 0:
            raise ValueError(f"`start` must be a non-negative integer and `end` must be greater than `start`.")
        if 'vif' in self._bins[var] and woe is None:
            raise ValueError(f"Please provide the `woe` DataFrame in order to update the VIF.")
        
        self.logger.info("Merging bins manually...")
        split = self._bins.get(var).get('split').copy()
        wait = split[start + 1:end + 1] if pd.isna(split[start]) else split[start:end + 1]
        if isinstance(wait[0], pd.Interval):
            merge = pd.Interval(left = wait[0].left, right = wait[-1].right, closed = wait[0].closed)
        else:
            merge = reduce(tuple.__add__, wait)
        split2 = split[:start] + [merge] + split[end + 1:]
        split3 = split2[1:] if pd.isna(split2[0]) else split2
        newcat = {}
        if pd.isna(split[start]):
            newcat = {-1: merge}
            newcat.update({i: v for i, v in enumerate(split[1:])})
            newcat.update({i: merge for i in range(start, end)})
        else:
            if pd.isna(split2[0]):
                newcat = {i:v for i, v in enumerate(split[1:])}
                newcat.update({i: merge for i in range(start - 1, end)})
            else:
                newcat = {i:v for i, v in enumerate(split)}
                newcat.update({i: merge for i in range(start, end + 1)})
        cut = self._cuts[var].cat.codes.map(newcat).astype(pd.CategoricalDtype(categories = split3, ordered = True))
        cut.name = var
        self._cuts[var] = cut
        self.logger.info("  Attribute '_cuts' updated.")
        if pd.isna(split[start]):
            self._bins[var].update({'fillnan': merge, 'fillnum': getattr(self, 'x_' + train_label)[var].isna().sum()})
        else:
            fillnan = self._bins[var].get('fillnan')
            if fillnan is not None:
                nanidx = split.index(fillnan)
                if nanidx >= start and nanidx <= end:
                    self._bins[var]['fillnan'] = merge
        
        binscnt = bins_cnt(cut, getattr(self, 'y_' + train_label))
        self._bins[var].update({'split': split2, 'bin': list(range(len(binscnt)))})
        self._bins[var].update(group_agg(binscnt.to_numpy()))
        self.logger.info("  Attribute '_bins' updated.")
        
        for s in self._samp_labels:
            psi_label = '_psi_with_' + s
            if hasattr(self, psi_label):
                ts = self.tobins(feature = getattr(self, 'x_' + s)[var])
                psi = self.psi(ts)
                getattr(self, psi_label)[var] = psi
                self.logger.info(f"  Attribute {repr(psi_label)} updated.")
        
        if hasattr(self, '_psi_by_time'):
            time_train = getattr(self, 'time_' + train_label)
            if time_train.nunique() < 2:
                raise ValueError('all values of time in the {train_label} are the same.')
            group = cut.groupby(by = time_train.to_numpy(), sort = True)
            s_list = [g for _, g in group]
            psit = psi_roll(s_list)
            getattr(self, '_psi_by_time').loc[var] = psit
            self.logger.info("  Attribute '_psi_by_time' updated.")
        
        if hasattr(self, '_vif'):
            woe[var] = self.bins2woe(cut)
            colnames = woe.columns.to_list()
            i = colnames.index(var)
            data = woe.to_numpy()

            X = np.delete(data, i, axis = 1)
            X = add_constant(X)
            y = data[:, i]
            if np.all(y == 0):
                self.logger.warning(f"All values in {var} is zero, VIF will be set to np.inf.")
                getattr(self, '_vif')[var] = np.inf
            else:
                mod = OLS(y, X)
                res = mod.fit()
                vifvalue = 1/(1-res.rsquared)
                getattr(self, '_vif')[var] = vifvalue
            self.logger.info("  Attribute '_vif' updated.")

    def tobins(self, feature: pd.Series, autofill = True, retnfill = False) -> pd.Series | tuple[pd.Series, dict]:
        '''Convert features to bins.
        
        Args:
            autofill: Whether to fill nan values with bin that can be merged into.
            retfill: Whether to return a dict which contains keys 'fillnan' and 'fillnum', if autofill = False return {} anyway.
                fillnan is the bin into which NaN values are merged, fillnum is the count of merged NaN values.
        
        Returns:
            A pandas Series of category dtype, or a tuple consisting of such a Series and a dict.
        '''
        train_label = self.train_label
        if feature.name not in self.feature_names:
            raise ValueError(f'Feature {feature.name} is not in the {train_label} dataset.')
        
        if feature.name in self._floatvars:
            if not pd.api.types.is_float_dtype(feature):
                feature = pd.to_numeric(feature, downcast = 'float')
        else:
            feature = feature.astype('category')
        isna = feature.isna()
        if getattr(self, 'x_' + train_label)[feature.name].notna().all() and isna.any():
            self.logger.warning(f"Feature {feature.name} has nan values that are not in the {train_label} dataset.")
        
        bin = self._bins.get(feature.name)
        split = bin['split'].copy()
        fillnan = bin.get('fillnan')
        
        iscat = isinstance(feature.dtype, pd.CategoricalDtype)
        split2 = split[1:] if pd.isna(split[0]) else split
        
        if iscat: 
            newcat = missdict({np.nan: fillnan if autofill else np.nan})
            newcat.update({i:v for v in split2 for i in v})
            cut = feature.astype(object).map(newcat).astype('category')

            diff = set(cut.cat.categories).difference(set(split2))
            if len(diff) > 0:
                split2 += list(diff)
                self.logger.warning(f"Feature {feature.name} has values that are not in the {train_label} dataset, these values will be binned to ('_NotFound_',).")
            cut = cut.cat.set_categories(split2, ordered = True)
        else:
            if len(split2) > 0:
                split2 = [split2[0].left] + [i.right for i in split2]
                cut = pd.cut(feature, split2, include_lowest= True, precision = 8)
                if autofill and fillnan is not None:
                    cut.fillna(fillnan, inplace = True)
            else:
                self.logger.warning(f"Feature {feature.name} is all nan values in the {train_label} dataset, other values will be binned to '[-inf, inf]'.")
                cut = feature.copy()
                cut[~isna] = pd.Interval(-np.inf, np.inf, closed = 'both')
                cut = cut.astype('category').cat.as_ordered()
        
        if retnfill:
            filled = {}
            if autofill and fillnan is not None:
                filled = {'fillnan': fillnan, 'fillnum': isna.sum()}
            return cut, filled
        return cut
    
    def bins2woe(self, cut: pd.Series, miss_fill = 0) -> pd.Series:
        '''Convert a binned feature to WOE values.
        
        Args:
            cut: A single feature that has been binned.
            miss_fill: Determines the WOE value of the missing value.
                <0: Use the minimum WOE among all bins.
                =0: Use 0 as the WOE.
                >0: Use the maximum WOE among all bins.
        
        Returns:
            a pandas Series.
        '''
        bin = self._bins.get(cut.name)
        split = bin['split'].copy()
        woe_bin = bin['woe_bin']
        
        if pd.isna(split[0]):
            woedict = {-1: woe_bin[0]}
            woedict.update({i: v for i,v in enumerate(woe_bin[1:])})
        else:
            woedict = {i: v for i,v in enumerate(woe_bin)}
        
        woe = cut.cat.codes.map(woedict)
        if miss_fill == 0:
            miss_val = 0
        elif miss_fill < 0:
            miss_val = max(woe_bin)
        else:
            miss_val = min(woe_bin)
        woe.fillna(miss_val, inplace = True)
        woe.name = cut.name
        return woe
    
    def binstats(self) -> pd.DataFrame:
        '''Convert the dict form binning indicators of _bins into a pandas DataFrame.
        
        Returns:
            a pandas DataFrame.
        '''
        fts_bins = []
        for k,v in self._bins.items():
            bins_dict = {}
            for i in ['bin', 'split', 'binscnt', 'badcnt', 'goodcnt', 'count', 'cum_badcnt', 'cum_goodcnt', 'cum_binscnt', 
                      'badprop', 'goodprop', 'binsprop', 'cum_badprop', 'cum_goodprop', 'cum_binsprop', 
                      'badrate', 'goodrate', 'tot_badrate', 'cum_badrate', 'cum_goodrate', 
                      'woe_bin', 'iv_bin', 'iv', 'lift', 'cum_lift', 'ks_bin', 'ks']:
                bins_dict.update({i: v[i]})
            fts_bins.append(pd.DataFrame(bins_dict, index = [k] * len(v['bin'])))
        fts_bins = pd.concat(fts_bins, axis = 0)
        fts_bins.index.name = 'Features'
        fts_bins.sort_values(['ks', 'bin'], ascending = [False, True], inplace = True)
        return fts_bins

    def transform(self, samp: str | pd.DataFrame, woe: bool = False, retnfill: bool = False, miss_fill: int = 0, warn: bool = True
                  ) -> pd.DataFrame | tuple[pd.DataFrame, dict]:
        '''Convert the sample set into bins or WOE.
        
        Args:
            samp: Sample label or pandas DataFrame.
            woe: Whether to convert the sample set to WOE. False indicates conversion to bins.
            retnfill: Whether to return the NaN value merging information for features. For details, refer to the 'tobins' method.
            miss_fill: Determines the WOE value of the missing value, just for WOE transfromation. 
                <0: Use the minimum WOE among all bins.
                =0: Use 0 as the WOE.
                >0: Use the maximum WOE among all bins.
            warn: Whether to issue a warning if any features are missing.
        
        Returns:
            A pandas DataFrame of category dtypes, or a tuple consisting of such a pandas DataFrame and a dict.
        '''
        filled = {}
        if isinstance(samp, str):
            if samp == self.train_label:
                trans = self._cuts
            else:
                attr_x = 'x_' + samp
                if not hasattr(self, attr_x):
                    raise ValueError('samp does not exist.')
                samp = getattr(self, attr_x)
                trans = []
                self.logger.info(f'Transforming {attr_x} with woe = {woe} and miss_fill = {miss_fill}...')
                for c, s in samp.items():
                    if retnfill:
                        cut, fill = self.tobins(s, retnfill = retnfill)
                        trans.append(cut)
                        filled.update({c: fill})
                    else:
                        trans.append(self.tobins(s))
                trans = pd.concat(trans, axis = 1)
        elif isinstance(samp, pd.DataFrame):
            samp = self.initialize(samp, label = 'the specified', warn = warn).get('x')
            trans = []
            self.logger.info(f'Transforming the specified dataset with woe = {woe} and miss_fill = {miss_fill}...')
            for c, s in samp.items():
                if retnfill:
                    cut, fill = self.tobins(s, retnfill = retnfill)
                    trans.append(cut)
                    filled.update({c: fill})
                else:
                    trans.append(self.tobins(s))
            trans = pd.concat(trans, axis = 1)
        else:
            raise TypeError('Unsupported type for parameter `samp`.')
        
        if woe:
            trans2woe = []
            for c, s in trans.items():
                trans2woe.append(self.bins2woe(cut = s, miss_fill = miss_fill))
            trans2woe = pd.concat(trans2woe, axis = 1)
            if retnfill:
                return trans2woe, filled
            return trans2woe
        else:
            if retnfill:
                return trans, filled
            return trans
    
    def binsagg(self, cuts: pd.DataFrame, flag: pd.Series, init_bins: dict = {}, cores: int = 1) -> dict: 
        '''Calculate grouped statistical metrics for given binned features and flag.
        
        Args:
            cuts: A pandas DataFrame of binned features.
            flag: A pandas Series of binary int values.
            init_bins: if a feature have already been binned with autofill = True, the split used for binning should be provided, along with the fillnan and fillnum.
            cores: Number of CPU cores to use.
        '''
        self.logger.info("Calculating binning statistics...")
        bins = {}
        if cores > 1:
            with futures.ProcessPoolExecutor(max_workers = cores) as executor:
                to_do = {}
                for c,s in cuts.items():
                    init_bin = init_bins.get(c)
                    future = executor.submit(bin_agg, s, flag, init_bin)
                    to_do[future] = c
                for f in tqdm(futures.as_completed(to_do), total = len(to_do)):
                    bin = f.result()
                    name = to_do[f]
                    bins.update({name: bin})
        else:
            for c,s in cuts.items():
                init_bin = init_bins.get(c)
                bin = bin_agg(s, flag, init_bin)
                bins.update({c: bin})
        return bins

    def reset_drop(self, reason: str) -> None:
        '''Clean up the drop reason for the dropped features. 
        Instance attributes '_drop' and '_config' will be updated.
        
        Args:
            reason: drop reason.
        '''
        drop_config = self._config.get("drop")
        if drop_config:
            drop_config.pop(reason, None)

        dropfts = []
        for k, v in self._drop.items():
            if reason in v:
                v.pop(reason, None)
                if not v:
                    dropfts.append(k)
        for i in dropfts:
            self._drop.pop(i)
        self.logger.info(f"reset_drop(reason={repr(reason)}) completed.")
    
    def drop_manually(self, features: str | list[str], reason: str = 'specified') -> None:
        '''Manually add a drop reason for features.
        Instance attribute '_drop' will be updated.
        
        Args:
            features: Features to add drop reason.
            reason: drop reason.
        '''
        if not isinstance(features, list):
            features = [features]

        self.reset_drop(reason = reason)
        
        if 'drop' in self._config:
            self._config['drop'].update({reason: 'manually'})
        else:
            self._config.update({'drop': {reason: 'manually'}})
        
        self.logger.info(f"Dropping {reason} manually ...")
        for var in features:
            self.logger.info(f"  Drop {var} manually as {reason} .")
            if var not in self._drop:
                self._drop.update({var: {reason: 'manually'}})
            else:
                self._drop[var].update({reason: 'manually'})

    def drop_nan(self, nan: float | None = None) -> None:
        '''Drop features based on the proportion of None values.
        Instance attribute '_drop' will be updated.
        
        Args:
            nan: Features whose None values exceed that proportion are removed, drop nothing if None.
        '''
        reason = 'nan'
        if nan:
            if nan >= 0 and nan < 1:
                self.reset_drop(reason = reason)
            else:
                raise ValueError('`nan` must be in [0,1).')
        else:
            self.reset_drop(reason = reason)
            return None
        
        if 'drop' in self._config:
            self._config['drop'].update({'nan': nan})
        else:
            self._config.update({'drop': {'nan': nan}})
        
        if not hasattr(self, '_describe_feature'):
            self.describe_feature()
        self.logger.info(f"Dropping nan > {nan} ...")
        drop = self._describe_feature.loc[self._describe_feature['Missing_Rate'] > nan, ['Features', 'Missing_Rate']]
        for r,s in drop.iterrows():
            var, missrate = s['Features'], s['Missing_Rate']
            self.logger.info(f"  Drop {var} as {reason} = {missrate}.")
            if var not in self._drop:
                self._drop.update({var: {reason: missrate}})
            else:
                self._drop[var].update({reason: missrate})

    def drop_nan_by_time(self, nan: float | None = None, range: float | None = None) -> None:
        '''Drop features based on the max and range of their missing-value ratio across time intervals.
        Instance attribute '_drop' will be updated.

        Args:
            nan: Features whose None values exceed that proportion are removed, drop nothing if None.
            range: A feature is removed if the range of its NaN proportion exceeds this value, drop nothing if None.
        '''
        reason = 'nan_by_time'
        if nan or range:
            if (nan and nan >= 0 and nan < 1) or (range and range >= 0 and range < 1):
                self.reset_drop(reason = reason)
            else:
                raise ValueError('Both `nan` and `range` must be in [0,1).')
        else:
            self.reset_drop(reason = reason)
            return None
        
        if 'drop' in self._config:
            self._config['drop'].update({reason: nan})
        else:
            self._config.update({'drop': {reason: nan}})
        
        nan_rat = self.nan_by_time()
        self.logger.info(f"Dropping nan_by_time with nan = {nan} and range = {range}...")

        for c, v in nan_rat.iterrows():
            max_nan = v.max()
            extreme = v.max() - v.min()
            text = []
            if max_nan > nan:
                text.append(f"max(nan)={round(max_nan, 2)}")
            if extreme > range:
                text.append(f"range(nan)={round(extreme, 2)}")
            if len(text) > 0:
                text = ' and '.join(text)
                self.logger.info(f"  Drop {c} as {text}.")
                if c not in self._drop:
                    self._drop.update({c: {reason: text}})
                else:
                    self._drop[c].update({reason: text})
    
    def drop_bin_count(self) -> None:
        '''Features whose bins number are just one are removed.
        Instance attribute '_drop' will be updated.
        '''
        reason = 'bin_count'
        self.reset_drop(reason = reason)
        
        if 'drop' in self._config:
            self._config['drop'].update({reason: 1})
        else:
            self._config.update({'drop': {reason: 1}})
        
        self.logger.info(f"Dropping features with only one bin...")
        for k,v in self._bins.items():
            if len(v['bin']) == 1:
                self.logger.info(f"  Drop {k} as {reason} = 1.")
                if k not in self._drop:
                    self._drop.update({k: {reason: 1}})
                else:
                    self._drop[k].update({reason: 1})
    
    def drop_iv(self, samp: str, iv: float | None = None, cores = 1) -> None:
        '''Drop features based on IV values.
        Instance attribute '_drop' will be updated.
        
        Args:
            samp: Sample label.
            iv: Features with an IV less than this value are removed, drop nothing if None or < 0.
        '''
        reason = f"iv_{samp}"
        if iv:
            if iv > 0:
                self.reset_drop(reason = reason)
            else:
                raise ValueError('`iv` must be > 0.')
        else:
            self.reset_drop(reason = reason)
            return None
        
        if 'drop' in self._config:
            self._config['drop'].update({reason: iv})
        else:
            self._config.update({'drop': {reason: iv}})
        
        if not hasattr(self, f"_iv_{samp}"):
            self.iv(samp = samp, cores = cores)
        self.logger.info(f"Dropping features with IV < {iv} from the sample...")

        iv_samp = getattr(self, f"_iv_{samp}")
        for k,v in iv_samp.items():
            if v < iv:
                self.logger.info(f"  Drop {k} as IV = {v} in the {samp} dataset.")
                if k not in self._drop:
                    self._drop.update({k: {reason: float(v)}})
                else:
                    self._drop[k].update({reason: float(v)})
    
    def drop_iv_decline(self, samp: str, decline: float | None = -1.0, cores: int = 1) -> None:
        '''Drop features whose IV values decline significantly between training and `samp`.
        The IV values will be saved in the instance attribute '_iv_{samp}', a pandas Series.
        Instance attribute '_drop' will be updated. 
        
        Args:
            samp: Sample label.
            decline: A feature will be dropped if its IV value decline is greater than this threshold, drop nothing if None or >= 0.
        '''
        reason = 'iv_decline'
        if decline:
            if decline < 0:
                self.reset_drop(reason = reason)
            else:
                raise ValueError('`decline` must be < 0.')
        else:
            self.reset_drop(reason = reason)
            return None
        if 'drop' in self._config:
            self._config['drop'].update({reason: decline})
        else:
            self._config.update({'drop': {reason: decline}})
        
        self.iv(samp = self.train_label)
        if not hasattr(self, f"_iv_{samp}"):
            self.iv(samp = samp, cores = cores)

        iv_train = getattr(self, f"_iv_{self.train_label}")
        iv_samp = getattr(self, f"_iv_{samp}")
        self.logger.info(f"Dropping IV declines < {decline} in {samp}...")

        diff = (iv_samp - iv_train)/iv_samp
        for k, v in diff.items():
            if v < decline:
                self.logger.info(f"  Drop {k} as IV declines in {samp} = {v}.")
                if k not in self._drop:
                    self._drop.update({k: {reason: v}})
                else:
                    self._drop[k].update({reason: v})

    def drop_iv_by_time(self, iv_min: float | None = None, iv_mean: float | None = None, period: int | list[int, int] | None = None, cores: int = 1) -> None:
        '''Drop features based on IV values across different time periods.
        Instance attribute '_drop' will be updated.
        
        Args:
            iv_min: If the IV value of a feature for any specified time period falls below this threshold, 
                the feature will be dropped, drop nothing if None or < 0.
            iv_mean: If the average IV value of a feature across the specified time periods falls below this threshold, 
                the feature will be dropped, drop nothing if None or < 0.
            period: Specify the index range for sorted time partitions: use two integers for a range, 
                a positive integer for the first N, or a negative integer for the last N.
            cores: Number of CPU cores to use. 
        '''
        reason = 'iv_by_time'
        
        if iv_min and iv_min <= 0:
            raise ValueError('iv_min must be > 0.')
        elif iv_mean and iv_mean <= 0:
            raise ValueError('iv_mean must be > 0.')
        elif iv_min or iv_mean:
            self.reset_drop(reason = reason)
        else:
            self.reset_drop(reason = reason)
            return None
        
        if 'drop' in self._config:
            self._config['drop'].update({reason: {'iv_min': iv_min, 'iv_mean': iv_mean, 'period': period}})
        else:
            self._config.update({'drop': {reason: {'iv_min': iv_min, 'iv_mean': iv_mean, 'period': period}}})
        
        if not hasattr(self, '_iv_by_time'):
            self.iv_by_time(cores = cores)
        self.logger.info(f"Dropping iv_by_time with iv_min < {iv_min} and iv_mean < {iv_mean} and period = {period}...")
        
        time_period = getattr(self, 'time_'+ self.train_label)
        time_period = sorted(time_period.unique())
        if period:
            if isinstance(period, int):
                if period > 0:
                    time_period = time_period[:period]
                else:
                    time_period = time_period[period:]
            elif isinstance(period, list):
                time_period = time_period[period[0]:period[1]]
        
        iv_by_time = self._iv_by_time[time_period]
        t_reason = {}
        if iv_min:
            iv_by_time_min = iv_by_time.min(axis = 1)
            for k,v in iv_by_time_min.items():
                if v < iv_min:
                    t_reason[k] = f"min={round(v,4)}"
        if iv_mean:
            iv_by_time_mean = iv_by_time.mean(axis = 1)
            for k,v in iv_by_time_mean.items():
                if v < iv_mean:
                    if v in t_reason:
                        t_reason[k] += f", mean={round(v,4)}"
                    else:
                        t_reason[k] = f"mean={round(v,4)}"

        for k,v in t_reason.items():
            self.logger.info(f" Drop {k} as {reason}: {v}.")
            if k not in self._drop:
                self._drop.update({k: {reason: v}})
            else:
                self._drop[k].update({reason: v})

    def drop_corr(self, data: pd.DataFrame, corr: float = None) -> None:
        '''Drop features based on correlation coefficient of two features.
        Instance attribute '_drop' will be updated.
        
        Args:
            data: A numerical pandas DataFrame for calculating correlation coefficients.
            corr: When the correlation coefficient of two features is larger than this value, 
                then the feature with a smaller IV is removed, drop nothing if None.
        '''
        reason = 'corr' 
        if corr:
            if corr >= 0 and corr < 1:
                self.reset_drop(reason = reason)
            else:
                raise ValueError('`corr` must be in [0,1).')
        else:
            self.reset_drop(reason = reason)
            return None
        
        if 'drop' in self._config:
            self._config['drop'].update({'corr': corr})
        else:
            self._config.update({'drop': {'corr': corr}})
        
        self.logger.info(f"Dropping correlation > {corr}...")
        corrname = data.columns.to_list()
        corrvalue = data.corr().abs().to_numpy()
        ix, cl = np.where(np.triu(corrvalue, 1) > corr)

        filtvalue = np.array([corrvalue[i,j] for i,j in zip(ix,cl)])
        via = np.array([True] * len(ix))
        for i in np.argsort(-filtvalue):
            if not via[i]:
                continue
            ixname, clname = corrname[ix[i]], corrname[cl[i]]
            dropcorr = filtvalue[i]
            ixiv = self._bins.get(ixname).get('iv')
            cliv = self._bins.get(clname).get('iv')
            if ixiv < cliv:
                dropname, resrname = ixname, clname
                dropid = ix[i]
            else:
                dropname, resrname = clname, ixname
                dropid = cl[i]
            self.logger.info(f"  Drop {dropname} as Corr(it, {resrname})={dropcorr:.4f}")
            if dropname not in self._drop:
                self._drop.update({dropname: {reason: dropcorr}})
            else:
                self._drop[dropname].update({reason: dropcorr})
            via = (ix != dropid) & (cl != dropid) & via
            if not via.any():
                break
        
    def drop_psi_with_samp(self, samp: str | pd.DataFrame, psi: float | None = None) -> None:
        '''Drop features based on the PSI values between the train and another sample set.
        Instance attribute '_drop' will be updated.
        
        Args:
            samp: Sample label or pandas DataFrame.
            psi: If the PSI value of a feature is less than this threshold, it will be dropped, drop nothing if None or < 0.
        '''
        if isinstance(samp, str):
            label = samp
        elif isinstance(samp, pd.DataFrame):
            label = 'DataFrame'
        else:
            raise TypeError('Unsupported type for parameter `samp`.')
        
        reason = 'psi_with_' + label
        if psi:
            if psi > 0:
                self.reset_drop(reason = reason)
            else:
                raise ValueError('`psi` must be > 0.')
        else:
            self.reset_drop(reason = reason)
            return None
        if 'drop' in self._config:
            self._config['drop'].update({'psi_with_samp': psi})
        else:
            self._config.update({'drop': {'psi_with_samp': psi}})
        
        self.psi_with_samp(samp = samp)
        self.logger.info(f"Dropping PSI > {psi} with {label}...")
        for k,vpsi in getattr(self, '_'+reason).items():
            if vpsi > psi:
                self.logger.info(f"  Drop {k} for PSI with {label} = {vpsi}.")
                if k not in self._drop:
                    self._drop.update({k: {reason: float(vpsi)}})
                else:
                    self._drop[k].update({reason: float(vpsi)})
    
    def drop_psi_by_time(self, psi: float | None = None, cores: int = 1) -> None:
        '''Drop features based on the PSI values between adjacent time periods.
        Instance attribute '_drop' will be updated.
        
        Args:
            psi: A feature will be dropped if its PSI between any two adjacent time periods is greater than this value, drop nothing if None or < 0.
            cores: Number of CPU cores to use. 
        '''
        reason = 'psi_by_time'
        if psi:
            if psi > 0:
                self.reset_drop(reason = reason)
            else:
                raise ValueError('`psi` must be > 0.')
        else:
            self.reset_drop(reason = reason)
            return None
        if 'drop' in self._config:
            self._config['drop'].update({'psi_by_time': psi})
        else:
            self._config.update({'drop': {'psi_by_time': psi}})
        
        if not hasattr(self, '_psi_by_time'):
            self.psi_by_time(cores = cores)
        self.logger.info(f"Dropping features where max(PSI) by time > {psi}...")
        for k,v in getattr(self, '_' + reason).iterrows():
            maxpsi = v.max()
            if maxpsi > psi:
                self.logger.info(f"  Drop {k} as max(PSI) by time = {maxpsi}.")
                if k not in self._drop:
                    self._drop.update({k: {reason: float(maxpsi)}})
                else:
                    self._drop[k].update({reason: float(maxpsi)})
    
    def drop_woe_monotonicity(self, monotonicity: str | None = None) -> None:
        '''Drop features based on the monotonicity of their WOE.
        Instance attribute '_drop' will be updated.
        
        Args:
           monotonicity: 'increase', 'decrease' or 'either', drop nothing if None. 
        '''
        reason = 'woe_monotonicity'
        if monotonicity:
            if monotonicity in ('increase', 'decrease', 'either'):
                self.reset_drop(reason = reason)
            else:
                raise ValueError("`monotonicity` must be in ('increase', 'decrease', 'either').")
        else:
            self.reset_drop(reason = reason)
            return None
        if 'drop' in self._config:
            self._config['drop'].update({reason: monotonicity})
        else:
            self._config.update({'drop': {reason: monotonicity}})
        
        self.logger.info(f"Dropping features where woe monotonicity != {repr(monotonicity)}...")
        for k,v in self._bins.items():
            woe = v['woe_bin']
            woemono = True
            if len(woe) > 1:
                if pd.isna(v['split'][0]):
                    woe = woe[1:]
                if len(woe) > 1:
                    woem = woe[1:] > woe[:-1]
                    if monotonicity == 'increase' and not woem.all():
                        woemono = False
                    elif monotonicity == 'decrease' and woem.any():
                        woemono = False
                    elif woem.any() and not woem.all():
                        woemono = False
            else:
                woemono = False
            if not woemono:
                self.logger.info(f"  Drop {k} as woe monotonicity != {repr(monotonicity)}.")
                restr = 'neither' if monotonicity == 'either' else f"not {monotonicity}"
                if k not in self._drop:
                    self._drop.update({k: {reason: restr}})
                else:
                    self._drop[k].update({reason: restr})
    
    def drop_vif(self, data: pd.DataFrame, vif = None):
        '''Drop features based on VIF.

        Args:
            data: A numerical pandas DataFrame for the VIF calculation.
            vif: Features with a VIF greater than vif will be removed, drop nothing if None or < 0.
        '''
        reason = 'vif'
        if vif:
            if vif >= 1:
                self.reset_drop(reason = reason)
            else:
                raise ValueError('`vif` must be >= 1.')
        else:
            self.reset_drop(reason = reason)
            return None
        if 'drop' in self._config:
            self._config['drop'].update({'vif': vif})
        else:
            self._config.update({'drop': {'vif': vif}})
        
        if not hasattr(self, '_vif'):
            self.vif(data)
        self.logger.info(f"Dropping features where VIF > {vif}...")
        for k,vvif in getattr(self, '_vif').items():
            if vvif > vif:
                self.logger.info(f"  Drop {k} as VIF = {vvif}.")
                if k not in self._drop:
                    self._drop.update({k: {reason: float(vvif)}})
                else:
                    self._drop[k].update({reason: float(vvif)})

    @staticmethod
    def ranking(y_true: pd.Series, y_score: pd.Series, split: str = 'qcut', q: int | list = 10, bins: int | list = 10, 
                amount: pd.Series | pd.DataFrame | None = None, reverse: bool = False, precision: int = 8, **kwargs) -> pd.DataFrame:
        '''Returns a binned and sorted table of predicted values.

        Args:
            y_true: True values of flag.
            y_score: Predicted probabilities or scores.
            split: Binning method, supports 'qcut'(pandas.qcut), 'cut'(pandas.cut), and 'chi2'(chi2_split).
            q: See pandas.qcut for details.
            bins: See pandas.cut for details.
            amount: Calculate badrate from amount dimension; multiple amount columns supported.
            reverse: Whether to sort the predicted value bins in reverse order.
            precision: Specifies the display precision for bins.
            **kwargs: Additional parameters for the chi2_split method.
        
        Returns:
            A pandas DataFrame.
        '''
        if not isinstance(y_true, pd.Series):
            y_true = pd.Series(y_true)
        
        if split in ('qcut', 'cut'):
            if split == 'qcut':
                cut, bins = pd.qcut(y_score, q = q, duplicates = 'drop', retbins = True, precision = precision)
            else:
                cut, bins = pd.cut(y_score, bins = bins, include_lowest = True, duplicates = 'drop', retbins = True, precision = precision)
            cut = np.array(cut)
            y_ture_arr = np.array(y_true)
            bincnt = y_true.groupby([cut, y_ture_arr]).size().unstack()
            if 0 not in bincnt: bincnt[0] = 0
            if 1 not in bincnt: bincnt[1] = 0
            bincnt[2] = bincnt.sum(axis = 1)
            binsplit = bincnt.index.to_list()
            bincnt = bincnt.to_numpy()
            left = float(np.floor(bins[0]*10**precision) / 10**precision)
            right = float(np.ceil(bins[-1]*10**precision) / 10**precision)
        elif split == 'chi2': 
            cut, binsplit, bincnt = _chi_split(feature = y_score, flag = y_true, precision = precision, retbins = True, retcnt = True, **kwargs)
            cut = np.array(cut)
            left = float(np.floor(y_score.min()*10**precision) / 10**precision)
            right = float(np.ceil(y_score.max()*10**precision) / 10**precision)
        else:
            raise ValueError('`split` is not surpported')
        binsplit[0] = pd.Interval(left = left, right = binsplit[0].right, closed = 'both')
        binsplit[-1] = pd.Interval(left = binsplit[-1].left, right = right, closed = binsplit[-1].closed)
        
        if amount is not None:
            amount_arr = np.array(amount)
            if isinstance(amount, pd.Series) and pd.api.types.is_numeric_dtype(amount_arr):
                bad_amount = amount_arr * y_ture_arr
                amount_name = [amount.name + '_badrate']
            elif isinstance(amount, pd.DataFrame) and pd.api.types.is_numeric_dtype(amount_arr):
                bad_amount = amount_arr * y_ture_arr.reshape(-1, 1)
                amount_name = [i + '_badrate' for i in amount.columns]
            else:
                raise TypeError('Unsupported type for parameter `amount`.')
            bad_amount = pd.DataFrame(bad_amount).groupby(by = cut).sum().to_numpy()
            sum_amount = amount.groupby(by = cut).sum().to_numpy()
            amount_badrate = bad_amount / sum_amount
            
            
        if reverse:
            binsplit = binsplit[::-1]
            bincnt = bincnt[::-1]
            amount_badrate = amount_badrate[::-1]
        bin = group_agg(bincnt)
        bin['split'] = binsplit
        
        res = {}
        for i in ['split', 'binscnt', 'badcnt', 'goodcnt', 'binsprop', 'badrate', 'cum_badrate', 'woe_bin', 'iv_bin', 'lift', 'ks_bin']:
            res.update({i:bin[i]})
        res = pd.DataFrame(res)
        res['split'] = res['split'].astype('object')
        
        if amount is not None:
            res[amount_name] = amount_badrate
        res.index.name = 'bin'
        res.loc['total', 'split'] = pd.Interval(left = left, right = right, closed = 'both')
        res.loc['total', 'binscnt'] = bin['binscnt'].sum()
        res.loc['total', 'badcnt'] = bin['badcnt'].sum()
        res.loc['total', 'goodcnt'] = bin['goodcnt'].sum()
        res.loc['total', 'iv_bin'] = bin['iv_bin'].sum()
        res.loc['total', 'ks_bin'] = bin['ks_bin'].max()
        res.rename(columns = {'split': split + ' split'}, inplace = True)
        return res

    @staticmethod
    def ranking_bytime(y_true: pd.Series, y_score: pd.Series, time: pd.Series, same_cut: bool = True, split: str = 'qcut', 
        q: int | list = 10, bins: int | list = 10, amount: pd.Series | pd.DataFrame | None = None, reverse: bool = False, 
        precision: int = 8, **kwargs) -> dict[str, dict[str, pd.DataFrame]]:
        '''Returns the binned and sorted table of predicted values for each time period.

        Args:
            y_true: True values of flag.
            y_pred: Predicted probabilities or scores.
            time: Time Series values for grouping.
            same_cut: Whether to maintain consistent binning cuts across different time periods.
            split: Binning method, supports 'qcut'(pandas.qcut), 'cut'(pandas.cut), and 'chi2'(chi2_split).
            q: See pandas.qcut for details.
            bins: See pandas.cut for details.
            amount: Calculate badrate from amount dimension; multiple amount columns supported.
            reverse: Whether to sort the predicted value bins in reverse order.
            precision: Specifies the display precision for bins.
            **kwargs: Additional parameters for the chi2_split method.
        
        Returns:
            A dict with split key and a dict value with time keys and pandas DataFrame values.
        '''
        if not isinstance(split, list):
            split = [split]
        if not isinstance(time, np.ndarray):
            time = np.array(time)
        data = pd.DataFrame({'y_true': np.array(y_true), 'y_score': np.array(y_score)})
        if amount is not None:
            if isinstance(amount, pd.Series):
                amount_name = [amount.name]
            elif isinstance(amount, pd.DataFrame):
                amount_name = [i for i in amount.columns]
            else:
                raise TypeError('Unsupported type for parameter `amount`.')
            data[amount_name] = np.array(amount)
        
        res = {}
        for i in split:
            temp = {}
            if same_cut:
                if i == 'qcut':
                    _, bin = pd.qcut(y_score, q = q, duplicates = 'drop', retbins = True, precision = precision)
                elif i == 'cut':
                    _, bin = pd.cut(y_score, bins = bins, include_lowest = True, duplicates = 'drop', retbins = True, precision = precision)
                elif i == 'chi2':
                    _, bin = _chi_split(feature = y_score, flag = y_true, precision = precision, retbins = True, **kwargs)
                    bin = [bin[0].left] + [b.right for b in bin]
                bin[0] = np.float64(np.floor(y_score.min()*10**precision) / 10**precision)
                bin[-1] = np.float64(np.ceil(y_score.max()*10**precision) / 10**precision)
            for t, d in data.groupby(time):
                v = Frame.ranking(d['y_true'], d['y_score'], split = 'cut' if same_cut else i, q = q, bins = bin, 
                                  amount = d[amount_name] if amount is not None else None, reverse = reverse, **kwargs)
                c1 = v.columns[0]
                c2 = f"{t} {i + ' split' if same_cut else c1}"
                v.rename(columns = {c1: c2}, inplace = True)
                temp.update({t: v})
            res.update({i: temp})
        return res

    @staticmethod
    def ranking_writer(path: str, df: pd.DataFrame, flag: str | list[str], score: str, group: str | None = None, time: str | None = None, 
                       same_cut: bool = True, split: str = 'qcut', q: int | list = 10, bins: int | list = 10, amount: str | list[str] = None,  
                       reverse: bool = False, precision: int = 8, **kwargs) -> None:
        '''Generate a binning ranking table for given sample predictions and true labels, and save it to a xlsx file.

        Args:
            path: The file path with the .xlsx extension.
            df: pandas DataFrame containing sample predictions and true labels.
            flag: Label name(s). Multiple labels can be specified for separate outputs.
            score: Column name for the score/prediction.
            time: Column name for the time.
            same_cut: Whether to maintain consistent binning cuts across different time periods.
            split: Binning method, supports 'qcut'(pandas.qcut), 'cut'(pandas.cut), and 'chi2'(chi2_split).
            q: See pandas.qcut for details.
            bins: See pandas.cut for details.
            amount: Column name for calculate badrate from amount dimension; multiple amount columns supported.
            reverse: Whether to sort the predicted value bins in reverse order.
            precision: Specifies the display precision for bins.
            **kwargs: Additional parameters for the chi2_split method.
        '''
        if not isinstance(flag, list):
            flag = [flag]
        
        cols = flag + [score]
        if group:
            cols.append(group)
        if time:
            cols.append(time)
        if amount:
            if not isinstance(amount, list):
                amount = [amount]
            cols.extend(amount)
        df = df[cols].copy()
        
        if pd.api.types.is_numeric_dtype(df[score].dtype):
            df[score] = df[score].astype(float)
        for f in flag:
            if not pd.api.types.is_integer_dtype(df[f].dtype):
                df[f] = df[f].astype(int)
        
        excelwriter = pd.ExcelWriter(path)
        sheet_name = f'{split} ranking table'
        startrow = startcol = 0
        
        def writer(data, label, sheet_name, startrow, startcol):
            pd.DataFrame([label]).to_excel(excelwriter, sheet_name = sheet_name, startrow = startrow, startcol = startcol, header = False, index = False)
            startrow = startrow + 1
            max_col = 0
            for f in flag:
                bhv = data[data[f] >= 0].copy()
                if time:
                    tabs = Frame.ranking_bytime(bhv[f], bhv[score], bhv[time], same_cut = same_cut, split = split, q = q, 
                           bins = bins, amount = bhv[amount] if amount else None, reverse = reverse, precision = precision, **kwargs)
                    tabs = list(tabs.items())[0][1]
                    startrow, startcol = tabs_writer(excelwriter, tabs = tabs, sheet_name = sheet_name, startrow = startrow, 
                                                     startcol = startcol, title = f, tab_key = False)
                    max_col = max(max_col, max([v.shape[1] for k,v in tabs.items()]))
                else:
                    tabs = Frame.ranking(bhv[f], bhv[score], split = split, q = q, bins = bins, amount = bhv[amount] if amount else None, 
                                         reverse = reverse, precision = precision, **kwargs)
                    tabs.to_excel(excelwriter, sheet_name = sheet_name, startrow = startrow, startcol = startcol)
                    max_col = max(max_col, tabs.shape[1])
                startrow = startrow + 1
                
                print(label, f, 'completed.')
            return 0, startcol + max_col + 2
        
        startrow, startcol = writer(df, 'All', sheet_name, startrow, startcol)
        
        if group:
            groups = sorted(df[group].unique())
            for g in groups:
                startrow, startcol = writer(df[df[group] == g], g, sheet_name, startrow, startcol)
        excelwriter.close()
        
    @staticmethod
    def _mapcode(lang: str, split: list[pd.Interval | tuple[str]], value: list[int | float], feature: str, to: str, 
                 nan_val: int | float, oth_val: int | float, sort_tup: bool) -> list[str]:
        '''Generate Python code and SQL code for each bin.

        Args:
            lang: Language, 'py'(python) or 'sql'(SQL).
            split: Bins.
            value: Values corresponding to the bins.
            feature: Feature name.
            to: 'bin', 'woe', or 'score'.
            nan_val: Value returned when the feature value is missing.
            oth_val: Value returned when the feature value is unseen/unencountered.
            sort_tup: Whether to sort tuples, just for category features.
        
        Returns:
            A list containing the code for each line.
        '''
        istup = True if len(split) > 0 and isinstance(split[0], tuple) else False
        if lang == 'py':
            codes = []
            if istup:
                vardict = dict()
                for s, v in zip(split, value):
                    if sort_tup:
                        s = tuple(sorted(s))
                    for e in s:
                        vardict.update({e:v})
                codes.extend([
                    f"def get_{feature}_{to}(var):",
                    f"    if var is None or (isinstance(var, numbers.Number) and math.isnan(var)): return {nan_val}",
                    f"    {feature}_{to}_dict = {vardict}",
                    f"    return {feature}_{to}_dict.get(var, {oth_val})\n",
                ])
            else:
                codes.append(f"def get_{feature}_{to}(var):")
                lensplit = len(split)
                for i, s, v in zip(range(lensplit), split, value):
                    if i == 0:
                        if lensplit == 1:
                            codes.append(f"    if   var is not None and not (isinstance(var, numbers.Number) and math.isnan(var)): return {v}")
                        else:
                            codes.append(f"    if   var <= {s.right}: return {v}")
                    elif i < lensplit - 1:
                        codes.append(f"    elif var <= {s.right}: return {v}")
                    else:
                        codes.append(f"    elif var >  {s.left}: return {v}")
                codes.append(f"    else: return {nan_val}\n")
        elif lang == 'sql':
            lensplit = len(split)
            codes = [',case']
            if istup:
                for i, s, v in zip(range(lensplit), split, value):
                    if sort_tup:
                        s = tuple(sorted(s))
                    if i == 0:
                        if len(s) == 1:
                            codes[0] = f"{codes[0]} when {feature} = {repr(s[0])} then {v}"
                        else:
                            codes[0] = f"{codes[0]} when {feature} in {s} then {v}"
                    else:
                        if len(s) == 1:
                            codes.append(f"      when {feature} = {repr(s[0])} then {v}")
                        else:
                            codes.append(f"      when {feature} in {s} then {v}")
                codes.append(f'      when {feature} is null then {nan_val}')
                codes.append(f'      else {oth_val} end as {feature}_{to}\n')
            else:
                for i, s, v in zip(range(lensplit), split, value):
                    if i == 0:
                        if lensplit == 1:
                            codes[0] = f"{codes[0]} when {feature} is not null then {v}"
                        else:
                            codes[0] = f"{codes[0]} when {feature} <= {s.right} then {v}"
                    elif i < lensplit - 1:
                        codes.append(f"      when {feature} <= {s.right} then {v}")
                    else:
                        codes.append(f"      when {feature} >  {s.left} then {v}")
                codes.append(f"      else {nan_val} end as {feature}_{to}\n")
        else:
            raise ValueError(f'Unsupported value for parameter `lang`.')
        return codes

    def code_bin2num(self, lang: str, feature: str, sort_tup: bool = True) -> list[str]:
        '''Generate code to convert raw feature values into bin numbers.

        Args:
            lang: Language, 'py'(python) or 'sql'(SQL).
            feature: Feature name.
            sort_tup: Whether to sort tuples, just for category features.
        
        Returns:
            A list containing the code for each line.
        '''
        bin = self._bins.get(feature)
        split = bin['split'].copy()
        fillnan = bin.get('fillnan')
        nanext = pd.isna(split[0])
        if nanext:
            split = split[1:]
        istup = True if len(split) > 0 and isinstance(split[0], tuple) else False

        oth_val = -2
        if split == []:
            if lang == 'py':
                codes = [
                    f"def get_{feature}_bin(var):",
                    f"    res = -1 if var is None or (isinstance(var, numbers.Number) and math.isnan(var)) else {oth_val}",
                    f"    return res"
                ]
            elif lang == 'sql':
                codes = [
                    f",case when {feature} is null then -1",
                    f"      else {oth_val} end as {feature}_bin"
                ]
            else:
                raise ValueError(f'Unsupported value for parameter `lang`.')
            return codes
        if fillnan is not None:
            nan_val = split.index(fillnan)
        else:
            nan_val = -1
        value = list(range(len(split)))
        
        codes = self._mapcode(lang = lang, split = split, value = value, feature = feature, to = 'bin', 
                             nan_val = nan_val, oth_val = oth_val, sort_tup = sort_tup)
        return codes
    
    def code_bin2woe(self, lang: str, feature: str, sort_tup : bool = True, miss_fill: int = 0) -> list[str]:
        '''Generate code to convert raw feature values into bin WOE.
        
        Args:
            lang: Language, 'py'(python) or 'sql'(SQL).
            feature: Feature name.
            sort_tup: Whether to sort tuples, just for category features.
            miss_fill: Determines the WOE value of the missing value. 
                <0: Use the minimum WOE among all bins.
                =0: Use 0 as the WOE.
                >0: Use the maximum WOE among all bins.
            
        Returns:
            A list containing the code for each line.
        '''
        bin = self._bins.get(feature)
        split = bin['split'].copy()
        fillnan = bin.get('fillnan')
        nanext = pd.isna(split[0])
        if nanext:
            split = split[1:]

        woe_bin = bin['woe_bin'].tolist()
        if miss_fill == 0:
            oth_val = 0
        elif miss_fill < 0:
            oth_val = max(woe_bin)
        else:
            oth_val = min(woe_bin)
        if split == []:
            if lang == 'py':
                codes = [
                    f"def get_{feature}_woe(var):",
                    f"    return {oth_val}",
                ]
            elif lang == 'sql':
                codes = [f",{oth_val} as {feature}_woe"]
            else:
                raise ValueError(f'Unsupported value for parameter `lang`.')
            return codes
        if nanext:
            nan_val = woe_bin[0]
            value = woe_bin[1:]
        elif fillnan is not None:
            nanidx = split.index(fillnan)
            nan_val = woe_bin[nanidx]
            value = woe_bin
        else:
            nan_val = oth_val
            value = woe_bin

        codes = self._mapcode(lang = lang, split = split, value = value, feature = feature, to = 'woe', 
                             nan_val = nan_val, oth_val = oth_val, sort_tup = sort_tup)
        return codes
    
class LogitFrame(Frame):
    def __init__(self, *args, const: bool = True, **kwargs):
        """Initial sample set field configuration.
        
        Args:
            flag: Flag for sample category.
            time: Specify the time column for the sample.
            exclude: Exclude non-feature columns.
            catvars: Manually assign categorical features. If None, first tries to convert to float, then to category on failure.
            const: Whether to add an intercept for the model training samples.
        """
        super().__init__(*args, **kwargs)
        self._config.update({'x_data': {'const': const}})
    
    def drop_stepwise(self, data: pd.DataFrame, way: str, est: str = 'ols', pvalue: float = 0.1, criterion: str = 'aic', 
                      threshold: float = 0.1, intercept: bool = True) -> None:
        '''Drop features using a two-step method.
        Instance attribute '_drop' will be updated.
        
        Args:
            data: A numerical pandas DataFrame.
            way: Drop stepwise with the direction set to 'both', 'forward', or 'backward', drop nothing if None.
            est: Estimator, either 'ols'(statsmodels.api.OLS) or 'logit'(statsmodels.api.Logit).
            pvalue: Significance threshold for feature entry and removal.
            criterion: Model evaluation metric, 'aic' or 'bic'.
            threshold: Threshold for the decrease in the criterion.
            intercept: Whether the estimator includes an intercept.
        '''
        if way:
            if way in ('both', 'forward', 'backward'):
                self.reset_drop(reason = 'stepwise')
            else:
                raise ValueError("`way` must be in ('both', 'forward', 'backward').")
        else:
            self.reset_drop(reason = reason)
            return None
        config = {'stepwise': {'est': est, 'way': way, 'pvalue': pvalue, 'criterion': criterion, 'threshold': threshold, 'intercept':intercept}}
        if 'drop' in self._config:
            self._config['drop'].update(config)
        else:
            self._config.update({'drop': config})
        
        if est == 'ols':
            Est = OLS
        elif est == 'logit':
            Est = Logit
        else:
            raise ValueError('Unsupported value for parameter `est`.')

        if criterion not in ('aic', 'bic'):
            raise ValueError('Unsupported value for parameter `criterion`.')
        
        self.logger.info(f"Dropping stepwise with {config['stepwise']}...")

        remain = data.columns.to_list()
        y = getattr(self, 'y_' + self.train_label)
        drop = list()
        selected = list()
        
        step = 1
        if way == 'backward':
            self.logger.info(f"  Step {step}: add all features.")
            X = data[remain]
            if intercept:
                X = add_constant(X)
            res = Est(y, X).fit()
            if criterion == 'bic':
                cri = res.bic
            else:
                cri = res.aic
        else:
            cri = np.inf
        
        while remain:
            critn = list()
            pvalues = list()

            for i in remain:
                if way == 'backward':
                    xname = remain.copy()
                    xname.remove(i)
                else:
                    xname = selected + [i]
                X = data[xname]
                if intercept:
                    X = add_constant(X)
                res = Est(y, X).fit()

                if criterion == 'bic':
                    critn.append(res.bic)
                else:
                    critn.append(res.aic)
                pvalues.append(pd.Series(res.pvalues[1:] if intercept else res.pvalues, index = xname))
            
            idx = np.argmin(critn)
            name = remain.pop(idx)
            decline = cri - critn[idx]
            if decline > threshold:
                selected.append(name)
                
                if way == 'both':
                    if cri == np.inf:
                        self.logger.info(f"  Step {step}: add {name}.")
                    else:
                        self.logger.info(f"  Step {step}: add {name} for {'an' if criterion == 'aic' else 'a'} {criterion} decline of {decline}.")
                    drops = pvalues[idx][pvalues[idx] > pvalue]
                    
                    for i, p in drops.items():
                        reason = f"  Step {step}: drop {i} for a p-value of {p}."
                        self.logger.info(reason)
                        if i not in self._drop:
                            self._drop.update({i: {'stepwise': f"step {step}"}})
                        else:
                            self._drop[i].update({'stepwise': f"step {step}"})
                        drop.append(i)
                        selected.remove(i)
                    if len(selected) == 0:
                        break
                elif way == 'backward':
                    reason = f"  Step {step + 1}: drop {name} for an {criterion} decline of {decline}."
                    self.logger.info(reason)
                    if name not in self._drop:
                        self._drop.update({name: {'stepwise': f"step {step + 1}"}})
                    else:
                        self._drop[name].update({'stepwise': f"step {step + 1}"})
                else:
                    if cri == np.inf:
                        self.logger.info(f"  Step {step}: add {name}.")
                    else:
                        self.logger.info(f"  Step {step}: add {name} for an {criterion} decline of {decline}.")
                
                cri = critn[idx]
            else:
                if way == 'both':
                    enddrop = [name] + remain
                    self.logger.info(f"  Step {step}: drop other features as there is no further {criterion} reduction.")
                    for i in enddrop:
                        reason = f"  Step {step}: drop {i} as there is no further {criterion} reduction."
                        if i not in self._drop:
                            self._drop.update({i: {'stepwise': f"step {step}"}})
                        else:
                            self._drop[i].update({'stepwise': f"step {step}"})
                    drop.append(enddrop)
                elif way == 'backward':
                    drop = [name] + remain
                    drop, selected = selected, drop
                else:
                    drop = [name] + remain
                    self.logger.info(f"  Step {step}: drop other features as there is no further {criterion} reduction.")
                    for i in drop:
                        reason = f"  Step {step}: drop {i} as there is no further {criterion} reduction."
                        if i not in self._drop:
                            self._drop.update({i: {'stepwise': f"step {step}"}})
                        else:
                            self._drop[i].update({'stepwise': f"step {step}"})
                break
            step += 1
        X = data[selected]
        if intercept:
            X = add_constant(X)
        self._stepmod = Est(y, X).fit()
    
    def get_xy(self, label: str, drop: bool = True) -> dict[str, pd.DataFrame | pd.Series]:
        '''Get the X and y for model training or prediction.

        Args:
            label: Label of sample set.
            drop: Whether to exclude the dropped features.
        
        Returns:
            A dict with key x and y.
        '''
        const = self._config['x_data']['const']
        x = self.transform(samp = label, woe = True)
        select_fts = self.select if drop else self.feature_names
        if const:
            x = add_constant(x[select_fts])
        else:
            x = x[select_fts]
        return x, getattr(self, 'y_' + label)
    
    def get_metric(self, metric: str | list[str] = ['ks', 'auc'], bytime: bool = False) -> pd.DataFrame | dict[str, pd.DataFrame]:
        '''Retrieve the model's evaluation metrics on all sample sets.

        Args:
            metric: 'ks' and 'auc' are supported.
            bytime: Whether to calculate metrics by time.
        
        Returns:
            If not grouped by time, returns a DataFrame; otherwise, returns a dict with sample labels as keys.
        '''
        res = []
        for s in self._samp_labels:
            x, y = self.get_xy(label = s)
            prob = self._mod.predict(x)
            time = getattr(self, 'time_' + s) if bytime else None
            res.append(eva_metric(y, prob, metric, time))
        if bytime:
            res = {s: v for s,v in zip(self._samp_labels, res)}
        else:
            res = pd.concat(res)
            res.index = self._samp_labels
        return res

    def scorecard(self, base_odds: float = 1/35, base_score: float = 1000, pdo: float = 80, bs_share: bool = True) -> None:
        '''Calculate Logistic Regression Scorecard for Selected Features.
        The result will be saved in the instance attribute '_scorecard', a pandas DataFrame.
        
        Args:
            base_odds: Baseline odds ratio.
            base_score: Score at the baseline odds.
            pdo: Points to Double Odds - score decrease when odds double.
            bs_share: Whether to evenly distribute the base score across the selected features.
        '''
        self._config.update({'scorecard': {'base_odds': base_odds, 'base_score': base_score, 'pdo': pdo, 'bs_share': bs_share}})
        
        factor = -pdo / np.log(2)
        offset = base_score - factor * np.log(base_odds)
        self._config['scorecard'].update({'factor': float(factor), 'offset': float(offset)})
        
        const = self._config['x_data']['const']
        params = self._mod.params.copy()
        if const:
            b = params.iloc[0]
            w = params.iloc[1:]
        else:
            b = 0
            w = params
        baseoff = offset + factor * b
        self._config['scorecard'].update({'basic_score': float(baseoff)})
        
        card = []
        if bs_share:
            share = baseoff / len(w)
        else:
            share = 0
            card.append(pd.DataFrame({'Features': [''], 'Bins': ['basic_score'], 'Score': baseoff}))
        self._config['scorecard'].update({'share': float(share)})

        for k, v in w.items():
            bins = self._bins.get(k)
            split = bins.get('split').copy()
            woe = bins.get('woe_bin')

            score = share + factor * v * woe
            fillnan = bins.get('fillnan')
            if fillnan is not None:
                nanidx = split.index(fillnan)
                if nanidx == 0 and isinstance(split[0], pd.Interval):
                    split[0] = pd.Interval(split[0].left, split[0].right, closed = 'both')
                split[nanidx] = f"{split[nanidx]} or nan"
            if isinstance(split[0], pd.Interval):
                split[0] = pd.Interval(split[0].left, split[0].right, closed = 'both')
            card.append(pd.DataFrame({'Features': [k] * len(score), 'Bins': split, 'Score': score}))
        
        card = pd.concat(card, axis = 0)
        card = card.reset_index(drop = True).set_index('Features')
        self._scorecard = card

    def prob2score(self, prob: float | pd.Series) -> float | pd.Series:
        '''Transform prediction probabilities into scores with parameters identical to those used in scorecard conversion.
        
        Args:
            prob: Probability values, accepting either a scalar or a Series.
        
        Returns:
            Same type as the input.
        '''
        scd = self._config['scorecard']
        score = prob2score(prob, base_odds = scd['base_odds'], base_score = scd['base_score'], pdo = scd['pdo'])
        return score
    
    def code_bin2score(self, lang: str, feature: str, sort_tup: bool = True, miss_fill: float = 0) -> list[str]:
        '''Generate code to convert raw feature values into bin score.
        
        Args:
            lang: Language, 'py'(python) or 'sql'(SQL).
            feature: Feature name.
            sort_tup: Whether to sort tuples, just for category features.
            miss_fill: Determines the score value of the missing value.
                <0: Use the minimum score among all bins.
                =0: Use the share score of bins.
                >0: Use the maximum score among all bins.
        Returns:
            A list containing the code for each line.
        '''
        bin = self._bins.get(feature)
        split = bin['split'].copy()
        fillnan = bin.get('fillnan')
        nanext = pd.isna(split[0])
        if nanext:
            split = split[1:]

        share = self._config['scorecard']['share']
        factor = self._config['scorecard']['factor']
        param = self._mod.params[feature]
        woe_bin = bin['woe_bin']
        score = (share + factor * param * woe_bin).tolist()
        if miss_fill == 0:
            oth_val = np.round(share, 8)
        elif miss_fill < 0:
            oth_val = max(score)
        else:
            oth_val = min(score)
        if split == []:
            if lang == 'py':
                codes = [
                    f"def get_{feature}_score(var):",
                    f"    return {oth_val}"
                ]
            elif lang == 'sql':
                codes = [f",{oth_val} as {feature}_score"]
            else:
                raise ValueError(f'Unsupported value for parameter `lang`.')
            return codes
        if nanext:
            nan_val = score[0]
            value = score[1:]
        elif fillnan is not None:
            nanidx = split.index(fillnan)
            nan_val = score[nanidx]
            value = score
        else:
            nan_val = oth_val
            value = score
        
        codes = self._mapcode(lang = lang, split = split, value = value, feature = feature, to = 'score', 
                              nan_val = nan_val, oth_val = oth_val, sort_tup = sort_tup)
        return codes
    
    def py_score(self) -> list[str]:
        '''Generate Python scoring code.
        
        Returns:
            A list containing the code for each line.
        '''
        const = self._config['x_data']['const']
        params = self._mod.params.map(lambda x: f"{'' if x < 0 else '+'}{x}")
        if const:
            b = params.iloc[0]
            params = params.iloc[1:]
        # prob
        codes = [
            "import math", 
            "from .Python_Code_for_Bin_WOE import *\n",
            "# prob"
        ]
        codes.extend([f"{k}_woe = get_{k}_woe({k})" for k in params.index])
        codes.append("")
        codes.append(f"prob = 1/(1+math.exp(-({b if const else ''}")
        codes.extend([f"    {v} * {k}_woe" for k,v in params.items()])
        codes.append(")))\n")

        # score
        ## method 1
        if hasattr(self, '_scorecard'):
            codes.extend([
                "# score",
                "## method 1",
                "def prob2score(prob, base_odds, base_score, pdo):",
                "    factor = -pdo / math.log(2)",
                "    offset = base_score - factor * math.log(base_odds)",
                "    logodds =  math.log(prob / (1 - prob))",
                "    score = offset + factor * logodds",
                "    return score\n"
            ])
            scd = self._config['scorecard']
            base_odds = scd['base_odds']
            base_score = scd['base_score']
            pdo = scd['pdo']
            codes.append(f"score = prob2score(prob = prob, base_odds = {base_odds}, base_score = {base_score}, pdo = {pdo})\n")
        
        ## method 2
            codes.append("## method 2")
            codes.append("from .Python_Code_for_Bin_Score import *")
            codes.extend([f"{k}_score = get_{k}_score({k})" for k in params.index])
            codes.append("")
            bs_share = scd['bs_share']
            basic_score = scd['basic_score']
            codes.append(f"score = ({basic_score if not bs_share else ''}")
            codes.extend([f"    +{k}_score" for k in params.index])
            codes.append(")")
        return codes
    
    def sql_score(self) -> list[str]:
        '''Generate SQL scoring code.
        
        Returns:
            A list containing the code for each line.
        '''
        const = self._config['x_data']['const']
        params = self._mod.params.map(lambda x: f"{'' if x < 0 else '+'}{x}")
        if const:
            b = params.iloc[0]
            params = params.iloc[1:]
        # prob
        codes = ["-- prob\n", "select *"]
        codes.append(f"    ,1/(1+exp(-({b if const else ''}")
        codes.extend([f"        {v} * {k}_woe" for k,v in params.items()])
        codes.extend([
            "    ))) as prob",
            "from Table_Features_WOE",
        ])
        # score
        ## method 1
        if hasattr(self, '_scorecard'):
            scd = self._config['scorecard']
            base_odds = scd['base_odds']
            base_score = scd['base_score']
            pdo = scd['pdo']

            codes = [f"    {i}" for i in codes]
            codes = [
                "-- score", 
                "---- method 1", 
                "select *",
                f"    ,{pdo}/log(2)*(log(1-prob)-log(prob))+{base_score}+{pdo}/log(2)*log({base_odds}) as score",
                "from(",
            ] + codes + [');']
        
        ## method 2
            codes.extend([
                "-- method 2",
                "select *",
            ])
            bs_share = scd['bs_share']
            basic_score = scd['basic_score']
            codes.append(f"   ,({basic_score if not bs_share else ''}")
            codes.extend([f"        +{i}_score" for i in params.index])
            codes.append("    ) as score")
            codes.append("from Table_Features_Score;")
        return codes

class LGBMCFrame(Frame):
    def __init__(self, *args, cut_codes: bool = False, **kwargs):
        """Initial sample set field configuration.
        
        Args:
            flag: Flag for sample category.
            time: Specify the time column for the sample.
            exclude: Exclude non-feature columns.
            catvars: Manually assign categorical features. If None, first tries to convert to float, then to category on failure.
            cut_codes: Whether to use binned-encoded codes for categorical features.
        """
        super().__init__(*args, **kwargs)
        self._cut_codes = cut_codes
    
    def get_xy(self, label: str, drop: bool = True, mod: bool = False) -> dict:
        '''Get the X and y for model training or prediction.

        Args:
            label: Label of sample set.
            drop: Whether to exclude the dropped features.
            mod: Whether to extract only the features from the model. It has higher priority than drop.
        
        Returns:
            A dict with key x and y.
        '''
        if mod:
            select_fts = self._mod.feature_name_
        elif drop:
            select_fts = self.select
        else:
            select_fts = self.feature_names
        
        exist_float = []
        exist_cat = []
        for i in select_fts:
            if i in self._floatvars:
                exist_float.append(i)
            else:
                exist_cat.append(i)
        x = getattr(self, 'x_' + label)[select_fts]
        if exist_cat:
            x_cut = []
            if self._cut_codes:
                if not hasattr(self, '_cuts'):
                    raise ValueError('Split category features first or set cut_codes = False.')
                if label == self.train_label:
                    for i in exist_cat:
                        codes = self._cuts[i].cat.codes
                        codes.name = i
                        x_cut.append(codes)
                else:
                    for i in exist_cat:
                        codes = self.tobins(x[i]).cat.codes
                        codes.name = i
                        x_cut.append(codes)
            else:
                for i in exist_cat:
                    codes = x[i].cat.codes
                    codes.name = i
                    x_cut.append(codes)
            x = pd.concat([x[exist_float]] + x_cut, axis = 1).reindex(columns = select_fts)
        return x, getattr(self, 'y_' + label)
    
    def importance(self, features_info: pd.DataFrame | None = None, name_key: str | None = None) -> pd.Series | pd.DataFrame:
        '''Get model feature importance and sort in descending order.

        Args:
            features_info: Additional descriptive information about the features.
            name_key: Key specifying the feature name in `features_info`, otherwise use the row index for concatenation.
        
        Returns:
            If features_info is None, a pandas Series is returned; otherwise, a pandas DataFrame is returned.
        '''
        imps = pd.Series(self._mod.feature_importances_, index = self._mod.feature_name_, name = 'importance').sort_values(ascending = False)
        if features_info is not None:
            if name_key is not None:
                features_info = features_info.set_index(name_key)
            imps = imps.to_frame().join(features_info)
        return imps
    
    def drop_low_importance(self, importance: float | None = 0) -> None:
        '''Drop features based on importance. 

        Each run appends a new record of results and drop parameters and does not reset previous results.
        Call the reset_drop method to clear importance manually.
        Instance attribute '_drop' will be updated. 
        
        Args:
            importance: Features with an importance less than or equal to this value are removed, drop nothing if None or < 0.
        '''
        reason = 'low_importance'
        if importance is None or importance < 0:
            return None
        
        if 'drop' in self._config:
            if reason in self._config['drop']:
                times =  len(self._config['drop'][reason]) + 1
                self._config['drop'][reason].append(importance)
            else:
                times = 1
                self._config['drop'].update({reason: [importance]})
        else:
            times = 1
            self._config.update({'drop': {reason: [importance]}})
        
        if times == 1:
            suffix = 'st'
        elif times == 2:
            suffix = 'nd'
        elif times == 3:
            suffix = 'rd'
        else:
            suffix = 'th'
        
        self.logger.info(f"Dropping features importance for the {times}{suffix} time...")
        imp = self.importance()
        for k,v in imp.items():
            if v <= importance:
                self.logger.info(f"  Drop {k} as {reason} = {v} in the {times}{suffix} run.")
                if k in self._drop:
                    if reason in self._drop[k]:
                        self._drop[k][reason].append(v)
                    else:
                        self._drop[k].update({reason: [None] * (times - 1) + [v]})
                else:
                    self._drop.update({k: {reason: [None] * (times - 1) + [v]}})
    
    def drop_importance_decline(self, samp: str, decline: float | None = -0.3, params: dict = None) -> None:
        '''Drop features whose importance decline significantly between training and validation.
        The importance decline will be saved in the instance attribute '_importance_decline', a pandas Series.
        Instance attribute '_drop' will be updated.
        
        Args:
            samp: Sample label.
            decline: A feature will be dropped if its importance percentile decline is greater than this threshold, 
                drop nothing if None or >= 0.
            params: Model training parameters on sample.
        '''
        if isinstance(samp, str):
            x_samp, y_samp = self.get_xy(samp, mod = True)
        else:
            raise ValueError('Unsupported type for parameter `samp`.')
        
        reason = f'importance_decline_{samp}'
        if decline:
            if decline < 0:
                self.reset_drop(reason = reason)
            else:
                raise ValueError('`decline` must be < 0.')
        else:
            self.reset_drop(reason = reason)
            return None
        if 'drop' in self._config:
            self._config['drop'].update({reason: decline})
        else:
            self._config.update({'drop': {reason: decline}})
        
        self.logger.info(f"Dropping importance percentile declines < {decline} in {samp}...")

        init_imp = self.importance()
        if params:
            init_params = params
        else:
            init_params = {'verbose':-1}
        mod = self._mod.__class__(**init_params)
        mod.fit(x_samp, y_samp)
        samp_imp = pd.Series(mod.feature_importances_, index = mod.feature_name_, name = 'importance').sort_values(ascending = False)

        init_imp = init_imp/init_imp.iloc[0]
        samp_imp = samp_imp/samp_imp.iloc[0]
        diff = samp_imp - init_imp
        self._importance_decline = diff

        for k,v in diff.items():
            if v < decline:
                self.logger.info(f"  Drop {k} as importance percentile declines in {samp} = {v}.")
                if k not in self._drop:
                    self._drop.update({k: {reason: v}})
                else:
                    self._drop[k].update({reason: v})
    
    def pop_importance(self, metric: str = 'ks', minf: int = 50) -> tuple[pd.DataFrame, list[list[str]]]:
        '''Iteratively eliminate non-essential features and evaluate the metric.

        Args:
            metric: 'ks' or 'auc'.
            minf: Minimum number of features for modeling.

        Returns:
            Model evaluation metric values on each sample set after every feature elimination step, 
            and the model features removed at each step.
        '''
        self.logger.info(f"Iteratively eliminate non-essential features and evaluate the {metric}...")
        select = self.select
        len_select = len(str(len(select)))
        train_x, train_y = self.get_xy(self.train_label, mod = True)
        eval_sets = {s: self.get_xy(s, mod = True) for s in self._samp_labels[1:]}
        init_params = self._mod.get_params()
        init_params.update({'verbose':-1})
        mod = self._mod.__class__(**init_params)
        result = []
        step_drop = []
        while len(select) >= minf:
            print(f"\rNumber of features selected: {len(select)}{' ' * (len_select - len(str(len(select))))}", end = '')
            temp_x = train_x[select]
            mod.fit(temp_x, train_y)
            temp_prob = mod.predict_proba(temp_x)[:,1]
            if metric == 'ks':
                temp_metric = {self.train_label: ks(train_y, temp_prob)}
            elif metric == 'auc':
                temp_metric = {self.train_label: roc_auc_score(train_y, temp_prob)}
            else:
                raise ValueError('Unsupported value for parameter `metric`.')
            for s,xy in eval_sets.items():
                temp_prob = mod.predict_proba(xy[0][select])[:,1]
                if metric == 'ks':
                    temp_metric.update({s: ks(xy[1], temp_prob)})
                elif metric == 'auc':
                    temp_metric.update({s: roc_auc_score(xy[1], temp_prob)})
            temp_metric = pd.DataFrame(temp_metric, index = [0])
            result.append(temp_metric)
            
            importance = pd.Series(mod.feature_importances_, index = mod.feature_name_, name = 'importance').sort_values(ascending = False)
            select = importance[importance > 0].index.to_list()
            if len(select) == len(importance):
                step_drop.append([select.pop()])
            else:
                step_drop.append(importance[importance <= 0].index.to_list())
        result = pd.concat(result)
        result.reset_index(drop = True, inplace = True)
        result.index.name = 'step'
        print()
        return result, step_drop
    
    def get_metric(self, metric: str | list[str] = ['ks', 'auc'], bytime: bool = False) -> pd.DataFrame | dict[str, pd.DataFrame]:
        '''Retrieve the model's evaluation metrics on all sample sets.

        Args:
            metric: 'ks' and 'auc' are supported.
            bytime: Whether to calculate metrics by time.
        
        Returns:
            If not grouped by time, returns a DataFrame; otherwise, returns a dict with sample labels as keys.
        '''
        res = []
        for s in self._samp_labels:
            x, y = self.get_xy(label = s, mod = True)
            prob = self._mod.predict_proba(x)[:,1]
            time = getattr(self, 'time_' + s) if bytime else None
            temp = eva_metric(y, prob, metric, time)
            temp.index.name = s
            res.append(temp)
        if bytime:
            res = {s: v for s,v in zip(self._samp_labels, res)}
        else:
            res = pd.concat(res)
            res.index = self._samp_labels
        return res
    
    def get_param_metric(self, metric: str = 'ks', random: bool = True, **param) -> tuple[str, list, str, dict]:
        '''Tunes a single model parameter and returns the model's evaluation metric values on each sample set. 
        
        Args:
            metric: 'ks' or 'auc'.
            random: Whether to use a random seed for training at each parameter value.
            **param: Training parameters in LightGBM, taking only the first parameter.

        Returns:
            A tuple containing parameter name, parameter values, metric name, metric value.
            Metric values is a dict containing sample names and their corresponding metric values.
        '''
        params_init = self._mod.get_params()
        params_copy = params_init.copy()
        
        param, value = list(param.items())[0]
        self.logger.info(f"model fitting with {param} = {value}...")
        train_x, train_y = self.get_xy(self.train_label, mod = True)
        eval_sets = {s: self.get_xy(s, mod = True) for s in self._samp_labels[1:]}
        
        samp_metric = {s: [] for s in self._samp_labels}
        max_len = 0
        for v in value:
            v_str = str(round(v, 10))
            len_str = len(v_str)
            max_len = max(max_len, len_str)
            print(f"\r{param} = {v_str}{' ' * (max_len - len_str)}", end = '')
            if param == 'seed' or not random:
                params_copy.update({param: v})
            else:
                params_copy.update({param: v, 'seed': np.random.randint(0, 1000)})
            self._mod.set_params(**params_copy)
            self._mod.fit(train_x, train_y)
            train_prob = self._mod.predict_proba(train_x)[:,1]
            
            if metric == 'ks':
                samp_metric[self.train_label].append(ks(train_y, train_prob))
            elif metric == 'auc':
                samp_metric[self.train_label].append(roc_auc_score(train_y, train_prob))
            else:
                raise ValueError(f'Unsupported value for parameter `metric`.')
            for s, xy in eval_sets.items():
                prob = self._mod.predict_proba(xy[0])[:,1]
                if metric == 'ks':
                    samp_metric[s].append(ks(xy[1], prob))
                elif metric == 'auc':
                    samp_metric[s].append(roc_auc_score(xy[1], prob))
        self._mod.set_params(**params_init)
        print()
        return param, value, metric, samp_metric
    
    def prob2score(self, prob: float | pd.Series = None, base_odds: float = 1/35, base_score: float = 1000, pdo: float = 80) -> float | pd.Series:
        '''Set parameters for converting probability values to scores. If prob is provided, returns the converted score.
        
        Args:
            prob: Probability values, accepting either a scalar or a Series.
            base_odds: Baseline odds ratio.
            base_score: Score at the baseline odds.
            pdo: Points to Double Odds - score decrease when odds double.

        Returns:
            Same type as the input.
        '''
        self._config.update({'score': {'base_odds': base_odds, 'base_score': base_score, 'pdo': pdo}})
        if prob is not None:
            score = prob2score(prob, base_odds = base_odds, base_score = base_score, pdo = pdo)
            return score

    @staticmethod
    def _parse_tree(tree: dict, feature_names: list[str], lang: str = 'py', indent: int = 4) -> list[str]:
        '''Parse a single tree.

        Args:
            tree: A tree dict of LGBMClassifier.
            feature_names: Feature names the model used.
            lang: Language, 'py' or 'sql'.
            indent: The standard number of indentation spaces for code.
        
        Returns:
            A list containing the code for each line.
        '''
        tree_index = tree['tree_index']
        tree_structure = tree['tree_structure']
        def recursive_parse(node:dict, depth: int, lang: str, indent = indent):
            if 'leaf_index' in node:
                leaf_value = node['leaf_value']
                if lang == 'py':
                    return [f"{' ' * indent * depth}return {float(leaf_value)}"]
                elif lang == 'sql':
                    return [f"{float(leaf_value)}"]
            else:
                feature = feature_names[node['split_feature']]
                decision_type = node['decision_type']
                threshold = node['threshold']
                default_left = node['default_left']
                if decision_type == '<=':
                    reverse_type = '>'
                elif decision_type == '>':
                    reverse_type = '<='
                else:
                    raise ValueError(f"'==' is not supported to parse in tree_{tree_index}.")
                left = recursive_parse(node['left_child'], depth + 1, lang)
                right = recursive_parse(node['right_child'], depth + 1, lang)
                if lang == 'py':
                    indent = ' ' * indent * depth
                    codes = [f"{indent}if d[{repr(feature)}] is None or math.isnan(d[{repr(feature)}]) or d[{repr(feature)}] {decision_type if default_left else reverse_type} {threshold}:"]
                    codes.extend(left if default_left else right)
                    codes.append(f"{indent}else:")
                    codes.extend(right if default_left else left)
                    return codes
                elif lang == 'sql':
                    indent1 = ' '*indent*(depth*2-1)
                    indent2 = ' '*indent*(depth-1)*2
                    codes = [
                        f"case when {feature} is null or {feature} {decision_type if default_left else reverse_type} {threshold}",
                        f"{indent1}then {left[0] if default_left else right[0]}",
                    ]
                    if default_left and len(left) > 1:
                        codes.extend(left[1:])
                    elif not default_left and len(right) > 1:
                        codes.extend(right[1:])
                    
                    codes.append(f"{indent1}else {right[0] if default_left else left[0]}")
                    if default_left and len(right) > 1:
                        codes.extend(right[1:])
                    elif not default_left and len(left) > 1:
                        codes.extend(left[1:])
                    codes.append(f"{indent2}end")
                    return codes
        if lang == 'py':
            res = [f"def tree_{tree_index}(d):"] + recursive_parse(tree_structure, 1, lang)
        elif lang == 'sql':
            res = recursive_parse(tree_structure, 1, lang)
        return res
        
    def py_score(self, booster: 'lightgbm.basic.Booster' = None):
        '''Generate Python scoring code.

        Args:
            booster: If a booster is specified, the booster of the instance attribute '_mod' will not be used.
        
        Returns:
            A list containing the code for each line.
        '''
        if booster is None:
            dm = self._mod.booster_.dump_model()
        else:
            dm = booster.dump_model()
        
        trees = dm['tree_info']
        codes = ['import math\n']
        for t in trees:
            codes.extend(self._parse_tree(t, dm['feature_names'], lang = 'py'))
            codes.append('')
        codes.append("def predict(d):")
        lentrees = len(trees)
        treesidx = list(range(lentrees))
        for i in range(int(np.ceil(lentrees/10))):
            temp = ' + '.join(f"tree_{i}(d)" for i in treesidx[i*10:(i+1)*10])
            if i == 0:
                adj_str = f"    adj = {'(' if lentrees > 10 else ''}{temp}"
            else:
                adj_str = f"        + {temp}"
            codes.append(adj_str)
        if lentrees > 10:
            codes.append("    )")
        codes.append("    return 1 / (1 + math.exp(-adj))\n")
        
        score_config = self._config.get('score')
        if score_config:
            base_odds = score_config['base_odds']
            base_score = score_config['base_score']
            pdo = score_config['pdo']
            codes.extend([
                "# score",
                f"def prob2score(prob, base_odds = {base_odds}, base_score = {base_score}, pdo = {pdo}):",
                "    factor = -pdo / math.log(2)",
                "    offset = base_score - factor * math.log(base_odds)",
                "    logodds =  math.log(prob / (1 - prob))",
                "    score = offset + factor * logodds",
                "    return score\n",
            ])
        return codes

    def sql_score(self, booster: 'lightgbm.basic.Booster' = None):
        '''Generate SQL scoring code.
        
        Args:
            booster: If a booster is specified, the booster of the instance attribute '_mod' will not be used.
        
        Returns:
            A list containing the code for each line.
        '''
        if booster is None:
            dm = self._mod.booster_.dump_model()
        else:
            dm = booster.dump_model()
        trees = dm['tree_info']
        score_config = self._config.get('score')

        codes = ["select *, 1/(1+exp(-("]
        for t in trees:
            adj = self._parse_tree(t, dm['feature_names'], lang = 'sql', indent = 5)
            adj = [f"    {a}"  for a in adj]
            codes.extend(adj)
            codes.append('    +')
        codes.pop()
        codes[-1] = codes[-1] + "))) as prob"
        codes.extend(["from Table_Features", ';'])
        
        if score_config:
            codes.pop()
            base_odds = score_config['base_odds']
            base_score = score_config['base_score']
            pdo = score_config['pdo']

            codes2 = [f"select *, {pdo}/log(2)*(log(1-prob)-log(prob))+{base_score}+{pdo}/log(2)*log({base_odds}) as score"]
            codes[0] = f"from({codes[0]}"
            for i in range(1, len(codes)):
                codes[i] = f"    {codes[i]}"
            codes = codes2 + codes
            codes.append(")")
        return codes
        