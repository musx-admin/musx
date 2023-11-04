"""
An object-orientated implemention of Python iterators that yield patterns in data,
from simple looping and randomness to more complex processes such as markov
chains, cellular automata and chaos.  Many of these patterns allow subpatterns and
expressions to be embedded inside parent patterns and processed seamlessly by the 
Pattern's `next()` method.  For more information see the patterns.ipynb tutorial 
and the demos folder for many examples of using musx patterns to generate music.
"""

from collections.abc import Iterator
import random
from math import ceil, floor

class Pattern(Iterator):
    '''The base class for all patterns provides a specialized `next()` function.'''
    def __init__(self, items, mini, period=None):
        if not isinstance(items, list) or len(items) < mini:
            raise TypeError(f"{self.__class__.__name__} input {items} is not a list of {mini} or more elements.")
        self.items = items
        if period == None:
            period = len(items)
        self.period = period
        #print("***period is:", period)
        # length of items list
        self.ilen = len(self.items)
        # current index into items list
        self.i = 0 
        # length of current period
        self.plen = self._read(self.period) if isinstance(self.period, Iterator) else self.period
        #print("***plen is:", self.plen)
        # period counter
        self.p = 0
        # 'EOP' if the pattern just returned the last value of the current period
        #self.eop = None

    def __iter__(self):
        return self

    def _pname(self):
        return self.__class__.__name__
    
    @staticmethod
    def _read(pat, tup=False):
        """
        Internal function that checks if the next item is a pattern, expression,
        or basic data. Do not call this method directly, use Pattern's next() 
        function to return the next element(s) in a pattern.
        """
        #print(f"read input: ({pat},tup={tup})")
        if isinstance(pat, Pattern):
            x = next(pat)
            return x if tup else x[0]
        else:
            # if pat is a zero-arg lambda or function, call it to produce the return value
            if callable(pat):
                pat = pat()
            return [pat, "EOP"] if tup else pat

    def next(self, more=False):
        """
        A pattern savvy version of Python's builtin `next()` function. Use this
        method in place of Python's next() to access pattern elements in
        flexible ways.
        
        Parameters
        ----------
        more : False | True | int 
            If more is False (the default) then Pattern's next() function
            will return the next item in the pattern. If more is True then
            the (remaining) items in the current period are returned as a list. 
            Otherwises, if more is an integer greater than 0 then that many
            items will be returned as a list.

        Returns
        -------
        One or more items in the pattern.

        Examples
        --------
        ```python
        >>> c = Cycle([1, 2, 3, 4])
        >>> c.next()
        1
        >>> c.next(True)
        [2, 3, 4] 
        >>> c.next(6)
        [1, 2, 3, 4, 1, 2]
        ```

        It is possible to use Python's builtin `next()` function to read a pattern, in this
        case you will receive a two element list holding the item from the pattern and an
        'end of period' marker (EOP).  In contrast, Pattern's `next()` handles 
        end of periods invisibly and provides more flexibility for accessing the data.

        ```python
        >>> c = Cycle([1, 2, 3, 4])
        # python's next():
        >>> [next(c) for _ in range(4)]
        [[1, None], [2, None], [3, None], [4, 'EOP']]
        # pattern's next():
        >>>  c.next(4)
        [1, 2, 3, 4]
        ```
        """
        if more is False:
            return self.__next__()[0]
        items = []
        if more is True:
            # collect items until end of period            
            while True:
                i = self.__next__()
                items.append(i[0])
                if i[1] == 'EOP':
                    return items
        for i in range(0, more):
            items.append(self.__next__()[0])
        return items


class Cycle(Pattern):
    """
    Returns a pattern that yields its items in a continuous cycle.

    Parameters
    ----------
    items : list
        The list of values to generate.
    
    period : None | int | subpattern
        The period determines how many elements are read before
        an EOP (end-of-period) flag is returned. The default value
        is None, which allows the pattern to use its default length, 
        usually equal to the number of items in its data.

    Examples
    --------
    ```python
    >>> Cycle([1,2,3]).next(5)
    [1, 2, 3, 1, 2]
    ```
    """
    def __init__(self, items, period=None):
        super().__init__(items, 1, period)
    
    def __next__(self):
        item = Pattern._read(self.items[self.i], tup=True)
        #print(f"after read: item is {item}")
        if item[1] == 'EOP':
            # (sub)item is at the end of its period
            # so increment this pattern's index to the next item 
            if self.i == self.ilen - 1:
                self.i = 0
            else:
                self.i += 1
            # if p is now the last index in the current period
            # signal eop and read the next period length
            #print("self.p:", self.p, "self.plen:", self.plen)
            if self.p == self.plen - 1:
                self.p = 0
                self.plen = Pattern._read(self.period)  # get next period length
                #print(f"after xxx read: plen is {self.plen}")                
            else:
                self.p += 1 
                item[1] = None
        return item


