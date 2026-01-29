"""
pyeurostat - Modern Python client for EuroStat data

A standalone SDMX client for accessing EuroStat datasets with proper flag handling.

Main Features:
- Direct SDMX 2.1 API implementation
- Fixed flags=True bug from original eurostat library
- Enhanced data exploration with EuroStatExplorer class
- Automatic retry mechanisms for API failures
- Improved data filtering and visualization
- Support for both EuroStat and Comext endpoints

Usage:
    from pyeurostat import EuroStatExplorer
    
    # Initialize explorer
    es = EuroStatExplorer()
    
    # Download with filters and automatic flag handling
    df = es.download_with_filters(
        "une_rt_a",
        filter_pars={'geo': 'PT', 'age': 'TOTAL'},
        flags=True  # Now works correctly!
    )
"""

from .explorer import EuroStatExplorer

__version__ = "1.0.0"
__author__ = "onerafaz"

__all__ = ["EuroStatExplorer"]
