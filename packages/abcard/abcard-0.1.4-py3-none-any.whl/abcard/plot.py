import numpy as np
import pandas as pd
from io import BytesIO
from matplotlib import pyplot as plt
from matplotlib.axes import Axes

from .utils import to_str, check_memory, ylim_adj
from .stats import _iv, mod_eva, eva_metric


def plot_bin(ax: Axes, bin: dict, var_name: str | None = None, label: str | None = None, rotation: float = -30, 
             fontsize: str | float = 'medium') -> None:
    '''Plots the binning chart of a feature.

    Args:
        ax: Axis object.
        bin: Binning data.
        var_name: Displayable variable name.
        label: Displayable bin names.
        rotation: Rotation angle for bin names. Refer to matplotlib for details.
        fontsize: Font size for data labels and axis labels. Refer to matplotlib for details.
    '''
    ax2 = ax.twinx()
    ax.ticklabel_format(axis = 'y', style = 'sci', scilimits = (0,0), useMathText = True)
    xticks = bin['bin']
    nanbar = None
    
    if pd.isna(bin['split'][0]):
        nanbar = ax.bar(0, bin['binscnt'][0], color = 'white', edgecolor = 'grey', label = 'nan')
        bar = ax.bar(xticks[1:], bin['binscnt'][1:], color = 'lightgrey', edgecolor = 'black', label = 'count')
        ax2.scatter(xticks[0], bin['badrate'][0], color = 'red', zorder = 1.5)
        line, = ax2.plot(xticks[1:], bin['badrate'][1:], color = 'red', marker = '.', linestyle = '-.', linewidth = .5, label = 'badrate')
    else:
        bar = ax.bar(xticks, bin['binscnt'], color = 'lightgrey', edgecolor = 'black', label = 'count')
        line, = ax2.plot(xticks, bin['badrate'], color = 'red', marker = '.', linestyle = '-.', linewidth = .5, label = 'badrate')
    
    if 'fillnan' in bin and bin.get('fillnum') > 0:
        fillnan = bin.get('fillnan')
        nanidx = bin['split'].index(fillnan)
        nanbar = ax.bar(nanidx, bin.get('fillnum'), color = 'white', edgecolor = 'grey', label = 'nan')
        nanprop = bin.get('fillnum') / bin.get('count')
        ax.text(nanidx - 0.4, bin.get('fillnum'), f'{nanprop * 100:.2f}%', ha = 'left', va = 'bottom', fontsize = fontsize)

    for x, y, p in zip(xticks, bin['binscnt'], bin['binsprop']):
        ax.text(x - 0.4, y, f'{p * 100:.2f}%', ha = 'left', va = 'bottom', fontsize = fontsize)
    for x, y in zip(xticks, bin['badrate']):
        ax2.text(x, y, f'{y * 100:.2f}%', color = line.get_color(), ha = 'left', va = 'bottom', fontsize = fontsize)
    
    ax.set_xticks(xticks, xticks if label is None else label, rotation = 0 if label is None else rotation, fontsize = fontsize)
    ax.set_title(var_name if var_name else 'count - badrate', fontsize = fontsize)
    
    if nanbar is not None:
        ax.legend([nanbar, bar, line], ['count_nan', 'count', 'badrate'], fontsize = fontsize)
    else:
        ax.legend([bar, line], ['count', 'badrate'], fontsize = fontsize)


def plot_prop_trend(ax: Axes, prop: pd.DataFrame, var_name: str | None = None, label: str | None = None, 
                    rotation: float = -30, fontsize: str | float = 'medium'):
    '''Plots the time trend of proportions for each bin.

    Args:
        ax: Axis object.
        prop: Time trend data of proportions for each bin.
        var_name: Displayable variable name.
        label: Displayable bin names.
        rotation: Rotation angle for bin names. Refer to matplotlib for details.
        fontsize: Font size for data labels and axis labels. Refer to matplotlib for details.
    '''
    lenticks = prop.shape[0]
    ticks = range(lenticks)
    label = label if label else range(prop.shape[1])
    lenlabel = len(label)
    bottom = np.zeros(lenticks)
    ticklabel = prop.index
    prop = prop.to_numpy()
    for i in range(lenlabel):
        ax.bar(ticks, prop[:,i], bottom = bottom, label = label[i])
        bottom = bottom + prop[:,i]
    ax.set_xticks(ticks = ticks)
    ax.set_xticklabels(labels = ticklabel, rotation = rotation, fontsize = fontsize)
    if var_name:
        ax.set_title(var_name, fontsize = fontsize)
        ax.set_ylabel('proportion', fontsize = fontsize)
    else:
        ax.set_title('proportion', fontsize = fontsize)
    ax.legend(fontsize = fontsize, framealpha = 0.5, loc = (1, 0), ncols = np.ceil(lenlabel/15))

