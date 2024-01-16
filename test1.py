import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import platform

class SVNFileTransferApp:
    def __init__(self, master):
        self.master = master
        master.title("SVN File Transfer")

        self.create_menu()
        self.create_toolbar()
        self.create_widgets()

    def create_menu(self):
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.master.destroy)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about_dialog)

    def create_toolbar(self):
        toolbar = ttk.Frame(self.master)
        toolbar.grid(row=0, column=0, sticky="ew")

        ttk.Button(toolbar, text="Push", command=self.push_to_svn).pack(side="left", padx=5)
        ttk.Button(toolbar, text="Pull", command=self.pull_from_svn).pack(side="left", padx=5)
        ttk.Button(toolbar, text="Clear", command=self.clear_text).pack(side="left", padx=5)

    def create_widgets(self):
        self.frame = ttk.Frame(self.master)
        self.frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(self.frame, text="Enter message:", font=("Helvetica", 12)).grid(row=0, column=0, pady=(0, 5), sticky="w")

        # Create a Text widget with Scrollbar
        self.text_scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.entry = tk.Text(self.frame, wrap=tk.WORD, font=("Helvetica", 14), yscrollcommand=self.text_scrollbar.set)
        self.text_scrollbar.config(command=self.entry.yview)

        self.entry.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.text_scrollbar.grid(row=1, column=1, pady=5, sticky="ns")

        ttk.Label(self.frame, text="Status:", font=("Helvetica", 10)).grid(row=2, column=0, pady=(5, 0), sticky="w")
        self.status_var = tk.StringVar()
        ttk.Label(self.frame, textvariable=self.status_var, font=("Helvetica", 10)).grid(row=3, column=0, pady=(0, 5), sticky="w")

        # Configure row and column to expand with window size
        self.master.rowconfigure(1, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(0, weight=1)

        # About label using pack manager
        about_label = ttk.Label(self.master, text="SVN File Transfer App\nVersion 1.0\n(c) 2023 Omnivision Belgium",
                  font=("Helvetica", 8), foreground="gray")
        about_label.grid(row=0, column=0, pady=5, sticky="se")

    def get_svn_command(self):
        if platform.system() == "Windows":
            return "svn.exe"
        else:
            return "svn"

    def push_to_svn(self):
        message = self.entry.get("1.0", tk.END).strip()  # Get the entire content of the Text widget

        # Replace with the URL of your SVN repository
        svn_repository_url = "https://10.0.0.80/svn/be-design/users/yongkai.zhang"

        # Replace with the local path where you want to store the SVN working copy
        local_working_copy_path = "C:\\Users\\yongkai.zhang\\Documents\\svn\\be-design\\users\\yongkai.zhang"

        svn_command = self.get_svn_command()

        # Ensure the local directory exists
        os.makedirs(local_working_copy_path, exist_ok=True)

        # Check if the local repository exists, otherwise perform a checkout
        if not os.path.exists(os.path.join(local_working_copy_path, ".svn")):
            subprocess.run([svn_command, "checkout", svn_repository_url, local_working_copy_path])

        # Perform an update to get the latest changes
        subprocess.run([svn_command, "update", local_working_copy_path])

        # Write the message to the shared file
        file_path = os.path.join(local_working_copy_path, "clipboard.txt")
        with open(file_path, "a") as file:
            file.write(message + "\n")

        # Commit the changes to the SVN repository
        try:
            subprocess.run([svn_command, "commit", local_working_copy_path, "-m", "Updated clipboard.txt"])
            self.status_var.set("File updated and committed successfully.")
        except subprocess.CalledProcessError as e:
            self.status_var.set(f"Error committing changes: {e}")

    def pull_from_svn(self):
        # Replace with the URL of your SVN repository
        svn_repository_url = "https://10.0.0.80/svn/be-design/users/yongkai.zhang"

        # Replace with the local path where you want to store the SVN working copy
        local_working_copy_path = "C:\\Users\\yongkai.zhang\\Documents\\svn\\be-design\\users\\yongkai.zhang"

        svn_command = self.get_svn_command()

        # Ensure the local directory exists
        os.makedirs(local_working_copy_path, exist_ok=True)

        # Check if the local repository exists, otherwise perform a checkout
        if not os.path.exists(os.path.join(local_working_copy_path, ".svn")):
            subprocess.run([svn_command, "checkout", svn_repository_url, local_working_copy_path])

        # Perform an update to get the latest changes
        subprocess.run([svn_command, "update", local_working_copy_path])

        # Read the content from the shared file
        file_path = os.path.join(local_working_copy_path, "clipboard.txt")
        try:
            with open(file_path, "r") as file:
                content = file.read()
                self.entry.delete("1.0", tk.END)  # Clear the Text widget before inserting new content
                self.entry.insert("1.0", content)  # Insert the new content
                self.status_var.set("File content updated successfully.")
        except FileNotFoundError:
            self.status_var.set("Error: File not found. Please push some content first.")

    def clear_text(self):
        # Clear the content of the Text widget
        self.entry.delete("1.0", tk.END)
        self.status_var.set("")
        
        # Update the SVN repository after clearing the text
        self.push_to_svn()

    def show_about_dialog(self):
        about_message = (
            "SVN File Transfer App\n"
            "Version 1.0\n"
            "(c) 2023 Omnivision Belgium"
        )
        messagebox.showinfo("About", about_message)

if __name__ == "__main__":
    root = tk.Tk()
    app = SVNFileTransferApp(root)
    root.mainloop()
