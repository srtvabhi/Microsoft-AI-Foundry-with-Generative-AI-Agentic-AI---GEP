# Marketing Content Generator (Responses API)

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

            input_text = input("\nMarketing Request (or quit): ")

            if input_text.lower() == "quit":
                break

            response = openai_client.responses.create(
                model=model_deployment,
                instructions="""
                You are a marketing specialist.

                Create engaging and professional
                marketing content.
                """,
                input=input_text
            )

            print("\nResponse:")
            print(response.output_text)

    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()

#Test Prompts
#Write a LinkedIn post announcing a new AI-powered CRM platform.
#Create a marketing slogan for a cloud inventory system.
