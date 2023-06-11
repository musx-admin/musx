import types
from collections.abc import Iterator
import random
import matplotlib.pyplot as plt

class Pattern(Iterator):

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
        self.plen = self.read(self.period) if isinstance(self.period, Iterator) else self.period
        #print("***plen is:", self.plen)
        # period counter
        self.p = 0
        # 'EOP' if the pattern just returned the last value of the current period
        self.eop = None

    def __iter__(self):
        return self

    def _pname(self):
        return self.__class__.__name__
    
    @staticmethod
    def read(pat, tup=False):
        #print(f"read input: ({pat},tup={tup})")
        if isinstance(pat, Pattern):
            x = next(pat)
            return x if tup else x[0]
        else:
            return [pat, "EOP"] if tup else pat


class Cycle(Pattern):

    def __init__(self, items, period=None):
        super().__init__(items, 1, period)
    
    def __next__(self):
        item = Pattern.read(self.items[self.i], tup=True)
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
                self.plen = Pattern.read(self.period)  # get next period length
                #print(f"after xxx read: plen is {self.plen}")                
            else:
                self.p += 1 
                item[1] = None
        return item


class Palindrome(Pattern):

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
        item = Pattern.read(self.items[self.i], tup=True)
        if item[1] == 'EOP':
            if self.i == self.ilen - 1:
                self.i = 0
            else:
                self.i += 1
            if self.p == self.plen - 1:
                self.p = 0
                self.plen = Pattern.read(self.period)  # get next period length
            else:
                self.p += 1 
                item[1] = None
        return item 
 

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
        an EOP (end-of-period) flag is returned. By default the
        shuffle period will be equal to the number of items
        in the list.
    norep : bool
        If true then items cannot repeat after a shuffle.

    Returns
    -------
    The next item in the pattern.

    Raises
    ------
    * TypeError if items is not a list of one or more items.

    Examples
    --------
    ```python
    >>> p = jumble([1,2,3])
    >>> [read(p) for _ in range(10)]
    [1, 3, 2, 3, 2, 1] 
    ```
    """

    def __init__(self, items, period=None, norep=False):
        super().__init__(items.copy(), 2, period)
        # initialize for first period
        random.shuffle(self.items)
        self.norep = norep

    def __next__(self):
        item = Pattern.read(self.items[self.i], tup=True)
        if item[1] == 'EOP':
            # at end of items, reshuffle
            if self.i == self.ilen - 1:
                self.i = 0
                last = self.items[-1]
                random.shuffle(self.items)
                # continue to shuffle if user specified no repeat
                # and the next item is the same as the last
                while (self.norep and self.items[0] == last):
                    random.shuffle(self.items)             
            else:
                self.i += 1
            if self.p == self.plen - 1:
                self.p = 0
                self.plen = Pattern.read(self.period)  # get next period length
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

    Returns
    -------
    The next item in the pattern.
    
    Raises
    ------
    * TypeError: if items is not a list
    * ValueError: if a probability is not a float or int greater than 0        
    
    Examples
    --------
    ```python
    >>> p = choose(['A',['B', 2] 'C'])]
    [p.next() for _ in range(8)]
    ```
    """
    def __init__(self, items, period=None):
        super().__init__(items, 1, period)
        weights, self.items = [],[]
        for i in items:
            if isinstance(i, list):
                if len(i) != 2 or not isinstance(i[1], (int, float)):
                    raise TypeError(f"{self._pname()}: {i} is not a two element list [item, probability]")
                elif i[1] <= 0:
                    raise ValueError(f"{self._pname()}: item {i} probability value {i[1]} is not greater than 0.0.")    
                else: 
                    self.items.append(i[0])
                    weights.append(i[1])
            else: 
                self.items.append(i)
                weights.append(1)
        #print("raw weights:", weights)
        # normalize weights to values summing to 1.0
        total = sum(weights)
        normalized = [weights[i] / total for i in range(len(weights))]
        #print("normalized weights:", normalized)
        # Convert normalized weights into a monotonically increasing 
        # probability map between 0.0 and 1.0
        # Example
        #     items:      [     'A', 'B', 'C', 'D', 'E']
        #     normalized: [     0.1, 0.2, 0.3, 0.1, 0.3]
        #     probmap:    [0.0, 0.1, 0.3, 0.6, 0.7, 1.0]
        self.probmap = [0.0] + [sum([normalized[i] for i in range(0, w)]) 
                                for w in range(1, len(normalized))] + [1.0]
        #print("probmap:", self.probmap)
        self._chooseactiveitem()
        #print("activeitem:", self.activeitem)
    
    def _chooseactiveitem(self):
        """
        Selects a random number N between 0 and 1 and iterates 
        adjacent values in the probmap to find the pair with
        a left value <= N and a right value > N. 
        The index of the left value is the index of the next 
        item to select.
        """
        N = random.random()
        I = None
        for i in range(1, len(self.probmap)):
            #print(self.probmap[i-1], self.probmap[i])
            if (N >= self.probmap[i-1]) and N < self.probmap[i]:
                I = i-1
                #print("index:", I, ", value:",  self.items[I])
                break
        assert I != None, f"Probability {N} not [0.0-1.0)"
        self.activeitem = self.items[I]
    
    def __next__(self):
        item = Pattern.read(self.activeitem, tup=True)
        if item[1] == 'EOP':
            # at end of period, choose the next item
            self._chooseactiveitem()            
            if self.p == self.plen - 1:
                self.p = 0
                self.plen = Pattern.read(self.period)  # get next period length
            else:
                self.p += 1 
                item[1] = None
        return item 


