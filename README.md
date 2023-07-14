Git Script Documentation
This script is a graphical user interface (GUI) application written in Python using the tkinter library. It allows users to search for copyrighted fonts in a specified directory.

Prerequisites
Python and pip should be installed correctly.
The following dependencies are required:
chardet
If any of the dependencies are missing, the script automatically attempts to install them using the pip module.

Usage
Run the script using Python.
The GUI window will appear.
Select a folder by either entering the path manually in the entry field or clicking the "Browse" button and selecting a folder using the file dialog.
Choose the search mode by selecting one of the radio buttons:
"Only Monotype Fonts": Searches for files that contain the string "monotype" (case-insensitive).
"Any Copyright/Trademark": Searches for files that contain either the string "copyright" or "trademark" (case-insensitive), excluding those that contain the specified exclude string ("adobe" by default).
Click the "Search" button to start the search process.
The progress bar will show the progress of the search, and the progress label will display the current progress, the total number of files, and the estimated remaining time.
The results will be displayed in the text area below the progress bar. Each result represents a file path where a copyrighted font was found.
Scroll through the results using the scrollbar on the right.
Close the application window to exit the script.
Classes
SearchThread
A subclass of threading.Thread that performs the search operation in a separate thread. This allows the GUI to remain responsive during the search.

Constructor Parameters
path (string): The path to the directory to search in.
search_mode (string): The search mode to use ("monotype" or "copyright").
exclude_string (string): The string to exclude from the search results.
progressbar (ttk.Progressbar): The progress bar widget to update during the search.
progress_text (tk.StringVar): The string variable to update the progress label during the search.
results_text (tk.Text): The text widget to display the search results.
Methods
run(): Overrides the run() method of threading.Thread and starts the search process.
search(): Performs the search operation in the specified directory. It iterates over all files in the directory and its subdirectories, filters the files based on their extensions, checks their size, detects their encoding, and searches for the specified strings in the file content. The progress bar, progress label, and search results are updated during the search.
Application
The main application class that creates the GUI window and handles user interactions.

Constructor
Initializes the GUI window and sets its properties.
Methods
select_folder(): Opens a file dialog to select a folder and inserts the selected folder path into the entry field.
start_search(): Retrieves the folder path and search mode from the GUI elements and starts the search thread with the specified parameters.
GUI Elements
dropzone_label (tk.Label): Label widget that displays the instruction to select a folder.
entry (tk.Entry): Entry widget to manually enter the folder path.
browse_button (tk.Button): Button widget to open a file dialog and select a folder.
radio_monotype (tk.Radiobutton): Radiobutton widget for the "Only Monotype Fonts" search mode.
radio_copyright (tk.Radiobutton): Radiobutton widget for the "Any Copyright/Trademark" search mode.
search_button (tk.Button): Button widget to start the search process.
progressbar (ttk.Progressbar): Horizontal progress bar widget to display the progress of the search.
progress_label (tk.Label): Label widget to display the current progress, total number of files, and estimated remaining time.
results_text (tk.Text): Text widget to display the search results.
scrollbar (tk.Scrollbar): Scrollbar widget to scroll through the search results.
credit_label (tk.Label): Label widget to display the script's author.
Conclusion
This script provides a user-friendly way to search for copyrighted fonts in a specified directory. By utilizing a GUI, users can easily select the folder and choose the desired search mode. The script displays the search progress and presents the results in a readable format.
