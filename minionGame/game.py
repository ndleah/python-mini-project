import sys

instruction = '''
        Game Rules for Minion Game:
        1) Both players are given the same string.
        2) Stuart has to make substrings starting with consonants.
        3) Kevin has to make substrings starting with vowels.
        4) The player with higher score wins!
'''

VOWELS = {'a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'}

def is_vowel(char: str) -> bool:
    return char in VOWELS

def calculate_minion_scores(string_val: str) -> tuple:
    """Calculate Stuart (consonants) and Kevin (vowels) scores in O(N) time."""
    string_val = string_val.strip()
    n = len(string_val)
    stuart_score = 0  # Consonants
    kevin_score = 0   # Vowels

    for i in range(n):
        if is_vowel(string_val[i]):
            kevin_score += (n - i)
        else:
            stuart_score += (n - i)

    return stuart_score, kevin_score

def minion_game(s: str = None, player1_name: str = "Stuart", player2_name: str = "Kevin"):
    if not s:
        print(instruction)
        s = input("Enter any string / single word: ").strip()

    if not s:
        print("Error: Input string cannot be empty.")
        return

    stuart_score, kevin_score = calculate_minion_scores(s)

    print('\nOverall score:')
    print(f'{player1_name} (Consonants) : {stuart_score}')
    print(f'{player2_name} (Vowels)     : {kevin_score}')

    if stuart_score > kevin_score:
        print(f"-> {player1_name} wins with score {stuart_score}! 🏆")
    elif kevin_score > stuart_score:
        print(f"-> {player2_name} wins with score {kevin_score}! 🏆")
    else:
        print("-> Game ended in a Draw!")

def main():
    target_string = sys.argv[1] if len(sys.argv) > 1 else None
    minion_game(target_string)

if __name__ == '__main__':
    main()