"""
High-level Delta execution API.

Usage:
    import delta
    
    # One-liner training
    model = delta.run("model.delta", train_loader, epochs=100)
    
    # Or step by step
    model = delta.compile("model.delta")
    model.fit(train_loader, epochs=100)
    output = model.generate("First Citizen:", max_tokens=100)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, Union, Callable, List
from pathlib import Path
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset

from delta.compiler import Compiler, CompileOptions, CompileResult
from delta.source import SourceFile


@dataclass 
class DeltaModel:
    """
    A compiled Delta model ready for training/inference.
    
    Provides a simple interface:
        model = delta.compile("model.delta")
        model.fit(train_data, epochs=10, lr=3e-3)
        text = model.generate("Hello", max_tokens=100)
    """
    _module: nn.Module
    _compile_result: CompileResult
    _device: torch.device = field(default_factory=lambda: torch.device("cpu"))
    _vocab: Optional[Dict[str, int]] = None
    _vocab_inv: Optional[Dict[int, str]] = None
    
    def __init__(self, compile_result: CompileResult):
        self._compile_result = compile_result
        self._module = list(compile_result.graph_modules.values())[0]
        self._device = torch.device("cpu")
        self._init_params_from_sir()
    
    def _init_params_from_sir(self):
        """Initialize parameters from SIR param declarations."""
        if not self._compile_result.sir:
            return
        
        sir = self._compile_result.sir
        for name, param_node in sir.params.items():
            if hasattr(self._module, 'params') and hasattr(self._module.params, name):
                # Parse shape from the param name or use defaults
                shape = self._parse_param_shape(name, param_node)
                if shape:
                    # Initialize based on name pattern
                    if any(x in name.lower() for x in ['w_', 'w1', 'w2', 'emb', 'weight']):
                        data = torch.randn(*shape) * 0.02
                    elif any(x in name.lower() for x in ['_g', 'gamma', 'ln']):
                        data = torch.ones(*shape)
                    else:
                        data = torch.zeros(*shape)
                    setattr(self._module.params, name, nn.Parameter(data))
    
    def _parse_param_shape(self, name: str, node: Any) -> Optional[tuple]:
        """Parse parameter shape from SIR node or infer from name."""
        # Common transformer shapes
        shapes = {
            # Embeddings
            "tok_emb": (46, 64), "pos_emb": (32, 64),
            # Attention
            "W_q": (64, 64), "W_k": (64, 64), "W_v": (64, 64), "W_o": (64, 64),
            # Layer norm
            "ln1_g": (64,), "ln1_b": (64,), "ln2_g": (64,), "ln2_b": (64,),
            # FFN
            "ff_w1": (64, 256), "ff_b1": (256,),
            "ff_w2": (256, 64), "ff_b2": (64,),
            # MNIST
            "W1": (784, 256), "b1": (256,),
            "W2": (256, 128), "b2": (128,),
            "W3": (128, 10), "b3": (10,),
        }
        return shapes.get(name)
    
    def to(self, device: Union[str, torch.device]) -> "DeltaModel":
        """Move model to device. Use 'auto' for automatic GPU detection."""
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self._device = torch.device(device) if isinstance(device, str) else device
        self._module = self._module.to(self._device)
        return self
    
    def __call__(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass."""
        return self._module(x.to(self._device))
    
    def parameters(self):
        """Get model parameters."""
        return self._module.parameters()
    
    def train(self):
        """Set to training mode."""
        self._module.train()
        return self
    
    def eval(self):
        """Set to evaluation mode."""
        self._module.eval()
        return self
    
    def fit(
        self,
        data: Union[DataLoader, Any],
        epochs: int = 100,
        lr: float = 3e-3,
        log_every: int = 10,
        batch_size: int = 64
    ) -> List[float]:
        """
        Train the model.
        
        Args:
            data: DataLoader or Dataset yielding (x, y) tuples
            epochs: Number of epochs
            lr: Learning rate
            log_every: Print loss every N epochs
            batch_size: Batch size (if data is a Dataset)
        
        Returns:
            List of epoch losses
        """
        # Wrap Dataset in DataLoader if needed
        if not isinstance(data, DataLoader):
            data = DataLoader(data, batch_size=batch_size, shuffle=True)
        
        optimizer = torch.optim.AdamW(self._module.parameters(), lr=lr)
        losses = []
        
        print(f"Training on {self._device}...")
        print("─" * 50)
        
        for epoch in range(1, epochs + 1):
            self._module.train()
            epoch_loss = 0.0
            
            for x, y in data:
                # Handle non-tensor labels (e.g., int from MNIST)
                if not isinstance(x, torch.Tensor):
                    x = torch.tensor(x)
                if not isinstance(y, torch.Tensor):
                    y = torch.tensor(y)
                x, y = x.to(self._device), y.to(self._device)
                
                optimizer.zero_grad()
                logits = self._module(x)
                
                # Handle different output shapes
                if logits.dim() == 3:  # Sequence model [B, T, V]
                    loss = torch.nn.functional.cross_entropy(
                        logits.view(-1, logits.size(-1)), 
                        y.view(-1)
                    )
                else:  # Classification [B, C]
                    loss = torch.nn.functional.cross_entropy(logits, y)
                
                loss.backward()
                optimizer.step()
                epoch_loss += loss.item()
            
            avg_loss = epoch_loss / len(data)
            losses.append(avg_loss)
            
            if epoch % log_every == 0:
                print(f"Epoch {epoch:3d}  │  Loss: {avg_loss:.4f}")
        
        print("─" * 50)
        return losses
    
    def set_vocab(self, chars: str):
        """Set vocabulary for text generation."""
        self._vocab = {c: i for i, c in enumerate(sorted(set(chars)))}
        self._vocab_inv = {i: c for c, i in self._vocab.items()}
        return self
    
    def generate(
        self,
        prompt: str,
        max_tokens: int = 100,
        temperature: float = 1.0,
        ctx_len: int = 32
    ) -> str:
        """
        Generate text from a prompt.
        
        Args:
            prompt: Starting text
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (higher = more random)
            ctx_len: Context length for the model
        
        Returns:
            Generated text (excluding prompt)
        """
        if not self._vocab:
            raise ValueError("Call set_vocab(chars) first to set vocabulary")
        
        self._module.eval()
        
        # Encode and pad prompt
        tokens = [self._vocab.get(c, 0) for c in prompt]
        if len(tokens) < ctx_len:
            tokens = [0] * (ctx_len - len(tokens)) + tokens
        
        tokens = torch.tensor([tokens], dtype=torch.long, device=self._device)
        generated = []
        
        for _ in range(max_tokens):
            with torch.no_grad():
                ctx = tokens[:, -ctx_len:]
                logits = self._module(ctx)
                logits = logits[0, -1] / temperature
                probs = torch.softmax(logits, dim=-1)
                next_tok = torch.multinomial(probs, 1)
                tokens = torch.cat([tokens, next_tok.unsqueeze(0)], dim=1)
                generated.append(next_tok.item())
        
        return ''.join(self._vocab_inv.get(t, '?') for t in generated)
    
    def save(self, path: str):
        """Save model weights."""
        torch.save(self._module.state_dict(), path)
    
    def load(self, path: str):
        """Load model weights."""
        self._module.load_state_dict(torch.load(path, map_location=self._device))


