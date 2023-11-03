###############################################################################
"""
Implements operations on pitch classes, pitch class sets, and set matrices.
A pitch class (pc) is an integer 0-11 representing one of twelve
equal steps in the chromatic octave from C=0 to B=11. A pitch class set is
a tuple containing pitch classes. A matrix is a 2D array of pitch class sets,
that can be referenced by row type, e.g. 'p3', 'i9', 'ri2' 'r11'.
"""

# __pdoc__ = {
#     '_most_tightly_packed': False,
#     '_MatrixBase': False,
#     '_PCSetBase': False
# }

import copy
from collections import namedtuple
from collections.abc import Iterable
from musx import Pitch, keynum

_PCSetBase = namedtuple('_PCSetBase', ['set'])
_MatrixBase = namedtuple('_MatrixBase', ['matrix'])

class PCSet(_PCSetBase):

    _pcnames = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "T", "E"]
    
    def __new__(cls, pcs):
        if isinstance(pcs, Iterable):
            if isinstance(pcs[0], int):
                pcs = [i % 12 for i in pcs]
            elif isinstance(pcs[0], Pitch):
                pcs = [p.pc() for p in pcs]
            return super().__new__(cls, tuple(dict.fromkeys(pcs)))
        raise Exception(f"{pcs} is not an iterable of ints or Pitches.")
    
    def label(self):
        """
        Concatenates a string label from the set's pcs omitting spaces 
        and printing 10 and 11 as T and E.
        """
        label = ""
        for i in self.set: label += self._pcnames[i]
        return label

    def __str__(self):
        """
        Returns a str() string that displays the pc's in the set.
        """
        return f'<PCSet: {self.label()}>'

    def __repr__(self):
        """Returns a repr() string that if evaluated will recreate the PCSet()."""
        return f'PCSet({self.set})'
    
    @staticmethod
    def _steps(pc1, pc2):
        """Returns the number of ascending semitones from pc1 upto pc2."""
        return (pc2-pc1) % 12 if pc2 >= pc1 else (pc2+12) - pc1

    @staticmethod
    def _complement(pc):
        """Returns the interval complement of pc."""
        return PCSet._steps(pc, 12)

    def transpose(self, steps):
        """Transposes the set by a pitch class interval 0-11."""
        dist = steps % 12
        return PCSet([(p + dist) % 12 for p in self.set])
    
    def invert(self, t=0):
        """Inverts the pitch class set at the specified transposition level 't'."""
        t0 = PCSet( [PCSet._steps(x, 12) for x in self.set[::-1]] )
        return t0 if t == 0 else t0.transpose(t)

    def normalform(self):
        """
        Returns the normal form of a pitch class set. The normal
        form is the set rotation with the smallest outside interval
        and with the intervals most tightly packed to the left.
        """
        #print("in normalform()")
        pcs = self.set
        # insure that pcs are in low-to-high order so they ascend within one octave
        if not all(a<b for a,b in zip(pcs, pcs[1:])):
            #print('normalform is sorting')
            pcs = tuple(sorted(pcs))
        #assert all(a<b for a,b in zip(pcs, pcs[1:])), f'pitch class set {pcs} is not sorted low to high.'
        # List ascending order pc set with an "octave" pc on top.
        octave = [*pcs] + [pcs[0]]
        # Determine the intervals between pcs
        #deltas = pc_deltas(octave)
        deltas = [PCSet._steps(x, y) for x, y in zip(octave, octave[1:])]
        # Determine the largest interval
        largest = max(deltas)
        # Determine the index(es) of the largest interval in the octave.
        # index + 1 will then be the starting note for the normal order.
        indexes = [i + 1 for i, v in enumerate(deltas) if v == largest]
        # Collect rotations of pcs starting on each index, these
        # are the normal forms. There is often just one but there can
        # be multiple normal orders.
        normal_forms = [pcs[pos:] + pcs[:pos] for pos in indexes]

        # Debugging:
        # print("octave=", octave, "deltas=", deltas, "largest=", largest, "indexes=", indexes,
        #       "normal_forms=", normal_forms)

        # If there is only one normal form, return it.
        if len(normal_forms) == 1: 
            return PCSet(normal_forms[0])
        # To determine the "best normal form" out of multiple forms, choose
        # the set whose intervals are most tightly packed "to the left".
        return PCSet(self._most_tightly_packed(normal_forms))
    
    def _most_tightly_packed(self, normal_forms):
        """
        Returns the normal form that is most tightly packed to the left.
        Note: normal_forms is a list of tuples (NOT PCSets...)
        """
        #print("in _most_tightly_packed()")
        NORMALS = [copy.copy(x) for x in normal_forms]
        # Convert normal_forms to start on 0 so they become intervals
        # above the lowest pc. (The first and last interval will be the
        # same so we could drop them.)

        def pctranspose(pcs, steps):
            """Transposes the pitch class set by a pitch class interval 0-11."""
            dist = steps % 12
            return tuple((p + dist) % 12 for p in pcs)

        intervals = [pctranspose(n, PCSet._steps(n[0], 12)) for n in normal_forms]
        #intervals = [self.transpose(n, PCSet._steps(n[0], 12)) for n in normal_forms]
        INTERVALS = [copy.copy(x) for x in intervals]
        # Flop the interval vectors to group intervals of the same index together:
        #   0 1 2  0 1 2      0    1    2
        # [[1 2 2][1 4 1] => [[1 1][2 4][2 1]]
        flopped = [[*c] for c in zip(*intervals)]  # [*c] converts tuple into list...
        # Reverse the flop because we process the intervals top-to-bottom
        FLOPPED = [copy.copy(x) for x in flopped]
        flopped.reverse()
        REVERSED = [copy.copy(x) for x in flopped]
        # Debugging:
        #print("MTP: normals=", NORMALS, "intervals=", INTERVALS, "flopped=", FLOPPED, "revflopped=", REVERSED)
        try:
            # Find the first (left-most) flop whose intervals differ from each other.
            # If no intervals differ a StopIteration exception is thrown by next().
            left = next(filter(lambda x: len(set(x)) > 1, flopped))
            # Index of the smallest number in list is the index of the
            # most tightly packed normal form
    #        print("most_tightly_packed: normals=", NORMALS, "intervals=", INTERVALS, "flopped=", FLOPPED, "reversed=", REVERSED, "WINNER=", normal_forms[left.index(min(left))])
            return normal_forms[left.index(min(left))]
        except StopIteration:
            # All intervals are the same. The tie breaker is to return
            # the normal form with the lowest starting pitch class
            first_pitches = [n[0] for n in normal_forms]
            index_of_winner = first_pitches.index(min(first_pitches))
    #        print("most_tightly_packed: normals=", NORMALS, "intervals=", INTERVALS, "flopped=", FLOPPED, "reversed=", REVERSED, "TIE BREAKER=", normal_forms[index_of_winner])
            return normal_forms[index_of_winner]

    def primeform(self):
        """
        Returns the most tightly packed version of the set or its inversion,
        whichever is smaller, transposed to 0.
        """
        # get normal form 
        norm = self.normalform()
        # transpose by the complement so set starts on 0
        zero = norm.transpose(PCSet._steps(norm.set[0], 12))
        # invert with transposition of last pc so inversion starts on zero
        invr = zero.invert(zero.set[-1])
        #print("norm=", norm, ", zero=", zero, ", invert=", invr)
        return PCSet(self._most_tightly_packed([zero.set, invr.set]))

    def intervalvector(self):
        """Returns the set's interval vector as a list of six values."""
        pcs = self.set
        def iclass(i): return i if i < 7 else 12 - i
        prime = self.primeform().set
        icvec = [0, 0, 0, 0, 0, 0]
        for i1 in range(0, len(prime) - 1):
            for i2 in range(i1 + 1, len(prime)):
                intr = self._steps(prime[i1], prime[i2])
                ic = iclass(intr)
                #print(f"prime[{i1}]={prime[i1]}, prime[{i2}]={prime[i2]}, intr={intr}, iclass={ic}")            
                icvec[ic - 1] += 1
        return icvec

    def matrix(self):
        """
        Constructs a P by I matrix from the set. Matrix content can be accessed
        using rowform names such as 'p0', 'r11', 'i9', 'ri7', etc.
        """
        return Matrix(self.set)


