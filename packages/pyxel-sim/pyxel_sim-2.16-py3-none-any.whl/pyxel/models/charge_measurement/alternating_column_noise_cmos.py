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


# This code is adapted from NGHXRG of B.J. Rauscher, NASA/GSFC.

"""Readout noise model."""

import numpy as np
from astropy.units import Quantity

from pyxel.detectors import CMOS
from pyxel.detectors.channels import Channels
from pyxel.models.charge_measurement.uncorrelated_pink_noise_cmos import (
    create_pink_noise_cmos,
)
from pyxel.util import PinkNoiseGenerator


def create_alternating_column_noise_cmos(
    nb_pixels_overhead_after_row: int,
    nb_rows_overhead_after_frame: int,
    even_generator: PinkNoiseGenerator,
    odd_generator: PinkNoiseGenerator,
    shape: tuple[int, int],
    std: Quantity,
) -> np.ndarray:
    """Create a matrix with alternating column noise."""

    assert nb_pixels_overhead_after_row % 2 == 0
    assert shape[1] % 2 == 0

    noise_2d = np.zeros(shape)

    half_shape = (shape[0], shape[1] // 2)

    # create noise from even generator
    even_cols_noise = create_pink_noise_cmos(
        nb_pixels_overhead_after_row,
        nb_rows_overhead_after_frame,
        generator=even_generator,
        shape=half_shape,
        std=std,
    )
    # add even columns
    noise_2d[:, 0:None:2] = even_cols_noise

    # create noise from odd generator
    odd_cols_noise = create_pink_noise_cmos(
        nb_pixels_overhead_after_row,
        nb_rows_overhead_after_frame,
        generator=odd_generator,
        shape=half_shape,
        std=std,
    )
    # add odd columns
    noise_2d[:, 1:None:2] = odd_cols_noise

    return Quantity(noise_2d, unit="electron")


def create_alternating_column_noise_cmos_by_chan(
    channels: Channels,
    nb_pixels_overhead_after_row: int,
    nb_rows_overhead_after_frame: int,
    generator_by_chan: dict[str, tuple[PinkNoiseGenerator, PinkNoiseGenerator]],
    detector_shape: tuple[int, int],
    std_by_chan: dict[str, Quantity],
) -> np.ndarray:
    """Create a matrix with alternating column noise to each channel.

    Each channel has its own two generators, for even and odd columns.
    """
    noise_2d = np.zeros(detector_shape)
    for chan_label in list(channels):
        # construct a view on `noise_2d`, with every pixel belonging to
        # this channel, with respect to readout order
        this_chan_view = noise_2d[
            channels.get_channel_slices(detector_shape, chan_label)
        ]

        acn_noise = create_alternating_column_noise_cmos(
            nb_pixels_overhead_after_row,
            nb_rows_overhead_after_frame,
            even_generator=generator_by_chan[chan_label][0],
            odd_generator=generator_by_chan[chan_label][1],
            shape=this_chan_view.shape,
            std=std_by_chan[chan_label],
        )

        this_chan_view[:, :] = acn_noise

    return Quantity(noise_2d, unit="electron")


def alternating_column_noise_cmos(
    detector: CMOS,
    nb_pixels_overhead_after_row: int = 0,
    nb_rows_overhead_after_frame: int = 0,
    std: float | dict[str, float] = 1.0,
    seed: int | None = None,
) -> None:
    """Add alternating column noise into `pixel.volatile` array.

    Each channel has two generators, one for its even columns, one for its odds columns.
    The first generator adds pink noise into even columns. The second generator adds pink
    noise into odd columns.

    Generators are stored inside `CMOS` (`Detector`) object.

    Overhead reads are handled so: `nb_pixels_overhead_after_row` is divided by 2, i.e it is
    split between the two generators.

    Parameters
    ----------
    detector : CMOS
    nb_pixels_overhead_after_row : int, optional
        Number of overhead pixels to simulate after each row read.
        Used to advance the pink-noise generators consistently.
        Must be a multiple of 2.
        Default is ``0``.
    nb_rows_overhead_after_frame : int, optional
        Number of overhead rows to simulate after each frame read.
        Default is ``0``.
    std : float or dict of float, optional
        Standard deviation of the pink noise in electrons:
          - If a scalar is provided, it is applied identically to all channels.
          - If a dictionary is provided, keys must match channel labels defined in ``detector.geometry.channels``.

        All provided values must be positive. Default is ``1.0``.

        The `std` applies to both generators of a channel.
    seed : int or None, optional
        Random seed used for initializing the pink-noise generators.
        Only applied during the first invocation. Default is ``None``.
    """
    assert nb_pixels_overhead_after_row % 2 == 0

    # init the pink noise generators with the seed (only the first time)
    try:
        _ = detector.alternating_column_noise_generators
    except RuntimeError:
        detector.set_alternating_column_noise_generators(seed)

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
        noise_2d = create_alternating_column_noise_cmos_by_chan(
            detector.geometry.channels,
            nb_pixels_overhead_after_row,
            nb_rows_overhead_after_frame,
            generator_by_chan=detector.alternating_column_noise_generators,
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
        # readout order is not handled because undefined in the no channel case
        noise_2d = create_alternating_column_noise_cmos(
            nb_pixels_overhead_after_row,
            nb_rows_overhead_after_frame,
            even_generator=detector.alternating_column_noise_generators["default"][0],
            odd_generator=detector.alternating_column_noise_generators["default"][1],
            shape=detector.geometry.shape,
            std=Quantity(std, unit="electron"),
        )

    # pink noise do not accumulate in the pixel wells,
    # so we put it in `volatile`
    detector.pixel.volatile += noise_2d
