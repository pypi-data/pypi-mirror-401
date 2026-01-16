# mypy: disable-error-code="no-any-return,call-overload"
"""
SciexOndemandReader - RawReader-compatible Sciex WIFF file reader.

This module provides a RawReader-compatible implementation for reading Sciex WIFF files
using only the AnalystDataProvider DLL (no wiff2sqlite dependency).

The SciexOndemandReader class provides the same API as rawreader.RawReader:
- Properties: scans, cache, metadata, method
- Same caching/indexing strategy with cache_start/cache_end indices
- Supports sample_id, mslevel, and cachelevel parameters

Requirements:
- pythonnet (pip install pythonnet)
- Sciex DLLs must be available in the alpharaw ext/sciex directory
"""

import os
import site
import warnings

import numpy as np
import polars as pl

# CLR utilities - lazy loaded
HAS_DOTNET = False
DotNetWiffOps = None
AnalystWiffDataProvider = None
AnalystDataProviderFactory = None
CultureInfo = None
Thread = None
System = None


SCAN_SCHEMA = {
    "scan_id": pl.Int64,
    "rt": pl.Float64,
    "mslevel": pl.Int64,
    "polarity": pl.Utf8,
    "precursor_mz": pl.Float64,
    "precursor_z": pl.Int64,
    "collision_energy": pl.Float64,
    "isolation_lower_mz": pl.Float64,
    "isolation_upper_mz": pl.Float64,
    "cache_start": pl.Int64,
    "cache_end": pl.Int64,
    "fill_time": pl.Float64,
    "cycle_index": pl.Int64,
    "experiment_index": pl.Int64,
}
CACHE_SCHEMA = {
    "mz": pl.Float64,
    "inty": pl.Float32,
}


def _resolve_sciex_ext_dir() -> str:
    for site_dir in site.getsitepackages():
        potential_ext_dir = os.path.join(site_dir, "alpharaw", "ext", "sciex")
        if os.path.exists(potential_ext_dir):
            return potential_ext_dir

    try:
        import alpharaw
    except Exception:
        return ""

    alpharaw_dir = os.path.dirname(alpharaw.__file__)
    ext_dir = os.path.join(alpharaw_dir, "ext", "sciex")
    return ext_dir if os.path.exists(ext_dir) else ""


def _polarity_label(details) -> str:
    if details.Polarity == details.Polarity.Positive:
        return "positive"
    if details.Polarity == details.Polarity.Negative:
        return "negative"
    return ""


def _initialize_dotnet():
    """Lazy initialize .NET dependencies when needed."""
    global HAS_DOTNET
    global DotNetWiffOps, AnalystWiffDataProvider, AnalystDataProviderFactory
    global CultureInfo, Thread, System

    if HAS_DOTNET or DotNetWiffOps is not None:
        return  # Already initialized

    try:
        # require pythonnet, pip install pythonnet on Windows
        import clr

        clr.AddReference("System")

        import System as _System
        from System.Globalization import CultureInfo as _CultureInfo
        from System.Threading import Thread as _Thread

        CultureInfo = _CultureInfo
        Thread = _Thread
        System = _System

        other = CultureInfo("en-US")

        Thread.CurrentThread.CurrentCulture = other
        Thread.CurrentThread.CurrentUICulture = other

        ext_dir = _resolve_sciex_ext_dir()
        if not os.path.exists(ext_dir):
            raise ImportError("Could not find alpharaw ext/sciex directory with DLLs")

        # Add Sciex DLL references
        clr.AddReference(
            os.path.join(ext_dir, "Clearcore2.Data.AnalystDataProvider.dll"),
        )
        clr.AddReference(os.path.join(ext_dir, "Clearcore2.Data.dll"))
        clr.AddReference(os.path.join(ext_dir, "WiffOps4Python.dll"))

        import Clearcore2
        from Clearcore2.Data.AnalystDataProvider import (
            AnalystDataProviderFactory as _AnalystDataProviderFactory,
        )
        from Clearcore2.Data.AnalystDataProvider import (
            AnalystWiffDataProvider as _AnalystWiffDataProvider,
        )
        import WiffOps4Python
        from WiffOps4Python import WiffOps as _DotNetWiffOps

        AnalystDataProviderFactory = _AnalystDataProviderFactory
        AnalystWiffDataProvider = _AnalystWiffDataProvider
        DotNetWiffOps = _DotNetWiffOps

        HAS_DOTNET = True
    except Exception as e:
        # allows to use the rest of the code without clr
        warnings.warn(
            f"Dotnet-based dependencies could not be loaded. Sciex support is disabled. Error: {e}",
            stacklevel=2,
        )
        HAS_DOTNET = False