class Matrix (_MatrixBase):
    # dictionary holding all possible row form labels: "p0" ... "ri11"
    # A label like "I8" is split into two values "i" 8
    _rowforms = {s+str(i) : (s, i) for s in ["p","i","r","ri"] for i in range(12) }

    def __new__(cls, sourceset):
        """
        Returns a zero-based PbyI matrix for the given pc set, which must be a tuple 
        containing valid pcs (0-11) and no repeated values.
        """
        if Matrix._checkset(sourceset):
            # create the matrix
            # get the interval complement of the first note in the row.
            t0 = PCSet._complement(sourceset[0])
            # transpose pcrow by the complement so it now starts on 0.
            p0 = [(p + t0) % 12 for p in sourceset]
            # invert (complement) p0 to make i0.
            i0 = [PCSet._complement(p) for p in p0]
            # transpose the p0 row by each inverted pc to form the P by I matrix.
            rows = tuple( tuple([(p + i) % 12 for p in p0]) for i in i0 )
            #print("***ROWS:", rows)
            return super().__new__(cls, rows)
        raise Exception(f"{sourceset} is not a valid pitch class set (tuple).")

    def row(self, rowform):
        """
        Returns a PCSet from the matrix given its rowform label.
        
        Parameters
        ----------
        rowform : string
            A string concatentation of a row type (p, i, r, ri) and a
            transposition level (0 ... 11). Examples: 'p9' 'ri0' 'i6' 'r11'.   
        """
        try:
            # splits a rowform label like "I5" into a tuple of two values: ("i", 5)
            form,trans = self._rowforms[rowform.lower()]
        except:
            print(f'"{rowform}" is not a valid rowform. Valid examples: "p9" "ri0" "i6" "r11".')
        size = len(self.matrix)
        assert 0 <= trans < size, "Not a valid transposition level: {}.".format(trans)
        row = col = 0
        if form in ['p', 'r']:
            while row < size:
                if self.matrix[row][col] == trans:
                    break
                row += 1
            assert row < size, "Not a valid row transposition: {}.".format(row)
            return PCSet(self.matrix[row] if form == 'p' else tuple(self.matrix[row][::-1]))
        elif form in ['i', 'ri']:
            while col < size:
                if self.matrix[row][col] == trans:
                    break
                col += 1
            assert col < size, "Not a valid row transposition: {}.".format(col)
            rng = range(0, size) if form == 'i' else reversed(range(0, size))
            return PCSet( tuple(self.matrix[r][col] for r in rng) )
        else:
            raise Exception("Not a valid row form: {}".format(form))

    def print(self, notes=False):
        """
        Pretty prints the pc matrix.

        Parameters
        ----------
        notes : bool
            If true then note names are printed, otherwise pitch classes are printed.
        """
        print('(')
        if notes == False:
            nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'E']
            for r in self.matrix:
                print('  ', tuple(nums[pc] for pc in r))
        else:
            notes = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
            for r in self.matrix:
                print('  ', tuple(notes[pc] for pc in r))
        print(')')

    @staticmethod
    def _checkset(set):
        """returns True if set values are valid otherwise False."""
        # set must be a tuple
        if not isinstance(set, tuple):
            return False
        # set must contain only integers 0-11 without duplicate values.
        for i,pc in enumerate(set):
            if not (isinstance(pc, int) and 0 <= pc and pc < 12
                    and pc not in set[i+1:]):
                return False
        return set

    def __str__(self):
        """Returns the P0 set as the print representation for the matrix."""
        return f'<Matrix: {PCSet(self.matrix[0]).label()}>'

    __repr__ = __str__