class Palindrome(Pattern):
    """
    Returns a generator that yields its items in a palindrome.

    Parameters
    ----------
    items : list
        The list of values to generate.

    wrap : '++' | '+-' | '-+' | '--'
        Determines how first and last elements are treated when the pattern reverses.
        If the items are [1, 2, 3] then wrap will produce:

        * '++' Both first and last items are repeated: 1,2,3,3,2,1,1,2,3 ...
        * '+-' Only the first item is repeated: 1,2,3,2,1,1,2,3 ...
        * '-+' Only the last item is repeated: 1,2,3,3,2,1,2,3 ...
        * '--' Neither is repeated: 1,2,3,2,1,2,3 ...
    
    period : None | int | subpattern
        The period determines how many elements are read before
        an EOP (end-of-period) flag is returned. By default the
        period length will be equal to the number of items in the list.

    Examples
    --------
    ```python
    >>> palindrome([1,2,3]).next(10)
    [1, 2, 3, 3, 2, 1, 1, 2, 3, 3]
    >>> Palindrome([1,2,3], wrap='+-').next(10)
    [1, 2, 3, 3, 2, 1, 2, 3, 3, 2]
    print(Palindrome([1,2,3], wrap='-+').next(10)
    [1, 2, 3, 2, 1, 1, 2, 3, 2, 1]
    >>> Palindrome([1,2,3], wrap='--').next(10)
    [1, 2, 3, 2, 1, 2, 3, 2, 1, 2]
    ```
    """
    def __init__(self, items, period=None,  wrap='++'):
        match wrap:
            case '++': items = items + items[::-1]    # repeat first and last
            case '+-': items = items + items[-2::-1]  # repeat first not last
            case '-+': items = items + items[-1:0:-1] # repeat last not first
            case '--': items = items + items[-2:0:-1] # dont repeat first or last
            case _:
                raise ValueError(f"Wrap value {wrap} is not '++', '+-', '-+', or '--'.")
        super().__init__(items, 3, period)

    def __next__(self):
        item = Pattern._read(self.items[self.i], tup=True)
        if item[1] == 'EOP':
            if self.i == self.ilen - 1:
                self.i = 0
            else:
                self.i += 1
            if self.p == self.plen - 1:
                self.p = 0
                self.plen = Pattern._read(self.period)  # get next period length
            else:
                self.p += 1 
                item[1] = None
        return item 


