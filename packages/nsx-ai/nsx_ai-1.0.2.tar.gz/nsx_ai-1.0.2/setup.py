import setuptools 

# Read README for the long description on PyPI 
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nsx-ai",  # 📦 Package Name (pip install nsx)
    version="1.0.2",  # 🚀 Current Version (Increment this for upgrades)
    author="Ananya Kumar",
    author_email="ananya8154@gmail.com",
    description="Neuro-Symbolic AI Framework with Agentic Capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ananya868/nsx",  # Repo URL
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/nsx/issues",
        "Documentation": "https://github.com/yourusername/nsx/wiki",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
    ],
    package_dir={"": "src"},  # Tells setup that code is inside 'src'
    packages=setuptools.find_packages(where="src"),  # Auto-finds 'nsai' folder
    python_requires=">=3.8",  # Minimum Python version
    install_requires=[
        "torch>=2.0.0",   # Core Dependency
        "numpy",
        "litellm",        
        # Add other deps here
    ],
)