# Changelog

All notable changes in this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-01-11

### Added
- DVC integration module (scripts/utils_dvc.py) for data versioning
- DVC pipeline configuration (dvc.yaml) for reproducible data pipelines
- DVC metadata logging to MLflow for experiment tracking
- Version management module (scripts/_version.py) with setuptools-scm support

### Changed
- Enhanced baseline_modeling.py to automatically log DVC metadata to MLflow
- Updated utils_validation.py with DVC support in train_model function
- Updated .gitignore to exclude DVC cache and artifacts

## [0.1.0] - 2026-01-08

### Added
- Basic project structure
- TimeSeriesValidator for time series validation
- BaselineFeatureExtractor for feature extraction
- Support for LightGBM and XGBoost models
- MLflow integration for experiment tracking
- Hyperparameter optimization via Optuna
- Model stacking
- Baseline modeling
- Training pipeline
- Model registry

### Infrastructure
- PyPI package configuration (`pyproject.toml`)
- GitHub Actions for CI/CD
- Docker setup for MLflow tracking server

---

## Types of Changes
- `Added` - new features
- `Changed` - changes to existing features
- `Deprecated` - features that will be removed soon
- `Removed` - removed features
- `Fixed` - bug fixes
- `Security` - security fixes