import numpy as np
from scipy.sparse.linalg import svds

__all__ = [
    "pca_decompose_arpack",
    "pca_decompose_flats",
    "pca_synthesize_flat",
]


def squash_dims(a, naxes=2):
    """
    Squashed (merges) last `naxes` dims together into flat. Inverse operation is `reshape(original_shape)`.
    """
    dims = a.shape[-naxes:]
    size = np.prod(dims)
    new_shape = a.shape[:-naxes] + (size,)
    return a.reshape(new_shape)


def pca_decompose_arpack(A, k):
    """
    Partial PCA decomposition for data x in shape ``(m, n)`` m samples of n random variables.

    Compute the largest or smallest k singular values and corresponding singular vectors of a sparse matrix A. k needs
    to be strictly smaller than ``min(m, n)``.

    .. Note:: The order in which the singular values are returned is not guaranteed.
    """
    m, n = A.shape
    if not m <= n:
        raise ValueError

    # center data
    A_mean = A.mean(0)
    A_centered = A - A_mean

    u, s, vh = svds(A_centered, k=k)  # arpack is default solver

    return s, vh, A_mean


def pca_decompose_flats(flats, n_components):
    """
    PCA decomposition of flats field.

    Parameters
    ----------
    flats: array
        Flats of dataset in shape ``(n_flats, pixel_y, pixel_x)``.
    n_components: int
        Number of components to compute. Needs to be strictly less than ``min(flats.shape)``.

    Returns
    -------
    C: array
        PCA components matrix in shape ``(n_components, pixel_y*pixel_x)``.
    mv: array
        Mean value of flats stack along stack axis as flat array.
    sv: array
        singular values (largest to smallest).

    Example
    -------
    We assume a stack of (dark-substracted) flats are stored in the array ``flats`` with shape ``(N, ny, nx)``.
    The projection with sample to correct is ``proj`` with shape ``(ny, nx)``.
    Furthermore, we assume 5 components are sufficient to fit the varations of the beam, check with singular values.

    >>> N_components = 5
    >>> from hotopy.holo import pca_decompose_flats, pca_synthesize_flat
    >>> C, mv, sv = pca_decompose_flats(flats, N_components)

    Generate a syntetic flat-field for the given (dark-substracted) raw projection image ``proj``:

    >>> flat_pca = pca_synthesize_flat(C, mv, proj)
    >>> holo_pca = proj / flat_pca

    Compare to classical static mean flat field:

    >>> holo_mean = proj / flats.mean(0)


    See Also
    --------
    pca_synthesize_flat
    flatfield_inpainting_correction

    """
    # merge last two axis (all pixels of the images) into long vector of all pixels
    flats_vec = squash_dims(np.asarray(flats), naxes=2)

    singular_values, components, mean = pca_decompose_arpack(flats_vec, n_components)

    # reserve order of components and singular values to be from largest to smaller singular values
    return components[::-1], mean, singular_values[::-1]


def pca_synthesize_flat(components, mean, proj):
    """
    Synthesizes flat field for given (dark subtracted) projection proj using the PCA analysis given in components and
    mean.

    Parameters
    ----------
    components: array
        Output from PCA analysis. Also input from scikit-learn PCA is possible, e.g. use the ``pca_fit.C_`` as input.
    mean: array
        Mean flat image
    proj:
        Projection to compute flat field for.

    Returns
    -------
    flat_pca: array
        Synthesized flat-field from PCA components matrix `C` and given projection `proj` in normal image shape.

    Example
    -------
    See example in :func:`pca_decompose_flats`.

    See Also
    --------
    pca_decompose_flats
    flatfield_inpainting_correction

    """

    proj_vec = squash_dims(proj)

    C = components
    Ct = C.transpose((-1, -2))
    w = (proj_vec - mean) @ Ct
    flat_vec = (w @ C) + mean

    return flat_vec.reshape(proj.shape)
