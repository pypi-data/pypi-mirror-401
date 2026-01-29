"""
ROI CCP generator.

This module provides the ROICCPGenerator class for generating SMLM point cloud
data of multiple CCPs distributed within a 3D volume (Region of Interest).
"""

from typing import List, Tuple

import numpy as np
from tqdm.auto import tqdm

from .ccp_generator import CCPGenerator


class ROICCPGenerator:
    """
    Generates point cloud data for multiple CCPs in a 3D volume (ROI).

    This generator creates realistic SMLM point clouds by:
    1. Randomly placing CCPs within a defined volume with collision avoidance
    2. Applying random orientations to each CCP
    3. Varying CCP parameters (surface area, close angle, flattening) with Gaussian noise
    4. Adding background noise (uniform and/or clustered)

    Attributes:
        config (dict): Configuration dictionary containing all parameters.
        rng (np.random.Generator): Random number generator for reproducibility.
    """

    def __init__(self, config: dict):
        """
        Initialize the ROI CCP generator with configuration.

        Args:
            config: Configuration dictionary with the following keys:

                Volume Configuration:
                    - volume_dims (list): ROI dimensions [x, y, z] in nm
                    - padding (list): Padding from edges [x, y, z] in nm

                CCP Distribution:
                    - num_ccps (int): Number of CCPs to generate
                    - min_ccp_spacing (float): Minimum center-to-center distance [nm]
                    - ccp_distribution (str): "random" or "uniform"
                    - max_placement_attempts (int): Max attempts per CCP

                CCP Parameter Variation:
                    - surface_area_std (float): Std of surface area variation [nm²]
                    - close_angle_std (float): Std of close angle variation [degrees]
                    - flattening_std (float): Std of flattening variation

                Random Orientation:
                    - apply_random_orientation (bool): Apply random 3D rotation

                CCP Configuration:
                    - ccp_config (dict): Base configuration for CCPGenerator

                Background Noise:
                    - add_background_noise (bool): Enable background noise
                    - background_uniform_density (float): Uniform noise density [points/μm³]
                    - add_clustered_noise (bool): Enable clustered noise
                    - clustered_noise_num_clusters (int): Number of noise clusters
                    - clustered_noise_points_per_cluster (int): Mean points per cluster
                    - clustered_noise_points_std (int): Std of points per cluster
                    - clustered_noise_cluster_radius (float): Mean cluster radius [nm]
                    - clustered_noise_radius_std (float): Std of cluster radius [nm]
                    - clustered_noise_shape (str): "spherical", "ellipsoidal", or "irregular"
                    - clustered_noise_elongation (float): Max elongation ratio for ellipsoids
                    - clustered_noise_num_subclusters (int): Subclusters for irregular shape

                Output Options:
                    - include_ccp_id (bool): Include CCP instance ID in output
                    - include_noise_label (bool): Label noise points with id=0

                General:
                    - seed (int): Random seed for reproducibility
                    - verbose (bool): Show progress bar
        """
        self.config = config
        self.rng = np.random.default_rng(config.get("seed"))
        self.verbose = config.get("verbose", False)

        # Extract volume parameters
        self.volume_dims = np.array(config.get("volume_dims", [10000.0, 10000.0, 2000.0]))
        self.padding = np.array(config.get("padding", [500.0, 500.0, 200.0]))

        # CCP distribution parameters
        self.num_ccps = config.get("num_ccps", 50)
        self.min_spacing = config.get("min_ccp_spacing", 200.0)
        self.distribution_type = config.get("ccp_distribution", "random")
        self.max_attempts = config.get("max_placement_attempts", 1000)

        # Output options
        self.include_ccp_id = config.get("include_ccp_id", True)
        self.include_noise_label = config.get("include_noise_label", True)

    def generate(self) -> Tuple[np.ndarray, dict]:
        """
        Generate point cloud for all CCPs in the ROI with background noise.

        Returns:
            point_cloud: np.ndarray of shape (N, 3) or (N, 4) if include_ccp_id.
                         If include_noise_label, noise points have id=0.
            stats: dict with generation statistics including:
                - requested_ccps: Number of CCPs requested
                - placed_ccps: Number of CCPs successfully placed
                - total_ccp_points: Points from CCPs
                - total_noise_points: Points from background noise
                - total_points: Total number of points
                - success_rate: Fraction of CCPs successfully placed
        """
        # Calculate placement bounds
        min_bounds = self.padding
        max_bounds = self.volume_dims - self.padding

        # Place CCPs in the volume
        ccp_placements = self._place_ccps(min_bounds, max_bounds)

        # Generate point cloud for each CCP
        all_ccp_points = []
        ccp_config_base = self.config.get("ccp_config", {}).copy()

        pbar = tqdm(
            enumerate(ccp_placements, start=1),
            total=len(ccp_placements),
            desc="Generating CCPs",
            disable=not self.verbose,
        )

        for ccp_id, (position, rotation_matrix, ccp_params) in pbar:
            # Create CCP config with varied parameters
            ccp_config = ccp_config_base.copy()
            ccp_config.update(ccp_params)
            ccp_config["seed"] = self.rng.integers(0, 2**31)
            ccp_config["apply_random_rotation"] = False  # We handle rotation here

            # Generate single CCP point cloud
            ccp_generator = CCPGenerator(ccp_config)
            points, _ = ccp_generator.generate()

            if points.size == 0:
                continue

            # Apply rotation and translation
            transformed_points = points @ rotation_matrix.T + position

            # Add CCP ID if requested
            if self.include_ccp_id or self.include_noise_label:
                ccp_ids = np.full((len(transformed_points), 1), ccp_id)
                transformed_points = np.hstack([transformed_points, ccp_ids])

            all_ccp_points.append(transformed_points)

        # Combine all CCP points
        if all_ccp_points:
            ccp_point_cloud = np.vstack(all_ccp_points)
        else:
            n_cols = 4 if (self.include_ccp_id or self.include_noise_label) else 3
            ccp_point_cloud = np.empty((0, n_cols))

        total_ccp_points = len(ccp_point_cloud)

        # Generate background noise
        noise_points = self._generate_background_noise()
        total_noise_points = len(noise_points)

        # Combine CCP points and noise
        if noise_points.size > 0:
            if self.include_ccp_id or self.include_noise_label:
                # Add id=0 for noise points
                noise_ids = np.zeros((len(noise_points), 1))
                noise_points = np.hstack([noise_points, noise_ids])
            point_cloud = np.vstack([ccp_point_cloud, noise_points]) if ccp_point_cloud.size > 0 else noise_points
        else:
            point_cloud = ccp_point_cloud

        # Remove ID column if not requested
        if not self.include_ccp_id and not self.include_noise_label and point_cloud.shape[1] == 4:
            point_cloud = point_cloud[:, :3]

        # Compile statistics
        stats = {
            "requested_ccps": self.num_ccps,
            "placed_ccps": len(ccp_placements),
            "total_ccp_points": total_ccp_points,
            "total_noise_points": total_noise_points,
            "total_points": len(point_cloud),
            "success_rate": len(ccp_placements) / self.num_ccps if self.num_ccps > 0 else 0.0,
            "volume_dims": self.volume_dims.tolist(),
            "padding": self.padding.tolist(),
        }

        return point_cloud, stats

    def _place_ccps(self, min_bounds: np.ndarray, max_bounds: np.ndarray) -> List[Tuple[np.ndarray, np.ndarray, dict]]:
        """
        Determine positions, orientations, and parameters of CCPs in the volume.

        Uses collision detection to prevent CCP overlap.

        Args:
            min_bounds: Minimum position bounds [x, y, z].
            max_bounds: Maximum position bounds [x, y, z].

        Returns:
            List of (position, rotation_matrix, ccp_params) tuples.
        """
        placements = []
        placed_positions = []
        placed_radii = []

        # Get base CCP config for parameter variation
        ccp_config_base = self.config.get("ccp_config", {})
        base_surface_area = ccp_config_base.get("surface_area", 20000.0)
        base_close_angle = ccp_config_base.get("close_angle", 60.0)
        base_flattening = ccp_config_base.get("flattening", 0.0)

        # Parameter variation std
        surface_area_std = self.config.get("surface_area_std", 3000.0)
        close_angle_std = self.config.get("close_angle_std", 10.0)
        flattening_std = self.config.get("flattening_std", 0.1)

        # Generate candidate positions
        if self.distribution_type == "uniform":
            candidate_positions = self._fibonacci_volume_points(self.num_ccps * 3, min_bounds, max_bounds)
        else:
            candidate_positions = None

        attempts = 0
        candidate_idx = 0

        pbar = tqdm(
            total=self.num_ccps,
            desc="Placing CCPs",
            disable=not self.verbose,
        )

        while len(placements) < self.num_ccps and attempts < self.max_attempts * self.num_ccps:
            attempts += 1

            # Generate varied CCP parameters
            surface_area = max(5000, self.rng.normal(base_surface_area, surface_area_std))
            close_angle = np.clip(self.rng.normal(base_close_angle, close_angle_std), 10, 170)
            flattening = np.clip(self.rng.normal(base_flattening, flattening_std), -0.5, 0.7)

            ccp_params = {
                "surface_area": surface_area,
                "close_angle": close_angle,
                "flattening": flattening,
            }

            # Estimate effective radius for this CCP
            from .ccp_model import SpheroidCapModel

            temp_model = SpheroidCapModel(surface_area, close_angle, flattening)
            effective_radius = temp_model.get_effective_radius()

            # Get candidate position
            if self.distribution_type == "uniform" and candidate_positions is not None:
                if candidate_idx >= len(candidate_positions):
                    position = self._sample_random_position(min_bounds, max_bounds)
                else:
                    position = candidate_positions[candidate_idx]
                    candidate_idx += 1
            else:
                position = self._sample_random_position(min_bounds, max_bounds)

            # Check collision with existing CCPs
            if self._check_collision(position, effective_radius, placed_positions, placed_radii):
                continue

            # Check minimum spacing constraint
            if not self._check_spacing(position, placed_positions):
                continue

            # Generate random rotation matrix
            if self.config.get("apply_random_orientation", True):
                rotation_matrix = self._random_rotation_matrix()
            else:
                rotation_matrix = np.eye(3)

            # Store placement
            placements.append((position, rotation_matrix, ccp_params))
            placed_positions.append(position)
            placed_radii.append(effective_radius)
            pbar.update(1)

        pbar.close()

        if self.verbose and len(placements) < self.num_ccps:
            print(
                f"Warning: Could only place {len(placements)}/{self.num_ccps} CCPs "
                f"with minimum spacing of {self.min_spacing} nm."
            )

        return placements

    def _sample_random_position(self, min_bounds: np.ndarray, max_bounds: np.ndarray) -> np.ndarray:
        """
        Sample a random position within the bounds.

        Args:
            min_bounds: Minimum position bounds.
            max_bounds: Maximum position bounds.

        Returns:
            Random position as np.ndarray.
        """
        return self.rng.uniform(min_bounds, max_bounds)

    def _fibonacci_volume_points(self, n_points: int, min_bounds: np.ndarray, max_bounds: np.ndarray) -> np.ndarray:
        """
        Generate approximately uniformly distributed points in a 3D volume
        using Fibonacci-like sampling.

        Args:
            n_points: Number of points to generate.
            min_bounds: Minimum position bounds.
            max_bounds: Maximum position bounds.

        Returns:
            np.ndarray: Shape (n_points, 3), points in the volume.
        """
        # Use 3D Fibonacci lattice approximation
        golden_ratio = (1 + np.sqrt(5)) / 2
        points = np.zeros((n_points, 3))

        for i in range(n_points):
            # Distribute along each axis using golden ratio offsets
            x = (i / golden_ratio) % 1
            y = (i / (golden_ratio**2)) % 1
            z = (i / (golden_ratio**3)) % 1

            points[i] = min_bounds + np.array([x, y, z]) * (max_bounds - min_bounds)

        # Shuffle to avoid bias
        self.rng.shuffle(points)

        return points

    def _check_collision(
        self,
        position: np.ndarray,
        radius: float,
        placed_positions: List[np.ndarray],
        placed_radii: List[float],
    ) -> bool:
        """
        Check if a CCP at the given position would collide with existing CCPs.

        Args:
            position: Candidate position.
            radius: Effective radius of the candidate CCP.
            placed_positions: List of placed CCP positions.
            placed_radii: List of placed CCP radii.

        Returns:
            True if collision would occur, False otherwise.
        """
        if not placed_positions:
            return False

        for placed_pos, placed_rad in zip(placed_positions, placed_radii):
            distance = np.linalg.norm(position - placed_pos)
            min_distance = radius + placed_rad
            if distance < min_distance:
                return True

        return False

    def _check_spacing(self, position: np.ndarray, placed_positions: List[np.ndarray]) -> bool:
        """
        Check if a position satisfies the minimum spacing constraint.

        Args:
            position: Candidate position.
            placed_positions: List of placed CCP positions.

        Returns:
            True if spacing constraint is satisfied.
        """
        if not placed_positions:
            return True

        placed_array = np.array(placed_positions)
        distances = np.linalg.norm(placed_array - position, axis=1)
        return np.all(distances >= self.min_spacing)

    def _random_rotation_matrix(self) -> np.ndarray:
        """
        Generate a random 3D rotation matrix using uniform random quaternion.

        Returns:
            np.ndarray: 3x3 rotation matrix.
        """
        u1, u2, u3 = self.rng.random(3)

        q0 = np.sqrt(1 - u1) * np.sin(2 * np.pi * u2)
        q1 = np.sqrt(1 - u1) * np.cos(2 * np.pi * u2)
        q2 = np.sqrt(u1) * np.sin(2 * np.pi * u3)
        q3 = np.sqrt(u1) * np.cos(2 * np.pi * u3)

        R = np.array(
            [
                [1 - 2 * (q2 * q2 + q3 * q3), 2 * (q1 * q2 - q0 * q3), 2 * (q1 * q3 + q0 * q2)],
                [2 * (q1 * q2 + q0 * q3), 1 - 2 * (q1 * q1 + q3 * q3), 2 * (q2 * q3 - q0 * q1)],
                [2 * (q1 * q3 - q0 * q2), 2 * (q2 * q3 + q0 * q1), 1 - 2 * (q1 * q1 + q2 * q2)],
            ]
        )

        return R

    def _generate_background_noise(self) -> np.ndarray:
        """
        Generate background noise points in the volume.

        Returns:
            np.ndarray: Shape (N, 3), noise point coordinates.
        """
        noise_points = []

        # Uniform noise
        if self.config.get("add_background_noise", True):
            density = self.config.get("background_uniform_density", 0.5)  # points/μm³
            # Convert to points/nm³ (1 μm³ = 10^9 nm³)
            density_nm3 = density / 1e9

            # Calculate volume and expected number of noise points
            volume = np.prod(self.volume_dims)
            n_uniform_noise = int(self.rng.poisson(density_nm3 * volume))

            if n_uniform_noise > 0:
                uniform_noise = self.rng.uniform([0, 0, 0], self.volume_dims, size=(n_uniform_noise, 3))
                noise_points.append(uniform_noise)

        # Clustered noise
        if self.config.get("add_clustered_noise", True):
            clustered_points = self._generate_clustered_noise()
            if len(clustered_points) > 0:
                noise_points.append(clustered_points)

        if noise_points:
            return np.vstack(noise_points)
        else:
            return np.empty((0, 3))

    def _generate_clustered_noise(self) -> np.ndarray:
        """
        Generate realistic clustered noise points.

        Supports multiple cluster shapes:
        - "spherical": Simple Gaussian spheres (legacy behavior)
        - "ellipsoidal": Randomly oriented ellipsoids with varying aspect ratios
        - "irregular": Multi-core clusters with irregular boundaries

        Returns:
            np.ndarray: Shape (N, 3), clustered noise point coordinates.
        """
        n_clusters = self.config.get("clustered_noise_num_clusters", 10)
        mean_points = self.config.get("clustered_noise_points_per_cluster", 20)
        points_std = self.config.get("clustered_noise_points_std", 10)
        mean_radius = self.config.get("clustered_noise_cluster_radius", 50.0)
        radius_std = self.config.get("clustered_noise_radius_std", 20.0)
        shape = self.config.get("clustered_noise_shape", "irregular")
        elongation = self.config.get("clustered_noise_elongation", 3.0)
        n_subclusters = self.config.get("clustered_noise_num_subclusters", 3)

        all_cluster_points = []

        for _ in range(n_clusters):
            # Random cluster center within volume
            center = self.rng.uniform([0, 0, 0], self.volume_dims)

            # Randomize number of points per cluster (log-normal like distribution)
            n_points = max(5, int(self.rng.normal(mean_points, points_std)))

            # Randomize cluster radius
            cluster_radius = max(10.0, self.rng.normal(mean_radius, radius_std))

            if shape == "spherical":
                # Simple Gaussian sphere
                cluster_points = self._generate_spherical_cluster(center, cluster_radius, n_points)

            elif shape == "ellipsoidal":
                # Randomly oriented ellipsoid
                cluster_points = self._generate_ellipsoidal_cluster(center, cluster_radius, n_points, elongation)

            elif shape == "irregular":
                # Multi-core irregular cluster
                cluster_points = self._generate_irregular_cluster(
                    center, cluster_radius, n_points, n_subclusters, elongation
                )
            else:
                # Default to spherical
                cluster_points = self._generate_spherical_cluster(center, cluster_radius, n_points)

            # Clip to volume bounds
            cluster_points = np.clip(cluster_points, [0, 0, 0], self.volume_dims)
            all_cluster_points.append(cluster_points)

        if all_cluster_points:
            return np.vstack(all_cluster_points)
        else:
            return np.empty((0, 3))

    def _generate_spherical_cluster(self, center: np.ndarray, radius: float, n_points: int) -> np.ndarray:
        """
        Generate a simple Gaussian spherical cluster.

        Args:
            center: Cluster center position.
            radius: Cluster radius (used as 3*sigma for Gaussian).
            n_points: Number of points to generate.

        Returns:
            np.ndarray: Shape (n_points, 3), cluster points.
        """
        sigma = radius / 3.0
        return self.rng.normal(center, sigma, size=(n_points, 3))

    def _generate_ellipsoidal_cluster(
        self, center: np.ndarray, radius: float, n_points: int, max_elongation: float
    ) -> np.ndarray:
        """
        Generate a randomly oriented ellipsoidal cluster.

        The ellipsoid has random aspect ratios and orientation, creating
        more realistic elongated or flattened cluster shapes.

        Args:
            center: Cluster center position.
            radius: Base radius (mean of semi-axes).
            n_points: Number of points to generate.
            max_elongation: Maximum ratio between longest and shortest axis.

        Returns:
            np.ndarray: Shape (n_points, 3), cluster points.
        """
        # Generate random aspect ratios for ellipsoid axes
        # One axis can be elongated, creating prolate or oblate shapes
        elongation = self.rng.uniform(1.0, max_elongation)
        flatten = self.rng.uniform(0.5, 1.0)

        # Random assignment of elongation to axes
        axis_order = self.rng.permutation(3)
        scales = np.array([1.0, 1.0, 1.0])
        scales[axis_order[0]] = elongation
        scales[axis_order[1]] = flatten
        # scales[axis_order[2]] remains 1.0

        # Normalize so mean scale equals radius
        scales = scales / np.mean(scales) * radius / 3.0

        # Generate points in unit sphere, then scale
        # Using rejection sampling for uniform distribution in ellipsoid
        points = []
        while len(points) < n_points:
            # Generate candidate points
            candidates = self.rng.normal(0, 1, size=(n_points * 2, 3))
            # Apply anisotropic scaling
            candidates = candidates * scales
            points.extend(candidates[: n_points - len(points)])

        points = np.array(points[:n_points])

        # Apply random rotation
        rotation = self._random_rotation_matrix()
        points = points @ rotation.T

        # Translate to center
        return points + center

    def _generate_irregular_cluster(
        self,
        center: np.ndarray,
        radius: float,
        n_points: int,
        n_subclusters: int,
        max_elongation: float,
    ) -> np.ndarray:
        """
        Generate an irregular multi-core cluster.

        This simulates realistic protein aggregates that often consist of
        multiple merged smaller aggregates with irregular boundaries.

        Args:
            center: Overall cluster center position.
            radius: Overall cluster radius.
            n_points: Total number of points to generate.
            n_subclusters: Number of subclusters to merge.
            max_elongation: Maximum elongation for individual subclusters.

        Returns:
            np.ndarray: Shape (n_points, 3), cluster points.
        """
        # Randomize number of subclusters (at least 1)
        actual_subclusters = max(1, int(self.rng.poisson(n_subclusters)))

        # Distribute points among subclusters (not uniform)
        weights = self.rng.dirichlet(np.ones(actual_subclusters) * 2)
        points_per_subcluster = (weights * n_points).astype(int)
        # Ensure at least some points in each
        points_per_subcluster = np.maximum(points_per_subcluster, 3)
        # Adjust total to match n_points
        diff = n_points - np.sum(points_per_subcluster)
        if diff > 0:
            points_per_subcluster[0] += diff
        elif diff < 0:
            points_per_subcluster[0] = max(3, points_per_subcluster[0] + diff)

        all_points = []

        for i in range(actual_subclusters):
            # Subcluster center is offset from main center
            # Distance from center follows exponential-like distribution
            offset_distance = self.rng.exponential(radius * 0.4)
            offset_direction = self.rng.normal(0, 1, 3)
            offset_direction = offset_direction / (np.linalg.norm(offset_direction) + 1e-10)
            subcluster_center = center + offset_direction * offset_distance

            # Subcluster radius is smaller than main cluster
            subcluster_radius = radius * self.rng.uniform(0.3, 0.7)

            # Generate subcluster as ellipsoid
            n_sub_points = points_per_subcluster[i]
            sub_points = self._generate_ellipsoidal_cluster(
                subcluster_center, subcluster_radius, n_sub_points, max_elongation
            )
            all_points.append(sub_points)

        if all_points:
            return np.vstack(all_points)
        else:
            return np.empty((0, 3))
