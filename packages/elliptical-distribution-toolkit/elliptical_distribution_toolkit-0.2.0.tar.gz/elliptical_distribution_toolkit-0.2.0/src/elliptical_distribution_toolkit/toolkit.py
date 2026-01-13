"""
-------------------------------------------------------------------------------

Implementation of the elliptical-distribution-toolkit package

-------------------------------------------------------------------------------
"""

import numpy as np
import scipy.stats
import scipy.special
import scipy.optimize
from typing import Union


def infer_data_dimension(data: np.ndarray) -> int:
    """Infers the dimension of the data.

    For a J x N panel of data, J ~ # records and N ~ # dimensions. Numpy
    data.ndim returns a memory-based value of the matrix dimension (eg
    np.eye(3) = 2, not 3). Since (J x N) vs (N x J) cannot be enforced at
    the api level, it is assumed that J >= N and `N` is inferred to be the
    smaller of the two shape values from data.

    Parameters
    ----------
    data: np.ndarray
        J x N panel of data: J records (rows), N dimensions (columns)

    Returns
    -------
    int
        Inferred dimension of `data`
    """

    return 1 if data.ndim == 1 else min(data.shape)


# noinspection PyPep8Naming
def covariance_to_correlation(covariance_mtx: np.ndarray) -> tuple:
    """Transforms a covariance matrix into a correlation matrix.

    Parameters
    ----------
    covariance_mtx: np.ndarray
        square, positive-definite matrix

    Returns
    -------
    tuple
        correlation_mtx: np.ndarray
            square, positive-definite correlation matrix
        std_devs: np.ndarray
            standard deviations of the scatter matrix
    """

    # compute normalizing matrix
    std_devs = np.sqrt(np.diag(covariance_mtx))
    S = np.outer(std_devs, std_devs)
    S_inv = 1.0 / S

    # normalize cov to corr
    correlation_mtx = covariance_mtx * S_inv

    # return
    return correlation_mtx, std_devs


def t_distribution_samplecount_loss_factor(df_target: float) -> float:
    """Returns the loss factor as an interpolation from a lookup table.

    Parameters
    ----------
    df_target: float
        Shape parameter for which to return the loss factor

    Returns
    -------
    float
        The associated loss factor
    """

    # precomputed loss values as a function of df
    tabulated_loss_factors = np.array(
        [
            [3, 66],
            [3.25, 34],
            [3.5, 19],
            [3.75, 12],
            [4, 8.7],
            [4.25, 6.3],
            [4.5, 5.1],
            [4.75, 4.2],
            [5, 3.5],
            [5.5, 2.9],
            [6, 2.4],
            [6.5, 2.2],
            [7, 2],
            [7.5, 1.9],
            [8, 1.8],
            [8.5, 1.7],
            [9, 1.6],
            [9.5, 1.5],
            [10, 1.5],
            [11, 1.4],
            [12, 1.4],
            [13, 1.4],
            [14, 1.3],
            [15, 1.3],
            [16, 1.2],
            [17, 1.2],
            [18, 1.2],
            [19, 1.2],
            [20, 1.2],
            [25, 1.1],
            [30, 1.1],
            [40, 1.1],
            [50, 1.1],
            [60, 1.1],
            [70, 1],
            [80, 1],
            [90, 1],
            [100, 1],
        ]
    )

    # return interpolated value
    return np.interp(
        df_target, tabulated_loss_factors[:, 0], tabulated_loss_factors[:, 1]
    )


def minimum_sample_count_for_statistical_variance_bounds(
    variance_deviation_bound: float,
    variance_quantile_bound: float,
    df=None,
) -> int:
    """Returns min sample count to bound variance-of-variance statistics.

    Parameters
    ----------
    variance_deviation_bound: float
        Ratio of sample to theoretical variance (eg 1.05)
    variance_quantile_bound: float
        High-side quantile of variance-of-variance distribution (eg 0.9)
    df: float
        t-dist degrees of freedom df (df=None is Gaussian default)

    Returns
    -------
    int
        Minimum sample count to achieve statistical bounds

    Notes
    -----
    See Distribution of the sample variance at https://en.wikipedia.org/wiki/Variance,
    """

    # Gaussian target function
    def f(n_minus_one: float) -> float:
        return (
            n_minus_one
            / scipy.stats.chi2.ppf(1 - variance_quantile_bound, df=n_minus_one)
            - variance_deviation_bound
        )

    # try to solve for the Gaussian model
    n_lower_bound = 10
    n_upper_bound = 1e5
    try:
        n_minus_one_est = scipy.optimize.brentq(f, n_lower_bound, n_upper_bound)
        sample_count = np.round(n_minus_one_est).astype(int) + 1
    except RuntimeError:
        sample_count = np.nan

    # adjust for df-dependent loss factor assoc'd with the t distribution
    if (~np.isnan(sample_count)) and df is not None:
        loss_factor = t_distribution_samplecount_loss_factor(df)
        sample_count = np.round(loss_factor * sample_count).astype(int)

    # return
    return sample_count


