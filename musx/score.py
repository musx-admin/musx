###############################################################################
"""
This module implements a scheduling queue for generating musical scores.
The Score runs 'composers' (python generators) that output musical events
to sequences and score files.

Example
-------
```py
seq = Seq()
sco = Score(out=seq)
def bach(sco, num):
    for i in range(num):
        n = Note(time=queue.now, key=60+i)
        sco.add(n)
        yield .125
sco.compose(bach(sco, 10))
```

See the examples directory for many examples of composing!
"""

import types


class Score:
    """
    Runs composers in time sorted order. A composer is a python generator
    that is evaluated by the Score. When a composer executes it
    can add musical events or new composers to the score. To continue
    running a composer yields back a delta time indicating the next time
    point that the composer should compose 
    something. A composer stops running when it stops yielding delta
    times or it yields a negative delta time.
    """

    _queue = []
    """
    A time sorted list of queue entries. A queue entry is a list: 
    [<runtime>, <starttime>, <composer>], where <runtime> is the next time 
    (in seconds) at which <composer> will be called, <starttime> is 
    the time at which <composer> was initially inserted into the scheduer,
    and <composer> is a generator.
    """

    _latest_time = 0
    """The run time of the last queue entry."""


    def __init__(self, out=None):
        self._clean()
        self.out = out


    def _clean(self):
        self._queue = []
        self.running = False
        self._latest_time = self.now = self.elapsed = 0


    def _insert(self, entry):
        """
        Insert entry after all entries <= to it. Optimized
        for the most common case of appending at the end.
        """

        if entry[0] < self._latest_time:
            for i, e in enumerate(self._queue):
                if e[0] > entry[0]:
                    #print("inserting", entry)
                    self._queue.insert(i, entry)
                    return
        #print("insert: appending", entry)
        self._queue.append(entry)
        self._latest_time = entry[0]


    def _insure_entries(self, expr):
        """
        Parses composer expression(s) into a list of one or
        more queue entries. A composer expression can be a 
        composer, a list [*ahead*, *composer*], or a sequence
        of the same: [[*ahead1*, *composer1*], ...]
        """

        def isgen(x): return isinstance(x, types.GeneratorType)
        def isnum(x): return isinstance(x, (int, float))
        def islist(x): return isinstance(x, list)
        def ispair(x):
            if len(x) == 0:
                raise ValueError("empty generator spec.")
            elif isnum(x[0]):
                if x[0] < 0:
                    raise ValueError(f"not a number >= 0: {x}.")
                if len(x) != 2:
                    raise ValueError(f"not a generator spec: {x}.")
                if not isgen(x[1]):
                    raise ValueError(f"not a generator spec: {x}.")
                return True
            return False      
        
        now = self.now
        if not islist(expr):
            if isgen(expr):
                return [[now + 0, now + 0, expr]]
            raise TypeError(f"not a generator: {expr}")
        elif ispair(expr):
            return [[now + expr[0], now + expr[0], expr[1]]]

        # If we reach here, expr is a list that does not start with
        # a number so every item has to be a gen or a list [num gen]
        entries = []
        for e in expr:
            #print("e:", e)
            if not islist(e):
                if isgen(e):
                    entries.append([now + 0, now + 0, e])
                else:
                    raise TypeError(f"not a generator: {e}.")
            elif ispair(e):
                entries.append([now + e[0], now + e[0], e[1]])
            else:
                raise ValueError(f"not a generator list [time, gen]: {e}.")
        return entries


    def _run(self):
        """
        The scheduling loop that processes queued composers until there are
        no more composers to run. To process the current composer in the
        queue the Score performs the following tasks:

        * the current (first) composer is popped off the queue.
        * the queue's self.now and self.elapsed times are updated.
        * the composer generator is called via next().
        * if the next() call yields a positive ahead value back the composer
          is reinserted  back into the queue at time now + ahead, otherwise
          the composer is not reinserted in the queue.
        """

        self.running = True
        while len(self._queue) > 0:
            # Pop earliest entry from the queue and get its composer
            entry = self._queue.pop(0)
            # Set the current score time to the entry's time.
            self.now = entry[0]
            # print(f"before composer, score time is {self.now}")
            # Set the composer's elapsed time since starting
            self.elapsed = self.now - entry[1]
            #print("***elapsed=", self.elapsed)
            composer = entry[2]
            try:
                # Call the entry's composer. if it yields a positive number
                # increment entry's current scoretime and add it back into the _queue.
                delta = next(composer)
                if isinstance(delta, (int, float)): # and delta >= 0:
                    if delta >= 0:
                        # Advance entry's time and insert back into queue
                        entry[0] += delta
                        # print(f"after composer, delta is {delta} and entry time is now {entry[0]}")
                        self._insert(entry)
                else:
                    raise ValueError(f"invalid yield value {delta} from composer {entry[2]}.")
            except StopIteration:
                # print("stopping", composer)
                pass

 
    out = None
    """
    An optional object a composer can add musical events to. The Score
    does not examine the contents this variable.
    """


    running = False
    """True if the Score is running."""


    now = 0
    """
    The time point in the score that the currently executing composer is at.
    """
 

    elapsed = 0
    """
    The amount of time the currently executing composer has been running since
    it was added to the Score.
    """
 

    def compose(self, composer):
        """
        Starts running one or more composer generators. This function can be
        called at the top level and also by composers that are already running.

        Parameters
        ----------
        composer : generator | list
            If composer is a generator it is added to the queue at the current
            time. Otherwise composer can be a list [*ahead*, *composer*]
            or a list of the same [[*ahead*, *composer*], ...]  where
            *ahead* is a future time and *composer* is a composer generator.

        Example
        -------
        ```py
        def simp(q, num, rate, key):
            for _ in range(num):
                print("simp at", q.now, "plays", key)
                yield rate
        q=Score()
        # running one composer
        q.compose(simp(q, 5, 1, 60))
        # running two at times 0 and 5
        q.compose([[0, simp(q, 5, 1, 60)], [5, simp(q, 10, .251, 72)]])
        # a composer that composes composers =:)
        def simp2(q, num)
            for i in range(num):
                print("simp2 at", q.now)
                q.compose([q.now+i*2, simp(num, 5, .25, 60+i)])
            yield 2
        q.compose(simp2(q, num))
        ```
        """

        #print("in compose")
        if self.running:
            # A composer added while running just gets inserted it at
            # the propper time in the queue which is already running.
            for e in self._insure_entries(composer):
                #print("r adding", e)
                self._insert(e)
        else:
            for e in self._insure_entries(composer):
                #print("x adding", e)
                self._insert(e)
            try:
                # This is a loop that processes the queue until it is empty. It
                # is in a try statement because we always want to clean up, even
                # if an error is thrown.
                self._run()
            finally:
                self._clean()
                #print("Done!")

    def add(self, event):
        """
        Adds an event to the score. 
        """
        self.out.add(event)
        # Since the score is a scheduler we can just append the event to the seq.
        #self.out.append(event)


