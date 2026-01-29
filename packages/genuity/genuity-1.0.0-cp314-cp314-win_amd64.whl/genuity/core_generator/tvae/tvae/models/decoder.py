import torch
import torch.nn as nn
import torch.nn.functional as F


class TVAEDecoder(nn.Module):
    def __init__(self, latent_dim, output_dim, config, n_cont, n_cat):
        super().__init__()
        self.config = config
        self.latent_dim = latent_dim
        self.output_dim = output_dim
        self.n_cont = n_cont
        self.n_cat = n_cat
        self.fc1 = nn.Linear(latent_dim, config.hidden_dim)
        self.fc2 = nn.Linear(config.hidden_dim, config.hidden_dim)
        # Multi-head: separate heads for continuous and categorical
        if config.use_multi_head_decoder:
            self.cont_head = nn.Linear(config.hidden_dim, n_cont)
            self.cat_head = nn.Linear(config.hidden_dim, n_cat)
        else:
            self.out = nn.Linear(config.hidden_dim, output_dim)
        # Transformer attention (optional)
        if config.use_transformer_attention:
            encoder_layer = nn.TransformerEncoderLayer(
                d_model=config.hidden_dim, nhead=4
            )
            self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=1)
        else:
            self.transformer = None

    def forward(self, z):
        h = F.relu(self.fc1(z))
        h = F.relu(self.fc2(h))
        if self.transformer is not None:
            h = self.transformer(h.unsqueeze(1)).squeeze(1)
        if self.config.use_multi_head_decoder:
            cont_out = self.cont_head(h)
            # Apply sigmoid to continuous output to ensure [0, 1] range (matching MinMaxScaler)
            if self.n_cont > 0:
                cont_out = torch.sigmoid(cont_out)
            cat_out = self.cat_head(h)  # Logits for categorical (no activation, CrossEntropyLoss handles it)
            return cont_out, cat_out
        else:
            out = self.out(h)
            # For single-head, apply sigmoid to continuous part if present
            if self.n_cont > 0 and self.n_cat > 0:
                cont_part = torch.sigmoid(out[:, :self.n_cont])
                cat_part = out[:, self.n_cont:]  # Logits
                return torch.cat([cont_part, cat_part], dim=1)
            elif self.n_cont > 0:
                return torch.sigmoid(out)
            else:
                return out  # Categorical only, return logits
