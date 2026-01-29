"""
CCP point cloud generator.

This module provides the CCPGenerator class for generating SMLM point cloud
data of single Clathrin-Coated Pits with realistic error models.
"""

from typing import Tuple

import numpy as np

from .ccp_model import SpheroidCapModel


class CCPGenerator:
    """
    Generates point cloud data for a single Clathrin-Coated Pit.

    This generator creates realistic SMLM point clouds by:
    1. Defining the CCP geometry using SpheroidCapModel
    2. Generating clathrin binding sites on the spheroid cap surface
    3. Applying spatial exclusion for labeling (steric effects)
    4. Generating multiple localizations per binding site (blinking)
    5. Adding various error models:
       - Binding site jitter (structural heterogeneity)
       - Linker error (antibody arm displacement)
       - Localization uncertainty (photon-limited precision)
    6. Optionally applying random 3D rotation

    Attributes:
        config (dict): Configuration dictionary containing all parameters.
        model (SpheroidCapModel): The CCP geometry model.
        rng (np.random.Generator): Random number generator for reproducibility.
    """

    def __init__(self, config: dict):
        """
        Initialize the CCP generator with configuration.

        Args:
            config: Configuration dictionary with the following keys:

                CCP Geometry:
                    - surface_area (float): Surface area in nm² (default 20000)
                    - close_angle (float): Close angle in degrees (default 60)
                    - flattening (float): Flattening factor (default 0.0)

                Clathrin Binding Sites:
                    - num_clathrin_sites (int): Number of potential sites (default 200)
                    - use_spatial_exclusion (bool): Enable spatial exclusion (default True)
                    - min_labeling_distance (float): Min distance between labels [nm] (default 12.0)

                Labeling Parameters:
                    - density_of_labeling (float): Fraction of sites labeled (0-1)
                    - localizations_per_site (int): Mean localizations per site
                    - localizations_distribution (str): "constant" or "geometric"
                    - localizations_p (float): Geometric distribution parameter

                Localization Uncertainty:
                    - localization_precision_xy (float): Mean precision in XY [nm]
                    - localization_precision_z (float): Mean precision in Z [nm]
                    - localization_precision_distribution (str): "poisson_uniform" or "constant"

                Linker Error:
                    - linker_length (float): Linker length [nm] (0 = disabled)
                    - linker_type (str): "normal" (Gaussian) or "stick" (rigid rod)
                    - linker_flexibility (float): Flexibility std for "normal" type [nm]

                Binding Site Jitter:
                    - binding_site_jitter (float): Std of position jitter [nm] (0 = disabled)

                Rotation:
                    - apply_random_rotation (bool): Whether to apply random 3D rotation

                General:
                    - seed (int): Random seed for reproducibility
        """
        self.config = config
        self.rng = np.random.default_rng(config.get("seed"))

        # Initialize the CCP geometry model
        self.model = SpheroidCapModel(
            surface_area=config.get("surface_area", 20000.0),
            close_angle=config.get("close_angle", 60.0),
            flattening=config.get("flattening", 0.0),
        )

    def generate(self) -> Tuple[np.ndarray, dict]:
        """
        Generate CCP point cloud with all configured error models.

        Returns:
            point_cloud: np.ndarray of shape (N, 3), coordinates in nm centered at origin.
            stats: dict with generation statistics including:
                - num_clathrin_sites: Total potential binding sites
                - labeled_sites: Number of sites that were labeled
                - total_localizations: Total number of points generated
                - surface_area: CCP surface area
                - close_angle: CCP close angle
                - flattening: CCP flattening factor
                - effective_radius: CCP effective radius for collision detection
        """
        # 1. Generate binding sites on the spheroid cap
        num_sites = self.config.get("num_clathrin_sites", 200)
        binding_sites = self.model.get_binding_sites(num_sites, rng=self.rng)

        # 2. Apply spatial exclusion and density of labeling
        labeled_sites = self._apply_labeling(binding_sites)

        if len(labeled_sites) == 0:
            # No labeled sites
            empty_stats = self._get_empty_stats()
            return np.empty((0, 3)), empty_stats

        # 3. Apply binding site jitter (structural heterogeneity)
        jitter_std = self.config.get("binding_site_jitter", 0.0)
        if jitter_std > 0:
            jitter = self.rng.normal(0, jitter_std, size=labeled_sites.shape)
            labeled_sites = labeled_sites + jitter

        # 4. Generate multiple localizations per site (blinking)
        all_points = self._generate_localizations(labeled_sites)

        if len(all_points) == 0:
            empty_stats = self._get_empty_stats()
            return np.empty((0, 3)), empty_stats

        # 5. Apply linker error (antibody arm displacement)
        all_points = self._apply_linker_error(all_points)

        # 6. Apply localization uncertainty
        all_points = self._apply_localization_uncertainty(all_points)

        # 7. Apply random 3D rotation if enabled
        rotation_matrix = np.eye(3)
        if self.config.get("apply_random_rotation", False):
            rotation_matrix = self._random_rotation_matrix()
            all_points = all_points @ rotation_matrix.T

        # Compile statistics
        stats = {
            "num_clathrin_sites": num_sites,
            "labeled_sites": len(labeled_sites),
            "total_localizations": len(all_points),
            "surface_area": self.model.surface_area,
            "close_angle": self.model.close_angle,
            "flattening": self.model.flattening,
            "effective_radius": self.model.get_effective_radius(),
            "height": self.model.get_height(),
            "rim_radius": self.model.get_rim_radius(),
        }

        return all_points, stats

    def _apply_labeling(self, binding_sites: np.ndarray) -> np.ndarray:
        """
        Apply spatial exclusion and density of labeling to select labeled sites.

        Args:
            binding_sites: All potential binding sites, shape (N, 3).

        Returns:
            Selected labeled sites, shape (M, 3) where M <= N.
        """
        use_spatial_exclusion = self.config.get("use_spatial_exclusion", True)
        min_distance = self.config.get("min_labeling_distance", 12.0)
        density = self.config.get("density_of_labeling", 0.6)

        if len(binding_sites) == 0:
            return np.empty((0, 3))

        # Shuffle sites for random selection order
        indices = np.arange(len(binding_sites))
        self.rng.shuffle(indices)
        shuffled_sites = binding_sites[indices]

        if use_spatial_exclusion and min_distance > 0:
            # Apply spatial exclusion: iteratively select sites that are
            # far enough from already-selected sites
            selected_sites = []
            selected_positions = []

            for site in shuffled_sites:
                if len(selected_positions) == 0:
                    # First site is always selected
                    if self.rng.random() < density:
                        selected_sites.append(site)
                        selected_positions.append(site)
                else:
                    # Check distance to all selected sites
                    distances = np.linalg.norm(np.array(selected_positions) - site, axis=1)
                    if np.all(distances >= min_distance):
                        # Site is far enough, apply density filter
                        if self.rng.random() < density:
                            selected_sites.append(site)
                            selected_positions.append(site)

            if len(selected_sites) == 0:
                return np.empty((0, 3))
            return np.array(selected_sites)
        else:
            # No spatial exclusion, just apply density of labeling
            n_to_select = max(1, int(np.round(len(shuffled_sites) * density)))
            return shuffled_sites[:n_to_select]

    def _generate_localizations(self, labeled_sites: np.ndarray) -> np.ndarray:
        """
        Generate multiple localizations per labeled site (blinking simulation).

        Args:
            labeled_sites: Labeled binding sites, shape (N, 3).

        Returns:
            All localization points, shape (M, 3) where M >= N.
        """
        locs_per_site = self.config.get("localizations_per_site", 5)
        distribution = self.config.get("localizations_distribution", "geometric")
        p = self.config.get("localizations_p", 0.3)

        all_points = []

        for site in labeled_sites:
            if distribution == "geometric":
                # Geometric distribution: p is probability of continuing to blink
                # Number of blinks follows geometric distribution
                # Mean = 1 / (1 - p) when p is continuation probability
                # We use locs_per_site as target mean, so we adjust sampling
                n_locs = self.rng.geometric(1 - p)
                # Clip to reasonable range
                n_locs = min(n_locs, locs_per_site * 5)
            else:
                # Constant number of localizations
                n_locs = locs_per_site

            # Repeat site position for each localization
            site_locs = np.tile(site, (n_locs, 1))
            all_points.append(site_locs)

        if len(all_points) == 0:
            return np.empty((0, 3))

        return np.vstack(all_points)

    def _apply_linker_error(self, points: np.ndarray) -> np.ndarray:
        """
        Apply linker (antibody arm) displacement to points.

        Args:
            points: Point coordinates, shape (N, 3).

        Returns:
            Modified point coordinates with linker displacement applied.
        """
        linker_length = self.config.get("linker_length", 0.0)
        if linker_length <= 0:
            return points

        linker_type = self.config.get("linker_type", "normal")
        linker_flexibility = self.config.get("linker_flexibility", 5.0)
        n_points = len(points)

        if linker_type == "normal":
            # Gaussian displacement with flexibility as std dev
            # Use linker_flexibility as the std dev for displacement
            displacement = self.rng.normal(0, linker_flexibility, size=(n_points, 3))
        elif linker_type == "stick":
            # Rigid rod model: fixed length, random direction
            directions = self.rng.normal(0, 1, size=(n_points, 3))
            norms = np.linalg.norm(directions, axis=1, keepdims=True)
            norms = np.where(norms < 1e-10, 1.0, norms)
            directions = directions / norms
            displacement = directions * linker_length
        else:
            raise ValueError(f"Unknown linker_type: '{linker_type}'. Use 'normal' or 'stick'.")

        return points + displacement

    def _apply_localization_uncertainty(self, points: np.ndarray) -> np.ndarray:
        """
        Apply localization uncertainty (photon-limited precision) to points.

        Args:
            points: Point coordinates, shape (N, 3).

        Returns:
            Modified point coordinates with localization noise applied.
        """
        precision_xy = self.config.get("localization_precision_xy", 0.0)
        precision_z = self.config.get("localization_precision_z", 0.0)

        if precision_xy <= 0 and precision_z <= 0:
            return points

        n_points = len(points)
        distribution = self.config.get("localization_precision_distribution", "constant")

        if distribution == "poisson_uniform":
            # Generate per-point precision values using Poisson(3) + Uniform(0,1)
            # Then normalize to achieve the exact target mean
            dist_xy = self.rng.poisson(3, n_points) + self.rng.uniform(0, 1, n_points)
            dist_z = self.rng.poisson(3, n_points) + self.rng.uniform(0, 1, n_points)

            # Normalize by actual mean to achieve target mean exactly
            mean_dist_xy = np.mean(dist_xy)
            mean_dist_z = np.mean(dist_z)

            if mean_dist_xy > 0:
                sigma_xy = precision_xy * (dist_xy / mean_dist_xy)
            else:
                sigma_xy = np.full(n_points, precision_xy)

            if mean_dist_z > 0:
                sigma_z = precision_z * (dist_z / mean_dist_z)
            else:
                sigma_z = np.full(n_points, precision_z)
        else:
            # Constant precision for all points
            sigma_xy = np.full(n_points, precision_xy)
            sigma_z = np.full(n_points, precision_z)

        # Apply localization noise
        noise_x = self.rng.normal(0, 1, n_points) * sigma_xy
        noise_y = self.rng.normal(0, 1, n_points) * sigma_xy
        noise_z = self.rng.normal(0, 1, n_points) * sigma_z

        points_noisy = points.copy()
        points_noisy[:, 0] += noise_x
        points_noisy[:, 1] += noise_y
        points_noisy[:, 2] += noise_z

        return points_noisy

    def _random_rotation_matrix(self) -> np.ndarray:
        """
        Generate a random 3D rotation matrix using uniform random quaternion.

        Returns:
            np.ndarray: 3x3 rotation matrix.
        """
        # Generate random quaternion for uniform random rotation
        u1, u2, u3 = self.rng.random(3)

        q0 = np.sqrt(1 - u1) * np.sin(2 * np.pi * u2)
        q1 = np.sqrt(1 - u1) * np.cos(2 * np.pi * u2)
        q2 = np.sqrt(u1) * np.sin(2 * np.pi * u3)
        q3 = np.sqrt(u1) * np.cos(2 * np.pi * u3)

        # Convert quaternion to rotation matrix
        R = np.array(
            [
                [1 - 2 * (q2 * q2 + q3 * q3), 2 * (q1 * q2 - q0 * q3), 2 * (q1 * q3 + q0 * q2)],
                [2 * (q1 * q2 + q0 * q3), 1 - 2 * (q1 * q1 + q3 * q3), 2 * (q2 * q3 - q0 * q1)],
                [2 * (q1 * q3 - q0 * q2), 2 * (q2 * q3 + q0 * q1), 1 - 2 * (q1 * q1 + q2 * q2)],
            ]
        )

        return R

    def _get_empty_stats(self) -> dict:
        """Get statistics dictionary for empty generation."""
        return {
            "num_clathrin_sites": self.config.get("num_clathrin_sites", 200),
            "labeled_sites": 0,
            "total_localizations": 0,
            "surface_area": self.model.surface_area,
            "close_angle": self.model.close_angle,
            "flattening": self.model.flattening,
            "effective_radius": self.model.get_effective_radius(),
            "height": self.model.get_height(),
            "rim_radius": self.model.get_rim_radius(),
        }

    def get_binding_sites(self) -> np.ndarray:
        """
        Get the raw binding site coordinates (without any noise or labeling).

        Useful for visualization and validation.

        Returns:
            np.ndarray: Shape (N, 3), binding site coordinates in nm.
        """
        num_sites = self.config.get("num_clathrin_sites", 200)
        return self.model.get_binding_sites(num_sites)
