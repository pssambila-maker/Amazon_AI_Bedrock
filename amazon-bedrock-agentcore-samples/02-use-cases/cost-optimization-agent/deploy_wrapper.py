"""
Wrapper script to run deploy.py with proper UTF-8 encoding on Windows
"""
import sys
import io
import os

# Set UTF-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['PYTHONUTF8'] = '1'

# Now run the actual deploy script
import subprocess
result = subprocess.run(
    [sys.executable, 'deploy.py', '--region', 'us-east-2'],
    cwd=os.path.dirname(os.path.abspath(__file__)),
    env={**os.environ, 'PYTHONIOENCODING': 'utf-8', 'PYTHONUTF8': '1'}
)
sys.exit(result.returncode)
