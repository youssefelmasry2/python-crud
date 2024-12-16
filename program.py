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

        self.collection_var = tk.StringVar()
        self.operation_var = tk.StringVar()

        # Dropdown for collections
        ttk.Label(root, text="Select Collection:").pack(pady=5)
        self.collection_dropdown = ttk.Combobox(
            root, textvariable=self.collection_var, values=["departments", "professors", "courses", "students"]
        )
        self.collection_dropdown.pack(pady=5)

        # Dropdown for operation
        ttk.Label(root, text="Select Operation:").pack(pady=5)
        self.operation_dropdown = ttk.Combobox(
            root, textvariable=self.operation_var, values=["Create", "Read", "Update", "Delete"]
        )
        self.operation_dropdown.pack(pady=5)

        # Action button
        self.action_button = ttk.Button(root, text="Perform Operation", command=self.perform_operation)
        self.action_button.pack(pady=10)

        # Text box for input/output
        self.text_box = tk.Text(root, height=20, width=60)
        self.text_box.pack(pady=10)

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
        # Create dialog for entering document fields
        new_window = tk.Toplevel(self.root)
        new_window.title("Create Document")

        fields = self.get_fields_by_collection(collection)
        entries = {}

        for field in fields:
            # Skip '_id' since MongoDB will generate it automatically
            if field == "_id":
                continue
            ttk.Label(new_window, text=f"{field}:").pack(pady=5)
            entry = ttk.Entry(new_window)
            entry.pack(pady=5)
            entries[field] = entry

        def submit():
            document = {field: entry.get() for field, entry in entries.items()}
            try:
                # Insert the document without the '_id' field to let MongoDB generate it
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
        new_window = tk.Toplevel(self.root)
        new_window.title("Update Document")

        ttk.Label(new_window, text="Enter Query Field:").pack(pady=5)
        query_field = ttk.Entry(new_window)
        query_field.pack(pady=5)

        ttk.Label(new_window, text="Enter Query Value:").pack(pady=5)
        query_value = ttk.Entry(new_window)
        query_value.pack(pady=5)

        ttk.Label(new_window, text="Enter Field to Update:").pack(pady=5)
        update_field = ttk.Entry(new_window)
        update_field.pack(pady=5)

        ttk.Label(new_window, text="Enter New Value:").pack(pady=5)
        new_value = ttk.Entry(new_window)
        new_value.pack(pady=5)

        def submit():
            query = {query_field.get(): query_value.get()}
            update_data = {update_field.get(): new_value.get()}
            try:
                updated_count = db_handler.update(collection, query, update_data)
                messagebox.showinfo("Success", f"Number of documents updated: {updated_count}")
                new_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(new_window, text="Submit", command=submit).pack(pady=10)

    def delete_document(self, collection):
        new_window = tk.Toplevel(self.root)
        new_window.title("Delete Document")

        ttk.Label(new_window, text="Enter Query Field:").pack(pady=5)
        query_field = ttk.Entry(new_window)
        query_field.pack(pady=5)

        ttk.Label(new_window, text="Enter Query Value:").pack(pady=5)
        query_value = ttk.Entry(new_window)
        query_value.pack(pady=5)

        def submit():
            query = {query_field.get(): query_value.get()}
            try:
                deleted_count = db_handler.delete(collection, query)
                messagebox.showinfo("Success", f"Number of documents deleted: {deleted_count}")
                new_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(new_window, text="Submit", command=submit).pack(pady=10)

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
