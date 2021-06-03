################################################################################
"""
rhythm.py provides a mapping between alternate representations of rhythmic 
values: fractions, rhythmic symbols, lists of the same or strings of the same.

A fraction  is a ratio (or Fraction) of a whole note, e.g. 
1/4=quarter note, 1/8=eighth note, 3/2= dotted whole note (three half-notes),
7/25=seven 25ths notes, and so on. 
    
A rhythmic symbol consists of a metric letter: 'w'=whole,'h'=half, 'q'=quarter,
'e'=eighth, 's'=sixteenth, 't'=thirty-second, 'x'=sixty-fourth, optionally 
preceded by a tuple number (e.g. '3e') and followed by zero or more dots
e.g. (3q...).  Dotted values larger than the 64th are support.
Examples: 'q'=quarter, '3q'=triplet quarter, 'e.'=dotted-eighth,
'3s.'=triplet dotted sixteenth, 'h...'=triple dotted half.
    
Simple expressions involving rhythmic symbols can be formed using +, -, and
* to join rhythmic tokens. Examples: 'w*4'=duration of four whole notes,
's+3q'=sixteenth plus triplet quarter, 'w-s.'=whole less a dotted sixteenth.
"""

from fractions import Fraction
from .tools import parse_string_sequence

def rhythm(ref, tempo=60, beat=1/4):
    """
    Returns the value of ref converted to beat units (typically seconds) at a
    specified tempo. Ref can be a fraction of a whole note, a rhythmic symbol,
    a list of the same or a string of the same separated by commas and/or spaces.

    Parameters
    ----------
    ref : string | int | float | Fraction
        A fraction of a whole note, a rhythmic symbol, list of the same
        or string containing separeted by spaces and/or commas.
    tempo : int | float
        The metronome marking (beats per minute).
    beat : int | float
        The beat of the tempo. Defaults to 1/4, or quarter note.
    """
    if type(ref) is str:
        ref = ref.strip() # remove whitespace from start and end
        try:     
            return (_rhythms[ref] / beat) * (60/tempo)
        except:  
            pass
        # split string if it contains commas or spaces.
        #ref = ref.replace(',', ' ').split()
        ref = parse_string_sequence(ref)
        # if it didnt split then its a single expression,
        # otherwise its a series (list) of expressions.
        if len(ref) == 1: 
            expr = _rexpr(ref[0])
        else:
            expr = [_rexpr(e) for e in ref]
        #print("expr -> ", expr)
        return _reval(expr, beat, tempo)
    elif type(ref) is list:
        return [rhythm(r, tempo, beat) for r in ref]
    elif type(ref) is Fraction:
        return (ref / Fraction(beat)) * Fraction(60, tempo)
    else:
        return (ref / beat) * (60/tempo)


def _rexpr(expr, lev=0):
    """Convert rhythmic expression into prefix notation for evaluation."""
    ops = ['+', '-', '*']
    if lev < len(ops):
        expr = expr.split(ops[lev])
        for i, e in enumerate(expr):
            expr[i] = _rexpr(e, lev+1)
        if len(expr)>1:
            # convert to prefix notation: 'q+q+q' => ['+', 'q', 'q', 'q']
            expr = [ops[lev]] + expr
        else:
            expr = expr[0]
    return expr


def _reval(expr, beat, tempo):
    """Evaluate an already parsed rhythmic expression."""
    if type(expr) is str:
        return (_rhythms[expr] / beat) * (60/tempo)
    # expr is ['q','q'] or prefixed eval list ['+' ....]
    if expr[0] == '+':
        x = 0.0
        for e in expr[1:]: x += _reval(e, beat,tempo)
        return x
    elif expr[0] == '*':
        if len(expr) == 3 and expr[2].isdigit():
            return _reval(expr[1], beat,tempo)
    elif expr[0] == '-':
        x = _reval(expr[1], beat, tempo)
        for e in expr[2:]: x -= _reval(e, beat, tempo)
        return x
    else:
        return [_reval(e, beat, tempo) for e in expr]
    expr = expr[0].join(expr[1:])
    raise ValueError(f"not a rhythmic expression: {expr}.")
        

def intempo(time, tempo):
    """
    Returns a time value scaled to tempo.

    Parameters
    ----------
    time : int | float
        The value to scale to tempo.
    tempo : int | float
        The metronome marking (beats per minute).

    Returns
    -------
    The time value scaled to the tempo.
    """
    return time * (60.0 / tempo)


def _createrhythms():
    """Create a hash table of all rhythmic values."""
    #toks = [(s, Fraction(1, 2**n)) for n,s in enumerate('whqestx')]
    tab = {}
    # Iterate the rhythmic letters (w=whole, h=half ... x=sixty-fourth)
    for i,t in enumerate('whqestx'):
        sym = t
        # the rhythmic value of each type w=1/1, h=1/2 ...
        rat = Fraction(1, 2**i)
        # create the dotted, but dont go smaller than 1/64.
        # NB: when d is 0 there is no dot.
        for d in range(0,7-i):
            #print(sym+('.'*d), rat * (2 - Fraction(1, 2**d)))
            #_rhythms[sym+('.'*d)] = rat * (2 - Fraction(1, 2**d))
            tab[sym+('.'*d)] = rat * (2 - Fraction(1, 2**d))
            for pre in [3]:
                amt = Fraction(pre-1,pre)
                tab[str(pre)+sym+('.'*d)] = (amt * rat * (2 - Fraction(1, 2**d)))
    return tab


_rhythms = _createrhythms()


if __name__ == '__main__':
    pass