def plot_badrate_trend(ax: Axes, badrate: pd.DataFrame, var_name: str | None = None, label: str | None = None, 
                       rotation: float = -30, fontsize: str | float = 'medium'):
    '''Plots the time trend of badrates for each bin.

    Args:
        ax: Axis object.
        badrate: Time trend data of badrates for each bin.
        var_name: Displayable variable name.
        label: Displayable bin names.
        rotation: Rotation angle for bin names. Refer to matplotlib for details.
        fontsize: Font size for data labels and axis labels. Refer to matplotlib for details.
    '''
    ticks = range(badrate.shape[0])
    label = label if label else range(badrate.shape[1])
    ax.plot(badrate.to_numpy(), label = label, marker = '.')
    ax.set_xticks(ticks = ticks)
    ax.set_xticklabels(labels = badrate.index, rotation = rotation, fontsize = fontsize)
    if var_name:
        ax.set_title(var_name, fontsize = fontsize)
        ax.set_ylabel('badrate', fontsize = fontsize)
    else:
        ax.set_title('badrate', fontsize = fontsize)
    ax.legend(fontsize = fontsize, framealpha = 0.5, loc = (1, 0), ncols = np.ceil(len(label)/15))

def plot_iv_trend(ax: Axes, iv: pd.DataFrame, IV: float, var_name: str | None = None, rotation: float = -30, fontsize: str | float = 'medium'):
    '''Plots the time trend of IVs for each bin.

    Args:
        ax: Axis object.
        iv: Time trend data of IVs for each bin.
        IV: IV value across all training samples.
        var_name: Displayable variable name.
        rotation: Rotation angle for bin names. Refer to matplotlib for details.
        fontsize: Font size for data labels and axis labels. Refer to matplotlib for details.
    '''
    ticks = range(len(iv))
    ax.plot(ticks, iv, marker = '.')
    for x, y in zip(ticks, iv):
        ax.text(x, y, f'{y:.4f}', ha = 'center', va = 'bottom', fontsize = fontsize)
    
    ax.axhline(y = 0.02, color = 'red', linewidth = 0.5)
    ax.axhline(y = 0.01, color = 'red', linewidth = 0.5, linestyle = '--')
    ax.axhline(y = 0.005, color = 'red', linewidth = 0.5, linestyle = '-.')
    ax.set_xticks(ticks = ticks)
    ax.set_xticklabels(labels = iv.index, rotation = rotation, fontsize = fontsize)
    
    sub_title = f'IV = {IV:.4f}'
    ax.text(1, 1, sub_title, fontsize = fontsize, transform = ax.transAxes, horizontalalignment = 'right', verticalalignment='bottom')
    
    if var_name:
        ax.set_title(var_name, pad = 15, fontsize = fontsize)
        ax.set_ylabel('iv', fontsize = fontsize)
    else:
        ax.set_title('iv', fontsize = fontsize)

