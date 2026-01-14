import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
from .parser import Parser
from .builder import Builder
from .exporter import Exporter

class AIForgeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AIForge Manager v1.0.2")
        self.root.geometry("600x500")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        self.init_import_tab()
        self.init_export_tab()

        # Log Console
        self.log_frame = ttk.LabelFrame(root, text="Logs")
        self.log_frame.pack(fill='both', expand=True, padx=10, pady=5)
        self.log_text = tk.Text(self.log_frame, height=8, state='disabled')
        self.log_text.pack(fill='both', expand=True, padx=5, pady=5)

    def log(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    def init_import_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="AI -> Project")

        # Input File
        ttk.Label(tab, text="AI Dump File (.txt, .md):").pack(anchor='w', padx=10, pady=5)
        frame_in = ttk.Frame(tab)
        frame_in.pack(fill='x', padx=10)
        self.import_file_var = tk.StringVar()
        ttk.Entry(frame_in, textvariable=self.import_file_var).pack(side='left', fill='x', expand=True)
        ttk.Button(frame_in, text="Browse", command=self.browse_import_file).pack(side='right', padx=5)

        # Output Dir
        ttk.Label(tab, text="Output Project Directory:").pack(anchor='w', padx=10, pady=5)
        frame_out = ttk.Frame(tab)
        frame_out.pack(fill='x', padx=10)
        self.import_dir_var = tk.StringVar()
        ttk.Entry(frame_out, textvariable=self.import_dir_var).pack(side='left', fill='x', expand=True)
        ttk.Button(frame_out, text="Browse", command=self.browse_import_dir).pack(side='right', padx=5)

        # Convert Button
        ttk.Button(tab, text="Convert / Build Project", command=self.run_import).pack(pady=20)

    def init_export_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Project -> AI")

        # Project Dir
        ttk.Label(tab, text="Project Directory:").pack(anchor='w', padx=10, pady=5)
        frame_in = ttk.Frame(tab)
        frame_in.pack(fill='x', padx=10)
        self.export_dir_var = tk.StringVar()
        ttk.Entry(frame_in, textvariable=self.export_dir_var).pack(side='left', fill='x', expand=True)
        ttk.Button(frame_in, text="Browse", command=self.browse_export_dir).pack(side='right', padx=5)

        # Output File
        ttk.Label(tab, text="Output Log File (.txt, .md):").pack(anchor='w', padx=10, pady=5)
        frame_out = ttk.Frame(tab)
        frame_out.pack(fill='x', padx=10)
        self.export_file_var = tk.StringVar()
        ttk.Entry(frame_out, textvariable=self.export_file_var).pack(side='left', fill='x', expand=True)
        ttk.Button(frame_out, text="Browse", command=self.browse_export_file).pack(side='right', padx=5)

        # Export Button
        ttk.Button(tab, text="Export to AI Format", command=self.run_export).pack(pady=20)

    def browse_import_file(self):
        f = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt *.md"), ("All Files", "*.*")])
        if f: self.import_file_var.set(f)

    def browse_import_dir(self):
        d = filedialog.askdirectory()
        if d: self.import_dir_var.set(d)

    def browse_export_dir(self):
        d = filedialog.askdirectory()
        if d: self.export_dir_var.set(d)

    def browse_export_file(self):
        f = filedialog.asksaveasfilename(defaultextension=".md", filetypes=[("Markdown", "*.md"), ("Text", "*.txt")])
        if f: self.export_file_var.set(f)

    def run_import(self):
        inp = self.import_file_var.get()
        out = self.import_dir_var.get()
        if not inp or not out:
            messagebox.showerror("Error", "Please select input file and output directory")
            return
        
        self.log(f"Starting import: {inp} -> {out}")
        def task():
            try:
                parser = Parser()
                data = parser.parse(inp)
                builder = Builder()
                builder.build(data, out, mode='merge') # Safety default
                self.root.after(0, lambda: self.log("Import Completed Successfully!"))
                self.root.after(0, lambda: messagebox.showinfo("Success", "Project built successfully!"))
            except Exception as e:
                self.root.after(0, lambda: self.log(f"Error: {str(e)}"))
                self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
        
        threading.Thread(target=task).start()

    def run_export(self):
        inp = self.export_dir_var.get()
        out = self.export_file_var.get()
        if not inp or not out:
            messagebox.showerror("Error", "Please select project directory and output file")
            return
        
        self.log(f"Starting export: {inp} -> {out}")
        def task():
            try:
                exporter = Exporter()
                exporter.export(inp, out)
                self.root.after(0, lambda: self.log("Export Completed Successfully!"))
                self.root.after(0, lambda: messagebox.showinfo("Success", "Project export successfully!"))
            except Exception as e:
                self.root.after(0, lambda: self.log(f"Error: {str(e)}"))
                self.root.after(0, lambda: messagebox.showerror("Error", str(e)))

        threading.Thread(target=task).start()


def main():
    root = tk.Tk()
    app = AIForgeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
