"""
Speculative Decoding for accelerated inference.

Uses a small draft model to propose tokens, which are then verified
by the main model in parallel. Can provide 2-3x speedup.

References:
- Leviathan et al. "Fast Inference from Transformers via Speculative Decoding"
- Chen et al. "Accelerating Large Language Model Decoding with Speculative Sampling"
"""

import torch
import torch.nn as nn
from typing import Optional, Tuple, List, Any
from dataclasses import dataclass
import time


@dataclass
class SpeculativeConfig:
    """Configuration for speculative decoding."""
    # Draft model settings
    num_speculative_tokens: int = 4  # Tokens to speculate ahead

    # Acceptance threshold
    acceptance_threshold: float = 0.0  # 0 = always accept if valid

    # Sampling
    temperature: float = 0.7
    top_p: float = 0.9

    # Performance
    max_verify_batch: int = 8  # Max parallel verifications


class SpeculativeDecoder:
    """
    Speculative decoding with draft model verification.

    The draft model quickly generates candidate tokens, then the
    main model verifies them in a single forward pass.

    This works because:
    1. Draft model is much smaller/faster (e.g., 350M vs 7B)
    2. Main model verification is parallelizable
    3. Most speculated tokens are accepted
    """

    def __init__(
        self,
        main_model: nn.Module,
        draft_model: nn.Module,
        tokenizer: Any,
        config: Optional[SpeculativeConfig] = None,
        device: torch.device = None
    ):
        self.main_model = main_model
        self.draft_model = draft_model
        self.tokenizer = tokenizer
        self.config = config or SpeculativeConfig()
        self.device = device or next(main_model.parameters()).device

        # Move models to device
        self.main_model.to(self.device).eval()
        self.draft_model.to(self.device).eval()

        # Stats
        self.stats = {
            "tokens_generated": 0,
            "tokens_accepted": 0,
            "speculation_rounds": 0,
            "total_time": 0.0,
        }

    @torch.inference_mode()
    def generate(
        self,
        prompt: str,
        max_tokens: int = 256,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
    ) -> str:
        """
        Generate text using speculative decoding.

        Args:
            prompt: Input text
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (default from config)
            top_p: Nucleus sampling threshold (default from config)

        Returns:
            Generated text
        """
        temperature = temperature or self.config.temperature
        top_p = top_p or self.config.top_p

        # Tokenize
        input_ids = self.tokenizer.encode(prompt)
        input_ids = torch.tensor([input_ids], device=self.device)

        start_time = time.perf_counter()
        generated = input_ids

        tokens_generated = 0
        while tokens_generated < max_tokens:
            # Speculative decoding step
            generated, n_accepted = self._speculative_step(
                generated, temperature, top_p
            )

            tokens_generated += n_accepted
            self.stats["tokens_accepted"] += n_accepted
            self.stats["speculation_rounds"] += 1

            # Check for EOS
            if generated[0, -1].item() == getattr(self.tokenizer, 'eos_token_id', 2):
                break

        self.stats["tokens_generated"] = tokens_generated
        self.stats["total_time"] = time.perf_counter() - start_time

        return self.tokenizer.decode(generated[0].tolist())

    def _speculative_step(
        self,
        input_ids: torch.Tensor,
        temperature: float,
        top_p: float
    ) -> Tuple[torch.Tensor, int]:
        """
        Perform one speculative decoding step.

        1. Generate K draft tokens with draft model
        2. Verify all K tokens with main model in one pass
        3. Accept verified tokens, resample rejected one

        Returns:
            Updated input_ids and number of accepted tokens
        """
        k = self.config.num_speculative_tokens

        # Step 1: Generate draft tokens
        draft_tokens, draft_probs = self._draft_generate(input_ids, k, temperature)

        # Step 2: Verify with main model
        # Create input with all draft tokens appended
        extended_input = torch.cat([input_ids, draft_tokens], dim=1)

        # Get main model logits for all positions
        main_logits = self.main_model(extended_input)

        # Get probabilities for verification positions
        verify_start = input_ids.shape[1] - 1  # Start from last input token
        main_probs = []
        for i in range(k + 1):  # +1 for the last position
            pos = verify_start + i
            if pos < main_logits.shape[1]:
                logits = main_logits[:, pos, :] / max(temperature, 0.01)
                probs = torch.softmax(logits, dim=-1)
                main_probs.append(probs)

        # Step 3: Acceptance/rejection
        accepted_tokens = []

        for i in range(k):
            if i >= len(main_probs) - 1:
                break

            draft_token = draft_tokens[0, i].item()
            draft_prob = draft_probs[i][0, draft_token].item()
            main_prob = main_probs[i][0, draft_token].item()

            # Acceptance probability: min(1, main_prob / draft_prob)
            acceptance_prob = min(1.0, main_prob / max(draft_prob, 1e-10))

            if torch.rand(1).item() < acceptance_prob:
                accepted_tokens.append(draft_token)
            else:
                # Reject: resample from adjusted distribution
                # p'(x) = normalize(max(0, main(x) - draft(x)))
                adjusted = torch.clamp(main_probs[i] - draft_probs[i], min=0)
                if adjusted.sum() > 0:
                    adjusted = adjusted / adjusted.sum()
                    new_token = torch.multinomial(adjusted, num_samples=1).item()
                else:
                    new_token = torch.multinomial(main_probs[i], num_samples=1).item()
                accepted_tokens.append(new_token)
                break  # Stop after first rejection

        # If all accepted, sample one more from main model
        if len(accepted_tokens) == k and len(main_probs) > k:
            next_token = torch.multinomial(main_probs[k], num_samples=1).item()
            accepted_tokens.append(next_token)

        # Build result
        if accepted_tokens:
            new_tokens = torch.tensor([accepted_tokens], device=self.device)
            result = torch.cat([input_ids, new_tokens], dim=1)
        else:
            result = input_ids

        return result, len(accepted_tokens)

    def _draft_generate(
        self,
        input_ids: torch.Tensor,
        num_tokens: int,
        temperature: float
    ) -> Tuple[torch.Tensor, List[torch.Tensor]]:
        """
        Generate draft tokens with the draft model.

        Returns:
            Generated tokens and their probabilities
        """
        generated = input_ids
        tokens = []
        probs = []

        for _ in range(num_tokens):
            logits = self.draft_model(generated)
            next_logits = logits[:, -1, :] / max(temperature, 0.01)
            next_probs = torch.softmax(next_logits, dim=-1)

            next_token = torch.multinomial(next_probs, num_samples=1)
            tokens.append(next_token)
            probs.append(next_probs)

            generated = torch.cat([generated, next_token], dim=1)

        return torch.cat(tokens, dim=1), probs

    def get_stats(self) -> dict:
        """Get decoding statistics."""
        stats = self.stats.copy()
        if stats["speculation_rounds"] > 0:
            stats["acceptance_rate"] = (
                stats["tokens_accepted"] /
                (stats["speculation_rounds"] * self.config.num_speculative_tokens)
            )
        else:
            stats["acceptance_rate"] = 0.0

        if stats["total_time"] > 0:
            stats["tokens_per_second"] = stats["tokens_generated"] / stats["total_time"]
        else:
            stats["tokens_per_second"] = 0.0

        return stats

    def reset_stats(self):
        """Reset statistics."""
        self.stats = {
            "tokens_generated": 0,
            "tokens_accepted": 0,
            "speculation_rounds": 0,
            "total_time": 0.0,
        }


