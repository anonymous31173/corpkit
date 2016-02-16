from __future__ import print_function
import corpkit

class Interrogation(object):
    """
    Stores results of a corpus interrogation, before or after editing.
    """

    def __init__(self, results = None, totals = None, query = None, concordance = None):
        """initialise the class"""
        self.results = results
        """pandas `DataFrame` containing counts for each subcorpus"""
        self.totals = totals
        """pandas `Series` containing summed results"""
        self.query = query
        """`dict` containing values that generated the result"""
        self.concordance = concordance
        """pandas `DataFrame` containing concordance lines, if concordance lines were requested."""

    def __str__(self):
        if self.query.get('corpus'):
            prst = self.query['corpus'].name
        else:
            try:
                prst = self.query['interrogation'].query['corpus'].name
            except:
                prst = 'edited'
        st = 'Corpus interrogation: %s\n\n' % (prst)
        return st

    def __repr__(self):
        if 'results' in self.__dict__:
            return "<corpkit.interrogation.Interrogation instance: %d subcorpora, %d entries>" % self.results.shape
        else:
            return "<corpkit.interrogation.Interrogation instance: %d total>" % self.totals.sum()

    def edit(self, *args, **kwargs):
        """Edit results of interrogations, do keywording, sort, etc.

           >>> # rel. frequencies for words without initial capital
           >>> rel = data.edit('%', 'self', skip_entries = r'^[A-Z]')

        ``just/skip_entries`` and ``just/skip_subcorpora`` can take a few different kinds of input:

        * str: treated as regular expression to match
        * list: 

          * of integers: indices to match
          * of strings: entries/subcorpora to match

        ``merge_entries`` and ``merge_subcorpora``, however, are best entered as dicts:

        ``{newname: criteria, newname2: criteria2}```

        where criteria is a string, list, etc.

        :param operation: Kind of maths to do on inputted lists:

           ``'+'``, ``'-'``, ``'/'``, ``'*'``, ``'%'``: self explanatory

           ``'k'``: log likelihood (keywords)

           ``'a'``: get distance metric

           ``'d'``: get percent difference (alternative approach to keywording)

        :type operation: str
        
        :param denominator: List of results or totals.

           If list of results, for each entry in dataframe 1, locate
           entry with same name in dataframe 2, and do maths there
           if 'self', do all merging/keeping operations, then use
           edited dataframe1 as denominator

        :type denominator: pandas.Series/pandas.DataFrame/dict/`self`

        :param sort_by: Calculate slope, stderr, r, p values, then sort by.

           ``'increase'``: highest to lowest slope value
           ``'decrease'``: lowest to highest slope value
           ``'turbulent'``: most change in y axis values
           ``'static'``: least change in y axis values
           ``'total/most'``: largest number first
           ``'infreq/least'``: smallest number first
           ``'name'``: alphabetically

        :type sort_by: str

        :param keep_stats: Keep/drop stats values from dataframe after sorting
        :type keep_stats: bool
        
        :param keep_top: After sorting, remove all but the top *keep_top* results
        :type keep_top: int
        
        :param just_totals: Sum each column and work with sums
        :type just_totals: bool
        
        :param threshold: When using results list as dataframe 2, drop values occurring fewer than n times. If not keywording, you can use:
                                
           ``'high'``: ``denominator total / 2500``
           
           ``'medium'``: ``denominator total / 5000``
           
           ``'low'``: ``denominator total / 10000``
                            
           If keywording, there are smaller default thresholds

        :type threshold: int/bool
        :param just_entries: Keep matching entries
        :type just_entries: see above
        :param skip_entries: Skip matching entries
        :type skip_entries: see above
        :param merge_entries: Merge matching entries
        :type merge_entries: see above
        :param newname: New name for merged entries
        :type newname: str/``'combine'``
        :param just_subcorpora: Keep matching subcorpora
        :type just_subcorpora: see above
        :param skip_subcorpora: Skip matching subcorpora
        :type skip_subcorpora: see above
        :param span_subcorpora: If subcorpora are numerically named, span all from *int* to *int2*, inclusive
        :type span_subcorpora: tuple -- ``(int, int2)``
        :param merge_subcorpora: Merge matching subcorpora
        :type merge_subcorpora: see above
        :param new_subcorpus_name: Name for merged subcorpora
        :type new_subcorpus_name: str/``'combine'``

        :param replace_names: Edit result names and then merge duplicate names.
        :type replace_names: dict -- ``{criteria: replacement_text}``; str -- a regex to delete from names
        :param projection:         a  to multiply results in subcorpus by n
        :type projection: tuple -- ``(subcorpus_name, n)``
        :param remove_above_p: Delete any result over ``p``
        :type remove_above_p: bool
        :param p:                  set the p value
        :type p: float
        
        :param revert_year: When doing linear regression on years, turn annual subcorpora into 1, 2 ...
        :type revert_year: bool
        
        :param print_info: Print stuff to console showing what's being edited
        :type print_info: bool
        
        :param spelling: Convert/normalise spelling:
        :type spelling: str -- ``'US'``/``'UK'``
        
        :param selfdrop: When keywording, try to remove target corpus from reference corpus
        :type selfdrop: bool
        
        :param calc_all: When keywording, calculate words that appear in either corpus
        :type calc_all: bool

        :returns: :class:`corpkit.interrogation.Interrogation`
        """
        from editor import editor
        return editor(self, *args, **kwargs)

    def visualise(self,
            title = '',
            x_label = None,
            y_label = None,
            style = 'ggplot',
            figsize = (8, 4),
            save = False,
            legend_pos = 'best',
            reverse_legend = 'guess',
            num_to_plot = 7,
            tex = 'try',
            colours = 'Accent',
            cumulative = False,
            pie_legend = True,
            partial_pie = False,
            show_totals = False,
            transparent = False,
            output_format = 'png',
            interactive = False,
            black_and_white = False,
            show_p_val = False,
            indices = False,
            transpose = False,
            **kwargs):
        """Visualise corpus interrogations.

           >>> data.visualise('An example plot', kind = 'bar', save = True)

        :param title: A title for the plot
        :type title: str
        :param x_label: A label for the x axis
        :type x_label: str
        :param y_label: A label for the y axis
        :type y_label: str
        :param kind: The kind of chart to make
        :type kind: str ('line'/'bar'/'barh'/'pie'/'area')
        :param style: Visual theme of plot
        :type style: str ('ggplot'/'bmh'/'fivethirtyeight'/'seaborn-talk'/etc)
        :param figsize: Size of plot
        :type figsize: tuple (int, int)
        :param save: If bool, save with *title* as name; if str, use str as name
        :type save: bool/str
        :param legend_pos: Where to place legend
        :type legend_pos: str ('upper right'/'outside right'/etc)
        :param reverse_legend: Reverse the order of the legend
        :type reverse_legend: bool
        :param num_to_plot: How many columns to plot
        :type num_to_plot: int/'all'
        :param tex: Use TeX to draw plot text
        :type tex: bool
        :param colours: Colourmap for lines/bars/slices
        :type colours: str
        :param cumulative: Plot values cumulatively
        :type cumulative: bool
        :param pie_legend: Show a legend for pie chart
        :type pie_legend: bool
        :param partial_pie: Allow plotting of pie slices only
        :type partial_pie: bool
        :param show_totals: Print sums in plot where possible
        :type show_totals: str -- 'legend'/'plot'/'both'
        :param transparent: Transparent .png background
        :type transparent: bool
        :param output_format: File format for saved image
        :type output_format: str -- 'png'/'pdf'
        :param black_and_white: Create black and white line styles
        :type black_and_white: bool
        :param show_p_val: Attempt to print p values in legend if contained in df
        :type show_p_val: bool
        :param indices: To use when plotting "distance from root"
        :type indices: bool
        :param stacked: When making bar chart, stack bars on top of one another
        :type stacked: str
        :param filled: For area and bar charts, make every column sum to 100
        :type filled: str
        :param legend: Show a legend
        :type legend: bool
        :param rot: Rotate x axis ticks by *rot* degrees
        :type rot: int
        :param subplots: Plot each column separately
        :type subplots: bool
        :param layout: Grid shape to use when *subplots* is True
        :type layout: tuple -- (int, int)
        :param interactive: Experimental interactive options
        :type interactive: list -- [1, 2, 3]
        :returns: matplotlib figure
        """
        locs = locals()
        locs.pop('self', None)
        if kwargs:
            for k, v in kwargs.items():
                locs[k] = v
        locs.pop('kwargs', None)

        from plotter import plotter
        branch = kwargs.pop('branch', 'results')
        if branch.lower().startswith('r'):
            plotter(self.results, **locs)
        elif branch.lower().startswith('t'):
            plotter(self.totals, **locs)   

    def save(self, savename, savedir = 'saved_interrogations', **kwargs):
        """
        Save an interrogation as pickle to ``savedir``.

           >>> o = corpus.interrogate('w', 'any')
           >>> o.save('savename')

        will create ``saved_interrogations/savename.p``
        
        :param savename: A name for the saved file
        :type savename: str
        
        :param savedir: Relative path to directory in which to save file
        :type savedir: str
        
        :param print_info: Show/hide stdout
        :type print_info: bool
        
        :returns: None
        """
        from other import save
        save(self, savename, savedir = savedir, **kwargs)

    def quickview(self, n = 25):
        """view top n results as painlessly as possible.

           >>> data.quickview(n = 5)

        :param n: Show top *n* results
        :type n: int
        :returns: None
        """
        from other import quickview
        quickview(self, n = n)

    def multiindex(self, indexnames = False):
        """Create a `pd.MultiIndex` object from slash-separated results.

           >>> mi = data.multiindex()

        :param indexnames: provide custom names for the new index
        :type indexnames: list of strings

        :returns: :class:`corpkit.interrogation.Interrogation`, with ``pd.MultiIndex`` as :py:attr:`~corpkit.interrogation.Interrogation.results` attribute
        """

        from other import make_multi
        return make_multi(self, indexnames = indexnames)

