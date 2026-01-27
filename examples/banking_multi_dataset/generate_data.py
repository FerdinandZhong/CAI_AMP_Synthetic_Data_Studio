#!/usr/bin/env python3
"""
Banking Multi-Dataset Generator

This script generates synthetic banking data with three interconnected datasets:
Customers, Accounts, and Transactions.

Usage:
    python generate_data.py --num-customers 10 --output output.json
    python generate_data.py --num-customers 50 --topics "High Net Worth,Small Business" --model claude-3-5-sonnet
"""

import argparse
import json
import requests
import sys
from pathlib import Path
from datetime import datetime


class BankingDataGenerator:
    def __init__(self, api_url="http://localhost:8000"):
        self.api_url = api_url
        self.script_dir = Path(__file__).parent

    def load_prompt(self):
        """Load the custom prompt from file"""
        prompt_path = self.script_dir / "custom_prompt.txt"
        with open(prompt_path, 'r') as f:
            return f.read()

    def load_examples(self):
        """Load example data from file"""
        examples_path = self.script_dir / "examples.json"
        with open(examples_path, 'r') as f:
            return json.load(f)

    def get_model_config(self, model_name):
        """Get model configuration based on model name"""
        models = {
            "claude-3-5-sonnet": {
                "model_id": "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
                "inference_type": "aws_bedrock"
            },
            "claude-3-5-haiku": {
                "model_id": "us.anthropic.claude-3-5-haiku-20241022-v1:0",
                "inference_type": "aws_bedrock"
            },
            "llama-3-70b": {
                "model_id": "us.meta.llama3-2-70b-instruct-v1:0",
                "inference_type": "aws_bedrock"
            },
            "llama-3-90b": {
                "model_id": "us.meta.llama3-2-90b-instruct-v1:0",
                "inference_type": "aws_bedrock"
            }
        }
        return models.get(model_name, models["claude-3-5-haiku"])

    def generate(self, num_customers=10, topics=None, model_name="claude-3-5-haiku",
                 temperature=0.7, output_file=None):
        """
        Generate synthetic banking data

        Args:
            num_customers: Number of customer records to generate
            topics: List of topics/customer segments to generate
            model_name: Model to use for generation
            temperature: Sampling temperature (0.0-1.0)
            output_file: Path to save output (default: auto-generated)
        """
        print(f"🏦 Banking Data Generator")
        print(f"=" * 60)

        # Load prompt and examples
        print("📝 Loading prompt and examples...")
        custom_prompt = self.load_prompt()
        examples = self.load_examples()

        # Default topics if none provided
        if topics is None:
            topics = [
                "Young Professional with multiple accounts",
                "Small Business owner",
                "Retiree with high net worth",
                "New customer with minimal history",
                "Family with joint accounts"
            ]

        # Get model configuration
        model_config = self.get_model_config(model_name)

        print(f"🤖 Model: {model_name}")
        print(f"📊 Customers to generate: {num_customers}")
        print(f"🎯 Topics: {', '.join(topics)}")
        print(f"🌡️  Temperature: {temperature}")
        print(f"\n⏳ Generating data...\n")

        # Prepare API request
        request_data = {
            "use_case": "custom",
            "model_id": model_config["model_id"],
            "inference_type": model_config["inference_type"],
            "num_questions": num_customers,
            "technique": "freeform",
            "custom_prompt": custom_prompt,
            "example_custom": examples,
            "topics": topics,
            "is_demo": True,
            "max_concurrent_topics": min(5, len(topics)),
            "model_params": {
                "temperature": temperature,
                "top_p": 1.0,
                "max_tokens": 8192
            }
        }

        try:
            # Make API request
            response = requests.post(
                f"{self.api_url}/api/v1/synthesize",
                json=request_data,
                timeout=300
            )
            response.raise_for_status()
            result = response.json()

            # Process results
            if result.get("status") == "completed":
                print("✅ Generation completed successfully!")

                # Count statistics
                total_customers = 0
                total_accounts = 0
                total_transactions = 0

                all_data = []
                for topic, records in result.get("qa_pairs", {}).items():
                    for record in records:
                        # Parse the record if it's in question/solution format
                        if isinstance(record, dict) and "solution" in record:
                            try:
                                data = json.loads(record["solution"])
                            except json.JSONDecodeError:
                                continue
                        else:
                            data = record

                        all_data.append(data)
                        total_customers += 1
                        total_accounts += len(data.get("accounts", []))
                        total_transactions += len(data.get("transactions", []))

                print(f"\n📈 Statistics:")
                print(f"   Customers: {total_customers}")
                print(f"   Accounts: {total_accounts}")
                print(f"   Transactions: {total_transactions}")
                print(f"   Avg accounts per customer: {total_accounts/total_customers:.1f}")
                print(f"   Avg transactions per account: {total_transactions/total_accounts:.1f}")

                # Save to file
                if output_file is None:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_file = f"banking_data_{timestamp}.json"

                output_path = Path(output_file)
                output_path.parent.mkdir(parents=True, exist_ok=True)

                with open(output_path, 'w') as f:
                    json.dump(all_data, f, indent=2)

                print(f"\n💾 Data saved to: {output_path}")
                print(f"\n✨ Next steps:")
                print(f"   1. Review the data: cat {output_path} | jq .")
                print(f"   2. Evaluate quality: python evaluate_data.py --input-file {output_path}")
                print(f"   3. Flatten to CSV: python flatten_to_csv.py --input {output_path}")

                return str(output_path)
            else:
                print(f"❌ Generation failed: {result.get('error', 'Unknown error')}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"❌ API request failed: {e}")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None


def main():
    parser = argparse.ArgumentParser(
        description="Generate synthetic banking data with referential integrity",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate 10 customers with default topics
  python generate_data.py --num-customers 10

  # Generate 50 customers with custom topics
  python generate_data.py --num-customers 50 --topics "High Net Worth,Small Business,Retiree"

  # Use Claude Sonnet model with higher temperature
  python generate_data.py --num-customers 20 --model claude-3-5-sonnet --temperature 0.9

  # Specify output file
  python generate_data.py --num-customers 100 --output data/banking_dataset.json
        """
    )

    parser.add_argument(
        "--num-customers",
        type=int,
        default=10,
        help="Number of customer records to generate (default: 10)"
    )

    parser.add_argument(
        "--topics",
        type=str,
        default=None,
        help="Comma-separated list of topics/customer segments (default: predefined list)"
    )

    parser.add_argument(
        "--model",
        type=str,
        default="claude-3-5-haiku",
        choices=["claude-3-5-sonnet", "claude-3-5-haiku", "llama-3-70b", "llama-3-90b"],
        help="Model to use for generation (default: claude-3-5-haiku)"
    )

    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Sampling temperature 0.0-1.0 (default: 0.7)"
    )

    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output file path (default: banking_data_TIMESTAMP.json)"
    )

    parser.add_argument(
        "--api-url",
        type=str,
        default="http://localhost:8000",
        help="API base URL (default: http://localhost:8000)"
    )

    args = parser.parse_args()

    # Parse topics if provided
    topics = None
    if args.topics:
        topics = [t.strip() for t in args.topics.split(",")]

    # Generate data
    generator = BankingDataGenerator(api_url=args.api_url)
    output_file = generator.generate(
        num_customers=args.num_customers,
        topics=topics,
        model_name=args.model,
        temperature=args.temperature,
        output_file=args.output
    )

    if output_file:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
