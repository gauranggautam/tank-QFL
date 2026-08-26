import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk, messagebox
import inspect
import importlib.util
import sys
import io
import os
import ast
import sv_ttk  # The theme library

class FunctionRunnerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Function Runner")
        self.root.geometry("850x700")
        self.root.minsize(600, 500)

        # --- Initialize instance variables ---
        self.functions = {}  # <<< THIS LINE WAS MISSING
        self.arg_entries = {}
        self.current_function = None

        # --- Set Dark Theme by Default ---
        sv_ttk.set_theme("dark")

        # --- Main Layout ---
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1) # Docstring box expands
        main_frame.rowconfigure(4, weight=1) # Output box expands

        # --- Top Frame for File and Function Selection ---
        top_frame = ttk.Frame(main_frame)
        top_frame.grid(row=0, column=0, sticky="ew", pady=5)
        top_frame.columnconfigure(2, weight=1)

        ttk.Button(top_frame, text="Select .py File", command=self._select_file).pack(side=tk.LEFT, padx=5)
        self.file_label = ttk.Label(top_frame, text="No file selected")
        self.file_label.pack(side=tk.LEFT, padx=5)

        ttk.Label(top_frame, text="Select Function:").pack(side=tk.LEFT, padx=(20, 5))
        self.function_combo = ttk.Combobox(top_frame, state="readonly", width=30)
        self.function_combo.pack(side=tk.LEFT, padx=5)
        self.function_combo.bind("<<ComboboxSelected>>", self._on_function_select)
        
        # --- Docstring Display ---
        docstring_frame = ttk.LabelFrame(main_frame, text="Docstring", padding="10")
        docstring_frame.grid(row=1, column=0, sticky="nsew", pady=10)
        docstring_frame.columnconfigure(0, weight=1)
        docstring_frame.rowconfigure(0, weight=1)
        
        self.docstring_text = scrolledtext.ScrolledText(docstring_frame, wrap=tk.WORD, height=8, relief=tk.FLAT)
        self.docstring_text.grid(row=0, column=0, sticky="nsew")
        self.docstring_text.config(bg="#2b2b2b", fg="#ffffff", insertbackground='white', state=tk.DISABLED)

        # --- Arguments Frame ---
        self.args_frame = ttk.LabelFrame(main_frame, text="Arguments", padding="10")
        self.args_frame.grid(row=2, column=0, sticky="ew", pady=5)
        self.args_frame.columnconfigure(0, weight=1)

        # --- Execution and Output ---
        ttk.Button(main_frame, text="▶ Run Function", command=self._execute_function, style='Accent.TButton').grid(row=3, column=0, pady=10)

        output_frame = ttk.LabelFrame(main_frame, text="Output", padding="10")
        output_frame.grid(row=4, column=0, sticky="nsew", pady=5)
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)

        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, height=10)
        self.output_text.grid(row=0, column=0, sticky="nsew")
        self.output_text.config(bg="#2b2b2b", fg="#ffffff", insertbackground='white')

    def _select_file(self):
        """Opens a file dialog to select a Python file."""
        filepath = filedialog.askopenfilename(
            title="Select a Python File",
            filetypes=(("Python files", "*.py"), ("All files", "*.*"))
        )
        if not filepath:
            return

        self.file_label.config(text=os.path.basename(filepath))
        self._load_functions_from_file(filepath)

    def _load_functions_from_file(self, filepath):
        """Loads a .py file as a module and inspects it for functions."""
        try:
            module_name = os.path.splitext(os.path.basename(filepath))[0]
            spec = importlib.util.spec_from_file_location(module_name, filepath)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            self.functions.clear()
            # Find functions defined IN THAT FILE (not imported ones)
            for name, func in inspect.getmembers(module, inspect.isfunction):
                if func.__module__ == module_name:
                    self.functions[name] = func

            self.function_combo['values'] = list(self.functions.keys())
            if self.functions:
                self.function_combo.current(0)
                self._on_function_select(None)
            else:
                self.function_combo.set('')
                self._clear_details()

        except Exception as e:
            messagebox.showerror("Error Loading File", f"Could not load or inspect the file:\n{e}")
            self._clear_details()

    def _on_function_select(self, event):
        """Updates the UI when a new function is selected."""
        func_name = self.function_combo.get()
        if not func_name:
            return

        self.current_function = self.functions[func_name]

        doc = inspect.getdoc(self.current_function) or "No docstring found."
        self.docstring_text.config(state=tk.NORMAL)
        self.docstring_text.delete(1.0, tk.END)
        self.docstring_text.insert(tk.END, doc)
        self.docstring_text.config(state=tk.DISABLED)

        for widget in self.args_frame.winfo_children():
            widget.destroy()
        self.arg_entries.clear()

        try:
            sig = inspect.signature(self.current_function)
            for param_name, param in sig.parameters.items():
                row = ttk.Frame(self.args_frame)
                row.pack(fill=tk.X, pady=2)
                
                label_text = f"{param_name}"
                if param.annotation != param.empty:
                    label_text += f" ({param.annotation.__name__})"
                
                ttk.Label(row, text=label_text, width=20).pack(side=tk.LEFT)
                entry = ttk.Entry(row, width=50)
                entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
                
                if param.default != param.empty:
                    entry.insert(0, repr(param.default))
                    
                self.arg_entries[param_name] = entry
        except ValueError:
             ttk.Label(self.args_frame, text="Cannot inspect arguments for this function.").pack()

    def _execute_function(self):
        """Gathers inputs, runs the function, and shows the output."""
        if not self.current_function:
            messagebox.showwarning("Warning", "No function selected.")
            return

        kwargs = {}
        try:
            for name, entry in self.arg_entries.items():
                val_str = entry.get()
                # Only evaluate if the string is not empty
                if val_str.strip():
                    kwargs[name] = ast.literal_eval(val_str)
        except (ValueError, SyntaxError) as e:
            messagebox.showerror(
                "Invalid Input",
                f"Error in argument format: {e}\n\nPlease use valid Python syntax (e.g., 'text' for strings, [1, 2] for lists)."
            )
            return
            
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        self.output_text.delete(1.0, tk.END)
        
        try:
            return_value = self.current_function(**kwargs)
            prints = captured_output.getvalue()

            self.output_text.insert(tk.END, "--- Printed Output ---\n")
            self.output_text.insert(tk.END, prints if prints else "None\n")
            self.output_text.insert(tk.END, "\n--- Return Value ---\n")
            self.output_text.insert(tk.END, repr(return_value))

        except Exception as e:
            self.output_text.insert(tk.END, f"--- EXECUTION ERROR ---\n{type(e).__name__}: {e}")
        finally:
            # Restore stdout
            sys.stdout = old_stdout

    def _clear_details(self):
        """Clears all dynamic fields."""
        self.function_combo['values'] = []
        self.function_combo.set('')
        self.docstring_text.config(state=tk.NORMAL)
        self.docstring_text.delete(1.0, tk.END)
        self.docstring_text.config(state=tk.DISABLED)
        for widget in self.args_frame.winfo_children():
            widget.destroy()
        self.output_text.delete(1.0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = FunctionRunnerApp(root)
    root.mainloop()