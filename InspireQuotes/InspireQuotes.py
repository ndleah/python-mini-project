# A game that sends you an inspirational quote when you choose a number.

def inspirational_quote(number):
    quotes = {
        1: "Believe you can and you're halfway there. -Theodore Roosevelt",
        2: "The future belongs to those who believe in the beauty of their dreams. -Eleanor Roosevelt.",
        3: "The only way to do great work is to love what you do. -Steve Jobs.",
        4: "Everything youve ever wanted is on the other side of fear. -George Addair.",
        5: "Success is not final, failure is not fatal: It is the courage to continue that counts. –Winston Churchill.",
        6: "The strongest principle of growth lies in the human choice. -George Eliot.",
        7: "Be yourself; everyone else is already taken. -Oscar Wilde.",
        8: "Be the change that you wish to see in the world. -Mahatma Gandh.",
        9: "If people are doubting how far you can go, go so far that you cant hear them anymore. -Michele Ruiz"
    }
    return quotes.get(number)

def main(): 
    print("Choose a number between 1-9 to receive an inpiring quote. ")
    try:
        number = int(input())
        quote = inspirational_quote(number)
        print(quote) 
    except ValueError:
        print("Please enter a valid number.")
        
if __name__ == "__main__":
    main()
    