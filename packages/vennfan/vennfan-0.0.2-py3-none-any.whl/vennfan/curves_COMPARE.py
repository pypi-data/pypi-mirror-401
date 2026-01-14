import numpy as np
from scipy.optimize import fminbound
from typing import Optional

# ---------------------------------------------------------------------------
# Curve helpers
# ---------------------------------------------------------------------------

def get_sine_curve(
    X,
    i: float,
    N: int,
    p: float = 0.33,
    decay: str = "linear",  # "linear" or "exponential"
    epsilon: Optional[float] = None,
    delta: Optional[float] = None,
    b: float = 0.8,
    corrected: bool = False,
):
    """
    Compute a nonlinear, sine-based boundary curve for a given class index.

    The returned curve is based on a π-shifted sine:
        base(X) = sin(2**i * X - π)
    and then transformed as:
        curve(X) = amp(i) * sign(base) * |base|**p

    where the amplitude ``amp(i)`` depends on ``decay``:

    - ``decay="linear"``:
        * If ``N <= 2``: a simple linear ramp is used.
        * If ``N > 2``: amplitude is interpolated linearly from
          ``1 - epsilon`` at ``i=0`` to ``delta`` at ``i=N-2``.
          If ``epsilon``/``delta`` are not provided, they default to ``1/N``.
    - ``decay="exponential"``:
        amp(i) = b ** (i + epsilon)

    Special cases
    -------------
    - If ``i == N - 1``, returns zeros with the same shape as ``X``.
    - If ``corrected`` is True and ``i < 1``, positive-sign regions are clipped to 1:
        returns ``curve`` where ``sign(base) < 0``, else 1.

    Parameters
    ----------
    X : array_like
        Input angles (radians). Will be converted to a float NumPy array.
    i : float
        Class index (typically integer-valued). Controls frequency via ``2**i``.
    N : int
        Number of classes/levels. Used to determine amplitude schedules and the
        terminal case ``i == N - 1``.
    p : float, default=0.33
        Exponent applied to ``|sin|``. Must be positive for typical use.
    decay : {"linear", "exponential"}, default="linear"
        Amplitude schedule type.
    epsilon : float, optional
        For ``decay="linear"`` (when ``N > 2``): start offset controlling ``amp(0)=1-epsilon``.
        For ``decay="exponential"``: exponent offset in ``b**(i+epsilon)``.
    delta : float, optional
        For ``decay="linear"`` (when ``N > 2``): end value controlling the amplitude at ``i=N-2``.
        Ignored for ``decay="exponential"``.
    b : float, default=0.8
        Base for exponential decay. Only used when ``decay="exponential"``.
    corrected : bool, default=False
        If True, apply clipping behavior for small ``i`` as described above.

    Returns
    -------
    numpy.ndarray
        Array of the same shape as ``X`` containing the boundary curve values.

    Raises
    ------
    ValueError
        If ``decay`` is not one of {"linear", "exponential"}.
    """
    X = np.asarray(X, float)

    if i == N - 1:
        return np.zeros_like(X)

    base = np.sin(2**i * X - np.pi)
    if decay == "linear":
        if N <= 2:
            amp = (N-1-i) / N
        else:
            if epsilon is None:
                epsilon = 1 / N
            if delta is None:
                delta = 1 / N
            amp = 1 - epsilon + i*(delta+epsilon-1) / (N-2)
    elif decay == "exponential":
        amp = b ** (i+epsilon)
    else:
        raise ValueError("decay must be 'linear' or 'exponential'")

    sgn = np.sign(base)
    curve = amp * sgn * np.abs(base) ** p
    if i < 1 and corrected:
        return np.where(sgn < 0, curve, 1)
    return curve