def dot_net_array_to_np_array(src, dtype: np.dtype = np.float64) -> np.ndarray:
    """Convert .NET array to numpy array."""
    if src is None:
        return np.array([], dtype=dtype)
    return np.asarray(src, dtype=dtype)


class SciexOndemandReader:
    """
    RawReader-compatible Sciex WIFF file reader using AnalystDataProvider DLL.

    This class provides the same API as rawreader.RawReader but only uses the
    AnalystDataProvider DLL without wiff2sqlite dependency. It supports:
    - Multiple sample selection via sample_id
    - MS level filtering via mslevel parameter
    - Selective caching via cachelevel parameter
    - Same data structure with scans and cache DataFrames

    Parameters
    ----------
    file_path : str
        Path to the WIFF or WIFF2 file
    sample_id : int | None, optional
        Sample index to load (0-based). If None, loads the last sample.
    centroid : bool, optional
        Whether to centroid the data (currently not implemented)
    mslevel : list[int] | None, optional
        List of MS levels to load (e.g., [1], [2], [1, 2]). If None, loads all.
    cachelevel : list[int] | None, optional
        List of MS levels to cache spectrum data for. If None, caches all.
    silent : bool, optional
        If True, suppresses warning messages
    keep_k_peaks : int, optional
        Maximum number of peaks to keep per spectrum

    Attributes
    ----------
    scans : pl.DataFrame
        DataFrame with scan metadata including cache_start/cache_end indices
    cache : pl.DataFrame
        DataFrame with flattened peak data (mz, inty columns)
    metadata : dict
        File metadata including creation time, sample count, etc.
    method : dict
        Acquisition method information (empty for AnalystDataProvider)
    params : dict
        Reader initialization parameters
    """

    def __init__(
        self,
        file_path: str,
        sample_id: int | None = None,
        centroid: bool = False,
        mslevel: list[int] | None = None,
        cachelevel: list[int] | None = None,
        silent: bool = False,
        keep_k_peaks: int = 100000,
    ):
        """Initialize the Sciex WIFF file reader."""
        _initialize_dotnet()

        if not HAS_DOTNET:
            raise ValueError(
                "Dotnet-based dependencies are required for reading Sciex files. "
                "Please ensure pythonnet and Sciex DLLs are properly installed.",
            )

        self.file_path = file_path
        self.silent = silent
        self.keep_k_peaks = keep_k_peaks

        # Store parameters
        self.params = {
            "file_path": file_path,
            "sample_id": sample_id,
            "centroid": centroid,
            "mslevel": mslevel,
            "cachelevel": cachelevel,
            "silent": silent,
            "keep_k_peaks": keep_k_peaks,
        }

        if centroid and not silent:
            warnings.warn(
                "Centroiding is not yet implemented for SciexOndemandReader",
                stacklevel=2,
            )

        # Initialize .NET objects
        self._wiffDataProvider = AnalystWiffDataProvider()
        self._wiff_file = AnalystDataProviderFactory.CreateBatch(
            file_path,
            self._wiffDataProvider,
        )

        # Get sample count and resolve sample_id
        self.sample_names = list(self._wiff_file.GetSampleNames())
        self.sample_count = len(self.sample_names)

        if sample_id is None:
            # Default to last sample
            sample_id = self.sample_count - 1
        elif sample_id < 0 or sample_id >= self.sample_count:
            raise ValueError(
                f"sample_id {sample_id} out of range. File contains {self.sample_count} samples.",
            )

        self.sample_id = sample_id
        self.params["sample_id"] = sample_id

        # Load the sample
        self.wiffSample = self._wiff_file.GetSample(self.sample_id)
        self.msSample = self.wiffSample.MassSpectrometerSample

        # Initialize metadata
        self.metadata = {
            "name": str(self.sample_names[self.sample_id]) if self.sample_names else "",
            "created_date": self.wiffSample.Details.AcquisitionDateTime.ToString("O"),
            "acquired": self.wiffSample.Details.AcquisitionDateTime.ToString("O"),
            "sample_type": "dda",  # Assume DDA for now
            "sample_count": self.sample_count,
            "sample_id": self.sample_id,
        }

        # Method information (not available from AnalystDataProvider)
        self.method: dict = {}

        # Load scans and cache
        self._load_scans(mslevel=mslevel, cachelevel=cachelevel)

    def _load_scans(
        self,
        mslevel: list[int] | None = None,
        cachelevel: list[int] | None = None,
    ) -> None:
        """
        Load scan metadata and peak data from the WIFF file.

        Parameters
        ----------
        mslevel : list[int] | None
            MS levels to load. If None, loads all levels.
        cachelevel : list[int] | None
            MS levels to cache peak data for. If None, caches all levels.
        """
        experiment_count = self.msSample.ExperimentCount
        if experiment_count <= 0:
            self.scans = pl.DataFrame(schema=SCAN_SCHEMA)
            self.cache = pl.DataFrame(schema=CACHE_SCHEMA)
            return

        exp_list = [self.msSample.GetMSExperiment(i) for i in range(experiment_count)]
        scan_count = exp_list[0].Details.NumberOfScans

        # Pre-compute experiment metadata with cached method references
        exp_meta = []
        for exp in exp_list:
            details = exp.Details
            polarity = _polarity_label(details)
            swath_center_mz = None
            swath_isolation_window = None
            if details.IsSwath and details.MassRangeInfo.Length > 0:
                swath_center_mz = DotNetWiffOps.get_center_mz(details)
                swath_isolation_window = DotNetWiffOps.get_isolation_window(details)
            # Cache method references to avoid repeated attribute lookup
            exp_meta.append(
                (
                    exp,
                    polarity,
                    swath_center_mz,
                    swath_isolation_window,
                    exp.GetMassSpectrumInfo,  # Cache method reference
                    exp.GetRTFromExperimentCycle,  # Cache method reference
                    exp.GetMassSpectrum,  # Cache method reference
                ),
            )

        # Pre-allocate lists for better performance
        scan_ids: list[int] = []
        rts: list[float] = []
        ms_levels: list[int] = []
        polarities: list[str] = []
        precursor_mzs: list[float | None] = []
        precursor_zs: list[int | None] = []
        collision_energies: list[float | None] = []
        isolation_lower_mzs: list[float | None] = []
        isolation_upper_mzs: list[float | None] = []
        cache_starts: list[int | None] = []
        cache_ends: list[int | None] = []
        fill_times: list[float | None] = []
        cycle_indices: list[int] = []
        experiment_indices: list[int] = []
        all_peak_mz: list[np.ndarray] = []
        all_peak_inty: list[np.ndarray] = []
        current_peak_idx = 0

        # Convert mslevel and cachelevel to sets for O(1) lookup
        mslevel_set = set(mslevel) if mslevel is not None else None
        cachelevel_set = set(cachelevel) if cachelevel is not None else None

        # Cache numpy functions
        np_argpartition = np.argpartition
        np_sort = np.sort
        keep_k = self.keep_k_peaks

        # Track scan_id globally across all experiments and cycles
        scan_id = 0

        for cycle_index in range(scan_count):
            for experiment_index, (
                exp,
                polarity,
                swath_center_mz,
                swath_isolation_window,
                get_spectrum_info,
                get_rt,
                get_spectrum,
            ) in enumerate(exp_meta):
                mass_spectrum_info = get_spectrum_info(cycle_index)
                ms_level = mass_spectrum_info.MSLevel

                # Filter by mslevel if specified (using set for O(1) lookup)
                if mslevel_set is not None and ms_level not in mslevel_set:
                    continue

                # Get retention time (in minutes)
                rt = get_rt(cycle_index)

                # Get precursor information for MS2+
                if ms_level > 1:
                    parent_mz = float(mass_spectrum_info.ParentMZ)
                    center_mz = (
                        swath_center_mz
                        if swath_center_mz is not None and swath_center_mz > 0
                        else parent_mz
                    )
                    isolation_window = (
                        swath_isolation_window
                        if swath_isolation_window is not None
                        and swath_isolation_window > 0
                        else 3.0
                    )

                    precursor_mz = center_mz if center_mz > 0 else None
                    parent_charge = mass_spectrum_info.ParentChargeState
                    precursor_charge = int(parent_charge) if parent_charge > 0 else None
                    collision_energy = float(mass_spectrum_info.CollisionEnergy)
                    if center_mz > 0 and isolation_window > 0:
                        half_window = isolation_window / 2
                        isolation_lower_mz = center_mz - half_window
                        isolation_upper_mz = center_mz + half_window
                    else:
                        isolation_lower_mz = None
                        isolation_upper_mz = None
                else:
                    precursor_mz = None
                    precursor_charge = None
                    collision_energy = None
                    isolation_lower_mz = None
                    isolation_upper_mz = None

                # Determine if we should cache this scan's peaks
                should_cache = cachelevel_set is None or ms_level in cachelevel_set

                cache_start = None
                cache_end = None

                # For MS2+ scans, always check if they're empty (even if not caching)
                # to match RawReader behavior
                mass_spectrum = None
                if ms_level > 1:
                    mass_spectrum = get_spectrum(cycle_index)
                    # Skip empty MS2+ scans (empty DDA placeholders)
                    if mass_spectrum.NumDataPoints <= 0:
                        continue

                # Load spectrum for caching if needed (MS1 or MS2 with caching enabled)
                if should_cache:
                    if mass_spectrum is None:
                        mass_spectrum = get_spectrum(cycle_index)
                    num_points = mass_spectrum.NumDataPoints

                    if num_points > 0:
                        # Extract peak data
                        mz_array = dot_net_array_to_np_array(
                            mass_spectrum.GetActualXValues(),
                        )
                        int_array = dot_net_array_to_np_array(
                            mass_spectrum.GetActualYValues(),
                            dtype=np.float32,
                        )

                        # Keep top K peaks if needed
                        n_peaks = len(mz_array)
                        if n_peaks > keep_k:
                            # Use argpartition for O(n) performance instead of argsort's O(n log n)
                            idxes = np_argpartition(int_array, -keep_k)[-keep_k:]
                            idxes = np_sort(idxes)
                            mz_array = mz_array[idxes]
                            int_array = int_array[idxes]
                            n_peaks = keep_k

                        # Store peak data and indices
                        if n_peaks > 0:
                            cache_start = current_peak_idx
                            cache_end = current_peak_idx + n_peaks
                            current_peak_idx = cache_end

                            all_peak_mz.append(mz_array)
                            all_peak_inty.append(int_array)

                scan_ids.append(scan_id)
                rts.append(rt)
                ms_levels.append(ms_level)
                polarities.append(polarity)
                precursor_mzs.append(precursor_mz)
                precursor_zs.append(precursor_charge)
                collision_energies.append(collision_energy)
                isolation_lower_mzs.append(isolation_lower_mz)
                isolation_upper_mzs.append(isolation_upper_mz)
                cache_starts.append(cache_start)
                cache_ends.append(cache_end)
                fill_times.append(None)
                cycle_indices.append(cycle_index)
                experiment_indices.append(experiment_index)
                scan_id += 1

        # Create scans DataFrame
        if scan_ids:
            self.scans = pl.DataFrame(
                {
                    "scan_id": scan_ids,
                    "rt": rts,
                    "mslevel": ms_levels,
                    "polarity": polarities,
                    "precursor_mz": precursor_mzs,
                    "precursor_z": precursor_zs,
                    "collision_energy": collision_energies,
                    "isolation_lower_mz": isolation_lower_mzs,
                    "isolation_upper_mz": isolation_upper_mzs,
                    "cache_start": cache_starts,
                    "cache_end": cache_ends,
                    "fill_time": fill_times,
                    "cycle_index": cycle_indices,
                    "experiment_index": experiment_indices,
                },
            )
        else:
            self.scans = pl.DataFrame(schema=SCAN_SCHEMA)

        # Create cache DataFrame
        if all_peak_mz:
            self.cache = pl.DataFrame(
                {
                    "mz": pl.Series(
                        np.concatenate(all_peak_mz),
                        dtype=pl.Float64,
                    ),
                    "inty": pl.Series(
                        np.concatenate(all_peak_inty),
                        dtype=pl.Float32,
                    ),
                },
            )
        else:
            # Empty cache
            self.cache = pl.DataFrame(schema=CACHE_SCHEMA)

    def close(self) -> None:
        """Close the file and clean up resources."""
        if hasattr(self, "_wiffDataProvider") and self._wiffDataProvider is not None:
            self._wiffDataProvider.Close()

    def __enter__(self) -> "SciexOndemandReader":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.close()

    def __repr__(self) -> str:
        return (
            f"SciexOndemandReader(file_path='{self.file_path}', "
            f"sample_id={self.sample_id}, scans={len(self.scans)})"
        )


