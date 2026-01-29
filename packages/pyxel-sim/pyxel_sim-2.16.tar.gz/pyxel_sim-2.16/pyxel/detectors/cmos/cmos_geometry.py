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


class CMOSGeometry(Geometry):
    """Geometrical attributes of a :term:`CMOS`-based detector.

    Parameters
    ----------
    row : int
        Number of pixel rows.
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
    reference_pixels : ReferenceGeometry
    masked_pixels : ReferenceGeometry
    """

    def __init__(
        self,
        row: int,
        col: int,
        total_thickness: float | None = None,  # unit: um
        pixel_vert_size: float | None = None,  # unit: um
        pixel_horz_size: float | None = None,  # unit: um
        pixel_scale: float | None = None,  # unit: arcsec/pixel
        channels: Channels | None = None,
        reference_pixels: ReferenceGeometry | None = None,
        masked_pixels: ReferenceGeometry | None = None,
    ):
        super().__init__(
            row=row,
            col=col,
            total_thickness=total_thickness,
            pixel_vert_size=pixel_vert_size,
            pixel_horz_size=pixel_horz_size,
            pixel_scale=pixel_scale,
            channels=channels,
            masked_pixels=masked_pixels,
        )

        self.reference_pixels: ReferenceGeometry | None = reference_pixels

    def __eq__(self, other) -> bool:
        return (
            type(self) is type(other)
            and super().__eq__(other)
            and self.reference_pixels == other.reference_pixels
        )

    def to_dict(self) -> Mapping:
        """Get the attributes of this instance as a `dict`."""
        dct = dict(super().to_dict())
        dct["reference_pixels"] = (
            self.reference_pixels.to_dict() if self.reference_pixels else None
        )

        return dct

    @classmethod
    def from_dict(cls, dct: dict) -> Self:
        """Create a new instance of `Geometry` from a `dict`."""
        # TODO: This is a simplistic implementation. Improve this.
        new_dct: dict = dct.copy()

        channels: Channels | None = None
        if "channels" in new_dct:
            channels_dct: Mapping | None = new_dct.pop("channels")

            if channels_dct is not None:
                channels = Channels.from_dict(channels_dct)

        reference: ReferenceGeometry | None = None
        if "reference_pixels" in new_dct:
            reference_dct: Mapping | None = new_dct.pop("reference_pixels")

            if reference_dct is not None:
                reference = ReferenceGeometry.from_dict(reference_dct)

        mask: ReferenceGeometry | None = None
        if "masked_pixels" in new_dct:
            mask_dct: Mapping = new_dct.pop("masked_pixels")

            if mask_dct is not None:
                mask = ReferenceGeometry.from_dict(mask_dct)

        return cls(
            **new_dct,
            channels=channels,
            reference_pixels=reference,
            masked_pixels=mask,
        )