class Range(Pattern):
    """
    Range is similar in syntax to Python's range() generator, but its *start*,
    *stop* and *step* parameters will accept integers, patterns, or thunks 
    (lambda expressions or functions of zero arguments). Unlike Python's 
    range() the Range pattern does not terminate: once the step is out-of-bounds 
    the pattern will reset itself to its next start, stop and step values
    as determined by the range values passed in.  Another difference is that
    patterns always return   something, so incompatible start, stop and step specifications will raise
    an error rather than return nothing.

    Parameters
    ----------
    start : int | pattern | thunk
        The initial value to generate.
    stop : int | pattern | thunk
        The limit on the range. This must be strictly larger or smaller 
        than the start.
    step : int | pattern | thunk
        A non-zero increment amount, defaults to 1.
    period : None | int | subpattern
        The period determines how many elements are read before
        an EOP (end-of-period) flag is returned. By default the
        period length will be the distance between start and stop.
    """
    def __init__(self, start, stop=None, step=None, period=None):
        if stop is None:
            stop = start
            start = 0
        if step is None:
            step = 1
        # class init only handles the period value.
        super().__init__([], 0, period)
        # the items field will hold the user's start stop and step values.
        self.items = [start, stop, step]
        # if no period specified then zero out the counters. If a period was
        # specified then uptate
        if not period:
            self.period, self.p, self.plen = None, None, None
        #print("self.period=", self.period, "self.plen=", self.plen, "self.p=", self.p)
        self._setrange()

    def __next__(self):
        # self.range is [start, stop, step, span]
        # start is incremented by step and span is decremented by 1.
        # get current value
        next = [self.range[0], None]
        # increment start by step
        self.range[0] += self.range[2]
        # decrement range count by 1
        self.range[3] -= 1
        # if current range is complete call _setrange() to make a new range
        if self.range[3] == 0:
            self._setrange()
            # if no explict period then signal end of period.
            if not self.period:
                next[1] = 'EOP'
        # if user set an explict period return EOP if at the end.
        if self.period:
            if self.p == self.plen - 1:
                self.p = 0
                self.plen = Pattern._read(self.period)  # get next period length
                next[1] = 'EOP'
            else:
                self.p += 1 
        # return current value
        return next
     
    def _setrange(self):
        names = ["start", "stop", "step"]
        # assign self.range the numeric values [start, stop, step, span]
        # start is the value that ranges, stop is the boundary of 
        # the range, step is the increment, and span is the distance
        # between start and stop. 
        self.range = []
        # self.items could hold constants, patterns or thunks.
        for i,v in enumerate(self.items):
            v = Pattern._read(v)
            # allow only ints.
            if not isinstance(v, int):
                raise TypeError(f"{names[i]} value {v} is not an integer.")
            self.range.append(v)
        start, stop, step = self.range
        # step cannot be zero, if step is positive then start must be
        # strictly less than stop, if step is negative then start must
        # be strictly larger than stop.
        if not ((start < stop and step > 0) or (start > stop and step < 0)):
            raise ValueError(f"Step {step} not in range for start={start} stop={stop}.")
        # set the span of the pattern to the initial distance between
        # start and stop as a positive integer. so if its a descending 
        # range swap start and stop and insure step is positive.
        if step < 0:
            start, stop = stop, start
            step = abs(step)
        self.range.append(ceil((stop - start) / step))
        #print(f"Range: start={start}, stop={stop}, step={step} period={self.period}")        

        
class Shuffle(Pattern):
    """
    Returns a pattern that yields its items by random permutation.

    Parameters
    ----------
    items : list  
        The list of items to generate. Each item in the list
        can be a python object or a sub-pattern.

    period : None | int | subpattern
        The period determines how many elements are read before
        an EOP (end-of-period) flag is returned. The defaule value
        is none, which means the shuffle'a period length will be
        equal to the number of items in the pattern.

    norep : bool
        If true then after shuffles the next item cannot repeat
        the last item produced.

    Examples
    --------
    The first example permits direct repetition between shuffles, the second forbids it.
    ```python
    >>> Shuffle(["a","b","c"]).next(12)
    ['c', 'a', 'b', 'b', 'a', 'c', 'a', 'b', 'c', 'c', 'b', 'a']
    >>> Shuffle(["a","b","c"], norep=True).next(12)
    ['a', 'c', 'b', 'c', 'b', 'a', 'c', 'a', 'b', 'c', 'a', 'b']
    ```
    """
    def __init__(self, items, period=None, norep=False):
        super().__init__(items.copy(), 1, period)
        # initialize for first period
        random.shuffle(self.items)
        self.norep = norep

    def __next__(self):
        item = Pattern._read(self.items[self.i], tup=True)
        if item[1] == 'EOP':
            # at end of items, reshuffle
            if self.i == self.ilen - 1:
                self.i = 0
                last = self.items[-1]
                random.shuffle(self.items)
                # continue to shuffle if user specified no repeat
                # and the next item is the same as the last
                while (self.norep and self.items[0] == last and self.ilen > 1):
                    random.shuffle(self.items)             
            else:
                self.i += 1
            if self.p == self.plen - 1:
                self.p = 0
                self.plen = Pattern._read(self.period)  # get next period length
            else:
                self.p += 1 
                item[1] = None
        return item 


