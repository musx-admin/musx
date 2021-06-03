###############################################################################
"""
A collection of python generators that produce many different patterns in data,
from simple looping and randomness to more complex processes such as markov
chains, cellular automata and chaos.
"""

import random as ran
from sys import maxsize as max_int
from .ran import between
from .tools import isnum, isseq, isgen

def cycle(items, stop=None):
    """
    Returns a generator that yields its items in a continuous cycle.

    Parameters
    ----------
    items : list
        The list of values to generate.
    
    stop : int | None
        The number of times to read from the pattern before stopping.
        If None then the generator is unbounded. The default is None.

    Returns
    -------
    The next item in the pattern.

    Raises
    ------
    * TypeError: if items is not a list.
    * ValueError: if items is an empty list.
    * TypeError: if stop is not an int.

    Examples
    --------
    >>> [cycle([1,2,3]) for _ in range(5)]
    [1, 2, 3, 1, 2]
    """
    if stop == None:
        stop = max_int
    if not isinstance(items, list):
        raise TypeError(f'Items value {items} is not a list.')
    end = len(items)
    if end < 1:
        raise ValueError('Items list is empty.')
    if not isinstance(stop, int):
        raise TypeError(f"Stop value {stop} is not an integer.")
    pos = 0
    for _ in range(stop):
        yield items[pos]
        pos += 1
        if pos >= end:
            pos = 0


def jumble(items, stop=None, norep=False):
    """
    Returns a generator that yields its items in random permutation.

    Parameters
    ----------
    items : list  
        The list of values to generate.

    stop : int | None
        The number of times to read from the pattern before stopping.
        If None then the generator is unbounded. The default is None.
    norep : bool
        If true then items cannot repeat after a shuffle.
    Returns
    -------
    The next item in the pattern.

    Raises
    ------
    * TypeError: if items is not a list.
    * ValueError: if items is an empty list.
    * TypeError: if stop is not an int.

    Examples
    --------
    ```python
    >>> [jumble([1,2,3]) for _ in range(6)]
    [1, 3, 2, 3, 2, 1] 
    ```
    """
    if stop == None:
        stop = max_int
    if not isinstance(items, list):
        raise TypeError(f'Items value {items} is not a list.')
    end = len(items)
    if end < 1:
        raise ValueError('Items list is empty.')
    if not isinstance(stop, int):
        raise TypeError(f"Stop value {stop} is not an integer.")
    pos = 0
    items = list(items) # copy before shuffling!
    ran.shuffle(items)
    last = items[-1]
    for _ in range(stop):
        yield items[pos]
        pos += 1
        if pos >= end:
            pos = 0
            ran.shuffle(items)
            if norep and end>1:
                while (items[0] == last):
                    ran.shuffle(items)
            last = items[-1]


def palindrome(items, stop=None, wrap='++'):
    """
    Returns a generator that yields its items in a palindrome.

    Parameters
    ----------
    items : list
        The list of values to generate.
    stop : int | None
        The number of times to read from the pattern before stopping.
        If None then the generator is unbounded. The default is None.
    wrap: str
        Determines if first and last elements are repeated when the pattern reverses. 
        For example if the items are [1, 2, 3] then wrap will produce:

        * '++' : both first and last are repeated: 1,2,3,3,2,1,1,2,3 ...
        * '+-' : Only the first is repeated: 1,2,3,2,1,1,2,3 ...
        * '-+' : Only the last is repeated: 1,2,3,3,2,1,2,3 ...
        * '--' : Neither is repeated: 1,2,3,2,1,2,3 ...

    Returns
    -------
    The next item in the pattern.
    
    Raises
    ------
    * TypeError: if items is not a list.
    * ValueError: if items is an empty list.
    * TypeError: if stop is not an int.
    * ValueError if wrap is not one of the allowed values.

    Examples
    --------
    ```python
    >>> [palindrome([1,2,3]) for _ in range(8)]
    [1, 2, 3, 3, 2, 1, 1, 2]
    ```
    """
    if stop == None:
        stop = max_int
    if not isinstance(items, list):
        raise TypeError(f'Items value {items} is not a list.')
    end = len(items)
    if end < 1:
        raise ValueError('Items list is empty.')
    if not isinstance(stop, int):
        raise TypeError(f"Stop value {stop} is not an integer.")
    pos = 0
    indexes = [i for i in range(end)]
    if wrap == '++' :
        indexes += indexes[::-1]    # repeat first and last
    elif wrap == '+-':
        indexes += indexes[-2::-1]  # repeat first not last
    elif wrap == '-+':
        indexes += indexes[-1:0:-1] # repeat last not first
    elif wrap == '--':
        indexes += indexes[-2:0:-1] # dont repeat first or last
    else:
        raise ValueError(f"Wrap value {wrap} is not ++, +-, -+, or --.")
    end = len(indexes)
    for _ in range(stop):
        yield items[indexes[pos]]
        pos += 1
        if pos >= end:
            pos = 0


