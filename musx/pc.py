###############################################################################
"""
Implements operations on pitch classes, pitch class sets, and twelve-tone
matrices.  A pitch class (pc) is an integer 0-11 representing one of twelve
equal steps in the chromatic octave from C=0 to B=11. A pitch class set is
a tuple containing pitch classes. A twelve-tone matrix is a 2D array of
pitch class sets, where each set contains all twelve pitch classes.
"""

__pdoc__ = {'most_tightly_packed': False
}


def pcset(keynums):
    """
    Converts a list or tuple of key numbers or pitch classes into a
    pitch class set (tuple).

    Parameters
    ----------
    keynums : list | tuple
        A list or tuple of keynums 0-127 or pitch classes 0-11.
    
    Returns
    -------
    A tuple containing the set of pitch classes.
    """   
    return tuple(dict.fromkeys(k % 12 for k in keynums))


def pcinterval(pc1, pc2):
    """Returns the number of ascending semitones from pc1 upto pc2."""
    return (pc2-pc1) % 12 if pc2 >= pc1 else (pc2+12) - pc1


def pccomplement(pc):
    """Returns the interval complement of pc."""
    return pcinterval(pc, 12)


def pctranspose(pcs, steps):
    """Transposes the pitch class set by a pitch class interval 0-11."""
    dist = steps % 12
    return tuple((p + dist) % 12 for p in pcs)


def pcinvert(pcs, t=0):
    """Inverts a pitch class set at the specified transposition level."""
    t0 = [pcinterval(x, 12) for x in pcs[::-1]]
    return tuple(t0) if t == 0 else pctranspose(t0, t)


def most_tightly_packed(normal_forms):
    """
    Returns the normal form that is most tightly packed to the left.
    See: Understanding Post-Tonal Theory, page 75.
    """

    # Convert normal_forms to start on 0 so they become intervals
    # above the lowest pc. (The first and last interval will be the
    # same so we could drop them.)
    intervals = [pctranspose(n, pcinterval(n[0], 12)) for n in normal_forms]
    # Flop the interval vectors to group intervals of the same index together:
    #   0 1 2  0 1 2      0    1    2
    # [[1 2 2][1 4 1] => [[1 1][2 4][2 1]]
    flopped = [[*c] for c in zip(*intervals)]  # [*c] converts tuple into list...
    # Reverse the flop because we process the intervals top-to-bottom
    flopped.reverse()
    # Debugging:
    # print("intervals=", intervals, "flopped=", flopped)
    try:
        # Find the first (left-most) flop whose intervals differ from each other.
        # If no intervals differ a StopIteration exception is thrown by next().
        left = next(filter(lambda x: len(set(x)) > 1, flopped))
        # Index of the smallest number in list is the index of the
        # most tightly packed normal form
        return normal_forms[left.index(min(left))]
    except StopIteration:
        # All intervals are the same. The tie breaker is to return
        # the normal form with the lowest starting pitch class
        first_pitches = [n[0] for n in normal_forms]
        index_of_winner = first_pitches.index(min(first_pitches))
        return normal_forms[index_of_winner]


def normalform(pcs):
    """
    Returns the normal form of a pitch class set. The normal
    form is the set rotation with the smallest outside interval
    and with the intervals most tightly packed to the left.
    See: Understanding Post-Tonal Theory, page 75.

    Parameters
    ----------
    pcs : tuple
        A tuple of pitch classes.
    """
    # insure that pcs are in low-to-high order so they ascend within one octave
    if not all(a<b for a,b in zip(pcs, pcs[1:])):
        #print('normalform is sorting')
        pcs = tuple(sorted(pcs))
    #assert all(a<b for a,b in zip(pcs, pcs[1:])), f'pitch class set {pcs} is not sorted low to high.'
    # List ascending order pc set with an "octave" pc on top.
    octave = [*pcs] + [pcs[0]]
    # Determine the intervals between pcs
    #deltas = pc_deltas(octave)
    deltas = [pcinterval(x, y) for x, y in zip(octave, octave[1:])]
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
        return normal_forms[0]
    # To determine the "best normal form" out of multiple forms, choose
    # the set whose intervals are most tightly packed "to the left".
    return most_tightly_packed(normal_forms)


def primeform(pcs):
    """
    Returns the most tightly packed version of pcs or its inversion
    transposed to 0.
    """
    # get normal form and
    norm = normalform(pcs)
    # transpose by the complement so set starts on 0
    zero = pctranspose(norm, pcinterval(norm[0], 12))
    # invert with transposition of last pc so inversion starts on zero
    invr = pcinvert(zero, zero[-1])
    return most_tightly_packed([zero, invr])