class SelfSpeculativeDecoder:
    """
    Self-speculative decoding using early exit from the same model.

    Uses early layers of the model as the draft model, avoiding
    the need for a separate draft model.
    """

    def __init__(
        self,
        model: nn.Module,
        tokenizer: Any,
        draft_exit_layer: int = 4,  # Exit after this layer for draft
        config: Optional[SpeculativeConfig] = None,
        device: torch.device = None
    ):
        self.model = model
        self.tokenizer = tokenizer
        self.draft_exit_layer = draft_exit_layer
        self.config = config or SpeculativeConfig()
        self.device = device or next(model.parameters()).device

        self.model.to(self.device).eval()

        # This requires model to support early exit
        # Implementation depends on model architecture

    @torch.inference_mode()
    def generate(
        self,
        prompt: str,
        max_tokens: int = 256,
        temperature: Optional[float] = None
    ) -> str:
        """Generate with self-speculative decoding."""
        temperature = temperature or self.config.temperature

        input_ids = self.tokenizer.encode(prompt)
        input_ids = torch.tensor([input_ids], device=self.device)

        generated = input_ids

        for _ in range(max_tokens):
            # This is a simplified version
            # Full implementation requires model with early exit support

            logits = self.model(generated)
            next_logits = logits[:, -1, :] / max(temperature, 0.01)
            probs = torch.softmax(next_logits, dim=-1)
            next_token = torch.multinomial(probs, num_samples=1)

            generated = torch.cat([generated, next_token], dim=1)

            if next_token.item() == getattr(self.tokenizer, 'eos_token_id', 2):
                break

        return self.tokenizer.decode(generated[0].tolist())