def steps(start, step, stop=None):
    """
    A generator that returns a value incremented by a stepping amount.

    Parameters
    ----------
    start : int
        The initial step value to generate.
    step : int
        The amount to add to the step each time.
    stop : int | None
        The number of values to read from the pattern. Defaults to max_int.
    """
    if stop == None:
        stop = max_int
    for _ in range(stop):
        yield start
        start += step


def choose(items, weights=[], stop=None):
    """
    A generator that returns its items using weighted random selection.
    By default all items have an equal probability of being returned.

    Parameters
    ----------
    items : list
        The list of values to generate.
    weights : list
        A list of probablity weights for selecting the corresponding items.
        Weights do not have to sum to 1 as the generator automatically 
        converts them to probabilities. If no weights are provided then
        items are chosen with equal probability.
    stop : int | None
        The number of times to read from the pattern before stopping.
        If None then the generator is unbounded. The default is None.

    Returns
    -------
    The next item in the pattern.
    
    Raises
    ------
    * TypeError: if items is not a list.
    * ValueError: if items is an empty list.
    * TypeError: if stop is not an int.
    * TypeError if weights is not a list.
    * ValueError if any weight is not a float or int.
    * IndexError if the number of items and weight are not the same.
    
    Examples
    --------
    ```python
    >>> [choose([1,2,3]) for _ in range(8)]
    [1,2,2,1,3,2,1,1]
    ```
    """
    if stop == None:
        stop = max_int
    if not isinstance(items, list):
        raise TypeError(f'Items value {items} is not a list.')
    end = len(items)
    if end < 1:
        raise ValueError('Items list is an empty.')
    if not isinstance(stop, int):
        raise TypeError(f"Stop value {stop} is not an integer.")
    if not weights:
        # convert proportion to monotonically increasing values to 1.0
        weights = [(i+1)/end for i in range(end)]
    else:
        if not isinstance(weights, list):
            raise TypeError(f'Weights value {weights} is not a list.')
        for w in weights:
            if not isinstance(w, (int, float)):
                raise IndexError("Weight {w} is not an int or float.")
        if end == len(weights):
            # convert weights so they sum to 1.0
            total = sum(weights)
            weights = [w/total for w in weights]
            # convert weights to monotonically increasing values to 1.0
            for i in range(1, end):
                weights[i] += weights[i-1]
        elif end < len(weights):
            raise IndexError('Too many weights provided.')
        else:
            raise IndexError('Too few weights provided.')
    #print('weights=', weights)
    count = 0
    while count < stop:
        val = ran.random() #ran.uniform(0.0,1.0)
        #print("choice=", val)
        for i in range(end):
            if val < weights[i]:
                break
        #print('  index=', i)
        yield items[i]
        count += 1


def drunk(val, width=1, stop=None, filt=None):
    """
    Returns numbers in a "drunken walk" where the next value returned is 
    constrained to lie within the bounds of the previous value plus/minus width.
    If val and width are both integers then integer values are returned
    otherwise floating point values are returned.

    Parameters
    ----------
    val : int | float
        The initial value returned by the walk. Thereafter drunk internally
        updates this value according to width.
    width : int | float
        Constrains the next value returned to be within the bounds of the
        current value plus/minus width.
    filt : None | function
        If specified, filt is a function of one argument that will be 
        called with the current value to produce the value returned.
    """
    if stop == None:
        stop = max_int
    func = ran.randint if isinstance(val, int) and isinstance(width, int) else ran.uniform
    i = 0
    while i < stop:
        yield val 
        val += func(-width, width)
        i += 1


