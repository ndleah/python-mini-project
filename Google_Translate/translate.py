from googletrans import Translator, LANGUAGES
translator = Translator()

language_options = LANGUAGES.items()
language_codes = []
language_names = []

def errors():
    print('Unknown Language. Wisely choose from this')
    print(f"Language Codes {language_codes}\n")
    print(f'Or from Language Names \n {language_names}')

for options in language_options:
    language_codes.append(options[0])
    language_names.append(options[1].lower())
    
    
translating_from = input("Enter the language you want to translate from\n").lower()
word = input('Enter the word\n').lower()
translating_to = input("Enter the language you want to translate to\n").lower()

try:
    
    if translating_from and translating_to in language_codes or language_names:
        translation =  translator.translate(word,src=translating_from, dest=translating_to).text
    
        print(translation.capitalize())
    else:
        errors()
except:
    print("Something went wrong or \n")
    errors()