def pcivector(pcs):
    """Returns the interval vector of a pitch class set."""
    def iclass(i): return i if i < 7 else 12 - i
    prime = primeform(pcs)
    icvec = [0, 0, 0, 0, 0, 0]
    for i1 in range(0, len(prime) - 1):
        for i2 in range(i1 + 1, len(prime)):
            ic = iclass(pcinterval(prime[i1], prime[i2]))
            icvec[ic - 1] += 1
    return icvec


def pcmatrix(pcrow):
    """Returns pitch class matrix containing all forms of the pitch class row."""
    # get the interval complement of the first note in the row.
    t0 = pccomplement(pcrow[0])
    # transpose pcrow by the complement so it now starts on 0.
    p0 = [(p + t0) % 12 for p in pcrow]
    # invert (complement) p0 to make i0.
    i0 = [pccomplement(p) for p in p0]
    # transpose the p0 row by each inverted pc to form the P by I matrix.
    return tuple(pctranspose(p0, i) for i in i0)


def pcmatrixrow(matrix, form, trans):
    """
    Returns the row for the specified form and transposition level.
    
    Parameters
    ----------
    matrix : tuple
        A pitch class matrix created by pcmatrix().
    form : 'p' | 'r' | 'i' | 'ri'
        The row form to return: 'p' is prime, 'r' is retrogade, 'i' is inversion, and 'ri' is retrograde-inversion.
    trans : pc
        The pitch class transposition level of the row to return.

    Returns
    -------
    A tuple containing the pitch classes for the given form and transposition.
    """
    size = len(matrix)
    assert 0 <= trans < size, "Not a valid transposition level: {}.".format(trans)
    row = col = 0
    if form in ['p', 'r']:
        while row < size:
            if matrix[row][col] == trans:
                break
            row += 1
        assert row < size, "Not a valid row transposition: {}.".format(row)
        return matrix[row] if form == 'p' else matrix[row][::-1]
    elif form in ['i', 'ri']:
        while col < size:
            if matrix[row][col] == trans:
                break
            col += 1
        assert col < size, "Not a valid row transposition: {}.".format(col)
        rng = range(0, size) if form == 'i' else reversed(range(0, size))
        return tuple(matrix[r][col] for r in rng)
    else:
        raise Exception("Not a valid row form: {}".format(form))


def ppmatrix(matrix, notes=False):
    """
    Pretty prints the given pitch class matrix.

    Parameters
    ----------
    matrix : tuple
        The pitch class matrix to print.
    notes : bool
        If true then note names are printed, otherwise pitch classes are printed.
    """

    print('(')
    if notes == False:
        nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'E']
        for r in matrix:
            print('  ', tuple(nums[pc] for pc in r))
    else:
        notes = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
        for r in matrix:
            print('  ', tuple(notes[pc] for pc in r))
    print(')')


def pctest(knums):
    pcs = pcset(knums)
    normal = normalform(pcs)
    prime = primeform(pcs)
    vector = pcivector(prime)
    print("normal=", normal, "prime=", prime, "vector", vector)


if __name__ == '__main__':
    from musx import keynum
    names = {0:'C', 1:'C#', 2:'D', 3:'Eb', 4:'E', 5:'F', 6:'F#', 7:'G', 8:'Ab', 9:'A', 10:'Bb', 11:'B'}
    def pitchclassname(pc):
        return names[pc]
    def pitchclassnames(pcs):
        return [pitchclassname(n) for n in pcs]
    #==========================================================================
    
    def testnormal(notes, correct):
        keys = keynum(notes)
        result = normalform(pcset(keys )) #, sort=True
        print(f'{notes}: => {result} => {pitchclassnames(result)}')
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
        keys = keynum(notes)
        pcs = pcset(keys)
        result = pctranspose(pcs, t)
        print(f'{notes}: => T{t} => {result} => {pitchclassnames(result)}')
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
        keys = keynum(notes)
        pcs = pcset(keys)
        result = pcinvert(pcs, t)
        print(f'{notes}: => T{t}I => {result} => {pitchclassnames(result)}')
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
        keys = keynum(notes)
        normal = normalform(pcset(keys )) #, sort=True
        result = primeform(normal)
        print(f'{notes}: normal => {normal} prime => {result} => {pitchclassnames(result)}')
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

    def matrix(notes):
        keys = keynum(notes)
        pcs = pcset(keys)
        mat = pcmatrix(pcs)
        ppmatrix(mat)
        return mat

    print('\n=== Matrix ========================================')

    berg = matrix('g3 bf d4 fs a c5 e af b cs6 ds f')
    print(f'p7:  {pcmatrixrow(berg, "p", 7)}')
    print(f'r7:  {pcmatrixrow(berg, "r", 7)}')
    print(f'i7:  {pcmatrixrow(berg, "i", 7)}')
    print(f'ri7: {pcmatrixrow(berg, "ri", 7)}')

    tiny = matrix('a4 c5 d')

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

