#  Copyright (c) European Space Agency, 2020.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

"""TBW."""

from collections.abc import Mapping

from typing_extensions import Self

from pyxel.detectors import Channels, ReferenceGeometry
from pyxel.detectors.geometry import Geometry


class CCDRegions:
    """Row layout definition for a CCD detector.

    This class describes the partitioning of detector rows into:
    - an image region
    - an overscan region

    Parameters
    ----------
    image_row : int
        Number of row(s) in the image region.
    overscan_row : int
        Number of row(s) in the overscan region.

    Raises
    ------
    ValueError
        If `image_row` is not strictly positive.
    ValueError
        If `overscan_row` exceeds `image_row`.
    """

    def __init__(self, image_row: int, overscan_row: int):
        if image_row <= 0:
            raise ValueError("'image_row' must be strictly positive")
            # TODO: Check if overscan rows can be less than image rows!
        elif overscan_row > image_row:
            raise ValueError("'overscan_row' cannot exceed 'image_row'")

        self._image_row: int = image_row
        self._overscan_row: int = overscan_row

    def __eq__(self, other) -> bool:
        return type(self) is type(other) and (
            (self._image_row, self._overscan_row)
            == (
                other._image_row,
                other._overscan_row,
            )
        )

    @property
    def image_row(self) -> int:
        """Number of rows in the image region."""
        return self._image_row

    @property
    def overscan_row(self) -> int:
        """Number of rows in the overscan region."""
        return self._overscan_row

    @property
    def num_rows(self) -> int:
        """Total number of rows (image + overscan)."""
        return self.image_row + self.overscan_row

    def to_dict(self) -> Mapping:
        """Convert to a dictionary."""
        return {
            "image_row": self._image_row,
            "overscan_row": self._overscan_row,
        }

    @classmethod
    def from_dict(cls, dct: dict) -> Self:
        """Create a class `CCDRegions` from a dictionary."""
        return cls(**dct)


