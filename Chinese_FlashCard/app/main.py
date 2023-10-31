from random import shuffle
from app import MainApp
from models import create_dictionary

def main():
    dct = create_dictionary()
    keyslist = list(dct.keys())
    shuffle(keyslist)
    app = MainApp(keyslist,dct)
    app.mainloop()

if __name__ == "__main__":
    main()