def get_cosine_curve(
    X,
    i: float,
    N: int,
    p: float = 0.33,
    decay: str = "linear",  # "linear" or "exponential"
    epsilon: Optional[float] = None,
    delta: Optional[float] = None,
    b: float = 0.8,
    corrected: bool = False,
):
    """
    Compute a nonlinear, cosine-based boundary curve for a given class index.

    The returned curve is based on a cosine with frequency scaling:
        base(X) = cos((2**i)/2 * (X + 2π))
    and then transformed as:
        curve(X) = amp(i) * sign(base) * |base|**p

    where the amplitude ``amp(i)`` depends on ``decay`` (same conventions as
    :func:`get_sine_curve`):

    - ``decay="linear"``:
        * If ``N <= 2``: a simple linear ramp is used.
        * If ``N > 2``: amplitude is interpolated linearly from
          ``1 - epsilon`` at ``i=0`` to ``delta`` at ``i=N-2``.
          If ``epsilon``/``delta`` are not provided, they default to ``1/N``.
    - ``decay="exponential"``:
        amp(i) = b ** (i + epsilon)

    Special cases
    -------------
    - If ``i == N - 1``, returns zeros with the same shape as ``X``.
    - If ``corrected`` is True and ``i < 2``, positive-sign regions are clipped to 1:
        returns ``curve`` where ``sign(base) < 0``, else 1.

    Parameters
    ----------
    X : array_like
        Input angles (radians). Will be converted to a float NumPy array.
    i : float
        Class index (typically integer-valued). Controls frequency via ``2**i``.
    N : int
        Number of classes/levels. Used to determine amplitude schedules and the
        terminal case ``i == N - 1``.
    p : float, default=0.33
        Exponent applied to ``|cos|``. Must be positive for typical use.
    decay : {"linear", "exponential"}, default="linear"
        Amplitude schedule type.
    epsilon : float, optional
        For ``decay="linear"`` (when ``N > 2``): start offset controlling ``amp(0)=1-epsilon``.
        For ``decay="exponential"``: exponent offset in ``b**(i+epsilon)``.
    delta : float, optional
        For ``decay="linear"`` (when ``N > 2``): end value controlling the amplitude at ``i=N-2``.
        Ignored for ``decay="exponential"``.
    b : float, default=0.8
        Base for exponential decay. Only used when ``decay="exponential"``.
    corrected : bool, default=False
        If True, apply clipping behavior for small ``i`` as described above.

    Returns
    -------
    numpy.ndarray
        Array of the same shape as ``X`` containing the boundary curve values.

    Raises
    ------
    ValueError
        If ``decay`` is not one of {"linear", "exponential"}.
    """
    X = np.asarray(X, float)

    if i == N - 1:
        return np.zeros_like(X)

    base = np.cos(2**i / 2 * (X + 2*np.pi))
    if decay == "linear":
        if N <= 2:
            amp = (N-1-i) / N
        else:
            if epsilon is None:
                epsilon = 1 / N
            if delta is None:
                delta = 1 / N
            amp = 1 - epsilon + i*(delta+epsilon-1) / (N-2)
    elif decay == "exponential":
        amp = b ** (i+epsilon)
    else:
        raise ValueError("decay must be 'linear' or 'exponential'")

    sgn = np.sign(base)
    curve = amp * sgn * np.abs(base) ** p
    if i < 2 and corrected:
        return np.where(sgn < 0, curve, 1)
    return curve