def markov(rules, stop=None, preset=None):
    """
    Returns a generator that yields items in a Markov chain. The chain is expressed
    as a dictionary of rules, each rule associates a tuple of one or more past 
    outcomes with a list of weighted potential outcomes:

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

    Raises
    -------
    * TypeError if rules is not a list.
    * ValueError if rules is an empty list.
    * IndexError if all rule keys are not the same length (markov order).
    * ValueError if a rule's key is empty.
    * ValueError if a rule has no outcomes.
    * IndexError if a rule outcome is a list that is not length 2.
    * ValueError if a rule outcome is a list and the second element is not an int or float.
    * IndexError if preset is not the same length as markov order.
    * ValueError if a past does not match any rule.

    Examples
    --------
    ```python
    >>> markov({'a': ['b', ['c', 3]], 
                'b': ['a'],
                'c': [['a', 5] 'c', [b, 2.5]]})
    ```
    This is a 1st order markov process with three rules:

    1) if the last outcome was 'a' then the next outcome is either 'b' or 'c',
    with 'c' three times as likely as 'b'.
    2) if the last outcome was 'b' then the next outcome is 'a'.
    3) if the last outcome was 'c' then the next outcome is either 'a', 'c' or 'b',
    with 'c' being the least likely and 'a' being the most likely outcome.
    """
    if stop == None:
        stop = max_int
    if not isinstance(rules, dict):
        raise TypeError(f"Rules value {rules} is not a dictionary.")
    end = len(rules)
    if end < 1:
        raise ValueError("Rules list is empty.")
    if not isinstance(stop, int):
        raise TypeError(f"Stop value {stop} is not an integer.")
    if preset and not isinstance(preset, tuple):
        preset = (preset,)
    data = {}
    order = 0  # the order of the markov process is the number of past events
    for key, value in rules.items():
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
    history = preset

    # yield loop
    for _ in range(stop):
        # find the rule that matches current history
        outcomes = data.get(history)
        if not outcomes:
            raise ValueError(f'No rule match for {history}.')
        # find the next outcome
        randnum = ran.random()
        outcome = None
        # find the outcome for the random number
        for out in outcomes:
            if randnum < out[1]:
                outcome = out[0] # next outcome
                break       
        # left-shift history with current choice appended
        history = history[1:] + (outcome,)
        yield outcome


def markov_analyze(seq, order):
    """
    Calculates the markov rules of the given order for the specified list of
    data. The rules can be passed to `markov()` to generate a markov chain
    based on the sequence analyzed.
    
    Parameters
    ----------
    seq : list
        The list of data to analyse.
    order : int
        The markov order of the analysis.

    Returns
    -------
    A dictionary containing the markov analysis of the data.

    Examples
    --------
    ```
    >>> markov_analyze([2, 2, 1, 3, 4, 4, 1, 2], 1)
    {(2,): [[2, 2], [1, 1]], (1,): [[3, 1], [2, 1]], (3,): [[4, 1]], (4,): [[4, 1], [1, 1]]}
    ```
    """
    # each window is a list of one or more past values followed
    # by the subsequent value: (past+, next)
    windows = []
    end = len(seq)
    for i in range(end):
        windows.append(tuple(seq[(i+j) % end] for j in range(order+1)) )
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
    return rules


def states(cells, stop=None, rule=None):
    """
    Returns a generator that produces states from a cellular automata 
    that holds an array of initial states and a rule function that 
    updates the states to their next values. See: `getstates()`.

    Parameters
    ----------
    states : list    
        A list containing the initial states of the cellular automata. A
        flat list of states produces a one dimensional automata and a row
        major list of lists will create a two dimensional automata.

    stop : int | None
        The number of times to read from the pattern before stopping.
        If None then the generator is unbounded. The default is None.
   
    rule : function
        The rule function implements the automata's state transition. The
        function is called automatically and passed two arguments, the 
        states and the index of the current cell in the states. The function
        can use `getstate()` to access one or more neighbor states in order
        to calculate the next state of the current cell.
        for more information.

    Returns
    -------
    The next item in the pattern.
    """
    if stop == None:
        stop = max_int
    if not isinstance(cells, list):
        raise TypeError(f'Cells value {cells} is not a list.')
    if not cells:
        raise ValueError('Cells list is empty.')
    if not isinstance(stop, int):
        raise TypeError(f"Stop value {stop} is not an integer.")
    if not callable(rule):
        raise TypeError(f"Func value {rule} is not a function.")
    if isinstance(cells[0], list):
        # cells is a 2D automata (a list of lists)
        indexes = [(row, col) for row in range(len(cells)) for col in range(len(cells[0]))]
        period = len(indexes)
        # values is a 2D copy of cells with at least 1 row and col
        current = [list(r) for r in cells] # list(r) is copy
        # future same as values but set to 0's
        future = [[0 for _ in r] for r in cells]
    else:
        # cells is a 1D automata but see below.
        indexes = [(0, col) for col in range(len(cells))]
        period = len(indexes)
        # values is a 2D copy of cells with at least 1 row and col
        current = [list(cells)]   # list(cells) is copy
        # future as values but set to 0's
        future = [[0 for _ in cells]] # init future to 0's.
    
    print('current:', current, 'future:', future, 'indexes:', indexes)

    # reverse the states so that when the loop starts and
    # flips with j == 0 the present states will be correct
    current, future = future, current
    i = 0
    while i < stop:
        j = i % period
        if j == 0:
            #print("flipping present and future i=", i)
            current, future = future, current
        pos = indexes[j]
        val = current[pos[0]][pos[1]]
        nxt = rule(current, pos)
        future[pos[0]][pos[1]] = nxt
        i += 1
        yield val

        
