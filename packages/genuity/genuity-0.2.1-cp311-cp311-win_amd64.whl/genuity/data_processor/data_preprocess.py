# Updated TabularPreprocessor
import pandas as pd
import numpy as np
import joblib
import warnings
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import (
    StandardScaler,
    MinMaxScaler,
    RobustScaler,
    MaxAbsScaler,
    OneHotEncoder,
    OrdinalEncoder,
)
import category_encoders as ce

import warnings
from datetime import datetime
import textwrap

warnings.filterwarnings("ignore")

# ANSI Color Codes for nicer terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class TabularPreprocessor:
    """
    Advanced tabular preprocessor that classifies columns, handles missing values,
    encodes categorical variables (supports: 'label', 'onehot', 'binary', 'embedding', 'target', 'frequency', 'hash', or None),
    removes long-text columns, computes outlier bounds,
    applies scaling and PCA, and saves state for postprocessing.
    """

    def __init__(
        self,
        cardinality_ratio_threshold: int = 100000,  # find hyper
        outlier_iqr_multiplier: float = 1.5,
        text_length_threshold: int = 100,
        max_char_threshold: int = 500,
        n_pca_components: int = 0,
        scaler_type: str = "standard",  # 'standard', 'minmax', 'robust', 'maxabs', or None
        imputation_strategy: str = "auto",  # 'auto', 'mean', 'median', 'mode', 'ml'
        encoding_strategy: str = "onehot",  # 'onehot', 'ordinal', or None
        handle_datetime: bool = True,
        random_state: int = 42,
        verbose: bool = True,
    ):
        self.cardinality_ratio_threshold = cardinality_ratio_threshold
        self.outlier_iqr_multiplier = outlier_iqr_multiplier
        self.text_length_threshold = text_length_threshold
        self.max_char_threshold = max_char_threshold
        self.n_pca_components = n_pca_components
        self.scaler_type = scaler_type
        self.imputation_strategy = imputation_strategy
        self.encoding_strategy = encoding_strategy
        self.handle_datetime = handle_datetime
        self.random_state = random_state
        self.verbose = verbose
        self._reset_attributes()

    def _reset_attributes(self):
        self.continuous_cols_ = []
        self.categorical_cols_ = []
        self.binary_cols_ = []
        self.long_text_cols_ = []
        self.datetime_cols_ = []
        self.outlier_bounds_ = {}
        self.pca_ = None
        self.scaler_ = None
        self.imputers_ = {}
        self.column_mappings_ = {}
        self.encoder_ = None
        self.feature_names_ = []
        self.encoded_col_names_ = []
        self.is_fitted_ = False
        self.original_dtypes_ = {}

    def _print_step(self, msg: str, level: str = "INFO"):
        """
        Prints a formatted message with timestamp and level.
        Levels: INFO, WARN, ERROR, SUCCESS, HEADER
        """
        if not self.verbose:
            return
            
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        icon_map = {
            "INFO": "[INFO]",
            "WARN": "[WARN]",
            "ERROR": "[ERROR]",
            "SUCCESS": "[SUCCESS]",
            "HEADER": "[Step]"
        }
        
        color_map = {
            "INFO": Colors.BLUE,
            "WARN": Colors.WARNING,
            "ERROR": Colors.FAIL,
            "SUCCESS": Colors.GREEN,
            "HEADER": Colors.HEADER + Colors.BOLD
        }
        
        icon = icon_map.get(level, "")
        color = color_map.get(level, "")
        reset = Colors.ENDC
        
        # Handle multi-line messages for better readability
        lines = msg.split('\n')
        for i, line in enumerate(lines):
            prefix = f"[{timestamp}] {icon} " if i == 0 else f"           "
            print(f"{color}{prefix}{line}{reset}")

    def _print_banner(self, msg: str):
        if self.verbose:
            print(f"\n{Colors.HEADER}{'='*60}")
            self._print_step(f"{msg}", level="HEADER")
            print(f"{'='*60}{Colors.ENDC}\n")

    def fit_transform(self, df: pd.DataFrame) -> dict:
        """Fit and transform the data with comprehensive validation."""
        # Input validation
        if df is None or df.empty:
            raise ValueError("DataFrame cannot be None or empty")

        if not isinstance(df, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame")

        # Record original dtypes immediately
        self.original_dtypes_ = df.dtypes.to_dict()

        # Check for infinite values
        if df.isin([np.inf, -np.inf]).any().any():
            raise ValueError("DataFrame contains infinite values")

        # Check for all-null columns
        null_columns = df.columns[df.isnull().all()].tolist()
        if null_columns:
            self._print_step(f"Dropping {len(null_columns)} all-null columns: {null_columns[:5]}...", level="WARN")
            df = df.drop(columns=null_columns)

        self._print_banner("Starting Preprocessing Pipeline")
        self._reset_attributes()
        # restore original dtypes to reset state after _reset_attributes
        self.original_dtypes_ = df.dtypes.to_dict()

        df_processed = df.copy()
        if self.handle_datetime:
            df_processed = self._process_datetime(df_processed)

        self._classify_columns(df_processed)
        df_numeric = self._convert_to_numeric(df_processed)
        df_clean = (
            df_numeric.drop(columns=self.long_text_cols_)
            if self.long_text_cols_
            else df_numeric
        )
        df_imputed = self._handle_missing_values(df_clean)
        self._compute_outlier_bounds(df_imputed)
        outlier_flags = self._create_outlier_flags(df_imputed)
        df_base, encoded_df = self._apply_encoding(df_imputed)
        df_scaled = self._apply_scaling(df_base)
        df_final, pca_df = self._apply_pca(df_scaled)

        parts = []
        if self.continuous_cols_:
            parts.append(df_final[self.continuous_cols_])
        if not pca_df.empty:
            parts.append(pca_df)
        if not encoded_df.empty:
            parts.append(encoded_df)
        if self.binary_cols_:
            parts.append(df_final[self.binary_cols_])
        parts.append(outlier_flags)
        preprocessed = pd.concat(parts, axis=1)

        result = {
            "continuous": (
                df_final[self.continuous_cols_].copy()
                if self.continuous_cols_
                else pd.DataFrame(index=df.index)
            ),
            "categorical": encoded_df.copy(),
            "binary": (
                df_final[self.binary_cols_].copy()
                if self.binary_cols_
                else pd.DataFrame(index=df.index)
            ),
            "outlier_flags": outlier_flags.copy(),
            "pca_features": pca_df.copy(),
            "preprocessed": preprocessed.copy(),
        }

        self.feature_names_ = list(preprocessed.columns)
        self.is_fitted_ = True
        # Persist some mapping info
        self.column_mappings_["conversions"] = self.column_mappings_.get("conversions", {})
        self._print_banner("Preprocessing Pipeline Complete")
        return result

    def _process_datetime(self, df: pd.DataFrame) -> pd.DataFrame:
        self._print_step("Processing datetime columns...")
        out = df.copy()
        # Identify and convert datetime columns
        for col in out.columns:
            if pd.api.types.is_datetime64_any_dtype(out[col]):
                self.datetime_cols_.append(col)
            elif out[col].dtype == "object":
                # Heuristic: check if first valid value looks like a date
                first_valid = (
                    out[col].dropna().iloc[0] if not out[col].dropna().empty else None
                )
                if first_valid and isinstance(first_valid, str):
                    try:
                        # Try converting the column
                        temp = pd.to_datetime(out[col], errors="coerce")
                        # If more than 50% are valid dates, treat as datetime
                        if temp.notna().mean() > 0.5:
                            out[col] = temp
                            self.datetime_cols_.append(col)
                    except (ValueError, TypeError):
                        pass

        # Extract features
        for col in list(self.datetime_cols_):
            if col in out.columns:
                out[f"{col}_year"] = out[col].dt.year
                out[f"{col}_month"] = out[col].dt.month
                out[f"{col}_day"] = out[col].dt.day
                out[f"{col}_dow"] = out[col].dt.dayofweek
                out.drop(columns=[col], inplace=True)

        return out

    def _classify_columns(self, df: pd.DataFrame):
        self._print_step("Classifying columns...", level="HEADER")
        n = len(df)
        cutoff = max(2, n // max(1, self.cardinality_ratio_threshold))
        for col in df.columns:
            if self._is_long_text_column(df[col]):
                self.long_text_cols_.append(col)
                continue
            nunique = df[col].nunique(dropna=True)
            if pd.api.types.is_numeric_dtype(df[col]):
                if nunique <= 2:
                    self.binary_cols_.append(col)
                    # Don't add binary columns to categorical_cols - they're already 0/1
                elif nunique >= cutoff:
                    self.continuous_cols_.append(col)
                else:
                    self.categorical_cols_.append(col)
            else:
                # object or categorical
                non_na = df[col].dropna().astype(str)
                avg_len = non_na.map(len).mean() if not non_na.empty else 0
                if avg_len <= self.text_length_threshold:
                    self.categorical_cols_.append(col)
                else:
                    self.long_text_cols_.append(col)
        self._print_step(
            f"Continuous: {len(self.continuous_cols_)} | Categorical: {len(self.categorical_cols_)} | Binary: {len(self.binary_cols_)} | Dropped text: {len(self.long_text_cols_)}",
            level="SUCCESS"
        )

    def _is_long_text_column(self, s: pd.Series) -> bool:
        try:
            non_null = s.dropna()
            if non_null.empty:
                return False
            return non_null.astype(str).map(len).max() > self.max_char_threshold
        except Exception:
            return False

    def _convert_to_numeric(self, df: pd.DataFrame) -> pd.DataFrame:
        self._print_step("Converting to numeric where possible...", level="HEADER")
        out = df.copy()
        conv = {}
        for col in out.columns:
            if col in self.long_text_cols_:
                conv[col] = f"{out[col].dtype}→kept_long_text"
                continue
            orig_dtype = out[col].dtype
            denom = out[col].notna().sum()
            if denom == 0:
                conv[col] = f"{orig_dtype}→kept_no_non_na"
                continue
            num = pd.to_numeric(out[col], errors="coerce")
            if num.notna().sum() >= 0.8 * denom:
                out[col] = num
                conv[col] = f"{orig_dtype}→numeric"
            else:
                conv[col] = f"{orig_dtype}→kept"
        self.column_mappings_["conversions"] = conv
        return out

    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        self._print_step(f"Imputing missing ({self.imputation_strategy})...", level="HEADER")
        out = df.copy()
        for col in out.columns:
            if col in self.long_text_cols_ or out[col].isna().sum() == 0:
                continue
            if self.imputation_strategy == "auto":
                if pd.api.types.is_numeric_dtype(out[col]):
                    val, strat = out[col].mean(), "mean"
                else:
                    val, strat = (
                        out[col].mode().iloc[0]
                        if not out[col].mode().empty
                        else "Unknown"
                    ), "mode"
                out[col].fillna(val, inplace=True)
            elif self.imputation_strategy in {"mean", "median", "mode"}:
                # Check if column is numeric for mean/median
                if self.imputation_strategy in {"mean", "median"} and not pd.api.types.is_numeric_dtype(out[col]):
                    # Fall back to mode for non-numeric columns
                    val = (
                        out[col].mode().iloc[0]
                        if not out[col].mode().empty
                        else "Unknown"
                    )
                    strat = "mode"
                else:
                    func = getattr(out[col], self.imputation_strategy)
                    val, strat = func(), self.imputation_strategy
                out[col].fillna(val, inplace=True)
            elif self.imputation_strategy == "ml":
                out = self._ml_impute_column(out, col)
                continue
            else:
                val, strat = (
                    out[col].mode().iloc[0] if not out[col].mode().empty else "Unknown"
                ), "fallback"
                out[col].fillna(val, inplace=True)

            self.imputers_[col] = {"value": val, "strategy": strat}
        return out

    def _ml_impute_column(self, df: pd.DataFrame, target: str) -> pd.DataFrame:
        y = df[target]
        # use errors='ignore' in case long_text_cols_ or target not present
        drop_cols = list(self.long_text_cols_) + [target]
        X = df.drop(columns=drop_cols, errors="ignore").select_dtypes(
            include=[np.number]
        )
        mask = y.notna()
        # If too few rows to train, fallback
        if mask.sum() < 10:
            fallback = (
                y.mean()
                if pd.api.types.is_numeric_dtype(y)
                else (y.mode().iloc[0] if not y.mode().empty else 0)
            )
            df[target].fillna(fallback, inplace=True)
            self.imputers_[target] = {"value": fallback, "strategy": "fallback"}
            return df

        Model = (
            RandomForestRegressor
            if pd.api.types.is_numeric_dtype(y)
            else RandomForestClassifier
        )
        model = Model(n_estimators=50, random_state=self.random_state)
        X_train = X[mask].fillna(X.mean())
        try:
            model.fit(X_train, y[mask])
        except Exception as e:
            # fallback to simple imputation
            fallback = (
                y.mean()
                if pd.api.types.is_numeric_dtype(y)
                else (y.mode().iloc[0] if not y.mode().empty else 0)
            )
            df[target].fillna(fallback, inplace=True)
            self.imputers_[target] = {"value": fallback, "strategy": "fallback"}
            self._print_step(f"ML imputation failed for {target}, fallback used: {e}")
            return df

        X_missing = X[~mask].fillna(X.mean())
        preds = model.predict(X_missing)
        df.loc[~mask, target] = preds
        self.imputers_[target] = {"model": model, "strategy": "ml"}
        return df

    def _compute_outlier_bounds(self, df: pd.DataFrame):
        self._print_step("Computing outlier bounds...")
        for col in self.continuous_cols_:
            vals = pd.to_numeric(df[col], errors="coerce").dropna()
            if vals.empty:
                continue
            q1, q3 = np.percentile(vals, [25, 75])
            iqr = q3 - q1
            self.outlier_bounds_[col] = (
                q1 - self.outlier_iqr_multiplier * iqr,
                q3 + self.outlier_iqr_multiplier * iqr,
            )

    def _create_outlier_flags(self, df: pd.DataFrame) -> pd.DataFrame:
        self._print_step("Creating outlier flags...")
        flags = pd.DataFrame(index=df.index)
        for col, (low, high) in self.outlier_bounds_.items():
            vals = pd.to_numeric(df[col], errors="coerce")
            flags[f"{col}_outlier"] = ((vals < low) | (vals > high)).astype(int)
        return flags

    def _apply_encoding(self, df: pd.DataFrame):
        self._print_step("Encoding categorical columns...")
        enc_cols = list(self.categorical_cols_)
        if not self.encoding_strategy:
            enc_df = df[enc_cols].copy() if enc_cols else pd.DataFrame(index=df.index)
            base = df.drop(columns=enc_cols) if enc_cols else df.copy()
            self.encoder_ = None
            self.encoded_col_names_ = enc_cols
            return base, enc_df

        if not enc_cols:
            self.encoder_ = None
            self.encoded_col_names_ = []
            return df.copy(), pd.DataFrame(index=df.index)

        cat = df[enc_cols]
        strategy = self.encoding_strategy.lower()
        if strategy in ["onehot"]:
            # Use sparse if possible, but convert to dense for DataFrame
            self.encoder_ = OneHotEncoder(handle_unknown="ignore", sparse_output=True)
            arr_sparse = self.encoder_.fit_transform(cat)
            try:
                cols = list(self.encoder_.get_feature_names_out(enc_cols))
            except Exception:
                # sklearn older versions: try feature_names_in_
                try:
                    cols = list(self.encoder_.get_feature_names_out())
                except Exception:
                    # As last resort, synthesize columns
                    cols = [f"{c}_{v}" for c in enc_cols for v in pd.unique(cat[c].astype(str))]
            arr = arr_sparse.toarray()
        elif strategy in ["label", "embedding"]:
            self.encoder_ = OrdinalEncoder(
                handle_unknown="use_encoded_value", unknown_value=-1
            )
            arr = self.encoder_.fit_transform(cat)
            cols = enc_cols
        elif strategy == "binary":
            self.encoder_ = ce.BinaryEncoder(cols=enc_cols)
            arr_df = self.encoder_.fit_transform(cat)
            cols = arr_df.columns.tolist()
            arr = arr_df.values
        elif strategy == "hash":
            self.encoder_ = ce.HashingEncoder(cols=enc_cols, n_components=8)
            arr_df = self.encoder_.fit_transform(cat)
            cols = arr_df.columns.tolist()
            arr = arr_df.values
        elif strategy == "frequency":
            self.encoder_ = ce.CountEncoder(cols=enc_cols, normalize=True)
            arr_df = self.encoder_.fit_transform(cat)
            cols = arr_df.columns.tolist()
            arr = arr_df.values
        elif strategy == "target":
            if not hasattr(self, "target") or self.target is None:
                raise ValueError(
                    "Target encoding requires a target variable. Set self.target before fit_transform."
                )
            self.encoder_ = ce.TargetEncoder(cols=enc_cols)
            arr_df = self.encoder_.fit_transform(cat, self.target)
            cols = arr_df.columns.tolist()
            arr = arr_df.values
        else:
            raise ValueError(f"Unknown encoding strategy: {self.encoding_strategy}")

        self.encoded_col_names_ = list(cols)
        enc_df = pd.DataFrame(arr, columns=cols, index=df.index)
        base = df.drop(columns=enc_cols)
        return base, enc_df

    def _apply_scaling(self, df: pd.DataFrame) -> pd.DataFrame:
        if not self.scaler_type or not self.continuous_cols_:
            return df.copy()
        self._print_step(f"Applying {self.scaler_type} scaling...")
        mapper = {
            "standard": StandardScaler,
            "minmax": MinMaxScaler,
            "robust": RobustScaler,
            "maxabs": MaxAbsScaler,
        }
        if self.scaler_type not in mapper:
            self._print_step(f"Scaler type {self.scaler_type} not recognized; skipping scaling.")
            return df.copy()
        self.scaler_ = mapper[self.scaler_type]()
        out = df.copy()
        # ensure numeric and no-nans for scaler fit
        cont_data = df[self.continuous_cols_].copy().fillna(df[self.continuous_cols_].mean())
        out[self.continuous_cols_] = self.scaler_.fit_transform(cont_data)
        return out

    def _apply_pca(self, df: pd.DataFrame):
        if not self.continuous_cols_:
            return df.copy(), pd.DataFrame(index=df.index)
        n = self.n_pca_components or max(1, len(self.continuous_cols_) // 5)
        n = min(n, len(self.continuous_cols_))
        self._print_step(f"Applying PCA with {n} components...")
        # Fill NaNs for PCA input using column means (should be imputed already, but guard)
        cont_matrix = df[self.continuous_cols_].copy().fillna(df[self.continuous_cols_].mean())
        self.pca_ = PCA(n_components=n, random_state=self.random_state)
        comps = self.pca_.fit_transform(cont_matrix)
        cols = [f"gen_pca_{i+1}" for i in range(n)]
        return df.copy(), pd.DataFrame(comps, columns=cols, index=df.index)

    def save_preprocessor(self, filepath: str):
        if not self.is_fitted_:
            raise ValueError("Must fit before saving")
        state = {
            "config": {
                "cardinality_ratio_threshold": self.cardinality_ratio_threshold,
                "outlier_iqr_multiplier": self.outlier_iqr_multiplier,
                "text_length_threshold": self.text_length_threshold,
                "max_char_threshold": self.max_char_threshold,
                "n_pca_components": self.n_pca_components,
                "scaler_type": self.scaler_type,
                "imputation_strategy": self.imputation_strategy,
                "encoding_strategy": self.encoding_strategy,
                "handle_datetime": self.handle_datetime,
                "random_state": self.random_state,
                "verbose": self.verbose,
            },
            "state": {
                "continuous_cols_": self.continuous_cols_,
                "categorical_cols_": self.categorical_cols_,
                "binary_cols_": self.binary_cols_,
                "long_text_cols_": self.long_text_cols_,
                "datetime_cols_": self.datetime_cols_,
                "outlier_bounds_": self.outlier_bounds_,
                "pca_": self.pca_,
                "scaler_": self.scaler_,
                "imputers_": self.imputers_,
                "encoder_": self.encoder_,
                "feature_names_": self.feature_names_,
                "column_mappings_": self.column_mappings_,
                "encoded_col_names_": getattr(self, "encoded_col_names_", []),
                "original_dtypes_": {k: str(v) for k, v in self.original_dtypes_.items()},
            },
        }
        joblib.dump(state, filepath)

    @classmethod
    def load_preprocessor(cls, filepath: str):
        state = joblib.load(filepath)
        cfg = state["config"]
        pre = cls(**cfg)
        st = state["state"]
        pre.continuous_cols_ = st["continuous_cols_"]
        pre.categorical_cols_ = st["categorical_cols_"]
        pre.binary_cols_ = st["binary_cols_"]
        pre.long_text_cols_ = st["long_text_cols_"]
        pre.datetime_cols_ = st.get("datetime_cols_", [])
        pre.outlier_bounds_ = st["outlier_bounds_"]
        pre.pca_ = st.get("pca_")
        pre.scaler_ = st.get("scaler_")
        pre.imputers_ = st.get("imputers_", {})
        pre.encoder_ = st.get("encoder_")
        pre.feature_names_ = st.get("feature_names_", [])
        pre.column_mappings_ = st.get("column_mappings_", {})
        pre.encoded_col_names_ = st.get("encoded_col_names_", [])
        raw_dtypes = st.get("original_dtypes_", {})
        # convert saved dtype strings back to pandas dtypes
        pre.original_dtypes_ = {k: pd.api.types.pandas_dtype(v) for k, v in raw_dtypes.items()}
        pre.is_fitted_ = True
        return pre

    def get_column_info(self) -> dict:
        return {
            "continuous_columns": self.continuous_cols_,
            "categorical_columns": self.categorical_cols_,
            "binary_columns": self.binary_cols_,
            "dropped_text_columns": self.long_text_cols_,
            "datetime_columns": self.datetime_cols_,
            "outlier_bounds": self.outlier_bounds_,
            "feature_names": self.feature_names_,
            # Short keys for convenience
            "continuous": self.continuous_cols_,
            "categorical": self.categorical_cols_,
            "binary": self.binary_cols_,
            "datetime": self.datetime_cols_
        }
