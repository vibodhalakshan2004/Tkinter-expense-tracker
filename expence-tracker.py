import tkinter as tk
from tkinter import ttk, messagebox
import json


#Creat a Window
root=tk.Tk()
root.title('Personal Expense Tracker')
root.geometry('700x500')
root.resizable(False,False)

#ttk style
style = ttk.Style()
style.theme_use("vista")


#Create Labels
ttk.Label(root,text='Category').grid(row=0,column=0,padx=10,pady=10)
ttk.Label(root,text='Amount').grid(row=1,column=0,padx=10,pady=10)
ttk.Label(root,text='Date').grid(row=2,column=0,padx=10,pady=10)

#Create Category Combobox
category=ttk.Combobox(root,values=["Food", "Transport", "Utilities", "Entertainment"])
category.grid(row=0,column=1,padx=10,pady=10)
category.current(0)

#Create Entries 
amount=ttk.Entry(root)
amount.grid(row=1,column=1,padx=10,pady=10)

date=ttk.Entry(root)
date.grid(row=2,column=1,padx=10,pady=10)

#Create Expence Table
tree=ttk.Treeview(root,columns=('Category','Amount','Date'),show='headings')
tree.heading("Category", text="Category")
tree.heading("Amount", text="Amount")
tree.heading("Date", text="Date")
tree.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

#Add vertical scrollbar for table
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=4, column=3, sticky="ns")


expense_list=[]
total=0
count=0
#Add Expenses Funtion
def add_expenses():
    global total,count

    cat=category.get()
    amt=amount.get()
    dt=date.get()

    if not (amt and dt):
        messagebox.showwarning("Input Error", "Please enter all fields")
        return
    
    try:
        amt = float(amt)
    except:
        messagebox.showwarning("Input Error", "Amount must be a number")
        return
    
    total+=amt
    count+=1

    expense = {"category": cat, "amount": amt, "date": dt}
    expense_list.append(expense)
    tree.insert("", index="end", values=(cat, amt, dt))
    Total_expenses.configure(text=f'Total Amount = {total}')
    No_of_expenses.configure(text=f'No of Expenses = {count}')

    amount.delete(0, tk.END)
    date.delete(0, tk.END)
    category.current(0)
    

#Create save expenses funtion

def save_expenses():
    with open("expenses.json", "w") as f:
        json.dump(expense_list, f)
    messagebox.showinfo("Saved", "Expenses saved successfully!")

    amount.delete(0, tk.END)
    date.delete(0, tk.END)
    category.current(0)
    
#Create load expenses funtion
def load_expenses():
    global expense_list
    try:
        with open("expenses.json", "r") as f:
            expense_list = json.load(f)
        for item in tree.get_children():
            tree.delete(item)
        for exp in expense_list:
            tree.insert("", "end", values=(exp["category"], exp["amount"], exp["date"]))
    except FileNotFoundError:
        messagebox.showinfo("No file", "No saved expenses found.")

    amount.delete(0, tk.END)
    date.delete(0, tk.END)
    category.current(0)
    

#Buttons

ttk.Button(root,text='Add Expense',command=add_expenses).grid(row=3 ,column=0,padx=10,pady=10)
ttk.Button(root,text='Save Expense',command=save_expenses).grid(row=3 ,column=1,padx=10,pady=10)
ttk.Button(root,text='Load Expense',command=load_expenses).grid(row=3 ,column=2,padx=10,pady=10)

#Labels

No_of_expenses=ttk.Label(root,text='No. of Expenses = 0')
No_of_expenses.grid(row=5,column=0,pady=10)

Total_expenses=ttk.Label(root,text='Total Amount = 0')
Total_expenses.grid(row=5,column=1,pady=10)

root.mainloop()