def vennfan_find_extrema(
    curve_mode: str,
    p: float,
    decay: str = "linear",  # "linear" or "exponential"
    epsilon: Optional[float] = None,
    delta: Optional[float] = None,
    b: float = 0.8,
    N: int = 6,
) -> tuple[float, float, float, float]:
    """
    Numerically estimate extrema of the disc-mapped boundary curves for a "vennfan" layout.

    This function searches over X in [0, 2π] and uses 1D bounded optimization to estimate:
        (x_min, x_max, y_min, y_max)
    for the *projected* coordinates produced by mapping a boundary curve y_old(X) onto
    the unit disc via:
        rho(X) = 1 - y_old(X)
        u(X)   = rho(X) * cos(X)
        v(X)   = rho(X) * sin(X)

    The boundary curve y_old(X) is computed using either :func:`get_sine_curve`
    or :func:`get_cosine_curve` depending on ``curve_mode`` and the provided
    amplitude schedule parameters.

    Heuristics used (to reduce the number of optimizations)
    -------------------------------------------------------
    - If ``curve_mode == "sine"``:
        * x_max, x_min, y_max are estimated using i=0
        * y_min is estimated using i=1
    - If ``curve_mode == "cosine"``:
        * x_max, y_max are estimated using i=0
        * x_min is estimated over i in {0, 1}
        * y_min is estimated over i in {1, 2}

    Parameters
    ----------
    curve_mode : {"sine", "cosine"}
        Which base curve family to use for y_old(X).
    p : float
        Exponent applied to |sin| or |cos| inside the boundary curve. Must be > 0.
    decay : {"linear", "exponential"}, default="linear"
        Amplitude schedule passed through to the underlying curve function.
    epsilon : float, optional
        Passed through to the underlying curve function. See :func:`get_sine_curve`
        and :func:`get_cosine_curve` for interpretation under each decay mode.
    delta : float, optional
        Passed through to the underlying curve function for linear decay (N > 2).
    b : float, default=0.8
        Exponential decay base passed through to the underlying curve function.
    N : int, default=6
        Number of classes/levels used by the underlying curve function.

    Returns
    -------
    (x_min, x_max, y_min, y_max) : tuple[float, float, float, float]
        Extrema of the projected coordinates u(X) and v(X) over the searched ranges.

    Raises
    ------
    ValueError
        If ``p <= 0`` or if ``curve_mode`` is not in {"sine", "cosine"}.

    Notes
    -----
    The function uses numerical optimization (scipy.optimize.fminbound) over fixed
    sub-intervals of [0, 2π]. The returned values are therefore approximations that
    depend on the chosen intervals and heuristics.
    """
    if p <= 0:
        raise ValueError("p must be > 0.")
    if curve_mode not in ("sine", "cosine"):
        raise ValueError("curve_mode must be 'sine' or 'cosine'.")

    # Pick curve function
    curve_fn = get_sine_curve if curve_mode == "sine" else get_cosine_curve

    # Projected coordinates u(X), v(X) for a given i
    def _u_of_X(X: float, i: int) -> float:
        y_old = float(curve_fn(X, i, N, p=p, decay=decay, epsilon=epsilon, delta=delta, b=b))
        rho = 1.0 - y_old
        return rho * np.cos(X)

    def _v_of_X(X: float, i: int) -> float:
        y_old = float(curve_fn(X, i, N, p=p, decay=decay, epsilon=epsilon, delta=delta, b=b))
        rho = 1.0 - y_old
        return rho * np.sin(X)

    if curve_mode == "sine":
        # x_max from i=0  (maximize u)
        i_xmax = 0
        a, b = 0.0, np.pi
        x_at = fminbound(lambda X: -_u_of_X(X, i_xmax), a, b)
        x_max = _u_of_X(x_at, i_xmax)

        # x_min from i=0  (minimize u)
        i_xmin = 0
        a, b = 0.0, np.pi
        x_at = fminbound(lambda X: _u_of_X(X, i_xmin), a, b)
        x_min = _u_of_X(x_at, i_xmin)

        # y_max from i=0  (maximize v)
        i_ymax = 0
        a, b = 0.0, np.pi
        x_at = fminbound(lambda X: -_v_of_X(X, i_ymax), a, b)
        y_max = _v_of_X(x_at, i_ymax)

        # y_min from i=1  (minimize v)
        i_ymin = 1
        a, b = np.pi, np.pi*3/2
        x_at = fminbound(lambda X: _v_of_X(X, i_ymin), a, b)
        y_min = _v_of_X(x_at, i_ymin)

    else:  # curve_mode == "cosine"
        # x_max from i=0  (maximize u)
        i_xmax = 0
        a, b = 0.0, np.pi
        x_at = fminbound(lambda X: -_u_of_X(X, i_xmax), a, b)
        x_max = _u_of_X(x_at, i_xmax)

        # y_max from i=0  (maximize v)
        i_ymax = 0
        a, b = 0.0, np.pi
        x_at = fminbound(lambda X: -_v_of_X(X, i_ymax), a, b)
        y_max = _v_of_X(x_at, i_ymax)

        # x_min from i=1  (minimize u)
        x_min = 0
        for i_xmin in [0,1]:
            a, b = np.pi/2, np.pi*3/2
            x_at = fminbound(lambda X: _u_of_X(X, i_xmin), a, b)
            x_min = min(_u_of_X(x_at, i_xmin), x_min)

        # y_min from i=2  (minimize v)
        y_min = 0
        for i_ymin in [1,2]:
            a, b = np.pi*5/4, np.pi*7/4
            x_at = fminbound(lambda X: _v_of_X(X, i_ymin), a, b)
            y_min = min(_v_of_X(x_at, i_ymin), y_min)

    return float(x_min), float(x_max), float(y_min), float(y_max)
