from pathlib import Path
from setuptools import setup, find_packages

this_dir = Path(__file__).parent
readme_path = this_dir / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="kafal",
    version="1.0.0",
    author="Janmay Joshi",
    author_email="codejanmay@gmail.com",
    description="Embeddable DSL for trading quant models, research factors, and backtesting.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/janmayjoshiii/kafal-DSL",  
    packages=find_packages(exclude=("tests", "examples", "installer", "build", "dist")),
    python_requires=">=3.10",
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.21.0",
    ],
    license="KAFAL License 1.0 (Proprietary)",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Development Status :: 3 - Alpha",
    ],
    include_package_data=True,
    zip_safe=False,
)
