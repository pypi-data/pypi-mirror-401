from io import BytesIO
import time
import pymupdf
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from concurrent import futures
from tqdm import tqdm

from .frame import Frame
from .plot import plot_corr, plot_cut, plot_eva, plot_score
from .utils import to_str, palette, dict2list

if not hasattr(pd.DataFrame, 'map'):
    pd.DataFrame.map = pd.DataFrame.applymap

def rectsplit(rect: pymupdf.Rect, nrows: int | list[int | float] = 1, ncols: int | list[int | float] = 1, 
              flatten: int | None = 1, margin: float | tuple[float] = 30, rectspacing: float = 10) -> list[pymupdf.Rect]:
    '''Divides a PyMuPDF.Rect object into multiple sub-regions.

    Args:
        nrows: Integer indicating the number of rows, or a sequence representing the height weights for each row.
        ncols: Integer indicating the number of columns, or a sequence representing the width weights for each column.
        flatten: The direction in which to flatten the regions. 0 flattens row-wise, 1 flattens column-wise.
        margin: The width of the margin to preserve around the edges.
        rectspacing: The space to be used as an interval between each sub-region.

    Returns:
        A list composed of PyMuPDF.Rect objects.
    '''
    if isinstance(margin, (float, int)):
        margin = (margin,) * 4
    nrows = np.ones(nrows) if isinstance(nrows, int) else np.array(nrows)
    rowrat = nrows/nrows.sum()
    ncols = np.ones(ncols) if isinstance(ncols, int) else np.array(ncols)
    colrat = ncols/ncols.sum()
    height = rect.y1 - rect.y0 - margin[2] - margin[3] - (nrows.size - 1)*rectspacing
    width = rect.x1 - rect.x0 - margin[0] - margin[1] - (ncols.size - 1)*rectspacing
    if width <=0 or height <= 0:
        raise ValueError('Not enough space to split.')
    height = np.floor(height*rowrat*1000)/1000
    width = np.floor(width*colrat*1000)/1000

    rowlocs = (height + rectspacing).cumsum()
    rowstart = rect.y0 + margin[2] + np.hstack((np.array([0]), rowlocs[:-1]))
    rowend = rect.y0 + margin[2] + rowlocs - rectspacing

    collocs = (width + rectspacing).cumsum()
    colstart = rect.x0 + margin[0] + np.hstack((np.array([0]), collocs[:-1]))
    colend = rect.x0 + margin[0] + collocs - rectspacing

    if flatten is not None:
        if flatten == 0:
            split = [pymupdf.Rect(cs, rs, ce, re) for cs,ce in zip(colstart, colend) for rs,re in zip(rowstart, rowend)]
        elif flatten == 1:
            split = [pymupdf.Rect(cs, rs, ce, re) for rs,re in zip(rowstart, rowend) for cs,ce in zip(colstart, colend)]
        else:
            raise ValueError('`flatten` must be 0 or 1.' )
    else:
        split = [[pymupdf.Rect(cs, rs, ce, re) for cs,ce in zip(colstart, colend)] for rs,re in zip(rowstart, rowend)]
    return split

def insrttxt(text: str, doc: pymupdf.Document | None = None, page: int | None = None, loc: tuple[float, float, int] | None = None, 
             split: list[pymupdf.Rect] | None = None, fontname: str = "Courier", fontsize: float = 11, font_aspect_ratio: float = 0.6, 
             indent_1: int = 0, indent_2: int = 0, linespacing: float = 0.2, paraspacing: float = 0.2, next_line: bool = False, 
             **kwargs) -> tuple:
    '''Inserts text into a specified position on a PDF page.

    Args:
        text: Text to insert.
        doc: A pymupdf.Document object. If None, a new document will be automatically created.
        page: The target page for insertion. If None or the specified page does not exist, a new page will be created. See doc.load_page for details.
        loc: A 3-element tuple (x, y, n) specifying the insertion coordinates and the index of the corresponding region within split.
            If None, it will be set to the top-left corner of the first region in split.
            If the coordinates are not within a region, they will be reset to the top-left corner of the next region in split (which may be the first region of the next page).
            If the specified region index n is out of the bounds of split, a new page will be created, and the location will be reset to the top-left corner of the first region.
        split: A list composed of pymupdf.Rect objects.
        fontname: The font name. It is recommended to use a monospaced font; otherwise, line breaks may not occur at appropriate positions.
        fontsize: The font size.
        font_aspect_ratio: Specifies the aspect ratio (height to width) of the font.
        indent_1: Number of characters for the indentation of the first line of a paragraph. If the loc horizontal position is greater than this indentation, the starting print position follows loc.
        indent_2: Number of characters for the indentation of the remaining lines in a paragraph.
        linespacing: Line spacing.
        paraspacing: Paragraph spacing.
        next_line: Whether to move to the next line after all text has been printed.
        kwargs: Other arguments. See pymupdf.Shape.insert_text for details.

    Returns:
        A tuple representing the next insertion coordinates and its corresponding region index (x, y, n).
    '''
    if doc is None:
        doc = pymupdf.open()
    
    if page is None or doc.page_count == 0 or page + 1 > doc.page_count:
        page = doc.new_page() 
    else:
        page = doc.load_page(page)
    
    if split is None:
        split = rectsplit(page.bound())
    lensplit = len(split)

    if loc is None:
        loc = (split[0].x0, split[0].y0 + fontsize, 0)
    elif loc[2] >= lensplit:
        page = doc.new_page()
        loc = (split[0].x0, split[0].y0 + fontsize, 0)
    elif not split[loc[2]].contains(pymupdf.Point(loc[0], loc[1])):
        if loc[2] < lensplit - 1:
            loc = (split[loc[2] + 1].x0, split[loc[2] + 1].y0 + fontsize, loc[2] + 1)
        else:
            page = doc.new_page()
            loc = (split[0].x0, split[0].y0 + fontsize, 0)

    locx, locy, nrect = loc
    text = text.split('\n')
    lentext = len(text)

    shape = page.new_shape()
    
    for n, txt in enumerate(text):
        rect_roll = 0 # the number of rects rolled
        locx = max(locx, split[nrect].x0 + indent_1 * fontsize * font_aspect_ratio)
        ts = 0
        lentxt = len(txt)
        while ts < lentxt:
            while locx + fontsize * font_aspect_ratio <= split[nrect].x1 and locy <= split[nrect].y1:
                tc = np.floor((split[nrect].x1 - locx) / (fontsize * font_aspect_ratio)).astype(dtype = np.int32)
                td = ts + tc
                point = pymupdf.Point(locx, locy)
                shape.insert_text(point, txt[ts:td], fontname = fontname, fontsize = fontsize, **kwargs)
                if td >= lentxt:
                    if n == lentext - 1: # all paragraphs finished
                        if next_line != '\n':
                            locx += (lentxt - ts) * fontsize * font_aspect_ratio
                        else:
                            locx = split[nrect].x0
                            locy += fontsize * (1 + linespacing)
                    else: # current paragraph finished
                        locx = split[nrect].x0 + indent_1 * fontsize * font_aspect_ratio
                        locy += fontsize * (1 + paraspacing)
                        if locy > split[nrect].y1:
                            nrect += 1
                            if nrect == lensplit:
                                shape.finish()
                                shape.commit()
                                nrect = 0
                                page = doc.new_page()
                                shape = page.new_shape()
                            locx = split[nrect].x0 + indent_1 * fontsize * font_aspect_ratio
                            locy = split[nrect].y0 + fontsize
                    ts = td
                    break
                else:
                    ts = td
                    locx = split[nrect].x0 + indent_2 * fontsize * font_aspect_ratio
                    locy += fontsize * (1 + linespacing)
            if nrect == lensplit - 1 or ts >= lentxt:
                shape.finish()
                shape.commit()
            if ts < lentxt:
                nrect += 1
                if ts == 0:
                    rect_roll += 1
                    if rect_roll >= lensplit:
                        raise ValueError("Not enough space to print in every Rect.")
                if nrect == lensplit:
                    nrect = 0
                    page = doc.new_page()
                    shape = page.new_shape()
                locx = split[nrect].x0 + (indent_1 if ts == 0 else indent_2) * fontsize * font_aspect_ratio
                locy = split[nrect].y0 + fontsize
    return locx, locy, nrect

def tabadj(arr: np.array, th: float = 0, pct: float = 80, max_width: int | None = None, retn_rat: bool = False) -> tuple:
    '''To reduce the printing area, automatically adjust the table width and height.

    Args:
        arr: A numpy.array with string elements.
        th: The minimum percentage by which the table size should be reduced in each iteration, must be >= 0.
        pct: The percentile for column widths.
        max_width: The maximum column width (number of characters).
        retn_rat: Whether to return the final reduction ratio of the table size.
        
    Returns: 
        A tuple containing the height of each row, the width of each column, the height of each row's text box, 
        the width of each row's text box, and optionally the final reduction ratio of the table size.
    '''
    if th < 0 or pct < 0:
        raise ValueError('`th` and `pct` must be non-negative.')
    datalen = np.vectorize(len)(arr)
    datalen = np.where(datalen == 0, 1, datalen)
    numcols = arr.shape[1]
    boxwd = datalen.copy()
    boxht = np.ones(datalen.shape)
    
    nlexist = np.vectorize(str.__contains__)(arr, '\n')
    nlindex = np.where(nlexist)
    nltxtlen = {}
    for i,j in zip(*nlindex):
        txtlen = np.array([len(x) for x in arr[i, j].split('\n')])
        nltxtlen[(int(i),int(j))] = txtlen
        boxwd[i,j] = txtlen.max()
        boxht[i,j] = len(txtlen)
    
    lencol = np.max(boxwd, axis = 0)
    lenrow = np.max(boxht, axis = 1)
    
    if pct >= 100:
        return lenrow, lencol, boxht, boxwd
    
    lenpet = np.percentile(boxwd, pct, axis = 0, method = 'lower')
    if max_width and max_width > 0:
        lenpet = np.where(lenpet > max_width, max_width, lenpet)
    colminus = lencol - lenpet
    
    rats = []
    xinds = []
    rowht = []
    colsum = lencol.sum()
    rowsum = lenrow.sum()
    init_area = colsum * rowsum
    new_area = init_area
    for y in range(numcols):
        minus = colminus[y] * rowsum
        xadd = 0
        xind = [int(i) for i in np.where(boxwd[:, y] > lenpet[y])[0]]
        xinds.append(xind)
        rowadjs = []
        for x in xind:
            if nlexist[x, y]:
                rowadj = np.ceil(nltxtlen[(x, y)] / lenpet[y]).sum()
            else:
                rowadj = np.ceil(datalen[x, y] / lenpet[y])
            rowadjs.append(rowadj)
            xadd += rowadj - lenrow[x]
        rowht.append(rowadjs)
        add = xadd * (colsum - colminus[y])
        rats.append((minus - add) / init_area)

    posy = int(np.argmax(rats))
    posx = xinds[posy]
    rat = rats[posy]
    
    while rat > th:
        boxwd[posx, posy] = lenpet[posy]
        boxht[posx, posy] = rowht[posy]
        lencol[posy] = lenpet[posy]
        lenrow[posx] = np.max(boxht[posx, :], axis = 1)

        lenpet = np.percentile(boxwd, pct, axis = 0, method = 'lower')
        if max_width and max_width > 0:
            lenpet = np.where(lenpet > max_width, max_width, lenpet)
        colminus = lencol - lenpet

        rats = []
        xinds = []
        rowht = []
        colsum = lencol.sum()
        rowsum = lenrow.sum()
        new_area = colsum * rowsum
        for y in range(numcols):
            minus = colminus[y] * rowsum
            xadd = 0
            xind = [int(i) for i in np.where(boxwd[:, y] > lenpet[y])[0]]
            xinds.append(xind)
            rowadjs = []
            for x in xind:
                if nlexist[x, y]:
                    rowadj = np.ceil(nltxtlen[(x, y)] / lenpet[y]).sum()
                else:
                    rowadj = np.ceil(datalen[x, y] / lenpet[y])
                rowadjs.append(rowadj)
                xadd += rowadj - lenrow[x]
            rowht.append(rowadjs)
            add = xadd * (colsum - colminus[y])
            rats.append((minus - add) / new_area)

        posy = int(np.argmax(rats))
        posx = xinds[posy]
        rat = rats[posy]
    
    if retn_rat:
        return lenrow, lencol, boxht, boxwd, new_area / init_area
    return lenrow, lencol, boxht, boxwd


