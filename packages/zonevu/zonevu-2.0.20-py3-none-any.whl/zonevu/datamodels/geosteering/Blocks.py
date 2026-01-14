#  Copyright (c) 2024 Ubiterra Corporation. All rights reserved.
#  #
#  This ZoneVu Python SDK software is the property of Ubiterra Corporation.
#  You shall use it only in accordance with the terms of the ZoneVu Service Agreement.
#  #
#  This software is made available on PyPI for download and use. However, it is NOT open source.
#  Unauthorized copying, modification, or distribution of this software is strictly prohibited.
#  #
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
#  PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
#  FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#  ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
#

"""
Geosteering block model.

Defines blocks used to model stratigraphy for geosteering predictions.
"""

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Union

import numpy as np

from ...datamodels.geosteering.Horizon import Horizon
from ...datamodels.geosteering.Pick import Pick
from ..geospatial.Coordinate import Coordinate
from ..geospatial.GeoLocation import GeoLocation
from ..geospatial.LineSegment import LineSegment
from ..geospatial.Polyline import Polyline


@dataclass
class GeosteerItem(ABC):
    """Base for geosteering items used in interpretations (picks, horizons)."""
    next_item: Optional['GeosteerItem']

    @property
    @abstractmethod
    def kind(self) -> str:
        pass

    @property
    # @abstractmethod
    def next(self) -> 'GeosteerItem | None':
        return self.next_item

    def find_next_block(self) -> Union['Block', None]:
        item = self
        while True:
            item = item.next
            if item is None or isinstance(item, Block):
                return item


@dataclass
class Layer:
    """
    A layer in a geosteering block corresponding to a horizon in a geosteering interpretation
    """
    block: 'Block'
    #: The horizon defining the top of this layer
    horz: Horizon
    #: The horizon defining the bottom of this layer
    bottom_horz: Horizon
    #: The tvd of the top of this layer at the start of the block
    tvd_start: float
    #: The tvd of the top of this layer at the end of the block
    tvd_end: float
    #: The thickness (TVT) of this layer (bottom - top)
    thickness: float

    @property
    def polygon(self) -> Polyline:
        """
        A polygon in (md, tvd) space that is a layer in a geosteering block

        :return:
        """
        return self.make_polygon_with_thickness(self.thickness)

    @property
    def top(self) -> LineSegment:
        s = self
        return LineSegment(Coordinate(s.block.md_start, s.tvd_start), Coordinate(s.block.md_end, s.tvd_end))

    @property
    def bottom(self) -> LineSegment:
        s = self
        return LineSegment(Coordinate(s.block.md_start, s.tvd_start + s.thickness), Coordinate(s.block.md_end, s.tvd_end + s.thickness))

    def make_polygon_with_thickness(self, thickness: float) -> Polyline:
        """
        A polygon in (md, tvd) space from the top of this block with specified thickness

        :return:
        """
        s = self
        x1 = s.block.md_start
        x2 = s.block.md_end
        y1a = s.tvd_start
        y1b = y1a + thickness
        y2a = s.tvd_end
        y2b = y2a + thickness
        coordinates = [Coordinate(x1, y1a), Coordinate(x2, y2a), Coordinate(x2, y2b), Coordinate(x1, y1b)]
        p = Polyline(coordinates)
        return p
    
    def make_polygon_from_tvd(self, tvd: float) -> Polyline:
        """
        A polygon in (md, tvd) space from the minimum of the specified tvd and the top of this block to the top of this block

        :return:
        """
        x1 = self.block.md_start
        x2 = self.block.md_end
        y1b = self.tvd_start
        y2b = self.tvd_end
        tvd = min(tvd, y1b, y2b)
        y1a = tvd
        y2a = tvd
        coordinates = [Coordinate(x1, y1a), Coordinate(x2, y2a), Coordinate(x2, y2b), Coordinate(x1, y1b)]
        p = Polyline(coordinates)
        return p
    
    def make_polygon_to_tvd(self, tvd: float) -> Polyline:
        """
        A polygon in (md, tvd) space from the bottom of this block to the maximum of the specified tvd and the bottom of this block

        :return:
        """
        x1 = self.block.md_start
        x2 = self.block.md_end
        y1a = self.tvd_start + self.thickness
        y2a = self.tvd_end + self.thickness
        tvd = max(tvd, y1a, y2a)
        y1b = tvd
        y2b = tvd
        coordinates = [Coordinate(x1, y1a), Coordinate(x2, y2a), Coordinate(x2, y2b), Coordinate(x1, y1b)]
        p = Polyline(coordinates)
        return p

