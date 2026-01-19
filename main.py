import os
import sys

# Configure Panda3D for bundled executable
def configure_panda3d():
    """Configure Panda3D for proper execution in bundled mode."""
    # Set graphics backend based on platform
    if sys.platform.startswith('win'):
        # Windows - prefer OpenGL
        os.environ.setdefault('PANDA_WIN32API', 'wgl')
    elif sys.platform.startswith('linux'):
        # Linux - use OpenGL
        os.environ.setdefault('PANDA_LINUXAPI', 'glx')
    elif sys.platform.startswith('darwin'):
        # macOS - use OpenGL
        os.environ.setdefault('PANDA_OSXAPI', 'cocoa')

    # Force window type
    os.environ.setdefault('window-type', 'onscreen')

    # Set audio to none for bundled executable (avoids audio issues)
    os.environ.setdefault('audio-library-name', 'null')

    # Set model path for bundled resources
    if hasattr(sys, '_MEIPASS'):
        model_path = os.path.join(sys._MEIPASS, 'models')
        if os.path.exists(model_path):
            current_model_path = os.environ.get('model-path', '')
            if current_model_path:
                os.environ['model-path'] = f"{model_path};{current_model_path}"
            else:
                os.environ['model-path'] = model_path

# Configure before importing Panda3D
configure_panda3d()

from bigbang_simulator import BigBangSimulator


if __name__ == "__main__":
    try:
        app = BigBangSimulator()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")  # Keep console open on Windows