if __name__ == '__main__':
    print('Score Tests...')

    def gen(): yield 0
    def foo(): return 0
    x = []
    q = Score()

    print("\ntesting input:", x)
    try: l = q._insure_entries(x)
    except ValueError as e: print("ERROR:",e)
    except TypeError as e: print("ERROR:", e)
    else: print(l)

    x = gen
    print("\ntesting input:", x)
    try: l = q._insure_entries(x)
    except ValueError as e: print("ERROR:", e)
    except TypeError as e: print("ERROR:", e)
    else: print(l)

    x = gen()
    print("\ntesting input:", x)
    try: l = q._insure_entries(x)
    except ValueError as e: print("ERROR:", e)
    except TypeError as e: print("ERROR:", e)
    else: print(l)

    x = [5, gen()]
    print("\ntesting input:", x)
    try: l = q._insure_entries(x)
    except ValueError as e: print("ERROR:", e)
    except TypeError as e: print("ERROR:", e)
    else: print(l)

    x = [gen(), 5]
    print("\ntesting input:", x)
    try: l = q._insure_entries(x)
    except ValueError as e: print("ERROR:", e)
    except TypeError as e: print("ERROR:", e)
    else: print(l)

    x = [gen()]
    print("\ntesting input:", x)
    try: l = q._insure_entries(x)
    except ValueError as e: print("ERROR:", e)
    except TypeError as e: print("ERROR:", e)
    else: print(l)

    x = [[gen()]]
    print("\ntesting input:", x)
    try: l = q._insure_entries(x)
    except ValueError as e: print("ERROR:", e)
    except TypeError as e: print("ERROR:", e)
    else: print(l)

    x = [gen(), gen(), gen(), [20, gen]]
    print("\ntesting input:", x)
    try: l = q._insure_entries(x)
    except ValueError as e: print("ERROR:", e)
    except TypeError as e: print("ERROR:", e)
    else: print(l)

    x = [gen(), gen(), gen(), [20, gen()]]
    print("\ntesting input:", x)
    try: l = q._insure_entries(x)
    except ValueError as e: print("ERROR:", e)
    except TypeError as e: print("ERROR:", e)
    else: print(l)

    x = [5]
    print("\ntesting input:", x)
    try: l = q._insure_entries(x)
    except ValueError as e: print("ERROR:", e)
    except TypeError as e: print("ERROR:", e)
    else: print(l)

    x = [0, gen(), 45]
    print("\ntesting input:", x)
    try: l = q._insure_entries(x)
    except ValueError as e: print("ERROR:", e)
    except TypeError as e: print("ERROR:", e)
    else: print(l)

    x = [gen(), gen(), [45, gen()]]
    print("\ntesting input:", x)
    try: l = q._insure_entries(x)
    except ValueError as e: print("ERROR:", e)
    except TypeError as e: print("ERROR:", e)
    else: print(l)

    x = [gen(), gen(), [-2, gen()]]
    print("\ntesting input:", x)
    try: l = q._insure_entries(x)
    except ValueError as e: print("ERROR:", e)
    except TypeError as e: print("ERROR:", e)
    else: print(l)

    print('...Done!')


