#!/usr/bin/env python3
"""
Banking Data Generation - API Example

Simple example showing how to use the Synthetic Data Studio API
to generate banking data with custom prompts and examples.

Usage:
    python api_example.py
"""

import requests
import json
from pathlib import Path


def load_files():
    """Load prompt and examples from files"""
    script_dir = Path(__file__).parent

    with open(script_dir / "custom_prompt.txt", 'r') as f:
        custom_prompt = f.read()

    with open(script_dir / "examples.json", 'r') as f:
        examples = json.load(f)

    return custom_prompt, examples


def generate_banking_data():
    """Generate banking data using the API"""

    # Load prompt and examples
    print("📝 Loading prompt and examples...")
    custom_prompt, examples = load_files()

    # Configure the request
    request_data = {
        # Use CUSTOM use case to provide our own prompt and examples
        "use_case": "custom",

        # Model configuration (AWS Bedrock)
        "model_id": "us.anthropic.claude-3-5-haiku-20241022-v1:0",
        "inference_type": "aws_bedrock",

        # Generation configuration
        "num_questions": 5,  # Generate 5 customer records
        "technique": "freeform",
        "is_demo": True,

        # Custom prompt and examples
        "custom_prompt": custom_prompt,
        "example_custom": examples,

        # Topics for diverse generation
        "topics": [
            "Young Professional with multiple accounts",
            "Small Business owner",
            "Retiree with high net worth"
        ],

        # Concurrency settings
        "max_concurrent_topics": 3,

        # Model parameters
        "model_params": {
            "temperature": 0.7,
            "top_p": 1.0,
            "max_tokens": 8192
        }
    }

    print("🚀 Sending request to API...")
    print(f"   Model: Claude 3.5 Haiku")
    print(f"   Records: 5 customers")
    print(f"   Topics: {len(request_data['topics'])}")

    # Make API request
    response = requests.post(
        "http://localhost:8000/api/v1/synthesize",
        json=request_data,
        timeout=300
    )

    # Check response
    if response.status_code == 200:
        result = response.json()
        print("\n✅ Generation successful!")

        # Save results
        output_file = "banking_data_output.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)

        print(f"💾 Results saved to: {output_file}")

        # Print summary
        total_records = sum(len(v) for v in result.get("qa_pairs", {}).values())
        print(f"\n📊 Generated {total_records} customer records")

        return result
    else:
        print(f"\n❌ Request failed: {response.status_code}")
        print(response.text)
        return None


def generate_with_file_path():
    """Alternative: Use file path instead of inline examples"""

    custom_prompt, _ = load_files()

    request_data = {
        "use_case": "custom",
        "model_id": "us.anthropic.claude-3-5-haiku-20241022-v1:0",
        "inference_type": "aws_bedrock",
        "num_questions": 3,
        "technique": "freeform",
        "custom_prompt": custom_prompt,
        "example_path": "examples/banking_multi_dataset/examples.json",  # Use file path
        "topics": ["High Net Worth Individuals"],
        "is_demo": True
    }

    response = requests.post(
        "http://localhost:8000/api/v1/synthesize",
        json=request_data,
        timeout=300
    )

    return response.json() if response.status_code == 200 else None


def generate_with_different_models():
    """Examples with different model providers"""

    custom_prompt, examples = load_files()

    # Example 1: AWS Bedrock Claude Sonnet
    claude_sonnet_config = {
        "use_case": "custom",
        "model_id": "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
        "inference_type": "aws_bedrock",
        "num_questions": 5,
        "technique": "freeform",
        "custom_prompt": custom_prompt,
        "example_custom": examples,
        "topics": ["Small Business Banking"],
        "is_demo": True
    }

    # Example 2: AWS Bedrock Llama
    llama_config = {
        "use_case": "custom",
        "model_id": "us.meta.llama3-2-90b-instruct-v1:0",
        "inference_type": "aws_bedrock",
        "num_questions": 5,
        "technique": "freeform",
        "custom_prompt": custom_prompt,
        "example_custom": examples,
        "topics": ["Retail Banking"],
        "is_demo": True
    }

    # Example 3: Cloudera AI Inference (CAII)
    caii_config = {
        "use_case": "custom",
        "model_id": "your-model-id",
        "inference_type": "caii",
        "caii_endpoint": "https://your-caii-endpoint.cloudera.com",
        "num_questions": 5,
        "technique": "freeform",
        "custom_prompt": custom_prompt,
        "example_custom": examples,
        "topics": ["Business Banking"],
        "is_demo": True
    }

    # Choose which config to use
    print("Model options:")
    print("1. Claude Sonnet (high quality)")
    print("2. Llama 90B (fast)")
    print("3. CAII (custom endpoint)")

    return claude_sonnet_config  # Return example config


def evaluate_generated_data(data_file: str):
    """Evaluate generated banking data"""

    # Load evaluation prompt
    script_dir = Path(__file__).parent
    with open(script_dir / "evaluation_prompt.txt", 'r') as f:
        eval_prompt = f.read()

    request_data = {
        "use_case": "custom",
        "model_id": "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
        "inference_type": "aws_bedrock",
        "technique": "freeform",
        "import_path": data_file,
        "import_type": "local",
        "custom_prompt": eval_prompt,
        "is_demo": True,
        "max_workers": 4
    }

    print(f"\n🔍 Evaluating data from: {data_file}")

    response = requests.post(
        "http://localhost:8000/api/v1/evaluate",
        json=request_data,
        timeout=300
    )

    if response.status_code == 200:
        result = response.json()
        print("✅ Evaluation complete!")

        # Print scores
        if "evaluations" in result:
            scores = [e.get("score", 0) for e in result["evaluations"]]
            avg_score = sum(scores) / len(scores) if scores else 0
            print(f"📊 Average Score: {avg_score:.1f}/10")
            print(f"   Records evaluated: {len(scores)}")

        return result
    else:
        print(f"❌ Evaluation failed: {response.status_code}")
        return None


def main():
    """Main function"""
    print("=" * 60)
    print("🏦 Banking Multi-Dataset Generator - API Example")
    print("=" * 60)
    print()

    # Generate data
    result = generate_banking_data()

    if result:
        print("\n" + "=" * 60)
        print("✨ Next Steps:")
        print("=" * 60)
        print("\n1. Review the generated data:")
        print("   cat banking_data_output.json | jq .")
        print("\n2. Validate referential integrity:")
        print("   python validate_data.py --input banking_data_output.json")
        print("\n3. Flatten to CSV files:")
        print("   python flatten_to_csv.py --input banking_data_output.json")
        print("\n4. Evaluate data quality:")
        print("   python api_example.py --evaluate banking_data_output.json")
        print()


if __name__ == "__main__":
    main()
