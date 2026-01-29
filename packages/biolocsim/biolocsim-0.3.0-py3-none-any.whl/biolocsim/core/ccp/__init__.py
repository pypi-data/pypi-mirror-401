"""
CCP (Clathrin-Coated Pit) simulation module.

This module provides generators for simulating SMLM point cloud data of:
1. Single Clathrin-Coated Pits (CCPGenerator)
2. Multiple CCPs distributed in a 3D volume (ROICCPGenerator)
"""

from .ccp_generator import CCPGenerator
from .roi_generator import ROICCPGenerator

__all__ = ["CCPGenerator", "ROICCPGenerator"]
