"""
Author: Jens Lucht
"""

import torch
from numpy import ndarray, newaxis
from torch import ones, as_tensor

from ..optimize import AlternatingProjections
from .propagation import FresnelTFPropagator, expand_fresnel_numbers
from .constraints import AmplitudeProjector, ConstraintOperator, WaveConstraints


class AP:
    """
    Alternating projections for holographic phase retrieval. See, for example [1].

    Parameters
    ----------
    shape: tuple
        Dimension of the image to reconstruct. For 2D a tuple of length two.
    fresnel_nums: float, array_like
        Fresnel numbers of hologram(s) to reconstruct. Supports astigmatism.
    betadelta: float | None
        Ratio between absorption and phase (complex) refractive index for homogeneous object assumption as float. ``0.0``
        corresponds to pure-phase object (default). If ``None``, no homogeneous object constraint is applied.

        .. Note:: This parameter is ignored if ``constraints`` are passed to the reconstruction call.
    dtype: Datatype
        .. Note:: should currently **not** be used.
    device: torch.Device | None
        Device to perform computations on. ``None`` uses default device, usually the CPU.

    Returns
    -------
    Callable:
        AP reconstructor ``fn``. Reconstruct holograms with ``fn(holograms)``.

    Example
    -------

    We demonstrate the use of the AP implementation on real example data of glass beads, see [1]:

    >>> from hotopy.datasets import beads
    >>> from hotopy.holo import AP
    >>> import torch
    >>> data = beads()
    >>> holos, fnums = data["holograms"], data["fresnelNumbers"]

    Here we perform the actual AP reconstruction:

    >>> ap = AP(holos.shape[-2:], fnums, betadelta=4e-3, device="cuda")
    >>> psi_ap = ap(holos).cpu()   # note: psi is the complex wave

    Finally, we need to convert to the phase and absorption representation:

    >>> phi_ap torch.angle(psi_ap)  # retrieve phase from wave object
    >>> mu_ap = torch.log(abs(psi_ap)  # ... and absorption

    References
    ----------
    .. [1]
        J. Hagemann, M. Töpperwien, T. Salditt; Phase retrieval for near-field X-ray imaging beyond linearisation or
        compact support. Appl. Phys. Lett. 23 July 2018; 113 (4): 041109. :doi:`10.1063/1.5029927`
    """

    algorithm = AlternatingProjections

    def __init__(
        self,
        shape,
        fresnel_nums,
        betadelta=0.0,
        dtype=None,
        device=None,
    ):
        self.dtype = dtype
        self.device = device
        self.ndim = len(shape)
        self.betadelta = betadelta

        fresnel_nums = expand_fresnel_numbers(fresnel_nums, shape=shape)

        self.propagator = FresnelTFPropagator(
            shape,
            fresnel_nums,
            dtype=dtype,
            device=device,
            keep_type=False,
        )

    def __call__(
        self,
        holograms,
        constraints=None,
        x=None,
        max_iter: int = 100,
        keep_type=False,
    ):
        """
        Reconstruct holograms.

        Parameters
        ----------
        holograms :
            Intensities measured at detector.
        constraints :
            Constraints projectors for object/sample.
        max_iter : int, Optional
            Maximal number of iterations.
        """
        holograms_t = type(holograms)
        holograms = as_tensor(holograms, device=self.device)
        shape = holograms.shape[-self.ndim :]

        # if single image is entered expand to stack of one image
        single_image = holograms.ndim == self.ndim
        if single_image:
            holograms = holograms[newaxis]

        projector_holos = AmplitudeProjector(holograms.sqrt())
        projector_object = (
            constraints if constraints is not None else WaveConstraints(betadelta=self.betadelta)
        )

        # ensure correct device placement
        if isinstance(projector_object, ConstraintOperator):
            projector_object.to_device(self.device)

        # initialize with plane wave (ones) or initial guess x if given
        if x is None:
            # start from 1 = exp(0), i.e. all zero object
            x = ones(shape, device=self.device, dtype=torch.complex64)
        else:
            x = as_tensor(x, device=self.device)

        # AP
        ap = self.algorithm(
            self.propagator,
            (projector_object, projector_holos),
            x,
            max_iter=max_iter,
        )

        # iterate util stopping condition is met
        while not ap.done():
            ap.step()

        # recast into numpy if requested
        if keep_type and holograms_t is ndarray:
            out = ap.x.cpu().numpy()
        else:
            out = ap.x

        # remove stack axis if single image
        if single_image:
            out = out[0]

        return out
