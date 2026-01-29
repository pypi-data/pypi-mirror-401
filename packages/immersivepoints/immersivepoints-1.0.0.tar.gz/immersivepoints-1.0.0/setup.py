from setuptools import setup, find_packages

setup(
    name="immersivepoints",
    version="1.0.0",
    description="Render point clouds inline in Jupyter notebooks and in VR",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="ImmersivePoints",
    url="https://github.com/rmeertens/ImmersivePoints",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "numpy",
        "ipython",
    ],
    extras_require={
        "dev": [
            "jupyter",
            "pytest",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    keywords="point cloud, visualization, 3D, VR, jupyter",
)
