"""
Domain-Specific Fine-Tuning Example

This example shows how to fine-tune a small language model
for a specific domain (e.g., customer support, medical, legal).

Usage:
    python custom_domain.py --domain customer_support
"""

import argparse
from datasets import Dataset

# Sample domain-specific data
DOMAIN_DATA = {
    "customer_support": [
        {
            "instruction": "How do I reset my password?",
            "response": "To reset your password: 1) Go to the login page, 2) Click 'Forgot Password', 3) Enter your email, 4) Check your inbox for the reset link, 5) Create a new password.",
        },
        {
            "instruction": "What is your return policy?",
            "response": "We offer a 30-day return policy for all unused items in original packaging. To initiate a return, please contact our support team with your order number.",
        },
        {
            "instruction": "How do I track my order?",
            "response": "You can track your order by logging into your account and visiting the 'Orders' section. Alternatively, use the tracking number sent to your email.",
        },
    ],
    "coding_assistant": [
        {
            "instruction": "Write a Python function to reverse a string",
            "response": "def reverse_string(s):\n    return s[::-1]\n\n# Example usage:\nprint(reverse_string('hello'))  # Output: 'olleh'",
        },
        {
            "instruction": "Explain what a list comprehension is in Python",
            "response": "A list comprehension is a concise way to create lists in Python. Syntax: [expression for item in iterable if condition]. Example: [x**2 for x in range(5)] creates [0, 1, 4, 9, 16].",
        },
    ],
}


def format_for_training(examples: list[dict]) -> list[dict]:
    """Format examples for LMFast training."""
    formatted = []
    for ex in examples:
        text = f"""Below is an instruction. Write a response.

### Instruction:
{ex['instruction']}

### Response:
{ex['response']}"""
        formatted.append({"text": text})
    return formatted


def main():
    parser = argparse.ArgumentParser(description="Domain-specific fine-tuning")
    parser.add_argument(
        "--domain",
        type=str,
        default="customer_support",
        choices=list(DOMAIN_DATA.keys()),
        help="Domain to fine-tune for",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="HuggingFaceTB/SmolLM-135M",
        help="Base model",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=100,
        help="Training steps",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output directory",
    )
    args = parser.parse_args()
    
    from lmfast import SLMTrainer, SLMConfig, TrainingConfig
    
    print("=" * 60)
    print(f"Domain-Specific Fine-Tuning: {args.domain.upper()}")
    print("=" * 60)
    
    # Prepare data
    raw_data = DOMAIN_DATA[args.domain]
    formatted_data = format_for_training(raw_data)
    dataset = Dataset.from_list(formatted_data)
    
    print(f"\nDomain: {args.domain}")
    print(f"Training samples: {len(dataset)}")
    
    # Configure
    output_dir = args.output or f"./{args.domain}_model"
    
    model_config = SLMConfig(
        model_name=args.model,
        max_seq_length=1024,
    )
    
    training_config = TrainingConfig(
        output_dir=output_dir,
        max_steps=args.max_steps,
        batch_size=2,
        learning_rate=2e-4,
    )
    
    # Train
    trainer = SLMTrainer(model_config, training_config)
    
    print(f"\nTraining for {args.max_steps} steps...")
    metrics = trainer.train(dataset)
    
    print(f"\nTraining complete! Metrics: {metrics}")
    
    # Test with domain-specific prompt
    print("\n" + "=" * 60)
    print("Testing domain-specific response:")
    print("=" * 60)
    
    test_prompts = {
        "customer_support": "How can I contact customer support?",
        "coding_assistant": "How do I read a file in Python?",
    }
    
    prompt = test_prompts[args.domain]
    response = trainer.generate(
        f"Below is an instruction. Write a response.\n\n### Instruction:\n{prompt}\n\n### Response:\n",
        max_new_tokens=150,
    )
    
    print(f"\nPrompt: {prompt}")
    print(f"Response: {response}")
    
    # Save
    trainer.save(output_dir)
    print(f"\nModel saved to: {output_dir}")


if __name__ == "__main__":
    main()
