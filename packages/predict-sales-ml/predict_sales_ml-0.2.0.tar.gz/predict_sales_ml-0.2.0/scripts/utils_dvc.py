"""
Утилиты для работы с DVC и логирования версий данных в MLflow.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any

import mlflow
import yaml


def get_dvc_lock_path() -> Path:
    """Возвращает путь к dvc.lock файлу."""
    return Path("dvc.lock")


def get_dvc_config_path() -> Path:
    """Возвращает путь к конфигурации DVC."""
    return Path(".dvc/config")


def get_git_commit_hash() -> Optional[str]:
    """Получает хеш текущего Git commit."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )
        return result.stdout.strip()
    except (
        subprocess.CalledProcessError,
        FileNotFoundError,
        subprocess.TimeoutExpired,
    ):
        return None


def get_git_branch() -> Optional[str]:
    """Получает текущую Git ветку."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )
        return result.stdout.strip()
    except (
        subprocess.CalledProcessError,
        FileNotFoundError,
        subprocess.TimeoutExpired,
    ):
        return None


def get_dvc_data_version() -> Optional[Dict[str, Any]]:
    """
    Извлекает версию данных из dvc.lock.

    Returns:
        Dict с информацией о версиях:
        {
            'stage': 'process_data',
            'deps': {
                'sales_train.csv': {'md5': '...', 'size': ...},
                ...
            },
            'outs': {
                'sales_monthly_clean.parquet': {'md5': '...', 'size': ...},
                ...
            },
            'lock_hash': '...'  # хеш самого dvc.lock
        }
    """
    lock_path = get_dvc_lock_path()

    if not lock_path.exists():
        return None

    try:
        with open(lock_path, "r", encoding="utf-8") as f:
            lock_data = yaml.safe_load(f)

        # Получаем хеш самого lock файла для отслеживания изменений
        lock_hash = None
        try:
            result = subprocess.run(
                ["git", "hash-object", str(lock_path)],
                capture_output=True,
                text=True,
                check=True,
                timeout=10,
            )
            lock_hash = result.stdout.strip()
        except (
            subprocess.CalledProcessError,
            FileNotFoundError,
            subprocess.TimeoutExpired,
        ):
            pass

        # Извлекаем информацию о стадии process_data
        stages = lock_data.get("stages", {})
        process_stage = stages.get("process_data", {})

        if not process_stage:
            return None

        # Извлекаем deps и outs
        deps = {}
        for dep in process_stage.get("deps", []):
            path = Path(dep["path"])
            deps[path.name] = {
                "md5": dep.get("md5"),
                "size": dep.get("size"),
                "path": str(path),
            }

        outs = {}
        for out in process_stage.get("outs", []):
            path = Path(out["path"])
            outs[path.name] = {
                "md5": out.get("md5"),
                "size": out.get("size"),
                "path": str(path),
            }

        return {
            "stage": "process_data",
            "deps": deps,
            "outs": outs,
            "lock_hash": lock_hash,
        }

    except (yaml.YAMLError, KeyError, IOError) as e:
        print(f"Ошибка при чтении dvc.lock: {e}", file=sys.stderr)
        return None


def get_dvc_config() -> Optional[Dict[str, Any]]:
    """
    Читает конфигурацию DVC из .dvc/config.

    Returns:
        Dict с конфигурацией DVC или None.
    """
    config_path = get_dvc_config_path()

    if not config_path.exists():
        return None

    try:
        config = {}
        current_section = None

        with open(config_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if line.startswith("[") and line.endswith("]"):
                    current_section = line[1:-1]
                    config[current_section] = {}
                elif "=" in line and current_section:
                    key, value = line.split("=", 1)
                    config[current_section][key.strip()] = value.strip()

        return config if config else None

    except IOError as e:
        print(f"Ошибка при чтении .dvc/config: {e}", file=sys.stderr)
        return None


def log_dvc_metadata_to_mlflow(
    log_artifacts: bool = True,
    log_params: bool = True,
    log_tags: bool = True,
) -> None:
    """
    Логирует метаданные DVC в текущий MLflow run.

    Args:
        log_artifacts: Если True, сохраняет dvc.lock и .dvc/config как артефакты
        log_params: Если True, логирует версии данных как параметры
        log_tags: Если True, логирует Git информацию как теги
    """
    active_run = mlflow.active_run()
    if active_run is None:
        print(
            "Предупреждение: нет активного MLflow run. Пропускаем логирование DVC метаданных."
        )
        return

    # Получаем версию данных
    dvc_version = get_dvc_data_version()

    # Получаем Git информацию
    git_commit = get_git_commit_hash()
    git_branch = get_git_branch()

    # Логируем параметры
    if log_params:
        if dvc_version:
            mlflow.log_param(
                "dvc_data_version", dvc_version.get("lock_hash", "unknown")
            )
            mlflow.log_param("dvc_stage", dvc_version.get("stage", "unknown"))

            # Логируем хеши входных данных (deps)
            deps = dvc_version.get("deps", {})
            for filename, info in deps.items():
                if info.get("md5"):
                    mlflow.log_param(
                        f"dvc_dep_{filename}_md5", info["md5"][:16]
                    )  # Первые 16 символов

            # Логируем хеши выходных данных (outs)
            outs = dvc_version.get("outs", {})
            for filename, info in outs.items():
                if info.get("md5"):
                    mlflow.log_param(f"dvc_out_{filename}_md5", info["md5"][:16])

        if git_commit:
            mlflow.log_param("git_commit", git_commit[:16])  # Первые 16 символов

        if git_branch:
            mlflow.log_param("git_branch", git_branch)

    # Логируем теги
    if log_tags:
        if git_commit:
            mlflow.set_tag("git_commit_full", git_commit)
        if git_branch:
            mlflow.set_tag("git_branch", git_branch)
        if dvc_version:
            mlflow.set_tag("dvc_versioned", "true")
        else:
            mlflow.set_tag("dvc_versioned", "false")

    # Логируем артефакты
    if log_artifacts:
        # Сохраняем dvc.lock
        lock_path = get_dvc_lock_path()
        if lock_path.exists():
            mlflow.log_artifact(str(lock_path), artifact_path="dvc")

        # Сохраняем .dvc/config
        config_path = get_dvc_config_path()
        if config_path.exists():
            mlflow.log_artifact(str(config_path), artifact_path="dvc")

        # Сохраняем dvc.yaml
        dvc_yaml_path = Path("dvc.yaml")
        if dvc_yaml_path.exists():
            mlflow.log_artifact(str(dvc_yaml_path), artifact_path="dvc")

        # Сохраняем JSON с полной информацией о версиях
        if dvc_version:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".json", delete=False
            ) as f:
                json.dump(dvc_version, f, indent=2)
                mlflow.log_artifact(f.name, artifact_path="dvc")
                Path(f.name).unlink()  # Удаляем временный файл