def compile(source: Union[str, Path], mode: str = "train") -> DeltaModel:
    """
    Compile a Delta program.
    
    Args:
        source: Path to .delta file or inline Delta code
        mode: Execution mode (train, infer, analyze)
    
    Returns:
        Compiled DeltaModel
    
    Example:
        model = delta.compile("model.delta")
        model.fit(train_loader, epochs=100)
    """
    if isinstance(source, Path) or (isinstance(source, str) and Path(source).exists()):
        source_file = SourceFile.from_path(Path(source))
    else:
        source_file = SourceFile.from_string(source, "<inline>")
    
    result = Compiler(CompileOptions(mode=mode, optimize=False)).compile(source_file)
    
    if not result.success:
        raise RuntimeError(f"Compilation failed:\n" + "\n".join(str(e) for e in result.errors))
    
    return DeltaModel(result)


def run(
    source: Union[str, Path],
    data: DataLoader,
    epochs: int = 100,
    lr: float = 3e-3,
    device: str = "auto"
) -> DeltaModel:
    """
    Compile and train in one call.
    
    Args:
        source: Path to .delta file
        data: Training DataLoader
        epochs: Number of epochs
        lr: Learning rate
        device: Device ("auto", "cpu", "cuda")
    
    Returns:
        Trained model
    
    Example:
        model = delta.run("model.delta", train_loader, epochs=100)
    """
    model = compile(source)
    
    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    
    model.fit(data, epochs=epochs, lr=lr)
    return model
