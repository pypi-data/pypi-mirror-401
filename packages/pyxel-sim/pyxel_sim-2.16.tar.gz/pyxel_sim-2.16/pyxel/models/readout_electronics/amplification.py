#  Copyright (c) European Space Agency, 2020.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

"""Readout electronics model."""

from astropy.units import Quantity

from pyxel.detectors import Detector


def apply_amplify(
    signal_2d: Quantity,
    amplifier_gain: Quantity,
) -> Quantity:
    """Apply gain from the output amplifier and signal processor.

    Parameters
    ----------
    signal_2d : ndarray
        2D signal to amplify. Unit: V
    amplifier_gain : float
        Gain of amplifier. Unit: V/V

    Returns
    -------
    ndarray
        2D amplified signal. Unit: V
    """
    amplified_signal_2d = signal_2d * amplifier_gain

    return amplified_signal_2d.to("V")


def simple_amplifier(detector: Detector) -> None:
    """Amplify signal using gain from the output amplifier and the signal processor.

    The amplification can be either uniform across the entire detector or
    defined per readout channel.

    Parameters
    ----------
    detector : Detector
        Pyxel Detector object.
    """
    pre_amplification: float | dict[str, float] = (
        detector.characteristics.pre_amplification
    )

    if isinstance(pre_amplification, dict):
        ######################################################
        # Pre-amplification per-channel                      #
        ######################################################
        pre_amplification_2d = Quantity(
            detector.characteristics.pre_amplification_map, unit="V/V"
        )
        amplified_signal_2d: Quantity = apply_amplify(
            signal_2d=Quantity(detector.signal),
            amplifier_gain=pre_amplification_2d,
        )

    else:
        ######################################################
        # Uniform pre-amplification across the full detector #
        ######################################################
        pre_amplification_1d = Quantity(
            detector.characteristics.pre_amplification, unit="V/V"
        )
        amplified_signal_2d = apply_amplify(
            signal_2d=Quantity(detector.signal),
            amplifier_gain=pre_amplification_1d,
        )

    detector.signal = amplified_signal_2d
