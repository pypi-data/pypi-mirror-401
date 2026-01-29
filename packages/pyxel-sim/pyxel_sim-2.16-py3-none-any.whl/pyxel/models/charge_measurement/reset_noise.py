#  Copyright (c) European Space Agency, 2020.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.
#
#
"""Reset noise models."""

import astropy.constants as const
import numpy as np
import xarray as xr
from astropy.units import Quantity, Unit

from pyxel.detectors import Detector
from pyxel.util import set_random_seed


def compute_ktc_noise(
    temperature: Quantity[Unit("K")],
    capacitance: Quantity[Unit("F")],
    shape: tuple[int, int],
) -> Quantity[Unit("V")]:
    """Compute KTC noise array. Formula from :cite:p:`Goebel_2018`.

    Parameters
    ----------
    temperature : Quantity
        Temperature. Unit: K
    capacitance : Quantity
        Node capacitance. Unit: F
    shape : tuple
        Shape of the output array.

    Returns
    -------
    Quantity
        2D array.

    Example
    -------
    >>> compute_ktc_noise(
    ...     temperature=Quantity(273, unit="K"),
    ...     capacitance=Quantity(41.0, unit="fF"),
    ...     shape=(2, 2),
    ... )
    <Quantity [[ 0.0004925 , -0.00018549],
           [-0.00016014, -0.00032533]] V>
    """

    rms = np.sqrt(Quantity(const.k_B) * temperature / capacitance).to("V")
    return Quantity(np.random.normal(scale=rms.to_value("V"), size=shape), unit="V")


def ktc_noise(
    detector: Detector,
    node_capacitance: float | None = None,
    seed: int | None = None,
) -> None:
    """Apply KTC reset noise to detector signal array.

    This model adds thermal reset noise based on the
    ``detector.characteristics.temperature``
    and node capacitance.

    The kTC formula can be retrieved here :cite:p:`Goebel_2018`.

    Parameters
    ----------
    detector : Detector
        Pyxel detector object.
    node_capacitance : float, optional
        Node capacitance. Unit: F
        If not provided, it is retrieved from ``detector.characteristics.node_capacitance``.
    seed : int, optional
        Random seed.

    Notes
    -----
    This noise is only applied during the first readout or in destructive readout mode.

    For more information, you can find examples here:

    * :external+pyxel_data:doc:`use_cases/CMOS/cmos`
    * :external+pyxel_data:doc:`use_cases/APD/saphira`
    """
    if node_capacitance is not None:
        if node_capacitance <= 0:
            raise ValueError("Node capacitance should be larger than 0!")

        capacitance: float = node_capacitance
    else:
        try:
            capacitance = detector.characteristics.node_capacitance
        except AttributeError as ex:
            raise AttributeError(
                "Characteristic node_capacitance not available for the detector"
                " used. Please specify node_capacitance in the model argument!"
            ) from ex

    if detector.is_first_readout or not detector.non_destructive_readout:
        # This is the first readout or the destructive mode is enabled
        with set_random_seed(seed):
            noise_2d: Quantity[Unit("V")] = compute_ktc_noise(
                temperature=Quantity(detector.environment.temperature, unit="K"),
                capacitance=Quantity(capacitance, unit="F"),
                shape=detector.geometry.shape,
            )

        # Save the KTC noise computed once for a given exposure
        # Store as a 'Quantity' object (with its unit)
        detector.data["/reset_noise/output_calculation"] = xr.DataArray(
            noise_2d,
            dims=["y", "x"],
            coords={
                "y": range(detector.geometry.row),
                "x": range(detector.geometry.col),
            },
        )

    else:
        noise_2d = Quantity(detector.data["/reset_noise/output_calculation"].data)

    # Add to the signal with the unit
    detector.signal += noise_2d