import pandas as pd
class Results(pd.core.frame.DataFrame):
    """
    A class for interrogation results, with methods for editing, visualising,
    saving and quickviewing
    """

    def __init__(self, data):
        pd.core.frame.DataFrame.__init__(self, data)

    #def __repr__(self):
        #return "<corpkit.interrogation.Results instance: %d unique results>" % len(self.columns)

    def edit(self, *args, **kwargs):
        """calls corpkit.editor.editor()"""
        from editor import editor
        return editor(self, *args, **kwargs)

    def visualise(self, title, *args, **kwargs):
        """calls corpkit.plotter.plotter()"""
        from plotter import plotter
        plotter(title, self, *args, **kwargs)

    def save(self, savename, *args, **kwargs):
        """Save data to pickle file"""
        from other import save
        save(self, savename, *args, **kwargs)

    def quickview(self, n = 25):
        """Print top results from an interrogation or edit"""
        from other import quickview
        quickview(self, n = n)
    
class Totals(pd.core.series.Series):
    """
    A class for interrogation totals, with methods for editing, plotting,
    saving and quickviewing
    """
    def __init__(self, data):
        pd.core.series.Series.__init__(self, data)

    #def __repr__(self):
        #return "<corpkit.interrogation.Totals instance: %d unique results>" % self.sum()

    def edit(self, *args, **kwargs):
        """calls corpkit.editor.editor()"""
        from editor import editor
        return editor(self, *args, **kwargs)

    def visualise(self, title, *args, **kwargs):
        """calls corpkit.plotter.plotter()"""
        from plotter import plotter
        plotter(title, self, *args, **kwargs)

    def save(self, savename, *args, **kwargs):
        """Save data to pickle file"""
        from other import save
        save(self, savename, *args, **kwargs)

    def quickview(self, n = 25):
        """Print top results from an interrogation or edit"""
        from other import quickview
        quickview(self, n = n)
    
