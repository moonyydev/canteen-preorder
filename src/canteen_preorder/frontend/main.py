import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import tkinter as tk
import canteen_preorder.backend as backend
from canteen_preorder.backend import Category, NotFoundError, ConstraintError, Cost
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
crorder_frame = tk.Frame(window, bg = '#F1F0E9')
vieworders_frame = tk.Frame(window, bg = '#F1F0E9')



def show_frame(frame):
    welcome_frame.pack_forget()
    login_frame.pack_forget()
    staff_frame.pack_forget()
    student_frame.pack_forget()
    crmeal_frame.pack_forget()
    updstock_frame.pack_forget()
    updcost_frame.pack_forget()
    updaval_frame.pack_forget()
    crorder_frame.pack_forget()
    vieworders_frame.pack_forget()
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



#Creating mew meal
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

    availability_str = meal_availability_entry.get().lower()

    if availability_str in ["true", "yes", "1"]:
        availability = True
    elif availability_str in ["false", "no", "0"]:
        availability = False
    else:
        messagebox.showwarning(title="Invalid Availability",message= "Enter true/false, yes/no or 1/0")
        
    stock = int(meal_stock_entry.get())
    

    added_meal = backend.create_meal(name, cost, category, stock, availability)
    staff_tree.insert("", "end", values=(added_meal.meal_id, added_meal.name, f"${added_meal.cost:.2f}", added_meal.category, added_meal.stock, added_meal.available))

    staff_interface()



#Updating meal stock
def open_update_stock():
    global updstock_frame, id_entry, updstock_entry
    updstock_frame.destroy()
    updstock_frame = tk.Frame(window, bg='#F1F0E9')

    updstock_mlabel = tk.Label(updstock_frame, text="Update Meal Stock",font=('Arial', 20), bg='#F1F0E9', fg='#0D4715')
    back_button = tk.Button(updstock_frame, text="Back to Main", font=('Arial', 14), bg = '#F1F0E9', fg = '#0D4715', command=staff_interface)
    update_button = tk.Button(updstock_frame, text="Update Stock", font=('Arial', 14), bg = '#F1F0E9', fg = '#0D4715', command=handle_update_stock) 

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

def handle_update_stock():
    try:
      stock = int(updstock_entry.get())
      meal_id = int(id_entry.get())

      backend.update_meal_stock(meal_id, stock)
      for item in staff_tree.get_children():
          values = staff_tree.item(item)['values']
          if values[0] == meal_id:
              staff_tree.item(item, values=(values[0], values[1], values[2], values[3], stock, values[5]))

      staff_interface()

    except NotFoundError:
        messagebox.showwarning(title="Update Error", message="There is no meal with such ID!")
    except ConstraintError:
        messagebox.showwarning(title="Invalid Stock", message="Stock cannot be negative!")



#Updating meal cost
def open_update_cost():
    global updcost_frame, id_entry, updcost_entry
    updcost_frame.destroy()
    updcost_frame = tk.Frame(window, bg='#F1F0E9')

    updcost_mlabel = tk.Label(updcost_frame, text="Update Meal Cost",font=('Arial', 20), bg='#F1F0E9', fg='#0D4715')
    back_button = tk.Button(updcost_frame, text="Back to Main", font=('Arial', 14), bg = '#F1F0E9', fg = '#0D4715', command=staff_interface)
    update_button = tk.Button(updcost_frame, text="Update Cost", font=('Arial', 14), bg = '#F1F0E9', fg = '#0D4715', command=handle_update_cost) 

    id_label = tk.Label(updcost_frame, text = "Meal ID:", font = ('Arial', 20), bg = '#F1F0E9', fg = '#0D4715')
    id_entry = tk.Entry(updcost_frame, bg = '#F1F0E9', fg = '#0D4715')
    updcost_label = tk.Label(updcost_frame, text = "New Cost:", font = ('Arial', 20), bg = '#F1F0E9', fg = '#0D4715')
    updcost_entry = tk.Entry(updcost_frame, bg = '#F1F0E9', fg = '#0D4715')      

    back_button.pack(pady=10)
    updcost_mlabel.pack()
    id_label.pack(pady=10)
    id_entry.pack()
    updcost_label.pack(pady=10)
    updcost_entry.pack()
    update_button.pack(pady=10)

    show_frame(updcost_frame)

