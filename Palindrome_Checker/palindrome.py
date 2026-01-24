import pyinputplus as pyip
import string

#Check if word is a palindrome
def word_check():
    strng = pyip.inputStr("\nWhat word would you like to check?\n") #User enters suspected palindrome
    strng = strng.lower() #Adjust to lowercase to remove case sensitivity errors

    word_reversed = strng[::-1] #string slicing reverses word & compares it
    if strng == word_reversed:
        print(f'\nThe word "{strng}" is a palindrome!')
    else:
        print(f'\nThe word "{strng}" is not a palindrome.')

def sentence_check():
    strng = pyip.inputStr("\nEnter a sentence to check for palindromes!\n") #User enters suspected palindrome

    strng = strng.lower() #Adjust to lowercase to remove case sensitivity
    strng = strng.strip(string.punctuation) #remove punctuation

    word_list = strng.split()
    pdromes = []

    #Iterate over every word in the string to check for palindromes
    for word in word_list:
        word_reversed = word[::-1]
        #store palindromes in their own list
        if word == word_reversed:
            pdromes.append(word)

    #Get count of total palindromes and list them out    
    pdrome_count = len(pdromes)
    if pdrome_count == 1:
        print('\n1 palindrome was detected!')
        print(f'-{pdromes[0]}')
    elif pdrome_count > 1:
        print(f'\n{pdrome_count} palindromes detected!')
        print(f'Palindromes: ')
        for word in pdromes:
            print(f'-{word}')
    else:
        print('\nNo palindromes were detected.')

def main():
    choice = pyip.inputInt('\nCheck a [1] Word or [2] Sentence?\n', min=1, max=2)
    if choice == 1:
        word_check()
    else:
        sentence_check()

#Run main program
main()

#Infinite loop for re-runs

while True:
    restart = pyip.inputYesNo("\nWould you like to check another word or sentence? (y/n): \n")
    if restart == "yes":
        main()
    else:
        print("\n--Ending Program---")
        break