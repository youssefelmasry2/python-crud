import tkinter as tk
from tkinter import ttk, messagebox
from main import MongoDBHandler

# Initialize the MongoDB handler
db_handler = MongoDBHandler()

# Initialize the main application window
class MongoDBApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MongoDB CRUD Operations")
        self.root.geometry("500x600")
        self.root.configure(bg="#2c3e50")  # Set background to a dark blue color

        # Title
        ttk.Label(
            root,
            text="MongoDB CRUD Operations",
            font=("Arial", 20, "bold"),
            foreground="white",
            background="#2c3e50"
        ).pack(pady=20)

        self.collection_var = tk.StringVar()
        self.operation_var = tk.StringVar()

        # Welcome text
        self.welcome_label = tk.Label(
            root, text="Welcome to Our Large-Scale DB Project",
            font=("Arial", 16, "bold"), fg="white", bg="#2c3e50"
        )
        self.welcome_label.pack(pady=10)

        # Dropdown for collections
        ttk.Label(root, text="Select Collection:", background="#2c3e50", foreground="white").pack(pady=5)
        self.collection_dropdown = ttk.Combobox(
            root, textvariable=self.collection_var,
            values=["departments", "professors", "courses", "students"]
        )
        self.collection_dropdown.pack(pady=5, padx=10)

        # Dropdown for operation
        ttk.Label(root, text="Select Operation:", background="#2c3e50", foreground="white").pack(pady=5)
        self.operation_dropdown = ttk.Combobox(
            root, textvariable=self.operation_var,
            values=["Create", "Read", "Update", "Delete"]
        )
        self.operation_dropdown.pack(pady=5, padx=10)

        # Action button
        self.action_button = ttk.Button(root, text="Perform Operation", command=self.perform_operation)
        self.action_button.pack(pady=20, padx=10)
        self.action_button.configure(style='TButton')

        # Text box for input/output
        self.text_box = tk.Text(root, height=20, width=60, bg="white", fg="black", font=("Arial", 12))
        self.text_box.pack(pady=10, padx=10)

        # Styling for buttons
        style = ttk.Style()
        style.configure('TButton', background='black', foreground='white', font=('Arial', 12, 'bold'))
        style.map('TButton', background=[('active', 'gray')])

    def perform_operation(self):
        collection = self.collection_var.get()
        operation = self.operation_var.get()

        if not collection or not operation:
            messagebox.showwarning("Input Error", "Please select a collection and an operation.")
            return

        if operation == "Create":
            self.create_document(collection)
        elif operation == "Read":
            self.read_documents(collection)
        elif operation == "Update":
            self.update_document(collection)
        elif operation == "Delete":
            self.delete_document(collection)
        else:
            messagebox.showwarning("Operation Error", "Invalid operation selected.")

    def create_document(self, collection):
        new_window = tk.Toplevel(self.root)
        new_window.title("Create Document")
        new_window.configure(bg="#2c3e50")

        fields = self.get_fields_by_collection(collection)
        entries = {}

        for field in fields:
            if field == "_id":
                continue
            ttk.Label(new_window, text=f"{field}:", background="#2c3e50", foreground="white").pack(pady=5)
            entry = ttk.Entry(new_window)
            entry.pack(pady=5, padx=10)
            entries[field] = entry

        def submit():
            document = {field: entry.get() for field, entry in entries.items()}

            if any(not value.strip() for value in document.values()):
                messagebox.showwarning("Input Error", "All fields are required.")
                return

            try:
                document_id = db_handler.create(collection, document)
                messagebox.showinfo("Success", f"Document created with ID: {document_id}")
                new_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(new_window, text="Submit", command=submit).pack(pady=10)

    def read_documents(self, collection):
        query = {}
        try:
            documents = db_handler.read(collection, query)
            self.text_box.delete(1.0, tk.END)
            for doc in documents:
                self.text_box.insert(tk.END, f"{doc}\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_document(self, collection):
        # Implement update functionality here
        pass

    def delete_document(self, collection):
        new_window = tk.Toplevel(self.root)
        new_window.title("Delete Document")
        new_window.configure(bg="#2c3e50")

        try:
            documents = db_handler.read(collection, {})
            document_names = [doc.get('name', str(doc['_id'])) for doc in documents]

            if not document_names:
                messagebox.showinfo("No Data", "No documents found in this collection.")
                new_window.destroy()
                return

            ttk.Label(new_window, text="Select Document to Delete:", background="#2c3e50", foreground="white").pack(pady=5)
            self.document_var = tk.StringVar()
            self.document_dropdown = ttk.Combobox(new_window, textvariable=self.document_var, values=document_names)
            self.document_dropdown.pack(pady=5, padx=10)

            def submit():
                selected_document_name = self.document_var.get()

                if not selected_document_name:
                    messagebox.showwarning("Selection Error", "Please select a document to delete.")
                    return

                query = {'name': selected_document_name} if 'name' in documents[0] else {'_id': selected_document_name}
                try:
                    deleted_count = db_handler.delete(collection, query)
                    messagebox.showinfo("Success", f"Number of documents deleted: {deleted_count}")
                    new_window.destroy()
                except Exception as e:
                    messagebox.showerror("Error", str(e))

            ttk.Button(new_window, text="Delete", command=submit).pack(pady=10)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def get_fields_by_collection(self, collection):
        fields = {
            "departments": ["_id", "name", "head"],
            "professors": ["_id", "name", "email", "department_id"],
            "courses": ["_id", "title", "department_id", "professor_id"],
            "students": ["_id", "name", "email", "enrolled_date", "enrolled_courses"],
        }
        return fields.get(collection, [])

if __name__ == "__main__":
    root = tk.Tk()
    app = MongoDBApp(root)
    root.mainloop()