# Convenience function
def load_wiff_file(
    filename: str,
    sample_id: int | None = None,
    mslevel: list[int] | None = None,
    cachelevel: list[int] | None = None,
    **kwargs,
) -> SciexOndemandReader:
    """
    Load a WIFF file and return a SciexOndemandReader object.

    Parameters
    ----------
    filename : str
        Path to the WIFF file
    sample_id : int | None, optional
        Sample index to load. If None, loads the last sample.
    mslevel : list[int] | None, optional
        MS levels to load (e.g., [1], [2], [1, 2]). If None, loads all.
    cachelevel : list[int] | None, optional
        MS levels to cache peak data for. If None, caches all.
    **kwargs
        Additional arguments to pass to SciexOndemandReader constructor

    Returns
    -------
    SciexOndemandReader
        Loaded WIFF data reader
    """
    return SciexOndemandReader(
        filename,
        sample_id=sample_id,
        mslevel=mslevel,
        cachelevel=cachelevel,
        **kwargs,
    )


def get_sample_count(filename: str) -> int:
    """
    Get the number of samples in a WIFF file.

    Parameters
    ----------
    filename : str
        Path to the WIFF file

    Returns
    -------
    int
        Number of samples in the WIFF file
    """
    _initialize_dotnet()

    if not HAS_DOTNET:
        raise ValueError(
            "Dotnet-based dependencies are required for reading Sciex files.",
        )

    wiffDataProvider = AnalystWiffDataProvider()
    try:
        wiff_file = AnalystDataProviderFactory.CreateBatch(
            filename,
            wiffDataProvider,
        )
        sample_names = list(wiff_file.GetSampleNames())
        return len(sample_names)
    finally:
        wiffDataProvider.Close()


