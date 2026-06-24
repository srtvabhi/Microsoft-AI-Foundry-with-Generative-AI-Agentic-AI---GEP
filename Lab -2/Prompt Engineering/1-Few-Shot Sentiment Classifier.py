# Few-Shot Sentiment Classifier

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

        # ✅ Few-shot examples for sentiment classification
        few_shot_examples = [
            {"role": "user", "content": "I love this product, it's amazing!"},
            {"role": "assistant", "content": "Positive"},

            {"role": "user", "content": "This is the worst experience I've ever had."},
            {"role": "assistant", "content": "Negative"},

            {"role": "user", "content": "The product is okay, nothing special."},
            {"role": "assistant", "content": "Neutral"},

            {"role": "user", "content": "Absolutely fantastic service!"},
            {"role": "assistant", "content": "Positive"},

            {"role": "user", "content": "I'm not happy with the results."},
            {"role": "assistant", "content": "Negative"}
        ]

        while True:
            input_text = input('\nEnter text for sentiment analysis (or "quit"): ')
            
            if input_text.lower() == "quit":
                break
            if len(input_text.strip()) == 0:
                print("Please enter valid text.")
                continue

            # ✅ Build messages
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a sentiment analysis assistant. "
                        "Classify the user's input into exactly one word: "
                        "Positive, Negative, or Neutral. "
                        "Do not explain. Do not add extra text."
                    )
                }
            ]

            # Add few-shot examples
            messages.extend(few_shot_examples)

            # Add current input
            messages.append({
                "role": "user",
                "content": input_text
            })

            # ✅ API call
            completion = openai_client.chat.completions.create(
                model=model_deployment,
                messages=messages,
                temperature=0  # 🔥 Important for classification consistency
            )

            print("\nSentiment:", completion.choices[0].message.content.strip())

    except Exception as ex:
        print("Error:", ex)

if __name__ == '__main__':
    main()


# test prompt
# I really enjoyed this movie!
# This is terrible.
# It works fine, nothing special.