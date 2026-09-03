import math
import sys
import tkinter as tk
from tkinter import messagebox

try:
    import customtkinter as ctk
    ctk.set_appearance_mode("bright")
    ctk.set_default_color_theme("blue")
    BaseAppClass = ctk.CTk
except Exception:
    BaseAppClass = tk.Tk

def calculate_sip(amt: float, tenure_years: int, rate_pct: float) -> tuple:
    """Calculate SIP Maturity value M and total invested N."""
    P = amt
    i = (rate_pct / 100.0) / 12.0
    n = tenure_years * 12

    if i > 0:
        M = int(P * ((pow((1 + i), n) - 1) / i) * (1 + i))
    else:
        M = int(P * n)
    N = int(amt * n)
    return M, N

def calculate_lumpsum(amt: float, tenure_years: int, rate_pct: float) -> tuple:
    """Calculate Lump-sum Maturity value M and invested P."""
    P = int(amt)
    rate = rate_pct / 100.0
    M = math.ceil(P * pow(1 + rate, tenure_years))
    return M, P

class App(BaseAppClass):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("SIP / Investment Calculator")
        self.geometry('360x620')
        self.Details = None

        def dispPie(M, N):
            try:
                import matplotlib.pyplot as plt
                import numpy as np

                names = ['Invested Amount\n(' + str(format(N, ',d')) + ')', 'Maturity Value\n(' + str(format(M, ',d')) + ')']
                pi = np.array([N, max(0, M - N)])
                fig, ax = plt.subplots(figsize=(5, 5))
                ax.pie(pi, labels=names, autopct='%1.1f%%', colors=['#3498DB', '#2ECC71'])
                plt.title("Investment Breakdown")
                plt.tight_layout()
                plt.show(block=False)
            except Exception as e:
                messagebox.showinfo("Breakdown Details", f"Invested Amount: {N:,}\nMaturity Value: {M:,}")

        def Display(M, N):
            self.MatDisp.configure(text=str(format(M, ',d')))
            self.AmtDisp.configure(text=str(format(N, ',d')))

            if hasattr(self, 'Details') and self.Details:
                try:
                    self.Details.destroy()
                except Exception:
                    pass

            if hasattr(ctk, 'CTkButton'):
                self.Details = ctk.CTkButton(self, text='Details Chart 📊', fg_color='#E74C3C', border_color='#E74C3C', command=lambda: dispPie(M, N))
            else:
                self.Details = tk.Button(self, text='Details Chart 📊', bg='#E74C3C', fg='white', command=lambda: dispPie(M, N))
            self.Details.grid(row=6, column=0, padx=20, pady=10, sticky='ew')

        def pressedCalculate():
            ten_str = self.ten.get().strip() if hasattr(self.ten, 'get') else ""
            if not ten_str:
                messagebox.showerror('Error', 'Please select or enter tenure in years.')
                return
            try:
                tenure = int(ten_str)
                if tenure <= 0:
                    messagebox.showerror('Error', 'Tenure must be greater than zero.')
                    return
            except ValueError:
                messagebox.showerror('Error', 'Tenure must be a valid whole integer number.')
                return

            roi_str = self.roi.get().strip().replace('%', '') if hasattr(self.roi, 'get') else ""
            if not roi_str:
                messagebox.showerror('Error', 'Please enter Expected Rate of Return (%)')
                return
            try:
                rate = float(roi_str)
                if rate <= 0 or rate > 100:
                    messagebox.showerror('Error', 'Rate of Return must be between 0% and 100%.')
                    return
            except ValueError:
                messagebox.showerror('Error', 'Only numeric Rate of Return values allowed.')
                return

            sip_str = self.Amt.get().strip().replace(',', '') if hasattr(self.Amt, 'get') else ""
            lump_str = self.ls.get().strip().replace(',', '') if hasattr(self.ls, 'get') else ""

            if not sip_str and not lump_str:
                messagebox.showerror('Error', 'Please enter either SIP Amount or Lump-sum Amount.')
                return
            if sip_str and lump_str:
                messagebox.showerror('Error', 'Please calculate either Lump-sum or SIP, not both at the same time.')
                return

            if sip_str:
                try:
                    amt = float(sip_str)
                    M, N = calculate_sip(amt, tenure, rate)
                    Display(M, N)
                except ValueError:
                    messagebox.showerror('Error', 'Invalid numeric format for SIP Amount.')
            elif lump_str:
                try:
                    amt = float(lump_str)
                    M, P = calculate_lumpsum(amt, tenure, rate)
                    Display(M, P)
                except ValueError:
                    messagebox.showerror('Error', 'Invalid numeric format for Lump-sum Amount.')

        def pressedReset():
            if hasattr(self.Amt, 'delete'):
                self.Amt.delete(0, 'end')
            if hasattr(self.ls, 'delete'):
                self.ls.delete(0, 'end')
            if hasattr(self.roi, 'delete'):
                self.roi.delete(0, 'end')
            self.MatDisp.configure(text="")
            self.AmtDisp.configure(text="")
            if hasattr(self, 'Details') and self.Details:
                try:
                    self.Details.destroy()
                    self.Details = None
                except Exception:
                    pass

        # Build UI layout
        if hasattr(ctk, 'CTkFrame'):
            self.InputFrame = ctk.CTkFrame(master=self, fg_color='#F5B7B1')
            self.InputFrame.grid(row=0, column=0, sticky='ew')

            self.SIPamt = ctk.CTkLabel(master=self.InputFrame, text='SIP Amount  ')
            self.SIPamt.grid(row=0, column=0, padx=20, pady=10, sticky='ew')

            self.Amt = ctk.CTkEntry(master=self.InputFrame, placeholder_text='2000', border_color="#E74C3C")
            self.Amt.grid(row=0, column=1, padx=20, pady=10, sticky='ew')

            self.Tenure = ctk.CTkLabel(master=self.InputFrame, text="Tenure (in years) ")
            self.Tenure.grid(row=1, column=0, padx=20, pady=10, sticky='ew')

            self.ten = ctk.CTkComboBox(master=self.InputFrame, values=['5', '10', '15', '20', '25', '30', '35'], border_color="#E74C3C", button_color="#E74C3C")
            self.ten.grid(row=1, column=1, padx=20, pady=10, sticky='ew')

            self.ror = ctk.CTkLabel(master=self.InputFrame, text='Rate of Return (%) ')
            self.ror.grid(row=2, column=0, padx=20, pady=10, sticky='ew')

            self.roi = ctk.CTkEntry(master=self.InputFrame, placeholder_text='12%', border_color="#E74C3C")
            self.roi.grid(row=2, column=1, padx=20, pady=10, sticky='ew')

            self.lumpSum = ctk.CTkLabel(master=self.InputFrame, text='Lump-sum Amount  ')
            self.lumpSum.grid(row=3, column=0, padx=20, pady=10, sticky='ew')

            self.ls = ctk.CTkEntry(master=self.InputFrame, placeholder_text='100000', border_color="#E74C3C")
            self.ls.grid(row=3, column=1, padx=20, pady=10, sticky='ew')

            self.Output = ctk.CTkFrame(master=self, fg_color='#E74C3C')
            self.Output.grid(row=1, column=0, sticky='ew')

            self.InvAmt = ctk.CTkLabel(master=self.Output, text="Invested Amount")
            self.InvAmt.grid(row=5, column=0, padx=20, pady=10, sticky='ew')

            self.AmtDisp = ctk.CTkLabel(master=self.Output, text='')
            self.AmtDisp.grid(row=5, column=1, padx=20, pady=10, sticky='ew')

            self.MatVal = ctk.CTkLabel(master=self.Output, text='Maturity Value   ')
            self.MatVal.grid(row=6, column=0, padx=10, pady=10, sticky='ew')

            self.MatDisp = ctk.CTkLabel(master=self.Output, text='')
            self.MatDisp.grid(row=6, column=1, padx=20, pady=10, sticky='ew')

            self.Calculate = ctk.CTkButton(self, text="Calculate", fg_color="#E74C3C", border_color="black", command=pressedCalculate)
            self.Calculate.grid(row=4, column=0, padx=20, pady=10, sticky='ew')

            self.Reset = ctk.CTkButton(self, text="Reset", fg_color="#E74C3C", border_color="black", command=pressedReset)
            self.Reset.grid(row=5, column=0, padx=20, pady=10, sticky='ew')

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()