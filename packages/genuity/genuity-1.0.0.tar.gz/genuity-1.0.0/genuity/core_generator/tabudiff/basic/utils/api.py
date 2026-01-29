"""
High-level API for TabuDiff basic: train from CSV and generate CSV.
"""

import os
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from ..config.config import TabuDiffConfig
from .factory import TabuDiffFactory


class TabuDiffAPI:
    def __init__(self, config: TabuDiffConfig | None = None):
        self.config = config or TabuDiffConfig()
        self.factory = TabuDiffFactory()
        self.score_model: nn.Module | None = None
        self.scheduler = None
        self.data_mean = None
        self.data_std = None
        self.data_min = None
        self.data_max = None
        self.column_names = None

    def fit(self, data: pd.DataFrame | np.ndarray | torch.Tensor, verbose: bool = True) -> nn.Module:
        """Fit model to data (DataFrame, Numpy, or Tensor)."""
        from tqdm import tqdm
        torch.manual_seed(self.config.seed)

        # Handle various input types
        if isinstance(data, pd.DataFrame):
            self.column_names = data.columns.tolist()
            data_tensor = torch.tensor(data.values, dtype=torch.float32, device=self.config.device)
            # Capture range for DataFrame mode specifically? 
            # Or just rely on tensor values.
            self.data_max = torch.tensor(data.max().values, dtype=torch.float32, device=self.config.device)
             # Note: data.min() usually not needed for simple clamp if we assume standard 
        elif isinstance(data, np.ndarray):
            data_tensor = torch.tensor(data, dtype=torch.float32, device=self.config.device)
            # Capture range
            self.data_max = data_tensor.max(dim=0)[0] # Tensor min/max
        elif isinstance(data, torch.Tensor):
            data_tensor = data.to(dtype=torch.float32, device=self.config.device)
            self.data_max = data_tensor.max(dim=0)[0]
        else:
            raise ValueError("Data must be DataFrame, Numpy array, or Torch Tensor")

        # Normalize
        if self.config.normalize_data:
            self.data_mean = data_tensor.mean(dim=0, keepdim=True)
            self.data_std = data_tensor.std(dim=0, keepdim=True) + 1e-8
            data_tensor = (data_tensor - self.data_mean) / self.data_std
        
        # Capture Min after normalization? No, usually before or after? 
        # Code used to capture max before normalization for clamping?
        # Previous code: `self.data_max = torch.tensor(df.max().values...)` -> This is REAL data max.
        # Then `self.data_min` was captured in `_df_to_tensor` comments but ignored?
        # Actually `data_min` was only used in generate for clamping.
        
        # Consistent Range Capture (Real Data)
        if hasattr(data, 'values'):
             pass # Already done for DF
        elif isinstance(data, (np.ndarray, torch.Tensor)):
             # We should capture real data min/max for clamping later
             if isinstance(data, np.ndarray):
                 t = torch.tensor(data, device=self.config.device)
             else:
                 t = data
             self.data_min = t.min(dim=0)[0]
             self.data_max = t.max(dim=0)[0]

        feature_dim = data_tensor.shape[1]

        self.scheduler = self.factory.create_scheduler(self.config)
        self.score_model = self.factory.create_score_network(self.config, feature_dim)

        optimizer = optim.Adam(
            self.score_model.parameters(), lr=self.config.learning_rate
        )
        self.score_model.train()

        num_batches = max(
            1, (len(data_tensor) + self.config.batch_size - 1) // self.config.batch_size
        )

        if verbose:
            print(f"Training TabuDiff for {self.config.num_epochs} epochs")
            print(f"   Data shape: {data_tensor.shape}")
            print(f"   Batch size: {self.config.batch_size}")
            print(f"   Batches per epoch: {num_batches}")

        epoch_iterator = tqdm(
            range(self.config.num_epochs), 
            desc="Training", 
            disable=not verbose
        )

        for epoch in epoch_iterator:
            epoch_loss = 0.0
            perm = torch.randperm(len(data_tensor), device=self.config.device)

            for b in range(num_batches):
                idx = perm[
                    b * self.config.batch_size : (b + 1) * self.config.batch_size
                ]
                x0 = data_tensor[idx]

                t_indices = torch.randint(
                    0,
                    self.scheduler.num_steps,
                    (x0.size(0),),
                    device=self.config.device,
                )
                betas = self.scheduler.betas[t_indices]
                alpha_bars = self.scheduler.alphas_cumprod[t_indices]

                eps = torch.randn_like(x0)
                xt = (
                    torch.sqrt(alpha_bars).unsqueeze(1) * x0
                    + torch.sqrt(1 - alpha_bars).unsqueeze(1) * eps
                )

                t_cont = t_indices.float() / (self.scheduler.num_steps - 1)
                eps_theta = self.score_model(xt, t_cont.unsqueeze(1))

                loss = torch.mean((eps_theta - eps) ** 2)
                epoch_loss += loss.item()

                optimizer.zero_grad(set_to_none=True)
                loss.backward()

                if self.config.clip_gradients:
                    torch.nn.utils.clip_grad_norm_(
                        self.score_model.parameters(), self.config.gradient_clip_value
                    )

                optimizer.step()

            avg_loss = epoch_loss / num_batches
            epoch_iterator.set_postfix({'loss': f'{avg_loss:.4f}'})

        if verbose:
            print(f"Training complete! Final loss: {avg_loss:.6f}")

        return self.score_model

    def fit_dataframe(self, df: pd.DataFrame, verbose: bool = True) -> nn.Module:
        return self.fit(df, verbose=verbose)

    def fit_csv(self, csv_path: str) -> nn.Module:
        df = pd.read_csv(csv_path)
        return self.fit_dataframe(df)

    def generate_dataframe(self, num_samples: int | None = None) -> pd.DataFrame:
        if self.score_model is None or self.scheduler is None:
            raise RuntimeError("Model not trained. Call fit_dataframe or load first.")
        if num_samples is None:
            num_samples = self.config.num_samples

        print(f"Generating {num_samples} synthetic samples...")

        sampler = self.factory.create_sampler(
            self.config, self.score_model, self.scheduler
        )
        with torch.no_grad():
            samples = sampler.sample(
                num_samples=num_samples,
                feature_dim=self.score_model.net[-1].out_features,
            )

        # Denormalize if data was normalized during training
        if (
            self.config.normalize_data
            and self.data_mean is not None
            and self.data_std is not None
        ):
            samples = samples * self.data_std + self.data_mean

        if self.data_min is not None and self.data_max is not None:
             samples = torch.max(torch.min(samples, self.data_max), self.data_min)

        df_syn = pd.DataFrame(samples.cpu().numpy())
        if self.column_names is not None and len(self.column_names) == df_syn.shape[1]:
            df_syn.columns = self.column_names
        return df_syn

    def save(self, path: str | None = None):
        """Save the model with all metadata for reconstruction"""
        if self.score_model is None:
            raise RuntimeError("Nothing to save. Train or load first.")
        if path is None:
            path = self.config.model_save_path
            
        save_dict = {
            "state_dict": self.score_model.state_dict(),
            "data_min": self.data_min.tolist() if self.data_min is not None else None,
            "data_max": self.data_max.tolist() if self.data_max is not None else None,
            "data_mean": self.data_mean.tolist() if self.data_mean is not None else None,
            "data_std": self.data_std.tolist() if self.data_std is not None else None,
            "column_names": self.column_names,
            "feature_dim": self.score_model.net[-1].out_features
        }
        torch.save(save_dict, path)
        return path

    def load(self, feature_dim: int | None = None, path: str | None = None) -> nn.Module:
        """Load a saved model and restore metadata"""
        if path is None:
            path = self.config.model_save_path
            
        try:
            checkpoint = torch.load(path, map_location=self.config.device, weights_only=True)
        except (TypeError, AttributeError):
            checkpoint = torch.load(path, map_location=self.config.device)
            
        # If it's old style (just state_dict), checkpoint is the state_dict
        if "state_dict" in checkpoint:
            state_dict = checkpoint["state_dict"]
            f_dim = feature_dim or checkpoint.get("feature_dim")
            if f_dim is None:
                raise ValueError("feature_dim must be provided to load old-style models")
            
            self.score_model = self.factory.create_score_network(self.config, f_dim)
            self.score_model.load_state_dict(state_dict)
            
            # Restore metadata if available
            if checkpoint.get("data_min") is not None:
                self.data_min = torch.tensor(checkpoint["data_min"], device=self.config.device)
            if checkpoint.get("data_max") is not None:
                self.data_max = torch.tensor(checkpoint["data_max"], device=self.config.device)
            if checkpoint.get("data_mean") is not None:
                self.data_mean = torch.tensor(checkpoint["data_mean"], device=self.config.device)
            if checkpoint.get("data_std") is not None:
                self.data_std = torch.tensor(checkpoint["data_std"], device=self.config.device)
            self.column_names = checkpoint.get("column_names")
        else:
            # Old style load
            if feature_dim is None:
                raise ValueError("feature_dim must be provided to load old-style models")
            self.score_model = self.factory.create_score_network(self.config, feature_dim)
            self.score_model.load_state_dict(checkpoint)

        self.score_model.eval()
        self.scheduler = self.factory.create_scheduler(self.config)
        return self.score_model

    def fit_csv_and_generate_csv(
        self, input_csv: str, output_csv: str, num_samples: int | None = None
    ) -> str:
        df = pd.read_csv(input_csv)
        self.fit_dataframe(df)
        df_syn = self.generate_dataframe(num_samples=num_samples)
        df_syn.to_csv(output_csv, index=False)
        return output_csv
