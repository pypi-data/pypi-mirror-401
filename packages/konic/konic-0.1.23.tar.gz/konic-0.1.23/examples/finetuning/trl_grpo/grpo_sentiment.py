"""TRL GRPO Finetuning Example - Sentiment-Guided Response Generation.

This example demonstrates how to use Konic's TRL backend with Group Relative
Policy Optimization (GRPO) for RLHF training.

Key concepts demonstrated:
- Using the TRL GRPO backend instead of native PPO
- Custom reward functions using the @llm_reward decorator
- Basic LoRA configuration for parameter-efficient finetuning
- Comparing GRPO vs native PPO approaches

GRPO Benefits:
- No value head required (simpler architecture)
- Group-based relative rewards (compares multiple generations)
- Often faster convergence for reward optimization tasks

Requirements:
    pip install konic[trl]

Model: GPT-2 (small and fast for demonstration)
Dataset: IMDB movie reviews
Goal: Train the model to generate positive, concise, and coherent responses
"""

import re

from konic.finetuning import (
    DatasetConfig,
    DatasetSource,
    GenerationConfig,
    KonicFinetuningEngine,
    KonicFinetuningMethodType,
    KonicLLMRewardComposer,
    LoraConfig,
    TrainingConfig,
    llm_reward,
)

# =============================================================================
# Custom Reward Composer
# =============================================================================


class SentimentRewardComposer(KonicLLMRewardComposer):
    """Custom reward composer that encourages positive, concise, and coherent text.

    This composer combines three reward signals:
    1. brevity_bonus: Rewards shorter responses (max 1.0 for very short)
    2. positivity_reward: Rewards positive sentiment words
    3. coherence_penalty: Penalizes repetitive text patterns
    """

    POSITIVE_WORDS = {
        "good",
        "great",
        "excellent",
        "amazing",
        "wonderful",
        "fantastic",
        "love",
        "enjoy",
        "happy",
        "best",
        "perfect",
        "beautiful",
        "brilliant",
        "outstanding",
        "superb",
        "delightful",
        "impressive",
        "positive",
    }

    @llm_reward
    def brevity_bonus(self, prompt: str, response: str) -> float:
        """Reward shorter, more concise responses."""
        max_length = 300
        response_length = len(response)
        if response_length >= max_length:
            return 0.0
        return max(0.0, 1.0 - (response_length / max_length))

    @llm_reward
    def positivity_reward(self, prompt: str, response: str) -> float:
        """Reward responses containing positive sentiment words."""
        words = response.lower().split()
        if not words:
            return 0.0
        positive_count = sum(1 for word in words if word in self.POSITIVE_WORDS)
        density = positive_count / len(words)
        return min(1.0, density / 0.3)

    @llm_reward
    def coherence_penalty(self, prompt: str, response: str) -> float:
        """Penalize repetitive patterns in the response."""
        if not response:
            return 1.0
        words = response.lower().split()
        if len(words) < 2:
            return 1.0

        # Check for consecutive repeated words
        repeated_words = sum(1 for i in range(1, len(words)) if words[i] == words[i - 1])
        word_repetition_ratio = repeated_words / len(words)

        # Check for repeated bigrams
        bigrams = [f"{words[i]} {words[i + 1]}" for i in range(len(words) - 1)]
        unique_bigrams = set(bigrams)
        bigram_repetition_ratio = 1.0 - (len(unique_bigrams) / len(bigrams)) if bigrams else 0.0

        # Check for repeated character patterns
        char_pattern_penalty = 0.3 if re.search(r"(.)\1{4,}", response) else 0.0

        total_penalty = (
            0.4 * word_repetition_ratio + 0.3 * bigram_repetition_ratio + char_pattern_penalty
        )
        return max(0.0, 1.0 - total_penalty)


# =============================================================================
# Main Training Script
# =============================================================================


def main():
    """Run the TRL GRPO finetuning example."""
    print("=" * 60)
    print("Konic TRL GRPO Finetuning Example")
    print("=" * 60)
    print()

    # LoRA configuration
    lora_config = LoraConfig(
        r=8,
        lora_alpha=16,
        lora_dropout=0.1,
        target_modules=["c_attn", "c_proj"],
        bias="none",
        fan_in_fan_out=True,
    )

    # Training hyperparameters
    training_config = TrainingConfig(
        learning_rate=5e-5,
        batch_size=4,
        gradient_accumulation_steps=2,
        kl_penalty_weight=0.05,  # Used as beta in GRPO
    )

    # Generation config for GRPO
    generation_config = GenerationConfig(
        max_new_tokens=64,
        temperature=0.8,
        top_p=0.9,
        do_sample=True,
    )

    # Dataset configuration
    dataset_config = DatasetConfig(
        source=DatasetSource.HUGGINGFACE,
        name="imdb",
        prompt_column="text",
        split="train",
        max_samples=200,  # Smaller for demo
        shuffle=True,
    )

    # Create engine with TRL GRPO backend
    print("Creating TRL GRPO finetuning engine...")
    engine = KonicFinetuningEngine(
        model_name="gpt2",
        reward_composer=SentimentRewardComposer(),
        dataset_config=dataset_config,
        lora_config=lora_config,
        training_config=training_config,
        generation_config=generation_config,
        method=KonicFinetuningMethodType.TRL_GRPO,  # Use TRL GRPO backend
    )

    print(f"Backend: {engine.backend_name}")
    print()

    # Run training
    print("Starting TRL GRPO training...")
    print("GRPO generates multiple responses per prompt and uses relative rewards.")
    print()

    result = engine.train(
        max_iterations=25,
        save_every=10,
    )

    # Print results
    print("\n" + "=" * 60)
    print("Training Complete!")
    print("=" * 60)
    print(result.summary())

    # Test the model
    print("\nTesting trained model with sample prompts...")
    print("-" * 60)

    test_prompts = [
        "The movie was",
        "I really think that this film",
        "Overall, my experience was",
    ]

    eval_results = engine.evaluate(test_prompts)

    for prompt, response, reward in zip(
        eval_results["prompts"], eval_results["responses"], eval_results["rewards"]
    ):
        print(f"\nPrompt: {prompt}")
        print(f"Response: {response[:200]}...")
        print(f"Reward: {reward:.3f}")

    print("\n" + "=" * 60)
    print("TRL GRPO Example complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
