from tkinter import *


root = Tk()
root.configure(bg="black")
root.title("Weights in different planet")

mylabel=Label(root,text="Enter Weight in earth: ",font=("Algerian",12),bg="black",fg="red")
e=Entry(root,width=50,borderwidth=15)
mylabel.grid(row=0 ,column=0, columnspan=1)
e.grid(row=0, column=1, columnspan=2)
e.get()

def myclickmerc():
    weight_merc = round((int(e.get()) / 9.798) * 3.7, 2)
    mylabel1 = Label(root, text="Your Weight In Mercury: " + str(weight_merc), padx=20, pady=20)
    mylabel1.grid(row=5, column=0, columnspan=3)

def myclickven():
    weight_ven = round((int(e.get()) / 9.798) * 8.87, 2)
    mylabel2 = Label(root, text="Your Weight In Venus: " + str(weight_ven), padx=20, pady=20)
    mylabel2.grid(row=5, column=0, columnspan=3)

def myclickmars():
    weight_mars = round((int(e.get()) / 9.798) * 3.71, 2)
    mylabel3 = Label(root, text="Your Weight In Mars: " + str(weight_mars), padx=20, pady=20)
    mylabel3.grid(row=5, column=0, columnspan=3)

def myclickjupi():
    weight_jupi = round((int(e.get()) / 9.798) * 24.92, 2)
    mylabel4 = Label(root, text="Your Weight In Jupiter: " + str(weight_jupi), padx=20, pady=20)
    mylabel4.grid(row=5, column=0, columnspan=3)

def myclicksat():
    weight_sat = round((int(e.get()) / 9.798) * 10.44, 2)
    mylabel5 = Label(root, text="Your Weight In Saturn: " + str(weight_sat), padx=20, pady=20)
    mylabel5.grid(row=5, column=0, columnspan=3)

def myclickuran():
    weight_uran = round((int(e.get()) / 9.798) * 8.87, 2)
    mylabel6 = Label(root, text="Your Weight In Uranus: " + str(weight_uran), padx=20, pady=20)
    mylabel6.grid(row=5, column=0, columnspan=3)

def myclicknept():
    weight_nept = round((int(e.get()) / 9.798) * 11.15, 2)
    mylabel7 = Label(root, text="Your Weight In Neptune: " + str(weight_nept), padx=20, pady=20)
    mylabel7.grid(row=5, column=0, columnspan=3)

def myclickplut():
    weight_plut = round((int(e.get()) / 9.798) * 0.58, 2)
    mylabel8 = Label(root, text="Your Weight In Pluto: " + str(weight_plut), padx=20, pady=20)
    mylabel8.grid(row=5, column=0, columnspan=3)

def myclicksun():
    weight_sun = round((int(e.get()) / 9.798) * 274, 2)
    mylabel9 = Label(root, text="Your Weight In Sun: " + str(weight_sun), padx=20, pady=20)
    mylabel9.grid(row=5, column=0, columnspan=3)

def myclickmoon():
    weight_moon = round((int(e.get()) / 9.798) * 1.625, 2)
    mylabel9 = Label(root, text="Your Weight In Moon: " + str(weight_moon), padx=20, pady=20)
    mylabel9.grid(row=5, column=0, columnspan=3)




mybutton1= Button(root,text="Mercury",font=("arial", 12),padx=70,pady=25,command=myclickmerc,bg="green",fg="white")
mybutton2= Button(root,text="Venus",font=("arial", 12),padx=81,pady=25,command=myclickven,bg="blue",fg="white")
mybutton3= Button(root,text="Mars",font=("arial", 12),padx=75,pady=25,command=myclickmars,bg="red",fg="white")
mybutton4= Button(root,text="Jupiter",font=("arial", 12),padx=75,pady=25,command=myclickjupi,bg="green",fg="white")
mybutton5= Button(root,text="Saturn",font=("arial", 12),padx=80,pady=25,command=myclicksat,bg="blue",fg="white")
mybutton6= Button(root,text="Uranus",font=("arial", 12),padx=70,pady=25,command=myclickuran,bg="red",fg="white")
mybutton7= Button(root,text="Neptune",font=("arial", 12),padx=70,pady=25,command=myclicknept,bg="green",fg="white")
mybutton8= Button(root,text="Pluto",font=("arial", 12),padx=85,pady=25,command=myclickplut,bg="blue",fg="white")
mybutton9= Button(root,text="Sun",font=("arial", 12),padx=80,pady=25,command=myclicksun,bg="red",fg="white")
mybutton10= Button(root,text="Moon",font=("arial", 12),padx=80,pady=25,command=myclickmoon,bg="yellow",fg="blue")
mybutton1.grid(row=1 ,column=0)
mybutton2.grid(row=1 ,column=1)
mybutton3.grid(row=1,column=2)
mybutton4.grid(row=2 ,column=0)
mybutton5.grid(row=2 ,column=1)
mybutton6.grid(row=2 ,column=2)
mybutton7.grid(row=3 ,column=0)
mybutton8.grid(row=3 ,column=1)
mybutton9.grid(row=3 ,column=2)
mybutton10.grid(row=4 ,column=1)




root.mainloop()