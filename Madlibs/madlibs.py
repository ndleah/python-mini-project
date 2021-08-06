import random
print("Title : Eat, Drink, And Be Sick")
noun = []
for i in range(4):
    n = input("Enter noun : ")
    noun.append(n)
plural = []
for i in range(6):
    pn = input("Enter plural noun : ")
    plural.append(pn)
adjective = []
for i in range(2):
    a = input("Enter adjective : ")
    adjective.append(a)
adverb = input("Enter adverb : ")
letter = input("Enter any letter : ")
body_part = input("Enter any body part : ")
print("An inspector from the Department of Health and ", random.choice(noun) , " Services paid a surprise visit to our " , random.choice(adjective) , " school cafeteria.")
print("The lunch special, prepared by our " , random.choice(adjective) , "dietician, was spaghetti and " , random.choice(noun) , " balls with a choice of either a " , random.choice(noun) , " salad or French " , random.choice(plural) , ".")
print("The inspector found the meat-" , random.choice(plural) , " to be overcooked and discovered a live " , random.choice(noun) , " in the fries,causing him to have a " + body_part + " ache.")
print("In response, he threw up all over his " , random.choice(plural) , ".")
print("In his report, the inspector " + adverb + " recommended that the school cafeteria serve only nutritious " , random.choice(plural) , " as well as low-calorie " , random.choice(plural) , " and that all of the saturated " , random.choice(plural) , " be eliminated.")
print("He rated the cafeteria a " + letter + "-minus.")