class Concordance(pd.core.frame.DataFrame):
    """
    A class for concordance lines, with methods for saving,
    formatting and editing.
    """
    
    def __init__(self, data):

        pd.core.frame.DataFrame.__init__(self, data)
        self.results = data

    def format(self, kind = 'string', n = 100, window = 35, columns = 'all', **kwargs):
        """
        Print conc lines nicely, to string, LaTeX or CSV

           >>> lines.format(window = 25, n = 10, columns = ['l', 'm', 'r'])

        :param kind: output format
        :type kind: str (``'string'``/``'latex'``/``'csv'``)
        :param n: Print first ``n`` lines only
        :type n: int/'all'
        :param window: how many characters to show to left and right
        :type window: int
        :param columns: which columns to show
        :type columns: list
        :returns: None
        """
        from other import concprinter
        return concprinter(self, kind = kind, n = n, window = window, columns = columns, **kwargs)

    def __repr__(self):
        return self.format(return_it = True)

    def calculate(self):
        """Make new Interrogation object from (modified) concordance lines"""
        from process import interrogation_from_conclines
        newdata = interrogation_from_conclines(self)
        return newdata

    def shuffle(self, inplace = False):
        """Shuffle concordance lines

        :param inplace: Modify current object, or create a new one
        :type inplace: bool
        """
        import random
        index = list(self.index)
        random.shuffle(index)
        shuffled = self.ix[index]
        shuffled.reset_index()
        if inplace:
            self = shuffled
        else:
            return shuffled

    def edit(self, *args, **kwargs):
        """Delete or keep rows by subcorpus or by middle column text.

        >>> skipped = conc.edit(skip_entries = r'to_?match')"""

        from editor import editor
        return editor(self, *args, **kwargs)

