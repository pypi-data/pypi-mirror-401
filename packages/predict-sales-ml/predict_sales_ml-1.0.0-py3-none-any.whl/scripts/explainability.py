"""
Модуль для explainability и error analysis моделей.

Содержит функции для:
- SHAP values анализа (для tree-based моделей)
- Анализ ошибок модели (error analysis)
- Визуализация результатов
"""

import pandas as pd
import numpy as np
import shap
import mlflow
import matplotlib
import matplotlib.pyplot as plt
from scipy import stats
from typing import Optional, Dict, Any
from pathlib import Path

matplotlib.use("Agg")


def calculate_shap_values(
    model,
    X: pd.DataFrame,
    max_samples: int = 1000,
    tree_explainer: bool = True,
) -> Optional[Dict[str, Any]]:
    """
    Вычисляет SHAP values для tree-based модели.

    Args:
        model: Обученная tree-based модель (LightGBM, XGBoost, etc.)
        X: DataFrame с фичами для объяснения
        max_samples: Максимальное количество образцов для объяснения
                    (для ускорения вычислений)
        tree_explainer: Если True, использует TreeExplainer (быстрее для tree моделей)

    Returns:
        dict с SHAP values и explainer объектом, или None если SHAP недоступен
    """
    if len(X) > max_samples:
        print(f"Ограничение выборки для SHAP: {len(X)} -> {max_samples} образцов")
        X_sample = X.sample(n=max_samples, random_state=42)
    else:
        X_sample = X.copy()

    X_sample_clean = X_sample.fillna(0)

    try:
        if tree_explainer:
            explainer = shap.TreeExplainer(model)
        else:
            explainer = shap.KernelExplainer(model.predict, X_sample_clean.iloc[:100])

        print("Вычисление SHAP values...")
        shap_values = explainer.shap_values(X_sample_clean)

        return {
            "shap_values": shap_values,
            "explainer": explainer,
            "X_sample": X_sample_clean,
            "feature_names": list(X_sample_clean.columns),
        }
    except Exception as e:
        print(f"Ошибка при вычислении SHAP values: {e}")
        return None


def plot_shap_summary(
    shap_result: Dict[str, Any],
    output_path: Optional[Path] = None,
    max_display: int = 20,
    show: bool = True,
) -> Optional[Path]:
    """
    Создаёт SHAP summary plot (bar plot важности фичей).

    Args:
        shap_result: Результат calculate_shap_values()
        output_path: Путь для сохранения графика (опционально)
        max_display: Максимальное количество фичей для отображения
        show: Показывать ли график

    Returns:
        Path к сохранённому файлу или None
    """
    if shap_result is None:
        print("SHAP result is None. Не удалось создать summary plot.")
        return None

    shap_values = shap_result["shap_values"]
    X_sample = shap_result["X_sample"]

    try:
        plt.figure(figsize=(10, max(8, max_display * 0.4)))
        shap.summary_plot(
            shap_values,
            X_sample,
            plot_type="bar",
            max_display=max_display,
            show=False,
        )
        plt.tight_layout()

        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(output_path, dpi=150, bbox_inches="tight")
            print(f"SHAP summary plot сохранён: {output_path}")
            if not show:
                plt.close()
            return output_path

        if show:
            plt.show()
        else:
            plt.close()

        return None
    except Exception as e:
        print(f"Ошибка при создании SHAP summary plot: {e}")
        return None


