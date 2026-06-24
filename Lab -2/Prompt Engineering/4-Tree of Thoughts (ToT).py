# Tree of Thoughts (ToT) 

import os
from dotenv import load_dotenv
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

def generate_thoughts(client, model, problem):
    """Generate multiple candidate solutions (branches)"""

    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert problem solver. "
                "Generate 3 different possible solutions to the given problem. "
                "Keep them distinct and concise."
            )
        },
        {
            "role": "user",
            "content": problem
        }
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7
    )

    return response.choices[0].message.content


def evaluate_thoughts(client, model, problem, thoughts):
    """Evaluate and score each solution"""

    messages = [
        {
            "role": "system",
            "content": (
                "You are an evaluator. "
                "Analyze the given solutions and compare them. "
                "List pros and cons of each and clearly indicate the best solution."
            )
        },
        {
            "role": "user",
            "content": f"Problem:\n{problem}\n\nSolutions:\n{thoughts}"
        }
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.3
    )

    return response.choices[0].message.content


def main():
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        load_dotenv()
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        model = os.getenv("MODEL_DEPLOYMENT")

        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(),
            "https://ai.azure.com/.default"
        )

        client = OpenAI(
            base_url=endpoint,
            api_key=token_provider
        )

        while True:
            problem = input("\nEnter problem (or 'quit'): ")

            if problem.lower() == "quit":
                print("Exiting...")
                break

            if not problem.strip():
                print("Please enter a valid problem.")
                continue

            print("\n🌱 Generating multiple reasoning paths...\n")
            thoughts = generate_thoughts(client, model, problem)
            print("Candidate Solutions:\n")
            print(thoughts)

            print("\n🌿 Evaluating solutions...\n")
            evaluation = evaluate_thoughts(client, model, problem, thoughts)

            print("Final Evaluation:\n")
            print(evaluation)

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()


# test prompt : A company wants to increase customer retention by 20%.