class MedusaDecoder:
    """
    Medusa-style parallel decoding with multiple prediction heads.

    Uses additional heads to predict multiple future tokens in parallel,
    then verifies with tree attention.

    Reference: Cai et al. "Medusa: Simple Framework for Accelerating LLM Generation"
    """

    def __init__(
        self,
        model: nn.Module,
        medusa_heads: nn.ModuleList,  # Additional prediction heads
        tokenizer: Any,
        num_heads: int = 4,  # Number of Medusa heads
        config: Optional[SpeculativeConfig] = None,
        device: torch.device = None
    ):
        self.model = model
        self.medusa_heads = medusa_heads
        self.tokenizer = tokenizer
        self.num_heads = num_heads
        self.config = config or SpeculativeConfig()
        self.device = device or next(model.parameters()).device

        self.model.to(self.device).eval()
        self.medusa_heads.to(self.device).eval()

    @torch.inference_mode()
    def generate(
        self,
        prompt: str,
        max_tokens: int = 256,
        temperature: Optional[float] = None
    ) -> str:
        """
        Generate with Medusa parallel decoding.

        Note: This is a simplified implementation. Full Medusa uses
        tree attention for efficient verification.
        """
        temperature = temperature or self.config.temperature

        input_ids = self.tokenizer.encode(prompt)
        input_ids = torch.tensor([input_ids], device=self.device)

        generated = input_ids

        for _ in range(max_tokens):
            # Get main model hidden states
            # This requires model to return hidden states
            outputs = self.model(generated, output_hidden_states=True)

            if hasattr(outputs, 'hidden_states'):
                hidden = outputs.hidden_states[-1]
            else:
                # Fallback to logits-only
                logits = outputs if isinstance(outputs, torch.Tensor) else outputs.logits
                next_logits = logits[:, -1, :] / max(temperature, 0.01)
                probs = torch.softmax(next_logits, dim=-1)
                next_token = torch.multinomial(probs, num_samples=1)
                generated = torch.cat([generated, next_token], dim=1)

                if next_token.item() == getattr(self.tokenizer, 'eos_token_id', 2):
                    break
                continue

            # Get predictions from each Medusa head
            # Each head predicts token at different future position
            candidate_tokens = []
            for head in self.medusa_heads:
                head_logits = head(hidden[:, -1:, :])
                head_probs = torch.softmax(head_logits / max(temperature, 0.01), dim=-1)
                token = torch.multinomial(head_probs.squeeze(1), num_samples=1)
                candidate_tokens.append(token)

            # Simplified: just take first head prediction
            # Full Medusa would build a tree and verify
            next_token = candidate_tokens[0]
            generated = torch.cat([generated, next_token], dim=1)

            if next_token.item() == getattr(self.tokenizer, 'eos_token_id', 2):
                break

        return self.tokenizer.decode(generated[0].tolist())
