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

    for module in missing_modules:
        pip_main(['install', module])

valid_extensions = ['.ACFM', '.AMFM', '.DFONT', '.EOT', '.FNT', '.FON', '.GDF', '.GDR', '.GTF', '.MMM', '.OTF', '.PFA', '.TPF', '.TTC', '.TTF', '.WOFF']
import chardet


class SearchThread(threading.Thread):
    def __init__(self, path, search_mode, exclude_strings, progressbar, progress_text, results_text, results_label_var):
        super().__init__()
        self.path = path
        self.search_mode = search_mode
        self.exclude_strings = exclude_strings
        self.progressbar = progressbar
        self.progress_text = progress_text
        self.results_text = results_text
        self.results_label_var = results_label_var
        self.font_copyright_found = False
        self.num_results = 0

    def run(self):
        self.progressbar["value"] = 0
        self.progress_text.set("Analized fonts 0/0 (0.00%) - Remaining Time: 0.00 seconds")
        self.results_text.delete(1.0, tk.END)
        self.results_label_var.set("Results: 0 found")
        self.search()
        results_available = self.font_copyright_found
        if not results_available:
            self.results_text.insert(tk.END, "No copyrighted fonts found.")

    def search(self):
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

                if os.path.getsize(file_path) <= 10 * 1024 * 1024:
                    with open(file_path, 'rb') as f:
                        raw_data = f.read()
                        encoding = chardet.detect(raw_data)['encoding']

                    try:
                        with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                            content = f.read()

                            if self.search_mode == "monotype":
                                if "monotype" in content.lower():
                                    results.append(file_path)
                                    self.font_copyright_found = True
                                    self.num_results += 1
                            else:
                                if all((exclude_string.lower() not in content.lower() for exclude_string in self.exclude_strings)) \
                                        and any((keyword in content.lower() for keyword in ["copyright", "trademark"])):
                                    results.append(file_path)
                                    self.font_copyright_found = True
                                    self.num_results += 1
                    except UnicodeDecodeError:
                        pass

                progress += 1
                elapsed_time = time.time() - start_time
                remaining_files = total_files - progress
                remaining_time = elapsed_time * (remaining_files / progress) if progress > 0 else 0
                self.progressbar["value"] = (progress / total_files) * 100
                self.progress_text.set(
                    f"Analized fonts {progress}/{total_files} ({self.progressbar['value']:.2f}%) - Remaining Time: {remaining_time:.2f} seconds")
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, "\n".join(results))
                self.results_label_var.set(f"Results: {self.num_results} founds")

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
        self.mode_var.set("copyright")

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
        self.progress_text.set("Analized fonts 0/0 (0.00%) - Remaining Time: 0.00 seconds")
        self.progress_label = tk.Label(self, textvariable=self.progress_text, font=("Arial", 12), bg="#F0F0F0")
        self.progress_label.pack(pady=10)

        self.results_label_var = tk.StringVar()
        self.results_label_var.set("Results: 0 found")
        self.results_label = tk.Label(self, textvariable=self.results_label_var, font=("Arial", 14, "bold"), bg="#F0F0F0")
        self.results_label.pack(pady=10)

        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.results_text = tk.Text(self, width=160, height=8, font=("Arial", 10), wrap="word",
                                    yscrollcommand=self.scrollbar.set)
        self.results_text.pack(pady=10)

        self.scrollbar.config(command=self.results_text.yview)

        self.credit_frame = tk.Frame(self, bg="#F0F0F0")
        self.credit_frame.pack(side=tk.BOTTOM, anchor=tk.E, padx=10, pady=5)

        self.credit_label = tk.Label(self.credit_frame, text="Coded with", font=("Arial", 10), fg="black")
        self.credit_label.pack(side=tk.LEFT)

        self.heart_label = tk.Label(self.credit_frame, text="\u2764", font=("Arial", 10), fg="red")
        self.heart_label.pack(side=tk.LEFT)

        self.name_label = tk.Label(self.credit_frame, text="by Alberto Z.", font=("Arial", 10), fg="black")
        self.name_label.pack(side=tk.LEFT)

        self.search_thread = None

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, folder)

    def start_search(self):
        folder = self.entry.get()
        search_mode = self.mode_var.get()
        exclude_strings = ["adobe", "google", "microsoft"]  # Modify this list to include additional exclude strings

        self.search_thread = SearchThread(folder, search_mode, exclude_strings, self.progressbar,
                                          self.progress_text, self.results_text, self.results_label_var)

        self.search_thread.start()


root = Application()
root.mainloop()
