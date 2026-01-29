"""
Nucleus NPC generator.

This module provides the NucleusGenerator class for generating SMLM point cloud
data of multiple NPCs distributed on a nuclear envelope (ellipsoid surface).
"""

from typing import List, Tuple

import numpy as np
from tqdm.auto import tqdm

from .npc_generator import NPCGenerator


class NucleusGenerator:
    """
    Generates point cloud data for NPCs distributed on a nuclear envelope.

    The nucleus is modeled as an ellipsoid, and NPCs are placed on its surface
    with their axes oriented perpendicular to the surface normal (z-axis of NPC
    aligns with the outward surface normal).

    Attributes:
        config (dict): Configuration dictionary containing all parameters.
        rng (np.random.Generator): Random number generator for reproducibility.
    """

    def __init__(self, config: dict):
        """
        Initialize the nucleus generator with configuration.

        Args:
            config: Configuration dictionary with the following keys:

                Nucleus Geometry:
                    - nucleus_semi_axes (list): [a, b, c] semi-axes of ellipsoid [nm]
                    - nucleus_center (list): [x, y, z] center position [nm]

                NPC Distribution:
                    - num_npcs (int): Number of NPCs to generate
                    - min_npc_spacing (float): Minimum center-to-center distance [nm]
                    - npc_distribution (str): "uniform" or "random"
                    - max_placement_attempts (int): Max attempts to place each NPC

                NPC Configuration:
                    - npc_config (dict): Configuration for individual NPCs (NPCGenerator config)

                Output Options:
                    - include_npc_id (bool): Whether to include NPC instance ID in output

                General:
                    - seed (int): Random seed for reproducibility
                    - verbose (bool): Whether to show progress bar
        """
        self.config = config
        self.rng = np.random.default_rng(config.get("seed"))
        self.verbose = config.get("verbose", False)

        # Extract parameters
        self.semi_axes = np.array(config.get("nucleus_semi_axes", [5000.0, 4000.0, 2500.0]))
        self.center = np.array(config.get("nucleus_center", [0.0, 0.0, 0.0]))
        self.num_npcs = config.get("num_npcs", 100)
        self.min_spacing = config.get("min_npc_spacing", 150.0)
        self.distribution_type = config.get("npc_distribution", "random")
        self.max_attempts = config.get("max_placement_attempts", 1000)
        self.include_npc_id = config.get("include_npc_id", True)

    def generate(self) -> Tuple[np.ndarray, dict]:
        """
        Generate point cloud for all NPCs on nucleus surface.

        Returns:
            point_cloud: np.ndarray of shape (N, 3) or (N, 4) if include_npc_id.
            stats: dict with generation statistics including:
                - requested_npcs: Number of NPCs requested
                - placed_npcs: Number of NPCs successfully placed
                - total_points: Total number of points generated
                - success_rate: Fraction of NPCs successfully placed
        """
        # Place NPCs on the ellipsoid surface
        npc_placements = self._place_npcs_on_surface()

        if not npc_placements:
            # No NPCs could be placed
            empty_points = np.empty((0, 4 if self.include_npc_id else 3))
            stats = {
                "requested_npcs": self.num_npcs,
                "placed_npcs": 0,
                "total_points": 0,
                "success_rate": 0.0,
            }
            return empty_points, stats

        # Generate point cloud for each NPC
        all_points = []
        npc_config = self.config.get("npc_config", {}).copy()

        pbar = tqdm(
            enumerate(npc_placements, start=1),
            total=len(npc_placements),
            desc="Generating NPCs",
            disable=not self.verbose,
        )

        for npc_id, (position, rotation_matrix) in pbar:
            # Create a new seed for each NPC based on the main seed
            npc_config["seed"] = self.rng.integers(0, 2**31)

            # Generate single NPC point cloud
            npc_generator = NPCGenerator(npc_config)
            points, _ = npc_generator.generate()

            if points.size == 0:
                continue

            # Transform points: rotate to align with surface normal, then translate
            transformed_points = points @ rotation_matrix.T + position

            # Add NPC ID if requested
            if self.include_npc_id:
                npc_ids = np.full((len(transformed_points), 1), npc_id)
                transformed_points = np.hstack([transformed_points, npc_ids])

            all_points.append(transformed_points)

        # Combine all points
        if all_points:
            point_cloud = np.vstack(all_points)
        else:
            point_cloud = np.empty((0, 4 if self.include_npc_id else 3))

        # Compile statistics
        stats = {
            "requested_npcs": self.num_npcs,
            "placed_npcs": len(npc_placements),
            "total_points": len(point_cloud),
            "success_rate": len(npc_placements) / self.num_npcs if self.num_npcs > 0 else 0.0,
            "nucleus_semi_axes": self.semi_axes.tolist(),
            "nucleus_center": self.center.tolist(),
        }

        return point_cloud, stats

    def _place_npcs_on_surface(self) -> List[Tuple[np.ndarray, np.ndarray]]:
        """
        Determine positions and orientations of NPCs on the ellipsoid surface.

        Uses the configured distribution type:
        - "uniform": Attempts to distribute NPCs as evenly as possible using
                     Fibonacci spiral method with collision checking
        - "random": Random placement with collision checking

        Returns:
            List of (position, rotation_matrix) tuples for each successfully placed NPC.
        """
        placements = []

        if self.distribution_type == "uniform":
            # Use Fibonacci spiral for more uniform distribution
            candidate_positions = self._fibonacci_ellipsoid_points(self.num_npcs * 3)
        else:
            # Random sampling
            candidate_positions = None

        placed_positions = []
        attempts = 0
        candidate_idx = 0

        pbar = tqdm(
            total=self.num_npcs,
            desc="Placing NPCs",
            disable=not self.verbose,
        )

        while len(placements) < self.num_npcs and attempts < self.max_attempts * self.num_npcs:
            attempts += 1

            # Get candidate position
            if self.distribution_type == "uniform" and candidate_positions is not None:
                if candidate_idx >= len(candidate_positions):
                    # Exhausted candidates, switch to random
                    position = self._sample_random_ellipsoid_point()
                else:
                    position = candidate_positions[candidate_idx]
                    candidate_idx += 1
            else:
                position = self._sample_random_ellipsoid_point()

            # Check minimum spacing constraint
            if self._check_spacing(position, placed_positions):
                # Calculate surface normal and rotation matrix
                normal = self._get_ellipsoid_normal(position)
                rotation_matrix = self._get_rotation_matrix_to_align_z(normal)

                # Apply random rotation around the normal (local z-axis of NPC)
                local_z_rotation = self.rng.uniform(0, 2 * np.pi)
                local_rotation = self._rotation_matrix_z(local_z_rotation)
                rotation_matrix = rotation_matrix @ local_rotation

                # Store placement
                placements.append((position + self.center, rotation_matrix))
                placed_positions.append(position)
                pbar.update(1)

        pbar.close()

        if self.verbose and len(placements) < self.num_npcs:
            print(
                f"Warning: Could only place {len(placements)}/{self.num_npcs} NPCs "
                f"with minimum spacing of {self.min_spacing} nm."
            )

        return placements

    def _sample_random_ellipsoid_point(self) -> np.ndarray:
        """
        Sample a random point on the ellipsoid surface.

        Uses the method of sampling from a unit sphere and scaling.
        Note: This doesn't produce perfectly uniform distribution on the ellipsoid,
        but is a reasonable approximation.

        Returns:
            np.ndarray: Point on the ellipsoid surface (relative to center).
        """
        # Sample uniformly on unit sphere using normal distribution
        u = self.rng.normal(0, 1, 3)
        u = u / np.linalg.norm(u)

        # Scale to ellipsoid
        return u * self.semi_axes

    def _fibonacci_ellipsoid_points(self, n_points: int, shuffle: bool = True) -> np.ndarray:
        """
        Generate approximately uniformly distributed points on ellipsoid using Fibonacci spiral.

        The Fibonacci spiral method generates points that are evenly distributed
        on a sphere surface, which are then scaled to the ellipsoid.

        Args:
            n_points: Number of points to generate.
            shuffle: If True, shuffle the points to avoid bias from sequential
                     placement (which would prefer one hemisphere over another
                     when combined with spacing constraints). Defaults to True.

        Returns:
            np.ndarray: Shape (n_points, 3), points on the ellipsoid surface.
        """
        points = np.zeros((n_points, 3))
        golden_ratio = (1 + np.sqrt(5)) / 2

        for i in range(n_points):
            # Fibonacci spiral on unit sphere
            # theta: azimuthal angle (0 to 2*pi, multiple rotations)
            # phi: polar angle (0 to pi, from north to south pole)
            theta = 2 * np.pi * i / golden_ratio
            phi = np.arccos(1 - 2 * (i + 0.5) / n_points)

            # Spherical to Cartesian
            x = np.sin(phi) * np.cos(theta)
            y = np.sin(phi) * np.sin(theta)
            z = np.cos(phi)

            # Scale to ellipsoid
            points[i] = np.array([x, y, z]) * self.semi_axes

        # Shuffle to avoid placement bias when using with spacing constraints
        if shuffle:
            self.rng.shuffle(points)

        return points

    def _check_spacing(self, position: np.ndarray, placed_positions: List[np.ndarray]) -> bool:
        """
        Check if a position satisfies the minimum spacing constraint.

        Args:
            position: Candidate position to check.
            placed_positions: List of already placed NPC positions.

        Returns:
            True if the position is valid (far enough from all others).
        """
        if not placed_positions:
            return True

        placed_array = np.array(placed_positions)
        distances = np.linalg.norm(placed_array - position, axis=1)
        return np.all(distances >= self.min_spacing)

    def _get_ellipsoid_normal(self, point: np.ndarray) -> np.ndarray:
        """
        Calculate the outward unit normal at a point on the ellipsoid.

        For ellipsoid x²/a² + y²/b² + z²/c² = 1, the gradient (outward normal)
        is proportional to (x/a², y/b², z/c²).

        Args:
            point: Point on the ellipsoid surface (relative to center).

        Returns:
            np.ndarray: Unit normal vector pointing outward.
        """
        # Gradient of ellipsoid equation
        normal = point / (self.semi_axes**2)
        # Normalize
        norm = np.linalg.norm(normal)
        if norm < 1e-10:
            return np.array([0.0, 0.0, 1.0])  # Fallback
        return normal / norm

    def _get_rotation_matrix_to_align_z(self, target_direction: np.ndarray) -> np.ndarray:
        """
        Get rotation matrix that rotates [0, 0, 1] to align with target_direction.

        Uses Rodrigues' rotation formula.

        Args:
            target_direction: Target direction vector (will be normalized).

        Returns:
            np.ndarray: 3x3 rotation matrix.
        """
        z_axis = np.array([0.0, 0.0, 1.0])
        target = target_direction / np.linalg.norm(target_direction)

        # Check if target is already aligned with z-axis
        dot = np.dot(z_axis, target)
        if np.abs(dot - 1.0) < 1e-10:
            return np.eye(3)
        if np.abs(dot + 1.0) < 1e-10:
            # 180-degree rotation around x-axis
            return np.diag([1.0, -1.0, -1.0])

        # Rodrigues' rotation formula
        v = np.cross(z_axis, target)
        s = np.linalg.norm(v)
        c = dot

        # Skew-symmetric cross-product matrix of v
        vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])

        # Rotation matrix
        R = np.eye(3) + vx + vx @ vx * ((1 - c) / (s**2))

        return R

    def _rotation_matrix_z(self, angle: float) -> np.ndarray:
        """
        Create a rotation matrix for rotation around the z-axis.

        Args:
            angle: Rotation angle in radians.

        Returns:
            np.ndarray: 3x3 rotation matrix.
        """
        cos_a = np.cos(angle)
        sin_a = np.sin(angle)
        return np.array([[cos_a, -sin_a, 0], [sin_a, cos_a, 0], [0, 0, 1]])

    def get_nucleus_surface_points(self, n_points: int = 1000) -> np.ndarray:
        """
        Get points on the nucleus surface for visualization.

        Args:
            n_points: Number of points to sample.

        Returns:
            np.ndarray: Shape (n_points, 3), points on the nucleus surface.
        """
        points = self._fibonacci_ellipsoid_points(n_points)
        return points + self.center
