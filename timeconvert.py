import colorama
import time
colorama.init(autoreset=True)

stimezones = ["GMT", "WET", "CET", "EET", "UTC"]
while True:
    timez1 = input(colorama.Fore.BLUE + "what is your time zone? (currently only supports GMT, UTC, WET, CET and EET) " + colorama.Fore.GREEN)
    if (timez1 in stimezones):
        break
    else:
        print(colorama.Fore.RED + "Error: invalid time zone, make sure your spelling is right and that you're writing in all capital ")

while True:
    timez2 = input(colorama.Fore.BLUE + "which timezone do you want to convert to? " + colorama.Fore.GREEN)
    if (timez2 in stimezones):
        break
    else:
        print(colorama.Fore.RED + "Error: invalid time zone, make sure your spelling is right and that you're writing in all capital ")

while True:
    time1 = input(colorama.Fore.BLUE + "what time is it for you? (only input the hour, not the minute. use 24h format) " + colorama.Fore.GREEN)
    try:
        tester = int(time1)
        if (int(time1) <= 24):
            if (int(time1) > 12):
                time1 = int(time1) - 12
                suffix = "PM"
                break
            else:
                suffix = "AM"
                break
        else:
            print(colorama.Fore.RED + "Error: you can only input numbers, not letters or any special characters and you cannot go above 24")
    except:
        print(colorama.Fore.RED + "Error: you can only input numbers, not letters or any special characters and you cannot go above 24")
        
print()
print()
input(colorama.Fore.CYAN + f"your timezone is {timez1}, you want to convert it to {timez2}, it is {time1} o' clock {suffix} for you, press enter to continue (ctrl+c to try again) ")
print()
print(colorama.Fore.BLACK + colorama.Back.WHITE + "performing calculation...")

if (timez1 == "GMT" or timez1 == "UTC" or timez1 == "WET"):
    if (timez2 == "GMT" or timez2 == "UTC" or timez2 == "WET"):
        answer = int(time1)
    elif (timez2 == "EET"):
        answer = int(time1) + 2
    elif (timez2 == "CET"):
        answer = int(time1) + 1
    else:
        answer = colorama.Fore.RED + "Error: something didn't go as planned (please report if you see this message)"
elif (timez1 == "EET"):
    if (timez2 == "GMT" or timez2 == "UTC" or timez2 == "WET"):
        answer = int(time1) - 2
    elif (timez2 == "CET"):
        answer = int(time1) - 1
    elif (timez2 == "EET"):
        answer = int(time1)
    else:
        print(colorama.Fore.RED + "Error: you can only input numbers, not letters or any special characters and you cannot go above 24")
elif (timez1 == "CET"):
    if (timez2 == "CET"):
        answer = int(time1)
    elif (timez2 == "GMT", "UTC", "WET"):
        answer = int(time1) -1
    elif (timez2 == "EET"):
        answer = int(time1) + 1
time.sleep(3)
print()
if (answer == 0):
    answer = 12
elif (answer > 12):
    answer = answer - 12
print(f"in {timez2} it is {answer} o' clock!")