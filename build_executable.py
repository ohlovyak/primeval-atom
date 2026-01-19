#!/usr/bin/env python3
"""
Build script for creating standalone executable of Primeval Atom.
This script can be run locally to test the build process.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def install_dependencies():
    """Install required dependencies for building."""
    print("Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)


def run_tests():
    """Run tests before building."""
    print("Running tests...")
    result = subprocess.run([sys.executable, "-m", "pytest", "--tb=short"])
    if result.returncode != 0:
        print("Tests failed! Aborting build.")
        sys.exit(1)


def build_executable():
    """Build the executable using PyInstaller."""
    print("Building executable...")

    # Clean previous builds
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")

    # Use PyInstaller with --onedir instead of --onefile for better Panda3D compatibility
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onedir",  # Create a directory instead of single file
        "--windowed",  # No console window
        "--name", "PrimevalAtom",
        "--collect-all", "panda3d",
        "--collect-all", "direct",
        "--runtime-hook=panda3d_runtime_hook.py",
        "--exclude-module=tkinter",
        "--exclude-module=unittest",
        "--exclude-module=tests",
        "--exclude-module=pytest",
        "--exclude-module=coverage",
        "--exclude-module=setuptools",
        "--exclude-module=pkg_resources",
        "--clean",
        "main.py"
    ]

    print("Running PyInstaller with command:")
    print(" ".join(cmd))

    result = subprocess.run(cmd, check=True)
    print("Executable built successfully!")


def create_distribution():
    """Create distribution package."""
    print("Creating distribution package...")

    dist_dir = Path("dist")
    if not dist_dir.exists():
        print("No dist directory found!")
        return

    # Create archive based on platform
    if sys.platform.startswith('win'):
        archive_name = "PrimevalAtom-Windows.zip"
        shutil.make_archive("PrimevalAtom-Windows", 'zip', "dist")
    elif sys.platform.startswith('linux'):
        archive_name = "PrimevalAtom-Linux.tar.gz"
        subprocess.run([
            "tar", "-czf", archive_name, "-C", "dist", "."
        ], check=True)
    elif sys.platform.startswith('darwin'):
        archive_name = "PrimevalAtom-macOS.tar.gz"
        subprocess.run([
            "tar", "-czf", archive_name, "-C", "dist", "."
        ], check=True)
    else:
        archive_name = f"PrimevalAtom-{sys.platform}.tar.gz"
        subprocess.run([
            "tar", "-czf", archive_name, "-C", "dist", "."
        ], check=True)

    print(f"Distribution package created: {archive_name}")


def main():
    """Main build process."""
    print("Building Primeval Atom executable...")

    try:
        install_dependencies()
        run_tests()
        build_executable()
        create_distribution()
        print("\nBuild completed successfully!")
        print("Check the 'dist' directory for the executable.")
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nBuild cancelled.")
        sys.exit(1)


if __name__ == "__main__":
    main()