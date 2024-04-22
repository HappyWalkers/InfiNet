from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import argparse
import os

api_key = "uxcZFMC9rChDMiXUb4ntLkq6wqAMSRX2"
model = "mistral-large-latest"

client = MistralClient(api_key=api_key)

# chat_response = client.chat(
#     model=model,
#     messages=[ChatMessage(role="user", content="What is the best French cheese?")]
# )

# print(chat_response.choices[0].message.content)


# the caption dir contains caption files named "*.txt"
# the files are in hierarchical structure
# the function should use the Mistral API to generate a summary of the captions if the files contain more than one line
# the summary should be rewritten to the same file
def caption_summary(caption_dir):
    summary_template = "You're a very accurate caption assistant.  You'll be given some sentences that describe each frame in a video. You'll sum up the sentences using less than 50 words that can then be used to reconstruct the video.{}"
    dir_queue = []
    dir_queue.append(caption_dir)
    while len(dir_queue) > 0:
        current_dir = dir_queue.pop(0)
        for f in os.listdir(current_dir):
            if os.path.isdir(os.path.join(current_dir, f)):
                dir_queue.append(os.path.join(current_dir, f))
            else:
                if f.endswith(".txt"):
                    with open(os.path.join(current_dir, f), "r") as file:
                        lines = file.readlines()
                        if len(lines) > 1:
                            chat_response = client.chat(
                                model=model,
                                messages=[ChatMessage(role="user", content=summary_template.format("".join(lines)))]
                            )
                            with open(os.path.join(current_dir, f), "w") as file:
                                file.write(chat_response.choices[0].message.content)


# the main function should take arguments from command line
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--caption_dir", type=str, help="Path to the directory containing the captions")
    args = parser.parse_args()
    caption_summary(args.caption_dir)

if __name__ == '__main__':
    main()