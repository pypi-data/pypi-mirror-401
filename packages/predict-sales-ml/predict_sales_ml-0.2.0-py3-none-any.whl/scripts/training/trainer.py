import logging
import time
from typing import Optional, Dict, Any, List
import pandas as pd
import mlflow
import mlflow.lightgbm
import mlflow.xgboost

from scripts.models.base import BaseModel
from scripts.utils_validation import TimeSeriesValidator, evaluate_model

import pickle
import tempfile
import os
import traceback

logger = logging.getLogger(__name__)


class ModelTrainer:
    """
    Класс для обучения и оценки моделей с MLflow логированием.

    Инкапсулирует логику обучения, оценки и сохранения моделей,
    работая с моделями через интерфейс BaseModel.
    """

    def __init__(
        self,
        model: BaseModel,
        validator: Optional[TimeSeriesValidator] = None,
        clip_min: float = 0.0,
        clip_max: float = 20.0,
    ):
        """
        Инициализирует ModelTrainer.

        Args:
            model: Модель для обучения (наследник BaseModel)
            validator: Валидатор временных рядов (опционально)
            clip_min, clip_max: Границы для обрезки предсказаний
        """
        self.model = model
        self.validator = validator
        self.clip_min = clip_min
        self.clip_max = clip_max

    def train(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_val: Optional[pd.DataFrame] = None,
        y_val: Optional[pd.Series] = None,
        **fit_kwargs,
    ) -> BaseModel:
        """
        Обучает модель на предоставленных данных.

        Args:
            X_train: Обучающие данные
            y_train: Целевая переменная
            X_val: Валидационные данные (опционально)
            y_val: Целевая переменная для валидации
            **fit_kwargs: Дополнительные параметры для fit()

        Returns:
            Обученная модель
        """
        logger.info(f"Начало обучения модели: {self.model.name}")

        start_time = time.time()

        # Обучаем модель
        self.model.fit(X_train, y_train, X_val=X_val, y_val=y_val, **fit_kwargs)

        elapsed_time = time.time() - start_time
        logger.info(f"Обучение завершено за {elapsed_time:.2f} секунд")

        # Логируем время обучения в MLflow (если есть активный run)
        try:
            mlflow.log_metric("training_time_seconds", float(elapsed_time))
        except Exception:
            pass

        return self.model

    def evaluate(
        self,
        X_val: Optional[pd.DataFrame] = None,
        y_val: Optional[pd.Series] = None,
        X_test: Optional[pd.DataFrame] = None,
        y_test: Optional[pd.Series] = None,
        log_to_mlflow: bool = True,
        metadata_val: Optional[pd.DataFrame] = None,
        metadata_test: Optional[pd.DataFrame] = None,
        run_explainability: bool = False,
        explainability_output_dir: Optional[str] = None,
        max_shap_samples: int = 1000,
    ) -> Dict[str, Any]:
        """
        Оценивает модель на validation и/или test данных.
        Использует evaluate_model из utils_validation для единообразия.

        Args:
            X_val, y_val: Валидационные данные
            X_test, y_test: Тестовые данные
            log_to_mlflow: Логировать метрики в MLflow
            metadata_val: DataFrame с метаданными для validation
            metadata_test: DataFrame с метаданными для test
            run_explainability: Если True, запускает SHAP и error analysis
            explainability_output_dir: Директория для сохранения explainability результатов
            max_shap_samples: Максимальное количество образцов для SHAP

        Returns:
            dict с метриками, feature importance и explainability результатами
        """
        if not self.model.is_trained:
            raise ValueError("Модель не обучена. Вызовите train() перед evaluate()")

        # Получаем feature names из модели
        feature_names = None
        if hasattr(self.model, "feature_names") and self.model.feature_names:
            feature_names = self.model.feature_names
        elif X_val is not None:
            feature_names = list(X_val.columns)
        elif X_test is not None:
            feature_names = list(X_test.columns)

        # Используем модель напрямую (не обертку) для evaluate_model
        model_for_eval = (
            self.model.model
            if hasattr(self.model, "model") and self.model.model is not None
            else self.model
        )

        # Используем evaluate_model из utils_validation
        results = evaluate_model(
            model=model_for_eval,
            X_val=X_val,
            y_val=y_val,
            X_test=X_test,
            y_test=y_test,
            clip_min=self.clip_min,
            clip_max=self.clip_max,
            feature_names=feature_names,
            log_to_mlflow=log_to_mlflow,
            metadata_val=metadata_val,
            metadata_test=metadata_test,
            run_explainability=run_explainability,
            explainability_output_dir=explainability_output_dir,
            max_shap_samples=max_shap_samples,
        )

        return results

    def log_config_to_mlflow(
        self,
        X_train: pd.DataFrame,
        feature_names: Optional[List[str]] = None,
    ):
        """
        Логирует конфигурацию в MLflow.

        Args:
            X_train: Обучающие данные
            feature_names: Список названий фичей (опционально)
        """
        try:
            # Базовая информация о модели
            mlflow.log_param("model_name", self.model.name)
            mlflow.log_param("model_type", self.model.__class__.__name__)
            mlflow.log_param("n_train_samples", int(X_train.shape[0]))
            mlflow.log_param("n_features", int(X_train.shape[1]))

            # Логируем гиперпараметры модели
            for key, value in self.model.params.items():
                try:
                    mlflow.log_param(key, value)
                except Exception:
                    mlflow.log_param(key, str(value))

            # Логируем конфигурацию валидации
            if self.validator is not None:
                mlflow.log_param(
                    "train_months",
                    f"{self.validator.train_months[0]}-{self.validator.train_months[1]}",
                )
                mlflow.log_param(
                    "val_months",
                    f"{self.validator.val_months[0]}-{self.validator.val_months[1]}",
                )
                mlflow.log_param("test_month", int(self.validator.test_month))
                mlflow.log_param(
                    "production_month", int(self.validator.production_month)
                )

            # Логируем best iteration, если доступно
            best_iter = self.model.get_best_iteration()
            if best_iter is not None:
                mlflow.log_param("best_iteration", best_iter)

        except Exception as e:
            logger.warning(f"Не удалось залогировать конфигурацию в MLflow: {e}")

    def save_model_to_mlflow(self, artifact_path: str):
        """
        Сохраняет модель в MLflow.

        Args:
            name: Путь для сохранения модели в MLflow
        """
        if not self.model.is_trained:
            raise RuntimeError("Модель не обучена. Обучите модель перед сохранением.")

        logger.info(f"Сохранение модели {self.model.name} в MLflow...")
        logger.info(f"Tracking URI: {mlflow.get_tracking_uri()}")

        try:
            active_run = mlflow.active_run()
            if active_run:
                logger.info(f"Active run ID: {active_run.info.run_id}")
            else:
                logger.warning("Нет активного MLflow run")

            # Определяем тип модели и используем соответствующий logger
            model_type = self.model.__class__.__name__

            if "LightGBM" in model_type:
                # Для LightGBM моделей используем mlflow.lightgbm
                # Нужно получить sklearn-модель из обертки
                if hasattr(self.model, "model") and self.model.model is not None:
                    mlflow.lightgbm.log_model(
                        self.model.model, artifact_path=artifact_path
                    )
                else:
                    raise RuntimeError("LightGBM модель не инициализирована")

            elif "XGBoost" in model_type:
                # Для XGBoost моделей используем mlflow.xgboost
                if hasattr(self.model, "model") and self.model.model is not None:
                    mlflow.xgboost.log_model(
                        self.model.model, artifact_path=artifact_path
                    )
                else:
                    raise RuntimeError("XGBoost модель не инициализирована")

            elif "Stacking" in model_type:
                # Для stacking моделей сохраняем через pickle или pyfunc
                with tempfile.TemporaryDirectory() as tmpdir:
                    model_path = os.path.join(tmpdir, "model.pkl")
                    with open(model_path, "wb") as f:
                        pickle.dump(self.model, f)
                    mlflow.log_artifacts(tmpdir, artifact_path=artifact_path)

            else:
                # Для других моделей используем generic log_model
                if hasattr(self.model, "model") and self.model.model is not None:
                    mlflow.sklearn.log_model(
                        self.model.model, artifact_path=artifact_path
                    )
                else:
                    with tempfile.TemporaryDirectory() as tmpdir:
                        model_path = os.path.join(tmpdir, "model.pkl")
                        with open(model_path, "wb") as f:
                            pickle.dump(self.model, f)
                        mlflow.log_artifacts(tmpdir, artifact_path=artifact_path)

            logger.info(f"Модель успешно сохранена в MLflow: {artifact_path}")

        except Exception as e:
            logger.warning(f"Не удалось сохранить модель в MLflow: {e}")
            logger.warning(f"Тип ошибки: {type(e).__name__}")
            logger.warning(f"Traceback:\n{traceback.format_exc()}")
            # Не пробрасываем исключение, чтобы не ломать весь pipeline
            # Ошибка сохранения модели не критична для обучения и оценки