def insrttab(df: pd.DataFrame, doc: pymupdf.Document | None = None, page: int | None = None, loc: tuple[float, float, int] | None = None, 
             split: list[pymupdf.Rect] | None = None, font_aspect_ratio: float = 0.6, head: bool = True, headfont: str = 'Courier-Bold',
             index: bool = True, nan: str = 'nan', datafont: str = "Courier", th: float = 0, pct: float = 100, max_width: int | None = None, 
             fitcol: bool = True, fontsize: float = 11, gridspacing: float = 0.2, txtalign_hz: str = 'center', txtalign_vt: str = 'center', 
             tabalign_hz: str = 'center', tabalign_vt: str = 'top', precision: int = 4, iter_display_limit: tuple = (1, 10), style: int = 2, 
             databar: str | list[str] = None, colorbar: list[tuple[float]] | None = None, **kwargs) -> tuple:
    '''Inserts a table into a specified position on a PDF page.
    
    Args:
        df: A pandas.DataFrame.
        doc: A pymupdf.Document object. If None, a new document will be automatically created.
        page: The target page for insertion. If None or the specified page does not exist, a new page will be created. See doc.load_page for details.
        loc: A 3-element tuple (x, y, n) specifying the insertion coordinates and the index of the corresponding region within split.
            If None, it will be set to the top-left corner of the first region in split.
            If the coordinates are not within a region, they will be reset to the top-left corner of the next region in split (which may be the first region of the next page).
            If the specified region index n is out of the bounds of split, a new page will be created, and the location will be reset to the top-left corner of the first region.
        split: A list composed of pymupdf.Rect objects. Inserts items sequentially through each Rect area (column by column, row by row).
            The number of columns per batch is auto-calculated based on the current Rect's dimensions.
            Recalculation for the next batch occurs only after the current batch's rows are fully populated.
        font_aspect_ratio: Specifies the aspect ratio (height to width) of the font.
        head: Whether to print the table header.
        headfont: Font name for printing table headers and row indexes. It is recommended to use a monospaced font; otherwise, line breaks may not occur at appropriate positions.
        index: Whether to print the table indexes.
        nan: Text annotation for NaN values.
        datafont: Font for printing table content.
        th: The minimum percentage by which the table size should be reduced in each iteration, must be >= 0.
        pct: The percentile for column widths.
        max_width: The maximum column width (number of characters).
        fitcol: Whether to shrink font size to fit the entire table into the print area when the page region width is insufficient.
        fontsize: Font size for printing the table.
        gridspacing: Spacing between grid cells.
        txtalign_hz: Horizontal alignment of text within cells: 'left', 'center', or 'right'.
        txtalign_vt: Vertical alignment of text within cells: 'top', 'center', or 'bottom'.
        tabalign_hz: Horizontal alignment of the table within the print area: 'left', 'center', or 'right'.
        tabalign_vt: Vertical alignment of the table within the print area: 'top', 'center', or 'bottom'.
        precision: Printing precision for floats. 
        iter_display_limit: Maximum length to display for iterable object. Default shows the first 10 characters of the first element.
        style: Specifies table style. Default 0: no borders; 1: three-line table; 2: adds horizontal lines between rows (excluding when indices are identical) based on style 1; 3: adds vertical lines between columns based on style 2; 4: adds left/right outer borders based on style 3.
        databar: Specifies column names for data bar visualization. Default None; can use list to specify multiple columns.
        colorbar: Specifies color for data bars. Defined by an RGB tuple with values between 0 and 1. Automatically generated if None.
        kwargs: Other arguments. See pymupdf.Shape.insert_text for details.

    Returns:
        A tuple representing the next insertion coordinates and its corresponding region index (x, y, n).
    '''
    if doc is None:
        doc = pymupdf.open()
    
    if page is None or doc.page_count == 0 or page + 1 > doc.page_count:
        page = doc.new_page() 
    else:
        page = doc.load_page(page)
    
    if split is None:
        split = rectsplit(page.bound())
    lensplit = len(split)
    
    if loc is None:
        loc = (split[0].x0, split[0].y0, 0)
    elif loc[2] >= lensplit:
        page = doc.new_page()
        loc = (split[0].x0, split[0].y0, 0)
    elif not split[loc[2]].contains(pymupdf.Point(loc[0], loc[1])):
        if loc[2] < lensplit - 1:
            loc = (split[loc[2] + 1].x0, split[loc[2] + 1].y0, loc[2] + 1)
        else:
            page = doc.new_page()
            loc = (split[0].x0, split[0].y0, 0)

    locx, locy, nrect = loc

    if isinstance(df.columns, pd.MultiIndex):
        dfhead = np.vectorize(repr)(df.columns)
    else:
        dfhead = df.columns.fillna(nan).map(lambda x:to_str(x, precision, iter_display_limit, nan)).to_numpy()
    if isinstance(df.index, pd.MultiIndex):
        dfind = np.vectorize(repr)(df.index)
    else:
        dfind = df.index.fillna(nan).map(lambda x:to_str(x, precision, iter_display_limit, nan)).to_numpy()
    dfdat = df.map(lambda x:to_str(x, precision, iter_display_limit, nan)).to_numpy()
    
    if index:
        dfdat = np.hstack([dfind.reshape(-1,1), dfdat])
        dfhead = np.hstack(['Ind' if df.index.name is None else str(df.index.name), dfhead])
    if head:
        dfdat = np.vstack([dfhead.reshape(1,-1), dfdat])
    if databar is not None:
        if not isinstance(databar, list):
            databar = [databar]
        barext = df[databar].agg(['min', 'max']).to_numpy()
        
        barlen = []
        for i,j in barext.T:
            if i >= 0:
                barlen.append(j)
            elif i < 0 and j > 0:
                barlen.append(j - i)
            elif j <= 0:
                barlen.append(-i)
        barlen = np.array(barlen)
        bararr = df[databar].to_numpy()
        bardat = np.divide(bararr, barlen, out=np.zeros_like(bararr), where=barlen!=0)
        dfcolumns = df.columns.to_list()
        barind = [dfcolumns.index(i) for i in databar]
        if index:
            barind = [i + 1 for i in barind]
        if colorbar is None:
            colorbar = palette(len(databar))
    
    lenrow, lencol, lentxtboxht, lentxtboxwd = tabadj(dfdat, th, pct, max_width)
    if txtalign_hz == 'left':
        alignwd = np.zeros(lentxtboxwd.shape)
    elif txtalign_hz == 'center':
        alignwd = (lencol - lentxtboxwd) * fontsize * font_aspect_ratio / 2
    elif txtalign_hz == 'right':
        alignwd = (lencol - lentxtboxwd) * fontsize * font_aspect_ratio
    else:
        raise ValueError('Unsupported value for parameter `txtalign_hz`.')
    if txtalign_vt == 'top':
        alignvt = np.zeros(lentxtboxht.shape)
    elif txtalign_vt == 'center':
        alignvt = (lenrow.reshape(-1,1) - lentxtboxht) * fontsize / 2
    elif txtalign_vt == 'bottom':
        alignvt = (lenrow.reshape(-1,1) - lentxtboxht) * fontsize
    else:
        raise ValueError('Unsupported value for parameter `txtalign_vt`.')

    linewid = fontsize * 0.03
    multlinewid = linewid * 3

    width = gridspacing * fontsize * 2 + lencol * fontsize * font_aspect_ratio
    height = gridspacing * fontsize * 2 + lenrow * fontsize
    
    realwid = split[nrect].x1 - split[nrect].x0
    realhgt = split[nrect].y1 - split[nrect].y0
    
    zoomin = (split[nrect].x1 - locx) / width.sum()
    zoomin = np.floor(zoomin * 1000) / 1000
    if fitcol and zoomin < 1:
        fontsize *= zoomin
        width *= zoomin
        height *= zoomin
        alignwd *= zoomin
        alignvt *= zoomin

    sumwid = 0
    sc = 1 if index else 0   #split tab on columns
    colnum = len(width)
    rownum = len(height)
    i = 0 #col index
    while i <= colnum:
        if i != colnum:
            if not index and width[i] > realwid:
                raise ValueError(f"Column {i} width ({width[i]:.2f}) > region width ({realwid:.2f}).")
            if index and i > 0 and (width[0] + width[i]) > realwid:
                raise ValueError(f"Index width + Column {i} width ({width[0]:.2f} + {width[i]:.2f}) > region width ({realwid:.2f}).")
        
        if i == colnum or locx + sumwid + width[i] > split[nrect].x1:
            sr = 1 if head else 0   #split tab on rows
            j = 0 # row index
            if i == 0:
                locx = split[nrect].x0
                locy = split[nrect].y0 + fontsize
                sumwid = 0
                continue
            tsc = i
            sumhgt = 0
            while j <= rownum:
                if j != rownum:
                    if not head and height[j] > realhgt:
                        raise ValueError(f"Row {j} height ({height[j]:.2f}) > region height ({realhgt:.2f}).")
                    if head and j > 0 and (height[0] + height[j]) > realhgt:
                        raise ValueError(f"Column index height + Row {j} height ({height[0]:.2f} + {height[j]:.2f}) > region height ({realhgt:.2f}).")
                
                if j == rownum or locy + sumhgt + height[j] > split[nrect].y1:
                    # tab horizontal alignment
                    width_space = split[nrect].x1 - sumwid - locx
                    if width_space > 0:
                        if tabalign_hz == 'left':
                            locx += multlinewid
                        elif tabalign_hz == 'center':
                            locx += width_space / 2
                        elif tabalign_hz == 'right':
                            locx += width_space - multlinewid
                    twidth = np.hstack([0, width[0], width[sc:tsc]]) if index else np.hstack([0, width[sc:tsc]])
                    cmwidth = np.cumsum(twidth)
                    cmwidth2 = cmwidth[2:-1] if index else cmwidth[1:-1]
                    if j == 0 or (j == sr and sr != rownum): # not enough space
                        nrect += 1
                        if nrect == lensplit:
                            page = doc.new_page()
                            nrect = 0
                        locx = split[nrect].x0
                        locy = split[nrect].y0
                        realwid = split[nrect].x1 - split[nrect].x0
                        realhgt = split[nrect].y1 - split[nrect].y0
                        continue
                    tsr = j
                    
                    # tab vertical alignment
                    if tabalign_vt == 'top':
                        locy += multlinewid
                    elif tabalign_vt == 'center':
                        locy += (split[nrect].y1 - sumhgt - locy) / 2
                    elif tabalign_vt == 'bottom':
                        locy += split[nrect].y1 - sumhgt - locy - multlinewid
                    # temp data to write
                    tdfdat = dfdat[sr:tsr, sc:tsc]
                    tlentxtboxht = lentxtboxht[sr:tsr, sc:tsc]
                    tlentxtboxwd = lentxtboxwd[sr:tsr, sc:tsc]
                    talignwd = alignwd[sr:tsr, sc:tsc]
                    talignvt = alignvt[sr:tsr, sc:tsc]
                    
                    if head:
                        tdfdat = np.vstack([dfdat[0:1, sc:tsc], tdfdat])
                        tlentxtboxht = np.vstack([lentxtboxht[0:1, sc:tsc], tlentxtboxht])
                        tlentxtboxwd = np.vstack([lentxtboxwd[0:1, sc:tsc], tlentxtboxwd])
                        talignwd = np.vstack([alignwd[0:1, sc:tsc], talignwd])
                        talignvt = np.vstack([alignvt[0:1, sc:tsc], talignvt])
                        if index:
                            tdfdat = np.hstack([np.vstack([dfdat[0:1, 0:1], dfdat[sr:tsr, 0:1]]), tdfdat])
                            tlentxtboxht = np.hstack([np.vstack([lentxtboxht[0:1, 0:1], lentxtboxht[sr:tsr, 0:1]]), tlentxtboxht])
                            tlentxtboxwd = np.hstack([np.vstack([lentxtboxwd[0:1, 0:1], lentxtboxwd[sr:tsr, 0:1]]), tlentxtboxwd])
                            talignwd = np.hstack([np.vstack([alignwd[0:1, 0:1], alignwd[sr:tsr, 0:1]]), talignwd])
                            talignvt = np.hstack([np.vstack([alignvt[0:1, 0:1], alignvt[sr:tsr, 0:1]]), talignvt])
                    elif index:
                        tdfdat = np.hstack([dfdat[sr:tsr, 0:1], tdfdat])
                        tlentxtboxht = np.hstack([lentxtboxht[sr:tsr, 0:1], tlentxtboxht])
                        tlentxtboxwd = np.hstack([lentxtboxwd[sr:tsr, 0:1], tlentxtboxwd])
                        talignwd = np.hstack([alignwd[sr:tsr, 0:1], talignwd])
                        talignvt = np.hstack([alignvt[sr:tsr, 0:1], talignvt])
                    
                    theight = np.hstack([0, height[0], height[sr:tsr]]) if head else np.hstack([0, height[sr:tsr]])
                    cmtheight = np.cumsum(theight)
                    txtstartx = locx + gridspacing * fontsize + cmwidth[:-1] + talignwd
                    tabstarty = locy + (0.76 + gridspacing) * fontsize + cmtheight[:-1]
                    txtstarty = tabstarty.reshape(-1,1) + talignvt
                    
                    shape = page.new_shape()
                    if databar is not None:
                        cmtheight3 = cmtheight[1:] if head else cmtheight.copy()
                        for n, db in enumerate(barind):
                            if db >= sc and db < tsc:
                                dbind = db - sc + 1 if index else db - sc
                                basex0 = locx + cmwidth[dbind]
                                dbrows = sr - 1 if index else sr
                                dbrown = tsr - 1 if index else tsr
                                bd = bardat[dbrows:dbrown, n]
                                bd = bd * twidth[dbind + 1]
                                if np.isnan(bd).all():
                                    continue
                                bdmin = np.nanmin(bd)
                                if bdmin < 0:
                                    basex0 -= bdmin
                                for dbt in range(len(cmtheight3[:-1])):
                                    color = colorbar[n]
                                    dbx0 = basex0
                                    dbx1 = dbx0 + bd[dbt]
                                    if dbx0 > dbx1:
                                        dbx0, dbx1 = dbx1, dbx0
                                        color = (0,0,1) # blue
                                    dby0 = locy + cmtheight3[dbt] 
                                    dby1 = locy + cmtheight3[dbt + 1] 
                                    dbrect = pymupdf.Rect(dbx0, dby0, dbx1, dby1)
                                    shape.draw_rect(dbrect)
                                    shape.finish(fill = color, width = 0, fill_opacity = 0.25)
                    
                    if style > 0:
                        linestart = pymupdf.Point(locx, locy - multlinewid / 2)
                        lineend = pymupdf.Point(locx + sumwid, locy - multlinewid / 2)
                        shape.draw_line(linestart, lineend)
                        shape.finish(width = multlinewid)
                        if head:
                            linestart = pymupdf.Point(locx, locy + height[0])
                            lineend = pymupdf.Point(locx + sumwid, locy + height[0])
                            shape.draw_line(linestart, lineend)
                            shape.finish(width = linewid * 2)
                        if index:
                            linestart = pymupdf.Point(locx + width[0], locy)
                            lineend = pymupdf.Point(locx + width[0], locy + sumhgt)
                            shape.draw_line(linestart, lineend)
                            shape.finish(width = linewid * 2)
                        linestart = pymupdf.Point(locx, locy + sumhgt + multlinewid / 2)
                        lineend = pymupdf.Point(locx + sumwid, locy + sumhgt + multlinewid / 2)
                        shape.draw_line(linestart, lineend)
                        shape.finish(width = multlinewid)
                    if style > 1:
                        cmtheight2 = cmtheight[2:-1] if head else cmtheight[1:-1]
                        if index and len(cmtheight2) > 0:
                            temp_ind = tdfdat[1:, 0] if head else tdfdat[:, 0]
                            for t in range(len(cmtheight2)):
                                if temp_ind[t] != temp_ind[t + 1]:
                                    ls = cmtheight2[t]
                                    linestart = pymupdf.Point(locx, locy + ls)
                                    lineend = pymupdf.Point(locx + sumwid, locy + ls)
                                    shape.draw_line(linestart, lineend)
                                    shape.finish(width = linewid)
                        else:
                            for ls in cmtheight2:
                                linestart = pymupdf.Point(locx, locy + ls)
                                lineend = pymupdf.Point(locx + sumwid, locy + ls)
                                shape.draw_line(linestart, lineend)
                                shape.finish(width = linewid)
                    if style > 2:
                        for ls in cmwidth2:
                            linestart = pymupdf.Point(locx + ls, locy)
                            lineend = pymupdf.Point(locx + ls, locy + sumhgt)
                            shape.draw_line(linestart, lineend)
                            shape.finish(width = linewid)
                    if style > 3:
                        linestart = pymupdf.Point(locx - multlinewid / 2, locy - multlinewid)
                        lineend = pymupdf.Point(locx - multlinewid / 2, locy + sumhgt + multlinewid)
                        shape.draw_line(linestart, lineend)
                        linestart = pymupdf.Point(locx + sumwid + multlinewid / 2, locy - multlinewid)
                        lineend = pymupdf.Point(locx + sumwid + multlinewid / 2, locy + sumhgt + multlinewid)
                        shape.draw_line(linestart, lineend)
                        shape.finish(width = multlinewid)
                    
                    for tx in range(tdfdat.shape[0]):
                        for ty in range(tdfdat.shape[1]):
                            tboxwd = int(tlentxtboxwd[tx,ty])
                            txt = tdfdat[tx,ty].split('\n')
                            txt = [t[s: s+tboxwd] for t in txt for s in range(0, len(t), tboxwd)]
                            for b, wtxt in enumerate(txt):
                                if txtalign_hz == 'left':
                                    wtxt = wtxt.ljust(tboxwd)
                                elif txtalign_hz == 'center':
                                    wtxt = wtxt.center(tboxwd)
                                elif txtalign_hz == 'right' :
                                    wtxt = wtxt.rjust(tboxwd)
                                point = pymupdf.Point(txtstartx[tx,ty], txtstarty[tx, ty] + b * fontsize)
                                if (tx == 0 and head) or (ty == 0 and index):
                                    shape.insert_text(point, wtxt, fontname = headfont, fontsize = fontsize, **kwargs)
                                else:
                                    shape.insert_text(point, wtxt, fontname = datafont, fontsize = fontsize, **kwargs)
                    
                    shape.commit()
                    sr = tsr

                    endy = locy + cmtheight[-1] + fontsize
                    if endy > split[nrect].y1 and not (i == colnum and j == rownum):
                        nrect += 1
                        if nrect == lensplit:
                            page = doc.new_page()
                            nrect = 0
                        locy = split[nrect].y0
                    else:
                        locy = float(endy)
                    locx = split[nrect].x0
                    
                    realwid = split[nrect].x1 - split[nrect].x0
                    realhgt = split[nrect].y1 - split[nrect].y0
                    
                    sumhgt = height[0] if head else 0
                    if j != rownum:
                        j -= 1
                else:
                    sumhgt += height[j]
                j += 1
            sumwid = width[0] if index else 0

            if i != colnum:
                i -= 1
            sc = tsc
        else:
            sumwid += width[i]
        i += 1
    return locx, locy, nrect

