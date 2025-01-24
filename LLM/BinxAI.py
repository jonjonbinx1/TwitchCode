import gpt4all
import os
import json

# Initialize the GPT-4All model
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Get the model path from the config
model_path = config["model_path"]
model = gpt4all.GPT4All(model_path, device="gpu")

# Initialize conversation history
conversation_history = ""
#load initial context if the file exists
if os.path.exists(config["model_initial_context"]):
    with open(config["model_initial_context"], "r") as file:
        conversation_history = file.read()
    print("initial context loaded")

#load the latest conversation history if the file exists
if os.path.exists("conversation_history.txt"):
    with open("conversation_history.txt", "r") as file:
        conversation_history = file.read()
while True:
    prompt = input("Enter your prompt: ")
    if prompt.lower() == "exit":
        break

    # Update conversation history with the new prompt
    conversation_history += prompt

    # Generate text with the conversation history
    response = model.generate(conversation_history)

    # Update conversation history with the model's response
    conversation_history += response

    # Print the generated text
    print(response)

# Save the conversation history to a text file
with open("conversation_history.txt", "w") as file:
    file.write(conversation_history)