def plot_shap_waterfall(
    shap_result: Dict[str, Any],
    sample_idx: int = 0,
    output_path: Optional[Path] = None,
    show: bool = True,
) -> Optional[Path]:
    """
    Создаёт SHAP waterfall plot для отдельного предсказания.

    Args:
        shap_result: Результат calculate_shap_values()
        sample_idx: Индекс образца для объяснения
        output_path: Путь для сохранения графика (опционально)
        show: Показывать ли график

    Returns:
        Path к сохранённому файлу или None
    """
    if shap_result is None:
        print("SHAP result is None. Не удалось создать waterfall plot.")
        return None

    shap_values = shap_result["shap_values"]
    explainer = shap_result["explainer"]
    X_sample = shap_result["X_sample"]

    try:
        if isinstance(shap_values, list):
            shap_values_sample = shap_values[0][sample_idx]
        else:
            shap_values_sample = shap_values[sample_idx]

        base_value = explainer.expected_value
        if isinstance(base_value, (list, np.ndarray)):
            base_value = base_value[0]

        explanation = shap.Explanation(
            values=shap_values_sample,
            base_values=base_value,
            data=X_sample.iloc[sample_idx].values,
            feature_names=X_sample.columns.tolist(),
        )

        plt.figure(figsize=(10, 8))
        shap.waterfall_plot(explanation, show=False)
        plt.tight_layout()

        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(output_path, dpi=150, bbox_inches="tight")
            print(f"SHAP waterfall plot сохранён: {output_path}")
            if not show:
                plt.close()
            return output_path

        if show:
            plt.show()
        else:
            plt.close()

        return None
    except Exception as e:
        print(f"Ошибка при создании SHAP waterfall plot: {e}")
        return None


def analyze_errors(
    y_true: pd.Series,
    y_pred: pd.Series,
    X: Optional[pd.DataFrame] = None,
    metadata: Optional[pd.DataFrame] = None,
    clip_min: float = 0.0,
    clip_max: float = 20.0,
) -> Dict[str, Any]:
    """
    Анализирует ошибки модели (residuals analysis).

    Args:
        y_true: Реальные значения
        y_pred: Предсказанные значения
        X: DataFrame с фичами (для анализа корреляции с ошибками)
        metadata: DataFrame с метаданными (shop_id, item_id, date_block_num, etc.)
        clip_min, clip_max: Границы для обрезки предсказаний

    Returns:
        dict с результатами анализа ошибок
    """
    y_pred_clipped = np.clip(y_pred, clip_min, clip_max)

    residuals = y_true - y_pred_clipped
    absolute_errors = np.abs(residuals)
    squared_errors = residuals**2

    results = {
        "residuals": residuals,
        "absolute_errors": absolute_errors,
        "squared_errors": squared_errors,
        "rmse": np.sqrt(squared_errors.mean()),
        "mae": absolute_errors.mean(),
        "error_stats": {
            "mean": float(residuals.mean()),
            "std": float(residuals.std()),
            "min": float(residuals.min()),
            "max": float(residuals.max()),
            "median": float(residuals.median()),
        },
    }

    # Анализ по магазинам (если доступны метаданные)
    if metadata is not None and "shop_id" in metadata.columns:
        shop_errors = metadata.copy()
        shop_errors["residual"] = residuals.values
        shop_errors["abs_error"] = absolute_errors.values

        shop_error_summary = (
            shop_errors.groupby("shop_id")["abs_error"]
            .agg(["mean", "std", "count"])
            .sort_values("mean", ascending=False)
        )

        results["shop_errors"] = shop_error_summary
        results["worst_shops"] = shop_error_summary.head(10)

    # Анализ по категориям товаров (если доступны метаданные)
    if metadata is not None and "item_category_id" in metadata.columns:
        category_errors = metadata.copy()
        category_errors["residual"] = residuals.values
        category_errors["abs_error"] = absolute_errors.values

        category_error_summary = (
            category_errors.groupby("item_category_id")["abs_error"]
            .agg(["mean", "std", "count"])
            .sort_values("mean", ascending=False)
        )

        results["category_errors"] = category_error_summary
        results["worst_categories"] = category_error_summary.head(10)

    # Анализ больших ошибок (outliers)
    error_threshold = absolute_errors.quantile(0.95)
    large_errors_mask = absolute_errors > error_threshold

    results["large_errors"] = {
        "count": int(large_errors_mask.sum()),
        "percentage": float(large_errors_mask.mean() * 100),
        "threshold": float(error_threshold),
        "mean_error": float(absolute_errors[large_errors_mask].mean()),
        "max_error": float(absolute_errors[large_errors_mask].max()),
    }

    # Корреляция между ошибками и фичами
    if X is not None:
        # Фильтруем константные столбцы (std = 0), чтобы избежать деления на ноль
        non_constant_cols = []
        residuals_series = pd.Series(residuals)

        for col in X.columns:
            col_std = X[col].std()
            if col_std > 1e-10:  # Игнорируем почти константные столбцы
                try:
                    corr = residuals_series.corr(X[col])
                    if pd.notna(corr):  # Игнорируем NaN корреляции
                        non_constant_cols.append(
                            {"feature": col, "correlation_with_abs_error": abs(corr)}
                        )
                except Exception:
                    # Пропускаем столбцы, для которых корреляция не может быть вычислена
                    continue

        if non_constant_cols:
            error_feature_corr = pd.DataFrame(non_constant_cols).sort_values(
                "correlation_with_abs_error", ascending=False
            )
            results["error_feature_correlation"] = error_feature_corr.head(20)
        else:
            results["error_feature_correlation"] = pd.DataFrame(
                columns=["feature", "correlation_with_abs_error"]
            )

    return results


