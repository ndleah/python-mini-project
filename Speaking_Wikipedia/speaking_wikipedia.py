import pyttsx3
import wikipedia
from pprint import pprint


def page(title: str, sentences = 2):
    """
    :param title: (str) the title of the Wikipedia page to summarize
    :param sentences: (int) the number of sentences to include in the summary (optional, default is 2)
    :return: (str) the summary of the Wikipedia page
    """

    content = wikipedia.summary(title, sentences = sentences)

    return content


def voicing_text(text):
    """
    Speaks the given text using the text-to-speech engine
    :param text: (str) the text to speak
    :return: (str) the input text
    """

    # Initialize the engine
    engine = pyttsx3.init()

    # Set the voice to be used
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    # Speak the text
    engine.say(text)

    engine.runAndWait()

    # returns the input text in order to provide subtitles for the spoken audio
    return text

def main():
    # Specify values:
    wiki_page = input("Enter the name of the  wikipedia page: ")

    specify_num_of_sentences = input("Do you want to specify the number of sentences (default is 2)? (y/n): ")

    if specify_num_of_sentences == "y" or specify_num_of_sentences == "Y":

        num_of_sentences = input("Enter the number of sentences to include in the summary: ")

        print(voicing_text(page(wiki_page, num_of_sentences)))
    else:

        print(voicing_text(page(wiki_page)))

if __name__ == "__main__":
    main()
