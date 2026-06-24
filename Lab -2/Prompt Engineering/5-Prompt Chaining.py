# Prompt Chaining

import os
from dotenv import load_dotenv
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

def call_llm(client, model, system_prompt, user_prompt, temperature=0.5):
    """Reusable function to call Azure OpenAI"""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=temperature
    )
    return response.choices[0].message.content.strip()


def main():
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        # Load environment variables
        load_dotenv()
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        model = os.getenv("MODEL_DEPLOYMENT")

        # Azure authentication
        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(),
            "https://ai.azure.com/.default"
        )

        client = OpenAI(
            base_url=endpoint,
            api_key=token_provider
        )

        while True:
            task = input("\nEnter task (or 'quit'): ")

            if task.lower() == "quit":
                print("Exiting...")
                break

            if not task.strip():
                print("Please enter a valid task.")
                continue

            print("\n🔹 Step 1: Identifying Target Audience...\n")

            # ✅ Prompt 1: Target audience
            step1_output = call_llm(
                client,
                model,
                "You are a marketing expert.",
                f"Task: {task}\n\nIdentify the target audience for this product launch."
            )

            print("Target Audience:\n", step1_output)

            print("\n🔹 Step 2: Generating Marketing Messages...\n")

            # ✅ Prompt 2: Marketing messages (uses step1 output)
            step2_output = call_llm(
                client,
                model,
                "You are a marketing strategist.",
                f"Task: {task}\n\nTarget Audience:\n{step1_output}\n\nGenerate key marketing messages tailored to this audience."
            )

            print("Marketing Messages:\n", step2_output)

            print("\n🔹 Step 3: Creating 30-Day Launch Plan...\n")

            # ✅ Prompt 3: Launch plan (uses step2 output)
            step3_output = call_llm(
                client,
                model,
                "You are a product launch planner.",
                f"Task: {task}\n\nMarketing Messages:\n{step2_output}\n\nCreate a detailed 30-day product launch plan."
            )

            print("Launch Plan:\n", step3_output)

            print("\n✅ Final Output: Complete Campaign\n")

            # ✅ Final combined output
            final_output = f"""
==============================
PRODUCT LAUNCH CAMPAIGN
==============================

🎯 Target Audience:
{step1_output}

📢 Marketing Messages:
{step2_output}

📅 30-Day Launch Plan:
{step3_output}
"""
            print(final_output)

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()

# test prompt  : Create a Product Launch Campaign for a fitness app