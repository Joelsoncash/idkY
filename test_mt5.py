import sys
import os
import subprocess
import importlib.util
import traceback

def check_package_installed(package_name):
    """Check if a package is installed"""
    try:
        spec = importlib.util.find_spec(package_name)
        return spec is not None
    except Exception as e:
        return f"Error checking package: {str(e)}"

def get_package_version(package_name):
    """Get the version of an installed package"""
    try:
        import pkg_resources
        return pkg_resources.get_distribution(package_name).version
    except Exception:
        return "Version not found"

def run_diagnostics():
    # Ensure the diagnostics file is in the current directory
    diagnostics_path = os.path.join(os.getcwd(), 'mt5_diagnostics.txt')
    
    with open(diagnostics_path, 'w') as f:
        try:
            # System Information
            f.write("SYSTEM DIAGNOSTICS\n")
            f.write("=" * 50 + "\n")
            f.write(f"Current Working Directory: {os.getcwd()}\n")
            f.write(f"Python version: {sys.version}\n")
            f.write(f"Python executable: {sys.executable}\n")
            f.write(f"Python path: {sys.path}\n\n")

            # Package Checks
            f.write("PACKAGE CHECKS\n")
            f.write("=" * 50 + "\n")
            packages_to_check = ['MetaTrader5', 'pandas', 'numpy']
            for package in packages_to_check:
                try:
                    # Attempt to import the package
                    __import__(package)
                    version = get_package_version(package)
                    f.write(f"{package}: Installed (Version: {version})\n")
                except ImportError:
                    f.write(f"{package}: Not Installed\n")
                except Exception as e:
                    f.write(f"{package}: Error - {str(e)}\n")

            # PIP Packages
            f.write("\nPIP PACKAGES\n")
            f.write("=" * 50 + "\n")
            try:
                pip_list = subprocess.check_output([sys.executable, '-m', 'pip', 'list']).decode('utf-8')
                f.write(pip_list + "\n")
            except Exception as e:
                f.write(f"Error running pip list: {str(e)}\n")

            # MetaTrader5 Specific Diagnostics
            f.write("\nMETATRADER5 DIAGNOSTICS\n")
            f.write("=" * 50 + "\n")
            try:
                import MetaTrader5 as mt5
                
                # Check package details
                f.write(f"MetaTrader5 imported successfully\n")
                f.write(f"Package path: {mt5.__file__}\n")
                
                # Try to get version
                try:
                    f.write(f"Package version: {mt5.__version__}\n")
                except Exception as ver_e:
                    f.write(f"Could not get package version: {str(ver_e)}\n")

                # Attempt to initialize
                try:
                    init_result = mt5.initialize()
                    if init_result:
                        f.write("MT5 initialized successfully\n")
                        f.write(f"MT5 version: {mt5.version()}\n")
                        
                        # Get terminal info
                        terminal_info = mt5.terminal_info()
                        if terminal_info:
                            f.write("\nTerminal Information:\n")
                            for attr, value in terminal_info._asdict().items():
                                f.write(f"{attr}: {value}\n")
                        
                        mt5.shutdown()
                    else:
                        error = mt5.last_error()
                        f.write(f"Failed to initialize MT5. Error code: {error}\n")
                except Exception as init_e:
                    f.write(f"Initialization error: {str(init_e)}\n")
                    f.write(traceback.format_exc())

            except ImportError as import_e:
                f.write(f"Failed to import MetaTrader5: {str(import_e)}\n")
                f.write(traceback.format_exc())
            except Exception as e:
                f.write(f"Unexpected MetaTrader5 error: {str(e)}\n")
                f.write(traceback.format_exc())

        except Exception as critical_e:
            f.write(f"CRITICAL ERROR: {str(critical_e)}\n")
            f.write(traceback.format_exc())

    print(f"Diagnostics written to {diagnostics_path}")

# Run the diagnostics
run_diagnostics()
