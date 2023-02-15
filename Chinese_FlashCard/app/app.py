import tkinter as tk

class MainApp(tk.Tk):
    def __init__(self,keys_list,dictionary):
        super().__init__()
        self.geometry("350x350")
        self.title("@MyApp")
        self.configure(bg="#C2FCEE")
        self.resizable(False,False)
        self.scrollbar = tk.Scrollbar(orient='vertical',relief='groove')
        self.keyslist = keys_list
        self.dictionary = dictionary
        self.setup()

    def setup(self):
        self.widgets()
        self.layouts()
        self.show_keys(select_id=self.lists)

    def widgets(self):
        self.lists = tk.Listbox(bg='#83FCE3',border=1,width=8,height=12,yscrollcommand=self.scrollbar.set)
        for n,line in enumerate(self.keyslist):
            self.lists.insert(n,line)
        self.lists.bind("<<ListboxSelect>>",self.show_keys)
        self.scrollbar.config(command = self.lists.yview)

        self.canvas = tk.Canvas(bg='#83FCE3',border=1,width=190,height=190,relief='groove')
        
        self.quit_btn = tk.Button(cursor='target',bg="#C2FCEE",text='quit',command=self.quit)
        
        # create a frame to align with the canvas widget
        self.frame = tk.Frame(bg="#C2FCEE",width=180,height=180)

        self.btn1 = tk.Button(self.frame,cursor='target',bg="#C2FCEE",text='Pinyin',command=self.show_pinyin)
        self.btn2 = tk.Button(self.frame,cursor='target',bg="#C2FCEE",text='Role',command=self.show_role)
        self.btn3 = tk.Button(self.frame,cursor='target',bg="#C2FCEE",text='Definition',command=self.show_definition)
        
        self.label1 = tk.Label(self.frame,bg="#C2FCEE",text='',font=('Roboto','15'))
        self.label2 = tk.Label(self.frame,bg="#C2FCEE",text='',font=('Roboto','15'))
        self.label3 = tk.Label(self.frame,bg="#C2FCEE",text='',font=('Roboto','15'))

    def layouts(self):

        self.lists.grid(column=0,row=0,padx=15,pady=8)
        self.scrollbar.grid(column=1,row=0,sticky="NS",pady=10)
        self.canvas.grid(column=2,row=0,padx=15,pady=15,sticky='N')
        self.quit_btn.grid(columnspan=1,row=1,pady=5,sticky='S')
        self.frame.grid(column=2,row=1)
        self.btn1.grid(column=2,row=1,pady=5,padx=5,ipadx=10)
        self.btn2.grid(column=2,row=2,pady=5,padx=1,ipadx=14)
        self.btn3.grid(column=2,row=3,pady=5,padx=5,ipadx=4)
        self.label1.grid(column=3,row=1,pady=5,padx=20)
        self.label2.grid(column=3,row=2,pady=5,padx=20)
        self.label3.grid(column=3,row=3,pady=5,padx=20)

    def show_keys(self,select_id):
        global select_keys
        # get the indices from our sinographs list
        select_id = self.lists.curselection()
        keyslists = self.lists
        # get selected items
        select_keys = ",".join(keyslists.get(i) for i in select_id)
        # delete the previous sinograph
        self.canvas.delete('all')
        # create a new sinograph
        self.canvas.create_text(100,100,text=select_keys,font=('Roboto','45'))

    def show_pinyin(self):
        self.label1['text'] = self.dictionary[select_keys][0]
    
    def show_role(self):
        self.label2['text'] = self.dictionary[select_keys][1]
    
    def show_definition(self):
        self.label3['text'] = self.dictionary[select_keys][2]