@check_memory()
def plot_cut(cut: pd.Series, flag: pd.Series, bin: dict, time: pd.Series | None = None, figsize: tuple = (12,9), show_name: bool = True, 
             show_label: bool = True, precision: int = 4, iter_display_limit: tuple = (1, 10), fontsize: str | float = 'medium', 
             rotation: float = -30, retnbuff: bool = False) -> plt.Figure | BytesIO:
    '''Plots the feature's binning chart along with time trend charts for bin proportions, badrate, and IV (if time is provided).

    Args:
        cut: The already binned feature.
        bin: Binning data.
        time: The time column used for grouping.
        figsize: Figure size for each plot, specified as (width, height) in inches.
        show_name: Whether to display the feature name on the plot.
        show_label: Whether to display the bin labels on the x-axis instead of simple bin indices.
        precision: Printing precision for floats. 
        iter_display_limit: Maximum length to display for iterable object. Default shows the first 10 characters of the first element.
        fontsize: Font size for data labels and axis labels. Refer to matplotlib for details.
        rotation: Rotation angle (in degrees) for the x-axis tick labels. Useful for preventing overlapping with long bin labels. 
        retnbuff: Whether to return a byte stream.
    
    Returns:
        A Figure or BytesIO object.
    '''
    if show_label:
        label = [to_str(i, precision, iter_display_limit) for i in bin['split']]
        label = [str(i) + ':' + s for i,s in enumerate(label)]
    else:
        label = None
    figsize = (figsize[0] * (1 + np.ceil(len(bin['split'])/20)/10), figsize[1])
    if time is None:
        fig, ax = plt.subplots(figsize = figsize)
        plot_bin(ax, bin, var_name = cut.name if show_name else None, label = label, rotation = rotation, fontsize= fontsize)
    else:
        fig, ax = plt.subplots(2, 2, figsize = figsize)
        cutcount = flag.groupby(by = [time.to_numpy(), cut.to_numpy(), flag.to_numpy()], dropna = False, sort = False).size().unstack()
        cutsize = cutcount.sum(axis = 1)
        timecount = cutcount.groupby(level = 0, sort = False).sum()
        timesize = timecount.sum(axis = 1)
        timeprop = cutsize.div(timesize, level = 0).unstack(fill_value = 0).sort_index()[bin['split']]
        badrate = cutcount[1].div(cutsize, fill_value = 0).unstack().sort_index()[bin['split']]
        timeiv = cutcount.fillna(0.5).groupby(level = 0).apply(lambda x: _iv(x.to_numpy()))
        plot_bin(ax[0, 0], bin, var_name = None, label = label, rotation = rotation, fontsize= fontsize)
        plot_prop_trend(ax[0, 1], timeprop, var_name = None, label = label, rotation = rotation, fontsize= fontsize)
        plot_iv_trend(ax[1, 0], timeiv, bin.get('iv'), var_name = None, rotation = rotation, fontsize= fontsize)
        plot_badrate_trend(ax[1, 1], badrate, var_name = None, label = label, rotation = rotation, fontsize= fontsize)
        if show_name:
            fig.suptitle(cut.name)
    fig.tight_layout()
    
    if retnbuff:
        buffer = BytesIO()
        fig.savefig(buffer, format = 'pdf')
        plt.close()
        del fig, ax
        return buffer
    return fig

def plot_corr(corr: pd.DataFrame, xlabel: str | None = None, ticklabels: bool = True, figsize: tuple = (8,6), 
              dpi: float = 72, rotation: float = 20) -> plt.Figure:
    '''Plots the correlation heatmap.

    Args:
        xlabel: x轴的标签。
        ticklabels: 是否打印corr的列名为轴刻度标签。
        figsize: Figure size for each plot, specified as (width, height) in inches.
        dpi: Specifies the resolution (dots per inch) of the figure.
        rotation: Rotation angle (in degrees) for the x-axis tick labels. Useful for preventing overlapping with long bin labels. 
    
    Returns:
        A Figure object.
    '''
    names = corr.columns.to_list()
    corr = corr.abs()
    data = np.tril(corr.to_numpy(), -1)
    data = data[1:, :-1]
    ticks = np.array(range(data.shape[0]))
    X,Y = np.meshgrid(ticks, ticks)
    
    fig = plt.figure(figsize = figsize, dpi = dpi)
    # plt.autoscale(enable = False, tight = False)
    plt.xlim(-0.5, max(ticks) + 0.5)
    plt.ylim(-0.5, max(ticks) + 0.5)
    
    plt.pcolormesh(X, Y, data, cmap = 'Oranges', edgecolors = 'white', vmin = 0, vmax = 1)
    plt.grid(False)
    plt.colorbar()
    plt.step(ticks + .5, ticks - .5, linestyle = '-.', color = 'black', linewidth = 0.5)
    plt.gca().xaxis.set_ticks_position('top')
    plt.gca().tick_params(direction = 'out')
    if ticklabels:
        plt.xticks(ticks, names[:-1], rotation = rotation, ha = 'left')
        plt.yticks(ticks, names[1:])
    else:
        ftsnum = list(range(len(names)))
        plt.xticks(ticks, ftsnum[:-1])
        plt.yticks(ticks, ftsnum[1:])
    if xlabel is None:
        xlabel = 'Correlation'
    plt.xlabel(xlabel)
    fontsize = figsize[1] * 20 / data.shape[0]
    for idx,x in np.ndenumerate(data):
        if x > 0:
            color = 'white' if x > 0.7 else 'black'
            plt.text(idx[1], idx[0], f'{x:.3f}', ha = 'center', va = 'center', color = color, fontsize = fontsize)
    plt.tight_layout()
    return fig

