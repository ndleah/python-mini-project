import sys
import json
import urllib.parse
import urllib.request

try:
    from googletrans import Translator, LANGUAGES
    GOOGLETRANS_AVAILABLE = True
except Exception:
    GOOGLETRANS_AVAILABLE = False
    LANGUAGES = {
        'en': 'english', 'es': 'spanish', 'fr': 'french', 'de': 'german',
        'it': 'italian', 'ja': 'japanese', 'ko': 'korean', 'zh-cn': 'chinese (simplified)',
        'ru': 'russian', 'hi': 'hindi', 'pt': 'portuguese', 'ar': 'arabic'
    }

language_codes = list(LANGUAGES.keys())
language_names = [v.lower() for v in LANGUAGES.values()]

def translate_mymemory_fallback(text: str, src: str = 'en', dest: str = 'es') -> str:
    """Translate text using public MyMemory API via HTTP request."""
    try:
        langpair = f"{src}|{dest}"
        url = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(text)}&langpair={urllib.parse.quote(langpair)}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            translated_text = data.get("responseData", {}).get("translatedText")
            if translated_text:
                return translated_text
    except Exception as e:
        print(f"MyMemory API fallback notice: {e}")
    return text

def normalize_lang_code(lang_str: str) -> str:
    """Convert language name or code to standard ISO language code."""
    lang_str = lang_str.strip().lower()
    if lang_str in language_codes:
        return lang_str
    if lang_str in language_names:
        for code, name in LANGUAGES.items():
            if name.lower() == lang_str:
                return code
    return None

def translate_text(text: str, src: str = 'auto', dest: str = 'en') -> str:
    """Translate text from source language to target language."""
    if not text:
        return ""

    src_code = normalize_lang_code(src) if src != 'auto' else 'auto'
    dest_code = normalize_lang_code(dest)

    if not dest_code:
        print(f"Error: Target language '{dest}' is not recognized.")
        print(f"Supported language codes: {language_codes[:10]}...")
        return None

    if GOOGLETRANS_AVAILABLE:
        try:
            translator = Translator()
            res = translator.translate(text, src=src_code or 'auto', dest=dest_code)
            if res and res.text:
                print(f"Translation ({src_code} -> {dest_code}): {res.text.capitalize()}")
                return res.text
        except Exception as e:
            print(f"Notice: googletrans library error ({e}). Using MyMemory API fallback...")

    # Fallback to MyMemory HTTP API
    src_final = src_code if src_code and src_code != 'auto' else 'en'
    translated = translate_mymemory_fallback(text, src_final, dest_code)
    print(f"Translation ({src_final} -> {dest_code}): {translated.capitalize()}")
    return translated

def main():
    if len(sys.argv) >= 4:
        src = sys.argv[1]
        dest = sys.argv[2]
        text = " ".join(sys.argv[3:])
    else:
        src = input("Enter the language to translate from (code/name, e.g. 'en' or 'english'): ").strip()
        text = input("Enter the word or phrase: ").strip()
        dest = input("Enter the language to translate to (code/name, e.g. 'es' or 'spanish'): ").strip()

    translate_text(text, src, dest)

if __name__ == '__main__':
    main()