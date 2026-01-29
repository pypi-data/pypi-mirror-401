"""
NPC point cloud generator.

This module provides the NPCGenerator class for generating SMLM point cloud
data of single Nuclear Pore Complexes with realistic error models.
"""

from typing import Tuple

import numpy as np

from .npc_model import NPCModel


class NPCGenerator:
    """
    Generates point cloud data for a single Nuclear Pore Complex.

    This generator creates realistic SMLM point clouds by:
    1. Defining the NPC geometry using NPCModel
    2. Applying partial labeling (density of labeling)
    3. Generating multiple localizations per binding site
    4. Adding various error models:
       - Binding site jitter (structural heterogeneity)
       - Linker error (antibody arm displacement)
       - Localization uncertainty (photon-limited precision)
    5. Optionally applying random z-axis rotation

    Attributes:
        config (dict): Configuration dictionary containing all parameters.
        model (NPCModel): The NPC geometry model.
        rng (np.random.Generator): Random number generator for reproducibility.
    """

    def __init__(self, config: dict):
        """
        Initialize the NPC generator with configuration.

        Args:
            config: Configuration dictionary with the following keys:

                NPC Geometry:
                    - nup_type (str): Preset NUP type ("nup107", "nup133", "nup96", "nup160", "custom")
                    - n_fold (int): Rotational symmetry (default 8)
                    - custom_radius_cr (float): Custom cytoplasmic ring radius [nm]
                    - custom_radius_nr (float): Custom nuclear ring radius [nm]
                    - custom_z_offset (float): Custom z-offset [nm]

                Labeling Parameters:
                    - density_of_labeling (float): Fraction of sites labeled (0-1)
                    - localizations_per_site (int): Number of localizations per binding site

                Localization Uncertainty:
                    - localization_precision_xy (float): Mean precision in XY [nm]
                    - localization_precision_z (float): Mean precision in Z [nm]
                    - localization_precision_distribution (str): "poisson_uniform" or "constant"

                Linker Error:
                    - linker_length (float): Antibody linker length [nm] (0 = disabled)
                    - linker_type (str): "normal" (Gaussian) or "stick" (rigid rod)

                Binding Site Jitter:
                    - binding_site_jitter (float): Std of position jitter [nm] (0 = disabled)

                Rotation:
                    - apply_random_z_rotation (bool): Whether to apply random rotation around z-axis

                General:
                    - seed (int): Random seed for reproducibility
        """
        self.config = config
        self.rng = np.random.default_rng(config.get("seed"))

        # Initialize the NPC model
        self.model = NPCModel(
            nup_type=config.get("nup_type", "nup107"),
            n_fold=config.get("n_fold", 8),
            custom_radius_cr=config.get("custom_radius_cr"),
            custom_radius_nr=config.get("custom_radius_nr"),
            custom_z_offset=config.get("custom_z_offset"),
        )

    def generate(self) -> Tuple[np.ndarray, dict]:
        """
        Generate NPC point cloud with all configured error models.

        Returns:
            point_cloud: np.ndarray of shape (N, 3), coordinates in nm centered at origin.
            stats: dict with generation statistics including:
                - total_binding_sites: Total number of binding sites in NPC
                - labeled_sites: Number of sites that were labeled
                - total_localizations: Total number of points generated
                - rotation_angle: Applied z-axis rotation angle in degrees (0 if disabled)
        """
        # Get base binding site coordinates
        binding_sites = self.model.get_binding_sites()
        n_sites = len(binding_sites)

        # 1. Apply density of labeling (random selection of sites)
        dol = self.config.get("density_of_labeling", 1.0)
        n_labeled = max(1, int(np.round(n_sites * dol)))  # At least 1 site
        labeled_indices = self.rng.choice(n_sites, size=n_labeled, replace=False)
        labeled_sites = binding_sites[labeled_indices].copy()

        # 2. Apply binding site jitter (structural heterogeneity)
        jitter_std = self.config.get("binding_site_jitter", 0.0)
        if jitter_std > 0:
            jitter = self.rng.normal(0, jitter_std, size=labeled_sites.shape)
            labeled_sites = labeled_sites + jitter

        # 3. Generate multiple localizations per site
        locs_per_site = self.config.get("localizations_per_site", 1)
        all_points = np.repeat(labeled_sites, locs_per_site, axis=0)
        n_points = len(all_points)

        # 4. Apply linker error (antibody arm displacement)
        all_points = self._apply_linker_error(all_points)

        # 5. Apply localization uncertainty
        all_points = self._apply_localization_uncertainty(all_points)

        # 6. Apply random z-axis rotation if enabled
        rotation_angle = 0.0
        if self.config.get("apply_random_z_rotation", False):
            rotation_angle = self.rng.uniform(0, 2 * np.pi)
            all_points = self._rotate_around_z(all_points, rotation_angle)

        # Compile statistics
        stats = {
            "total_binding_sites": n_sites,
            "labeled_sites": n_labeled,
            "total_localizations": n_points,
            "rotation_angle_deg": np.degrees(rotation_angle),
            "nup_type": self.model.nup_type,
            "n_fold": self.model.n_fold,
        }

        return all_points, stats

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
        n_points = len(points)

        if linker_type == "normal":
            # Gaussian displacement in each dimension
            # The linker_length is interpreted as the std dev of displacement
            displacement = self.rng.normal(0, linker_length, size=(n_points, 3))
        elif linker_type == "stick":
            # Rigid rod model: fixed length, random direction
            directions = self.rng.normal(0, 1, size=(n_points, 3))
            norms = np.linalg.norm(directions, axis=1, keepdims=True)
            # Avoid division by zero
            norms = np.where(norms < 1e-10, 1.0, norms)
            directions = directions / norms
            displacement = directions * linker_length
        else:
            raise ValueError(f"Unknown linker_type: '{linker_type}'. Use 'normal' or 'stick'.")

        return points + displacement

    def _apply_localization_uncertainty(self, points: np.ndarray) -> np.ndarray:
        """
        Apply localization uncertainty (photon-limited precision) to points.

        The localization precision can vary per-point based on the distribution type:
        - "constant": All points have the same precision
        - "poisson_uniform": Precision varies according to Poisson(3)+Uniform(0,1),
                             normalized to achieve the target mean precision

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
            # This fixes the bias in the original MATLAB implementation
            mean_dist_xy = np.mean(dist_xy)
            mean_dist_z = np.mean(dist_z)

            # Avoid division by zero
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
        # Each point gets noise drawn from N(0, sigma) where sigma varies per point
        noise_x = self.rng.normal(0, 1, n_points) * sigma_xy
        noise_y = self.rng.normal(0, 1, n_points) * sigma_xy
        noise_z = self.rng.normal(0, 1, n_points) * sigma_z

        points_noisy = points.copy()
        points_noisy[:, 0] += noise_x
        points_noisy[:, 1] += noise_y
        points_noisy[:, 2] += noise_z

        return points_noisy

    def _rotate_around_z(self, points: np.ndarray, angle: float) -> np.ndarray:
        """
        Rotate points around the z-axis.

        Args:
            points: Point coordinates, shape (N, 3).
            angle: Rotation angle in radians.

        Returns:
            Rotated point coordinates.
        """
        cos_a = np.cos(angle)
        sin_a = np.sin(angle)

        # Z-axis rotation matrix
        rotation_matrix = np.array([[cos_a, -sin_a, 0], [sin_a, cos_a, 0], [0, 0, 1]])

        return points @ rotation_matrix.T

    def get_binding_sites(self) -> np.ndarray:
        """
        Get the raw binding site coordinates (without any noise or labeling).

        Useful for visualization and validation.

        Returns:
            np.ndarray: Shape (2 * n_fold, 3), binding site coordinates in nm.
        """
        return self.model.get_binding_sites()
