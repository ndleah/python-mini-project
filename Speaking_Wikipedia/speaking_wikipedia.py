import sys
import pyttsx3
import wikipedia

def page(title: str, sentences: int = 2) -> str:
    """
    :param title: (str) the title of the Wikipedia page to summarize
    :param sentences: (int) the number of sentences to include in the summary
    :return: (str) the summary of the Wikipedia page
    """
    try:
        sentences_count = int(sentences)
    except (ValueError, TypeError):
        sentences_count = 2

    try:
        content = wikipedia.summary(title, sentences=sentences_count)
        return content
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Ambiguous topic '{title}'. Options include: {', '.join(e.options[:5])}"
    except wikipedia.exceptions.PageError:
        return f"Page '{title}' not found on Wikipedia."
    except Exception as e:
        return f"Error fetching Wikipedia page: {e}"

def voicing_text(text: str) -> str:
    """
    Speaks the given text using the text-to-speech engine
    :param text: (str) the text to speak
    :return: (str) the input text
    """
    if not text:
        return ""

    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        if voices:
            engine.setProperty('voice', voices[0].id)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"TTS Audio Notice: {text}")

    return text

def main():
    wiki_page = input("Enter the name of the Wikipedia page: ").strip()
    if not wiki_page:
        print("Error: Page title cannot be empty.")
        return

    specify_num_of_sentences = input("Do you want to specify the number of sentences (default is 2)? (y/n): ").strip().lower()

    if specify_num_of_sentences in ("y", "yes"):
        raw_num = input("Enter the number of sentences to include in the summary: ").strip()
        try:
            num = int(raw_num)
        except ValueError:
            print("Invalid number. Defaulting to 2 sentences.")
            num = 2
        summary_text = page(wiki_page, num)
    else:
        summary_text = page(wiki_page)

    print("\n--- Wikipedia Summary ---")
    print(summary_text)

    voicing_text(summary_text)

if __name__ == "__main__":
    main()

