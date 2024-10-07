import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, colorchooser
from PIL import Image, ImageTk
import os

# Global variables to store user data
selected_point = None
img_path = None
img_display = None
username = None
password = None
color_pattern = None

# Function to browse and select an image
def browse_image():
    global img_path, img_display
    img_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if img_path:
        img = Image.open(img_path)
        img = img.resize((300, 300), Image.LANCZOS)  # Resize the image to 300x300
        img_display = ImageTk.PhotoImage(img)
        img_label.config(image=img_display)
        img_label.image = img_display
        
        # Save the resized image to the current working directory
        save_path = os.path.join(os.getcwd(), os.path.basename(img_path))
        img.save(save_path)
        img_path = save_path  # Update img_path to the saved image path

# Function to handle image click for user creation
def on_image_click(event):
    global selected_point
    selected_point = (event.x, event.y)
    messagebox.showinfo("Point Selected", f"Point selected at: {selected_point}")
    img_label.unbind("<Button-1>")
    save_user_data()

# Function to save user data to a text file
def save_user_data():
    if selected_point:
        with open("users.txt", "a") as file:
            file.write(f"{username},{password},{selected_point[0]},{selected_point[1]},{os.path.basename(img_path)},{color_pattern}\n")
        messagebox.showinfo("User Created", "User created successfully!")

# Function to create a new user
def create_user():
    global username, password, selected_point, color_pattern
    selected_point = None

    username = simpledialog.askstring("Input", "Enter username:")
        
    if not username:
        return

    password = simpledialog.askstring("Input", "Enter password:", show='*')
    
    if not password:
        return

    color = colorchooser.askcolor(title="Choose color")
    if color[1] is None:
        return
    color_pattern = color[1]

    img_label.bind("<Button-1>", on_image_click)
    messagebox.showinfo("Select Point", "Click a point on the image to set as graphical password point.")

# Function to verify user click for authentication
def verify_user_click(event):
    click_point = (event.x, event.y)
    user_found = False
    with open("users.txt", "r") as file:
        for line in file:
            user_data = line.strip().split(",")
            if username == user_data[0] and password == user_data[1] and os.path.basename(img_path) == user_data[4] and color_pattern == user_data[5]:
                user_found = True
                saved_point = (int(user_data[2]), int(user_data[3]))
                if abs(saved_point[0] - click_point[0]) < 10 and abs(saved_point[1] - click_point[1]) < 10:
                    messagebox.showinfo("Authenticated", "User authenticated successfully!")
                else:
                    messagebox.showerror("Error", "Invalid graphical password point.")
                break
    if not user_found:
        messagebox.showerror("Error", "Invalid username, password, or color pattern.")
    img_label.unbind("<Button-1>")

# Function to authenticate a user
def authenticate_user():
    global username, password, img_path, img_display, color_pattern

    username = simpledialog.askstring("Input", "Enter username:")
    f=open("users.txt","r")
    s=f.read()
    if username not in s:
        messagebox.showinfo("Invalid", "Invalid Username :(")
        return
    
    if not username:
        return

    password = simpledialog.askstring("Input", "Enter password:", show='*')
    if password not in s:
        messagebox.showinfo("Invalid", "Invalid Password :(")
        return

    if not password:
        return

    color = colorchooser.askcolor(title="Choose color")
    if str(color[1]) not in s:
        messagebox.showinfo("Invalid", "Invalid Color selection :(")
        return
    if color[1] is None:
        return
    color_pattern = color[1]

    img_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if not img_path:
        return

    img = Image.open(img_path)
    img = img.resize((300, 300), Image.LANCZOS)  # Resize the image to 300x300
    img_display = ImageTk.PhotoImage(img)
    img_label.config(image=img_display)
    img_label.image = img_display

    img_label.bind("<Button-1>", verify_user_click)
    messagebox.showinfo("Authenticate", "Click the point on the image you used for registration.")

# Function to view the list of users
def view_users():
    try:
        with open("users.txt", "r") as file:
            users_list = file.readlines()
            if users_list:
                users_info = "\n".join(users_list)
                messagebox.showinfo("Registered Users", users_info)
            else:
                messagebox.showinfo("Registered Users", "No users registered yet.")
    except FileNotFoundError:
        messagebox.showinfo("Registered Users", "No users registered yet.")

# Function to remove a user from the users list
def remove_user():
    username_to_remove = simpledialog.askstring("Input", "Enter username to remove:")
    if not username_to_remove:
        return
    
    user_found = False
    try:
        with open("users.txt", "r") as file:
            users_list = file.readlines()
        
        with open("users.txt", "w") as file:
            for user in users_list:
                if user.split(",")[0] != username_to_remove:
                    file.write(user)
                else:
                    user_found = True
        
        if user_found:
            messagebox.showinfo("Remove User", f"User '{username_to_remove}' removed successfully.")
        else:
            messagebox.showerror("Remove User", f"User '{username_to_remove}' not found.")
    except FileNotFoundError:
        messagebox.showerror("Remove User", "No users registered yet.")

