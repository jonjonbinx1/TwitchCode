import gpt4all
import os
import json
import torch
import requests

class BinxyAI:
    # model = None
    conversation_history = []

    def StartBinxy(self, load_past_context):
        # Initialize the GPT-4All model
        with open("config.json", "r") as config_file:
            config = json.load(config_file)

        # Get the model path from the config (uncomment if needed)
        # model_path = config["model_path"]
        # self.model = gpt4all.GPT4All(model_path, device="cuda")

        # Load initial context if the file exists
        # if os.path.exists(config["model_initial_context"]):
        #     with open(config["model_initial_context"], "r") as file:
        #         initial_context = file.read()
        #     self.conversation_history.append(initial_context)
        #     print("Initial context loaded")

        # Load the latest conversation history if the file exists
        if os.path.exists("conversation_history.txt") and load_past_context:
            with open("conversation_history.txt", "r") as file:
                saved_history = file.read().splitlines()
                self.conversation_history.extend(saved_history)

    def GetResponseFromAPI(self, prompt):
        url = "http://localhost:4891/v1/chat/completions"
        headers = {
            "Content-Type": "application/json"
        }

        # Update conversation history with a sliding window
        if prompt.lower() == "exit":
            # Save the conversation history to a file
            with open("conversation_history.txt", "w") as file:
                file.write("\n".join(self.conversation_history))
            self.conversation_history.append("Say Goodbye Binxy!")
        else:
            self.conversation_history.append(f"You: {prompt}")
            if len(self.conversation_history) > 8:  # Sliding window of the last 4 user-AI pairs
                self.conversation_history = self.conversation_history[-8:]

        # Prepare the input prompt with the current sliding window conversation history
        input_prompt = "\n".join(self.conversation_history)
        data = {
            "model": "MPT Chat",
            "messages": [{"role": "user", "content": input_prompt}],
            "max_tokens": 500,
            "temperature": 0.28
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            response_json = response.json()
            content = response_json['choices'][0]['message']['content']
            self.conversation_history.append(f"Binxy: {content}")
            return content
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None
