import tkinter as tk
from tkinter import ttk, messagebox
import requests

def get_exchange_rate(base, target):
	try:
		url = f"https://api.exchangerate.host/latest?base={base}&symbols={target}"
		response = requests.get(url, timeout=5)
		response.raise_for_status()
		data = response.json()
		return data['rates'][target]
	except Exception as e1:
		try:
			url = f"https://open.er-api.com/v6/latest/{base}"
			response = requests.get(url, timeout=5)
			response.raise_for_status()
			data = response.json()
			return data['rates'][target]
		except Exception as e2:
			messagebox.showerror(
				"API Error",
				f"Both API attempts failed.\n\nError 1: {e1}\n\nError 2: {e2}"
			)
			return None

def convert_currency():
	try:
		amount = float(entry_amount.get())
		if (amount < 0):
			messagebox.showerror("Input Error", "Please enter a positive numeric amount.")
			return
		from_currency = combo_from.get()
		to_currency = combo_to.get()

		if from_currency == to_currency:
			label_result.config(text=f"{amount:.2f} {from_currency} = {amount:.2f} {to_currency}")
			return

		rate = get_exchange_rate(from_currency, to_currency)
		if rate:
			converted = amount * rate
			label_result.config(text=f"{amount:.2f} {from_currency} = {converted:.2f} {to_currency}")
	except ValueError:
		messagebox.showerror("Input Error", "Please enter a valid numeric amount.")

root = tk.Tk()
root.title("Real-Time Currency Converter")
root.geometry("400x270")
root.resizable(False, False)

tk.Label(root, text="Amount:").pack()
entry_amount = tk.Entry(root)
entry_amount.pack()

tk.Label(root, text="From Currency:").pack(pady=5)
combo_from = ttk.Combobox(root, values=["USD", "EUR", "GBP", "JPY", "AMD", "RUB", "CNY"], state="readonly")
combo_from.set("USD")
combo_from.pack()

tk.Label(root, text="To Currency:").pack(pady=5)
combo_to = ttk.Combobox(root, values=["USD", "EUR", "GBP", "JPY", "AMD", "RUB", "CNY"], state="readonly")
combo_to.set("EUR")
combo_to.pack()

tk.Button(root, text="Convert", command=convert_currency, bg="crimson").pack(pady=20)

label_result = tk.Label(root, text="", font=("Arial", 12))
label_result.pack()

root.mainloop()
