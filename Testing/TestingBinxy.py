from LLM.BinxAI import BinxyAI
from Audio.BinxyVoice import BinxyVoice
from SpeechToText.TalkToBinxy import Listener
binxy = BinxyAI()
binxy.StartBinxy(True)
binxy_voice = BinxyVoice()
binxy_listener = Listener()
# binxy_starters = ["Hey Binxy", "Hello Binxy", "Hi Binxy", "Binxy"]
while True:
    prompt = binxy_listener.listen_to_audio()
    prompt = prompt.replace("Banksy", "Binxy")
    # if(any(starter.lower() in prompt.lower() for starter in binxy_starters)):
    #     for starter in binxy_starters:
    #         if starter in prompt:
    #             prompt = prompt.lower().split(starter.lower(), 1)[1].strip()
    #         break
    if(len(prompt.split(" ")) >= 5 and prompt != "Sorry, I could not understand the audio."):
        print(prompt)
        response = binxy.GetResponseFromAPI(prompt)
        if "Binxy" in response:
            response = response.replace("Binxy", "")
        if "You" in response:
            response = response.replace("You", "")
        if ": " in response:
            response = response.split(": ")[1]
        print("\n\n" + response + "\n\n")
        binxy_voice.generate_and_play_speech(response)
        if prompt.lower() == "exit":
            break