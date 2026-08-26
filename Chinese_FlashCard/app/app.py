import tkinter as tk

class MainApp(tk.Tk):
    def __init__(self, keys_list, dictionary):
        super().__init__()
        self.geometry("480x380")
        self.title("Chinese Flashcards")
        self.configure(bg="#C2FCEE")
        self.resizable(False, False)
        self.scrollbar = tk.Scrollbar(orient='vertical', relief='groove')
        self.keyslist = keys_list
        self.dictionary = dictionary
        self.selected_key = None
        self.setup()

    def setup(self):
        self.widgets()
        self.layouts()
        if self.keyslist:
            self.lists.selection_set(0)
            self.show_keys(None)

    def widgets(self):
        self.lists = tk.Listbox(bg='#83FCE3', border=1, width=12, height=14, yscrollcommand=self.scrollbar.set)
        for n, line in enumerate(self.keyslist):
            self.lists.insert(n, line)
        self.lists.bind("<<ListboxSelect>>", self.show_keys)
        self.scrollbar.config(command=self.lists.yview)

        self.canvas = tk.Canvas(bg='#83FCE3', border=1, width=200, height=200, relief='groove')
        self.quit_btn = tk.Button(cursor='hand2', bg="#C2FCEE", text='Quit', command=self.quit)

        self.frame = tk.Frame(bg="#C2FCEE")

        self.btn1 = tk.Button(self.frame, cursor='hand2', bg="#C2FCEE", text='Pinyin', command=self.show_pinyin)
        self.btn2 = tk.Button(self.frame, cursor='hand2', bg="#C2FCEE", text='Role', command=self.show_role)
        self.btn3 = tk.Button(self.frame, cursor='hand2', bg="#C2FCEE", text='Definition', command=self.show_definition)

        self.label1 = tk.Label(self.frame, bg="#C2FCEE", text='', font=('Roboto', '12', 'bold'))
        self.label2 = tk.Label(self.frame, bg="#C2FCEE", text='', font=('Roboto', '12', 'bold'))
        self.label3 = tk.Label(self.frame, bg="#C2FCEE", text='', font=('Roboto', '12', 'bold'), wraplength=180, justify='left')

    def layouts(self):
        self.lists.grid(column=0, row=0, padx=10, pady=10, sticky='NS')
        self.scrollbar.grid(column=1, row=0, sticky="NS", pady=10)
        self.canvas.grid(column=2, row=0, padx=10, pady=10, columnspan=2, sticky='N')
        self.quit_btn.grid(column=0, row=1, pady=10, padx=10)
        self.frame.grid(column=2, row=1, columnspan=2, padx=10, sticky='NW')

        self.btn1.grid(column=0, row=0, pady=4, padx=4, sticky='W')
        self.label1.grid(column=1, row=0, pady=4, padx=8, sticky='W')

        self.btn2.grid(column=0, row=1, pady=4, padx=4, sticky='W')
        self.label2.grid(column=1, row=1, pady=4, padx=8, sticky='W')

        self.btn3.grid(column=0, row=2, pady=4, padx=4, sticky='W')
        self.label3.grid(column=1, row=2, pady=4, padx=8, sticky='W')

    def show_keys(self, event):
        select_id = self.lists.curselection()
        if not select_id:
            return
        self.selected_key = self.lists.get(select_id[0])
        self.canvas.delete('all')
        self.canvas.create_text(100, 100, text=self.selected_key, font=('Roboto', '45'))
        self.label1['text'] = ''
        self.label2['text'] = ''
        self.label3['text'] = ''

    def show_pinyin(self):
        if self.selected_key and self.selected_key in self.dictionary:
            self.label1['text'] = self.dictionary[self.selected_key][0]

    def show_role(self):
        if self.selected_key and self.selected_key in self.dictionary:
            self.label2['text'] = self.dictionary[self.selected_key][1]

    def show_definition(self):
        if self.selected_key and self.selected_key in self.dictionary:
            self.label3['text'] = self.dictionary[self.selected_key][2]