def handle_update_cost():
    try:
      cost = int(float(updcost_entry.get())*100)
      meal_id = int(id_entry.get())

      backend.update_meal_cost(meal_id, cost)
      for item in staff_tree.get_children():
          values = staff_tree.item(item)['values']
          if values[0] == meal_id:
              staff_tree.item(item, values=(values[0], values[1], f"${cost:.2f}", values[3], values[4], values[5]))

      staff_interface()

    except NotFoundError:
        messagebox.showwarning(title="Update Error", message="There is no meal with such ID!")
    except ConstraintError:
        messagebox.showwarning(title="Invalid Cost", message="Cost cannot be negative!")



#Updating meal availability
def open_update_availability():
    global updaval_frame, id_entry, updaval_entry
    updaval_frame.destroy()
    updaval_frame = tk.Frame(window, bg='#F1F0E9')

    updaval_mlabel = tk.Label(updaval_frame, text="Update Meal Availability",font=('Arial', 20), bg='#F1F0E9', fg='#0D4715')
    back_button = tk.Button(updaval_frame, text="Back to Main", font=('Arial', 14), bg = '#F1F0E9', fg = '#0D4715', command=staff_interface)
    updaval_button = tk.Button(updaval_frame, text="Update Availability", font=('Arial', 14), bg = '#F1F0E9', fg = '#0D4715', command=handle_update_aval) 

    id_label = tk.Label(updaval_frame, text = "Meal ID:", font = ('Arial', 20), bg = '#F1F0E9', fg = '#0D4715')
    id_entry = tk.Entry(updaval_frame, bg = '#F1F0E9', fg = '#0D4715')
    updaval_label = tk.Label(updaval_frame, text = "New Availability:", font = ('Arial', 20), bg = '#F1F0E9', fg = '#0D4715')
    updaval_entry = tk.Entry(updaval_frame, bg = '#F1F0E9', fg = '#0D4715')      

    back_button.pack(pady=10)
    updaval_mlabel.pack()
    id_label.pack(pady=10)
    id_entry.pack()
    updaval_label.pack(pady=10)
    updaval_entry.pack()
    updaval_button.pack(pady=10)

    show_frame(updaval_frame)

def handle_update_aval():
    try:
      aval_str = updaval_entry.get().lower()
      meal_id = int(id_entry.get())

      if aval_str in ["true", "yes", "1"]:
        aval = True
      elif aval_str in ["false", "no", "0"]:
          aval = False
      else:
          messagebox.showwarning(title="Invalid Input", message = "Please enter true/false, yes/no, 1/0")
        
      backend.update_meal_availability(meal_id,aval)

      for item in staff_tree.get_children():
          values = staff_tree.item(item)['values']
          if values[0] == meal_id:
              if aval:
                  staff_tree.item(item, values=(values[0], values[1], values[2], values[3], values[4], True))
              else:
                  staff_tree.delete(item)
                  

      staff_interface()

    except NotFoundError:
        messagebox.showwarning(title="Update Error", message="There is no meal with such ID!")


def open_view_orders():
    global vieworders_frame
    vieworders_frame.destroy()
    vieworders_frame = tk.Frame(window, bg = '#F1F0E9')
    #TODO add functionality 


def staff_interface():
    global staff_frame, staff_tree
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

    
    staff_tree = ttk.Treeview(staff_frame, columns=("ID", "Name", "Cost", "Category" ,"Stock", "Availability"))
    create_meal = tk.Button(staff_frame, text="Create Meal", font=('Arial', 14), bg = '#F1F0E9', fg = '#0D4715', width=50, command=open_create_meal)
    create_meal.pack(pady=10)
    update_stock = tk.Button(staff_frame, text="Update Stock", font=('Arial', 14), bg = '#F1F0E9', fg = '#0D4715', width=50, command=open_update_stock)
    update_stock.pack(pady=10)
    update_cost = tk.Button(staff_frame, text="Update Cost", font=('Arial', 14), bg = '#F1F0E9', fg = '#0D4715', width=50, command=open_update_cost)
    update_cost.pack(pady=10)
    update_availability = tk.Button(staff_frame, text="Update Availability", font=('Arial', 14), bg = '#F1F0E9', fg = '#0D4715', width=50, command=open_update_availability)
    update_availability.pack(pady=10)
    view_orders = tk.Button(staff_frame, text="View All Orders", font=('Arial', 14), bg = '#F1F0E9', fg = '#0D4715', width=50, command=open_view_orders)
    view_orders.pack(pady=10)

    show_frame(staff_frame)