def plot_error_analysis(
    error_results: Dict[str, Any],
    output_dir: Optional[Path] = None,
    show: bool = True,
) -> Dict[str, Optional[Path]]:
    """
    Создаёт визуализации для error analysis.

    Args:
        error_results: Результат analyze_errors()
        output_dir: Директория для сохранения графиков
        show: Показывать ли графики

    Returns:
        dict с путями к сохранённым файлам
    """
    saved_files = {}

    # 1. Распределение ошибок
    residuals = error_results["residuals"]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Гистограмма residuals
    axes[0, 0].hist(residuals, bins=50, edgecolor="black", alpha=0.7)
    axes[0, 0].axvline(0, color="red", linestyle="--", linewidth=2)
    axes[0, 0].set_xlabel("Residual (y_true - y_pred)")
    axes[0, 0].set_ylabel("Frequency")
    axes[0, 0].set_title("Распределение residuals")
    axes[0, 0].grid(True, alpha=0.3)

    # Q-Q plot для проверки нормальности
    stats.probplot(residuals, dist="norm", plot=axes[0, 1])
    axes[0, 1].set_title("Q-Q Plot (проверка нормальности)")
    axes[0, 1].grid(True, alpha=0.3)

    # Residuals vs Predicted
    y_pred = error_results.get("y_pred", None)
    if y_pred is not None:
        axes[1, 0].scatter(y_pred, residuals, alpha=0.5, s=10)
        axes[1, 0].axhline(0, color="red", linestyle="--", linewidth=2)
        axes[1, 0].set_xlabel("Predicted values")
        axes[1, 0].set_ylabel("Residuals")
        axes[1, 0].set_title("Residuals vs Predicted")
        axes[1, 0].grid(True, alpha=0.3)

    # Абсолютные ошибки по магазинам (если доступно)
    if "worst_shops" in error_results and len(error_results["worst_shops"]) > 0:
        worst_shops = error_results["worst_shops"].head(10)
        axes[1, 1].barh(range(len(worst_shops)), worst_shops["mean"].values, alpha=0.7)
        axes[1, 1].set_yticks(range(len(worst_shops)))
        axes[1, 1].set_yticklabels(worst_shops.index)
        axes[1, 1].set_xlabel("Mean Absolute Error")
        axes[1, 1].set_title("Топ-10 магазинов с наибольшими ошибками")
        axes[1, 1].grid(True, alpha=0.3, axis="x")
    else:
        # Корреляция ошибок с фичами
        if "error_feature_correlation" in error_results:
            corr_data = error_results["error_feature_correlation"].head(10)
            axes[1, 1].barh(
                range(len(corr_data)),
                corr_data["correlation_with_abs_error"].values,
                alpha=0.7,
            )
            axes[1, 1].set_yticks(range(len(corr_data)))
            axes[1, 1].set_yticklabels(corr_data["feature"].values)
            axes[1, 1].set_xlabel("|Correlation with Absolute Error|")
            axes[1, 1].set_title("Топ-10 фичей, коррелирующих с ошибками")
            axes[1, 1].grid(True, alpha=0.3, axis="x")
        else:
            axes[1, 1].text(
                0.5,
                0.5,
                "Недостаточно данных",
                ha="center",
                va="center",
                transform=axes[1, 1].transAxes,
            )

    plt.tight_layout()

    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        filepath = output_dir / "error_analysis.png"
        plt.savefig(filepath, dpi=150, bbox_inches="tight")
        saved_files["error_analysis"] = filepath
        print(f"Error analysis plot сохранён: {filepath}")
        if not show:
            plt.close()
    else:
        if show:
            plt.show()
        else:
            plt.close()

    return saved_files


