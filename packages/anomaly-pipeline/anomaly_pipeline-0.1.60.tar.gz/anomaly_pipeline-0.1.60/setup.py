from setuptools import setup, find_packages
from pathlib import Path

# 1. Read the README file from the current directory
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="anomaly_pipeline",
    version="0.1.60",
    description="Ensemble framework for detecting outliers in grouped time-series data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    # STOP using find_packages(). List them manually:
    packages=["anomaly_pipeline", "anomaly_pipeline.helpers"],
    include_package_data=True,
    install_requires=[
        "pandas",
        "numpy<2",  # important to avoid _ARRAY_API errors
        "joblib",
        "prophet",
        "scikit-learn",
        "google-cloud-bigquery",
        "google-cloud-storage",
        "statsmodels",
        "plotly",
        "pandas-gbq", 
        "gcsfs",
    ],
    
    # 👇 This is the crucial part you were missing!
    entry_points={
        'console_scripts': [
            # Defines a command 'run_anomaly_pipeline' that executes 
            # the 'main' function inside 'anomaly_pipeline.main' module.
            'run_anomaly_pipeline = anomaly_pipeline.main:timeseries_anomaly_detection',
        ],
    },
    
    # Metadata for PyPI searchability
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires='>=3.8',
)


