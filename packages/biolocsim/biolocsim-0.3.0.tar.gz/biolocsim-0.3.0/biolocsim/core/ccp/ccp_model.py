"""
CCP geometry model definitions.

This module defines the geometric structure of Clathrin-Coated Pits (CCPs),
modeled as spheroid caps (ellipsoidal caps) with configurable surface area,
close angle, and flattening.
"""

import numpy as np


class SpheroidCapModel:
    """
    Defines the geometry of a spheroid cap for CCP simulation.

    The spheroid cap is parametrized by:
    - surface_area: Total surface area in nm²
    - close_angle: Angle from pole to rim in degrees (0-180)
    - flattening: Flattening factor f = 1 - c/a
        - f > 0: Oblate spheroid (flattened)
        - f = 0: Perfect sphere
        - f < 0: Prolate spheroid (elongated)

    The geometry uses Z-axis as the symmetry axis, with:
    - Pole at +z (or -z for inverted caps)
    - Rim in the xy-plane (for 90° close angle)

    Attributes:
        surface_area (float): Surface area of the cap in nm².
        close_angle (float): Close angle in degrees.
        flattening (float): Flattening factor.
        radius (float): Equivalent spherical radius in nm.
        semi_axis_a (float): Equatorial semi-axis in nm.
        semi_axis_c (float): Polar semi-axis in nm.
    """

    def __init__(
        self,
        surface_area: float = 20000.0,
        close_angle: float = 60.0,
        flattening: float = 0.0,
    ):
        """
        Initialize the spheroid cap geometry model.

        Args:
            surface_area: Surface area of the cap in nm². Default is 20000 nm².
            close_angle: Angle from pole to rim in degrees (0-180). Default is 60°.
            flattening: Flattening factor f = 1 - c/a. Default is 0.0 (sphere).
                        Range: typically -0.5 to 0.7.

        Raises:
            ValueError: If parameters are out of valid range.
        """
        if surface_area <= 0:
            raise ValueError("surface_area must be positive.")
        if not -180 <= close_angle <= 180:
            raise ValueError("close_angle must be between -180 and 180 degrees.")
        if not -1 < flattening < 1:
            raise ValueError("flattening must be between -1 and 1 (exclusive).")

        self.surface_area = surface_area
        self.close_angle = close_angle
        self.flattening = flattening

        # Convert close angle to radians
        self._close_angle_rad = np.deg2rad(abs(close_angle))

        # Calculate equivalent spherical radius from surface area
        # For a spherical cap: A = 2 * pi * r^2 * (1 - cos(theta))
        # Therefore: r = sqrt(A / (2 * pi * (1 - cos(theta))))
        cos_theta = np.cos(self._close_angle_rad)
        denominator = 2 * np.pi * (1 - cos_theta)

        if denominator < 1e-10:
            # Very small close angle, treat as flat disk
            self.radius = np.sqrt(self.surface_area / np.pi)
        else:
            self.radius = np.sqrt(self.surface_area / denominator)

        # Handle negative close angle (inverted cap)
        if close_angle < 0:
            self.radius = -self.radius

        # Calculate spheroid semi-axes from flattening
        # c = 2r(1-f) / (2-f)  (polar axis)
        # a = 2r - c           (equatorial axis)
        self.semi_axis_c = 2 * self.radius * (1 - self.flattening) / (2 - self.flattening)
        self.semi_axis_a = 2 * self.radius - self.semi_axis_c

        # Calculate z-offset (height of cap center from rim plane)
        # This positions the cap so that the rim is centered
        self._z_offset = abs(self.radius) * 0.5 * (np.sin(self._close_angle_rad + np.pi / 2) + 1)

    def get_binding_sites(self, n_sites: int, rng: np.random.Generator = None) -> np.ndarray:
        """
        Generate binding site coordinates on the spheroid cap surface.

        Uses Fibonacci sphere sampling adapted for spheroid cap geometry.
        Points are distributed approximately uniformly on the cap surface.

        Args:
            n_sites: Number of binding sites to generate.
            rng: Random number generator for shuffling. If None, sites are
                 returned in Fibonacci order.

        Returns:
            np.ndarray: Shape (n_sites, 3), binding site coordinates in nm.
                        The cap is centered at origin with pole at +z.
        """
        if n_sites <= 0:
            return np.empty((0, 3))

        # Generate points on spheroid cap using adapted Fibonacci sampling
        points = self._fibonacci_spheroid_cap_points(n_sites)

        # Center the cap by shifting z coordinates
        points[:, 2] -= self._z_offset

        # Shuffle points if RNG is provided
        if rng is not None:
            rng.shuffle(points)

        return points

    def _fibonacci_spheroid_cap_points(self, n_points: int) -> np.ndarray:
        """
        Generate approximately uniformly distributed points on spheroid cap
        using Fibonacci spiral sampling.

        The algorithm:
        1. Generate points on a unit sphere cap using Fibonacci spiral
        2. Scale to spheroid by applying flattening transformation

        Args:
            n_points: Number of points to generate.

        Returns:
            np.ndarray: Shape (n_points, 3), points on the spheroid cap surface.
        """
        if n_points <= 0:
            return np.empty((0, 3))

        # For a spherical cap from pole to close_angle:
        # We sample z from cos(0) = 1 to cos(close_angle)
        cos_close = np.cos(self._close_angle_rad)

        # Fibonacci spiral parameters
        golden_ratio = (1 + np.sqrt(5)) / 2
        points = np.zeros((n_points, 3))

        for i in range(n_points):
            # Map index to z-coordinate on unit sphere cap
            # z goes from 1 (pole) to cos(close_angle) (rim)
            z = 1 - (1 - cos_close) * (i + 0.5) / n_points

            # Calculate radius in xy-plane for this z
            r_xy = np.sqrt(max(0, 1 - z * z))

            # Azimuthal angle using golden ratio for uniform distribution
            theta = 2 * np.pi * i / golden_ratio

            # Unit sphere coordinates
            x = r_xy * np.cos(theta)
            y = r_xy * np.sin(theta)

            # Scale to spheroid: x and y by semi_axis_a, z by semi_axis_c
            # But we need to ensure the point is ON the spheroid surface
            # For a spheroid: (x/a)^2 + (y/a)^2 + (z/c)^2 = 1

            # The z-coordinate on the spheroid cap
            # We parametrize by the polar angle on the equivalent sphere
            polar_angle = np.arccos(z)  # 0 at pole, close_angle at rim

            # On the spheroid, for a given polar angle:
            # x = a * sin(polar) * cos(theta)
            # y = a * sin(polar) * sin(theta)
            # z = c * cos(polar)
            sin_polar = np.sin(polar_angle)
            points[i, 0] = abs(self.semi_axis_a) * sin_polar * np.cos(theta)
            points[i, 1] = abs(self.semi_axis_a) * sin_polar * np.sin(theta)
            points[i, 2] = abs(self.semi_axis_c) * np.cos(polar_angle)

        return points

    def get_effective_radius(self) -> float:
        """
        Get the effective radius of the CCP for collision detection.

        This returns the maximum extent from the center, which is useful
        for bounding sphere collision detection.

        Returns:
            float: Effective radius in nm.
        """
        # The effective radius is the maximum of:
        # 1. The rim radius (horizontal extent)
        # 2. Half the height (vertical extent from center)
        rim_radius = abs(self.semi_axis_a) * np.sin(self._close_angle_rad)
        height = abs(self.semi_axis_c) * (1 - np.cos(self._close_angle_rad))

        return max(rim_radius, height / 2)

    def get_height(self) -> float:
        """
        Get the height of the spheroid cap from rim to pole.

        Returns:
            float: Height in nm.
        """
        return abs(self.semi_axis_c) * (1 - np.cos(self._close_angle_rad))

    def get_rim_radius(self) -> float:
        """
        Get the radius of the cap's rim (opening).

        Returns:
            float: Rim radius in nm.
        """
        return abs(self.semi_axis_a) * np.sin(self._close_angle_rad)

    def __repr__(self) -> str:
        return (
            f"SpheroidCapModel(surface_area={self.surface_area:.1f}, "
            f"close_angle={self.close_angle:.1f}, flattening={self.flattening:.2f}, "
            f"radius={abs(self.radius):.1f}, a={abs(self.semi_axis_a):.1f}, "
            f"c={abs(self.semi_axis_c):.1f})"
        )