class Choose(Pattern):
    """
    Yields its items by weighted random selection.
    By default all items have an equal probability of being returned.

    Parameters
    ----------
    items : list
        The list of items to generate.  Each item in the list can
        be an item or a list: [item weight] where the first value is
        the item to return and weight is the probability of the item
        being selected relative to the other items in the list. If
        no weight is provided for an item it receives a default 
        weight of 1.0. If no weights are provided then all the items
        are chosen with equal probability.

    weights : list | None
        A list of relative probablity weights that determine the likelyhood
        of its corresponding pattern item being returned. If no weights are
        provided then items are chosen with equal probability. Relative
        weights do not have to sum to 1 because the pattern automatically 
        converts them to probabilities. In addtion to numerical weifhts,
        dynamic weight *expressions* consisting of lambda expressions or
        functions of 0 arguments can also be specified. Dynamic weight
        expressions are reevaluated each time the pattern begins a new
        period to allow the pattern choices to evolve over time.
    
    period : None | int | subpattern
        The period determines how many elements are read before
        an EOP (end-of-period) flag is returned. By default the
        the period will be equal to the number of items in the list.

    Examples
    --------
    In this example the value 3 likely appears half the time.
    ```python
    >>> Choose([1,2,3], [1,1,2]).next(10)
    [3, 2, 1, 3, 1, 3, 3, 3, 1, 3]
    ```
    """
    def __init__(self, items, weights=[], period=None):
        super().__init__(items, 1, period)
        self.weights = weights.copy()
        if not self.weights:
            # equal probablity for each item. weights will hold monotonically
            # increasing, equally proportioned, exclusive upper bounds upto
            # and including 1.0. example: end=5 => [0.2, 0.4, 0.6, 0.8, 1.0]
            #self.weights = [(i+1)/self.ilen for i in range(self.ilen)]
            self.weights = [1 for _ in range(self.ilen)]
        elif not isinstance(self.weights, list):
            raise TypeError(f'Weights {self.weights} is not a list.')
        elif self.ilen < len(self.weights):
            raise IndexError('Too many weights provided.')
        elif self.ilen > len(self.weights):
            raise IndexError('Too few weights provided.')
        ####print('raw weights:', self.weights)       
        # evalindexes will hold the index(es) of weight
        # expressions that have to be dynamically evaluated.
        self.evalindexes = []
        for i,w in enumerate(weights):
            if isinstance(w, (int, float)):
                pass
            elif callable(w):
                self.evalindexes.append(i)
            else:
                raise IndexError(f"Weight {w} is not an int, float or thunk.")
        self._calcprobabilities()
        self._chooseactiveitem()
    
    def _calcprobabilities(self):
        '''
        Calculates a probability map from the user specified list
        of probability weights, any of which may be dynamic. Example:
            user weights: [1, 2, 3, 4]
            normalize to 1.0: [0.1, 0.2, 0.3, 0.4]
            probability map: [0.1, 0.3, 0.6, 1.0]
        the probability map splits the range [0-1) into proportional
        distribution indexes:
            indexes:   0        | 1         | 2         | 3
            segments:  0->.1=.1 | .1->.3=.2 | .3->.6=.3 | .6->1.0=.4
        Therefore, a uniform random number [0-1) will land in index 3 cell
        four times more often than in the index 0 cell, so the pattern's 
        item at index 3 will be returned four times as often as the 
        item at index 0.
        '''
        total = 0
        # copy user's weights to probabilities.
        self.probabilities = self.weights.copy()
        # calc total weight, for thunks eval them 
        # to get their current weight.
        for i,w in enumerate(self.probabilities):
            if i in self.evalindexes:
                w = w()  # evalute the thunk
                self.probabilities[i] = w
            total += w
        ####print("probabilities 1:", self.probabilities)
        # total weight is known and probablities list contains
        # only numeric weight values. rescale each weight so it
        # is now a fractional proportion of the total.
        for i,w in enumerate(self.probabilities):
            self.probabilities[i] = w/total
        ####print("probabilities 2:", self.probabilities)
        # convert values to monotonically increasing points from
        # 0 upto 1. the distance between points will be proportional
        # to their weight. 
        for i in range(1, self.ilen):
            self.probabilities[i] += self.probabilities[i-1]
        ####print("probabilities 3:", self.probabilities)

    def _chooseactiveitem(self):
        """
        pick the next item by generating a random value beween
        zero and one and then finding the first index in 
        self.probabilities whose value is greater than the random
        value. the item at the corresponding index in self.items
        is the next item to return.
        """
        val = random.random()
        for i in range(self.ilen):
            if val < self.probabilities[i]:
                self.activeitem = self.items[i]
                break

    def _hasdynamicweights(self):
        '''Returns true if pattern contains one or more dynamic weights.'''
        return True if self.evalindexes else False
    
    def __next__(self):
        item = Pattern._read(self.activeitem, tup=True)
        if item[1] == 'EOP':
            # at end of period, choose the next item
            self._chooseactiveitem()            
            if self.p == self.plen - 1:
                self.p = 0
                self.plen = Pattern._read(self.period)  # get next period length
                # if dynamic weight expressions recalculate probabiliies
                if self._hasdynamicweights():
                    ####print("recalculating weights")
                    self._calcprobabilities()
            else:
                self.p += 1 
                item[1] = None
        return item 


