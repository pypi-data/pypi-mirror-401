from __future__ import annotations

from datetime import datetime
import os

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

PROJECT_ROOT = os.environ.get(
    "HOST_PROJECT_ROOT", "/Users/samiegusa/Pet-projects/predict-future-sales"
)
PROJECT_IMAGE = "innowisemlinternshiptemp"

MOUNTS = [
    Mount(source=f"{PROJECT_ROOT}/data", target="/app/data", type="bind"),
    # temp artifacts for the DAG (e.g. small train parquet)
    Mount(source=f"{PROJECT_ROOT}/tmp", target="/app/tmp", type="bind"),
    Mount(source=f"{PROJECT_ROOT}/scripts", target="/app/scripts", type="bind"),
    Mount(source=f"{PROJECT_ROOT}/notebooks", target="/app/notebooks", type="bind"),
    Mount(source=f"{PROJECT_ROOT}/submissions", target="/app/submissions", type="bind"),
    Mount(source=f"{PROJECT_ROOT}/mlflow", target="/app/mlflow", type="bind"),
    Mount(source=f"{PROJECT_ROOT}/.dvc", target="/app/.dvc", type="bind"),
    Mount(
        source=f"{PROJECT_ROOT}/dvc.yaml",
        target="/app/dvc.yaml",
        type="bind",
        read_only=True,
    ),
    Mount(
        source=f"{PROJECT_ROOT}/dvc.lock",
        target="/app/dvc.lock",
        type="bind",
        read_only=True,
    ),
    Mount(
        source=f"{PROJECT_ROOT}/.git", target="/app/.git", type="bind", read_only=True
    ),
]

ENV = {
    "MLFLOW_TRACKING_URI": os.environ.get(
        "MLFLOW_TRACKING_URI", "http://host.docker.internal:5050"
    ),
    "MLFLOW_EXPERIMENT_NAME": os.environ.get(
        "MLFLOW_EXPERIMENT_NAME", "predict_future_sales_v2"
    ),
}

with DAG(
    dag_id="predict_sales_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
) as dag:
    verify_inputs = DockerOperator(
        task_id="verify_inputs",
        image=PROJECT_IMAGE,
        docker_url="unix://var/run/docker.sock",
        auto_remove=True,
        working_dir="/app",
        command=[
            "/app/.venv/bin/python",
            "-c",
            (
                "from pathlib import Path; "
                "paths=["
                "Path('data/processed/sales_monthly_with_features_encoded.parquet'),"
                "Path('data/processed/test_enriched_encoded.parquet')"
                "]; "
                "missing=[str(p) for p in paths if not p.exists()]; "
                "assert not missing, f'Missing inputs: {missing}'; "
                "print('OK: inputs exist')"
            ),
        ],
        environment=ENV,
        mounts=MOUNTS,
        mount_tmp_dir=False,
    )

    prepare_train_subset = DockerOperator(
        task_id="prepare_train_subset",
        image=PROJECT_IMAGE,
        docker_url="unix://var/run/docker.sock",
        auto_remove=True,
        working_dir="/app",
        command=[
            "/app/.venv/bin/python",
            "-c",
            (
                "from pathlib import Path; "
                "import pyarrow.dataset as ds; "
                "import pyarrow.parquet as pq; "
                "src = Path('data/processed/sales_monthly_with_features_encoded.parquet'); "
                "dst_dir = Path('tmp'); dst_dir.mkdir(parents=True, exist_ok=True); "
                "dst = dst_dir / 'train_small.parquet'; "
                "dataset = ds.dataset(str(src), format='parquet'); "
                # Keep a small time window to fit into Docker Desktop RAM.
                # IMPORTANT: feature extraction for target month N uses source month N-1,
                # so we include one extra month (30) to support training on 31..33.
                # We also include months 31-33 so validator can run val/test, and month 33
                # is needed to build production features for month 34.
                "f = (ds.field('date_block_num') >= 30) & (ds.field('date_block_num') <= 33); "
                "table = dataset.to_table(filter=f); "
                "pq.write_table(table, str(dst)); "
                "print(f'Wrote {dst} rows={table.num_rows} cols={table.num_columns}')"
            ),
        ],
        environment=ENV,
        mounts=MOUNTS,
        mount_tmp_dir=False,
    )

    train_and_log = DockerOperator(
        task_id="train_and_log",
        image=PROJECT_IMAGE,
        docker_url="unix://var/run/docker.sock",
        auto_remove=True,
        working_dir="/app",
        command='sh -c "/app/.venv/bin/python scripts/train_single.py --model lightgbm --run-name airflow_train_lightgbm --train-encoded tmp/train_small.parquet --test-encoded data/processed/test_enriched_encoded.parquet --train-start 31 --train-end 31 --val-start 32 --val-end 32 --test-month 33 --production-month 34 --submission-filename airflow_lgbm_submission.csv --no-timestamp --no-score"',
        environment=ENV,
        mounts=MOUNTS,
        mount_tmp_dir=False,
    )

    verify_outputs = DockerOperator(
        task_id="verify_outputs",
        image=PROJECT_IMAGE,
        docker_url="unix://var/run/docker.sock",
        auto_remove=True,
        working_dir="/app",
        command=[
            "/app/.venv/bin/python",
            "-c",
            (
                "from pathlib import Path; "
                "paths=["
                "Path('submissions/airflow_lgbm_submission.csv')"
                "]; "
                "missing=[str(p) for p in paths if not p.exists()]; "
                "assert not missing, f'Missing outputs: {missing}'; "
                "print('OK: outputs exist')"
            ),
        ],
        environment=ENV,
        mounts=MOUNTS,
        mount_tmp_dir=False,
    )

    verify_inputs >> prepare_train_subset >> train_and_log >> verify_outputs
