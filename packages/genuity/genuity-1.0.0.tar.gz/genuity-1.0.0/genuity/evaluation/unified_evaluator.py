"""
Unified Evaluation API for Raw Real and Synthetic Data

This module provides a unified interface for evaluating synthetic data quality.
It accepts raw (final format) real and synthetic data, and handles preprocessing/postprocessing
automatically when needed for compatibility.
"""

import pandas as pd
import numpy as np
from typing import Optional, Dict, List, Tuple, Any, Union
import warnings
import traceback

# Import data processors
try:
    from genuity.data_processor.data_preprocess import TabularPreprocessor
    from genuity.data_processor.data_postprocess import TabularPostprocessor
    HAS_PREPROCESSOR = True
except ImportError:
    HAS_PREPROCESSOR = False
    warnings.warn("Data preprocessor/postprocessor not available. Some features may be limited.")

# Import comprehensive evaluator
from .comprehensive_evaluator import ComprehensiveSyntheticEvaluator

warnings.filterwarnings("ignore")


class UnifiedEvaluator:
    """
    Unified evaluator that works with raw real and synthetic data.
    Automatically handles preprocessing/postprocessing when needed.
    """

    def __init__(
        self,
        real_data: pd.DataFrame,
        synthetic_data: pd.DataFrame,
        target_column: Optional[str] = None,
        categorical_columns: Optional[List[str]] = None,
        preprocessor: Optional[Any] = None,
        postprocessor: Optional[Any] = None,
        verbose: bool = True,
    ):
        """
        Initialize unified evaluator.

        Args:
            real_data: Raw real data (final format)
            synthetic_data: Raw synthetic data (final format)
            target_column: Target column for utility metrics
            categorical_columns: List of categorical column names
            preprocessor: Optional preprocessor object (for compatibility checks)
            postprocessor: Optional postprocessor object (for compatibility checks)
            verbose: Whether to print progress messages
        """
        self.verbose = verbose
        self.real_data_raw = real_data.copy()
        self.synthetic_data_raw = synthetic_data.copy()
        self.target_column = target_column
        self.categorical_columns = categorical_columns or []
        self.preprocessor = preprocessor
        self.postprocessor = postprocessor

        # Store processed versions if needed
        self.real_data_processed = None
        self.synthetic_data_processed = None

        # Validate and prepare data
        self._prepare_data()

    def _log(self, *args, **kwargs):
        """Log message if verbose."""
        if self.verbose:
            print("[UnifiedEvaluator]", *args, **kwargs)

    def _prepare_data(self):
        """Prepare data for evaluation, handling format mismatches."""
        self._log("Preparing data for evaluation...")

        # Ensure both are DataFrames
        if not isinstance(self.real_data_raw, pd.DataFrame):
            self.real_data_raw = pd.DataFrame(self.real_data_raw)
        if not isinstance(self.synthetic_data_raw, pd.DataFrame):
            self.synthetic_data_raw = pd.DataFrame(self.synthetic_data_raw)

        # Check column compatibility
        real_cols = set(self.real_data_raw.columns)
        synth_cols = set(self.synthetic_data_raw.columns)
        common_cols = real_cols & synth_cols

        if len(common_cols) == 0:
            raise ValueError(
                f"No common columns found between real and synthetic data. "
                f"Real: {list(real_cols)[:5]}, Synthetic: {list(synth_cols)[:5]}"
            )

        # Use only common columns
        self.real_data_raw = self.real_data_raw[list(common_cols)]
        self.synthetic_data_raw = self.synthetic_data_raw[list(common_cols)]

        # Auto-detect categorical columns if not provided
        if not self.categorical_columns:
            self.categorical_columns = self._auto_detect_categorical(self.real_data_raw)

        self._log(f"Data prepared: {len(common_cols)} columns, "
                  f"{len(self.real_data_raw)} real samples, "
                  f"{len(self.synthetic_data_raw)} synthetic samples")

    def _auto_detect_categorical(self, df: pd.DataFrame) -> List[str]:
        """Auto-detect categorical columns."""
        categorical = []
        for col in df.columns:
            if df[col].dtype == 'object' or df[col].dtype == 'category':
                categorical.append(col)
            elif len(df[col].unique()) < min(10, len(df) * 0.1):
                categorical.append(col)
        return categorical

    def _handle_preprocessing_if_needed(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Handle preprocessing if data format requires it.
        Returns (real_processed, synthetic_processed) or (real_raw, synthetic_raw) if not needed.
        """
        try:
            # Try to use raw data directly first
            real_ready = self.real_data_raw.copy()
            synth_ready = self.synthetic_data_raw.copy()

            # Check if we need preprocessing (e.g., one-hot encoded columns, scaled values)
            needs_preprocessing = False

            # Check for one-hot encoded columns (many columns with 0/1 values)
            for col in real_ready.columns:
                if col in synth_ready.columns:
                    unique_vals = set(real_ready[col].dropna().unique())
                    if unique_vals <= {0, 1} and real_ready[col].dtype in [np.int64, np.float64]:
                        # Might be one-hot encoded, but could also be binary
                        if len(unique_vals) == 2:
                            # Check if this looks like one-hot (many such columns)
                            one_hot_like = sum(
                                1 for c in real_ready.columns
                                if set(real_ready[c].dropna().unique()) <= {0, 1}
                            )
                            if one_hot_like > len(self.categorical_columns) * 2:
                                needs_preprocessing = True
                                break

            # If preprocessing is needed and we have preprocessor/postprocessor
            if needs_preprocessing and HAS_PREPROCESSOR and self.preprocessor and self.postprocessor:
                self._log("Detected preprocessed format. Using preprocessor/postprocessor...")
                try:
                    # Real data: inverse transform if needed
                    if hasattr(self.postprocessor, 'inverse_transform_modified_data'):
                        real_ready = self.postprocessor.inverse_transform_modified_data(real_ready)

                    # Synthetic data: inverse transform if needed
                    if hasattr(self.postprocessor, 'inverse_transform_modified_data'):
                        synth_ready = self.postprocessor.inverse_transform_modified_data(synth_ready)

                    self._log("Successfully converted preprocessed data to raw format")
                except Exception as e:
                    self._log(f"Warning: Could not use preprocessor/postprocessor: {e}")
                    self._log("Continuing with raw data as-is...")

            return real_ready, synth_ready

        except Exception as e:
            self._log(f"Error in preprocessing handling: {e}")
            self._log("Falling back to raw data...")
            return self.real_data_raw.copy(), self.synthetic_data_raw.copy()

    def evaluate(
        self,
        metrics: Optional[List[str]] = None,
        generate_plots: bool = True,
        save_plots_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Run comprehensive evaluation on raw real and synthetic data.

        Args:
            metrics: List of metric categories to evaluate.
                    Options: ['similarity', 'utility', 'privacy', 'detectability', 'missingness']
                    If None, evaluates all metrics.
            generate_plots: Whether to generate visualization plots
            save_plots_path: Path to save plots

        Returns:
            Dictionary containing evaluation results
        """
        self._log("=" * 60)
        self._log("UNIFIED SYNTHETIC DATA EVALUATION")
        self._log("=" * 60)

        # Prepare data (handle preprocessing if needed)
        real_ready, synth_ready = self._handle_preprocessing_if_needed()

        # Initialize comprehensive evaluator with ready data
        try:
            evaluator = ComprehensiveSyntheticEvaluator(
                real_data=real_ready,
                synthetic_data=synth_ready,
                target_column=self.target_column,
                categorical_columns=self.categorical_columns,
            )
        except Exception as e:
            self._log(f"Error initializing evaluator: {e}")
            self._log("Attempting to fix data issues...")

            # Try to fix common issues
            real_ready = self._fix_data_issues(real_ready)
            synth_ready = self._fix_data_issues(synth_ready)

            # Try again
            evaluator = ComprehensiveSyntheticEvaluator(
                real_data=real_ready,
                synthetic_data=synth_ready,
                target_column=self.target_column,
                categorical_columns=self.categorical_columns,
            )

        # Run evaluations
        results = {}

        if metrics is None:
            # Run all metrics
            results = evaluator.comprehensive_evaluation()
        else:
            # Run selected metrics
            if 'similarity' in metrics:
                results['similarity'] = evaluator.evaluate_similarity_metrics()
            if 'utility' in metrics:
                results['utility'] = evaluator.evaluate_utility_metrics()
            if 'privacy' in metrics:
                results['privacy'] = evaluator.evaluate_privacy_metrics()
            if 'detectability' in metrics:
                results['detectability'] = evaluator.evaluate_detectability_metrics()
            if 'missingness' in metrics:
                results['missingness'] = evaluator.evaluate_missingness_metrics()

            # Calculate overall scores
            evaluator.results = results
            evaluator._calculate_overall_scores()
            results['overall_scores'] = evaluator.results.get('overall_scores', {})

        # Generate plots if requested
        if generate_plots:
            try:
                evaluator.generate_visualizations(save_plots_path or "evaluation_plots.png")
                results['plots_saved'] = save_plots_path or "evaluation_plots.png"
            except Exception as e:
                self._log(f"Warning: Could not generate plots: {e}")

        # Add metadata
        results['metadata'] = {
            'real_data_shape': real_ready.shape,
            'synthetic_data_shape': synth_ready.shape,
            'num_columns': len(real_ready.columns),
            'categorical_columns': self.categorical_columns,
            'target_column': self.target_column,
        }

        return results

    def _fix_data_issues(self, df: pd.DataFrame) -> pd.DataFrame:
        """Fix common data issues that might cause evaluation errors."""
        df_fixed = df.copy()

        # Replace inf with nan
        df_fixed = df_fixed.replace([np.inf, -np.inf], np.nan)

        # Fill remaining inf/nan in numerical columns with median
        numeric_cols = df_fixed.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df_fixed[col].isnull().any():
                median_val = df_fixed[col].median()
                if pd.notna(median_val):
                    df_fixed[col].fillna(median_val, inplace=True)
                else:
                    df_fixed[col].fillna(0, inplace=True)

        # Ensure categorical columns are strings
        for col in self.categorical_columns:
            if col in df_fixed.columns:
                df_fixed[col] = df_fixed[col].astype(str)

        return df_fixed


# Convenience functions
def evaluate_synthetic_data(
    real_data: Union[pd.DataFrame, np.ndarray],
    synthetic_data: Union[pd.DataFrame, np.ndarray],
    target_column: Optional[str] = None,
    categorical_columns: Optional[List[str]] = None,
    preprocessor: Optional[Any] = None,
    postprocessor: Optional[Any] = None,
    metrics: Optional[List[str]] = None,
    generate_plots: bool = True,
    save_plots_path: Optional[str] = None,
    verbose: bool = True,
) -> Dict[str, Any]:
    """
    Main function to evaluate synthetic data quality.

    This function accepts raw (final format) real and synthetic data and automatically
    handles any preprocessing/postprocessing needed for compatibility.

    Args:
        real_data: Raw real data (DataFrame or array)
        synthetic_data: Raw synthetic data (DataFrame or array)
        target_column: Target column for utility metrics
        categorical_columns: List of categorical column names
        preprocessor: Optional preprocessor object (for compatibility)
        postprocessor: Optional postprocessor object (for compatibility)
        metrics: List of metrics to evaluate. If None, evaluates all.
        generate_plots: Whether to generate plots
        save_plots_path: Path to save plots
        verbose: Whether to print progress

    Returns:
        Dictionary with evaluation results including:
        - overall_scores: Overall quality scores by category
        - similarity: Similarity metrics
        - utility: Utility metrics
        - privacy: Privacy metrics
        - detectability: Detectability metrics
        - missingness: Missingness metrics
        - metadata: Evaluation metadata

    Example:
        >>> import pandas as pd
        >>> from genuity.evaluation import evaluate_synthetic_data
        >>>
        >>> real_df = pd.read_csv("real_data.csv")
        >>> synthetic_df = pd.read_csv("synthetic_data.csv")
        >>>
        >>> results = evaluate_synthetic_data(
        ...     real_data=real_df,
        ...     synthetic_data=synthetic_df,
        ...     target_column='outcome',
        ...     categorical_columns=['category', 'status']
        ... )
        >>>
        >>> print(f"Overall Quality: {results['overall_scores']['overall']:.3f}")
    """
    # Convert to DataFrames if needed
    if not isinstance(real_data, pd.DataFrame):
        if isinstance(real_data, np.ndarray):
            real_data = pd.DataFrame(real_data)
        else:
            raise TypeError(f"real_data must be DataFrame or ndarray, got {type(real_data)}")

    if not isinstance(synthetic_data, pd.DataFrame):
        if isinstance(synthetic_data, np.ndarray):
            synthetic_data = pd.DataFrame(synthetic_data)
        else:
            raise TypeError(f"synthetic_data must be DataFrame or ndarray, got {type(synthetic_data)}")

    # Create evaluator
    evaluator = UnifiedEvaluator(
        real_data=real_data,
        synthetic_data=synthetic_data,
        target_column=target_column,
        categorical_columns=categorical_columns,
        preprocessor=preprocessor,
        postprocessor=postprocessor,
        verbose=verbose,
    )

    # Run evaluation
    return evaluator.evaluate(
        metrics=metrics,
        generate_plots=generate_plots,
        save_plots_path=save_plots_path,
    )


# Alias for backward compatibility
evaluate_real_vs_synthetic = evaluate_synthetic_data