class Graph (Pattern):
    """
    The Graph pattern is a network of nodes, each node is a 2- or 3-tuple
    containing a *item*, *link*, and optional *id*.  The *item* is
    value to return from the node, and can be a pyton object, a subpattern,
    or thunk. The node's *link* is the identifier for the next node to 
    visit, and *id* is this node's unique id in the graph. If no id is given
    it will be set to the 1-based position of the node in the node list.
    
    Example
    -------
    A cycle of A B C as a graph (the first node is
    always followed by node 2, the second node by node 3, and node 3
    returns to node 1:
    ```python
    Graph( [('a', 2), ('b', 3), ('c', Cycle([1, 2])])
    ```
    """
    def __init__(self, items, period=None):
        super().__init__(items.copy(), 1, period)
        for i,n in enumerate(self.items):
            if isinstance(n, tuple):
                # if node id not provided set it to node's one-based index i+1.
                if len(n) == 2:
                    self.items[i] = n + (i+1,)
                elif len(n) < 2:
                    raise TypeError(f'Graph node {n} missing link value.')
                elif len(n) > 3:
                    raise TypeError(f'Too many elements in graph node {n}.')
            else:
                raise TypeError(f'Graph node {n} is not a tuple.')
        # set first node to be active node
        self.activenode = self.items[0]
        #print(f'nodes: {self.items}')
        #print(f'active node: {self.activenode}')
            
    def __next__(self):
        item = Pattern._read(self.activenode[0], True)
        #print(f"after read: item is {item}")
        if item[1] == 'EOP':
            # current node at end of period, choose the next node.
            self._nextactivenode()
            # check if this pattern is at EOP           
            if self.p == self.plen - 1:
                self.p = 0
                self.plen = Pattern._read(self.period)  # get next period length
            else:
                self.p += 1 
                item[1] = None
        return item
    
    def _nextactivenode(self):
        """
        Evaluate this node's link (identifier), find that
        node in the graph and make it the active node.
        """
        nextid = Pattern._read(self.activenode[1], False)
        #print(f"nextid: {nextid}")
        for i in range(self.ilen):
            if self.items[i][2] == nextid:
                self.activenode = self.items[i]
                #print(f"new active node: {self.activenode}")
                return
        raise ValueError(f"No node found for node id {nextid}.")