def insrtfig(fig: Figure | pymupdf.Document, doc: pymupdf.Document | None = None, page: int | None = None, 
             loc: tuple[float, float, int] | None = None, split: list[pymupdf.Rect] | None = None, dpi: float = 72, keep_proportion = True, 
             align_vt: str = 'center', align_hz: str = 'center', vector: bool = True, next_rect: bool = True) -> tuple:
    '''Inserts an image or another PDF page at a specified position on a PDF page.

    Args:
        fig: An image or another PDF page.
        doc: A pymupdf.Document object. If None, a new document will be automatically created.
        page: The target page for insertion. If None or the specified page does not exist, a new page will be created. See doc.load_page for details.
        loc: A 3-element tuple (x, y, n) specifying the insertion coordinates and the index of the corresponding region within split.
            If None, it will be set to the top-left corner of the first region in split.
            If the coordinates are not within a region, they will be reset to the top-left corner of the next region in split (which may be the first region of the next page).
            If the specified region index n is out of the bounds of split, a new page will be created, and the location will be reset to the top-left corner of the first region.
        split: A list composed of pymupdf.Rect objects.
        dpi: For a Figure object, specifies the resolution (dots per inch) of the inserted image.
        keep_proportion: Whether to maintain the fig's aspect ratio.
        align_vt: Vertical alignment of fig: 'top', 'center', or 'bottom'.
        align_hz: Horizontal alignment of fig: 'left', 'center', or 'right'.
        vector: For a Figure object, specifies whether to insert as vector graphics.
        next_rect: After image insertion, whether to move coordinates to the next available region.

    Returns:
        A tuple representing the next insertion coordinates and its corresponding region index (x, y, n).
    '''
    if doc is None:
        doc = pymupdf.open()
    
    if page is None or doc.page_count == 0 or page + 1 > doc.page_count:
        page = doc.new_page() 
    else:
        page = doc.load_page(page)
    
    if split is None:
        split = rectsplit(page.bound())
    lensplit = len(split)

    if loc is None:
        loc = (split[0].x0, split[0].y0, 0)
    elif loc[2] >= lensplit:
        page = doc.new_page()
        loc = (split[0].x0, split[0].y0, 0)
    elif not split[loc[2]].contains(pymupdf.Point(loc[0], loc[1])):
        if loc[2] < lensplit - 1:
            loc = (split[loc[2] + 1].x0, split[loc[2] + 1].y0, loc[2] + 1)
        else:
            page = doc.new_page()
            loc = (split[0].x0, split[0].y0, 0)
    
    locx, locy, nrect = loc
    rect = pymupdf.Rect(locx, locy, split[nrect].x1, split[nrect].y1)
    if keep_proportion:
        if isinstance(fig, Figure):
            aspect = float(fig.get_figwidth() / fig.get_figheight())
        elif isinstance(fig, pymupdf.Document):
            temp_rect = fig.load_page(-1).rect
            aspect = temp_rect.x1 / temp_rect.y1
        if rect.width / rect.height > aspect:
            width = rect.height * aspect
            if align_hz == 'left':
                rect.x1 = rect.x0 + width
            elif align_hz == 'center':
                align = (rect.width - width) / 2
                rect.x0 = rect.x0 + align
                rect.x1 = rect.x0 + width
            elif align_hz == 'right':
                align = rect.width - width
                rect.x0 = rect.x0 + align
                rect.x1 = rect.x0 + width
        else:
            height = rect.width / aspect
            if align_vt == 'top':
                rect.y1 = rect.y0 + height
            elif align_vt == 'center':
                align = (rect.height - height) / 2
                rect.y0 = rect.y0 + align
                rect.y1 = rect.y0 + height
            elif align_vt == 'bottom':
                align = rect.height - height
                rect.y0 = rect.y0 + align
                rect.y1 = rect.y0 + height
    if isinstance(fig, Figure):
        buffer = BytesIO()
        if vector:
            fig.savefig(buffer, format = 'pdf', dpi = dpi)
            temp_doc = pymupdf.open('pdf', stream = buffer.getvalue())
            page.show_pdf_page(rect, temp_doc)
            temp_doc.close()
        else:
            fig.savefig(buffer, format = 'png', dpi = dpi)
            page.insert_image(rect = rect, stream = buffer.getvalue())
    elif isinstance(fig, pymupdf.Document):
        page.show_pdf_page(rect, fig)
    if next_rect:
        nrect += 1
        if nrect < lensplit:
            locx = split[nrect].x0
            locy = split[nrect].y0
        else:
            locx = split[0].x0
            locy = split[0].y0
    else:
        locx = split[nrect].x0
        locy = rect.y1
    return locx, locy, nrect

