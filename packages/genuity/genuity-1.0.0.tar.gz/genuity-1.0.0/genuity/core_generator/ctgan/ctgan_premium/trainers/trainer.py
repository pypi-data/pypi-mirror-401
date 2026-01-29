import torch
import torch.nn.functional as F
import numpy as np
from collections import defaultdict
from typing import Dict, List, Union
import logging

from ..config.config import CTGANPremiumConfig
from ..models.generator import CTGANPremiumGenerator
from ..models.discriminator import CTGANPremiumDiscriminator
from ..samplers.sampler import CTGANPremiumSampler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CTGANPremiumTrainer:
    """Improved CTGAN trainer with better accuracy and stability"""

    def __init__(self, config: CTGANPremiumConfig):
        self.config = config
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Initialize components
        self.generator = CTGANPremiumGenerator(config).to(self.device)
        self.discriminator = CTGANPremiumDiscriminator(config).to(self.device)
        self.sampler = CTGANPremiumSampler(config)
        self.sampler.device = self.device # Ensure sampler uses correct device

        # Optimizers with better settings
        self.g_optimizer = torch.optim.Adam(
            self.generator.parameters(), lr=config.learning_rate, betas=(0.5, 0.999)
        )
        self.d_optimizer = torch.optim.Adam(
            self.discriminator.parameters(), lr=config.learning_rate, betas=(0.5, 0.999)
        )

        # Loss tracking
        self.losses = defaultdict(list)

    def compute_diversity_loss(self, generated_samples: torch.Tensor) -> torch.Tensor:
        """Compute diversity loss to prevent mode collapse"""
        # Compute pairwise distances
        distances = torch.cdist(generated_samples, generated_samples, p=2)

        # Encourage diversity by maximizing minimum distance
        min_distances = torch.min(
            distances + torch.eye(distances.size(0), device=self.device) * 1e6, dim=1
        )[0]
        diversity_loss = -torch.mean(min_distances)

        return diversity_loss

    def compute_correlation_loss(self, real_data: torch.Tensor, fake_data: torch.Tensor) -> torch.Tensor:
        """
        Compute correlation matching loss to force generator to capture column relationships.
        Using simple covariance matching.
        """
        # Center the data
        real_centered = real_data - torch.mean(real_data, dim=0)
        fake_centered = fake_data - torch.mean(fake_data, dim=0)
        
        # Compute Covariance Matrix (normalized by batch size)
        real_cov = torch.matmul(real_centered.t(), real_centered) / (real_data.size(0) - 1)
        fake_cov = torch.matmul(fake_centered.t(), fake_centered) / (fake_data.size(0) - 1)
        
        # Loss is L1 distance between covariance matrices
        loss = torch.nn.functional.l1_loss(fake_cov, real_cov)
        
        return loss

    def compute_conditional_loss(self, fake_data: torch.Tensor, cond_vec: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
        """
        Compute cross-entropy loss between generated data and conditional vector.
        Forces the generator to produce data matching the requested category.
        """
        if cond_vec is None or mask is None:
            return torch.tensor(0.0, device=self.device)

        loss = torch.tensor(0.0, device=self.device)
        batch_size = fake_data.size(0)
        
        # Iterate over output_info to find column indices
        # We only penalize the column that was indicated by 'mask'
        
        current_idx = self.config.n_continuous
        
        for i, info in enumerate(self.sampler.output_info):
            n_cats = info['num_categories']
            
            # Check which samples in batch conditioned on this column
            # mask[:, i] is 1 if column i was chosen
            col_mask = mask[:, i].bool()
            
            if col_mask.any():
                # Extract generated probabilities for this column
                # Shape: (batch_size, n_cats)
                gen_probs = fake_data[:, current_idx : current_idx + n_cats]
                
                # Extract target one-hot vector for this column
                # The cond_vec is a long global vector. We need the slice for this column.
                # Currently cond_vec is constructed as global one-hot.
                # We need to find the offset in cond_vec.
                # Sampler constructs cond_vec: [col1_cats, col2_cats, ...]
                
                # Calculate global offset for cond_vec
                # (Can pre-calc this but simple loop is fine for now)
                global_offset = 0
                for j in range(i):
                    global_offset += self.sampler.output_info[j]['num_categories']
                
                target_onehot = cond_vec[:, global_offset : global_offset + n_cats]
                
                # Filter rows relevant to this column
                selected_gen = gen_probs[col_mask]
                selected_target = target_onehot[col_mask]
                
                # Compute Cross Entropy
                # Since we have Softmax/Gumbel output (probs), and one-hot target:
                # Loss = -sum(target * log(predicted))
                # Add epsilon for numerical stability
                log_probs = torch.log(selected_gen + 1e-10)
                ce_loss = -torch.sum(selected_target * log_probs, dim=1).mean()
                
                loss += ce_loss
            
            current_idx += n_cats
            
        return loss

    def apply_packing(self, data: torch.Tensor, cond: torch.Tensor = None) -> torch.Tensor:
        """
        Pack samples for PacGAN.
        Reshapes (batch_size, features) -> (batch_size/pac, features*pac)
        """
        if not self.config.use_pacgan:
            if cond is not None:
                return torch.cat([data, cond], dim=1)
            return data

        pac = self.config.pac
        # Ensure batch size is divisible by pac
        batch_size = data.size(0)
        remainder = batch_size % pac
        if remainder != 0:
            # Drop last few samples to make it divisible
            new_batch_size = batch_size - remainder
            data = data[:new_batch_size]
            if cond is not None:
                 cond = cond[:new_batch_size]
        
        # Concatenate data and cond BEFORE packing if needed
        # Standard CTGAN: input to D is cat(data, cond)
        # PacGAN: cat(data_1, cond_1, data_2, cond_2, ...)
        
        if cond is not None:
            # Interleave data and cond? Or concate first then pack?
            # D expects: [data_1, cond_1, data_2, cond_2 ...] flattened
            combined = torch.cat([data, cond], dim=1) #(N, F+C)
            packed = combined.view(combined.size(0) // pac, -1) #(N/pac, (F+C)*pac)
            return packed
        else:
            packed = data.view(data.size(0) // pac, -1)
            return packed

    def train_step(self, real_data: torch.Tensor, cond: torch.Tensor, mask: torch.Tensor, epoch: int, batch_idx: int) -> Dict[str, float]:
        """Single training step with conditional sampling"""
        batch_size = real_data.size(0)
        losses = {}

        # Sample latent codes
        z = self.sampler.sample_z(batch_size, self.device)

        # Generate fake data
        # Pass condition to generator
        fake_data = self.generator(z, cond=cond)

        # Train Discriminator
        self.d_optimizer.zero_grad()

        # Real data discrimination
        # Pass condition to discriminator
        # Use packing if enabled
        d_real_input = self.apply_packing(real_data, cond)
        d_fake_input = self.apply_packing(fake_data.detach(), cond)
        
        # Note: Discriminator forward() handles concatenation if cond is passed separately,
        # but apply_packing handles it internally and returns a single tensor.
        # So we pass None for cond here.
        real_scores = self.discriminator(d_real_input, cond=None)
        fake_scores = self.discriminator(d_fake_input, cond=None)

        # Compute discriminator losses
        # WGAN-GP Loss: D(x) - D(z)
        # We want to MAXIMIZE D(real) - D(fake), so we MINIMIZE D(fake) - D(real)
        d_loss_real = -torch.mean(real_scores)
        d_loss_fake = torch.mean(fake_scores)

        d_loss = d_loss_real + d_loss_fake

        # Add gradient penalty if enabled
        if self.config.use_gradient_penalty:
            # We need to compute GP on packed inputs
            # Discriminator.compute_gradient_penalty typically takes real/fake and interpolates.
            # We must pass PACKED inputs to it.
            
            # Since our D takes packed inputs, we should interpolate BETWEEN packed_real and packed_fake.
            gradient_penalty = self.discriminator.compute_gradient_penalty(
                d_real_input, d_fake_input, cond=None
            )
            d_loss += self.config.gradient_penalty_weight * gradient_penalty
            losses["gradient_penalty"] = gradient_penalty.item()

        d_loss.backward()
        self.d_optimizer.step()

        # Train Generator (every n_critic steps)
        n_critic = 5
        if batch_idx % n_critic == 0:
            self.g_optimizer.zero_grad()

            # Generate new fake data
            z = self.sampler.sample_z(batch_size, self.device)
            fake_data = self.generator(z, cond=cond)

            # Get discriminator scores for fake data
            # Pack first
            d_fake_input_g = self.apply_packing(fake_data, cond)
            fake_scores = self.discriminator(d_fake_input_g, cond=None)

            # Compute generator loss (fool the discriminator)
            # WGAN Generator Loss: Maximize D(fake) => Minimize -D(fake)
            g_loss = -torch.mean(fake_scores)
            
            # Add Conditional Loss (Penalize missing the condition)
            cond_loss = self.compute_conditional_loss(fake_data, cond, mask)
            g_loss += self.config.conditional_loss_weight * cond_loss

            # Add diversity loss
            diversity_loss = self.compute_diversity_loss(fake_data)
            g_loss += self.config.diversity_loss_weight * diversity_loss

            # Add Correlation Loss (Feature Matching)
            corr_loss = torch.tensor(0.0, device=self.device)
            if hasattr(self.config, 'correlation_loss_weight') and self.config.correlation_loss_weight > 0:
                 corr_loss = self.compute_correlation_loss(real_data, fake_data)
                 g_loss += self.config.correlation_loss_weight * corr_loss

            g_loss.backward()
            self.g_optimizer.step()

            losses["generator_loss"] = g_loss.item()
            losses["diversity_loss"] = diversity_loss.item()
            losses["conditional_loss"] = cond_loss.item()
            losses["correlation_loss"] = corr_loss.item()
        
        # Store losses
        losses.update(
            {
                "discriminator_loss": d_loss.item(),
                "d_loss_real": d_loss_real.item(),
                "d_loss_fake": d_loss_fake.item(),
            }
        )

        return losses

    def fit(
        self, 
        real_data: np.ndarray, 
        epochs: int = 1000, 
        output_info: List[Dict] = None,
        verbose: bool = True
    ) -> Dict[str, List[float]]:
        """
        Train the model with Conditional Sampling.
        args:
            output_info: Metadata from Preprocessor.get_output_info()
        """
        real_data = np.array(real_data, dtype=np.float32)
        real_tensor = torch.tensor(real_data, dtype=torch.float32).to(self.device)
        
        # Initialize Conditional Sampler
        if output_info is None:
            output_info = []
        self.sampler.fit(real_data, output_info)
        
        # RE-INITIALIZE Models with correct output_info for Gumbel Softmax
        # This ensures the Generator knows about categorical groupings
        self.generator = CTGANPremiumGenerator(self.config, output_info).to(self.device)
        # Discriminator doesn't need output_info (just input dims), but good to reset
        self.discriminator = CTGANPremiumDiscriminator(self.config).to(self.device)
        
        # Re-init optimizers
        self.g_optimizer = torch.optim.Adam(
            self.generator.parameters(), lr=self.config.learning_rate, betas=(0.5, 0.999)
        )
        self.d_optimizer = torch.optim.Adam(
            self.discriminator.parameters(), lr=self.config.learning_rate, betas=(0.5, 0.999)
        )

        try:
            from tqdm.auto import tqdm
        except ImportError:
            def tqdm(iter_obj, **kwargs): return iter_obj

        # Training loop
        # Calculate steps per epoch
        batch_size = self.config.batch_size
        steps_per_epoch = max(1, len(real_data) // batch_size)
        
        with tqdm(range(epochs), desc="Training CTGAN", unit="epoch", disable=not verbose) as pbar:
            for epoch in pbar:
                epoch_losses = defaultdict(list)
                
                for step in range(steps_per_epoch):
                    # 1. Sample Condition and Matching Real Data
                    cond_vec, mask, real_idx = self.sampler.sample_cond(batch_size)
                    
                    if cond_vec is None:
                        # Fallback for datasets with no discrete columns
                        # Randomly sample real data
                        real_idx = np.random.randint(0, len(real_data), batch_size)
                        batch_data = real_tensor[real_idx]
                        cond = None
                        mask = None
                    else:
                        # Fetch the matching real rows
                        batch_data = real_tensor[real_idx]
                        cond = cond_vec.to(self.device)
                        mask = mask.to(self.device)

                    # Training step
                    step_losses = self.train_step(batch_data, cond, mask, epoch, step)

                    # Accumulate losses
                    for key, value in step_losses.items():
                        epoch_losses[key].append(value)

                # Average epoch losses
                avg_losses = {}
                for key, values in epoch_losses.items():
                    if values:
                        avg_loss = np.mean(values)
                        self.losses[key].append(avg_loss)
                        avg_losses[key] = avg_loss

                # Update progress bar
                if verbose and avg_losses:
                    display_metrics = {
                        "d_loss": f"{avg_losses.get('discriminator_loss', 0):.4f}",
                        "g_loss": f"{avg_losses.get('generator_loss', 0):.4f}",
                        "cond": f"{avg_losses.get('conditional_loss', 0):.4f}" # Show cond loss
                    }
                    if "diversity_loss" in avg_losses:
                        display_metrics["div"] = f"{avg_losses['diversity_loss']:.4f}"
                    if "correlation_loss" in avg_losses:
                        display_metrics["corr"] = f"{avg_losses['correlation_loss']:.4f}"
                    
                    pbar.set_postfix(display_metrics)

        return dict(self.losses)

    def generate(
        self, n_samples: int, return_numpy: bool = True
    ) -> Union[torch.Tensor, np.ndarray]:
        """Generate synthetic samples (conditioned for realism)"""
        self.generator.eval()

        with torch.no_grad():
            # 1. Sample Conditions to ensure output follows realistic marginals
            cond_vec, _, _ = self.sampler.sample_cond(n_samples)
            if cond_vec is not None:
                cond_vec = cond_vec.to(self.device)
            
            # 2. Sample latent codes
            z = self.sampler.sample_z(n_samples, self.device)

            # 3. Generate
            fake_data = self.generator(z, cond=cond_vec, hard_categorical=True)

        self.generator.train()

        if return_numpy:
            return fake_data.cpu().numpy()
        return fake_data

    def save_model(self, filepath: str):
        """Save the trained model"""
        torch.save(
            {
                "generator_state_dict": self.generator.state_dict(),
                "discriminator_state_dict": self.discriminator.state_dict(),
                "config": self.config,
                "losses": dict(self.losses),
                "sampler_output_info": self.sampler.output_info # Save sampler metadata
            },
            filepath,
        )

    def get_feature_importance(self) -> Dict[str, float]:
        """
        Get feature importance scores.
        Note: GANs do not provide intrinsic importance. This is a placeholder or 
        could be implemented via sensitivity analysis in the future.
        """
        importance = {}
        # Simple placeholder logic: Uniform importance
        total_feats = self.config.n_continuous + self.config.n_categorical
        score = 1.0 / max(1, total_feats)
        
        for i in range(self.config.n_continuous):
             importance[f"cont_{i}"] = score
        for i in range(self.config.n_categorical):
             importance[f"cat_{i}"] = score
             
        return importance

    def load_model(self, filepath: str):
        """Load a trained model"""
        checkpoint = torch.load(filepath, map_location=self.device)
        self.generator.load_state_dict(checkpoint["generator_state_dict"])
        self.discriminator.load_state_dict(checkpoint["discriminator_state_dict"])
        self.losses = defaultdict(list, checkpoint["losses"])
        
        # Restore sampler metadata if available (needed for inference if we want to condition)
        if "sampler_output_info" in checkpoint:
            self.sampler.output_info = checkpoint["sampler_output_info"]
            self.sampler.n_discrete_columns = len(self.sampler.output_info)
            # Rebuilding internal index (category_log_probs) requires real data, 
            # so strict Conditional Sampling for purely inference without original data 
            # might require saving log_probs too. 
            # But for now assuming re-fit or just simple usage.
