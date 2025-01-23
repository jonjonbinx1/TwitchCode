from transformers import pipeline

# Load the summarization pipeline from Hugging Face
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_messages(messages):
    concatenated_messages = " ".join(messages)
    summary_list = summarizer(concatenated_messages, max_length=150, min_length=40, do_sample=False)
    # Extract and print the text of the summary
    summary = summary_list[0]['summary_text']
    return summary

# Example usage with a list of chat messages
messages = [
    "Pikachu is my favorite Pokémon, hands down!",
    "I think Charmander is pretty cool too.",
    "The weather today is quite sunny.",
    "Bulbasaur has always been my top choice.",
    "Did you hear the new iPhone was released yesterday?",
    "Squirtle squad for life!",
    "I just finished reading a fantastic book.",
    "Jigglypuff's singing is so cute.",
    "Traveling helps broaden your perspective.",
    "Eevee's evolutions are amazing!",
    "Listening to music always relaxes me.",
    "Gengar is such a spooky Pokémon!",
    "I love playing video games in my free time.",
    "Mewtwo is a total powerhouse.",
    "How do you feel about pineapple on pizza?",
    "I think it's definitely Pikachu.",
    "No way, it's gotta be Gengar.",
    "I'm pretty sure it's Bulbasaur.",
    "It could be Jigglypuff.",
    "Pikachu is the most likely option.",
    "Maybe it's Charizard.",
    "I'm sure it's Gengar.",
    "Pikachu is the answer for sure!",
    "It might be Eevee.",
    "Gengar is my guess.",
    "Definitely Pikachu!",
    "Not sure, but I'll go with Pikachu.",
    "Could it be Squirtle?",
    "I have a strong feeling it's Gengar.",
    "I heard someone say it's Pikachu.",
    "Nah, it's probably Bulbasaur.",
    "It's gotta be Pikachu, right?",
    "Gengar all the way!",
    "I'm convinced it's Pikachu.",
    "My bet is on Gengar.",
]

summary = summarize_messages(messages)
print(f"Summary: {summary}")
