# data_preprocess.py
"""
TabularPreprocessor

- One-hot encoding (forced, reversible)
- MinMax scaling (forced, reversible)
- Optional PCA (disabled by default for exact reconstruction)
- Many imputation strategies (including 'ml' which trains temporary models but DOES NOT save them)
- Stores original missing mask to restore NaNs on inverse
- Safe defaults and a practical cardinality threshold

Usage:
    pre = TabularPreprocessor(verbose=True)
    out = pre.fit_transform(df)
    pre.save("preprocessor.joblib")
"""
from typing import Optional, Dict, Any
import pandas as pd
import numpy as np
import joblib
import warnings

from sklearn.preprocessing import OneHotEncoder, QuantileTransformer
from sklearn.decomposition import PCA
from sklearn.impute import KNNImputer
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

warnings.filterwarnings("ignore")


class TabularPreprocessor:
    def __init__(
        self,
        *,
        cardinality_ratio: float = 0.05,  # 5% unique -> categorical
        min_cardinality_cap: int = 10,
        max_cardinality_cap: int = 50,
        outlier_iqr_multiplier: float = 1.5,
        max_text_length: int = 500,
        imputation_strategy: str = "auto",  # 'auto', 'mean','median','mode','constant','quantile:q','random_uniform','random_normal','random','knn:k','ml'
        random_state: int = 42,
        n_pca_components: int = 0,  # 0 => disabled (default)
        verbose: bool = True,
    ):
        self.cardinality_ratio = float(cardinality_ratio)
        self.min_cardinality_cap = int(min_cardinality_cap)
        self.max_cardinality_cap = int(max_cardinality_cap)
        self.outlier_iqr_multiplier = float(outlier_iqr_multiplier)
        self.max_text_length = int(max_text_length)
        self.imputation_strategy = imputation_strategy
        self.random_state = int(random_state)
        self.n_pca_components = int(n_pca_components) if n_pca_components else 0
        self.verbose = bool(verbose)

        # stateful attributes
        self._reset_state()

    def _reset_state(self):
        self.original_columns_ = []
        self.continuous_cols_: list[str] = []
        self.categorical_cols_: list[str] = []
        self.binary_cols_: list[str] = []
        self.long_text_cols_: list[str] = []
        self.outlier_bounds_: Dict[str, tuple] = {}
        self.missing_mask_: Dict[str, pd.Series] = {}
        self.imputers_: Dict[str, dict] = {}
        self.encoder_: Optional[OneHotEncoder] = None
        self.scaler_: Optional[QuantileTransformer] = None
        self.pca_: Optional[PCA] = None
        self.feature_names_: list[str] = []
        self.is_fitted_ = False

    def _log(self, *args, **kwargs):
        if self.verbose:
            print("[TabularPreprocessor]", *args, **kwargs)

    # ----------------- Public API -----------------
    def fit_transform(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        if df is None or not isinstance(df, pd.DataFrame) or df.empty:
            raise ValueError("fit_transform expects a non-empty pandas DataFrame")

        # reset state and store original columns
        self._reset_state()
        self.original_columns_ = list(df.columns)

        # store missing masks (to reapply NaNs on inverse)
        for c in df.columns:
            self.missing_mask_[c] = df[c].isna()

        self._classify_columns(df)
        df_num = self._convert_to_numeric(df)
        df_imp = self._impute(df_num)
        self._compute_outlier_bounds(df_imp)
        outlier_flags = self._create_outlier_flags(df_imp)

        base_df, encoded_df = self._onehot_encode(df_imp)
        scaled_df = self._scale(base_df)
        pca_df = pd.DataFrame(index=df.index)
        if self.n_pca_components and self.continuous_cols_:
            scaled_df, pca_df = self._apply_pca(scaled_df)

        # long text pass-through (not dropped, to allow invertibility)
        long_text_df = df_imp[self.long_text_cols_].copy() if self.long_text_cols_ else pd.DataFrame(index=df.index)

        parts = []
        if self.continuous_cols_:
            parts.append(scaled_df[self.continuous_cols_])
        if not encoded_df.empty:
            parts.append(encoded_df)
        if not pca_df.empty:
            parts.append(pca_df)
        if not outlier_flags.empty:
            parts.append(outlier_flags)
        if not long_text_df.empty:
            parts.append(long_text_df)

        preprocessed = pd.concat(parts, axis=1) if parts else pd.DataFrame(index=df.index)

        self.feature_names_ = list(preprocessed.columns)
        self.is_fitted_ = True

        self._log("fit_transform complete. features:", len(self.feature_names_))
        return {
            "preprocessed": preprocessed,
            "continuous": scaled_df[self.continuous_cols_].copy() if self.continuous_cols_ else pd.DataFrame(index=df.index),
            "categorical": encoded_df.copy(),
            "outlier_flags": outlier_flags.copy(),
            "pca_features": pca_df.copy(),
            "long_text": long_text_df.copy(),
        }

    def save(self, filepath: str) -> None:
        if not self.is_fitted_:
            raise RuntimeError("Preprocessor must be fitted before saving")
        # Save essential state for inverse transforms (no temporary ML models)
        bundle = {
            "config": {
                "cardinality_ratio": self.cardinality_ratio,
                "min_cardinality_cap": self.min_cardinality_cap,
                "max_cardinality_cap": self.max_cardinality_cap,
                "outlier_iqr_multiplier": self.outlier_iqr_multiplier,
                "max_text_length": self.max_text_length,
                "imputation_strategy": self.imputation_strategy,
                "random_state": self.random_state,
                "n_pca_components": self.n_pca_components,
            },
            "state": {
                "original_columns_": self.original_columns_,
                "continuous_cols_": self.continuous_cols_,
                "categorical_cols_": self.categorical_cols_,
                "binary_cols_": self.binary_cols_,
                "long_text_cols_": self.long_text_cols_,
                "outlier_bounds_": self.outlier_bounds_,
                "missing_mask_": self.missing_mask_,
                "imputers_": self.imputers_,
                "encoder_": self.encoder_,
                "scaler_": self.scaler_,
                "pca_": self.pca_,
                "feature_names_": self.feature_names_,
            },
        }
        joblib.dump(bundle, filepath)
        self._log(f"Saved preprocessor state to {filepath}")

    @classmethod
    def load(cls, filepath: str) -> "TabularPreprocessor":
        bundle = joblib.load(filepath)
        cfg = bundle.get("config", {})
        pre = cls(
            cardinality_ratio=cfg.get("cardinality_ratio", 0.05),
            min_cardinality_cap=cfg.get("min_cardinality_cap", 10),
            max_cardinality_cap=cfg.get("max_cardinality_cap", 50),
            outlier_iqr_multiplier=cfg.get("outlier_iqr_multiplier", 1.5),
            max_text_length=cfg.get("max_text_length", 500),
            imputation_strategy=cfg.get("imputation_strategy", "auto"),
            random_state=cfg.get("random_state", 42),
            n_pca_components=cfg.get("n_pca_components", 0),
            verbose=False,
        )
        st = bundle.get("state", {})
        pre.original_columns_ = st.get("original_columns_", [])
        pre.continuous_cols_ = st.get("continuous_cols_", [])
        pre.categorical_cols_ = st.get("categorical_cols_", [])
        pre.binary_cols_ = st.get("binary_cols_", [])
        pre.long_text_cols_ = st.get("long_text_cols_", [])
        pre.outlier_bounds_ = st.get("outlier_bounds_", {})
        pre.missing_mask_ = st.get("missing_mask_", {})
        pre.imputers_ = st.get("imputers_", {})
        pre.encoder_ = st.get("encoder_", None)
        pre.scaler_ = st.get("scaler_", None)
        pre.pca_ = st.get("pca_", None)
        pre.feature_names_ = st.get("feature_names_", [])
        pre.is_fitted_ = True
        pre._log(f"Loaded preprocessor from {filepath}")
        return pre

    # ----------------- Internal helpers -----------------
    def _classify_columns(self, df: pd.DataFrame) -> None:
        n = len(df)
        cutoff = min(self.max_cardinality_cap, max(self.min_cardinality_cap, int(self.cardinality_ratio * n)))
        for col in df.columns:
            # long-text detection
            try:
                max_len = df[col].dropna().astype(str).map(len).max()
            except Exception:
                max_len = 0
            if max_len and max_len > self.max_text_length:
                self.long_text_cols_.append(col)
                continue

            nunique = df[col].nunique(dropna=True)
            if pd.api.types.is_numeric_dtype(df[col]):
                if nunique <= 2:
                    self.binary_cols_.append(col)
                    self.categorical_cols_.append(col)
                elif nunique > cutoff:
                    self.continuous_cols_.append(col)
                else:
                    self.categorical_cols_.append(col)
            else:
                if nunique <= cutoff:
                    self.categorical_cols_.append(col)
                else:
                    self.long_text_cols_.append(col)

        self._log(f"classified columns: continuous={len(self.continuous_cols_)}, categorical={len(self.categorical_cols_)}, binary={len(self.binary_cols_)}, text={len(self.long_text_cols_)}")

    def _convert_to_numeric(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        for c in out.columns:
            if c in self.long_text_cols_:
                continue
            non_nulls = out[c].notna().sum()
            if non_nulls == 0:
                continue
            num = pd.to_numeric(out[c], errors="coerce")
            if num.notna().sum() >= 0.8 * non_nulls:
                out[c] = num
        return out

    def _impute(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        rng = np.random.default_rng(self.random_state)

        for c in out.columns:
            if out[c].isna().sum() == 0 or c in self.long_text_cols_:
                continue

            is_num = pd.api.types.is_numeric_dtype(out[c])
            strat = self.imputation_strategy

            # AUTO behavior or Fallback for type mismatch
            # If user asks for 'mean' but column is string, fallback to 'mode'
            numeric_strats = {"mean", "median", "random_uniform", "random_normal"}
            if (strat == "auto") or (not is_num and (strat in numeric_strats or strat.startswith("quantile"))):
                strat = "median" if is_num else "mode"

            # SIMPLE: mean/median/mode
            if strat in {"mean", "median", "mode"}:
                val = getattr(out[c], strat)()
                out[c].fillna(val, inplace=True)
                self.imputers_[c] = {"strategy": strat, "value": float(val) if is_num else val}

            # CONSTANT
            elif strat == "constant":
                val = 0 if is_num else "__MISSING__"
                out[c].fillna(val, inplace=True)
                self.imputers_[c] = {"strategy": "constant", "value": val}

            # QUANTILE: 'quantile:0.25'
            elif strat.startswith("quantile") and is_num:
                try:
                    q = float(strat.split(":")[1])
                except Exception:
                    q = 0.5
                val = out[c].quantile(q)
                out[c].fillna(val, inplace=True)
                self.imputers_[c] = {"strategy": strat, "value": float(val)}

            # RANDOM_UNIFORM
            elif strat == "random_uniform" and is_num:
                lo, hi = float(out[c].min()), float(out[c].max())
                mask = out[c].isna()
                out.loc[mask, c] = rng.uniform(lo, hi, size=mask.sum())
                self.imputers_[c] = {"strategy": strat, "fallback": float(out[c].median())}

            # RANDOM_NORMAL
            elif strat == "random_normal" and is_num:
                mu, sigma = float(out[c].mean()), float(out[c].std()) if out[c].std() else 0.0
                mask = out[c].isna()
                out.loc[mask, c] = rng.normal(mu, sigma, size=mask.sum())
                self.imputers_[c] = {"strategy": strat, "fallback": float(mu)}

            # RANDOM (categorical)
            elif strat == "random" and not is_num:
                probs = out[c].value_counts(normalize=True)
                if probs.empty:
                    fallback = "__MISSING__"
                    out[c].fillna(fallback, inplace=True)
                    self.imputers_[c] = {"strategy": strat, "fallback": fallback}
                else:
                    mask = out[c].isna()
                    out.loc[mask, c] = rng.choice(probs.index.to_numpy(), p=probs.values, size=mask.sum())
                    self.imputers_[c] = {"strategy": strat, "fallback": probs.idxmax()}

            # KNN: 'knn:5'
            elif strat.startswith("knn") and is_num:
                try:
                    k = int(strat.split(":")[1])
                except Exception:
                    k = 5
                # Apply KNN only across numeric continuous columns
                knn_cols = [col for col in self.continuous_cols_ if col in out.columns]
                if knn_cols:
                    imputer = KNNImputer(n_neighbors=max(1, k))
                    out[knn_cols] = imputer.fit_transform(out[knn_cols])
                    self.imputers_[c] = {"strategy": strat, "fallback": float(out[c].median())}
                else:
                    fallback = out[c].median() if is_num else (out[c].mode().iloc[0] if not out[c].mode().empty else None)
                    out[c].fillna(fallback, inplace=True)
                    self.imputers_[c] = {"strategy": "fallback", "value": fallback}

            # ML (temporary) - does NOT save the model
            elif strat == "ml":
                y = out[c]
                X = out.select_dtypes(include=[np.number]).drop(columns=[c], errors="ignore")
                mask = y.notna()
                fallback = float(y.median()) if is_num else (y.mode().iloc[0] if not y.mode().empty else "__MISSING__")
                self.imputers_[c] = {"strategy": "ml", "fallback": fallback}

                if mask.sum() < 10 or X.shape[1] == 0:
                    out[c].fillna(fallback, inplace=True)
                else:
                    Model = RandomForestRegressor if is_num else RandomForestClassifier
                    model = Model(n_estimators=50, random_state=self.random_state)
                    try:
                        model.fit(X[mask].fillna(X.mean()), y[mask])
                        X_missing = X[~mask].fillna(X.mean())
                        out.loc[~mask, c] = model.predict(X_missing)
                        # model NOT saved on purpose
                    except Exception:
                        out[c].fillna(fallback, inplace=True)

            # fallback
            else:
                fallback = float(out[c].median()) if is_num else (out[c].mode().iloc[0] if not out[c].mode().empty else "__MISSING__")
                out[c].fillna(fallback, inplace=True)
                self.imputers_[c] = {"strategy": "fallback", "value": fallback}

        return out

    def _compute_outlier_bounds(self, df: pd.DataFrame) -> None:
        for c in self.continuous_cols_:
            vals = pd.to_numeric(df[c], errors="coerce").dropna()
            if vals.empty:
                continue
            q1, q3 = np.percentile(vals, [25, 75])
            iqr = q3 - q1
            self.outlier_bounds_[c] = (q1 - self.outlier_iqr_multiplier * iqr, q3 + self.outlier_iqr_multiplier * iqr)

    def _create_outlier_flags(self, df: pd.DataFrame) -> pd.DataFrame:
        flags = pd.DataFrame(index=df.index)
        for c, (low, high) in self.outlier_bounds_.items():
            vals = pd.to_numeric(df[c], errors="coerce")
            flags[f"{c}_outlier"] = ((vals < low) | (vals > high)).astype(int)
        return flags

    def _onehot_encode(self, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
        if not self.categorical_cols_:
            return df.copy(), pd.DataFrame(index=df.index)

        cat = df[self.categorical_cols_].fillna("__NA__").astype(str)
        self.encoder_ = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
        arr = self.encoder_.fit_transform(cat)
        cols = list(self.encoder_.get_feature_names_out(self.categorical_cols_))
        enc_df = pd.DataFrame(arr, columns=cols, index=df.index)
        base = df.drop(columns=self.categorical_cols_, errors="ignore")
        return base, enc_df

    def _scale(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Scale continuous columns using QuantileTransformer (Normal).
        """
        if not self.continuous_cols_:
            return df

        if not self.is_fitted_:
            # Initialize with Gaussian output distribution
            self.scaler_ = QuantileTransformer(
                output_distribution="normal", 
                random_state=self.random_state
            )
            self.scaler_.fit(df[self.continuous_cols_])

        scaled_data = self.scaler_.transform(df[self.continuous_cols_])
        scaled_df = df.copy()
        scaled_df[self.continuous_cols_] = scaled_data

        return scaled_df

    def _apply_pca(self, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
        if self.n_pca_components <= 0:
            return df.copy(), pd.DataFrame(index=df.index)
        cont_present = [c for c in self.continuous_cols_ if c in df.columns]
        if not cont_present:
            return df.copy(), pd.DataFrame(index=df.index)
        n = min(self.n_pca_components, len(cont_present))
        self.pca_ = PCA(n_components=n, random_state=self.random_state)
        comps = self.pca_.fit_transform(df[cont_present])
        cols = [f"PCA_{i+1}" for i in range(n)]
        pca_df = pd.DataFrame(comps, columns=cols, index=df.index)
        return df.copy(), pca_df

    # ----------------- Utility -----------------
    def get_column_info(self) -> Dict[str, Any]:
        return {
            "original_columns": self.original_columns_,
            "continuous_columns": self.continuous_cols_,
            "categorical_columns": self.categorical_cols_,
            "binary_columns": self.binary_cols_,
            "long_text_columns": self.long_text_cols_,
            "outlier_bounds": self.outlier_bounds_,
            "feature_names": self.feature_names_,
            "is_fitted": self.is_fitted_,
        }

    def get_output_info(self) -> list:
        """
        Returns metadata about the output columns, specifically for categorical features.
        Used by CTGAN Conditional Sampling.
        
        Returns:
            list of dicts: [
                {'name': 'col_name', 'num_categories': 3, 'start_idx': 4, 'end_idx': 7},
                ...
            ]
        """
        if not self.is_fitted_ or not self.encoder_:
            return []

        info = []
        # Calculate start index based on feature blocks in fit_transform
        # Order: 1. Continuous, 2. Categorical (Encoded), 3. PCA, 4. Outlier, 5. Long Text
        
        current_idx = 0
        if self.continuous_cols_:
            current_idx += len(self.continuous_cols_)
            
        # Iterate over encoder categories (guaranteed to match categorical_cols_ order)
        if self.categorical_cols_:
            for i, col in enumerate(self.categorical_cols_):
                if i < len(self.encoder_.categories_):
                    cats = self.encoder_.categories_[i]
                    n_cats = len(cats)
                    info.append({
                        'name': col,
                        'num_categories': n_cats,
                        'start_idx': current_idx,
                        'end_idx': current_idx + n_cats
                    })
                    current_idx += n_cats
                    
        return info
