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
from delta.types.types import TensorType, ConcreteDim
# Note: We import frontend AST types here for initializer evaluation.
# Ideally this metadata would be extracted during compilation, but
# for now we use the AST directly since CompileResult exposes it.
from delta.frontend.ast import ParamDecl, Call, Identifier, Literal


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
        """Initialize parameters from SIR param declarations, respecting user's initializers."""
        if not self._compile_result.sir:
            return
        
        # Extract initializers from CompileResult metadata if available,
        # otherwise fall back to extracting from AST directly
        if self._compile_result.param_initializers is not None:
            param_initializers = self._compile_result.param_initializers
        else:
            # Fallback: extract from AST if metadata not available
            param_initializers = {}
            if self._compile_result.ast:
                for item in self._compile_result.ast.items:
                    if isinstance(item, ParamDecl) and item.initializer:
                        param_initializers[item.name] = item.initializer
        
        sir = self._compile_result.sir
        for name, param_node in sir.params.items():
            if hasattr(self._module, 'params') and hasattr(self._module.params, name):
                # Parse shape from the param name or use defaults
                shape = self._parse_param_shape(name, param_node)
                if shape:
                    # Use the user's initializer if available
                    if name in param_initializers:
                        data = self._eval_initializer(param_initializers[name], shape)
                    else:
                        # Fallback: use name-based heuristics
                        data = self._init_from_name(name, shape)
                    setattr(self._module.params, name, nn.Parameter(data))
    
    def _eval_initializer(self, initializer_expr: Any, shape: tuple) -> torch.Tensor:
        """Evaluate an initializer expression (e.g., randn(10, 5) or zeros(5))."""
        # Handle Call expressions like randn(10, 5) or zeros(5)
        if isinstance(initializer_expr, Call) and isinstance(initializer_expr.func, Identifier):
            func_name = initializer_expr.func.name
            
            # Extract shape arguments from call args
            args = initializer_expr.args
            if func_name == "randn":
                # randn(10, 5) - use provided shape args, or fallback to shape
                if args and all(isinstance(a, Literal) and a.kind == 'int' for a in args):
                    init_shape = tuple(a.value for a in args)
                    return torch.randn(*init_shape)
                else:
                    return torch.randn(*shape)
            elif func_name == "zeros":
                # zeros(5) - use provided shape args, or fallback to shape
                if args and all(isinstance(a, Literal) and a.kind == 'int' for a in args):
                    init_shape = tuple(a.value for a in args)
                    return torch.zeros(*init_shape)
                else:
                    return torch.zeros(*shape)
            elif func_name == "ones":
                # ones(5) - use provided shape args, or fallback to shape
                if args and all(isinstance(a, Literal) and a.kind == 'int' for a in args):
                    init_shape = tuple(a.value for a in args)
                    return torch.ones(*init_shape)
                else:
                    return torch.ones(*shape)
            elif func_name == "rand":
                # rand(5) - use provided shape args, or fallback to shape
                if args and all(isinstance(a, Literal) and a.kind == 'int' for a in args):
                    init_shape = tuple(a.value for a in args)
                    return torch.rand(*init_shape)
                else:
                    return torch.rand(*shape)
        
        # Fallback: use shape with small random init
        return torch.randn(*shape) * 0.01
    
    def _init_from_name(self, name: str, shape: tuple) -> torch.Tensor:
        """Fallback initialization based on parameter name pattern."""
        name_lower = name.lower()
        # Weight matrices: use small random initialization
        if any(x in name_lower for x in ['w', 'weight', 'emb']) and not name_lower.startswith('b'):
            return torch.randn(*shape) * 0.02
        # Bias terms: use zeros
        elif name_lower.startswith('b') or 'bias' in name_lower:
            return torch.zeros(*shape)
        # Gamma/scale parameters: use ones
        elif any(x in name_lower for x in ['_g', 'gamma', 'ln', 'scale']):
            return torch.ones(*shape)
        # Default: use small random initialization (prevents dead neurons)
        else:
            return torch.randn(*shape) * 0.01
    
    def _extract_shape_from_initializer(self, initializer_expr: Any) -> Optional[tuple]:
        """Extract shape from an initializer expression like randn(3, 2)."""
        if isinstance(initializer_expr, Call) and isinstance(initializer_expr.func, Identifier):
            func_name = initializer_expr.func.name
            # Shape-defining initializers: randn, zeros, ones, rand, full
            if func_name in ('randn', 'zeros', 'ones', 'rand', 'full'):
                args = initializer_expr.args
                if args and all(isinstance(a, Literal) and a.kind == 'int' for a in args):
                    return tuple(a.value for a in args)
        return None
    
    def _parse_param_shape(self, name: str, node: Any) -> Optional[tuple]:
        """Parse parameter shape from SIR node's type or infer from name."""
        # First, try to extract shape from the parameter's type
        if hasattr(node, 'props') and hasattr(node.props, 'dtype'):
            dtype = node.props.dtype
            if isinstance(dtype, TensorType) and dtype.shape:
                # Extract concrete dimensions
                shape = tuple(
                    dim.value for dim in dtype.shape
                    if isinstance(dim, ConcreteDim)
                )
                if shape and all(isinstance(d, int) for d in shape):
                    return shape
        
        # Second, try to extract shape from initializer in param_initializers
        if self._compile_result.param_initializers:
            initializer = self._compile_result.param_initializers.get(name)
            if initializer:
                shape = self._extract_shape_from_initializer(initializer)
                if shape:
                    return shape
        
        # Third, check AST directly if param_initializers not available
        if self._compile_result.ast:
            for item in self._compile_result.ast.items:
                if isinstance(item, ParamDecl) and item.name == name and item.initializer:
                    shape = self._extract_shape_from_initializer(item.initializer)
                    if shape:
                        return shape
        
        # Fallback: use hardcoded shapes for common parameter names
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
            # Regression example (README quick start)
            "w": (10, 5), "b": (5,),
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
        # Custom loading for dictionary inputs (e.g. {"x": x, "y": y})
        if isinstance(data, dict):
            # Order by typical supervised keys if present, else values
            if "x" in data and "y" in data:
                data = torch.utils.data.TensorDataset(data["x"], data["y"])
            else:
                # Fallback: assume values are tensors in order
                data = torch.utils.data.TensorDataset(*data.values())

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