def getstate(cells, pos, inc):
    """
    A helper function to call within a cellular automata's rule function to
    access the value of neighbor cells at position pos + inc. See: `states()`.

    The new position pos+inc will automatically wrap mod the size of the cells
    array so will never go out of bounds.

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
    return cells[row][col]

# # Generator function        
# def foo(a,b):
#     c = 1
#     def gen():
#         yield a
#         yield b
#         yield c
#     return gen()
# def pval(func,args):
#     while True:
#         yield func(*args)


def rotation(items, swaprules, stop=None):
    """
    Permutes the elements in items according to one or more "swapping rules".
    See demos/coventry.py for an example of using rotation to create 
    change-ringing patterns.
    
    Parameters
    ----------
    items : list
        The list of items to generate
    swaprules : list | generator
        The value can be on or more swapping rules or a generator that produces
        swapping rules. A swapping rule is a list of (up to) four integers
        that controls the iterative swapping that is applied to all the data
        to produce the next generation of items:
        ```[start, step, width=1, end=len]```
        Start is the location (zero based index) in the pattern's data to begin
        swapping from, step is the rightward increment to move to the next swap
        start, width is the distance between the elements swapped.  End is the
        position in the item list to stop the swapping at, and defaults to the
        length of the item list.
    stop : int | None
        The number of times to read from the pattern before stopping.
        If None then the generator is unbounded. The default is None.
    """
    # convenience: if swaprules is a list then wrap it in a cycle(),
    # otherwise it should already be a generator that returns swaprules.
    source = swaprules
    if isseq(swaprules): # swaprules is a list or tuple
        if all(map(lambda x: isseq(x), swaprules)):   # a list of rules
            source = cycle(swaprules)
        elif all(map(lambda x: isnum(x), swaprules)): # list is one rule
            source = cycle([swaprules])
    if not isgen(source):
        raise ValueError(f"swaprules is not a valid list or generator ({swaprules})")
    items = items[:]  # copy user's list since we change it!
    size = len(items)
    if not stop:
        stop = max_int
    i = 0
    while i < stop:
        j = (i % size)
        if j == 0 and i != 0:   
            # if here we've yielded all items in the current generation
            # so do the rotations to create the next generation.
            rule = next(source)
            rlen = len(rule)
            start = rule[0]
            step = rule[1]
            width = rule[2] if rlen > 2 else 1
            end = rule[3] if rlen > 3 else size 
            # iterate left to right swapping items according to rule 
            for a,b in zip(range(start, end, step), range(start+width, end, step)):
                items[a], items[b] = items[b], items[a]
        yield items[j]
        i += 1


def all_rotations (items, rules, groups=False, repeatfirst=False):
    """
    Helper function used in conjunction with the rotation pattern to return
    a list of all the rotations of items until the first rotation occurs again.
    Warning: this function will run until the original generation returns; 
    rules that do not produce the original generation again will trigger
    an infinite loop. See: `rotation()`.

    Parameters
    ----------
    items : list
        The list of items to rotate.
    rules : rule | list
        A rule, list or generator of rules. See: `rotation()`.
    groups : bool
        If groups is True then each generation is collected in a sublist,
        otherwise the rotated items are returned in one flat list.
    repeatfirst : bool
        If repeatfirst is True then the first generation will also be appended
        to the end of list returned.
    """
    gen = rotation(items, rules)
    siz = len(items)
    data = []
    addr = data.append if groups else data.extend
    init = [next(gen) for _ in range(siz)]
    addr(init)
    while (True):
        more = [next(gen) for _ in range(siz)]
        if init == more:
            break
        addr(more)
    if repeatfirst:
        addr(init)
    return data



if __name__ == '__main__' :
    # LOOP --------------------------------------------------------------------
    def test_cycle():
        pat = cycle([1,2,3,4])
        print("pat=", pat)
        for _ in range(10):
            print("next=", next(pat))
    # PALINDROME --------------------------------------------------------------
    def test_palindrome():
        data = ['A', 'B', 'C', 'D']
        reps = 12
        pat = palindrome(data, wrap='++')
        print("palindrome ++ =", pat)
        for _ in range(reps):
            print("next=", next(pat))

        pat = palindrome(data, wrap='+-')
        print("palindrome +- =", pat)
        for _ in range(reps):
            print("next=", next(pat))

        pat = palindrome(data, wrap='-+')
        print("palindrome -+ =", pat)
        for _ in range(reps):
            print("next=", next(pat))

        pat = palindrome(data, wrap='--')
        print("palindrome -- =", pat)
        for _ in range(reps):
            print("next=", next(pat))
    # choose --------------------------------------------------------------------
    def test_choose():
        data = ['A','B','C','D']
        pat = choose(data)
        print("choose", pat)
        hist = {a: 0 for a in data}
        for _ in range(1000):
            x = next(pat)
            hist[x] += 1
        print("hist=", hist)
        data = ['A','B','C']
        wei = [1,2,1]
        pat = choose(data, wei)
        print("choose", pat)
        hist = {a: 0 for a in data}
        for _ in range(1000):
            x = next(pat)
            hist[x] += 1
        print("hist=", hist)
    # jumble -----------------------------------------------------------------
    def test_jumble():
        pat = jumble(['A', 'B', 'C', 'D'])
        print("pat=", pat)
        for _ in range(10):
            print("next=", next(pat))
    # MARKOV ------------------------------------------------------------------
    def test_markov():
        m=markov({'a': ['b', ['c', 3], 'd'], 
                  'b': ['a'], 
                  'c': [['a', 5], 'd'],
                  'd': ['b']},
                stop=20)
        print(m)
        print([o for o in m])

    def test_markov_analyze():
        seq=['a', 'b','a', 'b','a', 'c', 'b', 'a', 'b', 'b', 'c', 'b', 'c']
        print("markov_analyze()")
        print('seq=', seq)
        print('rules=', markov_analyze(seq, 1))

    # STATES ------------------------------------------------------------------
    def test_states():

        def add_neighbors(cells, index):
            left = getstate(cells, index, -1)
            right = getstate(cells, index, 1)
            return (left + right) % 3

        # example
        foo = states([0,1,0,1,0], rule=add_neighbors)
        for _ in range(25):
            print( [next(foo) for _ in range(5)])
     
        # example
        foo = states([1,0,2,2,0,2,1,2], rule=add_neighbors)
        for _ in range(12):
            print([next(foo) for _ in range(8)])
 
       # example 8 states
        def states8(cells, index):
            left = getstate(cells, index, -1)
            here = getstate(cells, index, 0)
            right = getstate(cells, index, 1)
            return (left & 0b100) + (here & 0b010) + (right & 0b001)

        foo = states([0,1,2,3,4,5,6,7], rule=states8)
        for _ in range(16):
            print([next(foo) for _ in range(8)])

        # example hglass
        hglass_states = [0, 1, 1, 1, 0, 0, 0, 0,   0, 0, 0, 1, 0, 0, 0, 0,   
                        0, 0, 0, 0, 0, 1, 0, 0,   0, 1, 0, 0, 0, 1, 1, 1]

        def hglass (cells, pos):
            here = getstate(cells, pos, (0,0))
            east = getstate(cells, pos, (0,1))
            west = getstate(cells, pos, (0,-1))
            south = getstate(cells, pos, (1,0))
            north = getstate(cells, pos, (-1,0))
            index = (east << 4) | (west << 3) | (south << 2) | (north << 1) | here
            return hglass_states[index]

        hglass_init = [
            [0, 0, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 0, 1, 0, 0],
            [0, 0, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 1, 0, 1, 1, 1],
            [1, 1, 0, 0, 1, 0, 1, 1],
            [1, 1, 1, 0, 0, 1, 1, 1],
            [0, 1, 0, 1, 1, 1, 1, 1],
            [1, 0, 0, 1, 1, 1, 1, 0]]

        foo = states(hglass_init, rule=hglass)
        print(foo)
        for _ in range(4):
            sixtyfour = [next(foo) for _ in range(64)]
            print([sixtyfour[i] for i in range(32)])

    #=========================================================================
    test_markov()
    #test_markov_analyze()

    

     