class Rotation(Pattern):
    """
    Permutes its items using one or more swapping rules.
    
    Parameters
    ----------
    items : list
        The list of items to generate

    swaps : list | Pattern
        A list of one or more swapping rules or a pattern that
        produces swapping rules. A swapping rule is a list of (up to) four 
        integers that control the iterative process applied to 
        all the items in order to produce the next generation of items:
        ```[start, step, width=1, end=len]```
        Start is the location (zero based index) in the pattern's data to begin
        swapping from, step is the rightward increment to move to the next swap
        start, width is the distance between the elements swapped.  End is the
        position in the item list to stop the swapping at, and defaults to the
        length of the item list.
        
    period : None | int | subpattern
        The period determines how many elements are read before
        an EOP (end-of-period) flag is returned. By default the
        shuffle period will be equal to the number of items in the list.

    Examples
    --------
    ```python
    >>> r = Rotation(['a', 'b', 'c', 'd'], swaps=[0, 2, 1, 3])
    >>> r.next(True)
    ['a', 'b', 'c', 'd']
    >>> r.next(True)
    ['b', 'a', 'c', 'd']
    >>> r.next(True)
    ['a', 'b', 'c', 'd']
    ```
    """
    def __init__(self, items, swaps, period=None):
        super().__init__(items.copy(), 1, period)
        isseq = lambda a: isinstance(a, (list, tuple))
        isint = lambda a: isinstance(a, int)
        if isseq(swaps): # swaprules is a list or tuple
            if all(map(lambda x: isseq(x), swaps)):   # a list of rules
                self.source = Cycle(swaps)
            elif all(map(lambda x: isint(x), swaps)): # the list is one rule
                self.source = Cycle([swaps])
        if not isinstance(self.source, Pattern):
            raise ValueError(f"Swap rules {swaps} is not a list or Pattern.")
        self.size = len(items)

    def __next__(self):
        item = Pattern._read(self.items[self.i], tup=True)
        #print(f"after read: item is {item}")
        if item[1] == 'EOP':
            # (sub)item is at the end of its period
            # so increment this pattern's index to the next item 
            if self.i == self.ilen - 1:
                self.i = 0
                # we've yielded all items in the current generation
                # so do the rotations to create the next generation.
                rule = Pattern._read(self.source, tup=False)  #next(self.source)
                rlen = len(rule)
                start = rule[0]
                step = rule[1]
                width = rule[2] if rlen > 2 else 1
                end = rule[3] if rlen > 3 else self.ilen 
                #print("rule:", rule, "rlen:", rlen, "start:", start, "step:", step, "width:", width, "end:", end)
                # iterate left to right swapping items according to rule 
                for a,b in zip(range(start, end, step), range(start+width, end, step)):
                    self.items[a], self.items[b] = self.items[b], self.items[a]
            else:
                self.i += 1
            # if p is now the last index in the current period
            # signal eop and read the next period length
            #print("self.p:", self.p, "self.plen:", self.plen)
            if self.p == self.plen - 1:
                self.p = 0
                self.plen = Pattern._read(self.period)  # get next period length
                #print(f"after xxx read: plen is {self.plen}")                
            else:
                self.p += 1 
                item[1] = None
        return item
    
    def all(self, grouped=False, wrapped=False):
        """
        Return a list of all rotations and stops when the first rotation occurs again.
        Warning: rules that do not produce the original generation will trigger
        an infinite loop!

        Parameters
        ----------
        grouped : bool
            If grouped is True then each generation is collected as a sublist,
            otherwise the rotated items are returned in one flat list.
        wrapped : bool
            If wrapped is True then the first generation will also be appended
            to the end of list returned.
        """
        size = self.ilen
        data = []
        conc = data.append if grouped else data.extend
        init = [self.__next__()[0] for _ in range(size)]
        conc(init)
        while (True):
            more = [self.__next__()[0] for _ in range(size)]
            if init == more:
                break
            conc(more)
        if wrapped:
            conc(init)
        return data
    
    
