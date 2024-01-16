import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import platform

class SVNFileTransferApp:
    def __init__(self, master):
        self.master = master
        master.title("SVN File Transfer")

        self.label = tk.Label(master, text="Enter message:")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.push_button = tk.Button(master, text="Push to SVN", command=self.push_to_svn)
        self.push_button.pack()

        self.pull_button = tk.Button(master, text="Pull from SVN", command=self.pull_from_svn)
        self.pull_button.pack()

    def get_svn_command(self):
        if platform.system() == "Windows":
            return "svn.exe"
        else:
            return "svn"

    def push_to_svn(self):
        message = self.entry.get()

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
            messagebox.showinfo("Success", "File updated and committed successfully.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Error committing changes: {e}")

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
                messagebox.showinfo("File Content", content)
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found. Please push some content first.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SVNFileTransferApp(root)
    root.mainloop()