from collections import OrderedDict
class Interrodict(OrderedDict):
    """
    A class for interrogations that do not fit in a single-indexed DataFrame.

    Methods for saving, editing, and generating multiindex DataFrame equivalent.
    """
    
    def __init__(self, data):
        from process import makesafe
        if type(data) == list:
            from collections import OrderedDict
            data = OrderedDict(data)
        # attribute access
        for index, (k, v) in enumerate(data.items()):
            setattr(self, makesafe(k), v)
        super(Interrodict, self).__init__(data)

    def __getitem__(self, key):
        """allow slicing, indexing"""
        from collections import OrderedDict
        from process import makesafe
        # allow slicing
        if isinstance( key, slice ) :
            n = OrderedDict()
            for ii in range(*key.indices(len(self))):
                n[self.keys()[ii]] = self[ii]
            return Interrodict(n) 

            return Interrodict([self[ii] for ii in range(*key.indices(len(self)))])
        # allow integer index
        elif type(key) == int:
            return next(v for i, (k, v) in enumerate(self.items()) if i == key)
            #return self.subcorpora.__getitem__(makesafe(self.subcorpora[key]))
        # dict key access
        else:
            try:
                return OrderedDict.__getitem__(self, key)
            except:
                from process import is_number
                if is_number(key):
                    return self.__getattribute__('c' + key)
        


    def __repr__(self):
        return "<corpkit.interrogation.Interrodict instance: %d items>" % (len(self.keys()))

    def __str__(self):
        return "<corpkit.interrogation.Interrodict instance: %d items>" % (len(self.keys()))

    #def __str__(self):
    #    return "<corpkit.interrogation.Interrodict instance: %d items>" % (len(self.keys()))

    def edit(self, *args, **kwargs):
        """Edit each value with :func:`~corpkit.interrogation.Interrogation.edit`.

        See :func:`~corpkit.interrogation.Interrogation.edit` for possible arguments.

        :returns: :class:`corpkit.interrogation.Interrodict`
        """

        from editor import editor
        return editor(self, *args, **kwargs)

    def multiindex(self, indexnames = False):
        """Create a ``pd.MultiIndex`` version of results.

        :param indexnames: provide custom names for the new index
        :type indexnames: list of strings

        :returns: A :class:`corpkit.interrogation.Interrogation`
        """
        from other import make_multi
        return make_multi(self, indexnames = indexnames)


    def save(self, savename, savedir = 'saved_interrogations', **kwargs):
        """
        Save an interrogation as pickle to ``savedir``.

           >>> o = corpus.interrogate('w', 'any')
           >>> o.save('savename')

        will create ``saved_interrogations/savename.p``
        
        :param savename: A name for the saved file
        :type savename: str
        
        :param savedir: Relative path to directory in which to save file
        :type savedir: str
        
        :param print_info: Show/hide stdout
        :type print_info: bool
        
        :returns: None
        """
        from other import save
        save(self, savename, savedir = savedir, **kwargs)

    def collapse(self, axis = 'y'):
        """
        Collapse Interrodict on an axis or along interrogation name.

        :param axis: collapse along x, y or name axis
        :type axis: str ('x'/'y'/'n')
        :returns: `corpkit.interrogation.Interrogation`
        """
        import pandas as pd
        if axis.lower()[0] not in ['x', 'y']:
            order = list(self.values()[0].results.columns)
            df = self.values()[0].results
            for i in self.values()[1:]:
                df = df.add(i.results, fill_value = 0)
        else:
            out = []
            for corpus_name, interro in self.items():
                if axis.lower().startswith('y'):
                    ax = 0
                elif axis.lower().startswith('x'):
                    ax = 1
                data = interro.results.sum(axis = ax)
                data.name = corpus_name
                out.append(data)
            # concatenate and transpose
            df = pd.concat(out, axis = 1).T
            # turn NaN to 0, sort
            df = df.fillna(0)
        
        #make interrogation object from df
        if not axis.lower().startswith('x'):
            df = df.edit(sort_by = 'total', print_info = False)
        else:
            df = df.edit(print_info = False)
        # make sure everything is int, not float
        for col in list(df.results.columns):
            df.results[col] = df.results[col].astype(int)
        return df