def plot_eva(data: dict[str: tuple[pd.Series, pd.Series]], beta: float = 1, figsize: tuple = (8,7), dpi: float = 72, retn_stats: bool = False) -> plt.Figure | tuple[plt.Figure, dict]:
    '''Calculates model evaluation metrics and plots corresponding graphs. 
        The PR curve will not plot the top 10 samples with the highest predicted probability (for smoothing purposes).
    
    Args:
        data: A key-value pair consisting of dataset names and their corresponding true labels and predicted probabilities (y_true, y_prob).
        beta: Specifies the weight of precision for the f-score. 
        figsize: Figure size for each plot, specified as (width, height) in inches.
        dpi: Specifies the resolution (dots per inch) of the figure.
        retn_stats: Whether to return the model evaluation result data.
    
    Returns:
        A Figure object, or a tuple of (Figure, dict), where the dict is a key-value pair of dataset names and their evaluation result data.
    ''' 
    plotstats = {}
    for k, v in data.items():
        plotstats[k] = mod_eva(v[0], v[1], beta= beta)
    
    fig, ax = plt.subplots(2, 2, figsize = figsize, dpi = dpi)
    
    for k, v in plotstats.items():
        ax[0,0].plot(v['p_f'], v['f'][:-1], zorder = 1, label = f'{k} (p={v["p_f_max"]:.3f}, f={v["f_max"]:.3f})')
        ax[0,0].scatter(v['p_f_max'], v['f_max'], s = 8, marker = '^', edgecolor = 'red', zorder = 2)
        ax[0,0].vlines(v['p_f_max'], ymin = 0, ymax = v['f_max'], color = 'grey', linestyle = '--', linewidth = 0.5)
        ax[0,0].tick_params(axis='x', which='minor', direction = 'in', labelsize='small', pad = -10)

        ax[0,1].plot(v['p_ks'], v['ks'], zorder = 1, label = f'{k} (p={v["p_ks_max"]:.3f}, ks={v["ks_max"]:.3f})')
        ax[0,1].scatter(v['p_ks_max'], v['ks_max'], s = 10, marker = '^', edgecolor = 'red', zorder = 2)
        ax[0,1].vlines(v['p_ks_max'], ymin = 0, ymax = v['ks_max'], color = 'grey', linestyle = '--', linewidth = 0.5)
        ax[0,1].tick_params(axis='x', which='minor', direction = 'in', labelsize='small', pad = -10)

        ax[1,0].plot(v['recall'][:-10], v['precision'][:-10], zorder = 1, label = f'{k} ')

        ax[1,1].plot(v['fpr'], v['tpr'], label = f'{k} (AUC={v["auc"] * 100:.2f}%)')
        
    ax[0,0].invert_xaxis()
    ax[0,0].set_title(f'F_score(beta={beta}) of Sample')
    ax[0,0].set_xlabel('Probability')
    ax[0,0].set_ylabel('F_score')
    ax[0,0].legend(fontsize = 'small')

    ax[0,1].invert_xaxis()
    ax[0,1].set_title('KS of Sample')
    ax[0,1].set_xlabel('Probability')
    ax[0,1].set_ylabel('KS')
    ax[0,1].legend(fontsize = 'small')

    ax[1,0].axline([0, 0], slope = 1, color = 'grey', linestyle = '--', linewidth = 0.5, label = 'y = x')
    ax[1,0].set_title('PR Curve of Sample')
    ax[1,0].set_xlabel('Recall')
    ax[1,0].set_ylabel('Precision')
    ax[1,0].legend(fontsize = 'small')

    ax[1,1].axline([0, 0], slope = 1, color = 'grey', linestyle = '--', linewidth = 0.5, label = 'y = x')
    ax[1,1].set_title('ROC Curve of Sample')
    ax[1,1].set_xlabel('FPR')
    ax[1,1].set_ylabel('TPR')
    ax[1,1].legend(loc = 'lower right', fontsize = 'small')
    
    plt.tight_layout()
    if retn_stats:
        return fig, plotstats
    return fig

