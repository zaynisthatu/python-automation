import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def main():
    conversation = []

    print("ChatGPT se baat shuru karo! ('bye' likho exit karne ke liye)\n")

    while True:
        user_input = input("Tum: ").strip()
        if user_input.lower() == "bye":
            print("Chat khatam. Conversation file mein save kar di gayi hai.")
            break

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # Ya "gpt-3.5-turbo" agar free user ho
                messages=[
                    {"role": "system", "content": "Tum ek friendly teacher ho jo Roman Urdu mein samjhata hai."},
                    {"role": "user", "content": user_input}
                ]
            )

            ai_response = response.choices[0].message.content.strip()
            print(f"ChatGPT: {ai_response}\n")

            conversation.append(f"**Tum:** {user_input}\n\n**ChatGPT:** {ai_response}\n\n---\n")

        except Exception as e:
            print(f"❌ Error: {e}")

    with open("chat_convo.md", "w", encoding="utf-8") as f:
        f.write("# ChatGPT Conversation\n\n")
        f.writelines(conversation)

if __name__ == "__main__":
    main()
