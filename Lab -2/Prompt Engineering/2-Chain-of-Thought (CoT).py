# Chain-of-Thought (CoT)
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

        # Initialize client
        openai_client = OpenAI(
            base_url=azure_openai_endpoint,
            api_key=token_provider
        )

        # Continuous loop
        while True:
            user_input = input('\nEnter a question (or type "quit" to exit): ')

            if user_input.lower() == "quit":
                print("Exiting...")
                break

            if not user_input.strip():
                print("Please enter a valid question.")
                continue

            # ✅ Explicit Chain-of-Thought Prompt
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful AI assistant. "
                        "Solve the problem step by step. "
                        "Clearly show each reasoning step. "
                        "Finally, provide the answer in a separate line starting with 'Final Answer:'."
                    )
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]

            # Call API
            completion = openai_client.chat.completions.create(
                model=model_deployment,
                messages=messages,
                temperature=0.3
            )

            # Print output
            print("\nResponse:\n")
            print(completion.choices[0].message.content.strip())

    except Exception as ex:
        print("Error:", ex)


if __name__ == "__main__":
    main()


# Test prompt :
# A car travels 40 km/h for 2.5 hours. How far does it go?