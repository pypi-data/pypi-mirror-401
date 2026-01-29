import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from tqdm import tqdm
import numpy as np
from ..models.encoder import TVAEEncoder
from ..models.decoder import TVAEDecoder
from ..samplers.sampler import TVAESampler


class TVAETrainer:
    def __init__(self, config):
        self.config = config
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.n_cont = len(config.continuous_dims) if config.continuous_dims else 0
        self.n_cat = sum(config.categorical_dims) if config.categorical_dims else 0
        self.categorical_dims = config.categorical_dims if config.categorical_dims else []
        self.input_dim = self.n_cont + self.n_cat
        self.latent_dim = config.latent_dim
        self.encoder = TVAEEncoder(self.input_dim, self.latent_dim, config).to(
            self.device
        )
        self.decoder = TVAEDecoder(
            self.latent_dim, self.input_dim, config, self.n_cont, self.n_cat
        ).to(self.device)
        self.sampler = TVAESampler(config)
        self.optimizer = optim.Adam(
            list(self.encoder.parameters()) + list(self.decoder.parameters()),
            lr=config.learning_rate,
            weight_decay=getattr(config, "weight_decay", 1e-5),
        )

        # Output info for reshaping generation output
        self.output_info = None

    def fit(self, data, epochs=1000, verbose=True, output_info=None):
        """Fit the TVAE model.

        Args:
            data: Training data (numpy array, preprocessed)
            epochs: Number of epochs
            verbose: Show progress
            output_info: List of categorical group info from preprocessor
        """
        self.output_info = output_info or []

        # Convert to tensor and create DataLoader for batch training
        data_tensor = torch.tensor(data, dtype=torch.float32)
        dataset = TensorDataset(data_tensor)
        batch_size = getattr(self.config, 'batch_size', 500)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True, pin_memory=True)

        losses = {"recon": [], "kl": [], "total": [], "kl_weight": []}

        # Use tqdm for epoch progress
        epoch_iterator = tqdm(range(epochs), desc="Training TVAE", disable=not verbose)

        for epoch in epoch_iterator:
            self.encoder.train()
            self.decoder.train()

            epoch_recon_loss = 0.0
            epoch_kl_loss = 0.0
            epoch_total_loss = 0.0
            num_batches = 0

            # Batch training loop with tqdm
            batch_iterator = tqdm(dataloader, desc=f"Epoch {epoch+1}/{epochs}",
                                 leave=False, disable=not verbose)

            for batch_data in batch_iterator:
                batch_data = batch_data[0].to(self.device)

                self.optimizer.zero_grad()

                # Encode
                mu, logvar = self.encoder(batch_data)
                std = torch.exp(0.5 * logvar)
                eps = torch.randn_like(std)
                z = mu + eps * std

                # Decode
                recon = self.decoder(z)

                # Compute reconstruction loss
                recon_loss = self._compute_reconstruction_loss(recon, batch_data)

                # KL loss (standard Gaussian prior)
                kl_loss = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp()) / batch_data.size(0)

                # KL annealing warmup
                kl_weight = self._compute_kl_weight(epoch, epochs)

                # Apply Beta scaling if config has it
                beta = getattr(self.config, 'beta', 1.0)
                kl_loss_scaled = beta * kl_loss

                # Monitor and prevent posterior collapse
                if epoch > 50 and kl_loss.item() < 1e-4:
                    # If KL is too small, increase the weight temporarily
                    kl_weight = min(kl_weight * 2.0, 2.0)

                total_loss = recon_loss + kl_weight * kl_loss_scaled

                total_loss.backward()

                # Gradient clipping for stability
                torch.nn.utils.clip_grad_norm_(
                    list(self.encoder.parameters()) + list(self.decoder.parameters()),
                    max_norm=1.0
                )

                self.optimizer.step()

                epoch_recon_loss += recon_loss.item()
                epoch_kl_loss += kl_loss.item()
                epoch_total_loss += total_loss.item()
                num_batches += 1

                # Update batch progress
                batch_iterator.set_postfix({
                    'loss': f'{total_loss.item():.4f}',
                    'recon': f'{recon_loss.item():.4f}',
                    'kl': f'{kl_loss.item():.4f}'
                })

            # Average losses for epoch
            avg_recon = epoch_recon_loss / num_batches if num_batches > 0 else 0.0
            avg_kl = epoch_kl_loss / num_batches if num_batches > 0 else 0.0
            avg_total = epoch_total_loss / num_batches if num_batches > 0 else 0.0

            losses["recon"].append(avg_recon)
            losses["kl"].append(avg_kl)
            losses["total"].append(avg_total)
            losses["kl_weight"].append(kl_weight)

            # Update epoch progress bar
            epoch_iterator.set_postfix({
                'loss': f'{avg_total:.4f}',
                'recon': f'{avg_recon:.4f}',
                'kl': f'{avg_kl:.4f}',
                'kl_w': f'{kl_weight:.3f}'
            })

        if verbose:
            print(f"\nTraining complete! Final loss: {losses['total'][-1]:.4f}")

        return losses

    def _compute_reconstruction_loss(self, recon, target):
        """Compute reconstruction loss properly for continuous and categorical features.

        According to TVAE paper:
        - Continuous: MSE loss
        - Categorical: CrossEntropyLoss (not BCEWithLogitsLoss)
        """
        if isinstance(recon, tuple):
            # Multi-head decoder returns (cont_out, cat_out)
            recon_cont, recon_cat = recon
            target_cont = target[:, :self.n_cont] if self.n_cont > 0 else None
            target_cat = target[:, self.n_cont:] if self.n_cat > 0 else None

            loss = 0.0

            # Continuous loss: MSE
            if self.n_cont > 0 and target_cont is not None:
                mse_loss = nn.MSELoss()(recon_cont, target_cont)
                loss += mse_loss

            # Categorical loss: CrossEntropyLoss
            if self.n_cat > 0 and target_cat is not None:
                # Convert one-hot to class indices for CrossEntropyLoss
                cat_indices = torch.argmax(target_cat, dim=1)
                ce_loss = nn.CrossEntropyLoss()(recon_cat, cat_indices)
                loss += ce_loss

            return loss
        else:
            # Single-head decoder returns concatenated output
            if self.n_cat > 0 and self.n_cont > 0:
                recon_cont = recon[:, :self.n_cont]
                recon_cat = recon[:, self.n_cont:]
                target_cont = target[:, :self.n_cont]
                target_cat = target[:, self.n_cont:]

                # Continuous: MSE
                mse_loss = nn.MSELoss()(recon_cont, target_cont)

                # Categorical: CrossEntropyLoss
                cat_indices = torch.argmax(target_cat, dim=1)
                ce_loss = nn.CrossEntropyLoss()(recon_cat, cat_indices)

                return mse_loss + ce_loss
            elif self.n_cat > 0:
                # Only categorical
                cat_indices = torch.argmax(target, dim=1)
                return nn.CrossEntropyLoss()(recon, cat_indices)
            else:
                # Only continuous
                return nn.MSELoss()(recon, target)

    def generate(self, n_samples):
        """Generate synthetic samples."""
        self.encoder.eval()
        self.decoder.eval()

        with torch.no_grad():
            z = self.sampler.sample(n_samples, device=self.device)
            samples = self.decoder(z)

            if isinstance(samples, tuple):
                # Multi-head decoder
                recon_cont, recon_cat = samples

                # Continuous: use as-is (already normalized)
                cont_samples = recon_cont.cpu().numpy()

                # Categorical: apply softmax and convert to one-hot
                cat_logits = recon_cat.cpu().numpy()
                cat_samples = self._logits_to_onehot(cat_logits)

                samples = np.concatenate([cont_samples, cat_samples], axis=1)
            else:
                # Single-head decoder
                samples = samples.cpu().numpy()

                # Process categorical part if present
                if self.n_cat > 0:
                    cont_part = samples[:, :self.n_cont] if self.n_cont > 0 else np.array([]).reshape(n_samples, 0)
                    cat_part = samples[:, self.n_cont:]

                    # Convert categorical logits to one-hot
                    cat_onehot = self._logits_to_onehot(cat_part)

                    if self.n_cont > 0:
                        samples = np.concatenate([cont_part, cat_onehot], axis=1)
                    else:
                        samples = cat_onehot

            return samples

    def _logits_to_onehot(self, logits):
        """Convert logits to one-hot encoding using softmax + argmax."""
        # Apply softmax
        exp_logits = np.exp(logits - np.max(logits, axis=1, keepdims=True))
        probs = exp_logits / exp_logits.sum(axis=1, keepdims=True)

        # Convert to one-hot
        n_samples, n_classes = logits.shape
        one_hot = np.zeros((n_samples, n_classes))

        if self.output_info and self.categorical_dims:
            # Process each categorical group separately
            start_idx = 0
            for cardinality in self.categorical_dims:
                end_idx = start_idx + cardinality
                group_probs = probs[:, start_idx:end_idx]
                argmax_idx = np.argmax(group_probs, axis=1)
                one_hot[np.arange(n_samples), start_idx + argmax_idx] = 1.0
                start_idx = end_idx
        else:
            # Simple argmax for all
            argmax_idx = np.argmax(probs, axis=1)
            one_hot[np.arange(n_samples), argmax_idx] = 1.0

        return one_hot

    def save_model(self, filepath, **kwargs):
        """Save the trained model with optional metadata"""
        save_dict = {
            "encoder": self.encoder.state_dict(),
            "decoder": self.decoder.state_dict(),
        }
        save_dict.update(kwargs)
        torch.save(save_dict, filepath)

    def load_model(self, filepath):
        """Load a trained model"""
        try:
            checkpoint = torch.load(filepath, map_location=self.device, weights_only=False)
        except (TypeError, AttributeError):
            checkpoint = torch.load(filepath, map_location=self.device)

        self.encoder.load_state_dict(checkpoint["encoder"])
        self.decoder.load_state_dict(checkpoint["decoder"])

    def get_feature_importance(self):
        # Placeholder
        return {}

    def _compute_kl_weight(self, epoch, total_epochs):
        """Compute KL weight with warmup (improved annealing).

        According to TVAE paper and best practices:
        - Start with low KL weight to allow reconstruction to learn
        - Gradually increase to prevent posterior collapse
        - Use warmup period (typically 50-100 epochs)
        """
        warmup_epochs = getattr(self.config, 'warmup_epochs', 50)
        max_kl_weight = getattr(self.config, 'max_kl_weight', 1.0)

        if epoch < warmup_epochs:
            # Linear warmup: gradually increase KL weight
            return (epoch / warmup_epochs) * max_kl_weight
        else:
            return max_kl_weight