def explain_model(
    model,
    X: pd.DataFrame,
    y_true: Optional[pd.Series] = None,
    y_pred: Optional[pd.Series] = None,
    metadata: Optional[pd.DataFrame] = None,
    max_shap_samples: int = 1000,
    output_dir: Optional[Path] = None,
    log_to_mlflow: bool = True,
) -> Dict[str, Any]:
    """
    Полный explainability анализ модели (SHAP + Error Analysis).

    Args:
        model: Обученная модель
        X: DataFrame с фичами
        y_true: Реальные значения (для error analysis)
        y_pred: Предсказанные значения (для error analysis)
        metadata: DataFrame с метаданными (shop_id, item_id, etc.)
        max_shap_samples: Максимальное количество образцов для SHAP
        output_dir: Директория для сохранения результатов
        log_to_mlflow: Логировать ли результаты в MLflow

    Returns:
        dict с результатами анализа
    """
    results = {}

    # SHAP анализ (только для tree-based моделей)
    model_type = type(model).__name__.lower()
    if "lgbm" in model_type or "xgb" in model_type or "tree" in model_type:
        print("\n=== SHAP Analysis ===")
        shap_result = calculate_shap_values(
            model=model,
            X=X,
            max_samples=max_shap_samples,
            tree_explainer=True,
        )

        if shap_result is not None:
            results["shap"] = shap_result

            # Создаём графики
            if output_dir:
                shap_dir = output_dir / "shap"
                summary_path = plot_shap_summary(
                    shap_result,
                    output_path=shap_dir / "shap_summary.png",
                    show=False,
                )
                waterfall_path = plot_shap_waterfall(
                    shap_result,
                    sample_idx=0,
                    output_path=shap_dir / "shap_waterfall.png",
                    show=False,
                )
                results["shap_plots"] = {
                    "summary": summary_path,
                    "waterfall": waterfall_path,
                }

                # Логируем в MLflow
                if log_to_mlflow:
                    try:
                        if summary_path:
                            mlflow.log_artifact(
                                str(summary_path), "explainability/shap"
                            )
                        if waterfall_path:
                            mlflow.log_artifact(
                                str(waterfall_path), "explainability/shap"
                            )
                    except Exception as e:
                        print(f"Не удалось залогировать SHAP plots в MLflow: {e}")
    else:
        print(f"SHAP анализ пропущен для модели типа {model_type}")

    # Error Analysis
    if y_true is not None and y_pred is not None:
        print("\n=== Error Analysis ===")
        error_results = analyze_errors(
            y_true=y_true,
            y_pred=y_pred,
            X=X,
            metadata=metadata,
        )
        results["errors"] = error_results

        # Добавляем y_pred в results для визуализации
        error_results["y_pred"] = y_pred

        # Создаём графики
        if output_dir:
            error_plots = plot_error_analysis(
                error_results,
                output_dir=output_dir / "error_analysis",
                show=False,
            )
            results["error_plots"] = error_plots

            # Логируем в MLflow
            if log_to_mlflow:
                try:
                    for plot_name, plot_path in error_plots.items():
                        if plot_path:
                            mlflow.log_artifact(
                                str(plot_path), "explainability/error_analysis"
                            )

                    # Логируем метрики ошибок
                    mlflow.log_metric(
                        "error_mean", error_results["error_stats"]["mean"]
                    )
                    mlflow.log_metric("error_std", error_results["error_stats"]["std"])
                    if "large_errors" in error_results:
                        mlflow.log_metric(
                            "large_errors_percentage",
                            error_results["large_errors"]["percentage"],
                        )
                except Exception as e:
                    print(f"Не удалось залогировать error analysis в MLflow: {e}")

    return results
