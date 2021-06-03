###############################################################################
"""
Implements Env, a class for line (xy) envelopes and routines that operate
on them.
"""

__pdoc__ = {
    'Env.__new__': True
}

    
from .tools import rescale


class Env (tuple):
    """
    A subclass of tuple that represents line envelopes containing a series
    of x and y values: x1, y1, x2, y2, ..., xn, yn.
    """
    def __new__(self, xypairs):
        """
        Returns a new Env.

        Parameters
        ----------
        xypairs : list or tuple
            A list or tuple containing x y pairs x1, y1, x2, y2, ..., xn, yn
            where the x and y are ints or float and x values are
            in monotonically increasing order.
        """
        if not isinstance(xypairs, (list, tuple)):
            raise TypeError(f"not a list or tuple: {xypairs}.")
        if len(xypairs) < 2:
            raise ValueError(f"not a valid envelope list: {xypairs}.")
        if not len(xypairs) % 2 == 0:
            raise ValueError("Env(): odd number of envelope values {xy}")
        xx = None
        for x, y in zip(xypairs[0::2], xypairs[1::2]):
            if not isinstance(x, (int, float)):
                raise TypeError(f"Env(): x value {x} is not an int or float.")
            if not isinstance(y, (int, float)):
                raise TypeError(f"Env(): y value {y} is not an int or float.")
            if xx is None:
                xx = x
            elif x < xx:
                raise TypeError(f"Env(): x values {xx} and {x} not in increasing order.")
            xx = x
        return tuple.__new__(Env, xypairs)

    def pairs(self):
        """
        Returns an iterator producing the pairs of x,y values
        in the envelope.
        """
        return zip(self[0::2], self[1::2])

    def unzip(self):
        """
        Returns the envelope's x and y values as two separate lists.
        """
        return self[0::2], self[1::2]
        
    def interp(self, x, mode='lin'):
        """
        Returns the interpolated y value of x in the envelope. 
        
        Parameters
        ----------
        x : int | float
            The x value to interpolate in the envelope. If x
            is not in bounds then the first or last y value is returned.
        mode : string
            Specifies the type of interpolation performed; 'lin' is linear,
            'cos' is cosine, 'exp' is exponential and '-exp' is inverted
            exponential.
        
        Returns
        -------
        The interpolated value of x.
        """
        # iterate segments of the line function as pairs of points to 
        # find the segment that contains the x value. xr and yr are the
        # right side coords, and xl and yl are the left side coords.
        walk = self.pairs()
        xr,yr = next(walk)
        xl,yl = xr,yr
        for wx,wy in walk:
            # stop if right side xr is greater than x since lx < x < rx
            if xr > x:
                break
            xl,yl = xr,yr
            xr,yr = wx,wy
        return rescale(x, xl, xr, yl, yr, mode)

    @staticmethod
    def _interp(x, xys, mode):
        xr,yr = xys[0:2]
        xl,yl = xr,yr
        # iterate remaining pairs of x y values stepping by 2
        for wx,wy in zip(xys[2::2], xys[3::2]):
            if xr > x:
                break
            xl,yl = xr,yr
            xr,yr = wx,wy
        # print(x, xl, xr, yl, yr, mode)
        return rescale(x, xl, xr, yl, yr, mode)

    # def between(self, x, other, mode):
    #     """
    #     Returns a randomly selected y value between the y values of this and
    #     the other envelope.

    #     Parameters
    #     ----------
    #     x : int | float
    #         The x value to interpolate in both envelopes.
    #     other : Env
    #         The other envelope.
    #     mode : string
    #         The interpolation mode. See `interp()`.
        
    #     Returns
    #     -------
    #         A randomly interpolated value
    #     """
    #     pass

    def max(self, coord='y'):
        """
        Returns the largest value for coord, which defaults to 'y'.
        """
        pass

    def min(self, coord='y'):
        """
        Returns the smallest value for coord, which defaults to 'y'.
        """
        pass

    def inverted(self):
        """
        Returns a version of the envelope inverted along the y axis.
        """
        pass

    def reversed(self):
        """
        Returns a version of the envelope reversed along the x axis.
        """
        pass

    def normalized(self, axis='xy'):
        """
        Returns a version of the envelope normalized to lie between 0 and 1.

        If axis is 'xy' then both are normalized, otherwise specify 'x' or 'y'.

        Parameters
        ----------
        axis : 'xy' | 'x' | 'y'
            The axis to normalize.
        """
        pass

    def segments(self, num, mode='lin'):
        """
        Returns a list of y points defining num segments of the envelope
        The first and last y values always included in the list.
        """
        x0, x1 = self[0], self[-2]
        y0, y1 = self[1], self[-1]
        incr = (x1 - x0) / num 
        segs = []
        segs.append(y0)
        for n in range(1, num):
            segs.append(self.interp(incr * n, mode))
        segs.append(y1)
        return segs


def interp(x, *xys, mode='lin', mul=None, add=None):
    """
    A function that interpolates a y value for a given x in a
    series of x,y coordinate pairs. If x is not within bounds
    then the first or last y value is returned.

    Parameters
    ----------
    x : int | float
        The x value to interpolate in the sequence of x y values. 
    xys : series of int or float | list
        Either a series of in-line x, y values representing the envelope
        or a single list of x y coordinate pairs.
    mode : 'lin' | 'cos' | 'exp' | '-exp'
        A string that specifies the type of interpolation performed;
        'lin' is linear, 'cos' is cosine, 'exp' is exponential and 
        '-exp' is inverted exponential. The default is 'lin'. Note
        that if specified the value must provided as an explicit
        keyword arg, e.g. mode='cos'.
    mul : None | number
        A value to multiply the result by.
    add : None | number
        A value to add to the result after any multiplication.
    Returns
    -------
    The interpolated value of x.
    """
    if len(xys) == 1 and isinstance(xys[0], (tuple,list)):
        xys = xys[0]
    if not xys or len(xys) & 1:
        raise ValueError(f"coordinates not x y pairs: {xys}.")
    val = Env._interp(x, xys, mode)
    if mul:
        val *= mul
    if add:
        val += add
    return val

#def interp(x, *xys, **mode):
#    if isinstance(xys[0], (list, tuple)):
#        xys = xys[0] 
#    if len(xys) & 1:
#        raise ValueError(f"coordinates not in x y format: {coords}.")
#    mode = mode['mode'] if mode else 'lin'
#    return Env._interp(x, xys, mode)

if __name__ == '__main__':
    env = Env([0, 0, 100, 1])
    print(env.segments(1, 'lin'))

    # print("Testing env")
    # env = Env([0, 0 , 50, 1, 100, 0])
    # print(env)
    # print(env.pairs())
    # for x,y in env.pairs():
    #     print("x=", x,"y=", y)
    # print(env.interp(49))

    import matplotlib.pyplot as plt
    data = [0,0,1,1]  #[0, 0, 0.2, 0.5, 0.5, 0.3, 1, 1]
    data = [0,34, 1,13, 2,18, 3,12, 4,38, 5,0, 6,25, 7,7]
    env = Env(data)
    l1 = [env.interp(x) for x in frange(0,7,.25)]
    l2 = [interp(x, *data) for x in frange(0,7,.25)]
    assert l1 == l2

    # px, py = env.unzip()
    # print("lists:" , px,py)
    # px, py = [],[]
    # for x in frange(0,7,.1):
    #     px.append(x)
    #     py.append(env.interp(x, '-exp'))
    px, py = [x for x in range(50)], env.segments(50-1, 'cos')
    print('len px=', len(px), "len py=", len(py))
    # plt.plot(px, py)
    # plt.show()