# Function to update a user's password
def update_password():
    global username, password
    username = simpledialog.askstring("Input", "Enter username:")
    if not username:
        return

    current_password = simpledialog.askstring("Input", "Enter current password:", show='*')
    if not current_password:
        return

    new_password = simpledialog.askstring("Input", "Enter new password:", show='*')
    if not new_password:
        return

    user_found = False
    updated_users = []

    try:
        with open("users.txt", "r") as file:
            users_list = file.readlines()
        
        for user in users_list:
            user_data = user.strip().split(",")
            if user_data[0] == username and user_data[1] == current_password:
                user_found = True
                user_data[1] = new_password  # Update password
            updated_users.append(",".join(user_data) + "\n")

        if user_found:
            with open("users.txt", "w") as file:
                file.writelines(updated_users)
            messagebox.showinfo("Update Password", "Password updated successfully.")
        else:
            messagebox.showerror("Update Password", "Invalid username or current password.")
    except FileNotFoundError:
        messagebox.showerror("Update Password", "No users registered yet.")

# Function to update a user's graphical password point
def update_graphical_password():
    global username, password, img_path, img_display, color_pattern

    username = simpledialog.askstring("Input", "Enter username:")
    if not username:
        return

    password = simpledialog.askstring("Input", "Enter password:", show='*')
    if not password:
        return

    color = colorchooser.askcolor(title="Choose color")
    if color[1] is None:
        return
    color_pattern = color[1]

    img_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if not img_path:
        return

    img = Image.open(img_path)
    img = img.resize((300, 300), Image.LANCZOS)  # Resize the image to 300x300
    img_display = ImageTk.PhotoImage(img)
    img_label.config(image=img_display)
    img_label.image = img_display

    def on_new_image_click(event):
        new_point = (event.x, event.y)
        user_found = False
        updated_users = []

        try:
            with open("users.txt", "r") as file:
                users_list = file.readlines()
            
            for user in users_list:
                user_data = user.strip().split(",")
                if user_data[0] == username and user_data[1] == password and user_data[5] == color_pattern:
                    user_found = True
                    user_data[2], user_data[3] = str(new_point[0]), str(new_point[1])
                updated_users.append(",".join(user_data) + "\n")

            if user_found:
                with open("users.txt", "w") as file:
                    file.writelines(updated_users)
                messagebox.showinfo("Update Graphical Password", "Graphical password point updated successfully.")
            else:
                messagebox.showerror("Update Graphical Password", "Invalid username, password, or color pattern.")
        except FileNotFoundError:
            messagebox.showerror("Update Graphical Password", "No users registered yet.")
        img_label.unbind("<Button-1>")

    img_label.bind("<Button-1>", on_new_image_click)
    messagebox.showinfo("Update Graphical Password", "Click the new point on the image to set as graphical password point.")

# Function to update a user's color pattern
def update_color_pattern():
    global username, password, color_pattern

    username = simpledialog.askstring("Input", "Enter username:")
    if not username:
        return

    password = simpledialog.askstring("Input", "Enter password:", show='*')
    if not password:
        return

    color = colorchooser.askcolor(title="Choose new color")
    if color[1] is None:
        return
    new_color_pattern = color[1]

    user_found = False
    updated_users = []

    try:
        with open("users.txt", "r") as file:
            users_list = file.readlines()
        
        for user in users_list:
            user_data = user.strip().split(",")
            if user_data[0] == username and user_data[1] == password:
                user_found = True
                user_data[5] = new_color_pattern  # Update color pattern
            updated_users.append(",".join(user_data) + "\n")

        if user_found:
            with open("users.txt", "w") as file:
                file.writelines(updated_users)
            messagebox.showinfo("Update Color Pattern", "Color pattern updated successfully.")
        else:
            messagebox.showerror("Update Color Pattern", "Invalid username or password.")
    except FileNotFoundError:
        messagebox.showerror("Update Color Pattern", "No users registered yet.")

# Function to handle the login process
def login():
    def check_login():
        if username_entry.get() == "admin" and password_entry.get() == "admin":
            login_window.destroy()
            open_main_window()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("300x200")

    tk.Label(login_window, text="Username:").pack(pady=5)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Password:").pack(pady=5)
    password_entry = tk.Entry(login_window, show='*')
    password_entry.pack(pady=5)

    tk.Button(login_window, text="Login", command=check_login).pack(pady=10)

    login_window.mainloop()

# Function to set up and display the main window
def open_main_window():
    global img_label

    root = tk.Tk()
    root.title("Graphical Password System")
    root.geometry("800x600")
    root.configure(bg='black')

    # Label to display the selected image
    img_label = tk.Label(root, bg='black')
    img_label.pack(pady=20)

    # Common button style
    button_style = {'bg': 'black', 'fg': 'white', 'font': ('Courier New', 10, 'bold')}

    # Browse button to select an image
    browse_button = tk.Button(root, text="Browse Image", command=browse_image, **button_style)
    browse_button.pack(pady=10)

    # Create User button to create a new user
    create_user_button = tk.Button(root, text="Create User", command=create_user, **button_style)
    create_user_button.pack(pady=10)

    # Authenticate User button to authenticate a user
    authenticate_user_button = tk.Button(root, text="Authenticate User", command=authenticate_user, **button_style)
    authenticate_user_button.pack(pady=10)

    # View Users button to view the list of registered users
 
    # Update Password button to update a user's password
    update_password_button = tk.Button(root, text="Update Password", command=update_password, **button_style)
    update_password_button.pack(pady=10)

    # Update Graphical Password button to update a user's graphical password point
    update_graphical_password_button = tk.Button(root, text="Update Graphical Password", command=update_graphical_password, **button_style)
    update_graphical_password_button.pack(pady=10)

    # Update Color Pattern button to update a user's color pattern
    update_color_pattern_button = tk.Button(root, text="Update Color Pattern", command=update_color_pattern, **button_style)
    update_color_pattern_button.pack(pady=10)

    # Start the GUI main loop
    root.mainloop()

# Start the login process
login()
