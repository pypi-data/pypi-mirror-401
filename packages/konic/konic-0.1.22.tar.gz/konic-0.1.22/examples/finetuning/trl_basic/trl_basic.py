"""Minimal TRL GRPO Example - The simplest way to use TRL backend.

This is the most basic example of using Konic's TRL GRPO backend.
Just 50 lines of code to get started with RLHF using TRL.

Requirements:
    pip install konic

Usage:
    python examples/finetuning/trl_basic.py
"""

from konic.finetuning import (
    DatasetConfig,
    DatasetSource,
    KonicFinetuningEngine,
    KonicFinetuningMethodType,
    KonicLLMRewardComposer,
    llm_reward,
)


class SimpleReward(KonicLLMRewardComposer):
    """Minimal reward: prefer longer, non-repetitive responses."""

    @llm_reward
    def quality(self, prompt: str, response: str) -> float:
        if len(response) < 10:
            return 0.0
        words = response.split()
        unique_ratio = len(set(words)) / len(words) if words else 0
        length_score = min(len(response) / 100, 1.0)
        return (unique_ratio + length_score) / 2


def main():
    print("Minimal TRL GRPO Example\n")

    engine = KonicFinetuningEngine(
        model_name="gpt2",
        reward_composer=SimpleReward(),
        dataset_config=DatasetConfig(
            source=DatasetSource.HUGGINGFACE,
            name="imdb",
            prompt_column="text",
            split="train",
            max_samples=20,
        ),
        method=KonicFinetuningMethodType.TRL_GRPO,
    )

    print(f"Backend: {engine.backend_name}\n")

    result = engine.train(max_iterations=5)
    print(result.summary())

    # Quick test
    output = engine.evaluate(["The movie was"])
    print(f"\nTest: '{output['prompts'][0]}' -> '{output['responses'][0][:80]}...'")


if __name__ == "__main__":
    main()