class Markov(Pattern):
    """
    Yields items in a Markov chain. The chain is expressed as a dictionary of 
    rules, each rule associates a tuple of one or more past outcomes with a 
    list of weighted potential outcomes:

    `{(past,...): [[outcome, weight], [outcome, weight], ...],  ...}`
    
    There are two shortcuts available when specifying rules:

    * If the rules use only one past value (markov order 1) then you can provide
    values as keys instead of tuples.
    * If an outcome has a probability weight of 1 then you can specify just the
    value instead of a two element list containing the value and 1.
 
    Parameters
    ----------
    rules : list
        A dictionary of rules that generate the Markov chain. Each rule is a
        key and value pair, where the key is a tuple of 1 or more past outcomes
        and the value is a list of pairs [[outcome, weight1], [outcome2, weight2],...]
        representing each possible next outcome together with its weight (probability).
        The length of the tuples determines the markov order of the generator
        and all rules must ha be the same and it .
        The <next> columns in the rule contain the potential next outcomes 
        with their probability weights. Each column can contain just an outcome,
        in which case it will be assigned a probability weight of 1, or it can 
        be expressed as a list [next, weight].
    stop : int | None
        The number of times to read from the pattern before stopping.
        If None then the generator is unbounded. The default is None.
    preset : past
        If specified it is the initial 'past' the markov chain uses to generate
        the first outcome.
    Returns
    -------
    The next item in the pattern.

    Examples
    --------
    A 1st order markov process with three rules:

    1. If the last outcome was 'a' then the next outcome is either 'b' or 'c', with 'c' three times as likely as 'b'.
    2. If the last outcome was 'b' then the next outcome is 'a'.
    3. If the last outcome was 'c' then the next outcome is either 'a', 'c' or 'b', with 'c' being the least likely and 'a' being the most likely outcome.
    
    ```python
    >>> m = Markov({'a': ['b', ['c', 3]], 
                    'b': ['a'],
                    'c': [['a', 5], 'c', ['b', 2.5]]})
    >>> "".join( m.next(20)) )
    cabacbabaccbabaccaca                
    ```
    """
    def __init__(self, items, period=None, preset=None):
        # init accepts a list, not a dict to initialize the pattern
        super().__init__(list(items.keys()), 1, period)
        # after init call set items to the actual dictionary
        self.items = items
        if preset and not isinstance(preset, tuple):
                preset = (preset,)
        data = {}
        order = 0  # the order of the markov process is the number of past events
        for key, value in self.items.items():
            # key holds previous outputs to match
            if not isinstance(key, tuple):
                key = (key,)
                #print("converted key to tuple ->", key)
            elif not len(key) > 0:
                raise TypeError('Rule key {key} is empty.')
            # value holds a list [[n1, w1], [n2, w2],...]
            if not isinstance(value, list):
                raise TypeError('Dictionary value {value} is not a list.')
            if not order:
                order = len(key)
                #print("initialized order to ", order)
            elif order != len(key):
                raise IndexError(f"Rule matches of differnt lengths: {order} and {len(key)}.")
            weight = 0  # calculated total weight of all the outcomes in the rule
            outcomes = []
            for col in value:
                # col is either an outcome or a list: [outcome, weight]
                # normalize to a list and sum their weights
                if isinstance(col, list):
                    if len(col) == 2:
                        if isinstance(col[1], (int, float)):
                            weight += col[1]
                            outcomes.append(list(col)) # copy the user's list
                        else:
                            raise ValueError(f"Outcome weight {col} is not an int or float.")
                    else:
                        raise IndexError("Outcome {col} is not a two element list [outcome, weight].")
                else:
                    weight += 1
                    outcomes.append([col, 1])
            # convert weights into probabilities 0.0 < p... < 1.0
            # convert first outcome's weight into a probability.
            outcomes[0][1] = outcomes[0][1] / weight
            # now convert the weights above it into probabilities and  
            # add to the previous probability. the result will be the
            # total probabilty 0-1 sectioned proportionally according
            # to the weights of the outputs
            for i in range(1, len(outcomes)):
                outcomes[i][1] = outcomes[i-1][1] + (outcomes[i][1]/weight)
            # assign outcomes to the key
            data[key] = outcomes
        # use the user's preset or the first past in the dictionary.
        if not preset:
            preset = next(iter(data)) # use first rule's past
        else:
            if order == len(preset):
                preset = list(preset) # copy users preset
            else:
                raise IndexError(f'Preset value {preset} is not a list of {order} \
                    {"elements" if order > 1 else "element"}.')
        # initialize the history to the preset. older values are to the left
        self.items = data
        self.history = preset

    def __next__(self):
        #item = Pattern._read(self.items[self.i], tup=True)
        # find the rule that matches current history
        outcomes = self.items.get(self.history)
        if not outcomes:
            raise ValueError(f'No rule match for {self.history}.')
        # find the next outcome
        randnum = random.random()
        outcome = None
        # find the outcome for the random number
        for out in outcomes:
            if randnum < out[1]:
                outcome = out[0] # next outcome
                break       
        # outcome is a tuple to left-shift history with current 
        # choice appended, and as a return value to Pattern.next()
        outcome = (outcome,)
        self.history = self.history[1:] + outcome
        return outcome

    @staticmethod
    def analyze(data, order=1):
        """
        A factory method that returns a new Markov pattern whose characteristics
        reflect the input data's structure at the given markov order. 
        
        Parameters
        ----------
        data : list
            The list of data to analyze.
        order : int
            The markov order for the analysis.

        Returns
        -------
        A Markov pattern that generates results based on the data and markov order.

        Examples
        --------
        ```python
        >>> m = Markov.analyze([2, 2, 1, 3, 4, 4, 1, 2], 1)
        >>> m.rules
        {(2,): [[2, 0.6666666666666666], [1, 1.0]], (1,): [[3, 0.5], [2, 1.0]], (3,): [[4, 1.0]], (4,): [[4, 0.5], [1, 1.0]]}
        >>> m.next(20)
        [1, 2, 2, 2, 1, 3, 4, 4, 1, 3, 4, 1, 2, 2, 1, 3, 4, 4, 4, 4]
        ```
        """
        # each window is a list of one or more past values followed
        # by the subsequent value: (past+, next)
        windows = []
        end = len(data)
        for i in range(end):
            windows.append(tuple(data[(i+j) % end] for j in range(order+1)) )
        histogram = {}
        for w in windows:
            if histogram.get(w):
                histogram[w] += 1
            else:
                histogram[w] = 1
        #print(histogram)
        rules = {}
        for item in histogram.items():
            # tuple of one or more past outcomes
            past_outcome = item[0][:-1] 
            future_outcome = item[0][-1]
            future_weight = histogram[item[0]]
            if rules.get(past_outcome):
                rules[past_outcome].append([future_outcome, future_weight])
            else:
                rules[past_outcome] = [[future_outcome, future_weight]]
        return Markov(rules)


