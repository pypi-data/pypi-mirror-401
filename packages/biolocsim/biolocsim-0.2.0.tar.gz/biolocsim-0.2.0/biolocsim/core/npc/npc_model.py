"""
NPC geometry model definitions.

This module defines the geometric structure of Nuclear Pore Complexes (NPCs),
including preset NUP configurations and binding site coordinate generation.
"""

import numpy as np


class NPCModel:
    """
    Defines the geometric structure of a Nuclear Pore Complex.

    The NPC is modeled as two concentric rings (cytoplasmic and nuclear)
    with n-fold rotational symmetry (typically 8-fold).

    Attributes:
        n_fold (int): Rotational symmetry of the NPC.
        radius_cr (float): Radius of the cytoplasmic ring in nm.
        radius_nr (float): Radius of the nuclear ring in nm.
        z_offset (float): Z-offset from center plane for each ring in nm.
    """

    # Preset NUP parameters based on literature and MATLAB reference code
    # All values are in nanometers (nm)
    PRESET_NUPS = {
        "nup107": {"radius_cr": 49.0, "radius_nr": 51.0, "z_offset": 30.0},
        "nup133": {"radius_cr": 50.1, "radius_nr": 50.1, "z_offset": 25.0},
        "nup96": {"radius_cr": 54.0, "radius_nr": 51.0, "z_offset": 24.0},
        "nup160": {"radius_cr": 52.5, "radius_nr": 42.5, "z_offset": 25.0},
    }

    def __init__(
        self,
        nup_type: str = "nup107",
        n_fold: int = 8,
        custom_radius_cr: float = None,
        custom_radius_nr: float = None,
        custom_z_offset: float = None,
    ):
        """
        Initialize NPC geometry model.

        Args:
            nup_type: Preset NUP type ("nup107", "nup133", "nup96", "nup160")
                      or "custom" for user-defined parameters.
            n_fold: Rotational symmetry (default 8 for typical NPC).
            custom_radius_cr: Custom cytoplasmic ring radius in nm (used if nup_type="custom").
            custom_radius_nr: Custom nuclear ring radius in nm (used if nup_type="custom").
            custom_z_offset: Custom z-offset from center plane in nm (used if nup_type="custom").

        Raises:
            ValueError: If nup_type is unknown and custom parameters are not provided.
        """
        self.n_fold = n_fold

        if nup_type == "custom":
            if custom_radius_cr is None or custom_radius_nr is None or custom_z_offset is None:
                raise ValueError("Custom NUP type requires custom_radius_cr, custom_radius_nr, and custom_z_offset.")
            self.radius_cr = custom_radius_cr
            self.radius_nr = custom_radius_nr
            self.z_offset = custom_z_offset
        elif nup_type in self.PRESET_NUPS:
            params = self.PRESET_NUPS[nup_type]
            self.radius_cr = params["radius_cr"]
            self.radius_nr = params["radius_nr"]
            self.z_offset = params["z_offset"]
        else:
            raise ValueError(
                f"Unknown NUP type: '{nup_type}'. "
                f"Available presets: {list(self.PRESET_NUPS.keys())} or use 'custom'."
            )

        self.nup_type = nup_type

    def get_binding_sites(self) -> np.ndarray:
        """
        Generate 3D coordinates of all binding sites for the NPC.

        The NPC consists of two rings:
        - Cytoplasmic ring (CR): at z = +z_offset
        - Nuclear ring (NR): at z = -z_offset

        Each ring has n_fold binding sites evenly distributed around the circle.

        Returns:
            np.ndarray: Shape (2 * n_fold, 3), binding site coordinates in nm.
                        First n_fold rows are CR sites, last n_fold rows are NR sites.
        """
        # Generate angles for n-fold symmetry
        # Start at angle offset to match MATLAB convention: angles = (1:n) * (2*pi/n)
        angles = np.linspace(0, 2 * np.pi, self.n_fold, endpoint=False) + (2 * np.pi / self.n_fold)

        # Cytoplasmic ring (positive z)
        cr_x = self.radius_cr * np.cos(angles)
        cr_y = self.radius_cr * np.sin(angles)
        cr_z = np.full(self.n_fold, self.z_offset)
        cr_sites = np.column_stack([cr_x, cr_y, cr_z])

        # Nuclear ring (negative z)
        nr_x = self.radius_nr * np.cos(angles)
        nr_y = self.radius_nr * np.sin(angles)
        nr_z = np.full(self.n_fold, -self.z_offset)
        nr_sites = np.column_stack([nr_x, nr_y, nr_z])

        # Combine both rings
        return np.vstack([cr_sites, nr_sites])

    def get_num_binding_sites(self) -> int:
        """
        Get the total number of binding sites in the NPC.

        Returns:
            int: Total number of binding sites (2 * n_fold).
        """
        return 2 * self.n_fold

    def __repr__(self) -> str:
        return (
            f"NPCModel(nup_type='{self.nup_type}', n_fold={self.n_fold}, "
            f"radius_cr={self.radius_cr}, radius_nr={self.radius_nr}, z_offset={self.z_offset})"
        )
