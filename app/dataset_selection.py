import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, scrolledtext
import pandas as pd
import requests
from io import StringIO

selected_data = None
column = None

root = tk.Tk()
root.title("Dataset Selection Tool")
root.iconbitmap('favicon.ico')
root.geometry("800x600")
log_text = scrolledtext.ScrolledText(root, height=10)
log_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

def load_dataset_from_url():
    url = simpledialog.askstring("Load from URL", "Enter the dataset URL:")
    if url:
        try:
            response = requests.get(url)
            data = pd.read_csv(StringIO(response.text))
            log_text.insert(tk.END, f"Dataset loaded successfully from URL.\n")
            return data
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load from URL\n{e}")
            return None

def load_dataset_from_file():
    filepath = filedialog.askopenfilename(initialdir="/", title="Select Dataset",
                                          filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if filepath:
        try:
            data = pd.read_csv(filepath)
            log_text.insert(tk.END, f"Dataset loaded successfully from file: {filepath}\n")
            return data
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load dataset\n{e}")
            return None


def load_and_select_dataset():
    global selected_data, column
    choice = messagebox.askquestion("Load Dataset", "Do you want to load the dataset from a URL?")
    data = load_dataset_from_url() if choice == 'yes' else load_dataset_from_file()

    if data is not None:
        columns = list(data.columns)
        column_info = "\n".join([f"{col}: {str(data[col].dropna().unique()[:5])} [...]" for col in columns])
        messagebox.showinfo("Column Info", f"Available columns and sample data:\n{column_info}")

        column = simpledialog.askstring("Select Column", "Type the column name for text analysis:")
        if column in columns:
            global selected_data
            selected_data = data[[column]]
            save_btn.config(state=tk.NORMAL)
        else:
            messagebox.showwarning("Warning", "Column not found.")
            save_btn.config(state=tk.DISABLED)


def save_selected_column():
    global selected_data, column
    if selected_data is not None and column is not None:
        save_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                                                 title="Save Selected Column")
        if save_path:
            try:
                selected_data[column].to_csv(save_path, index=False, header=False)
                messagebox.showinfo("Success", f"Column '{column}' saved successfully to {save_path}.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save the selected column\n{e}")

save_btn = tk.Button(root, text="Save Selected Column as TXT", command=save_selected_column, state=tk.DISABLED)
save_btn.pack(pady=20)

load_btn = tk.Button(root, text="Load and Select Dataset", command=load_and_select_dataset)
load_btn.pack(pady=20)


root.mainloop()