def plot_score(y_true: pd.Series, y_score: pd.Series, time: pd.Series | None = None, bins: int = 50, rotation: float = -30, 
               fontsize: str | float = 'medium', **kwargs) -> plt.Figure:
    '''Plots the distribution of predicted scores, along with a concise evaluation chart grouped by time (if time is provided). 

    Args:
        y_true: The true labels of y.
        y_score: The predicted score values of y.
        time: The time column used for grouping.
        bins: Number of bins for plotting the score distribution histogram.
        rotation: Rotation angle (in degrees) for the x-axis tick labels. Useful for preventing overlapping with long bin labels. 
        fontsize: Font size for data labels. Refer to matplotlib for details.
        kwargs: Additional parameters for plotting the histogram. Refer to matplotlib for details.
    
    Returns:
        A Figure object.
    '''
    if time is None:
        fig, ax = plt.subplots(1, 2, figsize = (10, 4))
        ax00, ax01 = ax
    else:
        fig, ax = plt.subplots(2, 2, figsize = (10, 8))
        (ax00, ax01), (ax10, ax11) = ax
    _, bins, _ = ax00.hist(y_score, bins = bins, color = 'grey', label = 'all sample', **kwargs)
    ax00.set_xlabel('score')
    ax00.set_ylabel('Density')
    ax00.legend()
    ax01.hist(y_score[y_true == 0], bins = bins, color = 'green', label = 'good sample', **kwargs)
    ax01.hist(y_score[y_true == 1], bins = bins, color = 'red', label = 'bad sample', **kwargs)
    ax01.set_xlabel('score')
    ax01.set_ylabel('Density')
    ax01.legend()
    
    if time is not None:
        stats = eva_metric(y_true = y_true, y_score = y_score, metric = 'ks', time = time)
        ticks = list(range(stats.shape[0]))
        ticklabels = stats.index
        bar = ax10.bar(ticks, stats['count'], color = 'lightgrey', edgecolor = 'black', label = 'count')
        ax10.set_xticks(ticks, ticklabels, rotation = rotation, ha = 'left')
        ax10.set_ylabel('count')
        ax102 = ax10.twinx()
        
        ax10.ticklabel_format(axis = 'y', style = 'sci', scilimits = (0,0), useMathText = True)
        line, = ax102.plot(ticks, stats['badrate'], color = 'red', marker = '.', linestyle = '-.', linewidth = .5, label = 'badrate')
        bottom, top = ylim_adj(y = stats['badrate'], space = (0.1, 0.1), minhgt = 0.05)
        ax102.set_ylim(bottom = bottom, top = top)
        ax102.set_ylabel('badrate')
        for x, y in zip(ticks, stats['badrate']):
            ax102.text(x, y, f'{y * 100:.2f}%', color = line.get_color(), ha = 'center', va = 'bottom', fontsize = fontsize)
        ax10.legend([bar, line], ['count', 'badrate'], fontsize = fontsize, loc = (0.2, 1), ncols = 2, frameon = False)

        line2, = ax11.plot(ticks, stats['ks'], color = 'red', marker = '.', linestyle = '-.', linewidth = .5, label = 'ks')
        ax11.set_ylabel('ks')
        bottom, top = ylim_adj(y = stats['ks'], space = (0.1, 0.25), minhgt = 0.05)
        ax11.set_ylim(bottom = bottom, top = top)
        ax11.set_xticks(ticks, ticklabels, rotation = rotation, ha = 'left')
        ax112 = ax11.twinx()
        line3, = ax112.plot(ticks, stats['score_mean'], color = 'blue', marker = '.', linestyle = '-.', linewidth = .5, label = 'mean score')
        ax112.set_ylabel('mean score')
        bottom, top = ylim_adj(y = stats['score_mean'], space = (0.25, 0.1), minhgt = 10)
        ax112.set_ylim(bottom = bottom, top = top)
        ax11.legend([line2, line3], ['ks', 'mean score'], fontsize = fontsize, loc = (0.2, 1), ncols = 2, frameon = False)
        
        for x, k, s in zip(ticks, stats['ks'], stats['score_mean']):
            ax11.text(x, k, f'{k:.3f}', color = line2.get_color(), ha = 'center', va = 'bottom', fontsize = fontsize)
            ax112.text(x, s, f'{s:.3f}', color = line3.get_color(), ha = 'center', va = 'bottom', fontsize = fontsize)
    
    plt.tight_layout()
    return fig

def plot_metric(param_name: str, param, metric_name: str, metric: dict, figsize = (10,5), dpi = 72) -> plt.Figure:
    '''Plots a graph based on given parameter values and model evaluation metric values.

    Args:
        param_name: Model parameter name.
        param: Model parameter values.
        metric_name: Model metric name.
        metric: Model metric values. A dict containing sample names and their corresponding metric values.
        figsize: Figure size for each plot, specified as (width, height) in inches.
        dpi: Specifies the resolution (dots per inch) of the figure.
        
    Returns:
        A Figure object.
    '''
    fig = plt.figure(figsize = figsize, dpi = dpi)
    for s, v in metric:
        plt.plot(param, v, marker = '.', label = s)
    plt.grid(True)
    plt.xticks(ticks = param, labels = [p.round(4) for p in param])
    plt.xlabel(param_name)
    plt.title(metric_name)
    plt.legend()
    return fig
