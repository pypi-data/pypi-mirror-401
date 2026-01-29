# Copyright or © or Copr. Thibault Pichon, CEA Paris-Saclay (2023)
#
# thibault.pichon@cea.fr
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

"""Function used to compute the glow induced by the unit cell of the pixel.

It considers a parameter the glow_per_frame, which is a contribution to the measured pixel signal each time the pixel is
selected for read. It is an additive contribution

References can be found there:
- https://onlinelibrary.wiley.com/doi/full/10.1002/asna.20230102
- REGAN, Michael W. et BERGERON, Louis E.
  Zero dark current in H2RG detectors: it is all multiplexer glow.
  Journal of Astronomical Telescopes, Instruments, and Systems,
  2020, vol. 6, no 1, p. 016001-016001.
"""

import numpy as np
from astropy.units import Quantity

from pyxel.detectors import APD, CMOS
from pyxel.util import set_random_seed


def glow(
    detector: CMOS | APD,
    glow_per_frame: float,
    std_deviation: float,
    seed: int | None = None,
) -> None:
    """Add glow effect to the detector non-volatile pixel charge.

    This model simulates the 'glow effect' caused by light emitted from the
    source-follower transistor within each pixel unit cell and subsequently
    collected by the detector sensitive layer. The glow signal is modeled as
    a normally distributed random process applied independently to each pixel.
    More information can be found in this paper :cite:p:`glow:2023`.

    Parameters
    ----------
    detector : CMOS or APD
        Pyxel detector object.
    glow_per_frame : float
        Value of the glow per frame. Unit e-/frame
    std_deviation : float
        Standard deviation of the glow distribution. Unit: e-
    seed : int, optional
        Random seed.
    """
    if std_deviation < 0.0:
        raise ValueError("'std_deviation' must be positive.")

    with set_random_seed(seed):
        glow_2d: np.ndarray = np.random.normal(
            loc=glow_per_frame,
            scale=std_deviation,
            size=detector.pixel.shape,
        )

    detector.pixel.non_volatile += Quantity(glow_2d, unit="electron")