class CCDGeometry(Geometry):
    """Geometrical description of a :term:`CCD` detector.

    A CCD geometry defines the detector dimensions with an optional overscan region.

    The row layout can be specified in one of two ways:
    - as an `int` defining the total number of rows.
    - as a `CCDRegions` defining image and overscan regions.

    Parameters
    ----------
    row : int or CCDRegions
        Row configuration of the detector.
    col : int
        Number of pixel columns.
    total_thickness : float
        Thickness of detector. Unit: um
    pixel_vert_size : float
        Vertical dimension of pixel. Unit: um
    pixel_horz_size : float
        Horizontal dimension of pixel. Unit: um
    pixel_scale : float
        Dimension of how much of the sky is covered by one pixel. Unit: arcsec/pixel
    """

    def __init__(
        self,
        row: int | CCDRegions,
        col: int,
        total_thickness: float | None = None,  # unit: um
        pixel_vert_size: float | None = None,  # unit: um
        pixel_horz_size: float | None = None,  # unit: um
        pixel_scale: float | None = None,  # unit: arcsec/pixel
        channels: Channels | None = None,
        masked_pixels: ReferenceGeometry | None = None,
    ):
        if isinstance(row, int) and row <= 0:
            raise ValueError("'row' must be strictly greater than 0.")

        if col <= 0:
            raise ValueError("'col' must be strictly greater than 0.")

        if total_thickness and not (0.0 <= total_thickness <= 10000.0):
            raise ValueError("'total_thickness' must be between 0.0 and 10000.0.")

        if pixel_vert_size and not (0.0 <= pixel_vert_size <= 1000.0):
            raise ValueError("'pixel_vert_size' must be between 0.0 and 1000.0.")

        if pixel_horz_size and not (0.0 <= pixel_horz_size <= 1000.0):
            raise ValueError("'pixel_horz_size' must be between 0.0 and 1000.0.")

            # TODO: Create a new class in channels to measure the matrix
        if channels is not None:
            # Vertical length: number of rows
            vertical_channels, horizontal_channels = channels.matrix.shape

            # vertical_channels = channels.matrix.shape[0]
            # Horizontal lengths: number of elements in a row
            # horizontal_channels = channels.matrix.shape[1]
            if isinstance(row, int):
                num_rows: int = row
            else:
                num_rows = row.num_rows

            if vertical_channels > num_rows:
                raise ValueError(
                    "Vertical size of the channel must be at least one pixel"
                )

            if horizontal_channels > col:
                raise ValueError(
                    "Horizontal size of the channel must be at least one pixel"
                )

        if isinstance(row, CCDRegions):
            region: CCDRegions = row

            masked_overscan_rows = list(
                range(region.image_row, region.image_row + region.overscan_row)
            )

            if masked_pixels is None:
                # Automatically mask overscan rows
                masked_pixels = ReferenceGeometry(row=masked_overscan_rows)
            else:
                # Add new masked pixels
                new_masked_row = (
                    set(masked_overscan_rows)
                    if masked_pixels.row is None
                    else set(masked_overscan_rows) | set(masked_pixels.row)
                )

                masked_pixels = ReferenceGeometry(
                    row=sorted(new_masked_row),
                    col=masked_pixels.col,
                )

        self._row: int | CCDRegions = row  # type: ignore[assignment]
        self._col: int = col

        self._total_thickness: float | None = total_thickness
        self._pixel_vert_size: float | None = pixel_vert_size
        self._pixel_horz_size: float | None = pixel_horz_size
        self._pixel_scale: float | None = pixel_scale

        # if channels:
        #     channels.validate(geometry=self)

        self.channels: Channels | None = channels
        self.masked_pixels: ReferenceGeometry | None = masked_pixels

        self._numbytes: int = 0

    def __eq__(self, other) -> bool:
        return type(self) is type(other) and (
            self._row,
            self._col,
            self._total_thickness,
            self._pixel_vert_size,
            self._pixel_horz_size,
            self._pixel_scale,
            self.channels,
            self.masked_pixels,
        ) == (
            other._row,
            other._col,
            other._total_thickness,
            other._pixel_vert_size,
            other._pixel_horz_size,
            other._pixel_scale,
            other.channels,
            other.masked_pixels,
        )

    @property
    def row(self) -> int:
        """Get Number of pixel rows."""
        if isinstance(self._row, int):
            return self._row

        return self._row.num_rows

    @row.setter
    def row(self, value: int) -> None:
        raise AttributeError

    @property
    def image_row(self) -> int:
        """Number of rows in the image region.

        Raises
        ------
        TypeError
            If the CCD geometry has no explicit image/overscan definition.
        """
        if not isinstance(self._row, CCDRegions):
            raise TypeError("CCD geometry does not define image/overscan regions.")

        return self._row.image_row

    @property
    def overscan_row(self) -> int:
        """Number of rows in the overscan region.

        Raises
        ------
        TypeError
            If the CCD geometry has no explicit image/overscan definition.
        """
        if not isinstance(self._row, CCDRegions):
            raise TypeError("CCD geometry does not define image/overscan regions.")

        return self._row.overscan_row

    @property
    def has_overscan(self) -> bool:
        """Check if the CCD geometry includes an overscan region."""
        return isinstance(self._row, CCDRegions)

    def to_dict(self) -> Mapping:
        """Get the attributes of this instance as a `dict`."""
        return {
            "row": self._row if isinstance(self._row, int) else self._row.to_dict(),
            "col": self.col,
            "total_thickness": self._total_thickness,
            "pixel_vert_size": self._pixel_vert_size,
            "pixel_horz_size": self._pixel_horz_size,
            "pixel_scale": self._pixel_scale,
            "channels": self.channels.to_dict() if self.channels else None,
            "masked_pixels": (
                self.masked_pixels.to_dict() if self.masked_pixels else None
            ),
        }

    @classmethod
    def from_dict(cls, dct: dict) -> Self:
        """Create a new instance of `Geometry` from a `dict`."""
        # TODO: This is a simplistic implementation. Improve this.
        new_dct: dict = dct.copy()

        if "row" not in new_dct:
            raise KeyError

        row_int_or_dct = new_dct.pop("row")

        row: int | CCDRegions
        if isinstance(row_int_or_dct, int):
            row = row_int_or_dct
        elif isinstance(row_int_or_dct, dict):
            row = CCDRegions.from_dict(row_int_or_dct)
        else:
            raise TypeError

        channels: Channels | None = None
        if "channels" in new_dct:
            channels_dct: Mapping | None = new_dct.pop("channels")

            if channels_dct is not None:
                channels = Channels.from_dict(channels_dct)

        mask: ReferenceGeometry | None = None
        if "masked_pixels" in new_dct:
            mask_dct: Mapping = new_dct.pop("masked_pixels")

            if mask_dct is not None:
                mask = ReferenceGeometry.from_dict(mask_dct)

        return cls(
            **new_dct,
            row=row,
            channels=channels,
            masked_pixels=mask,
        )