class States(Pattern):
    """
    Returns values from a state machine (cellular automata) and applies
    a transition function to update states to their next value.

    Parameters
    ----------
    states : list    
        A list containing the initial states of the cellular automata. A
        flat list of states produces a one dimensional automata and a row
        major list of lists will create a two dimensional automata.

    transitions : function
        The transitions function implements the automata's state 
        transitions. The function is automatically called and passed 
        two arguments, the pattern's state array and the index of the
        current cell in the states.  Your transition function should
        call `getstate()` to access one or more neighbor states of 
        the current cell in order to calculate its next state.

    Examples
    --------
    A transition function recives the pattern's array of states and
    the index to the current state. This function calls `getstate()`
    to accesses the cells to the left and right of the current cell
    and returns their sum mod 4, which then becomes the next value
    of the cell at the current state index.
    ```python
    def add_neighbors(cells, index):
        left = States.getstate(cells, index, -1)
        right = States.getstate(cells, index, 1)
        return (left + right) % 4

    >>> cells = States([0,1,0,1,0], transitions=add_neighbors)
    >>> for _ in range(5): print(cells.next(5))
    [0, 1, 0, 1, 0]
    [1, 0, 2, 0, 1]
    [1, 3, 0, 3, 1]
    [0, 1, 2, 1, 0]
    [1, 2, 2, 2, 1]
    ```
    """

    def __init__(self, cells, transitions):
        super().__init__(cells, 1)
        if not callable(transitions):
            raise TypeError(f"transitions {transitions} is not a function.")
        if isinstance(cells[0], list):
            # cells is a 2D automata (a list of lists)
            self.indexes = [(row, col) for row in range(len(cells)) for col in range(len(cells[0]))]
            self.period = len(self.indexes)
            # current is a 2D copy of cells with at least 1 row and col
            self.current = [list(r) for r in cells] # list(r) is copy
            # future same as values but set to 0's
            self.future = [[0 for _ in r] for r in cells]
        else:
            # cells is a 1D automata but see below.
            self.indexes = [(0, col) for col in range(len(cells))]
            self.period = len(self.indexes)
            # current is a 2D copy of cells with at least 1 row and col
            self.current = [list(cells)]   # list(cells) is copy
            # future as values but set to 0's
            self.future = [[0 for _ in cells]] # init future to 0's.
        self.transitions = transitions
        # reverse the states so that when the loop starts and
        # flips with j == 0 the present states will be correct
        self.current, self.future = self.future, self.current
        #print('current:', self.current, 'future:', self.future, 'indexes:', self.indexes)

    def __next__(self):
        j = self.i % self.period
        if j == 0:
            #print("flipping present and future i=", self.i)
            self.current, self.future = self.future, self.current
        pos = self.indexes[j]
        val = self.current[pos[0]][pos[1]]
        nxt = self.transitions(self.current, pos)
        #print("transitions value:", val)
        self.future[pos[0]][pos[1]] = nxt
        self.i += 1
        return (val,)

    @staticmethod
    def getstate(cells, pos, inc):
        """
        Call getstate() inside your States's transitions function to
        return the value (state) of the cell at position pos+inc.
        The new position pos+inc will automatically wrap mod the size of the cells
        array so cell access will never be out of bounds.

        Parameters
        ----------
        cells : list
            An array of cells holding the cellular automata's current states.

        pos : tuple
            The (*row*, *col*) index of the current cell in the cells array.
            Your rule function will receive this position in its pos argument.
            To access a neighbor cell, pass the pos value to getstate() along
            with a positional increment *inc*.
        
        inc : int | tuple
            A positive or negative offset to add to pos to calculate the position of the
            neighbor cell. This must be a tuple (*row*, *col*) for 2D automata. For 1D
            cases you can specify a positive or negative integer, or a tuple (0, *col*).

        Returns
        -------
        The value of the neighbor cell at pos+inc.
        """
        if not isinstance(inc, tuple):
            inc = (0, inc)
        row = (pos[0] + inc[0]) % len(cells)
        col = (pos[1] + inc[1]) % len(cells[0])
        #print("CELLS:", cells)
        return cells[row][col]

if __name__ == '__main__':
    pass

