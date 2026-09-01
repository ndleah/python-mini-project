import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

def generate_qr(content: str, save_name: str, target_dir: str = None) -> bool:
    """Generate QR code and save to target directory."""
    if not content:
        return False
    try:
        import qrcode
        qr = qrcode.make(str(content))
        if not target_dir:
            target_dir = os.getcwd()

        if not save_name.endswith('.png'):
            save_name = f"{save_name}.png"

        file_path = os.path.join(target_dir, save_name)
        qr.save(file_path)
        return True
    except Exception as e:
        print(f"Error generating QR code: {e}")
        return False

def run_gui():
    base = tk.Tk()
    base.geometry("420x220")
    base.title("QR Code Generator")
    base.resizable(False, False)

    data = tk.StringVar()
    name_to_save = tk.StringVar(value="my_qrcode")

    tk.Label(base, text="SAVE AS FILENAME:", font=("Arial", 10, "bold")).place(x=60, y=10)
    name_entry = tk.Entry(base, textvariable=name_to_save, width="35")
    name_entry.place(x=60, y=32)

    tk.Label(base, text="INSIDE QR CODE (URL / TEXT):", font=("Arial", 10, "bold")).place(x=60, y=60)
    data_entry = tk.Entry(base, textvariable=data, width="35")
    data_entry.place(x=60, y=82)
    data_entry.focus_set()

    status_label = tk.Label(base, text="", font=("Arial", 10, "bold"), fg="green")
    status_label.place(x=60, y=170)

    def get_code():
        data_var = data.get().strip()
        save_as = name_to_save.get().strip()

        if not data_var:
            messagebox.showwarning("Input Error", "Please enter content for the QR code.")
            return

        if not save_as:
            save_as = "qrcode"

        target_dir = filedialog.askdirectory(title="Select Output Directory")
        if not target_dir:
            return  # User cancelled directory selection

        if generate_qr(data_var, save_as, target_dir):
            status_label.configure(text=f"Saved successfully to: {target_dir}", fg="green")
            messagebox.showinfo("Success", f"QR Code saved to:\n{os.path.join(target_dir, save_as + '.png')}")
        else:
            status_label.configure(text="Error generating QR Code", fg="red")

    button = tk.Button(base, text="Generate QR Code", command=get_code, width="30", height="2", bg="navy", fg="white", font=("Arial", 10, "bold"))
    button.place(x=60, y=115)

    base.mainloop()

def main():
    run_gui()

if __name__ == '__main__':
    main()

