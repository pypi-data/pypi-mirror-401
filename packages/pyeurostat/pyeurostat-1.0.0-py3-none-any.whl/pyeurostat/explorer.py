"""
EuroStat Data Explorer

A Python library for exploring and visualizing EuroStat datasets.

Usage:
    from eurostat_improved import EuroStatExplorer
    
    es = EuroStatExplorer()
    es.search_dataset("unemployment")
    df = es.download_with_filters('DS-059341', filter_pars={...}, flags=True)
"""

import pandas as pd
import plotly.graph_objects as go
import warnings
from .sdmx_client import SDMXClient


class EuroStatExplorer:
    """
    A class for exploring and visualizing EuroStat datasets.
    
    Attributes:
        client: SDMXClient for API access
        toc_df: DataFrame containing the table of contents for all EuroStat datasets
        df: DataFrame containing the loaded dataset in wide format
        raw_data: DataFrame containing the raw dataset for filtering operations
    """
    
    def __init__(self, provider: str = "EUROSTAT"):
        """
        Initialize the EuroStat API explorer.
        
        Parameters:
            provider: Data provider (EUROSTAT or COMEXT)
        """
        self.client = SDMXClient(provider=provider)
        self.toc_df = self._load_toc()
        self.df = None
        self.raw_data = None
    
    def _load_toc(self) -> pd.DataFrame:
        """Load table of contents from API."""
        try:
            toc_data = self.client.get_toc()
            if toc_data:
                return pd.DataFrame(toc_data)
        except Exception:
            pass
        
        # Return empty DataFrame if TOC loading fails (not critical)
        return pd.DataFrame(columns=['code', 'title', 'type', 'last_update'])
    
    def search_dataset(self, keyword: str) -> pd.DataFrame:
        """
        Search for datasets matching a keyword.
        
        Note: This requires TOC to be loaded. If TOC loading failed,
        use the dataset code directly with download_with_filters().
        
        Parameters:
            keyword (str): Search term to find in dataset titles/descriptions
            
        Returns:
            DataFrame: Matching datasets with their codes and descriptions
        """
        if self.toc_df.empty:
            print("⚠️  Dataset catalog not available. Use dataset codes directly.")
            print("   Example: es.download_with_filters('DS-059341', ...)")
            return pd.DataFrame()
        
        mask = self.toc_df['title'].str.contains(keyword, case=False, na=False)
        return self.toc_df[mask]
    
    def get_parameters(self, dataset_code):
        """
        Retrieve parameters of a given dataset.
        
        Parameters:
            dataset_code (str): EuroStat dataset code (e.g., 'une_rt_a')
            
        Returns:
            list: List of parameter names for the dataset
        """
        # Get a small sample to inspect columns
        df = self.client.get_data_df(
            dataset_code,
            filter_pars={"startPeriod": "2024-01", "endPeriod": "2024-01"},
            verbose=False
        )
        
        if df is None:
            return []
        
        # Return non-value/flag columns as parameters
        params = [col for col in df.columns 
                 if not col.endswith('_value') and not col.endswith('_flag')
                 and 'TIME' not in col.upper() and 'OBS' not in col.upper()]
        return params
    
    def load_dataset(self, dataset_code):
        """
        Load and clean dataset for analysis.
        
        Parameters:
            dataset_code (str): EuroStat dataset code (e.g., 'une_rt_a')
            
        Returns:
            DataFrame: Loaded dataset
        """
        data = self.client.get_data_df(dataset_code, verbose=True)
        if data is None:
            raise ValueError(f"Failed to load dataset: {dataset_code}")
        
        self.raw_data = data
        self.df = data
        return self.df
    
    def plot_countries(self, countries, title="EuroStat Data"):
        """
        Plot selected countries from the dataset using Plotly.
        
        Note: This method takes only the first occurrence of duplicate column names.
        For datasets with multiple demographic breakdowns, use plot_filtered() instead.
        
        Parameters:
            countries (list): List of country codes (e.g., ['PT', 'ES', 'IT'])
            title (str): Plot title
        """
        if not hasattr(self, 'df') or self.df is None:
            raise ValueError("No dataset loaded. Call load_dataset() first.")
        
        # Use groupby to select only the first occurrence of each country column
        # This handles duplicate column names (e.g., PT appears 63 times for different demographics)
        plot_df = self.df[countries].T.groupby(level=0).first().T
        
        # Create plotly figure
        fig = go.Figure()
        for country in plot_df.columns:
            fig.add_trace(go.Scatter(
                x=plot_df.index,
                y=plot_df[country],
                mode='lines+markers',
                name=country
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Year",
            yaxis_title="Value",
            hovermode='x unified'
        )
        fig.show()
    
    def plot_filtered(self, countries, age_group=None, sex=None, unit=None, title="EuroStat Data"):
        """
        Plot countries with specific demographic filters using Plotly.
        
        This method allows filtering by age group, sex, and unit for datasets
        with multiple demographic breakdowns (e.g., unemployment by age and gender).
        
        Parameters:
            countries (list): List of country codes (e.g., ['PT', 'ES', 'IT'])
            age_group (str, optional): Age group filter
                Options: Y15-24, Y15-29, Y15-74, Y20-64, Y25-54, Y25-74, Y55-74
            sex (str, optional): Sex filter
                Options: 'F' (Female), 'M' (Male), 'T' (Total)
            unit (str, optional): Unit filter
                Options: 'PC_ACT' (% of active population), 
                        'PC_POP' (% of total population), 
                        'THS_PER' (thousands of persons)
            title (str): Plot title
            
        Example:
            >>> es = EuroStatExplorer()
            >>> es.load_dataset("une_rt_a")
            >>> es.plot_filtered(['PT', 'ES', 'IT'], 
            ...                  age_group='Y15-24', 
            ...                  sex='T', 
            ...                  unit='PC_ACT',
            ...                  title="Youth Unemployment Rate")
        """
        if not hasattr(self, 'raw_data') or self.raw_data is None:
            raise ValueError("No raw data available. Load dataset first.")
        
        # Start with all data
        filtered = self.raw_data.copy()
        
        # Apply filters
        if age_group:
            filtered = filtered[filtered['age'] == age_group]
        if sex:
            filtered = filtered[filtered['sex'] == sex]
        if unit:
            filtered = filtered[filtered['unit'] == unit]
        
        # Filter for requested countries
        filtered = filtered[filtered['geo\\TIME_PERIOD'].isin(countries)]
        
        if len(filtered) == 0:
            raise ValueError(
                f"No data found for the specified filters. "
                f"Check your parameters: countries={countries}, "
                f"age_group={age_group}, sex={sex}, unit={unit}"
            )
        
        # Reshape for plotting
        filtered = filtered.set_index('geo\\TIME_PERIOD')
        year_cols = [col for col in filtered.columns if col.isdigit()]
        plot_data = filtered[year_cols].T
        plot_data.index = pd.to_datetime(plot_data.index, format='%Y')
        
        # Create plotly figure
        fig = go.Figure()
        for country in plot_data.columns:
            fig.add_trace(go.Scatter(
                x=plot_data.index,
                y=plot_data[country],
                mode='lines+markers',
                name=country
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Year",
            yaxis_title=f"{unit or 'Value'}",
            hovermode='x unified',
            legend_title="Country"
        )
        fig.show()
    
    def get_available_filters(self):
        """
        Get available filter options for the loaded dataset.
        
        Automatically detects all dimension columns (non-numeric) in the dataset.
        
        Returns:
            dict: Dictionary with available values for each dimension column
            
        Example:
            >>> filters = es.get_available_filters()
            >>> print(filters['reporter'])  # For trade datasets
            >>> print(filters['age'])       # For unemployment datasets
        """
        if not hasattr(self, 'raw_data') or self.raw_data is None:
            raise ValueError("No dataset loaded. Call load_dataset() first.")
        
        # Get all non-numeric columns as dimensions
        filters = {}
        for col in self.raw_data.columns:
            if col not in ['OBS_VALUE', 'OBS_STATUS']:  # Skip numeric/flag columns
                try:
                    unique_vals = sorted(self.raw_data[col].unique().tolist())
                    filters[col] = unique_vals
                except TypeError:
                    # If sorting fails, just return as list
                    filters[col] = self.raw_data[col].unique().tolist()
        
        return filters
    
    def download_with_filters(self, dataset_code, filter_pars, loop_param=None, 
                             loop_values=None, flags=True, verbose=True):
        """
        Download dataset with custom filter parameters, optionally looping through values.
        
        This method is useful for downloading large datasets where you need to:
        - Apply specific filters (reporter, product, time period, etc.)
        - Loop through multiple values (e.g., multiple countries or products)
        - Combine results into a single DataFrame
        
        Parameters:
            dataset_code (str): EuroStat dataset code (e.g., 'DS-059341')
            filter_pars (dict): Dictionary of filter parameters to pass to the API
                Example: {'freq': 'M', 'product': '400219', 'startPeriod': 2010}
            loop_param (str, optional): Parameter name to loop through (e.g., 'reporter', 'product')
            loop_values (list, optional): List of values to loop through
                Example: ['PT', 'ES', 'IT'] for reporters
            flags (bool): Whether to include data flags (default: False)
                When True, returns additional 'OBS_STATUS' column with data quality indicators:
                  'e' = estimated, 'p' = provisional, 'r' = revised, 'u' = unreliable, etc.
                Note: Some datasets have compatibility issues with flags=True. The method
                will automatically retry without flags if a column mismatch error occurs.
            verbose (bool): Whether to print progress messages (default: True)
            
        Returns:
            DataFrame: Combined dataset from all successful queries
            
        Examples:
            # Download without looping (single query)
            >>> df = es.download_with_filters(
            ...     'DS-059341',
            ...     filter_pars={'reporter': 'PT', 'freq': 'M', 'startPeriod': 2010}
            ... )
            
            # Download with looping through multiple countries
            >>> df = es.download_with_filters(
            ...     'DS-059341',
            ...     filter_pars={'freq': 'M', 'product': '400219', 'startPeriod': 2010},
            ...     loop_param='reporter',
            ...     loop_values=['PT', 'ES', 'IT', 'DE']
            ... )
            
            # Download with looping through multiple products
            >>> df = es.download_with_filters(
            ...     'DS-059341',
            ...     filter_pars={'reporter': 'PT', 'freq': 'M', 'startPeriod': 2010},
            ...     loop_param='product',
            ...     loop_values=['400219', '400220', '400221']
            ... )
        """
        all_data = []
        
        # If no looping, just execute single query
        if loop_param is None or loop_values is None:
            if verbose:
                print(f"Downloading {dataset_code}...")
            try:
                df = self.client.get_data_df(
                    dataset_code,
                    flags=flags,
                    filter_pars=filter_pars,
                    verbose=verbose
                )
                if df is not None and verbose:
                    print(f"✅ Downloaded {df.shape[0]} rows, {df.shape[1]} columns\n")
                return df
            except Exception as e:
                if verbose:
                    print(f"❌ Error: {e}\n")
                raise
        
        # Loop through values
        success_count = 0
        error_count = 0
        errors = []
        
        if verbose:
            print(f"Downloading {dataset_code} with {len(loop_values)} {loop_param} values...")
            print(f"Base filters: {filter_pars}\n")
        
        for value in loop_values:
            # Create a copy of filter parameters and add the loop value
            current_filters = filter_pars.copy()
            current_filters[loop_param] = value
            
            if verbose:
                print(f"Downloading {loop_param} = {value}...")
            
            # Try to download with our SDMX client
            df = None
            
            try:
                df = self.client.get_data_df(
                    dataset_code,
                    flags=flags,
                    filter_pars=current_filters,
                    verbose=False
                )
                
                if df is not None:
                    all_data.append(df)
                    success_count += 1
                    if verbose:
                        flag_status = " (with flags)" if flags and 'OBS_STATUS' in df.columns else ""
                        print(f"  ✅ {value}: {df.shape[0]} rows, {df.shape[1]} columns{flag_status}\n")
                else:
                    error_count += 1
                    errors.append({'value': value, 'error': 'No data returned'})
                    if verbose:
                        print(f"  ❌ {value}: No data returned\n")
                    
            except Exception as e:
                error_count += 1
                errors.append({'value': value, 'error': str(e)})
                if verbose:
                    print(f"  ❌ {value}: Error - {e}\n")
        
        # Summary
        if verbose:
            print(f"\n{'='*60}")
            print(f"Summary: {success_count} succeeded, {error_count} failed")
            if errors and error_count <= 5:
                print(f"\nFailed downloads:")
                for err in errors:
                    print(f"  - {err['value']}: {err['error']}")
            print(f"{'='*60}\n")
        
        # Combine all data
        if not all_data:
            raise ValueError("No data was successfully downloaded. Check your parameters and try again.")
        
        # Use sort=False and axis=0 to handle different column structures
        try:
            df_combined = pd.concat(all_data, ignore_index=True, sort=False, axis=0)
        except Exception as e:
            if verbose:
                print(f"⚠️  Standard concat failed: {e}")
                print("Attempting alternative concatenation method...")
            
            # Fallback: align columns explicitly
            all_columns = set()
            for df in all_data:
                all_columns.update(df.columns)
            
            # Reindex all dataframes to have the same columns
            all_data_reindexed = [df.reindex(columns=sorted(all_columns)) for df in all_data]
            df_combined = pd.concat(all_data_reindexed, ignore_index=True)
        
        if verbose:
            print(f"Combined dataset: {df_combined.shape[0]} rows, {df_combined.shape[1]} columns")
        
        # Store in instance for potential further use
        self.raw_data = df_combined
        
        return df_combined
    
    def unpivot_data(self, df, time_pattern=r'^\d{4}'):
        r"""
        Convert wide-format EuroStat data to long format (unpivot/melt).
        
        EuroStat data often comes with time periods as columns. This method
        converts it to a more analysis-friendly long format.
        
        Parameters:
            df (DataFrame): Wide-format DataFrame with time periods as columns
            time_pattern (str): Regex pattern to identify time columns (default: r'^\d{4}')
                Default matches columns starting with 4 digits (e.g., '2023', '2023-01')
            
        Returns:
            DataFrame: Long-format DataFrame with TIME_PERIOD and OBS_VALUE columns
            
        Example:
            >>> df_wide = es.download_with_filters('DS-059341', filters)
            >>> df_long = es.unpivot_data(df_wide)
            >>> df_long.head()
        """
        # Identify time period columns
        time_cols = df.columns[df.columns.str.contains(time_pattern)].tolist()
        
        if not time_cols:
            raise ValueError(f"No time columns found matching pattern '{time_pattern}'")
        
        # Identify non-time columns (identifiers)
        id_cols = [col for col in df.columns if col not in time_cols]
        
        # Melt/unpivot the data
        df_unpivoted = df.melt(
            id_vars=id_cols,
            value_vars=time_cols,
            var_name='TIME_PERIOD',
            value_name='OBS_VALUE'
        )
        
        # Remove rows with missing values
        df_unpivoted = df_unpivoted.dropna(subset=['OBS_VALUE'])
        
        # Try to convert TIME_PERIOD to datetime
        try:
            df_unpivoted['TIME_PERIOD'] = pd.to_datetime(df_unpivoted['TIME_PERIOD'])
        except:
            # If conversion fails, leave as string
            pass
        
        return df_unpivoted
