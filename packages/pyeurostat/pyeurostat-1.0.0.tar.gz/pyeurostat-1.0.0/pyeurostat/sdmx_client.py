"""
Direct SDMX API Client for EuroStat

This module provides direct access to EuroStat's SDMX API without
depending on external eurostat libraries.
"""

import requests
import xml.etree.ElementTree as ET
from gzip import decompress
import re
from typing import Dict, List, Tuple, Optional, Any
import pandas as pd


class SDMXClient:
    """Client for EuroStat SDMX API."""
    
    BASE_URLS = {
        "EUROSTAT": "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/",
        "COMEXT": "https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/",
    }
    
    XMLSNS = {
        "message": "{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message}",
        "structure": "{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}",
        "common": "{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common}",
    }
    
    def __init__(self, provider: str = "EUROSTAT", timeout: int = 120):
        """
        Initialize SDMX client.
        
        Parameters:
            provider: Data provider (EUROSTAT or COMEXT)
            timeout: Request timeout in seconds
        """
        self.provider = provider
        self.base_url = self.BASE_URLS[provider]
        self.timeout = timeout
        self.session = requests.Session()
    
    def _make_request(self, url: str) -> Optional[requests.Response]:
        """Make HTTP request with error handling."""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None
    
    def get_toc(self) -> List[Dict[str, str]]:
        """
        Get table of contents (catalog) of all available datasets.
        
        Returns:
            List of dictionaries with dataset metadata
        """
        # Use a different endpoint that works better
        url = f"{self.base_url}dataflow/ESTAT?format=SDMX-ML"
        response = self._make_request(url)
        
        if response is None:
            return []
        
        try:
            # Parse XML response
            root = ET.fromstring(response.content)
            results = []
            
            # Find all dataflows
            for dataflow in root.findall('.//{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Dataflow'):
                df_id = dataflow.get('id', '')
                name_elem = dataflow.find('.//{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common}Name')
                name = name_elem.text if name_elem is not None else ''
                
                if df_id:
                    results.append({
                        "code": df_id,
                        "title": name,
                        "type": "dataset",
                        "last_update": "",
                    })
            
            return results
        except Exception as e:
            print(f"Failed to parse TOC: {e}")
            return []
    
    def get_data(
        self,
        dataset_code: str,
        flags: bool = False,
        filter_pars: Optional[Dict[str, Any]] = None,
        verbose: bool = False
    ) -> Optional[List[Tuple]]:
        """
        Download dataset from EuroStat SDMX API.
        
        Parameters:
            dataset_code: Dataset code (e.g., 'DS-059341', 'une_rt_a')
            flags: Include data quality flags
            filter_pars: Dictionary of filter parameters
            verbose: Print progress messages
        
        Returns:
            List of tuples: [header_tuple, data_row1, data_row2, ...]
        """
        filter_pars = filter_pars or {}
        
        # Build URL with query parameters instead of path segments
        # This is more reliable across different datasets
        params = []
        for key, value in filter_pars.items():
            if isinstance(value, list):
                params.append(f"{key}={'+'.join(str(v) for v in value)}")
            else:
                params.append(f"{key}={value}")
        
        param_str = "&".join(params) if params else ""
        
        # Build URL
        url = (
            f"{self.base_url}data/{dataset_code}?"
            f"{param_str}&" if param_str else f"{self.base_url}data/{dataset_code}?"
        ) + "format=TSV&compressed=true"
        
        if verbose:
            print(f"Fetching: {url[:120]}...")
        
        response = self._make_request(url)
        if response is None:
            return None
        
        try:
            # Decompress and parse TSV data
            data = decompress(response.content).decode("utf-8")
            return self._parse_tsv_data(data, flags=flags)
        except Exception as e:
            print(f"Failed to parse data: {e}")
            return None
    
    def _build_filter_string(self, filter_pars: Dict[str, Any]) -> str:
        """Build filter string for SDMX API."""
        if not filter_pars:
            return "?"
        
        # Make a copy to avoid modifying original
        pars = filter_pars.copy()
        
        # Separate time and dimension filters
        start_period = pars.pop("startPeriod", None)
        end_period = pars.pop("endPeriod", None)
        
        # Build dimension filter string
        # SDMX format: /dim1.dim2.dim3/ or /dim1+dim1b.dim2+dim2b/
        dim_filter = ""
        if pars:
            # For trade datasets, typical order is: freq.reporter.partner.product.flow
            # We'll just concatenate what we have
            dim_parts = [str(v) if not isinstance(v, list) else "+".join(str(x) for x in v)
                        for v in pars.values()]
            dim_filter = "/" + ".".join(dim_parts) if dim_parts else ""
        
        # Build time filter
        time_params = []
        if start_period:
            time_params.append(f"startPeriod={start_period}")
        if end_period:
            time_params.append(f"endPeriod={end_period}")
        
        time_filter = "&".join(time_params)
        if time_filter:
            return f"{dim_filter}?{time_filter}&"
        else:
            return f"{dim_filter}?" if dim_filter else "?"
    
    def _parse_tsv_data(self, data: str, flags: bool = False) -> List[Tuple]:
        """
        Parse TSV data from SDMX response.
        
        Parameters:
            data: Raw TSV string
            flags: Whether to include flag columns
        
        Returns:
            List of tuples with header and data rows
        """
        lines = data.split("\r\n")
        if not lines:
            return []
        
        result = []
        first_row = True
        
        for line in lines:
            if not line.strip():
                continue
            
            parts = re.split(r"\t|,", line)
            
            if first_row:
                # Parse header
                first_row = False
                n_text_fields = len(line[:line.find("\t")].split(","))
                
                if flags:
                    # Create header with _value and _flag suffixes
                    header = parts[:n_text_fields] + [
                        x.strip() + suffix
                        for x in parts[n_text_fields:]
                        for suffix in ("_value", "_flag")
                    ]
                else:
                    header = [x.strip() for x in parts]
                
                result.append(tuple(header))
            else:
                # Parse data row
                if parts == ['']:
                    continue
                
                n_text_fields = len(result[0]) - len([x for x in result[0] if any(c.isdigit() for c in str(x))])
                row = parts[:n_text_fields]
                
                # Parse values
                for val_str in parts[n_text_fields:]:
                    val_parts = val_str.strip().split(" ")
                    
                    # Parse value
                    if val_parts[0] in [":", "0n", "n", ""]:
                        value = None
                    else:
                        try:
                            value = float(val_parts[0])
                        except (ValueError, IndexError):
                            value = val_parts[0] if val_parts else None
                    
                    row.append(value)
                    
                    # Parse flag if requested
                    if flags:
                        flag = val_parts[1] if len(val_parts) > 1 else None
                        row.append(flag)
                
                # Ensure row length matches header length
                while len(row) < len(result[0]):
                    row.append(None)
                row = row[:len(result[0])]
                
                result.append(tuple(row))
        
        return result if len(result) > 1 else None
    
    def get_data_df(
        self,
        dataset_code: str,
        flags: bool = False,
        **kwargs
    ) -> Optional[pd.DataFrame]:
        """
        Download dataset and return as pandas DataFrame.
        
        Parameters:
            dataset_code: Dataset code
            flags: Include data quality flags
            **kwargs: Additional parameters (filter_pars, verbose)
        
        Returns:
            pandas DataFrame or None
        """
        data = self.get_data(dataset_code, flags=flags, **kwargs)
        
        if data is None or len(data) < 2:
            return None
        
        # Convert to DataFrame
        header = data[0]
        rows = data[1:]
        
        # Ensure all rows have same length as header
        normalized_rows = []
        for row in rows:
            row_list = list(row)
            while len(row_list) < len(header):
                row_list.append(None)
            normalized_rows.append(row_list[:len(header)])
        
        return pd.DataFrame(normalized_rows, columns=header)
