from setuptools import setup, find_packages
setup(
    name='non_blocking_ws',
    version='1.0.0',
    author='Mich Arens',
    description='Non Blocking WebSocket',
    packages=find_packages(where='src'),  # Specify the 'src' directory
    package_dir={'': 'src'},              # Specify that packages are in 'src'
    install_requires=[
        'websocket-client>=1.6.1'
        ], # List dependencies here
)