def student_interface():
    global student_frame
    student_frame.destroy()
    student_frame = tk.Frame(window, bg='#F1F0E9')
    
    welcome_label = tk.Label(student_frame, text="Student Dashboard",font=('Arial', 20), bg='#F1F0E9', fg='#0D4715')
    welcome_label.pack(pady=20)
    back_button = tk.Button(student_frame, text="Back to Login", font=('Arial', 14),command=lambda: show_frame(login_frame))
    back_button.pack(pady=10)

    student_tree = ttk.Treeview(student_frame, columns=("ID", "Name", "Cost", "Category" ,"Stock", "Availability"))
    student_tree.heading('#0', text="")
    student_tree.heading("ID", text="ID")
    student_tree.heading("Name", text="Meal Name")
    student_tree.heading("Cost", text="Price")
    student_tree.heading("Category", text="Category")
    student_tree.heading("Stock", text="Stock")
    student_tree.heading("Availability", text="Available")

    student_tree.column('#0', width=0, stretch=False)
    student_tree.column("ID", width=50, anchor="center")
    student_tree.column("Name", width=200, anchor="center")
    student_tree.column("Cost", width=100, anchor="center")
    student_tree.column("Category", width=100, anchor="center")
    student_tree.column("Stock", width=50, anchor="center")
    student_tree.column("Availability", width=100, anchor="center")

    student_tree.pack(pady=10, fill='x')
    meals = backend.get_meals()
    for meal in meals:
        student_tree.insert("", "end", values=(meal.meal_id, meal.name, f"${meal.cost/100:.2f}",meal.category.name, meal.stock, meal.available))

    create_order = tk.Button(student_frame, text="Create Order", font=('Arial', 14), bg = '#F1F0E9', fg = '#0D4715', width=50, command=open_create_order)
    create_order.pack(pady=10)
    
    show_frame(student_frame)
    

def open_create_order():
    global crorder_frame, meal_id_entry, meal_qn_entry
    crorder_frame.destroy()
    crorder_frame = tk.Frame(window, bg='#F1F0E9')

    crorder_label = tk.Label(crorder_frame, text="Create Order",font=('Arial', 20), bg='#F1F0E9', fg='#0D4715')
    back_button = tk.Button(crorder_frame, text="Back to Main", font=('Arial', 14), bg = '#F1F0E9', fg = '#0D4715', command=student_interface)
    create_button = tk.Button(crorder_frame, text="Create Order", font=('Arial', 14), bg = '#F1F0E9', fg = '#0D4715', command=handle_create_order)

    meal_id_label = tk.Label(crorder_frame, text="Meal ID:",font=('Arial', 20), bg='#F1F0E9', fg='#0D4715')
    meal_id_entry = tk.Entry(crorder_frame, font=('Arial', 20), bg='#F1F0E9', fg='#0D4715')
    meal_qn_label = tk.Label(crorder_frame, text="Meal Quantity:",font=('Arial', 20), bg='#F1F0E9', fg='#0D4715')
    meal_qn_entry = tk.Entry(crorder_frame, font=('Arial', 20), bg='#F1F0E9', fg='#0D4715')

    back_button.pack(pady=10)
    crorder_label.pack()
    meal_id_label.pack(pady=10)
    meal_id_entry.pack()
    meal_qn_label.pack(pady=10)
    meal_qn_entry.pack()
    create_button.pack(pady=10)   

    show_frame(crorder_frame)



def handle_create_order():
    try:
        meal_id = int(meal_id_entry.get())
        quantity = int(meal_qn_entry.get())
        items = [(meal_id, quantity)]
        cr_user = backend.login(username_entry.get(),password_entry.get())

        backend.create_order(cr_user.user_id, items)
        messagebox.showinfo(title="Success", message="Order was created!")
        student_interface()
    except NotFoundError:
        messagebox.showwarning(title="Update Error", message="The meal is not found")
    except ConstraintError:
        messagebox.showwarning(title="Stock Not Available", message="The order exceeds stock")







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
