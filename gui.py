import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["LibraryDB441"]
collection = db["books441"]

# Window Setup
root = tk.Tk()
root.title("Library Database Collector - MongoDB CRUD")
root.geometry("750x600")
root.config(bg="#e6f7f5")  # Light teal background

# Title
tk.Label(
    root,
    text="Library Database Collector - CRUD Operations",
    font=("Arial", 16, "bold"),
    bg="#00695c",
    fg="white",
    padx=10,
    pady=10
).pack(fill="x")

# Form Frame
form_frame = tk.Frame(root, bg="#e6f7f5")
form_frame.pack(pady=10, anchor="w", padx=20)

# Book ID
tk.Label(form_frame, text="Book ID:", bg="#e6f7f5", font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="w", pady=5)
id_entry = tk.Entry(form_frame, width=40)
id_entry.grid(row=0, column=1, pady=5)

# Title
tk.Label(form_frame, text="Book Title:", bg="#e6f7f5", font=("Arial", 11, "bold")).grid(row=1, column=0, sticky="w", pady=5)
name_entry = tk.Entry(form_frame, width=40)
name_entry.grid(row=1, column=1, pady=5)

# Author
tk.Label(form_frame, text="Author:", bg="#e6f7f5", font=("Arial", 11, "bold")).grid(row=2, column=0, sticky="w", pady=5)
age_entry = tk.Entry(form_frame, width=40)
age_entry.grid(row=2, column=1, pady=5)

# Genre
tk.Label(form_frame, text="Genre:", bg="#e6f7f5", font=("Arial", 11, "bold")).grid(row=3, column=0, sticky="w", pady=5)
country_entry = tk.Entry(form_frame, width=40)
country_entry.grid(row=3, column=1, pady=5)


# Insert Function
def insert():
    book_id = id_entry.get().strip()
    title = name_entry.get().strip()
    author = age_entry.get().strip()
    genre = country_entry.get().strip()

    if not (book_id and title and author and genre):
        messagebox.showwarning("Missing Data", "Please fill all fields.")
        return

    try:
        collection.insert_one({
            "book_id": book_id,
            "title": title,
            "author": author,
            "genre": genre
        })
        messagebox.showinfo("Success", "Book inserted successfully!")
        id_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        country_entry.delete(0, tk.END)
    except:
        messagebox.showerror("Error", "Failed to insert book.")

# Display Function
def read():
    try:
        documents = collection.find()
        result = ""
        for doc in documents:
            result += f"Book ID: {doc['book_id']}\nTitle: {doc['title']}\nAuthor: {doc['author']}\nGenre: {doc['genre']}\n\n"
        result_label.config(text=result)
    except:
        messagebox.showerror("Error", "Failed to display data.")

# Update Function
def update():
    update_window = tk.Toplevel(root)
    update_window.title("Update Book Record")
    update_window.geometry("400x300")
    update_window.config(bg="#f1f8e9")

    tk.Label(update_window, text="Title (to match):", bg="#f1f8e9").pack(pady=5)
    name_input = tk.Entry(update_window, width=30)
    name_input.pack()

    tk.Label(update_window, text="New Author:", bg="#f1f8e9").pack(pady=5)
    age_input = tk.Entry(update_window, width=30)
    age_input.pack()

    tk.Label(update_window, text="New Genre:", bg="#f1f8e9").pack(pady=5)
    country_input = tk.Entry(update_window, width=30)
    country_input.pack()

    def updateinfo():
        old_title = name_input.get()
        new_author = age_input.get()
        new_genre = country_input.get()

        if not (old_title and new_author and new_genre):
            messagebox.showwarning("Warning", "Fields cannot be empty.")
            return

        result = collection.update_one({"title": old_title}, {"$set": {"author": new_author, "genre": new_genre}})
        if result.modified_count > 0:
            messagebox.showinfo("Success", "Book updated successfully!")
            update_window.destroy()
        else:
            messagebox.showinfo("No Match", "No matching book found.")

    tk.Button(update_window, text="Confirm Update", command=updateinfo, bg="#2e7d32", fg="white").pack(pady=10)

# Delete Function
def delete():
    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Book Record")
    delete_window.geometry("350x200")
    delete_window.config(bg="#ffebee")

    tk.Label(delete_window, text="Enter Book ID to Delete:", bg="#ffebee").pack(pady=10)
    id_input = tk.Entry(delete_window, width=30)
    id_input.pack()

    def deleteInfo():
        old_id = id_input.get()
        result = collection.delete_many({"book_id": old_id})

        if result.deleted_count > 0:
            messagebox.showinfo("Success", "Book(s) deleted successfully!")
            delete_window.destroy()
        else:
            messagebox.showinfo("No Match", "No matching book found.")

    tk.Button(delete_window, text="Confirm Delete", command=deleteInfo, bg="#c62828", fg="white").pack(pady=10)

# Buttons Frame
btn_frame = tk.Frame(root, bg="#e6f7f5")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Insert", command=insert, bg="#00796b", fg="white", width=12).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Display Books", command=read, bg="#0288d1", fg="white", width=12).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Update", command=update, bg="#f9a825", fg="white", width=12).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Delete", command=delete, bg="#d32f2f", fg="white", width=12).grid(row=0, column=3, padx=5)

# Output Label
result_label = tk.Label(root, text="", justify="left", anchor="w", bg="#e6f7f5", font=("Arial", 10))
result_label.pack(fill="both", expand=True, padx=20, pady=10)

# Run App
root.mainloop()