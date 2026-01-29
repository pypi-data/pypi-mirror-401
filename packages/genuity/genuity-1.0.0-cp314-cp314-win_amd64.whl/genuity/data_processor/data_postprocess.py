# data_postprocess.py
"""
TabularPostprocessor

Reconstructs original DataFrame from the preprocessed output created by TabularPreprocessor.
- tolerant to extra columns (PCA, outlier flags, etc.)
- re-applies original NaNs using missing_mask_ stored in preprocessor
- uses saved encoder/scaler/pca to inverse-transform when possible
"""
from typing import Optional, Dict, Any
import pandas as pd
import numpy as np
import joblib


class TabularPostprocessor:
    def __init__(self, preprocessor_path: Optional[str] = None, preprocessor_object: Optional[object] = None, verbose: bool = True):
        if (preprocessor_path is None) and (preprocessor_object is None):
            raise ValueError("Provide either preprocessor_path or preprocessor_object")

        if preprocessor_path:
            bundle = joblib.load(preprocessor_path)
            cfg = bundle.get("config", {})
            st = bundle.get("state", bundle)
            # Populate fields
            self.original_columns = st.get("original_columns_", [])
            self.continuous_cols = st.get("continuous_cols_", [])
            self.categorical_cols = st.get("categorical_cols_", [])
            self.binary_cols = st.get("binary_cols_", [])
            self.long_text_cols = st.get("long_text_cols_", [])
            self.outlier_bounds = st.get("outlier_bounds_", {})
            self.missing_mask = st.get("missing_mask_", {})
            self.imputers = st.get("imputers_", {})
            self.encoder = st.get("encoder_", None)
            self.scaler = st.get("scaler_", None)
            self.pca = st.get("pca_", None)
            self.feature_names = st.get("feature_names_", [])
        else:
            # preprocessor_object assumed to be a fitted TabularPreprocessor instance
            pre = preprocessor_object
            self.original_columns = getattr(pre, "original_columns_", [])
            self.continuous_cols = getattr(pre, "continuous_cols_", [])
            self.categorical_cols = getattr(pre, "categorical_cols_", [])
            self.binary_cols = getattr(pre, "binary_cols_", [])
            self.long_text_cols = getattr(pre, "long_text_cols_", [])
            self.outlier_bounds = getattr(pre, "outlier_bounds_", {})
            self.missing_mask = getattr(pre, "missing_mask_", {})
            self.imputers = getattr(pre, "imputers_", {})
            self.encoder = getattr(pre, "encoder_", None)
            self.scaler = getattr(pre, "scaler_", None)
            self.pca = getattr(pre, "pca_", None)
            self.feature_names = getattr(pre, "feature_names_", [])

        self.verbose = verbose

    def _log(self, *args, **kwargs):
        if self.verbose:
            print("[TabularPostprocessor]", *args, **kwargs)

    def inverse_transform_modified_data(self, modified_df: pd.DataFrame) -> pd.DataFrame:
        """
        Reconstruct the original DataFrame from `modified_df` which is expected to be
        output of the preprocessor (or similar). This is robust to the presence/absence
        of PCA columns or direct scaled continuous columns.
        """
        if modified_df is None or not isinstance(modified_df, pd.DataFrame):
            raise ValueError("modified_df must be a pandas DataFrame")

        recon = pd.DataFrame(index=modified_df.index)

        # 1) Continuous reconstruction:
        # prefer direct continuous (scaled) columns if present
        cont_present = [c for c in self.continuous_cols if c in modified_df.columns]
        if cont_present and (self.scaler is not None):
            # Handle case where CTGAN output may have subset of continuous columns
            # Rebuild full array with correct column order for scaler
            n_rows = len(modified_df)
            full_arr = np.zeros((n_rows, len(self.continuous_cols)), dtype=np.float32)
            
            for i, col in enumerate(self.continuous_cols):
                if col in cont_present:
                    full_arr[:, i] = modified_df[col].values.astype(np.float32)
                    
            try:
                inv = self.scaler.inverse_transform(full_arr)
                # Only keep columns that were actually present
                recon_cont = pd.DataFrame(inv, columns=self.continuous_cols, index=modified_df.index)
                recon_cont = recon_cont[cont_present]  # Filter to only present cols
                
                # Clip to original data range to prevent out-of-range values
                # QuantileTransformer stores data_min_ and data_max_ after fit
                if hasattr(self.scaler, 'quantiles_'):
                    # For QuantileTransformer: use first and last quantile as bounds
                    for i, col in enumerate(cont_present):
                        col_idx = self.continuous_cols.index(col)
                        min_val = self.scaler.quantiles_[0, col_idx]
                        max_val = self.scaler.quantiles_[-1, col_idx]
                        recon_cont[col] = recon_cont[col].clip(lower=min_val, upper=max_val)
                    self._log("Applied range clipping to continuous columns.")
                
                recon = pd.concat([recon, recon_cont], axis=1)
                self._log("Reconstructed continuous from direct scaled columns.")
            except Exception as e:
                self._log(f"Scaler inverse_transform failed: {e}. Using raw values.")
                recon_cont = modified_df[cont_present].copy()
                recon = pd.concat([recon, recon_cont], axis=1)
        else:
            # try PCA inverse (if available)
            pca_cols = [c for c in modified_df.columns if str(c).startswith("PCA_")]
            if pca_cols and (self.pca is not None):
                # ensure correct order PCA_1..PCA_n
                pca_cols_sorted = sorted(pca_cols, key=lambda x: int(x.split("_")[1]))
                comps = modified_df[pca_cols_sorted].values
                inv_scaled = self.pca.inverse_transform(comps)
                cont_order = [c for c in self.continuous_cols]
                inv_df = pd.DataFrame(inv_scaled, columns=cont_order, index=modified_df.index)
                if self.scaler is not None:
                    inv_unscaled = self.scaler.inverse_transform(inv_df.values)
                    recon_cont = pd.DataFrame(inv_unscaled, columns=cont_order, index=modified_df.index)
                else:
                    recon_cont = inv_df
                recon = pd.concat([recon, recon_cont], axis=1)
                self._log("Reconstructed continuous from PCA -> inverse scale.")
            else:
                self._log("No continuous or PCA columns available for continuous reconstruction.")

        # 2) Categorical reconstruction via argmax decoding
        # CTGAN outputs continuous values (not strict 0/1), so argmax is more reliable
        if self.encoder is not None:
            try:
                expected = list(self.encoder.get_feature_names_out(self.categorical_cols))
            except Exception:
                expected = list(self.encoder.get_feature_names_out())
            
            # Use argmax-based decoding for each original categorical column
            fallback_cols = {}
            for orig_col in self.categorical_cols:
                # Find all one-hot columns for this categorical
                group = [col for col in expected if col.startswith(f"{orig_col}_")]
                if not group:
                    continue
                    
                # Build matrix for this group
                sub = np.zeros((len(modified_df), len(group)))
                for k, gcol in enumerate(group):
                    if gcol in modified_df.columns:
                        sub[:, k] = modified_df[gcol].astype(float).values
                
                # Argmax to get category index
                idx = np.argmax(sub, axis=1)
                
                # Map back to original category names
                cats = [g.split(f"{orig_col}_", 1)[1] for g in group]
                decoded = [cats[i] if i < len(cats) else np.nan for i in idx]
                
                # Convert __NA__ placeholders
                decoded = [np.nan if str(d) == "__NA__" else d for d in decoded]
                fallback_cols[orig_col] = decoded
            
            if fallback_cols:
                inv_df = pd.DataFrame(fallback_cols, index=modified_df.index)
                recon = pd.concat([recon, inv_df], axis=1)
                self._log("Inverse one-hot encoded categorical columns.")

        else:
            # No encoder available: copy any original categorical/binary columns if present in modified_df
            for c in (self.categorical_cols + self.binary_cols if hasattr(self, "binary_cols") else []):
                if c in modified_df.columns and c not in recon.columns:
                    recon[c] = modified_df[c]

        # 3) Long-text pass-through: copy as-is if present
        for col in self.long_text_cols:
            if col in modified_df.columns and col not in recon.columns:
                recon[col] = modified_df[col]

        # 4) Copy any remaining original columns present in modified_df
        for c in self.original_columns:
            if (c not in recon.columns) and (c in modified_df.columns):
                recon[c] = modified_df[c]

        # 5) Attempt to convert object columns to numeric/boolean if valid
        for col in recon.columns:
            if recon[col].dtype == 'object':
                # Check for boolean strings
                unique_vals = set(recon[col].dropna().unique())
                if unique_vals <= {'True', 'False', 'true', 'false'}:
                    recon[col] = recon[col].map({'True': True, 'False': False, 'true': True, 'false': False})
                else:
                    try:
                        recon[col] = pd.to_numeric(recon[col])
                    except (ValueError, TypeError):
                        # Could not convert, keep as object
                        pass

        # 6) Reorder columns to original order if possible
        ordered = [c for c in self.original_columns if c in recon.columns]
        if ordered:
            recon = recon[ordered]
        else:
            recon = recon.reindex(sorted(recon.columns), axis=1)

        # 7) Truncate (round) every value to 3 decimal places
        # Apply only to numeric columns to avoid errors on object columns that can't be rounded
        numeric_cols = recon.select_dtypes(include=[np.number]).columns
        if not numeric_cols.empty:
            recon[numeric_cols] = recon[numeric_cols].round(3)

        self._log("Inverse reconstruction complete. shape:", recon.shape)
        return recon

    def transform_new_data(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Transform raw new data using the saved preprocessor state:
        - Impute using stored imputers (for 'ml' use fallback)
        - Make outlier flags
        - Scale continuous (MinMax)
        - PCA (if available)
        - One-hot encode categoricals aligning to encoder's expected columns
        """
        if df is None or not isinstance(df, pd.DataFrame):
            raise ValueError("transform_new_data expects a pandas DataFrame")

        out = df.copy()

        # impute per stored imputers
        for col, info in self.imputers.items():
            if col in out.columns:
                if info.get("strategy") == "ml":
                    fallback = info.get("fallback", np.nan)
                    out[col] = out[col].fillna(fallback)
                elif info.get("strategy") in {"mean", "median", "mode", "constant", "fallback", "quantile"}:
                    val = info.get("value", info.get("fallback", np.nan))
                    out[col] = out[col].fillna(val)
                else:
                    val = info.get("value", info.get("fallback", np.nan))
                    out[col] = out[col].fillna(val)

        # outlier flags
        flags = pd.DataFrame(index=out.index)
        for c, (low, high) in self.outlier_bounds.items():
            if c in out.columns:
                vals = pd.to_numeric(out[c], errors="coerce")
                flags[f"{c}_outlier"] = ((vals < low) | (vals > high)).astype(int)

        # scale continuous
        scaled = out.copy()
        cont_present = [c for c in self.continuous_cols if c in out.columns]
        if cont_present and (self.scaler is not None):
            scaled[cont_present] = self.scaler.transform(out[cont_present])

        # pca features
        pca_df = pd.DataFrame(index=out.index)
        if cont_present and (self.pca is not None):
            comps = self.pca.transform(scaled[cont_present])
            cols = [f"PCA_{i+1}" for i in range(self.pca.n_components_)]
            pca_df = pd.DataFrame(comps, columns=cols, index=out.index)

        # one-hot encode categorical aligning to encoder's expected inputs
        enc_df = pd.DataFrame(index=out.index)
        if (self.encoder is not None) and (hasattr(self, "categorical_cols")) and self.categorical_cols:
            # ensure we provide all categorical columns to encoder.transform in the same order it was trained
            cats = []
            for c in self.categorical_cols:
                if c in out.columns:
                    cats.append(out[c].fillna("__NA__").astype(str))
                else:
                    # create a series of placeholder
                    cats.append(pd.Series(["__NA__"] * len(out), index=out.index))
            cat_df = pd.concat(cats, axis=1)
            cat_df.columns = self.categorical_cols
            try:
                arr = self.encoder.transform(cat_df)
                expected = list(self.encoder.get_feature_names_out(self.categorical_cols))
                enc_df = pd.DataFrame(arr, columns=expected, index=out.index)
            except Exception as e:
                # fallback: create zero-matrix for expected columns
                try:
                    expected = list(self.encoder.get_feature_names_out(self.categorical_cols))
                except Exception:
                    expected = []
                enc_df = pd.DataFrame(np.zeros((len(out), len(expected))), columns=expected, index=out.index)

        # assemble
        parts = []
        if cont_present:
            parts.append(scaled[cont_present])
        if not enc_df.empty:
            parts.append(enc_df)
        if not pca_df.empty:
            parts.append(pca_df)
        if not flags.empty:
            parts.append(flags)
        # long text pass-through if present
        long_text_df = out[self.long_text_cols].copy() if self.long_text_cols else pd.DataFrame(index=out.index)
        if not long_text_df.empty:
            parts.append(long_text_df)

        pre = pd.concat(parts, axis=1) if parts else pd.DataFrame(index=out.index)

        return {
            "preprocessed": pre,
            "continuous": (scaled[cont_present] if cont_present else pd.DataFrame(index=out.index)),
            "categorical": (enc_df if not enc_df.empty else pd.DataFrame(index=out.index)),
            "pca_features": (pca_df if not pca_df.empty else pd.DataFrame(index=out.index)),
            "outlier_flags": (flags if not flags.empty else pd.DataFrame(index=out.index)),
        }

    def get_column_mapping(self) -> Dict[str, Any]:
        return {
            "original_columns": getattr(self, "original_columns", []),
            "continuous_columns": getattr(self, "continuous_cols", []),
            "categorical_columns": getattr(self, "categorical_cols", []),
            "binary_columns": getattr(self, "binary_cols", []),
            "long_text_columns": getattr(self, "long_text_cols", []),
            "outlier_bounds": getattr(self, "outlier_bounds", {}),
            "feature_names": getattr(self, "feature_names", []),
        }
