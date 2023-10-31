import time
from essential_generators import DocumentGenerator

def typing_speed():

    # Generating a random sentence
    gen = DocumentGenerator()
    String = gen.sentence()
    wordcount=len(String.split())

    # Typing Speed Calculation
    print(String)
    print("----------------------------------------")
    startTime=time.time()
    textInput=str(input("Type the sentence: " ))
    endTime=time.time()
    accuracy= len(set(textInput.split())&set(String.split()))
    accuracy=accuracy/wordcount*100
    timeTaken=round(endTime-startTime,2)
    wpm=round((wordcount/timeTaken)*60)
    print("----------------------------------------")

    # Showing the results
    print ("Your accuracy is: ", accuracy)
    print ("Time taken: ", timeTaken, "seconds")
    print("Your typing speed is: ",wpm,"words per minute")

    if accuracy < 50 or wpm < 30:
        print("You need to practice typing more!")
    elif accuracy < 80 or wpm < 60:
        print("You are doing great!")
    elif accuracy <= 100 or wpm <= 100:
        print("You are a pro in typing!")
    else:
        print("You are a typing machine!")


if __name__ == "__main__":
    print("Let's Start")   
    typing_speed()

    while True :  
        if input("Do you want to try again? (y/n): ")=="y":
            print("\n")
            typing_speed()
        else:
            break    