@dataclass
class Block(GeosteerItem):
    """
    A geosteering block derived from a pair of geosteering interpretation pick

    NOTE: start = the heel-ward direction, and end = the toe-ward direction
    NOTE: in the interpretation, each block is followed by either a block or a fault.
    """
    start_pick: Pick
    end_pick: Pick
    layers: List[Layer] = field(default_factory=list[Layer])
    target_layer: Optional[Layer] = None

    @property
    def kind(self) -> str:
        return 'Block'

    @property
    def md_start(self) -> float:
        return self.start_pick.md

    @property
    def md_end(self) -> float:
        return self.end_pick.md

    @property
    def location_start(self) -> GeoLocation | None:
        if self.start_pick.latitude is None or self.start_pick.longitude is None:
            return None
        return GeoLocation(self.start_pick.latitude, self.start_pick.longitude)

    @property
    def location_end(self) -> GeoLocation | None:
        if self.end_pick.latitude is None or self.end_pick.longitude is None:
            return None
        return GeoLocation(self.end_pick.latitude, self.end_pick.longitude)

    @property
    def xyz_start(self) -> Coordinate | None:
        if self.start_pick.x is None or self.start_pick.y is None or self.start_pick.target_tvd is None:
            return None
        return Coordinate(self.start_pick.x, self.start_pick.y, self.start_pick.target_tvd)

    @property
    def xyz_end(self) -> Coordinate | None:
        if self.end_pick.x is None or self.end_pick.y is None or self.end_pick.target_tvd is None:
            return None
        return Coordinate(self.end_pick.x, self.end_pick.y, self.end_pick.target_tvd)

    @property
    def elevation_start(self) -> float | None:
        """
        Get elevation of target formation at start of block

        :return:
        """
        return self.start_pick.target_elevation

    @property
    def elevation_end(self) -> float | None:
        """
        Get elevation of target formation at end of block

        :return:
        """
        return self.end_pick.target_elevation

    @property
    def dip(self) -> float:
        """
        Get geologic dip of block in direction of increasing MD

        :return:
        """
        if self.xyz_start is None or self.xyz_end is None:
            return np.nan
        c1 = self.xyz_start.vector
        c2 = self.xyz_end.vector
        v = c2 - c1  # Vector pointing along top of block
        h = np.array([v[0], v[1], 0])  # Vector pointing along plane in direction of block
        v_norm = np.linalg.norm(v)
        h_norm = np.linalg.norm(h)
        cos_theta = np.dot(v, h) / (v_norm * h_norm)
        if cos_theta > 1:
            cos_theta = 1
        elif cos_theta < -1:
            cos_theta = -1
        try:
            dip_radians = math.acos(cos_theta)
            dip_degrees = math.degrees(dip_radians)
            return dip_degrees
        except ValueError as err:
            return np.nan

    @property
    def inclination(self) -> float:
        """
        This is the "MD dip" - inclination relative to the wellbore inclination

        :return:
        """
        dHX = self.end_pick.md - self.start_pick.md
        if self.end_pick.target_tvd is None or self.start_pick.target_tvd is None:
            return np.nan
        dTVD = self.end_pick.target_tvd - self.start_pick.target_tvd
        incl = 90 + math.atan2(-dTVD, dHX) * 180 / math.pi
        return incl

    @property
    def length(self) -> float:
        """
        Get length of block

        :return:
        """
        if self.xyz_start is None or self.xyz_end is None:
            return np.nan
        c1 = self.xyz_start.vector
        c2 = self.xyz_end.vector
        v = c2 - c1  # Vector pointing along top of block
        return float(np.linalg.norm(v))

    @property
    def md_length(self) -> float:
        md_len = self.md_end - self.md_start
        return md_len

    def contains_md(self, md: float):
        if self.md_start <= md < self.md_end:
            return True
        return False

    def make_copy(self) -> 'Block':
        block_copy = Block(next_item=None, start_pick=self.start_pick, end_pick=self.end_pick)
        for L in self.layers:
            l_copy = Layer(block=block_copy, horz=L.horz, bottom_horz=L.bottom_horz,
                           tvd_start=L.tvd_start, tvd_end=L.tvd_end, thickness=L.thickness)
            block_copy.layers.append(l_copy)
        return block_copy

    @classmethod
    def make_infill_block(cls, b1: 'Block', b2: 'Block') -> 'Block':
        b = Block(next_item=None, start_pick=b1.end_pick, end_pick=b2.start_pick)
        for l1, l2 in zip(b1.layers, b2.layers):
            infill_layer = Layer(block=b, horz=l1.horz, bottom_horz=l1.bottom_horz,
                                 tvd_start=l1.tvd_end, tvd_end=l2.tvd_start, thickness=l1.thickness)
            b.layers.append(infill_layer)
            if b1.target_layer is not None and infill_layer.horz == b1.target_layer.horz:
                b.target_layer = infill_layer
        return b

    def make_pick(self, md: float) -> Pick:
        p1 = self.start_pick
        p2 = self.end_pick
        m = (md - p1.md) / (p2.md - p1.md)

        def lerp(a, b):
            return a + (b - a) * m

        if self.xyz_start is not None and self.xyz_end is not None:    
            p1_v = self.xyz_start.vector
            p2_v = self.xyz_end.vector
            c = lerp(p1_v, p2_v)
        else:
            c = None
        if self.location_start is not None and self.location_end is not None:
            g1 = np.array([self.location_start.longitude, self.location_start.latitude, self.elevation_start])
            g2 = np.array([self.location_end.longitude, self.location_end.latitude, self.elevation_end])
            g = lerp(g1, g2)
        else:
            g = None
        d1 = np.array([p1.dx, p1.dy])
        d2 = np.array([p2.dx, p2.dy])
        d = lerp(d1, d2)
        target_tvd = c[2] if c is not None else None
        x = c[0] if c is not None else None
        y = c[1] if c is not None else None
        latitude = g[1] if g is not None else None
        longitude = g[0] if g is not None else None
        target_elevation = g[2] if g is not None else None
        tvt = lerp(p1.target_tvt, p2.target_tvt)
        elev = lerp(p1.elevation, p2.elevation)
        tvd = lerp(p1.tvd, p2.tvd)
        vx = lerp(p1.vx, p2.vx)
        p = Pick(target_tvd=target_tvd, x=x, y=y, md=md, block_flag=True, type_wellbore_id=p1.type_wellbore_id,
                 type_curve_def_id=p1.type_curve_def_id, latitude=latitude, longitude=longitude, target_elevation=target_elevation,
                 dx=d[0], dy=d[1], target_tvt=tvt, elevation=elev, tvd=tvd, vx=vx)
        return p


