from setuptools import setup
from setuptools.command.install import install
import subprocess
import sys
import os

class PostInstall(install):
    def run(self):
        super().run()
        
        install_script = os.path.join(os.path.dirname(__file__), "install.py")
        if os.path.exists(install_script):
            print("Running install.py to install all extra dependencies...")
            try:
                # use python -m pip to safely install things
                subprocess.check_call([sys.executable, install_script])
            except subprocess.CalledProcessError as e:
                print(f"install.py failed: {e}")
                sys.exit(1)  # fail install if your script fails

setup(
    cmdclass={
        "install": PostInstall
    }
)