class Report:
    def __init__(self, pagesize: tuple = (595, 842), margin: float | tuple[float] = 30, titlefont: str = 'Courier-Bold', titlesize: float = 17, 
                 titledelta: float = 2, txtfont: str = "Courier", txtsize: float = 11, font_aspect_ratio: float = 0.6) -> None:
        '''Initialize a PyMuPDF Document object.

        Args:
            pagesize: A tuple containing the (width, height) of the paper.
            margin: The width of the margin to preserve around the edges.
            titlefont: The font for document titles.
            titlesize: The font size for the document title.
            titledelta: The variation in font size between different heading levels.
            txtfont: The font for text.
            txtsize: The font size of text.
            font_aspect_ratio: Specifies the aspect ratio (height to width) of the font.
        '''
        self.pagesize = pagesize
        if isinstance(margin, (float, int)):
            margin = (margin,) * 4
        self.margin = margin
        self.titlefont = titlefont
        self.titlesize = titlesize
        self.titledelta = titledelta
        self.txtfont = txtfont
        self.txtsize = txtsize
        self.font_aspect_ratio = font_aspect_ratio
        self._is_closed = False
        
        self.doc = pymupdf.open(width = pagesize[0], height = pagesize[1])
        self.split = rectsplit(pymupdf.Rect(0,0,*pagesize), margin = margin)
        self.loc = (margin[0], margin[2], 0)
        self.toc = []
        self.new_page()
    
    def newline(self, fontsize: float = 11, start: int = 0, spacing: float = 0.3) -> None:
        '''Move the cursor to a specified position in the new line based on the font size.

        Args:
            fontsize: The font size.
            start: Number of characters to skip.
            spacing: Line spacing, expressed as a ratio of the font size.
        '''
        self.loc[0] = self.margin[0] + start * fontsize * self.font_aspect_ratio
        self.loc[1] += fontsize * (1 + spacing)
    
    def new_page(self) -> None:
        '''Add a new page and move the cursor to the start position.
        '''
        self.doc.new_page()
        self.loc = [self.margin[0], self.margin[2], 0]
    
    def close(self) -> None:
        '''Close the PyMuPDF Document if it is still open.
        '''
        if not self._is_closed:
            self.doc.close()
            self._is_closed = True

    def save(self, *args, **kwargs) -> None:
        '''Save the document.
        
        Args:
            args, kwargs: Refer to the pymupdf.Document.save method for details.
        '''
        self.doc.set_toc(self.toc, collapse = 0)
        last_page = 0
        foots = []
        for t in self.toc:
            if t[2] != last_page:
                foots.append(t[1:3])
                last_page = t[2]
        foots.append((foots[-1][0], self.doc.page_count + 1))
        for f1, f2 in zip(foots[:-1], foots[1:]):
            pages = list(range(f1[1]-1, f2[1]-1))
            txt = f1[0]
            self.footer(page = pages, text = txt, align = 'center')
            self.footer(page = pages, align = 'right')
        self.doc.save(*args, **kwargs)

    def text(self, text: str, split: list[pymupdf.Rect] | None = None, fontname: str = "Courier", fontsize: float = 11, font_aspect_ratio: float = 0.6, 
             indent_1: int = 0, indent_2: int = 0, linespacing: float = 0.3, paraspacing: float = 0.8, next_line: bool = False, **kwargs) -> None:
        '''Insert text at the current position in the document.
        
        Args:
            text: Text to insert.
            split: A list composed of pymupdf.Rect objects.
            fontname: The font name. It is recommended to use a monospaced font; otherwise, line breaks may not occur at appropriate positions.
            fontsize: The font size.
            font_aspect_ratio: Specifies the aspect ratio (height to width) of the font.
            indent_1: Number of characters for the indentation of the first line of a paragraph. If the loc horizontal position is greater than this indentation, the starting print position follows loc.
            indent_2: Number of characters for the indentation of the remaining lines in a paragraph.
            linespacing: Line spacing.
            paraspacing: Paragraph spacing.
            next_line: Whether to move to the next line after all text has been printed.
            kwargs: Other arguments. See pymupdf.Shape.insert_text for details.
        '''
        loc = insrttxt(text, doc = self.doc, page = -1, loc = self.loc, split = split or self.split, fontname = fontname, fontsize = fontsize, 
                       font_aspect_ratio = font_aspect_ratio, indent_1 = indent_1, indent_2 = indent_2,
                       linespacing = linespacing, paraspacing = paraspacing, next_line = next_line, **kwargs)
        self.loc = list(loc)

    def table(self, df: pd.DataFrame, split: list[pymupdf.Rect] | None = None, font_aspect_ratio: float = 0.6, head: bool = True, 
            index: bool = True, nan: str = '', th: float = 0, pct: float = 100, max_width: int | None = None, fitcol: bool = True, 
            fontsize: float = 11, gridspacing: float = 0.2, txtalign_hz: str = 'center', txtalign_vt: str = 'center', 
            tabalign_hz: str = 'center', tabalign_vt: str = 'top', precision: int = 4, iter_display_limit: tuple = (1, 10), style: int = 2, 
            databar: str | list[str] = None, colorbar: list[tuple[float]] | None = None, **kwargs) -> None:
        '''Insert a table at the current position in the document.
        
        Args:
            df: A pandas.DataFrame.
            split: A list composed of pymupdf.Rect objects. Inserts items sequentially through each Rect area (column by column, row by row).
                The number of columns per batch is auto-calculated based on the current Rect's dimensions.
                Recalculation for the next batch occurs only after the current batch's rows are fully populated.
            font_aspect_ratio: Specifies the aspect ratio (height to width) of the font.
            head: Whether to print the table header.
            index: Whether to print the table indexes.
            nan: Text annotation for NaN values.
            th: The minimum percentage by which the table size should be reduced in each iteration, must be >= 0.
            pct: The percentile for column widths.
            max_width: The maximum column width (number of characters).
            fitcol: Whether to shrink font size to fit the entire table into the print area when the page region width is insufficient.
            fontsize: Font size for printing the table.
            gridspacing: Spacing between grid cells.
            txtalign_hz: Horizontal alignment of text within cells: 'left', 'center', or 'right'.
            txtalign_vt: Vertical alignment of text within cells: 'top', 'center', or 'bottom'.
            tabalign_hz: Horizontal alignment of the table within the print area: 'left', 'center', or 'right'.
            tabalign_vt: Vertical alignment of the table within the print area: 'top', 'center', or 'bottom'.
            precision: Printing precision for floats. 
            iter_display_limit: Maximum length to display for iterable object. Default shows the first 10 characters of the first element.
            style: Specifies table style. Default 0: no borders; 1: three-line table; 2: adds horizontal lines between rows (excluding when indices are identical) based on style 1; 3: adds vertical lines between columns based on style 2; 4: adds left/right outer borders based on style 3.
            databar: Specifies column names for data bar visualization. Default None; can use list to specify multiple columns.
            colorbar: Specifies color for data bars. Defined by an RGB tuple with values between 0 and 1. Automatically generated if None.
            kwargs: Other arguments. See pymupdf.Shape.insert_text for details.
        '''
        loc = insrttab(df, doc = self.doc, page = -1, loc = self.loc, split = split,  font_aspect_ratio = font_aspect_ratio, head = head, 
            headfont = self.titlefont, index = index, nan = nan, datafont = self.txtfont, th = th, pct = pct, max_width = max_width, 
            fitcol = fitcol, fontsize = fontsize, gridspacing = gridspacing, txtalign_hz = txtalign_hz, txtalign_vt = txtalign_vt, 
            tabalign_hz = tabalign_hz, tabalign_vt = tabalign_vt, precision = precision, iter_display_limit = iter_display_limit, style = style, 
            databar = databar, colorbar = colorbar, **kwargs)
        self.loc = list(loc)


    def figure(self, fig: Figure | pymupdf.Document, split: list[pymupdf.Rect] | None = None, dpi: float = 72, keep_proportion = True, 
             align_vt: str = 'top', align_hz: str = 'center', vector: bool = True, next_rect: bool = True) -> None:
        '''Insert an image or another PDF page at the current position in the document.

        Args:
            fig: An image or another PDF page.
            split: A list composed of pymupdf.Rect objects.
            dpi: For a Figure object, specifies the resolution (dots per inch) of the inserted image.
            keep_proportion: Whether to maintain the fig's aspect ratio.
            align_vt: Vertical alignment of fig: 'top', 'center', or 'bottom'.
            align_hz: Horizontal alignment of fig: 'left', 'center', or 'right'.
            vector: For a Figure object, specifies whether to insert as vector graphics.
            next_rect: After image insertion, whether to move coordinates to the next available region.
        '''
        loc = insrtfig(fig, doc = self.doc, page = -1, loc = self.loc, split = split or self.split, dpi = dpi, keep_proportion = keep_proportion, 
                       align_vt = align_vt, align_hz = align_hz, vector = vector, next_rect = next_rect)
        self.loc = list(loc)
        
    def add_file_annot(self, obj: pd.DataFrame | str | BytesIO, filename: str, to_excel_kwargs: dict = {}, **kwargs) -> None:
        '''To attach another file at the current position in the document.

        Args:
            obj: A pandas DataFrame, string, or BytesIO object.
            filename: File name.
            kwargs: Refer to the pymupdf.Page.add_file_annot method for details.
        '''
        if isinstance(obj, pd.DataFrame):
            buff = BytesIO()
            obj.to_excel(buff, **to_excel_kwargs)
        elif isinstance(obj, str):
            buff = BytesIO(obj.encode('utf-8'))
        else:
            buff = obj
        point = pymupdf.Point(self.loc[0] + 10, self.loc[1] - 18) # 18 is icon height.
        self.doc.load_page(-1).add_file_annot(point, buff.getvalue(), filename, **kwargs)
        self.loc[0] += 28

    def current_headnum(self) -> list[int]:
        '''Return the current chapter numbers list, 1 based.

        Returns:
            A list of integer.
        '''
        headnum = []
        if len(self.toc) == 0:
            return [1]
        num = np.array([t[0] for t in self.toc])
        for i in range(num.max()):
            locn = np.where(num == i + 1)[0]
            lenlocn = len(locn)
            if lenlocn > 0:
                headnum.append(lenlocn)
                num = num[locn[-1] + 1:]
        return headnum

    def heading(self, level: int, text: str, align_hz: str, num: bool = False, **kwargs) -> int:
        '''Add a new line and print the heading.

        Args:
            level: Level of heading, 0-based. 0 means the title.
            text: The text of the heading.
            align_hz: Horizontal alignment of the heading: 'left', 'center', or 'right'.
            num: If True, print the current heading number before the text.
            kwargs: Other arguments. See pymupdf.Shape.insert_text for details.
        Returns:
            The font size of the current heading.
        '''
        if num:
            cnum = self.current_headnum()
            lencnum = len(cnum)
            if level > 0 and level < lencnum:
                cnum[level] += 1
            elif level >= lencnum:
                cnum += [1]* (level - lencnum + 1)
            if len(cnum) > 1:
                cnumstr = [str(i) for i in cnum[1: level+1]]
                text = '.'.join(cnumstr) + '. ' + text
        fontsize = self.titlesize - level * self.titledelta
        width = len(text) * fontsize * self.font_aspect_ratio
        space = self.pagesize[0] - self.loc[0] - self.margin[3] - width
        if align_hz == 'left':
            indent = 0
        elif align_hz == 'center':
            indent = space / fontsize / self.font_aspect_ratio / 2
        elif align_hz == 'right':
            indent = space / fontsize / self.font_aspect_ratio
        self.toc.append((level + 1, text, self.doc.page_count, self.loc[1]))
        self.newline(fontsize = fontsize)
        self.text(text, fontname = self.titlefont, fontsize = fontsize, indent_1 = indent, **kwargs)
        return fontsize
    
    def footer(self, page: int | list[int], text: str | None = None, align: str = 'right', fontsize: float = 11, **kwargs) -> None:
        '''Insert footers on specified pages.

        Args:
            page: Page number(s), either a single page number or a list of page numbers.
            text: The text to be inserted; defaults to the page number.
            align: The horizontal position of the footer, supporting 'left', 'center', or 'right'.
            fontsize: The font size.
            kwargs: Other arguments. See pymupdf.Page.insert_text for details.
        '''
        if not isinstance(page, list):
            page = [page]
        width = self.pagesize[0] - self.margin[0] - self.margin[1]
        y_loc = self.pagesize[1] - self.margin[3] + fontsize
        for page_num in page:
            pg = self.doc.load_page(page_num)
            txt = text or str(page_num + 1)
            available = width - len(txt) * fontsize * self.font_aspect_ratio
            if align == 'left':
                x_loc = self.margin[0]
            elif align == 'center':
                x_loc = self.margin[0] + available / 2
            elif align == 'right':
                x_loc = self.margin[0] + available
            else:
                raise ValueError('Unsupported value for parameter `align`.')
            pg.insert_text(point = pymupdf.Point(x_loc, y_loc), text = txt, fontname = self.txtfont, fontsize = fontsize, **kwargs)

