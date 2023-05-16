import subprocess
import sys

try:
    import pandas
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
