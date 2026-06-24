#Few-shot + Chain-of-Thought

import os
from dotenv import load_dotenv
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

def main():
    # Clear console
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        # Load environment variables
        load_dotenv()
        azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        model_deployment = os.getenv("MODEL_DEPLOYMENT")

        # Azure AD authentication
        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(),
            "https://ai.azure.com/.default"
        )

        # Initialize OpenAI client
        openai_client = OpenAI(
            base_url=azure_openai_endpoint,
            api_key=token_provider
        )

        # ✅ Few-shot + CoT examples
        few_shot_cot_examples = [
            {
                "role": "user",
                "content": "If 2 apples cost $4, how much do 5 apples cost?"
            },
            {
                "role": "assistant",
                "content": (
                    "Step 1: Calculate cost per apple = 4 ÷ 2 = 2\n"
                    "Step 2: Calculate cost of 5 apples = 5 × 2 = 10\n\n"
                    "Final Answer: $10"
                )
            },
            {
                "role": "user",
                "content": "A car travels 60 km in 1 hour. How far will it travel in 3 hours?"
            },
            {
                "role": "assistant",
                "content": (
                    "Step 1: Speed = 60 km per hour\n"
                    "Step 2: Time = 3 hours\n"
                    "Step 3: Distance = Speed × Time = 60 × 3 = 180\n\n"
                    "Final Answer: 180 km"
                )
            }
        ]

        # Continuous interaction loop
        while True:
            user_input = input('\nEnter a question (or type "quit" to exit): ')

            if user_input.lower() == "quit":
                print("Exiting...")
                break

            if not user_input.strip():
                print("Please enter a valid question.")
                continue

            # ✅ Build message list
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful AI assistant. "
                        "Solve the problem step by step. "
                        "Show all reasoning steps clearly. "
                        "End your response with 'Final Answer:' followed by the answer."
                    )
                }
            ]

            # Add few-shot CoT examples
            messages.extend(few_shot_cot_examples)

            # Add user input
            messages.append({
                "role": "user",
                "content": user_input
            })

            # ✅ API call
            completion = openai_client.chat.completions.create(
                model=model_deployment,
                messages=messages,
                temperature=0.2  # lower = better reasoning consistency
            )

            # Print response
            print("\nResponse:\n")
            print(completion.choices[0].message.content.strip())

    except Exception as ex:
        print("Error:", ex)


if __name__ == "__main__":
    main()

#Test Prompt :If a train travels 80 km/h for 2.5 hours, how far does it go?