def get_sample_names(filename: str) -> list[str]:
    """
    Get the sample names from a WIFF file.

    Parameters
    ----------
    filename : str
        Path to the WIFF file

    Returns
    -------
    list[str]
        List of sample names
    """
    _initialize_dotnet()

    if not HAS_DOTNET:
        raise ValueError(
            "Dotnet-based dependencies are required for reading Sciex files.",
        )

    wiffDataProvider = AnalystWiffDataProvider()
    try:
        wiff_file = AnalystDataProviderFactory.CreateBatch(
            filename,
            wiffDataProvider,
        )
        return list(wiff_file.GetSampleNames())
    finally:
        wiffDataProvider.Close()


# Example usage and testing
if __name__ == "__main__":
    print("SciexOndemandReader - RawReader-compatible Sciex WIFF reader")
    print("Usage example:")
    print("""
    from masster.sample.sciex_v2 import SciexOndemandReader, load_wiff_file

    # Create reader instance
    reader = SciexOndemandReader(
        "path/to/file.wiff",
        sample_id=0,
        mslevel=[1, 2],
        cachelevel=[1]
    )

    # Or use convenience function
    reader = load_wiff_file("path/to/file.wiff", sample_id=0)

    # Access scan and peak data (same API as rawreader.RawReader)
    print(f"Number of scans: {len(reader.scans)}")
    print(f"Number of cached peaks: {len(reader.cache)}")
    print(f"Scan columns: {reader.scans.columns}")

    # Get peaks for first scan
    if len(reader.scans) > 0:
        first_scan = reader.scans.row(0, named=True)
        if first_scan["cache_start"] is not None:
            peaks = reader.cache.slice(
                first_scan["cache_start"],
                first_scan["cache_end"] - first_scan["cache_start"]
            )
            print(f"First scan has {len(peaks)} peaks")

    # Metadata
    print(f"Metadata: {reader.metadata}")

    # Close when done
    reader.close()
    """)

    # Test that the module can be imported and classes instantiated
    try:
        print("\n[OK] Module imported successfully")
        print(f"[OK] Has dotnet support: {HAS_DOTNET}")

        # Test with example WIFF file if available
        example_file = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "test",
            "data",
            "2025_01_14_VW_7600_LpMx_DBS_CID_2min_TOP15_030msecMS1_005msecReac_CE35_DBS-ON_3.wiff",
        )

        if os.path.exists(example_file):
            print(f"\n[OK] Found example WIFF file: {example_file}")
            print("Testing WIFF file loading...")

            # Test loading the example file
            with SciexOndemandReader(example_file, cachelevel=[1]) as reader:
                print("[OK] Successfully loaded WIFF file")
                print(f"  - Sample count: {reader.sample_count}")
                print(f"  - Selected sample: {reader.sample_id}")
                print(f"  - Number of scans: {len(reader.scans)}")
                print(f"  - Number of cached peaks: {len(reader.cache)}")
                print(f"  - Creation time: {reader.metadata.get('created_date')}")
                print(f"  - Scan columns: {reader.scans.columns}")

                # Test getting peaks from first MS1 scan
                ms1_scans = reader.scans.filter(pl.col("mslevel") == 1)
                if len(ms1_scans) > 0:
                    first_ms1 = ms1_scans.row(0, named=True)
                    if (
                        first_ms1["cache_start"] is not None
                        and first_ms1["cache_end"] is not None
                    ):
                        peaks = reader.cache.slice(
                            first_ms1["cache_start"],
                            first_ms1["cache_end"] - first_ms1["cache_start"],
                        )
                        print(f"  - First MS1 scan has {len(peaks)} peaks")
                        if len(peaks) > 0:
                            mz_array = peaks["mz"].to_numpy()
                            inty_array = peaks["inty"].to_numpy()
                            print(
                                f"  - m/z range: {mz_array.min():.2f} - {mz_array.max():.2f}",
                            )
                            print(
                                f"  - Intensity range: {inty_array.min():.0f} - {inty_array.max():.0f}",
                            )
        else:
            print(f"\n[!] Example WIFF file not found at: {example_file}")

    except Exception as e:
        print(f"[X] Error during testing: {e}")
        import traceback

        traceback.print_exc()
