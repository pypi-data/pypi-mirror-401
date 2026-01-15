"""Coordinate conversion utilities for GPS and local NED frames."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional


EARTH_RADIUS_M = 6371000.0


@dataclass(frozen=True)
class GeoPoint:
    """Immutable GPS coordinate (lat, lon, alt in standard units).
    
    - lat_deg: Latitude in degrees
    - lon_deg: Longitude in degrees  
    - alt_m: Altitude in meters MSL
    """
    lat_deg: float
    lon_deg: float
    alt_m: float = 0.0
    
    @classmethod
    def from_mavlink(cls, lat: int, lon: int, alt: int = 0) -> GeoPoint:
        """Create from MAVLink format (lat*1e7, lon*1e7, alt in mm)."""
        return cls(lat / 1e7, lon / 1e7, alt / 1000.0)
    
    @classmethod
    def from_mavlink_int(cls, x: int, y: int, z: float) -> GeoPoint:
        """Create from MISSION_ITEM_INT (x=lat*1e7, y=lon*1e7, z=alt in m)."""
        return cls(x / 1e7, y / 1e7, z)
    
    @property
    def lat_e7(self) -> int:
        """Latitude in degE7 (MAVLink format)."""
        return int(self.lat_deg * 1e7)
    
    @property
    def lon_e7(self) -> int:
        """Longitude in degE7 (MAVLink format)."""
        return int(self.lon_deg * 1e7)
    
    @property
    def alt_mm(self) -> int:
        """Altitude in mm (MAVLink format)."""
        return int(self.alt_m * 1000)
    
    def is_valid(self) -> bool:
        """Check if coordinates are non-zero."""
        return not (self.lat_deg == 0.0 and self.lon_deg == 0.0)
    
    def __str__(self) -> str:
        return f"({self.lat_deg:.7f}, {self.lon_deg:.7f}, {self.alt_m:.1f}m)"


@dataclass(frozen=True)
class NEDPosition:
    """Immutable local NED position (North-East-Down in meters).
    
    - north: Positive towards geographic north
    - east: Positive towards geographic east
    - down: Positive towards Earth center
    """
    north: float
    east: float
    down: float
    
    @classmethod
    def from_xyz(cls, x: float, y: float, z: float) -> NEDPosition:
        """Create from MAVLink x/y/z (already NED)."""
        return cls(north=x, east=y, down=z)
    
    @classmethod
    def zero(cls) -> NEDPosition:
        """Create a zero position."""
        return cls(0.0, 0.0, 0.0)
    
    @property
    def altitude_agl(self) -> float:
        """Altitude above ground (inverted down)."""
        return -self.down
    
    @property
    def x(self) -> float:
        """Alias for north."""
        return self.north
    
    @property
    def y(self) -> float:
        """Alias for east."""
        return self.east
    
    @property
    def z(self) -> float:
        """Alias for down."""
        return self.down
    
    def distance_to(self, other: NEDPosition) -> float:
        """Calculate 3D distance to another NED position."""
        return math.sqrt(
            (self.north - other.north)**2 +
            (self.east - other.east)**2 +
            (self.down - other.down)**2
        )
    
    def distance_to_2d(self, other: NEDPosition) -> float:
        """Calculate 2D horizontal distance to another NED position."""
        return math.sqrt(
            (self.north - other.north)**2 +
            (self.east - other.east)**2
        )
    
    def heading_to(self, other: NEDPosition) -> float:
        """Calculate heading angle (degrees) to another NED position.
        
        Returns:
            Heading in degrees (0-360), where:
            - 0° = North
            - 90° = East
            - 180° = South
            - 270° = West
        """
        delta_north = other.north - self.north
        delta_east = other.east - self.east
        
        # atan2(east, north) gives angle from north (clockwise positive)
        heading_rad = math.atan2(delta_east, delta_north)
        heading_deg = math.degrees(heading_rad)
        
        # Normalize to 0-360
        if heading_deg < 0:
            heading_deg += 360.0
        
        return heading_deg
    
    def __str__(self) -> str:
        return f"NED({self.north:.2f}, {self.east:.2f}, {self.down:.2f})"


@dataclass
class HomePosition:
    """Home position with GPS and local NED."""
    gps: Optional[GeoPoint] = None
    local_ned: Optional[NEDPosition] = None
    is_set: bool = False
    
    def set_from_mavlink(self, lat: int, lon: int, alt: int, x: float, y: float, z: float) -> None:
        """Set from HOME_POSITION message."""
        self.gps = GeoPoint.from_mavlink(lat, lon, alt)
        self.local_ned = NEDPosition.from_xyz(x, y, z)
        self.is_set = True
    
    @property
    def lat_e7(self) -> int:
        return self.gps.lat_e7 if self.gps else 0
    
    @property
    def lon_e7(self) -> int:
        return self.gps.lon_e7 if self.gps else 0
    
    @property
    def alt_mm(self) -> int:
        return self.gps.alt_mm if self.gps else 0


@dataclass
class GPSOrigin:
    """GPS global origin (local NED frame origin).
    
    Can be set either from:
    1. GPS_GLOBAL_ORIGIN message (direct)
    2. Calculated from HOME_POSITION (origin = home GPS - home local offset)
    """
    gps: Optional[GeoPoint] = None
    is_set: bool = False
    source: str = "unknown"  # 'message' or 'calculated'
    
    def set_from_mavlink(self, lat: int, lon: int, alt: int) -> None:
        """Set from GPS_GLOBAL_ORIGIN message."""
        self.gps = GeoPoint.from_mavlink(lat, lon, alt)
        self.is_set = True
        self.source = "message"
    
    @classmethod
    def calculate_from_home(cls, home: HomePosition) -> Optional[GPSOrigin]:
        """Calculate origin from home position.
        
        The HOME_POSITION message gives us:
        - home GPS: GPS location of home
        - home local NED: Home's position in local NED frame
        
        If home is at local (10, 5, -2) NED, it means:
        - Home is 10m North, 5m East, 2m Up from origin
        
        So origin GPS = home GPS - local offset (converted to GPS)
        """
        if not home.is_set or not home.gps or not home.local_ned:
            return None
        
        if not home.gps.is_valid():
            return None
        
        # Home local offset from origin
        home_north = home.local_ned.north
        home_east = home.local_ned.east
        home_down = home.local_ned.down
        
        # Convert local offset to GPS delta
        dlat = home_north / EARTH_RADIUS_M * (180.0 / math.pi)
        dlon = home_east / (EARTH_RADIUS_M * math.cos(math.radians(home.gps.lat_deg))) * (180.0 / math.pi)
        
        # Origin GPS = Home GPS - offset
        origin_lat = home.gps.lat_deg - dlat
        origin_lon = home.gps.lon_deg - dlon
        # For altitude: origin is at z=0, home is at -home_down up from origin
        origin_alt = home.gps.alt_m + home_down  # home_down is Down, so + gives lower alt
        
        origin = cls()
        origin.gps = GeoPoint(lat_deg=origin_lat, lon_deg=origin_lon, alt_m=origin_alt)
        origin.is_set = True
        origin.source = "calculated"
        return origin


@dataclass
class CoordinateConverter:
    """Converts between GPS and local NED coordinates."""
    origin: GeoPoint
    home: Optional[GeoPoint] = None
    
    def gps_to_ned(self, point: GeoPoint) -> NEDPosition:
        """Convert GPS to local NED."""
        dlat = point.lat_deg - self.origin.lat_deg
        dlon = point.lon_deg - self.origin.lon_deg
        
        north = dlat * (math.pi / 180.0) * EARTH_RADIUS_M
        east = dlon * (math.pi / 180.0) * EARTH_RADIUS_M * math.cos(math.radians(self.origin.lat_deg))
        down = self.origin.alt_m - point.alt_m
        
        return NEDPosition(north=north, east=east, down=down)
    
    def ned_to_gps(self, ned: NEDPosition) -> GeoPoint:
        """Convert local NED to GPS."""
        lat = self.origin.lat_deg + ned.north / EARTH_RADIUS_M * (180.0 / math.pi)
        lon = self.origin.lon_deg + ned.east / (EARTH_RADIUS_M * math.cos(math.radians(self.origin.lat_deg))) * (180.0 / math.pi)
        alt = self.origin.alt_m - ned.down
        
        return GeoPoint(lat_deg=lat, lon_deg=lon, alt_m=alt)
    
    def relative_to_msl(self, alt_relative: float) -> float:
        """Convert relative altitude to MSL."""
        if self.home is None:
            raise ValueError("Home required")
        return self.home.alt_m + alt_relative
    
    def msl_to_relative(self, alt_msl: float) -> float:
        """Convert MSL to relative altitude."""
        if self.home is None:
            raise ValueError("Home required")
        return alt_msl - self.home.alt_m


def calculate_heading(from_north: float, from_east: float, to_north: float, to_east: float) -> float:
    """Calculate heading angle from one position to another.
    
    Args:
        from_north: Starting North position (meters)
        from_east: Starting East position (meters)
        to_north: Target North position (meters)
        to_east: Target East position (meters)
    
    Returns:
        Heading in degrees (0-360), where:
        - 0° = North
        - 90° = East
        - 180° = South
        - 270° = West
    """
    delta_north = to_north - from_north
    delta_east = to_east - from_east
    
    # atan2(east, north) gives angle from north (clockwise positive)
    heading_rad = math.atan2(delta_east, delta_north)
    heading_deg = math.degrees(heading_rad)
    
    # Normalize to 0-360
    if heading_deg < 0:
        heading_deg += 360.0
    
    return heading_deg


def calculate_heading_from_gps(from_lat: float, from_lon: float, to_lat: float, to_lon: float) -> float:
    """Calculate heading angle from one GPS position to another.
    
    Args:
        from_lat: Starting latitude (degrees)
        from_lon: Starting longitude (degrees)
        to_lat: Target latitude (degrees)
        to_lon: Target longitude (degrees)
    
    Returns:
        Heading in degrees (0-360), where:
        - 0° = North
        - 90° = East
        - 180° = South
        - 270° = West
    """
    # Convert GPS delta to local NED-like coordinates
    # North = delta_lat, East = delta_lon (adjusted for latitude)
    delta_lat = to_lat - from_lat
    delta_lon = to_lon - from_lon
    
    # Adjust longitude for latitude (longitude degrees are smaller near poles)
    delta_lon_adjusted = delta_lon * math.cos(math.radians((from_lat + to_lat) / 2))
    
    # Calculate heading
    heading_rad = math.atan2(delta_lon_adjusted, delta_lat)
    heading_deg = math.degrees(heading_rad)
    
    # Normalize to 0-360
    if heading_deg < 0:
        heading_deg += 360.0
    
    return heading_deg
