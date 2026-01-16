# Updated TabularPostprocessor
import pandas as pd
import numpy as np
import joblib
import warnings
import category_encoders as ce

import warnings
from datetime import datetime

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


class TabularPostprocessor:
    """
    Postprocessor that works with the TabularPreprocessor.
    Handles inverse transformations, predictions processing, and data reconstruction.
    Supports all encoding strategies: 'label', 'onehot', 'binary', 'embedding', 'target', 'frequency', 'hash', or None.
    """

    def __init__(self, preprocessor_path=None, preprocessor_object=None, verbose=True):
        self.verbose = verbose

        # Load serialized preprocessor state
        if preprocessor_path:
            state_bundle = joblib.load(preprocessor_path)
            self.config = state_bundle.get("config", {})
            state = state_bundle.get("state", state_bundle)
            self._print_step(f"Loaded preprocessor from {preprocessor_path}")
        elif preprocessor_object and preprocessor_object.is_fitted_:
            bundle = self._extract_preprocessor_state(preprocessor_object)
            self.config = bundle.get("config", {})
            state = bundle.get("state", bundle)
            self._print_step("Loaded preprocessor from object")
        else:
            raise ValueError(
                "Either preprocessor_path or fitted preprocessor_object must be provided"
            )

        # Extract fields from state
        self.continuous_cols = state.get("continuous_cols_", [])
        self.categorical_cols = state.get("categorical_cols_", [])
        self.binary_cols = state.get("binary_cols_", [])
        self.long_text_cols = state.get("long_text_cols_", [])
        self.datetime_cols = state.get("datetime_cols_", [])
        self.outlier_bounds = state.get("outlier_bounds_", {})
        self.pca = state.get("pca_", None)
        self.scaler = state.get("scaler_", None)
        self.imputers = state.get("imputers_", {})
        self.encoder = state.get("encoder_", None)
        self.column_mappings = state.get("column_mappings_", {})
        self.feature_names = state.get("feature_names_", [])
        self.encoding_strategy = self.config.get("encoding_strategy")
        self.handle_datetime = self.config.get("handle_datetime", False)
        # original dtypes
        raw_dtypes = state.get("original_dtypes_", {})
        self.original_dtypes = {k: pd.api.types.pandas_dtype(v) for k, v in raw_dtypes.items()}

        self._print_step("Postprocessor initialized successfully")

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

    def _extract_preprocessor_state(self, pre):
        config = {
            "cardinality_ratio_threshold": pre.cardinality_ratio_threshold,
            "outlier_iqr_multiplier": pre.outlier_iqr_multiplier,
            "text_length_threshold": pre.text_length_threshold,
            "max_char_threshold": pre.max_char_threshold,
            "n_pca_components": pre.n_pca_components,
            "scaler_type": pre.scaler_type,
            "imputation_strategy": pre.imputation_strategy,
            "encoding_strategy": pre.encoding_strategy,
            "handle_datetime": getattr(pre, "handle_datetime", False),
            "random_state": pre.random_state,
            "verbose": pre.verbose,
        }
        state = {
            "continuous_cols_": pre.continuous_cols_,
            "categorical_cols_": pre.categorical_cols_,
            "binary_cols_": pre.binary_cols_,
            "long_text_cols_": pre.long_text_cols_,
            "datetime_cols_": getattr(pre, "datetime_cols_", []),
            "outlier_bounds_": pre.outlier_bounds_,
            "pca_": pre.pca_,
            "scaler_": pre.scaler_,
            "imputers_": pre.imputers_,
            "encoder_": getattr(pre, "encoder_", None),
            "column_mappings_": pre.column_mappings_,
            "feature_names_": pre.feature_names_,
            "original_dtypes_": {k: str(v) for k, v in getattr(pre, "original_dtypes_", {}).items()},
        }
        return {"config": config, "state": state}

    def _get_ohe_feature_names(self, encoder):
        """
        Robustly obtain feature names from a fitted OneHotEncoder.
        """
        try:
            # preferred: pass input feature names if available
            if hasattr(encoder, "get_feature_names_out"):
                if hasattr(encoder, "feature_names_in_"):
                    return list(encoder.get_feature_names_out(encoder.feature_names_in_))
                else:
                    # pass nothing; some sklearn versions accept that
                    return list(encoder.get_feature_names_out())
        except Exception:
            pass
        # fallback: try to reconstruct using categories_ if available
        try:
            feat_names = []
            if hasattr(encoder, "feature_names_in_") and hasattr(encoder, "categories_"):
                for base, cats in zip(encoder.feature_names_in_, encoder.categories_):
                    feat_names.extend([f"{base}_{str(c)}" for c in cats])
                return feat_names
        except Exception:
            pass
        return []

    def inverse_transform_modified_data(self, modified_df):
        self._print_banner("Reconstructing to Original Space")
        recon = pd.DataFrame(index=modified_df.index)

        # 1. Inverse scale continuous
        cont = [c for c in self.continuous_cols if c in modified_df.columns]
        if cont and self.scaler:
            try:
                inv = self.scaler.inverse_transform(modified_df[cont])
                recon[cont] = pd.DataFrame(inv, columns=cont, index=modified_df.index)
                self._print_step("Inverse scaled continuous columns", level="SUCCESS")
            except Exception as e:
                self._print_step(f"Inverse scaling failed: {e}", level="ERROR")

        # 2. Inverse PCA to continuous
        if self.pca:
            pca_cols = [c for c in modified_df.columns if c.startswith("gen_pca_")]
            if pca_cols:
                try:
                    inv = self.pca.inverse_transform(modified_df[pca_cols].values)
                    for i, col in enumerate(self.continuous_cols):
                        if col not in recon:
                            recon[col] = inv[:, i]
                    self._print_step("Inverse PCA reconstructed continuous", level="SUCCESS")
                except Exception as e:
                    self._print_step(f"Inverse PCA failed: {e}", level="ERROR")

        # 3. Inverse encode categoricals (not binaries)
        if self.encoder and (self.encoding_strategy in ["onehot", "ordinal", "label", "embedding"]):
            if self.encoding_strategy in ["ordinal", "label", "embedding"]:
                # For ordinal/label/embedding encoding
                ordinal_cols = [col for col in self.categorical_cols if col in modified_df.columns]
                if ordinal_cols:
                    try:
                        arr = modified_df[ordinal_cols].values
                        inv = self.encoder.inverse_transform(arr)
                        recon[ordinal_cols] = pd.DataFrame(inv, columns=ordinal_cols, index=modified_df.index)
                        self._print_step("Inverse ordinal/label/embedding encoded categoricals")
                    except Exception as e:
                        self._print_step(f"Warning: inverse ordinal encoding failed: {e}")
            elif self.encoding_strategy == "onehot":
                try:
                    expected = self._get_ohe_feature_names(self.encoder)
                except Exception:
                    expected = []
                if expected:
                    # Ensure all expected encoded cols exist (fill zeros for missing)
                    for col in expected:
                        if col not in modified_df.columns:
                            modified_df[col] = 0
                    enc_input_cols = [col for col in expected if col in modified_df.columns]
                    try:
                        inv = self.encoder.inverse_transform(modified_df[enc_input_cols])
                        # inverse_transform returns 2D array with original categorical columns
                        categorical_cols = self.categorical_cols
                        recon[categorical_cols] = pd.DataFrame(inv, columns=categorical_cols, index=modified_df.index)
                        self._print_step("Inverse one-hot encoded categoricals")
                    except Exception as e:
                        self._print_step(f"Warning: inverse one-hot failed: {e}")
        elif self.encoding_strategy in ["binary", "hash", "frequency", "target"]:
            # Not generally invertible: copy encoded columns and warn
            for col in modified_df.columns:
                if col not in recon.columns:
                    recon[col] = modified_df[col]
            self._print_step(
                f"Warning: {self.encoding_strategy} encoding is not invertible. Encoded columns are copied as-is."
            )
        else:
            # direct copy back for binary or no-encoding
            for col in self.categorical_cols + self.binary_cols:
                if col in modified_df:
                    recon[col] = modified_df[col]

        # 4. Ensure binary columns are restored
        if self.binary_cols:
            for col in self.binary_cols:
                if col in modified_df and col not in recon.columns:
                    recon[col] = modified_df[col]

        # 5. Attempt to cast reconstructed columns back to original dtypes where possible
        for col, dtype in self.original_dtypes.items():
            if col in recon.columns:
                try:
                    # If original dtype was categorical-like - use pandas Categorical if possible
                    if pd.api.types.is_categorical_dtype(dtype):
                        recon[col] = recon[col].astype("category")
                    elif pd.api.types.is_datetime64_any_dtype(dtype):
                        recon[col] = pd.to_datetime(recon[col], errors="coerce")
                    else:
                        recon[col] = recon[col].astype(dtype)
                except Exception as e:
                    # If cast fails, keep best-effort and warn
                    self._print_step(f"Could not cast column {col} to {dtype}: {e}", level="WARN")

        self._print_banner("Reconstruction Complete")
        return recon

    def transform_new_data(self, df):
        self._print_banner("Transforming New Data")

        # 0. Datetime processing
        df_proc = df.copy()
        if self.handle_datetime and self.datetime_cols:
            for col in list(self.datetime_cols):
                if col in df_proc.columns:
                    # Try converting to datetime
                    try:
                        temp = pd.to_datetime(df_proc[col], errors='coerce')
                        df_proc[col] = temp
                    except (ValueError, TypeError):
                        pass

                    # Extract features
                    df_proc[f"{col}_year"] = df_proc[col].dt.year
                    df_proc[f"{col}_month"] = df_proc[col].dt.month
                    df_proc[f"{col}_day"] = df_proc[col].dt.day
                    df_proc[f"{col}_dow"] = df_proc[col].dt.dayofweek
                    df_proc.drop(columns=[col], inplace=True, errors="ignore")

        # 1. Drop long text
        df_clean = df_proc.drop(columns=self.long_text_cols, errors="ignore")

        # 2. Impute missing using stored values (skip ML models)
        df_imp = df_clean.copy()
        for col, info in self.imputers.items():
            if col in df_imp and "value" in info:
                df_imp[col].fillna(info["value"], inplace=True)

        # 3. Outlier flags
        flags = pd.DataFrame(index=df.index)
        for col, (low, high) in self.outlier_bounds.items():
            if col in df_imp:
                vals = pd.to_numeric(df_imp[col], errors="coerce")
                flags[f"{col}_outlier"] = ((vals < low) | (vals > high)).astype(int)

        # 4. Scale continuous
        df_scaled = df_imp.copy()
        if self.scaler and self.continuous_cols:
            # Ensure columns exist
            missing_cont = [c for c in self.continuous_cols if c not in df_scaled.columns]
            if missing_cont:
                # Fill missing continuous columns with 0 (safer for scaled space)
                for c in missing_cont:
                    df_scaled[c] = 0
            try:
                df_scaled[self.continuous_cols] = self.scaler.transform(
                    df_scaled[self.continuous_cols].fillna(df_scaled[self.continuous_cols].mean())
                )
            except Exception as e:
                self._print_step(f"Warning: scaling failed on new data: {e}")

        # 5. PCA
        pca_df = pd.DataFrame(index=df.index)
        if self.pca:
            try:
                comps = self.pca.transform(df_scaled[self.continuous_cols].fillna(df_scaled[self.continuous_cols].mean()))
                cols = [f"PCA_{i+1}" for i in range(self.pca.n_components_)]
                pca_df = pd.DataFrame(comps, columns=cols, index=df.index)
            except Exception as e:
                self._print_step(f"Warning: PCA transform failed for new data: {e}")

        # 6. Encode categoricals
        enc_df = pd.DataFrame(index=df.index)
        if self.encoder and self.categorical_cols:
            cols_to_encode = [col for col in self.categorical_cols if col in df_imp.columns]

            if cols_to_encode:
                try:
                    # Handle different encoder types
                    if self.encoding_strategy == "onehot":
                        arr = self.encoder.transform(df_imp[cols_to_encode])
                        # arr can be sparse
                        try:
                            cols = list(self._get_ohe_feature_names(self.encoder))
                        except Exception:
                            cols = []
                        if hasattr(arr, "toarray"):
                            arr = arr.toarray()
                        enc_df = pd.DataFrame(arr, columns=cols, index=df.index) if len(cols) == arr.shape[1] else pd.DataFrame(arr, index=df.index)
                    elif self.encoding_strategy in ["ordinal", "label", "embedding"]:
                        arr = self.encoder.transform(df_imp[cols_to_encode])
                        enc_df = pd.DataFrame(arr, columns=cols_to_encode, index=df.index)
                    elif self.encoding_strategy in ["binary", "hash", "frequency", "target"]:
                        enc_df = self.encoder.transform(df_imp[cols_to_encode])
                        enc_df.index = df.index
                except Exception as e:
                    self._print_step(f"Warning: encoding failed for new data: {e}")

        # 7. Binary columns (kept as-is)
        binary_df = pd.DataFrame(index=df.index)
        if self.binary_cols:
            existing_binary = [col for col in self.binary_cols if col in df_imp.columns]
            if existing_binary:
                binary_df = df_imp[existing_binary].copy()

        # 8. Assemble
        pre = pd.concat(
            [
                (
                    df_scaled[self.continuous_cols]
                    if self.continuous_cols
                    else pd.DataFrame(index=df.index)
                ),
                enc_df,
                binary_df,
                flags,
                pca_df,
            ],
            axis=1,
        )

        return {
            "preprocessed": pre,
            "continuous": (
                df_scaled[self.continuous_cols]
                if self.continuous_cols
                else pd.DataFrame(index=df.index)
            ),
            "categorical": enc_df,
            "binary": binary_df,
            "outlier_flags": flags,
            "pca_features": pca_df,
        }

    def get_column_mapping(self):
        return {
            "continuous_columns": self.continuous_cols,
            "categorical_columns": self.categorical_cols,
            "binary_columns": self.binary_cols,
            "dropped_text_columns": self.long_text_cols,
            "datetime_columns": self.datetime_cols,
            "outlier_bounds": self.outlier_bounds,
            "feature_names": self.feature_names,
        }

    def get_preprocessing_summary(self):
        summary = {
            "column_classification": {
                "continuous_columns": len(self.continuous_cols),
                "categorical_columns": len(self.categorical_cols),
                "binary_columns": len(self.binary_cols),
                "dropped_text_columns": len(self.long_text_cols),
                "datetime_columns": len(self.datetime_cols),
            },
            "transformations_applied": {
                "encoding": bool(self.encoding_strategy),
                "scaling": bool(self.config.get("scaler_type")),
                "pca": self.pca is not None,
                "outlier_detection": bool(self.outlier_bounds),
                "imputation": bool(self.imputers),
                "datetime_processing": self.handle_datetime,
            },
            "output_features": {
                "total_features": len(self.feature_names),
                "continuous_features": len(self.continuous_cols),
                "categorical_features": len(self.categorical_cols)
                + len(self.binary_cols),
                "outlier_flags": len(self.outlier_bounds),
                "pca_components": self.pca.n_components_ if self.pca else 0,
            },
        }
        if self.pca:
            summary["pca_info"] = {
                "n_components": self.pca.n_components_,
                "explained_variance_ratio": self.pca.explained_variance_ratio_.tolist(),
                "total_explained_variance": float(
                    self.pca.explained_variance_ratio_.sum()
                ),
            }
        return summary
