# Copyright or © or Copr. Antoine Kaszczyc and Aurelien Jarno, Centre de Recherche Astrophysique de Lyon (CRAL)  (2025)
#
# Antoine Kaszczyc <antoine.kaszczyc@univ-lyon1.fr>
# Aurelien Jarno <aurelien.jarno@univ-lyon1.fr>
#
# This file is part of the Pyxel general simulator framework.
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

"""Readout noise model."""

import numpy as np
from astropy.units import Quantity

from pyxel.detectors import CMOS
from pyxel.detectors.channels import Channels
from pyxel.models.charge_measurement.uncorrelated_pink_noise_cmos import (
    create_pink_noise_cmos,
)
from pyxel.util import PinkNoiseGenerator


def create_correlated_pink_noise_cmos_by_chan(
    channels: Channels,
    nb_pixels_overhead_after_row: int,
    nb_rows_overhead_after_frame: int,
    generator: PinkNoiseGenerator,
    detector_shape: tuple[int, int],
    std_by_chan: dict[str, Quantity],
) -> np.ndarray:
    """Create a matrix with correlated pink noise to each channel.

    Each channel receive the same noise from given generator,
    and readout pixel order is respected.
    """

    # it is assumed that every channel has the same shape
    (detector_nrows, detector_ncols) = detector_shape
    (nb_chans_y, nb_chans_x) = channels.matrix.shape
    chan_shape = (detector_nrows // nb_chans_y, detector_ncols // nb_chans_x)

    pink_noise = create_pink_noise_cmos(
        nb_pixels_overhead_after_row,
        nb_rows_overhead_after_frame,
        generator=generator,
        shape=chan_shape,
        std=Quantity(1, unit="electron"),  # we will handle `std` later
    )

    noise_2d = np.zeros(detector_shape)
    for chan_label in list(channels):
        # construct a view on `noise_2d`, with every pixel belonging to
        # this channel, with respect to readout order
        this_chan_view = noise_2d[
            channels.get_channel_slices(detector_shape, chan_label)
        ]
        # fill the pink noise inside the view
        this_chan_view[:, :] = pink_noise
        # apply std
        std = std_by_chan[chan_label]
        assert std.unit == "electron"
        assert std.value >= 0
        this_chan_view *= std.value

    return Quantity(noise_2d, unit="electron")


def correlated_pink_noise_cmos(
    detector: CMOS,
    nb_pixels_overhead_after_row: int = 0,
    nb_rows_overhead_after_frame: int = 0,
    std: float | dict[str, float] = 1.0,
    seed: int | None = None,
) -> None:
    """Add correlated pink noise into `pixel.volatile` array.

    For Correlated pink noise, each channel receive the same noise from one generator.
    The noise is read order dependent, and some overhead reads are simulated.
    Generator state is stored inside `CMOS` (`Detector`) object.

    Parameters
    ----------
    detector : CMOS
    nb_pixels_overhead_after_row : int, optional
        Number of overhead pixels to simulate after each row read.
        Used to advance the pink-noise generator consistently.
        Default is ``0``.
    nb_rows_overhead_after_frame : int, optional
        Number of overhead rows to simulate after each frame read.
        Default is ``0``.
    std : float or dict of float, optional
        Standard deviation of the pink noise in electrons:
          - If a scalar is provided, it is applied identically to all channels.
          - If a dictionary is provided, keys must match channel labels defined in ``detector.geometry.channels``.

        All provided values must be positive. Default is ``1.0``.
    seed : int or None, optional
        Random seed used for initializing the pink-noise generator.
        Only applied during the first invocation. Default is ``None``.
    """
    # init the pink noise generator with the seed (only the first time)
    try:
        _ = detector.correlated_pink_noise_generator
    except RuntimeError:
        detector.set_correlated_pink_noise_generator(seed)

    if detector.geometry.channels:
        ##########################################
        # channels                               #
        ##########################################

        # construct a dict to store one `std` for each channel
        # keys are channels labels
        # if user gave a scalar for `std` parameter, this scalar is
        # copied for every channel
        std_by_chan = dict()
        for chan_label in list(detector.geometry.channels):
            st = std if isinstance(std, (int, float)) else std[chan_label]
            if st < 0.0:
                raise ValueError("'std' must be positive.")
            std_by_chan[chan_label] = Quantity(st, unit="electron")

        # fill each channel with pink noise
        noise_2d = create_correlated_pink_noise_cmos_by_chan(
            detector.geometry.channels,
            nb_pixels_overhead_after_row,
            nb_rows_overhead_after_frame,
            generator=detector.correlated_pink_noise_generator,
            detector_shape=detector.geometry.shape,
            std_by_chan=std_by_chan,
        )

    else:
        ##########################################
        # no channels                            #
        ##########################################
        if isinstance(std, dict):
            raise ValueError(
                "Per-channel noise parameter was provided, but the detector "
                "does not define any geometry channels."
            )

        # fill whole detector with pink noise from the one generator
        noise_2d = create_pink_noise_cmos(
            nb_pixels_overhead_after_row,
            nb_rows_overhead_after_frame,
            generator=detector.correlated_pink_noise_generator,
            shape=detector.geometry.shape,
            std=Quantity(std, unit="electron"),
        )
        # no need to handle readout order, this property exists only for channels

    # pink noise do not accumulate in the pixel wells,
    # so we put it in `volatile`
    detector.pixel.volatile += noise_2d
