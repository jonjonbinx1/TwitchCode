from DougDougTwitchConnection import Twitch



def main():
    twitchConnection = Twitch()

    twitchConnection.twitch_connect("j0nj0nbinx")
    print(twitchConnection.channel)
    while(True):
        messageList = twitchConnection.twitch_receive_messages()
        for message in messageList:
            print(message["message"])
main()