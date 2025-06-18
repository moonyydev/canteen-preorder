import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import tkinter as tk
import canteen_preorder.backend as backend
from canteen_preorder.backend import Category
from tkinter import messagebox, Frame
from tkinter import ttk

backend = backend.PreorderBackend()
window = tk.Tk()

window.geometry("500x500")
window.title("School Canteen Pre-Order System")
window.configure(bg = '#F1F0E9')

welcome_frame = tk.Frame(window, bg = '#F1F0E9')
login_frame = tk.Frame(window, bg = '#F1F0E9')
staff_frame = tk.Frame(window, bg = '#F1F0E9')
student_frame = tk.Frame(window, bg = '#F1F0E9')
crmeal_frame = tk.Frame(window, bg = '#F1F0E9')
updstock_frame = tk.Frame(window, bg = '#F1F0E9')
updcost_frame = tk.Frame(window, bg = '#F1F0E9')
updaval_frame = tk.Frame(window, bg = '#F1F0E9')



def show_frame(frame):
    welcome_frame.pack_forget()
    login_frame.pack_forget()
    staff_frame.pack_forget()
    student_frame.pack_forget()
    crmeal_frame.pack_forget()
    updstock_frame.pack_forget()
    updcost_frame.pack_forget()
    updaval_frame.pack_forget()
    frame.pack(fill='both', expand=True, padx=20, pady=20)



def login():
    
    email = username_entry.get()
    password = password_entry.get()

    print(f"Attempting login with: {email}")

    user = backend.login(email,password)
    if user:
        is_staff = getattr(user, 'staff', False)
        if is_staff:
            messagebox.showinfo(title="Login Status", message=f"Stuff login success! Welcome {user.name}")
            staff_interface()
        else:
            messagebox.showinfo(title="Login Status", message=f"Login success! Welcome {user.name}")
            student_interface()
    else:
        messagebox.showinfo(title="Login Status", message="Login failed. Invalid email or password.")



def sign_up():
    name = name_entry.get()
    email = username_entry.get()
    password = password_entry.get()

    if staff_entry.get() == 'Y':
        staff = True
    else:
        staff = False
      
    if not name or not email or not password:
        messagebox.showwarning("Missing info, plese fill out all fields")
    else:
        if staff == True:
            backend.create_user(name, email, password, staff)
            messagebox.showinfo(title="Sign Up Status", message="Staff account created successfully!")
            staff_interface()
        else:
            backend.create_user(name, email, password, staff)
            messagebox.showinfo(title="Sign Up Status", message="Student account created successfully!")
            student_interface()



def show_name():
    name_label.grid(row=1, column=0)
    name_entry.grid(row=1, column=1)
    staff_label.grid(row=4, column=0)
    staff_entry.grid(row=4, column=1)



def open_create_meal():
    global crmeal_frame, meal_name_entry, meal_cost_entry, meal_category_entry, meal_stock_entry, meal_availability_entry
    crmeal_frame.destroy()
    crmeal_frame = tk.Frame(window, bg='#F1F0E9')

    crmeal_label = tk.Label(crmeal_frame, text="Create Meal",font=('Arial', 20), bg='#F1F0E9', fg='#0D4715')
    back_button = tk.Button(crmeal_frame, text="Back to Main", font=('Arial', 14), bg = '#F1F0E9', fg = '#0D4715', command=staff_interface)
    add_button = tk.Button(crmeal_frame, text="ADD", font=('Arial', 14), bg = '#F1F0E9', fg = '#0D4715', command=handle_add_meal)


    meal_name_label = tk.Label(crmeal_frame, text = "Meal Name:", font = ('Arial', 20), bg = '#F1F0E9', fg = '#0D4715')
    meal_name_entry = tk.Entry(crmeal_frame, bg = '#F1F0E9', fg = '#0D4715')
    meal_cost_label = tk.Label(crmeal_frame, text = "Meal Cost:", font = ('Arial', 20), bg = '#F1F0E9', fg = '#0D4715')
    meal_cost_entry = tk.Entry(crmeal_frame, bg = '#F1F0E9', fg = '#0D4715')
    meal_category_label = tk.Label(crmeal_frame, text = "Meal Category:", font = ('Arial', 20), bg = '#F1F0E9', fg = '#0D4715')
    meal_category_entry = tk.Entry(crmeal_frame, bg = '#F1F0E9', fg = '#0D4715')
    meal_stock_label = tk.Label(crmeal_frame, text = "Meal Stock:", font = ('Arial', 20), bg = '#F1F0E9', fg = '#0D4715')
    meal_stock_entry = tk.Entry(crmeal_frame, bg = '#F1F0E9', fg = '#0D4715')
    meal_availability_label = tk.Label(crmeal_frame, text = "Meal Availability:", font = ('Arial', 20), bg = '#F1F0E9', fg = '#0D4715')
    meal_availability_entry = tk.Entry(crmeal_frame, bg = '#F1F0E9', fg = '#0D4715')

    back_button.pack(pady=10)
    crmeal_label.pack()
    meal_name_label.pack(pady=10)
    meal_name_entry.pack()
    meal_cost_label.pack(pady=10)
    meal_cost_entry.pack()
    meal_category_label.pack(pady=10)
    meal_category_entry.pack()
    meal_stock_label.pack(pady=10)
    meal_stock_entry.pack()
    meal_availability_label.pack(pady=10)
    meal_availability_entry.pack()
    add_button.pack(pady=10)

    show_frame(crmeal_frame)

