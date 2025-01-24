from LLM.BinxAI import BinxyAI

binxy = BinxyAI()
binxy.StartBinxy(True)

while True:
    prompt = input("You: ")
    print(prompt)
    response = binxy.GetResponseFromAPI(prompt)
    if "Binxy" in response:
        response = response.replace("Binxy", "")
    if "You" in response:
        response = response.replace("You", "")
    if ": " in response:
        response = response.split(": ")[1]
    print("\n\n" + response + "\n\n")
    if prompt.lower() == "exit":
        break