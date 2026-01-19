"""
Runtime hook for PyInstaller to properly configure Panda3D.
This ensures Panda3D can find graphics libraries when bundled.
"""

import os
import sys

# Set up Panda3D configuration before importing panda3d
def setup_panda3d_config():
    """Configure Panda3D for bundled execution."""

    # Set the configuration directory
    if hasattr(sys, '_MEIPASS'):
        # Running in bundled mode
        bundle_dir = sys._MEIPASS

        # Add the bundle directory to Python path first
        if bundle_dir not in sys.path:
            sys.path.insert(0, bundle_dir)

        # Also add the _internal directory where packages are stored
        internal_dir = os.path.join(bundle_dir, '_internal')
        if os.path.exists(internal_dir) and internal_dir not in sys.path:
            sys.path.insert(0, internal_dir)

    # Configure graphics backend based on platform
    if sys.platform.startswith('win'):
        # Windows - try DirectX first, then OpenGL
        os.environ.setdefault('PANDA_WIN32API', 'wgl')
        os.environ.setdefault('load-display', 'pandagl')
    elif sys.platform.startswith('linux'):
        # Linux - use OpenGL
        os.environ.setdefault('PANDA_LINUXAPI', 'glx')
        os.environ.setdefault('load-display', 'pandagl')
    elif sys.platform.startswith('darwin'):
        # macOS - use OpenGL
        os.environ.setdefault('PANDA_OSXAPI', 'cocoa')
        os.environ.setdefault('load-display', 'pandagl')

    # Force window type to be onscreen
    os.environ.setdefault('window-type', 'onscreen')

    # Set model path to bundled resources
    if hasattr(sys, '_MEIPASS'):
        model_path = os.path.join(sys._MEIPASS, '_internal', 'models')
        if os.path.exists(model_path):
            os.environ.setdefault('model-path', model_path)

# Call setup before any panda3d imports
setup_panda3d_config()