class Rotation(Pattern):
    """
    Permutes its items using one or more swapping rules.
    
    Parameters
    ----------
    items : list
        The list of items to generate
    swaps : list | Pattern
        A list of or more swapping rules or a generator that
        produces swapping rules. A swapping rule is a list of (up to) four 
        integers that control the iterative process applied to 
        all the items in order to produce the next generation of items:
        ```[start, step, width=1, end=len]```
        Start is the location (zero based index) in the pattern's data to begin
        swapping from, step is the rightward increment to move to the next swap
        start, width is the distance between the elements swapped.  End is the
        position in the item list to stop the swapping at, and defaults to the
        length of the item list.
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
        item = Pattern.read(self.items[self.i], tup=True)
        #print(f"after read: item is {item}")
        if item[1] == 'EOP':
            # (sub)item is at the end of its period
            # so increment this pattern's index to the next item 
            if self.i == self.ilen - 1:
                self.i = 0
                # we've yielded all items in the current generation
                # so do the rotations to create the next generation.
                rule = Pattern.read(self.source, tup=False)  #next(self.source)
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
                self.plen = Pattern.read(self.period)  # get next period length
                #print(f"after xxx read: plen is {self.plen}")                
            else:
                self.p += 1 
                item[1] = None
        return item
    
    def all(self, grouped=False, wrapped=False):
        """
        Return a list of all rotations and stops when the first rotation occurs again.
        Warning: rules that do not produce the original generation will produce
        an infinite loop.

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


if __name__ == '__main__':

    #p = Cycle(['A', Cycle([100,200, 300], 4),'C'])
    p = Cycle([100, Cycle(['A', 'B'], period=4),300])
    p = Cycle([100, Cycle(['A', 'B'], period=Cycle([2,5,4])), 300])
    p = Cycle(['A', 'B'], period=Cycle([2,5,4]))
    #p = Shuffle(['A'], period=Cycle([2,5,4]), norep=True)
    #p = Choose([['A', 1], ['B', 2],['C', 3], ['D', 1], ['E', 3]])
    p = Choose([[Cycle([2,5,4]), 1], ['B', 2],['C', 3]])

    #p = Cycle(['x', 'y', Cycle([100, Cycle(['A', 'B', 'C'], 4),300]), 'z'])
    #p = Cycle([100, Cycle(['A', 'B', 'C'], 4),300])
    #p = Cycle(['A', 'B', 'C', 'D', 'E'], Cycle([1,2,3]))
    #p = Cycle([100, Cycle(['A', Cycle(['x','y'], 4), 'C']), 300])
    #p = Cycle([100, 200, 300, 400, 500, 600,], period=Cycle([1,2,3,4]))
        
    # def plot(data):
    #     plt.plot(data)
    #     plt.show()
        
    # def histo(data):
    #     plt.hist(data, bins=30, facecolor="blue", alpha=0.5) 
    #     plt.show()

    # data = [next(p)[0] for _ in range(2000)]
    # histo(data)

    data = ['a', Cycle(['b1', 'b2', 'b3']),'c']
    #data = ['a', 'b', 'c']
    rule = [0, 1, 1]
    #rule = [[0, 1, 1, 2], [1, 1, 1, 3]]
    rgen = Rotation(data, rule, period=5)
    #for g in range(8):
    #    print(f"gen{g+1}: {[next(rgen)[0] for _ in range(len(data))]}")
    print(rgen.all())



#    data = ['a','b','c']
#    rule = [[0, 1, 1, 2], [1, 1, 1, 3]]
#    for g, gen in enumerate(musx.all_rotations(data, rule, True, True)):
#        print(f"gen{g+1}: {gen}")
#        #print(musx.all_rotations(data, rule, False, False))

# for _ in range(25):
#     z=next(p)
#     print(f"pattern output {_ + 1:02}: {z}")
#     histo[z[0]] += 1
# print("histo:", histo)