@dataclass
class Throw:
    """
    A throw in a geosteering fault corresponding to a horizon in a geosteering interpretation
    """
    fault: 'Fault'
    horz: Horizon
    tvd_start: float
    tvd_end: float
    throw_amt: float

    @property
    def line(self) -> Polyline:
        line = Polyline([Coordinate(self.fault.md, self.tvd_start), Coordinate(self.fault.md, self.tvd_end)])
        return line


@dataclass
class Fault(GeosteerItem):
    """
    A geosteering fault derived from a pair of geosteering interpretation picks

    NOTE: in the interpretation, each fault is followed by a block.
    """
    pick: Pick
    throws: List[Throw] = field(default_factory=list[Throw])
    target_throw: Optional[Throw] = None
    # next_block: Optional[Block] = None

    @property
    def kind(self) -> str:
        return 'Fault'

    @property
    def md(self) -> float:
        return self.pick.md

    @property
    def location(self) -> GeoLocation | None:
        if self.pick.latitude is None or self.pick.longitude is None:
            return None
        return GeoLocation(self.pick.latitude, self.pick.longitude)

    def xyz(self) -> Coordinate | None:
        """
        XYZ of the top of target on heel-ward side of fault.

        :return:
        """
        if self.pick.x is None or self.pick.y is None or self.pick.target_tvd is None:
            return None
        return Coordinate(self.pick.x, self.pick.y, self.pick.target_tvd)

    @property
    def elevation(self) -> float | None:
        """
        Elevation of the top of target on heel-ward side of fault.

        :return:
        """
        return self.pick.target_elevation

    @property
    def trace(self) -> Polyline:
        pts = [Coordinate(self.md, min(t.tvd_start, t.tvd_end)) for t in self.throws]
        if len(self.throws) > 0:
            last_t = self.throws[-1]
            max_tvd = max(last_t.tvd_start, last_t.tvd_end)
            pts.append(Coordinate(self.md, max_tvd))
        return Polyline(pts)