def z_score(data: np.ndarray, loc: float, disp: float) -> np.ndarray:
    """Computes the z-score of `data` wrt (loc, disp).

    Parameters
    ----------
    data: np.ndarray
        1D array of data
    loc: float
        location parameter
    disp: float
        dispersion parameter

    Returns
    -------
    np.ndarray
        Signed Euclidian distance of the data
    """

    data_centered = data - loc
    return data_centered / disp


# noinspection SpellCheckingInspection,PyPep8Naming
def point_weights_tdist_parametric(
    data: np.ndarray,
    df: float,
    loc: Union[float, np.ndarray],
    scatter: Union[float, np.ndarray],
) -> np.ndarray:
    """Computes the weights of `data` under the t-distribution.

    Parameters
    ----------
    data: np.ndarray
        J x N panel of data: J records (rows), N dimensions (columns)
    df: float
        shape parameter (degrees of freedom)  [use np.inf for Gaussian case]
    loc: Union[float, np.ndarray]
        location parameter, scalar or 1 x N array
    scatter: Union[float, np.ndarray]
        square of the dispersion parameter, scalar or N x N pos. def. matrix

    Returns
    -------
    np.ndarray
        Weights associated with `data` points

    References
    ----------
    Meucci, ch 4, Risk and Asset Allocation, Springer, 2007
    """

    # branch on distribution
    if np.isinf(df):
        # normal case
        n_records = max(data.shape)
        weights = np.ones(n_records)

    else:
        # t-dist case
        Ma2 = mahal_explicit(data, loc, scatter)
        n_dim = infer_data_dimension(data)
        weights = (df + n_dim) / (df + Ma2)

    return weights


# noinspection PyPep8Naming
def mahal_explicit(
    data: np.ndarray,
    loc: Union[float, np.ndarray],
    scatter: Union[float, np.ndarray],
) -> np.ndarray:
    """Computes Ma2 of data given elliptical parameters.

    This function is called precise because `loc` and `scatter` are not
    estimated, but instead they are inputs.

    For data ~ (J x N) records and columns, returns

        Ma2 = diag(
            (data' - loc')' inv(scatter) (data' - loc')
        )

    by computing the alternative O(J)-complexity expression

        Ma2 = (U ** 2) x ones(N x 1)

    where, given S = L L',

        U = (L \ (data - loc)')' .

    For data ~ 1d, the z-score^2 is returned.

    Parameters
    ----------
    data: np.ndarray
        J x N panel of data: J records (rows), N dimensions (columns)
    loc: np.ndarray
        N-long 1D vector of data-ellipse location
    scatter: np.ndarray
        N x N scatter matrix

    Returns
    -------
    np.ndarray
        Mahalanobis squared distances associated with data points

    References
    ----------
    Meucci, ch 4, Risk and Asset Allocation, Springer, 2007
    """

    # branch on ndim
    if data.ndim == 1:
        return z_score(data, loc, np.sqrt(scatter)) ** 2

    # center the data
    data_centered = data - loc

    # scale the centered data by L from the Cholesky factorization of `scatter`
    l_scatter = np.linalg.cholesky(scatter)
    isotropic_pts = np.linalg.solve(l_scatter, data_centered.T).T

    # return squared Euclidian distances of the centered, isotropic pts
    return np.sum(isotropic_pts**2, axis=1)


