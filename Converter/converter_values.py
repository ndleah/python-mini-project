#dict with help menu options
options = {
"symbols":'''
LENGTH : L ----------------------------------------------------------------
centimeter : cm
foot : ft
inch : in
kilometer : km
meter : m
micrometer ; um
mile : mi
millimeter : mm
nanometer : nm
nautical mile : nmi
yard : yd                      

AREA : A ----------------------------------------------------------------
acre : ac
hectare : ha
sq ft : ft2
sq inch : in2
sq km : km2
sq m : m2
sq mile : mi
sq yard : yd2

VOLUME : V ----------------------------------------------------------------
cubic cm : cm3
cubic foot : ft3
cubic inch : in3
cubic m : m3
litre: l
milliliter : ml

MASS : M ----------------------------------------------------------------
gram : g
kilogram : kg
milligram : mg
ounce : oz
pound : lb
quintal :  q
tonne : t

TIME : T ----------------------------------------------------------------
day : d
hour : hr
minute : min
second : sec
week : w
year : y

''',

"help":'''
Welcome To Converter!

Enter your calculation in the following format:
Unit category <space> Unit <space> Value <space> Units to be coverted to

Unit category : L for length, A for area etc...
Unit : m for meter, mi for mile etc...

Eg :L m 60 km,mi,yd
Eg :A ha 60 ac

Type   "symbols" for symbols of units
Type   "help"       for help
Type   "q"            to quit
'''
}



#convertion table dictionarys
L= {"m":1 ,
    "km":10**(-3) ,
    "cm":10**(2) ,
    "mm":10**(3)  ,
    "um":10**(6)  ,
    "nm":10**(9) ,
    "mi":0.000621 ,
    "ft":3.28084 ,
    "in":39.3701 ,
    "yd":1.09361 ,
    "nmi":0.0005399}

A= {"ha":10**(-4) ,
    "ac":0.000247 ,
    "km2":10**(-6) ,
    "m2":1,
    "mi2":3.86*(10**-7)  ,
    "ft2":10.7639 ,
    "in2":1550.0031 ,
    "yd2":1.19599 }

V= {"m3":1 ,
    "cm3":10**(6) ,
    "ml":10**(6) ,
    "l":10**(3)  ,
    "in3":61023.7441  ,
    "ft3":35.31467}

M= {"g":1 ,
    "kg":10**(-3) ,
    "mg":10**(3),
    "t":10**(-6) ,
    "q":10**(-5) ,
    "lb":0.0022046 ,
    "oz":0.03527}

T= {"y":0.0027397 ,
    "w":0.142857 ,
    "d":1 ,
    "hr":24  ,
    "min":1440  ,
    "sec":86400 }

