"""
Native library loading for MicroPDF Python bindings.

This module handles finding and loading the native MicroPDF library,
including downloading prebuilt binaries if they're not available.
"""

import os
import platform
import sys
import urllib.request
import tarfile
import tempfile
import shutil
from pathlib import Path
from typing import Optional

# Version from package
try:
    from .version import __version__
except ImportError:
    __version__ = "0.4.0"

# Platform mappings
PLATFORM_MAP = {
    "Linux": "linux",
    "Darwin": "darwin",
    "Windows": "win32",
}

ARCH_MAP = {
    "x86_64": "x64",
    "AMD64": "x64",
    "aarch64": "arm64",
    "arm64": "arm64",
    "i386": "ia32",
    "i686": "ia32",
}

# Library file names by platform
LIB_NAMES = {
    "linux": "libmicropdf.so",
    "darwin": "libmicropdf.dylib",
    "win32": "micropdf.dll",
}


def get_platform_info() -> tuple[str, str]:
    """Get the current platform and architecture."""
    system = platform.system()
    machine = platform.machine()
    
    plat = PLATFORM_MAP.get(system, system.lower())
    arch = ARCH_MAP.get(machine, machine)
    
    return plat, arch


def get_lib_name() -> str:
    """Get the library name for the current platform."""
    plat, _ = get_platform_info()
    return LIB_NAMES.get(plat, "libmicropdf.so")


def find_library() -> Optional[Path]:
    """
    Find the native library.
    
    Search order:
    1. Bundled in package (lib/<platform>-<arch>/)
    2. System library path
    3. MICROPDF_LIB_PATH environment variable
    4. Rust build output (../micropdf-rs/target/release/)
    
    Returns:
        Path to the library, or None if not found.
    """
    plat, arch = get_platform_info()
    lib_name = get_lib_name()
    
    # 1. Check bundled library
    package_dir = Path(__file__).parent
    lib_dir = package_dir / "lib" / f"{plat}-{arch}"
    bundled_path = lib_dir / lib_name
    if bundled_path.exists():
        return bundled_path
    
    # Also check without platform suffix
    simple_lib_dir = package_dir / "lib" / f"{plat}-{arch}"
    if simple_lib_dir.exists():
        for f in simple_lib_dir.iterdir():
            if f.suffix in (".so", ".dylib", ".dll"):
                return f
    
    # 2. Check environment variable
    env_path = os.environ.get("MICROPDF_LIB_PATH")
    if env_path:
        env_lib = Path(env_path)
        if env_lib.exists():
            return env_lib
        env_lib = Path(env_path) / lib_name
        if env_lib.exists():
            return env_lib
    
    # 3. Check Rust build output (development mode)
    rust_target = package_dir.parent.parent.parent / "micropdf-rs" / "target" / "release" / lib_name
    if rust_target.exists():
        return rust_target
    
    # 4. Check system library paths
    if plat == "linux":
        for system_path in ["/usr/local/lib", "/usr/lib", "/lib"]:
            system_lib = Path(system_path) / lib_name
            if system_lib.exists():
                return system_lib
    elif plat == "darwin":
        for system_path in ["/usr/local/lib", "/opt/homebrew/lib"]:
            system_lib = Path(system_path) / lib_name
            if system_lib.exists():
                return system_lib
    
    return None


def download_library() -> Optional[Path]:
    """
    Download the prebuilt library from Bitbucket.
    
    Returns:
        Path to the downloaded library, or None if download failed.
    """
    if os.environ.get("MICROPDF_SKIP_DOWNLOAD", "").lower() in ("1", "true", "yes"):
        print("[micropdf] Skipping download (MICROPDF_SKIP_DOWNLOAD=1)")
        return None
    
    plat, arch = get_platform_info()
    lib_name = get_lib_name()
    
    download_url = f"https://bitbucket.org/lexmata/micropdf/downloads/micropdf-{plat}-{arch}.tar.gz"
    
    package_dir = Path(__file__).parent
    lib_dir = package_dir / "lib" / f"{plat}-{arch}"
    target_path = lib_dir / lib_name
    
    print(f"[micropdf] Downloading native library from {download_url}")
    
    try:
        # Create lib directory
        lib_dir.mkdir(parents=True, exist_ok=True)
        
        # Download to temp file
        with tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False) as tmp:
            tmp_path = Path(tmp.name)
        
        urllib.request.urlretrieve(download_url, tmp_path)
        
        # Extract
        with tarfile.open(tmp_path, "r:gz") as tar:
            # Extract to lib directory parent (archive contains platform dir)
            tar.extractall(lib_dir.parent)
        
        # Cleanup
        tmp_path.unlink()
        
        if target_path.exists():
            print(f"[micropdf] Successfully downloaded library to {target_path}")
            return target_path
        else:
            # Check if extraction put files in a subdirectory
            for f in lib_dir.parent.rglob("*.so"):
                if "micropdf" in f.name:
                    shutil.copy(f, target_path)
                    print(f"[micropdf] Successfully downloaded library to {target_path}")
                    return target_path
            for f in lib_dir.parent.rglob("*.dylib"):
                if "micropdf" in f.name:
                    shutil.copy(f, target_path)
                    print(f"[micropdf] Successfully downloaded library to {target_path}")
                    return target_path
        
        print("[micropdf] Download succeeded but library not found in archive")
        return None
        
    except Exception as e:
        print(f"[micropdf] Failed to download library: {e}")
        return None


def load_library() -> Optional[Path]:
    """
    Load the native MicroPDF library.
    
    This function tries to find the library, and if not found,
    attempts to download it.
    
    Returns:
        Path to the library, or None if not available.
    """
    # Try to find existing library
    lib_path = find_library()
    if lib_path:
        return lib_path
    
    # Try to download
    lib_path = download_library()
    if lib_path:
        return lib_path
    
    print("[micropdf] Warning: Native library not found")
    print("[micropdf] Some functionality may be limited")
    print("[micropdf] Set MICROPDF_LIB_PATH to specify library location")
    print("[micropdf] Or install the Rust library: cargo build --release")
    
    return None


# Module-level library path (set on first access)
_library_path: Optional[Path] = None


def get_library_path() -> Optional[Path]:
    """Get the path to the native library."""
    global _library_path
    if _library_path is None:
        _library_path = load_library()
    return _library_path
