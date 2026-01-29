#  Copyright (c) European Space Agency, 2020.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

"""Sub-package to handle and validate matrix structures and readout positions for multi-channels detectors.

**Example of four channels**

In this example four channels ``OP9``, ``OP13``, ``OP1`` and ``OP5`` are
defined in a matrix configuration as follows:

.. figure:: _static/channels.png
    :scale: 70%
    :alt: Channels
    :align: center

Based on the standard readout position, the **channel order** is: ``OP9`` (top-left), ``OP13`` (top-right),
``OP1`` (bottom-left) and ``OP1`` (bottom-right).

The corresponding YAML definition could be:

.. code-block:: yaml


 geometry:
    row: 1028
    col: 1024
    channels:
      matrix: [[OP9, OP13],
               [OP1, OP5 ]]
      readout_position:
        - OP9:  top-left
        - OP13: top-left
        - OP1:  bottom-left
        - OP5:  bottom-left
"""

from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass

import numpy as np
from astropy.units import Quantity
from typing_extensions import Self, overload


@dataclass
class ReferenceGeometry:
    """Class to store and validate the 1D or 2D matrix structure.

    Examples
    --------
    >>> matrix = Matrix([["OP9", "OP13"], ["OP1", "OP5"]])
    >>> matrix.shape
    (2, 2)
    >>> matrix.size
    4
    >>> matrix.ndim
    2
    >>> list(matrix)
    ['OP9', 'OP13', 'OP1', 'OP5']
    """

    row: Sequence[int] | None = None  # TODO: Use 'tuple' ?
    col: Sequence[int] | None = None

    @classmethod
    def from_dict(cls, dct: Mapping) -> Self:
        row: Sequence[int] | None = dct.get("row")
        col: Sequence[int] | None = dct.get("col")

        return cls(row=row, col=col)

    def to_dict(self) -> Mapping:
        return asdict(self)

    @overload
    def apply_mask(self, data_2d: np.ndarray, value: float | int) -> np.ndarray: ...
    @overload
    def apply_mask(self, data_2d: Quantity, value: Quantity) -> Quantity: ...

    def apply_mask(self, data_2d: np.ndarray | Quantity, value: float | int | Quantity):
        """Apply a 'value' to the row(s)/column(s).

        Parameters
        ----------
        data_2d : numpy or Quantity 2D array.
        value : float, int, Quantity
            The value to apply to the row(s)/column(s).

        Returns
        -------
        numpy or Quantity 2D array
            A new array in which all specified row(s) and column(s)
            are replaced by 'value'

        Examples
        --------
        >>> import numpy as np

        >>> data = np.array(
        ...     [
        ...         [0.0, 1.0, 2.0],
        ...         [3.0, 4.0, 5.0],
        ...         [6.0, 7.0, 8.0],
        ...     ]
        ... )
        >>> obj = ReferenceGeometry(row=[0, 2], col=[1])
        >>> obj.apply_mask(data_2d=data, value=np.nan)
        array([[nan, nan, nan],
               [ 3., nan,  5.],
               [nan, nan, nan]])
        """
        output_2d = data_2d.copy()

        if self.row:
            for row_idx in self.row:
                output_2d[row_idx, :] = value

        if self.col:
            for col_idx in self.col:
                output_2d[:, col_idx] = value

        return output_2d
