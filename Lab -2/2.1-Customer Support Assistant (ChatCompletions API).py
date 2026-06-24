# Customer Support Assistant (ChatCompletions API)

import os
from dotenv import load_dotenv
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

def main():
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        load_dotenv()

        azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        model_deployment = os.getenv("MODEL_DEPLOYMENT")

        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(),
            "https://ai.azure.com/.default"
        )

        openai_client = OpenAI(
            base_url=azure_openai_endpoint,
            api_key=token_provider
        )

        while True:
            input_text = input("\nCustomer Query (or quit): ")

            if input_text.lower() == "quit":
                break

            completion = openai_client.chat.completions.create(
                model=model_deployment,
                messages=[
                    {
                        "role": "system",
                        "content": """
                        You are a customer support assistant for an
                        e-commerce company.

                        Be professional, polite, and solution-oriented.
                        """
                    },
                    {
                        "role": "user",
                        "content": input_text
                    }
                ]
            )

            print("\nResponse:")
            print(completion.choices[0].message.content)

    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()

#Test Prompts
#A customer received a damaged laptop. Draft a response offering assistance.
#A customer wants a refund for an order placed 15 days ago.