def handle_add_meal():
    name = meal_name_entry.get()
    cost = int(float(meal_cost_entry.get())*100)
    category1 = meal_category_entry.get().upper()

    if category1 == "BREAKFAST":
        category = Category.BREAKFAST
    elif category1 == "LUNCH":
        category = Category.LUNCH
    elif category1 == "SNACK":
        category = Category.SNACK
    else:
        messagebox.showwarning(title="Invalid Input", message="Use BREAKFAST, LUNCH or SNACK")

    stock = int(meal_stock_entry.get())
    availability = bool(meal_availability_entry.get())

    added_meal = backend.create_meal(name, cost, category, stock, availability)
    staff_tree.insert("", "end", values=(added_meal.meal_id, added_meal.name, f"${added_meal.cost:.2f}", added_meal.category, added_meal.stock, added_meal.available))

    staff_interface()



def open_update_stock():
    global updstock_frame, id_entry, updstock_entry
    updstock_frame.destroy()
    updstock_frame = tk.Frame(window, bg='#F1F0E9')

    updstock_mlabel = tk.Label(updstock_frame, text="Update Meal Stock",font=('Arial', 20), bg='#F1F0E9', fg='#0D4715')
    back_button = tk.Button(updstock_frame, text="Back to Main", font=('Arial', 14), bg = '#F1F0E9', fg = '#0D4715', command=staff_interface)
    update_button = tk.Button(updstock_frame, text="Update", font=('Arial', 14), bg = '#F1F0E9', fg = '#0D4715', command=handle_update_meal) 

    id_label = tk.Label(updstock_frame, text = "Meal ID:", font = ('Arial', 20), bg = '#F1F0E9', fg = '#0D4715')
    id_entry = tk.Entry(updstock_frame, bg = '#F1F0E9', fg = '#0D4715')
    updstock_label = tk.Label(updstock_frame, text = "New Stock:", font = ('Arial', 20), bg = '#F1F0E9', fg = '#0D4715')
    updstock_entry = tk.Entry(updstock_frame, bg = '#F1F0E9', fg = '#0D4715')      

    back_button.pack(pady=10)
    updstock_mlabel.pack()
    id_label.pack(pady=10)
    id_entry.pack()
    updstock_label.pack(pady=10)
    updstock_entry.pack()
    update_button.pack(pady=10)

    show_frame(updstock_frame)

def handle_update_meal():
    stock = int(updstock_entry.get())
    meal_id = int(id_entry.get())

    backend.update_meal_stock(meal_id, stock)
    for item in staff_tree.get_children():
        values = staff_tree.item(item)['values']
        if values[0] == meal_id:
            staff_tree.item(item, values=(values[0], values[1], values[2], values[3], stock, values[5]))

    staff_interface()


