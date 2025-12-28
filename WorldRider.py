name = input("Enter your name: ")
print(f"Hello {name}, and welcome! We are going to go on a Journey... are you ready?")

# --- THE ENTRANCE ---
i1 = input("\nYou have reached the gates of the Dark Dungeon. Do you want to enter? (yes/no): ").lower()

if i1 == "yes":
    print("\nYou push the heavy iron gates open. They creak loudly, echoing into the abyss.")
    print("The air is cold and damp, but you step forward with courage.")
else:
    print("\nYou turn to run back to the safety of the woods...")
    print("Suddenly, two giant trolls jump from the shadows, blocking your path!")
    print("They laugh menacingly: 'Nobody leaves the Rider's path so easily!'")
    print("They grab you by the collar and throw you deep into the dungeon entrance.")

print("\n--- THE JOURNEY BEGINS ---")
print("You find yourself in a flickering torch-lit hallway.")

# --- THE FORK IN THE ROAD ---
i2 = input("You reach two paths. Do you go Left toward a 'golden glow' or Right toward 'heavy breathing'? ").lower()

# PATH 1: THE RIGHT (The Troll/Stone of Strength)
if "right" in i2:
    print("\nYou encounter a massive Troll blocking the path!")
    i3 = input("Do you choose to 'walk away' quietly or 'fight' the troll? ").lower()

    if i3 == "walk away":
        print("You sneak away... but fall into a pit of wolves. Game Over!")
    elif i3 == "fight":
        print("You defeat the troll and obtain the 'Stone of Strength'!")
        relic = "Stone of Strength"
    else:
        print("You hesitated... the troll smashes you. Game Over!")

# PATH 2: THE LEFT (The Temple/Amulet of Wisdom)
elif "left" in i2:
    print("\nYou find a hidden underground temple.")
    i4 = input("You see a golden chest. Do you 'open' it or 'ignore' it? ").lower()

    if i4 == "open":
        print("Light fills the room! You discover the 'Amulet of Wisdom'!")
        relic = "Amulet of Wisdom"
    elif i4 == "ignore":
        print("The floor collapses. Game Over!")
    else:
        print("The spirits consume you. Game Over!")

else:
    print("The walls close in while you hesitate. Game Over!")
    relic = None

# --- EXPANDED STORY: THE MERCHANT OF SOULS ---
if 'relic' in locals() and relic:
    print(f"\n--- NEW AREA: THE SILENT BAZAAR ---")
    print(f"As you carry your {relic}, you meet a hooded Merchant sitting by a blue fire.")
    print("Merchant: 'That is a fine prize. I can upgrade its power, but it will cost you your memories.'")
    
    trade = input("Do you 'trade' part of your soul for more power, or 'keep' walking? ").lower()
    
    if trade == "trade":
        print(f"\nYour {relic} begins to glow with a dark, purple energy.")
        print(f"You are now more powerful, but you have forgotten your name, {name[0]}... {name[0:2]}... ???")
        print("You have become the Shadow Rider. To be continued...")
    else:
        print(f"\nYou keep your soul intact and find a secret exit behind the merchant.")
        print(f"You emerge from the dungeon as {name}, the Hero of Light!")