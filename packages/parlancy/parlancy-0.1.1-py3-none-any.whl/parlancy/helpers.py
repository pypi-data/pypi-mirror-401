import subprocess
import sys

def run(command, env=None):
    try:
        subprocess.run(command, check=True, shell=True, env=env)
    except subprocess.CalledProcessError as e:
        print(f"Error executing: {command}")
        sys.exit(1)
