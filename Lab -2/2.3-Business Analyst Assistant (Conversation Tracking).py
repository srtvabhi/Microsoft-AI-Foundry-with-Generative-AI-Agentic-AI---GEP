# Business Analyst Assistant (Conversation Tracking)

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

        last_response_id = None

        while True:

            input_text = input("\nBusiness Query (or quit): ")

            if input_text.lower() == "quit":
                break

            response = openai_client.responses.create(
                model=model_deployment,
                instructions="""
                You are a business analyst.

                Analyze business situations and
                provide recommendations.
                """,
                input=input_text,
                previous_response_id=last_response_id
            )

            print("\nResponse:")
            print(response.output_text)

            last_response_id = response.id

    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()

#Test Conversation
#Prompt 1: A retail company has experienced a 15% decline in sales over the last quarter.
#Prompt 2: What could be the possible reasons?
#Prompt 3: Suggest strategies to improve sales.
#Prompt 4: Which strategy should be prioritized first?
