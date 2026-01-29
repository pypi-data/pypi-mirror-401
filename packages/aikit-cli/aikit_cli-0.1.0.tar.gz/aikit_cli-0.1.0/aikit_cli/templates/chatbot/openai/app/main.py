from provider import OpenAIProvider


def run():
    provider = OpenAIProvider()
    messages: list[dict] = []

    print("Chat started. Press Ctrl+C to exit.")

    try:
        while True:
            user_input = input("> ")
            messages.append({"role": "user", "content": user_input})

            reply = provider.chat(messages)
            print(reply)

            messages.append({"role": "assistant", "content": reply})
    except KeyboardInterrupt:
        print("\nBye.")


if __name__ == "__main__":
    run()
