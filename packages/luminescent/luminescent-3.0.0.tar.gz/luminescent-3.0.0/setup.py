from setuptools import setup, find_packages

setup(
    name="luminescent",  # Your package name
    version="3.0.0",  # Your package version
    description="GPU-accelerated fully differentiable FDTD for photonics and RF",
    author="Paul Shen",
    author_email="pxshen@alumni.stanford.edu",
    packages=find_packages(),  # Automatically find your package(s)
    install_requires=[
        "gdsfactory",
        # "pymeshfix",
        "electromagneticpython",
        "sortedcontainers",
        "scikit-rf",
        "opencv-python",
        "femwell",
        "rasterio",
        "rtree",
        "gmsh",
        "manifold3d",
        "pymeshlab==2023.12",
        "pyvista",
        'google-cloud-storage',
        'requests',
        'ImageIO',
    ],
)
# mv ~/anaconda3 ~/anaconda30
# cd luminescent
# /usr/bin/python3 -m build
# twine upload dist/*
# python -m twine upload --repository testpypi dist/*

# pip install gdsfactory pillow pymeshfix electromagneticpython sortedcontainers scikit-rf
#

# python3 -m venv venv
# python3 -m pip install gdsfactory electromagneticpython sortedcontainers scikit-rf opencv-python femwell rasterio rtree gmsh manifold3d pymeshlab pyvista --break-system-packages