def staff_interface():
    global staff_frame,staff_tree
    staff_frame.destroy()
    staff_frame = tk.Frame(window, bg='#F1F0E9')
    
    welcome_label = tk.Label(staff_frame, text="Staff Dashboard",font=('Arial', 20), bg='#F1F0E9', fg='#0D4715')
    welcome_label.pack(pady=20)
    back_button = tk.Button(staff_frame, text="Back to Login", font=('Arial', 14), bg = '#F1F0E9', fg = '#0D4715', command=lambda: show_frame(login_frame))
    back_button.pack(pady=10)

    staff_tree = ttk.Treeview(staff_frame, columns=("ID", "Name", "Cost", "Category" ,"Stock", "Availability"))
    
    staff_tree.heading('#0', text="")
    staff_tree.heading("ID", text="ID")
    staff_tree.heading("Name", text="Meal Name")
    staff_tree.heading("Cost", text="Price")
    staff_tree.heading("Category", text="Category")
    staff_tree.heading("Stock", text="Stock")
    staff_tree.heading("Availability", text="Available")

    staff_tree.column('#0', width=0, stretch=False)
    staff_tree.column("ID", width=50, anchor="center")
    staff_tree.column("Name", width=200, anchor="center")
    staff_tree.column("Cost", width=100, anchor="center")
    staff_tree.column("Category", width=100, anchor="center")
    staff_tree.column("Stock", width=50, anchor="center")
    staff_tree.column("Availability", width=100, anchor="center")

    staff_tree.pack(pady=10, fill='x')

    meals = backend.get_meals()
    for meal in meals:
        staff_tree.insert("", "end", values=(meal.meal_id, meal.name, f"${meal.cost/100:.2f}",meal.category.name, meal.stock, meal.available))

    
    create_meal = tk.Button(staff_frame, text="Create Meal", font=('Arial', 14), bg = '#F1F0E9', fg = '#0D4715', width=50, command=open_create_meal)
    create_meal.pack(pady=10)
    update_stock = tk.Button(staff_frame, text="Update Stock", font=('Arial', 14), bg = '#F1F0E9', fg = '#0D4715', width=50, command=open_update_stock)
    update_stock.pack(pady=10)
    update_cost = tk.Button(staff_frame, text="Update Cost", font=('Arial', 14), bg = '#F1F0E9', fg = '#0D4715', width=50)
    update_cost.pack(pady=10)
    update_availability = tk.Button(staff_frame, text="Update Availability", font=('Arial', 14), bg = '#F1F0E9', fg = '#0D4715', width=50)
    update_availability.pack(pady=10)


    show_frame(staff_frame)


def student_interface():
    global student_frame
    student_frame.destroy()
    student_frame = tk.Frame(window, bg='#F1F0E9')
    
    welcome_label = tk.Label(student_frame, text="Student Dashboard",font=('Arial', 20), bg='#F1F0E9', fg='#0D4715')
    welcome_label.pack(pady=20)
    back_button = tk.Button(student_frame, text="Back to Login", font=('Arial', 14),command=lambda: show_frame(login_frame))
    back_button.pack(pady=10)
    
    show_frame(student_frame)
    



login_label = tk.Label(login_frame, text = "Login screen", font = ('Arial', 30), bg = '#F1F0E9', fg = '#0D4715')
name_label = tk.Label(login_frame, text="Name:", font = ('Arial', 20), bg = '#F1F0E9', fg = '#0D4715')
name_entry = tk.Entry(login_frame, bg = '#F1F0E9', fg = '#0D4715')
username_label = tk.Label(login_frame, text = "Username:", font = ('Arial', 20), bg = '#F1F0E9', fg = '#0D4715')
username_entry = tk.Entry(login_frame, bg = '#F1F0E9', fg = '#0D4715')
password_label = tk.Label(login_frame, text = "Password:", font = ('Arial', 20), bg = '#F1F0E9', fg = '#0D4715')
password_entry = tk.Entry(login_frame, bg = '#F1F0E9', fg = '#0D4715')
staff_label = tk.Label(login_frame, text="Staff member?(Y/N)", font = ('Arial', 20), bg = '#F1F0E9', fg = '#0D4715')
staff_entry = tk.Entry(login_frame, bg = '#F1F0E9', fg = '#0D4715')
login_button = tk.Button(login_frame, text = "Login", font = ('Arial', 20), bg = '#F1F0E9', fg = '#0D4715', command=login)
signup_button = tk.Button(login_frame, text = "SignUp", font = ('Arial', 20), bg = '#F1F0E9', fg = '#0D4715', command=sign_up)
new_account_creation = tk.Button(login_frame, text="New user", font = ('Arial', 20), bg = '#F1F0E9', fg = '#0D4715', command=show_name)


login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
username_label.grid(row=2, column=0)
username_entry.grid(row=2, column=1, pady=10)
password_label.grid(row=3, column=0)
password_entry.grid(row=3, column=1, pady=10)
login_button.grid(row=5, column=0,)
new_account_creation.grid(row=5, column=2)
signup_button.grid(row=5, column=1)


show_frame(login_frame)
window.mainloop()