class ModReport(Report):
    def __init__(self, frame:Frame, title: str = 'Model', developer:str = 'developer', **kwargs) -> None:
        '''Initialize a PyMuPDF Document object for a model Frame object.

        Args:
            frame: A model Frame object.
            title: Model title.
            developer: Developer name.
            kwargs:
                pagesize: A tuple containing the (width, height) of the paper.
                margin: The width of the margin to preserve around the edges.
                titlefont: The font for document titles.
                titlesize: The font size for the document title.
                titledelta: The variation in font size between different heading levels.
                txtfont: The font for text.
                txtsize: The font size of text.
                font_aspect_ratio: Specifies the aspect ratio (height to width) of the font.
        '''
        super().__init__(**kwargs)
        self.frame = frame
        self.title = title
        self.developer = developer
        self.heading(0, f"{title} Report", 'center')
        self.newline(fontsize= self.titlesize, spacing= 0.8)
    
    def close(self) -> None:
        '''Close the PyMuPDF Document if it is still open.
        '''
        if not self._is_closed:
            self.frame = None
        super().close()
    
    def design(self) -> None:
        '''Generate a chapter covering the model design and a brief sample description.
        '''
        frame = self.frame
        datadesc = frame.describe_sample()
        
        fontsize = self.heading(1, 'Model Design', 'left', num = True)
        self.newline(fontsize= fontsize)
        
        localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        datainfo = pd.DataFrame(data = {0: [self.developer, localtime, frame._time, frame._flag, '']}, 
                    index = [f"{'Developer:':>15}", f"{'Report Time:':>15}", f"{'Time Var:':>15}", f"{'Flag:':>15}", f"{'Samples:':>15}"])
        fontsize -= self.titledelta
        self.table(datainfo, head = False, style = 0, fontsize = fontsize, txtalign_hz= 'left', tabalign_hz = 'left')
        
        if isinstance(datadesc, dict):
            for s in frame._samp_labels:
                self.table(datadesc[s], fontsize = fontsize, style = 1)
        elif isinstance(datadesc, pd.DataFrame):
            self.table(datadesc, fontsize = fontsize, style = 1)
    
    def describe_feature(self) -> None:
        '''Generate a chapter describing the model features.
        '''
        frame = self.frame
        ftsdesc = frame.describe_feature()
        view_des = ['Features', 'Dtype', 'Count', 'Missing', 'Missing_Rate', 'Unique']
        if len(frame._floatvars) > 0:
            view_des += ['Mean', 'Min', 'Max']
        if len(frame._catvars) > 0:
            view_des += ['Top', 'Freq']

        self.new_page()
        heading = 'Feature Description'
        fontsize = self.heading(1, heading, align_hz = 'left', num = True)
        self.add_file_annot(ftsdesc, heading + ".xlsx", icon = 'Paperclip')
        
        self.newline(fontsize= fontsize, spacing= -0.5)
        self.table(ftsdesc[view_des], databar = 'Missing_Rate')

    def bins(self, precision: int = 4, iter_display_limit: tuple = (1, 10)) -> None:
        '''Generate a chapter for the feature binning results.

        Args:
            precision: Printing precision for floats. 
            iter_display_limit: Maximum length to display for iterable object. Default shows the first 10 characters of the first element.
        '''
        frame = self.frame
        config = frame._config.get('split')
        fts_bins = frame.binstats().reset_index()
        fts_bins.sort_values(['ks', 'Features', 'bin'], ascending = [False, True, True], inplace = True)
        fts_bins.set_index('Features', inplace = True)
        fts_bins['split'] = fts_bins['split'].astype(object)
        itv_ind = (fts_bins['bin'] == 0) & (fts_bins['split'].map(lambda x: isinstance(x, pd.Interval))) 
        fts_bins.loc[itv_ind, 'split'] = fts_bins.loc[itv_ind, 'split'].map(lambda x: pd.Interval(x.left, x.right, closed = 'both'))
        
        nan_ind = pd.Series(False, index = fts_bins.index)
        for k, v in frame._bins.items(): #display the bin that nan merged to.
            fillnan = v.get('fillnan')
            if fillnan is not None:
                nan_ind = nan_ind | ((fts_bins.index == k) & (fts_bins['split'] == fillnan))
        fts_bins_x = fts_bins.copy()
        fts_bins_x.loc[nan_ind, 'split'] = fts_bins_x.loc[nan_ind,'split'].map(lambda x: f"{x} or nan")

        fts_bins_v = fts_bins[['bin', 'split', 'badcnt', 'goodcnt', 'binsprop', 'badrate', 'woe_bin', 'iv', 'lift', 'ks']].copy()
        fts_bins_v.loc[nan_ind, 'split'] = fts_bins_v.loc[nan_ind,'split'].map(lambda x: f"{to_str(x, precision, iter_display_limit)} or nan")
        
        self.new_page()
        heading = 'Feature Bins'
        fontsize = self.heading(1, heading, align_hz = 'left', num = True)
        self.add_file_annot(fts_bins_x, heading + ".xlsx", icon = 'Paperclip')
        
        self.newline(fontsize = fontsize, spacing = 0.8)
        fontsize -= self.titledelta
        self.text('Spliting Params:', fontname = self.titlefont, fontsize = fontsize, indent_1 = 2)
        # self.text(str(config), fontname = self.txtfont, fontsize = fontsize)
        config = dict2list(config, n_col = 2)
        self.table(pd.DataFrame(config), fontsize = fontsize, index = False, head = False, txtalign_hz = 'right', nan = 'None')
        
        self.newline(fontsize = fontsize)
        self.table(fts_bins_v, precision = precision, iter_display_limit = iter_display_limit, databar = ['binsprop', 'badrate'], nan = 'nan')
        
    def filter(self):
        '''Generate a chapter for the feature filtering results.
        '''
        frame = self.frame
        config = frame._config['drop']
        drop_reason = pd.DataFrame.from_dict(frame._drop, orient = 'index').reset_index()
        drop_reason.rename({'index': 'Features'}, axis = 1, inplace = True)

        self.new_page()
        heading = 'Features Filtering'
        fontsize = self.heading(1, heading, align_hz = 'left', num = True)
        self.add_file_annot(drop_reason, heading + ".xlsx", icon = 'Paperclip')

        self.newline(fontsize = fontsize, spacing = 0.8)
        fontsize -= self.titledelta
        self.text('Dropping Params:', fontname = self.titlefont, fontsize = fontsize, indent_1 = 2)
        # self.text(str(config), fontname = self.txtfont, fontsize = fontsize, indent_1 = 2)
        config = dict2list(config, n_col = 2)
        self.table(pd.DataFrame(config), fontsize = fontsize, index = False, head = False, txtalign_hz = 'right', nan = 'None')

        self.newline(fontsize = fontsize)
        self.table(drop_reason, style = 3)
        
    def analysis(self, y_true: pd.Series, y_score: pd.Series, flag: str, label: str | None = None, time: pd.Series | None = None, 
                 fig_bins: int = 50, tab_bins: int = 20, time_bins: int = 10, reverse: bool = False) -> None:
        '''Generate a chapter containing the model analysis and evaluation based on the given true values and scores.

        Args:
            y_true: Ground truth values for the samples.
            y_score: Predicted probabilities or scores from the model.
            flags: Name of true values.
            label: Name of the sample set.
            time: Sample time partition. Enables evaluation grouped by time.
            fig_bins: Number of bins for plotting the score distribution histogram.
            tab_bins: Number of bins for creating the score ranking table.
            time_bins: Number of bins for the score ranking table within each time partition.
            reverse: Whether to sort the `y_score` bins in reverse order.
        '''
        frame = self.frame
        Flag = flag.capitalize()
        samp_label = label.capitalize() if label else 'Sample'
        if y_score.isna().any():
            raise ValueError('y_score contains nan.')
        
        fig = plot_score(y_true, y_score, time, bins = fig_bins, fontsize = self.txtsize, alpha = 0.5, density = True)
        qcut = frame.ranking(y_true, y_score, split = 'qcut', q = tab_bins, reverse = reverse)
        chi2 = frame.ranking(y_true, y_score, split = 'chi2', reverse = reverse, maxbins = tab_bins, minbin = 0.01, woediff = 0)
        
        buffer = BytesIO()
        excelwriter = pd.ExcelWriter(buffer)
        sheet = f"ranking table"
        qcut.to_excel(excelwriter, sheet_name = sheet)
        chi2.to_excel(excelwriter, sheet_name = sheet, startrow = len(qcut) + 2)

        time_tab = {}
        if time is not None:
            time_tab = frame.ranking_bytime(y_true, y_score, time, same_cut = True, split = ['qcut', 'chi2'], q = time_bins, reverse = reverse, maxbins = time_bins, minbin = 0.01, woediff = 0)
            for c, v in time_tab.items():
                startrow = 0
                for t, d in v.items():
                    d.to_excel(excelwriter, sheet_name=f'{c} split by time', startrow = startrow)
                    startrow += len(d) + 2
        excelwriter.close()
        
        # pdf
        self.new_page()
        heading = f"{samp_label} Analysis on {Flag}"
        fontsize = self.heading(1, heading, align_hz = 'left', num = True)
        self.add_file_annot(buffer, heading + '.xlsx', icon = 'Paperclip')
        self.newline(fontsize = fontsize)
        self.figure(fig, next_rect = False)
        plt.close(fig)
        
        self.newline(fontsize = fontsize)
        heading = f"{samp_label} Scorecard Ranking Table on {Flag}"
        fontsize = self.heading(2, heading, align_hz = 'left', num = True)
        self.newline(fontsize = fontsize)
        
        self.table(qcut, databar = ['binsprop', 'badrate'])
        self.table(chi2, databar = ['binsprop', 'badrate'])
        
        if time_tab:
            for k, v in time_tab.items():
                self.newline(fontsize = fontsize)
                heading = f'{k.capitalize()} Split by Time of {samp_label} on {Flag}'
                fontsize = self.heading(2, heading, align_hz = 'left', num = True)
                self.newline(fontsize = fontsize)
                for t, d in v.items():
                    self.table(d, databar = ['binsprop', 'badrate'])
    
    def plotcuts(self, samp: str | pd.DataFrame = 'all', select_fts: list[str] | None = None, drop: bool = False, figsize: tuple = (12,9), 
                 show_name: bool = False, show_label: bool = False, precision: int = 4, iter_display_limit: tuple = (1, 10), 
                 rotation: float = -30, cores: int = 1) -> None:
        '''Generate a chapter containing the model binning plots.

        Args:
            samp: Sample label or a pandas DataFrame. Defaults to 'all', which indicates using all samples.
            select_fts: Plot only the specified features. If provided, only features in this list will be visualized.
            drop: If True, features that were dropped during preprocessing will not be plotted, this has lower priority than `select_fts`.
            figsize: Figure size for each plot, specified as (width, height) in inches.
            show_name: Whether to display the feature name on the plot.
            show_label: Whether to display the bin labels on the x-axis instead of simple bin indices.
            precision: Printing precision for floats. 
            iter_display_limit: Maximum length to display for iterable object. Default shows the first 10 characters of the first element.
            rotation: Rotation angle (in degrees) for the x-axis tick labels. Useful for preventing overlapping with long bin labels. 
            cores: Number of CPU cores to use.
        '''
        frame = self.frame
        train_label = frame.train_label
        if not select_fts:
            select_fts = frame.select if drop else getattr(frame, 'x_' + train_label).columns.to_list()
        
        if isinstance(samp, str):
            samp_lable = samp
            if samp == 'all':
                flag = pd.concat([getattr(frame, 'y_' + s) for s in frame._samp_labels])
                time = pd.concat([getattr(frame, 'time_' + s) for s in frame._samp_labels]) if frame._time else None
                cuts = pd.concat([getattr(frame, 'x_' + s)[select_fts] for s in frame._samp_labels])
                cuts, filled = frame.transform(samp = cuts, woe = False, retnfill = True, warn = False)
                bins = frame.binsagg(cuts, flag, init_bins = filled, cores = cores)
            else:
                flag = getattr(frame, 'y_' + samp)
                time = getattr(frame, 'time_' + samp) if frame._time else None
                if samp == train_label:
                    cuts = frame._cuts[select_fts]
                    bins = {i: frame._bins.get(i) for i in select_fts}
                else:
                    cuts = getattr(frame, 'x_' + samp)[select_fts]
                    cuts, filled = frame.transform(samp = cuts, woe = False, retnfill = True)
                    bins = frame.binsagg(cuts, flag, init_bins = filled, cores = cores, warn = False)
        elif isinstance(samp, pd.DataFrame):
            samp_lable = 'data'
            if frame._flag in samp:
                flag = pd.to_numeric(samp[frame._flag], downcast= 'signed')
            else:
                raise ValueError('Flag must be in samp.')
            if frame._time and frame._time in samp:
                time = samp[frame._time]
            else:
                time = None
            select_fts = [i for i in select_fts if i in samp]
            cuts, filled = frame.transform(samp = samp[select_fts], woe = False, retnfill = True, warn = False)
            bins = frame.binsagg(cuts, flag, init_bins = filled, cores = cores)
        else:
            raise TypeError('Unsupported type for parameter `samp`.')
        
        frame.logger.info("Drawing bins figure...")

        self.new_page()
        fontsize = self.heading(1, f'{samp_lable.capitalize()} Samples Binning Plot', align_hz = 'left', num = True)
        init_split = self.split
        self.split = rectsplit(pymupdf.Rect(0,0,*self.pagesize), nrows = 2, ncols = 1, margin = self.margin)

        num = 1
        if cores > 1:
            with futures.ProcessPoolExecutor(max_workers = cores) as executor:
                todo = {}
                for c,s in cuts.items():
                    bin = bins.get(c)
                    future = executor.submit(plot_cut, cut = s, flag = flag, bin = bin, time = time, figsize = figsize, 
                            show_name = show_name, show_label = show_label, precision = precision, iter_display_limit = iter_display_limit, 
                            rotation = rotation, fontsize = self.txtsize, retnbuff = True)
                    todo[future] = c
                for f in tqdm(todo, total = len(todo)):
                    buff = f.result()
                    temp_doc = pymupdf.open('pdf', stream = buff.getvalue())
                    c = todo[f]
                    bin = bins.get(c)
                    label = [to_str(i, precision, iter_display_limit) for i in bin['split']]
                    label = ', '.join([str(i) + ':' + s for i,s in enumerate(label)])
                    drop_reason = frame._drop.get(c)
                    if drop_reason:
                        drop_reason = {k: round(v,4) if isinstance(v, float) else v for k,v in drop_reason.items()}
                    
                    self.newline(fontsize = fontsize)
                    self.text(f'({num}) {c}', fontname = self.titlefont, fontsize = self.txtsize)
                    self.newline(fontsize = fontsize)
                    self.text('<Bins> ', fontname = self.titlefont, fontsize = self.txtsize)
                    self.text(label, fontname = self.txtfont, fontsize = self.txtsize)
                    if drop_reason:
                        self.newline(fontsize = fontsize)
                        self.text('<Drop Reason> ', fontname = self.titlefont, fontsize = self.txtsize)
                        self.text(str(drop_reason), fontname = self.txtfont, fontsize = self.txtsize)
                    self.newline(fontsize = fontsize)
                    self.figure(temp_doc, split = self.split)
                    temp_doc.close()
                    num += 1
        else:
            for c,s in tqdm(cuts.items(), total= cuts.shape[1]):
                bin = bins.get(c)
                buff = plot_cut(cut = s, flag = flag, bin = bin, time = time, figsize = figsize, show_name = show_name, 
                        show_label = show_label, precision = precision, iter_display_limit = iter_display_limit, rotation = rotation, 
                        fontsize = self.txtsize, retnbuff= True)
                temp_doc = pymupdf.open('pdf', stream = buff.getvalue())
                label = [to_str(i, precision, iter_display_limit) for i in bin['split']]
                label = ', '.join([str(i) + ':' + s for i,s in enumerate(label)])
                
                self.newline(fontsize = fontsize)
                self.text(f'({num}) {c}', fontname = self.titlefont, fontsize = self.txtsize)
                self.newline(fontsize = fontsize)
                self.text('<Bins> ', fontname = self.titlefont, fontsize = self.txtsize)
                self.text(label, fontname = self.txtfont, fontsize = self.txtsize)
                self.newline(fontsize = fontsize)
                self.figure(temp_doc, split = self.split)
                temp_doc.close()
                num += 1
        
        self.split = init_split

    def code(self, miss_fill: int = 0) -> None:
        '''Generate a chapter containing the deployment code.

        Args:
            miss_fill: Determines the WOE value of the missing value.
                <0: Use the minimum WOE among all bins.
                =0: Use 0 as the WOE.
                >0: Use the maximum WOE among all bins.
        '''
        frame = self.frame
        binpy = ["import math, numbers\n", "# Selected Features"]
        woepy = binpy.copy()
        select_fts = frame.select
        binsql = ["-- Selected Features", f"{'select *' if select_fts != [] else ''}"]
        woesql = binsql.copy()
        
        for i in select_fts:
            binpy.append(f'## {i}')
            binpy.extend(frame.code_bin2num(lang = 'py', feature = i))
            woepy.append(f'## {i}')
            woepy.extend(frame.code_bin2woe(lang = 'py', feature = i, miss_fill = miss_fill))
            
            binsql.append(f'    ---- {i}')
            temp_code = frame.code_bin2num(lang = 'sql', feature = i)
            binsql.extend([f'    {i}' for i in temp_code])
            woesql.append(f'    ---- {i}')
            temp_code = frame.code_bin2woe(lang = 'sql', feature = i, miss_fill = miss_fill)
            woesql.extend([f'    {i}' for i in temp_code])
        
        drop_fts = [i for i in frame._drop]
        temp_code = '\n# Dropped Features'
        binpy.append(temp_code)
        woepy.append(temp_code)
        temp_code = [
            "from Table_Features\n;\n" if select_fts != [] else "\n",
            "-- Dropped Features",
            f"{'select *' if drop_fts != [] else ''}"
        ]
        binsql.extend(temp_code)
        woesql.extend(temp_code)
        
        for i in frame._drop:
            binpy.append(f'## {i}')
            binpy.extend(frame.code_bin2num(lang = 'py', feature = i))
            woepy.append(f'## {i}')
            woepy.extend(frame.code_bin2woe(lang = 'py', feature = i, miss_fill = miss_fill))
            
            binsql.append(f'    ---- {i}')
            temp_code = frame.code_bin2num(lang = 'sql', feature = i)
            binsql.extend([f'    {i}' for i in temp_code])
            woesql.append(f'    ---- {i}')
            temp_code = frame.code_bin2woe(lang = 'sql', feature = i, miss_fill = miss_fill)
            woesql.extend([f'    {i}' for i in temp_code])
        temp_code = "from Table_Features\n;" if drop_fts != [] else ""
        binsql.append(temp_code)
        woesql.append(temp_code)

        self.new_page()
        fontsize = self.heading(1, 'Deployment Code', align_hz = 'left', num = True)
        self.newline(fontsize = fontsize, spacing = 0.8)
        fontsize -= self.titledelta
        
        text = "Python_Code_for_Bin_WOE"
        self.text(text, fontname = self.titlefont, fontsize = fontsize)
        self.add_file_annot('\n'.join(woepy), text + '.txt', icon = 'Paperclip')
        self.newline(fontsize = fontsize, spacing = 0.8)
        
        text = "SQL_Code_for_Bin_WOE"
        self.text(text, fontname = self.titlefont, fontsize = fontsize)
        self.add_file_annot('\n'.join(woesql), text + '.txt', icon = 'Paperclip')
        self.newline(fontsize = fontsize, spacing = 0.8)

        self.newline(fontsize = fontsize, spacing = 0.8)
        text = "Python_Code_for_Bin_Num"
        self.text(text, fontname = self.titlefont, fontsize = fontsize)
        self.add_file_annot('\n'.join(binpy), text + '.txt', icon = 'Paperclip')
        self.newline(fontsize = fontsize, spacing = 0.8)

        text = "SQL_Code_for_Bin_Num"
        self.text(text, fontname = self.titlefont, fontsize = fontsize)
        self.add_file_annot('\n'.join(binsql), text + '.txt', icon = 'Paperclip')
        self.newline(fontsize = fontsize, spacing = 0.8)
        
    def log(self):
        logstr = self.frame.loginfo.getvalue()[:-1] # The last char is '\n'.
        self.new_page()
        fontsize = self.heading(1, 'Development Log', align_hz = 'left', num = True)
        self.newline(fontsize = fontsize)
        self.text(logstr, fontname = self.txtfont, fontsize = self.txtsize - 2, indent_2 = 4)

