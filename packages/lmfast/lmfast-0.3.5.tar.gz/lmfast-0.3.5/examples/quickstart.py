"""
LMFast Quickstart Example

This script demonstrates the basic usage of LMFast for training
a small language model on custom data.

Usage:
    python quickstart.py
"""

from datasets import Dataset

# Create sample data
sample_data = [
    {"text": "Below is an instruction. Write a response.\n\n### Instruction:\nWhat is machine learning?\n\n### Response:\nMachine learning is a subset of artificial intelligence that enables computers to learn from data without being explicitly programmed."},
    {"text": "Below is an instruction. Write a response.\n\n### Instruction:\nExplain Python in one sentence.\n\n### Response:\nPython is a versatile, high-level programming language known for its readability and extensive libraries."},
    {"text": "Below is an instruction. Write a response.\n\n### Instruction:\nWhat is deep learning?\n\n### Response:\nDeep learning is a type of machine learning that uses neural networks with many layers to learn complex patterns from data."},
]

def main():
    """Main training example."""
    from lmfast import SLMTrainer, SLMConfig, TrainingConfig
    
    print("=" * 60)
    print("LMFast Quickstart")
    print("=" * 60)
    
    # Create dataset
    dataset = Dataset.from_list(sample_data)
    print(f"\nDataset: {len(dataset)} samples")
    
    # Configure model
    model_config = SLMConfig(
        model_name="HuggingFaceTB/SmolLM-135M",
        max_seq_length=512,
        load_in_4bit=True,
    )
    
    # Configure training
    training_config = TrainingConfig(
        output_dir="./quickstart_output",
        max_steps=50,  # Quick demo
        batch_size=1,
        learning_rate=2e-4,
        logging_steps=10,
    )
    
    print(f"\nModel: {model_config.model_name}")
    print(f"Max steps: {training_config.max_steps}")
    print(f"Output: {training_config.output_dir}")
    
    # Create trainer
    trainer = SLMTrainer(model_config, training_config)
    
    # Train
    print("\nStarting training...")
    metrics = trainer.train(dataset)
    
    print(f"\nTraining complete!")
    print(f"Final metrics: {metrics}")
    
    # Test generation
    print("\n" + "=" * 60)
    print("Testing generation:")
    print("=" * 60)
    
    prompt = "What is artificial intelligence?"
    response = trainer.generate(
        f"Below is an instruction. Write a response.\n\n### Instruction:\n{prompt}\n\n### Response:\n",
        max_new_tokens=100,
    )
    print(f"\nPrompt: {prompt}")
    print(f"Response: {response}")
    
    # Save model
    trainer.save("./quickstart_output/final")
    print(f"\nModel saved to ./quickstart_output/final")


if __name__ == "__main__":
    main()