# noinspection PyPep8Naming
def mahal_estimated(data: np.ndarray, weights: np.ndarray) -> np.ndarray:
    """Computes an estimate of Ma2 given data and weights.

    Location and scatter parameters are estimated from `data` using the
    `weights` that are input to this call.

    The mahal distance is invariant to scalar scaling of `data`:

        data -> scale data  -->  Ma2 -> Ma2.

    The distance scales inversely with a scalar scaling of `w`:

        w -> scale w  -->  Ma2 -> Ma2 / scale.

    Parameters
    ----------
    data: np.ndarray
        J x N panel of data: J records (rows), N dimensions (columns)
    weights: np.ndarray
        J-length vector of weights

    Returns
    -------
    np.ndarray
        Mahalanobis squared distances associated with data points
    """

    # location estimate
    loc_hat = weights.T.dot(data) / np.sum(weights)

    # compute QR and construct V from centered data
    n_records = max(data.shape)
    data_centered = data - loc_hat
    data_weighted_centered = np.sqrt(weights)[:, np.newaxis] * data_centered
    r_tilde = np.linalg.qr(data_weighted_centered, mode="r") / np.sqrt(
        n_records - 1
    )

    # compute isotropic points
    isotropic_pts = np.linalg.solve(r_tilde.T, data_centered.T).T

    # return squared Euclidian distances
    return np.sum(isotropic_pts**2, axis=1)


# noinspection SpellCheckingInspection,PyPep8Naming
def uv_studentt_centered_fit(data: np.ndarray, nu_max: float = 265) -> tuple:
    """Fits St(nu, 0, disp) to data, caps nu to `nu_max`.

    The cumulative Student-t distribution is indistinguishable from a Gaussian
    cumulative to within 1% of the relative abscissa value at a p = 0.999 level.
    """

    nu, loc, disp = scipy.stats.t.fit(data, floc=0)

    return min(nu, nu_max), disp


# noinspection SpellCheckingInspection,PyPep8Naming
def mv_studentt_elliptical_fit(
    data: np.ndarray, df: float, tol: float = 1e-6
) -> tuple:
    """Robust estimation of location and scatter given data and df value.

    Solves (4.81-4.82) of A Meucci pg 191 1st Ed. These are the implicit MLE
    expressions for loc_hat and scatter_hat under a t-distribution given a
    J x N data panel and a value of `df`, the degrees of freedom for the
    multivariate distribution.

    Once calibrated, the data takes the distribution of

        data ~ St(df, loc-hat, scatter-hat).

    And in addition, the point weights associated w/ the data are returned.

    Parameters
    ----------
    data: np.ndarray
        J x N panel of data: J records (rows), N dimensions (columns)
    df: float
        Degrees of freedom of the mv Student-t distribution
    tol: float
        Relative convergence tolerance (default = 1e-6)

    Returns
    -------
    tuple
        loc_hat: np.ndarray
            location-parameter estimate
        scatter_hat: np.ndarray
            scatter-matrix estimate
        weights: np.ndarray
            weights associated with data records
        n_iter: int
            iteration count for convergence

    References
    ----------
    Meucci, ch 4, Risk and Asset Allocation, Springer, 2007
    """

    # initialized weight vectors
    n_records = max(data.shape)
    n_dim = infer_data_dimension(data)
    w_old = np.ones(n_records)
    w_new = w_old - 0.99

    # iteration over implicit equations until relative convergence in weight
    n_iter = 0
    while np.linalg.norm((w_new - w_old) / w_new) / n_records > tol:
        # compute Ma2
        Ma2 = mahal_estimated(data, w_new)

        # revise weights
        w_old = w_new
        w_new = (df + n_dim) / (df + Ma2)

        # inc iter count
        n_iter += 1

    # compute loc-hat and scatter-hat
    loc_hat = w_new.T.dot(data) / np.sum(w_new)
    wc = np.sqrt(w_new)[:, np.newaxis] * (data - loc_hat)
    scatter_hat = wc.T.dot(wc) / (n_records - 1)

    # return estimates
    return loc_hat, scatter_hat, w_new, n_iter


# noinspection SpellCheckingInspection
def studentt_to_gaussian_conversion(
    stt_data: np.ndarray, nu: float, disp: float
) -> np.ndarray:
    """Converts St(nu, 0, disp^2) `data` to N(0, 1).

    The conversion goes as erf^-1( cdf_(nu, disp)( data ) ).
    """

    uniform_data = scipy.stats.t.cdf(stt_data, df=nu, scale=disp)
    gaussian_data = scipy.stats.norm.ppf(uniform_data, loc=0, scale=1)

    return gaussian_data
