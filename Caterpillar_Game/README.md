![Star Badge](https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20Useful&style=style=flat&color=BC4E99)
![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)
[![View My Profile](https://img.shields.io/badge/View-My_Profile-green?logo=GitHub)](https://github.com/ndleah)
[![View Repositories](https://img.shields.io/badge/View-My_Repositories-blue?logo=GitHub)](https://github.com/ndleah?tab=repositories)

# Caterpillar
<p align="center">
<img src="https://static.wikia.nocookie.net/pixar/images/e/ec/Heimlich.png/revision/latest?cb=20170807224005" width=30% height=30%>

## 🛠️ Description

A simple Caterpillar game built in python.

## ⚙️ Languages or Frameworks Used
```bash
pip install turtle
```

## 🌟 How to run
Running the script is really simple! Just open a terminal in the folder where your script is located and run the following command:

```sh
python Caterpillar.py
```
## How to run as a docker file. For Ubuntu machine.
### Steps:
1. Connect to the server with X11 forwarding:
```bash
ssh -X <username>@<hostname>
```

2. Allow X11 access:
```bash
xhost +local:docker
```

3. Build the Docker image:
```bash
docker build -t caterpillar-game .
```

4. Run the container:
```bash
docker run --network host \
  -e DISPLAY=localhost:10.0 \
  -e XAUTHORITY=/home/$USER/.Xauthority \
  -v /home/$USER/.Xauthority:/home/$USER/.Xauthority \
  caterpillar-game
```

## 📺 Demo
<p align="center">
<img src="https://github.com/ndleah/python-mini-project/blob/main/IMG/caterpillar.gif" width=70% height=70%>

## 🤖 Author
[Leah Nguyen](https://github.com/ndleah)