class LogitReport(ModReport):
    def __init__(self, frame, title = 'Logit Regression Model', developer = 'developer', **kwargs) -> None:
        '''Initialize a PyMuPDF Document object for a logit regression model Frame object.

        Args:
            frame: A logit regression model Frame object.
            title: Model title.
            developer: Developer name.
            kwargs:
                pagesize: A tuple containing the (width, height) of the paper.
                margin: The width of the margin to preserve around the edges.
                titlefont: The font for document titles.
                titlesize: The font size for the document title.
                titledelta: The variation in font size between different heading levels.
                txtfont: The font for text.
                txtsize: The font size of text.
                font_aspect_ratio: Specifies the aspect ratio (height to width) of the font.
        '''
        super().__init__(frame = frame, title = title, developer = developer, **kwargs)
    
    def correlation(self) -> None:
        '''Generate a chapter containing the WOE correlation heatmap of the final selected features.
        '''
        frame = self.frame
        samp_label = frame.train_label
        samp = getattr(frame, 'x_' + samp_label)[frame.select]
        woe = frame.transform(samp = samp, woe = True, warn = False)
        corr = woe.corr()
        fig = plot_corr(corr, ticklabels = False)

        self.new_page()
        heading = f"WOE Correlation of {samp_label.capitalize()}"
        fontsize = self.heading(1, heading, align_hz = 'left', num = True)
        self.add_file_annot(corr, heading + ".xlsx", icon = 'Paperclip')

        self.newline(fontsize = fontsize, spacing= 0.8)
        self.figure(fig, next_rect = False)
        plt.close(fig)
        
        for i,n in enumerate(corr.columns):
            self.newline(fontsize = self.txtsize)
            self.text(str(i) + ": " + n, fontname = self.txtfont, fontsize = self.txtsize)
    
    def scorecard(self) -> None:
        '''Generate a chapter containing the scorecard.
        '''
        config = self.frame._config.get('scorecard')
        card = self.frame._scorecard
        
        self.new_page()
        heading = 'Score Card'
        fontsize = self.heading(1, heading, align_hz = 'left', num = True)
        self.add_file_annot(card, heading + ".xlsx", icon = 'Paperclip')
        
        self.newline(fontsize = fontsize, spacing = 0.8)
        fontsize -= self.titledelta
        self.text('Card Params:', fontname = self.titlefont, fontsize = fontsize, indent_1 = 2)
        # self.text(str(config), fontname = self.txtfont, fontsize = fontsize)
        config = dict2list(config, n_col = 2)
        self.table(pd.DataFrame(config), fontsize = fontsize, index = False, head = False, txtalign_hz = 'right', nan = 'None')

        self.newline(fontsize = fontsize)
        self.table(card, nan = 'nan')

    def analysis(self, samp: str, fig_bins: int = 50, tab_bins: int = 20, time_bins: int = 10, reverse: bool = False) -> None:
        '''Generate a chapter containing the model analysis and evaluation for the specified samples.

        Args:
            samp: Sample label.
            fig_bins: Number of bins for plotting the score distribution histogram.
            tab_bins: Number of bins for creating the score ranking table.
            time_bins: Number of bins for the score ranking table within each time partition.
            reverse: Whether to sort the predicted probabilitie or score bins in reverse order.
        '''
        frame = self.frame
        Flag = frame._flag.capitalize()
        x, y_true = frame.get_xy(label = samp)
        y_score = frame._mod.predict(x)
        if hasattr(frame, '_scorecard'):
            y_score = frame.prob2score(y_score)
        time = getattr(frame, 'time_' + samp) if frame._time else None
        super().analysis(y_true, y_score, Flag, label = samp, time = time, fig_bins = fig_bins, tab_bins = tab_bins, time_bins = time_bins, reverse = reverse)

    def modres(self) -> None:
        '''Generate a chapter containing the model results.
        '''
        # Logit Regression Results
        frame = self.frame
        summary = frame._mod.summary()
        restab0 = summary.tables[0]
        restab1 = summary.tables[1]
        restab0df = pd.DataFrame(restab0.data)
        restab1df = pd.DataFrame(restab1.data[1:], columns = restab1.data[0]).set_index('')
        restab = restab0df.copy()
        restab[''] = None
        restab = pd.concat([restab, pd.DataFrame(restab1.data)], axis = 1)
        
        # MOD EVALUATION
        all_eva = {}
        for s in frame._samp_labels:
            x, y = frame.get_xy(label = s)
            prob = frame._mod.predict(x)
            all_eva[s] = (y, prob)
        fig = plot_eva(all_eva)

        # pdf
        self.new_page()
        fontsize = self.heading(1, 'Model Results', align_hz = 'left', num = True)
        self.newline(fontsize = fontsize)
        
        heading = restab0.title
        fontsize = self.heading(2, heading, align_hz = 'left', num = True)
        self.add_file_annot(restab, heading + ".xlsx", to_excel_kwargs = {'index': False, 'header': False}, icon = 'Paperclip')

        self.newline(fontsize = fontsize)
        self.table(restab0df, head = False, index = False, style= 1)
        self.newline(fontsize = fontsize)
        self.table(restab1df)

        self.new_page()
        fontsize = self.heading(2, 'Model Evaluation', align_hz = 'left', num = True)

        self.newline(fontsize = fontsize)
        self.figure(fig)
        plt.close(fig)
    
    def code(self, miss_fill: int = 0) -> None:
        '''Generate a chapter containing the deployment code.

        Args:
            miss_fill: Determines the risk level of the missing value.
                <0: Use the minimum WOE or score among all bins.
                =0: Use 0 as the WOE or the share score of bins.
                >0: Use the maximum WOE or score among all bins.
        '''
        super().code(miss_fill = miss_fill)
        frame = self.frame
        fontsize = self.titlesize - 2 * self.titledelta

        modscorepy = frame.py_score()
        modscoresql = frame.sql_score()
        
        if hasattr(frame, '_scorecard'):
            paranames = frame._mod.params.index.to_list()
            const = frame._config['x_data']['const']
            modfts = paranames[1:] if const else paranames
            scorepy = ["import math, numbers", "# Model Features"]
            scoresql = [f"-- Model Features", f"{'select *' if modfts != [] else ''}"]
            
            for i in modfts:
                scorepy.append(f"## {i}")
                scorepy.extend(frame.code_bin2score(lang = 'py', feature = i, miss_fill = miss_fill))
                scoresql.append(f'    ---- {i}')
                temp_code = frame.code_bin2score(lang = 'sql', feature = i, miss_fill = miss_fill)
                scoresql.extend([f'    {i}' for i in temp_code])
            scoresql.append(f"{'from Table_Features;' if modfts != [] else ''}")
            
            self.newline(fontsize = fontsize, spacing = 0.8)
            text = "Python_Code_for_Bin_Score"
            self.text(text, fontname = self.titlefont, fontsize = fontsize)
            self.add_file_annot('\n'.join(scorepy), text + '.txt', icon = 'Paperclip')
            self.newline(fontsize = fontsize, spacing = 0.8)

            text = "SQL_Code_for_Bin_Score"
            self.text(text, fontname = self.titlefont, fontsize = fontsize)
            self.add_file_annot('\n'.join(scoresql), text + '.txt', icon = 'Paperclip')
            self.newline(fontsize = fontsize, spacing = 0.8)

        self.newline(fontsize = fontsize, spacing = 0.8)
        text = "Python_Code_for_Logit_Model"
        self.text(text, fontname = self.titlefont, fontsize = fontsize)
        self.add_file_annot('\n'.join(modscorepy), text + '.txt', icon = 'Paperclip')
        self.newline(fontsize = fontsize, spacing = 0.8)

        text = "SQL_Code_for_Logit_Model"
        self.text(text, fontname = self.titlefont, fontsize = fontsize)
        self.add_file_annot('\n'.join(modscoresql), text + '.txt', icon = 'Paperclip')
        self.newline(fontsize = fontsize, spacing = 0.8)


