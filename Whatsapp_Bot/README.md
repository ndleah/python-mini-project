<!--Please do not remove this part-->
![Star Badge](https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20Useful&style=style=flat&color=BC4E99)
![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)

# Whatsapp Bot

<!--An image is an illustration for your project, the tip here is using your sense of humour as much as you can :D 

You can copy paste my markdown photo insert as following:
<p align="center">
<img src="your-source-is-here" width=40% height=40%>
-->
![whatsappbot](https://user-images.githubusercontent.com/87910771/147886971-3b084c89-3370-43a6-9bf7-cf31716691be.png)


## 🛠️ Description
<!--Remove the below lines and add yours -->
A Simple Bot made using Python to Send WhatsApp Message.

The used library is pywhatkit, and it can be found [here](https://github.com/Ankit404butfound/PyWhatKit).

## ⚙️ Languages or Frameworks Used
<!--Remove the below lines and add yours -->
Open Command Prompt and use the following command to install the required modules:

```sh 
pip install pywhatkit
```

## 🌟 How to run
<!--Remove the below lines and add yours -->
Just open a terminal in the folder where your script is located and run the following command:

```sh
python main.py
```

There are several options to send a message:

```sh
# Send a WhatsApp Message to a Contact at 1:30 PM
pywhatkit.sendwhatmsg("+910123456789", "Hi", 13, 30)

# Same as above but Closes the Tab in 2 Seconds after Sending the Message
pywhatkit.sendwhatmsg("+910123456789", "Hi", 13, 30, 15, True, 2)

# Send an Image to a Group with the Caption as Hello
pywhatkit.sendwhats_image("AB123CDEFGHijklmn", "Images/Hello.png", "Hello")

# Send an Image to a Contact with the no Caption
pywhatkit.sendwhats_image("+910123456789", "Images/Hello.png")

# Send a WhatsApp Message to a Group at 12:00 AM
pywhatkit.sendwhatmsg_to_group("AB123CDEFGHijklmn", "Hey All!", 0, 0)

# Send a WhatsApp Message to a Group instantly
pywhatkit.sendwhatmsg_to_group_instantly("AB123CDEFGHijklmn", "Hey All!")
```


## 📺 Demo

![demo](https://user-images.githubusercontent.com/87910771/147886979-a12cd79a-8f49-4603-b568-4991dde28feb.jpg)



## 🤖 Author
<!--Remove the below lines and add yours -->
[AnishLohiya](https://github.com/AnishLohiya),
[Yurnero-cyber](https://github.com/Yurnero-cyber)
