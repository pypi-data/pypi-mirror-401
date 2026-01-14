import pandas as pd
import numpy as np
import psutil
from functools import wraps
import logging

class missdict(dict):
    '''Subclass of dict that returns ('NotFound',) when a non-existent key is looked up.
    '''
    def __missing__(self, key):
        return ('_NotFound_',)

def interval_to_str(itv: pd.Interval, precision: int) -> str:
    '''Convert pandas Interval to string with specified precision. 
    
    Args:
        itv: A pandas Interval.
        precision: Floating point number accuracy.
    
    Returns:
        A string.
    '''
    left_bracket = '[' if itv.closed_left else '('
    right_bracket = ']' if itv.closed_right else ')'
    return f"{left_bracket}{round(itv.left, precision)}, {round(itv.right, precision)}{right_bracket}"

def iter_to_str(it: 'iterable', num: int, length: int) -> str:
    '''Convert a iterable object to a finite string.

    Args:
        num: Number of elements to display.
        length: Character count displayed for each individual element.

    Returns:
        A string.
    '''
    tupstr = []
    for i in it[:num]:
        ele = str(i)
        tupstr.append(ele[:length] + '...' if len(ele) > length else ele[:length])
    if len(it) > num:
        tupstr.append('...')
    return f"({', '.join(tupstr)})"

def to_str(val, precision: int = 4, iter_display_limit: tuple = (1, 10), nan = 'nan') -> str:
    '''Convert pandas Interval or iterable object to a finite string.

    Args:
        precision: Floating point number accuracy.
        iter_display_limit: Display limit for the number of elements and their character count. 
            Default shows the first 10 characters of the first element.
        nan: String for NaN value.

    Returns:
        A string.
    '''
    if pd.isna(val):
        return nan
    elif pd.api.types.is_numeric_dtype(type(val)):
        res = str(round(val, precision))
    elif isinstance(val, pd.Interval):
        res = interval_to_str(val, precision)
    elif isinstance(val, str):
        res = val
    elif hasattr(val, '__iter__'):
        res = iter_to_str(val, *iter_display_limit)
    else:
        res = str(val)
    return res

def dict2list(d: dict, n_col: int, fill: str | None = '') -> list:
    '''Convert a dict into a matrix-like list.

    Args:
        d: A dict.
        n_col: Number of columns in the matrix.
        add: Used to fill missing matrix elements.

    Returns:
        A list.
    '''
    lst = list(d.items())
    lend = len(d)
    i = 0
    res = []
    temp = []
    while True:
        if i < lend:
            value = list(lst[i])
            value[0] = f"{value[0]}:"
            if isinstance(value[1], dict):
                value[1] = '\n'.join([f"{k}: {v}" for k,v in value[1].items()])
            temp.extend(value)
            i += 1
            if i % n_col == 0:
                res.append(temp)
                temp = []
        else:
            if i % n_col == 0:
                break
            temp.extend((fill, fill))
            i += 1
            if i % n_col == 0:
                res.append(temp)
                break
    return res

class TextObjectHandler(logging.Handler):
    '''Text-like object used for writing log messages.
    '''
    def __init__(self, text_obj):
        super().__init__()
        self.text_obj = text_obj
        
    def emit(self, record):
        msg = self.format(record)
        self.text_obj.write(msg + '\n')

def check_memory(high_threshold= 0.95, low_mb= 500):
    '''A decorator for checking available memory size before function execution.

    Args:
        high_threshold: Maximum proportion of used memory.
        low_mb: Minimum available memory size in MB.
    '''
    if high_threshold <= 0 or high_threshold >= 1:
        raise ValueError("`high_threshold` must be in (0,1).")
    high_threshold *= 100
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            sys_mem = psutil.virtual_memory()
            if sys_mem.percent > high_threshold:
                raise MemoryError(f"Memory usage exceeds {high_threshold}%.")
            if sys_mem.available < low_mb * 1024 * 1024:
                raise MemoryError(f"System available memory < {low_mb} MB.")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def ylim_adj(y, space: tuple[float, float], minhgt: float = 0) -> tuple[float, float]:
    '''Used to adjust the position and height of the y-axis in an image.

    Args:
        space: tuple, with elements representing the distances from the y-axis to the bottom and top borders respectively. 
            Elements must be in the range [0,1).
        minhgt: Minimum height of the y-axis.
    
    Returns:
        A tuple.
    '''
    for i in space:
        if i < 0 or i >= 1:
            raise ValueError('`space` must be in [0,1).')
    if isinstance(y, np.ndarray):
        y = np.array(y)
    y_min = float(y.min())
    y_max = float(y.max())
    exp = y_max - y_min

    if exp == 0:
        if y_min > 0:
            exp = y_min
        elif y_min < 0:
            exp = -y_min
        else:
            return (None, None)
    
    bottom = y_min - exp * space[0]
    top = y_max + exp * space[1]

    if top - bottom < minhgt:
        diff = (minhgt - top + bottom)
        bottom -= diff * space[0]
        top += diff * space[1]
    return bottom, top

def palette(n) -> list[tuple[float, float, float]]:
    '''Returns a uniformly distributed color palette based on the three primary colors: red, green, and blue.

    Args:
        n: Number of colors.
    
    Returns:
        A list composed of tuples, where each tuple contains elements representing the values of red, green, and blue on a scale from 0 to 1.
    '''
    colors = []
    t = int(np.ceil(n ** (1/3)))
    for b in np.linspace(0,1,t):
        for g in np.linspace(0,1,t):
            for r in np.linspace(0,1,t):
                colors.append((r,g,b))
                if len(colors) >= n:
                    return colors

def tabs_writer(excelwriter: pd.ExcelWriter, tabs: dict[str, pd.DataFrame], sheet_name: str, startrow: int, startcol: int, 
                title: str | None = None, tab_key:bool = True) -> None:
    '''Performs read and write operations on a pandas ExcelWriter object.

    Args:
        excelwriter: A pandas ExcelWriter object.
        tabs: A dictionary mapping table names to pandas DataFrames for writing.
        startrow: The starting row position for writing.
        startcol: The starting column position for writing.
        title: A title to insert before writing.
        tab_key: Whether to write the table names.
    '''
    if title:
        pd.DataFrame([title]).to_excel(excelwriter, sheet_name = sheet_name, startrow = startrow, startcol = startcol, header = False, index = False)
        startrow = startrow + 1
    for t, d in tabs.items():
        if tab_key:
            pd.DataFrame([t]).to_excel(excelwriter, sheet_name = sheet_name, startrow = startrow, startcol = startcol, header = False, index = False)
            startrow = startrow + 1
        d.to_excel(excelwriter, sheet_name = sheet_name, startrow = startrow, startcol = startcol)
        startrow = startrow + len(d) + 2
    return startrow, startcol