#
## Module Testing
#

if __name__ == '__main__':
    from musx import keynum
    names = {0:'C', 1:'C#', 2:'D', 3:'Eb', 4:'E', 5:'F', 6:'F#', 7:'G', 8:'Ab', 9:'A', 10:'Bb', 11:'B'}
    def pitchclassname(pc):
        return names[pc]
    def pitchclassnames(pcs):
        return [pitchclassname(n) for n in pcs]
    def testnormal(notes, correct):
        correct = PCSet(correct)
        keys = keynum(notes)
        result = PCSet(keys).normalform() #, sort=True
        #print("*** result:", result)
        print(f'{notes}: => {result} => {pitchclassnames(result.set)}')
        assert result == correct, f'{result} does not match authority {correct}.'
        
    print('\n=== Normal Order ========================================')
    testnormal('f4 bf g5', (5, 7, 10))
    testnormal('ds4 cs5 g', (1, 3, 7))
    testnormal('af3 f4 a5', (5, 8, 9))
    testnormal('as2 b a3', (9, 10, 11))
    testnormal('c4 af e5', (0, 4, 8))
    testnormal('d4 b fs5', (11, 2, 6))
    testnormal('e2 b fs3', (4, 6, 11))
    testnormal('fs4 c5 gs', (6, 8, 0))
    testnormal('a2 e3 g', (4, 7, 9))
    testnormal('f2 d3 b', (11, 2, 5))

    #==========================================================================

    def testtranspose(notes, t, correct):
        correct = PCSet(correct)
        keys = keynum(notes)
        pcs = PCSet(keys)
        result = pcs.transpose(t)
        print(f'{notes}: => T{t} => {result} => {pitchclassnames(result.set)}')
        assert result == correct, f'{result} does not match authority {correct}.'
        
    print('\n=== Transposition ========================================')
    testtranspose('g4 a bf', 3, (10, 0, 1))
    testtranspose('b4 ds5 e', 2, (1, 5, 6))
    testtranspose('g4 gs a', 4, (11, 0, 1))
    testtranspose('f4 af a', 1, (6, 9, 10))
    testtranspose('a4 b ds5', 5, (2, 4, 8))
    testtranspose('c4 e f', 9, (9, 1, 2))
    testtranspose('e4 gs b', 10, (2, 6, 9))
    testtranspose('e4 f bf', 6, (10, 11, 4))
    
    #==========================================================================

    def testinversion(notes, t, correct):
        correct = PCSet(correct)        
        keys = keynum(notes)
        pcs = PCSet(keys)
        result = pcs.invert(t)
        print(f'{notes}: pcs={pcs}, T{t}I={result}') #=> {pitchclassnames(result)}
        assert result == correct, f'{result} does not match authority {correct}.'

    print('\n=== Inversion ========================================')
    testinversion('g4 bf c5', 0, (0, 2, 5))
    testinversion('f4 gs a', 0, (3, 4, 7))
    testinversion('g4 af a', 0, (3, 4, 5))
    testinversion('e4 fs b', 0, (1, 6, 8))
    testinversion('a4 d5 ds5', 0, (9, 10, 3))
    testinversion('a4 cs5 ds5', 0, (9, 11, 3))
    testinversion('c4 d f', 5, (0, 3, 5))
    testinversion('f#4 b c5', 3, (3, 4, 9))
    testinversion('f4 af c5', 9, (9, 1, 4))
    testinversion('g#4 b d5', 10, (8, 11, 2))
    testinversion('e4 f5 g5', 6, (11, 1, 2))

    #==========================================================================

    def testprimeform(notes, correct):
        correct = PCSet(correct) 
        keys = keynum(notes)
        normal = PCSet(keys).normalform() #, sort=True
        result = normal.primeform()
        print(f'{notes}: normal => {normal} prime => {result} => {pitchclassnames(result.set)}')
        assert result == correct, f'{result} does not match authority {correct}.'

    print('\n=== Prime Form ========================================')
    testprimeform('g3 b1 d5', (0, 3, 7))
    testprimeform('a6 c4 ef', (0, 3, 6))
    testprimeform('fs3 b c#4', (0, 2, 7))
    testprimeform('F4 Ab Bb7', (0, 2, 5))
    testprimeform('df4 f3 a6', (0, 4, 8))
    testprimeform('ef7 ff4 gf3', (0, 1, 3) )
    testprimeform('g4 a3 cs5', (0, 2, 6))
    testprimeform('af2 cs3 d1', (0, 1, 6))
    testprimeform('cs4 e5 fs3', (0, 2, 5))
    testprimeform('cs5 g4 a2', (0, 2, 6))
    testprimeform('bf3 a4 f5', (0, 1, 5))
    testprimeform('gs3 cs2 e6', (0, 3, 7))
    testprimeform('f3 fs e2', (0, 1, 2))
    testprimeform('g4 d4 a', (0, 2, 7))

    #==========================================================================

    def testintervalvector(pcs, correct):
        pcs = PCSet(pcs)
        #print("*** pcs:", pcs)
        correct = correct
        #print("*** correct:", correct)
        prime  = pcs.primeform()
        #print("*** prime:", prime)
        result = prime.intervalvector()
        print(f'{pcs}: primeform={prime}, icvector={result}')
        assert result == correct, f'{result} does not match authority {correct}.'

    print('\n=== Interval Vector ========================================')
    testintervalvector([2,3,7,10], [1,0,1,2,2,0])
    testintervalvector([2,3,8,9],  [2,0,0,0,2,2])
    testintervalvector([1,4,8], [0,0,1,1,1,0])
    testintervalvector([1,3,4,7], [1,1,2,1,0,1])
    testintervalvector([0,2,4,6,9], [0,3,2,2,2,1])
    testintervalvector([0,1,3,5,7,8], [2,3,2,3,4,1])
    testintervalvector([9,10,11,0,1], [4,3,2,1,0,0])
    testintervalvector([6,7,9,11,0], [2,2,2,1,2,1])
    testintervalvector([4,5,6,7,8], [4,3,2,1,0,0])
    testintervalvector([0,2,4,6,8], [0,4,0,4,0,2])
    testintervalvector([11,1,2,4,6], [1,3,2,1,3,0])
    testintervalvector([4,5,7,8,10], [2,2,3,1,1,1])
    testintervalvector([9,11,1,2,5], [1,2,2,3,1,1])

    #==========================================================================

    print('\n=== Matrix ========================================')
    # def testmatrix(pcset, correct):
    #     matrix = pcset.matrix()
    #     print("pcset:", pcset, ", matrix:", matrix)
    #     matrix.print()
    #     matrix.print(True)
    #     print(f'p7 equal:  {matrix.row("p7") == correct.row("p7")}
    #     print(f'r equal7:  {matrix.row("r7")}')
    #     print(f'i7:  {matrix.row("i7")}')
    #     print(f'ri7: {matrix.row("ri7")}')

    berg = PCSet([pc % 12 for pc in keynum('g3 bf d4 fs a c5 e af b cs6 ds f')])
    # correct = ( (0,3,7,11,2,5,9,1,4,6,8,10),
    #             (9,0,4,8,11,2,6,10,1,3,5,7),
    #             (5,8,0,4,7,10,2,6,9,11,1,3),
    #             (1,4,8,0,3,6,10,2,5,7,9,11),
    #             (10,1,5,9,0,3,7,11,2,4,6,8),
    #             (7,10,2,6,9,0,4,8,11,1,3,5),
    #             (3,6,10,2,5,8,0,4,7,9,11,1),
    #             (11,2,6,10,1,4,8,0,3,5,7,9),
    #             (8,11,3,7,10,1,5,9,0,2,4,6),
    #             (6,9,1,5,8,11,3,7,10,0,2,4),
    #             (4,7,11,3,6,9,1,5,8,10,0,2),
    #             (2,5,9,1,4,7,11,3,6,9,10,0))

    set = PCSet([pc % 12 for pc in keynum('a4 c5 d')])
    tiny = set.matrix()
    print(tiny.matrix)
    tiny.print()
    tiny.print(True)
"""
    #==========================================================================

    def pctest(notes):
        knums = keynum(notes)
        pcs = pcset(knums)
        normal = normalform(pcs)
        prime = primeform(pcs)
        vector = pcivector(prime)
        print(f'{notes}: pcset => {pcs} normal => {normal} prime => {prime} vector => {vector}')

    print('\n=== Other Tests ========================================')

    pctest('c4 cs fs')
    pctest('a4 bf ef')
    pctest('b3 cs4 d')
    pctest('bf3 ef4 df')

"""
