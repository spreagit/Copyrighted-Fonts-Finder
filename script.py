import os
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import time
import threading

try:
    from pip._internal import main as pip_main
except ImportError:
    messagebox.showerror("Error", "The 'pip' module is not available. Make sure you have Python and pip installed correctly.")
    exit()

# Automatic installation of missing dependencies
missing_modules = []
required_modules = ['chardet']
for module in required_modules:
    try:
        __import__(module)
    except ImportError:
        missing_modules.append(module)

if missing_modules:
    messagebox.showinfo("Information", f"Some missing modules have been detected: {', '.join(missing_modules)}. "
                                        f"Proceeding with the automatic installation of missing dependencies...")
    for module in missing_modules:
        pip_main(['install', module])

valid_extensions = ['.ACFM', '.AMFM', '.DFONT', '.EOT', '.FNT', '.FON', '.GDF', '.GDR', '.GTF', '.MMM', '.OTF', '.PFA', '.TPF', '.TTC', '.TTF', '.WOFF']
import chardet


class SearchThread(threading.Thread):
    def __init__(self, path, search_mode, exclude_string, progressbar, progress_text, results_text):
        super().__init__()
        self.path = path
        self.search_mode = search_mode
        self.exclude_string = exclude_string
        self.progressbar = progressbar
        self.progress_text = progress_text
        self.results_text = results_text

    def run(self):
        self.progressbar["value"] = 0
        self.progress_text.set("0/0 (0.00%) - Remaining Time: 0.00 seconds")
        self.results_text.delete(1.0, tk.END)
        self.search()

    def search(self):
        # Check if the path is a directory
        if not os.path.isdir(self.path):
            messagebox.showerror("Error", "The specified path is not a valid directory.")
            return

        results = []

        total_files = 0
        for root_dir, _, files in os.walk(self.path):
            for file in files:
                extension = os.path.splitext(file)[1].upper()
                if extension in valid_extensions:
                    total_files += 1

        progress = 0
        start_time = time.time()

        for root_dir, _, files in os.walk(self.path):
            for file in files:
                file_path = os.path.join(root_dir, file)

                extension = os.path.splitext(file_path)[1].upper()
                if extension not in valid_extensions:
                    continue

                # Check the file size
                if os.path.getsize(file_path) <= 10 * 1024 * 1024:  # Maximum size of 10 MB
                    # Detect file encoding
                    with open(file_path, 'rb') as f:
                        raw_data = f.read()
                        encoding = chardet.detect(raw_data)['encoding']

                    try:
                        # Open the file in read mode with the detected encoding
                        with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                            content = f.read()

                            # Check if the string is present in the file (case-insensitive)
                            if self.search_mode == "monotype":
                                if "monotype" in content.lower():
                                    results.append(file_path)
                            else:
                                if ("copyright" in content.lower() or "trademark" in content.lower()) \
                                        and self.exclude_string.lower() not in content.lower():
                                    results.append(file_path)
                    except UnicodeDecodeError:
                        pass

                progress += 1
                elapsed_time = time.time() - start_time
                remaining_files = total_files - progress
                remaining_time = elapsed_time * (remaining_files / progress) if progress > 0 else 0
                self.progressbar["value"] = (progress / total_files) * 100
                self.progress_text.set(
                    f"{progress}/{total_files} ({self.progressbar['value']:.2f}%) - Remaining Time: {remaining_time:.2f} seconds")
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, "\n".join(results))

                # Update the GUI
                self.progressbar.update_idletasks()
                self.results_text.update_idletasks()

            if progress == total_files:
                break


class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Copyrighted Fonts Finder")
        self.geometry("1200x600")
        self.configure(bg="#F0F0F0")

        self.dropzone_label = tk.Label(self, text="Select a folder", font=("Arial", 16, "bold"), bg="#F0F0F0")
        self.dropzone_label.pack(pady=20)

        self.entry = tk.Entry(self, width=70, font=("Arial", 12))
        self.entry.pack(pady=10)

        self.browse_button = tk.Button(self, text="Browse", command=self.select_folder,
                                       font=("Arial", 12, "bold"), bg="#FF9800", fg="black", relief=tk.RAISED, width=10)
        self.browse_button.pack(pady=10)

        self.mode_var = tk.StringVar()
        self.mode_var.set("monotype")

        self.radio_frame = tk.Frame(self, bg="#F0F0F0")
        self.radio_frame.pack(pady=10)

        self.radio_monotype = tk.Radiobutton(self.radio_frame, text="Only Monotype Fonts", variable=self.mode_var,
                                             value="monotype", font=("Arial", 12), bg="#F0F0F0")
        self.radio_monotype.pack(side=tk.LEFT, padx=10)

        self.radio_copyright = tk.Radiobutton(self.radio_frame, text="Any Copyright/Trademark ",
                                               variable=self.mode_var, value="copyright", font=("Arial", 12),
                                               bg="#F0F0F0")
        self.radio_copyright.pack(side=tk.LEFT)

        self.search_button = tk.Button(self, text="Search", command=self.start_search,
                                       font=("Arial", 12, "bold"), bg="#1E90FF", fg="black", relief=tk.RAISED, width=10)
        self.search_button.pack(pady=10)

        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Custom.Horizontal.TProgressbar", thickness=36, troughcolor="#E0E0E0",
                             troughrelief=tk.FLAT, background="#4CAF50")

        self.progressbar = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=700, mode='determinate',
                                            style="Custom.Horizontal.TProgressbar", value=0)
        self.progressbar.pack(pady=10)

        self.progress_text = tk.StringVar()
        self.progress_text.set("0/0 (0.00%) - Remaining Time: 0.00 seconds")
        self.progress_label = tk.Label(self, textvariable=self.progress_text, font=("Arial", 12), bg="#F0F0F0")
        self.progress_label.pack(pady=10)

        self.results_label = tk.Label(self, text="Results:", font=("Arial", 14, "bold"), bg="#F0F0F0")
        self.results_label.pack(pady=10)

        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.results_text = tk.Text(self, width=160, height=8, font=("Arial", 10), wrap="word",
                                    yscrollcommand=self.scrollbar.set)
        self.results_text.pack(pady=10)

        self.scrollbar.config(command=self.results_text.yview)

        self.credit_label = tk.Label(self, text="Coded with love by Alberto Z.", font=("Arial", 10),
                                     bg="#F0F0F0", fg="black", anchor=tk.E)
        self.credit_label.pack(side=tk.BOTTOM, anchor=tk.E, padx=10, pady=5)

        self.search_thread = None

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, folder)

    def start_search(self):
        folder = self.entry.get()
        search_mode = self.mode_var.get()

        self.search_thread = SearchThread(folder, search_mode, "adobe", self.progressbar,
                                          self.progress_text, self.results_text)

        self.search_thread.start()


root = Application()
root.mainloop()
