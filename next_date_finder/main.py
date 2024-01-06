date=input("Enter DD/MM/YYYY: ").split('/')
d=int(date[0])
m=int(date[1])
y=int(date[2])
er=0

def leapyr(y):
    if(y%4==0 and (y%100!=0 or y%400==0)):
        return True
    return False

if(m==1 or m==3 or m==5 or m==7 or m==8 or m==10 or m==12):
    if(d<31):
        d+=1
    if(d==31 and m!=12):
        d=1
        m+=1
    if(d==31 and m==12):
        d=1
        m=1
        y+=1
    if(d>31):
        er=1
elif(m==4 or m==6 or m==9 or m==11):
    if(d<30):
        d+=1
    if(d==30):
        d=1
        m+=1
    if(d>30):
        er=1
elif(m==2):
    if(leapyr(y)):
        if(d==29):
            m+=1
            d=1
        if(d<29):
            d+=1
        if(d>29):
            er=1
    else:
        if(d==28):
            m+=1
            d=1
        if(d<28):
            d+=1
        if(d>28):
            er=1
else:
    er=1

if(er==1):
    print("INVALID INPUT")
else:
    print("The next date is {}/{}/{}".format(d,m,y))