class LGBMCReport(ModReport):
    def __init__(self, frame, title = 'LGBMClassifier Model', developer = 'developer', **kwargs):
        '''Initialize a PyMuPDF Document object for a LGBMClassifier model Frame object.

        Args:
            frame: A LGBMClassifier model Frame object.
            title: Model title.
            developer: Developer name.
            kwargs:
                pagesize: A tuple containing the (width, height) of the paper.
                margin: The width of the margin to preserve around the edges.
                titlefont: The font for document titles.
                titlesize: The font size for the document title.
                titledelta: The variation in font size between different heading levels.
                txtfont: The font for text.
                txtsize: The font size of text.
                font_aspect_ratio: Specifies the aspect ratio (height to width) of the font.
        '''
        super().__init__(frame = frame, title = title, developer = developer, **kwargs)

    def modres(self, features_info: pd.DataFrame | None = None, name_key = None) -> None:
        '''Generate a chapter containing the model results.

        Args:
            features_info: Additional descriptive information about the features.
            name_key: Key specifying the feature name in `features_info`, otherwise use the row index for concatenation.
        '''
        frame = self.frame
        mod_params = dict2list(frame._mod.get_params(), 2)
        mod_params = pd.DataFrame(mod_params)
        importance = frame.importance(features_info = features_info, name_key = name_key)
        # MOD EVALUATION
        all_eva = {}
        for s in frame._samp_labels:
            x, y = frame.get_xy(label = s, mod = True)
            prob = frame._mod.predict_proba(x)[:,1]
            all_eva[s] = (y, prob)
        fig = plot_eva(all_eva)
        
        # pdf
        self.new_page()
        fontsize = self.heading(1, 'Model Results', align_hz = 'left', num = True)
        self.newline(fontsize = fontsize)
        
        heading = 'Model Parameters'
        fontsize = self.heading(2, heading, align_hz = 'left', num = True)
        self.newline(fontsize = fontsize)
        self.table(mod_params, fontsize = fontsize, index = False, head = False, txtalign_hz = 'right', nan = 'None')

        fontsize = self.heading(2, 'Model Evaluation', align_hz = 'left', num = True)
        self.newline(fontsize = fontsize)
        self.figure(fig)
        plt.close(fig)

        self.new_page()
        fontsize = self.heading(2, 'Feature Importance', align_hz = 'left', num = True)
        self.newline(fontsize = fontsize)
        self.table(importance, databar = 'importance')
    
    def analysis(self, samp: str, fig_bins: int = 50, tab_bins: int = 20, time_bins: int = 10, reverse: bool = False) -> None:
        '''Generate a chapter containing the model analysis and evaluation for the specified samples.

        Args:
            samp: Sample label.
            fig_bins: Number of bins for plotting the score distribution histogram.
            tab_bins: Number of bins for creating the score ranking table.
            time_bins: Number of bins for the score ranking table within each time partition.
            reverse: Whether to sort the predicted probabilitie or score bins in reverse order.
        '''
        frame = self.frame
        Flag = frame._flag.capitalize()
        x, y_true = frame.get_xy(label = samp, mod = True)
        y_score = frame._mod.predict_proba(x)[:, 1]
        y_score = pd.Series(y_score, index = x.index)
        if 'score' in frame._config:
            y_score = frame.prob2score(y_score)
        time = getattr(frame, 'time_' + samp) if frame._time else None
        super().analysis(y_true, y_score, Flag, label = samp, time = time, fig_bins = fig_bins, tab_bins = tab_bins, time_bins = time_bins, reverse = reverse)

    def code(self, miss_fill = 0):
        '''Generate a chapter containing the deployment code.

        Args:
            miss_fill: Determines the risk level of the missing value.
                <0: Use the minimum WOE or score among all bins.
                =0: Use 0 as the WOE or the share score of bins.
                >0: Use the maximum WOE or score among all bins.
        '''
        super().code(miss_fill = miss_fill)
        frame = self.frame
        fontsize = self.titlesize - 2 * self.titledelta

        modscorepy = frame.py_score()
        modscoresql = frame.sql_score()

        self.newline(fontsize = fontsize, spacing = 0.8)
        text = "Python_Code_for_LGBMClassifier"
        self.text(text, fontname = self.titlefont, fontsize = fontsize)
        self.add_file_annot('\n'.join(modscorepy), text + '.txt', icon = 'Paperclip')
        self.newline(fontsize = fontsize, spacing = 0.8)

        text = "SQL_Code_for_LGBMClassifier"
        self.text(text, fontname = self.titlefont, fontsize = fontsize)
        self.add_file_annot('\n'.join(modscoresql), text + '.txt', icon = 'Paperclip')
        self.newline(fontsize = fontsize, spacing = 0.8)