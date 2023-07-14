<h1>Copyrighted Fonts Finder</h1>
-------------------------------------------------------------------
<h2>What it is ?</h2>
<p>This script provides a user-friendly way to search for copyrighted fonts in a specified directory</p>
<p>The fonts extensions compatibles are:</p>
<p>'.ACFM', '.AMFM', '.DFONT', '.EOT', '.FNT', '.FON', '.GDF', '.GDR', '.GTF', '.MMM', '.OTF', '.PFA', '.TPF', '.TTC', '.TTF', '.WOFF'</p>

<p>Note: since verifying a copyright is quite complex this script cannot be considered 100% infallible.</p>

<h2>Prerequisites</h2>
<ul>
    <li><a href="https://www.python.org/downloads/">Python</a> and <a href="https://pip.pypa.io/en/stable/installation/" target="_BLANK">pip</a> should be installed correctly.</li>
    <li>The following dependencies are required:
        <ul>
            <li>chardet</li>
            Note: the script automatically attempts to install it using the <code>pip</code> module.
        </ul>
    </li>
</ul>
<h2>Usage</h2>
<ol>
    <li>Run the script using Python.</li>
    <li>The GUI window will appear.</li>
    <li>Select a folder by either entering the path manually in the entry field or clicking the "Browse" button and selecting a folder using the file dialog.</li>
    <li>Choose the search mode by selecting one of the radio buttons:
        <ul>
            <li>"Only Monotype Fonts": Searches for files that contain the string "monotype" (case-insensitive).</li>
            <li>"Any Copyright/Trademark": Searches for files that contain either the string "copyright" or "trademark" (case-insensitive), excluding those that contain the specified exclude string ("adobe" by default assuming you have an adobe license and "google" fonts because they are free).</li>
            <li>Note: You could create a new branch changing the searching strings like you want changing the elements of the array inside the variable called "exclude_strings"</li>
        </ul>
    </li>
    <li>Click the "Search" button to start the search process.</li>
    <li>The progress bar will show the progress of the search, and the progress label will display the current progress, the total number of files, and the estimated remaining time.</li>
    <li>The results will be displayed in the text area below the progress bar. Each result represents a file path where a copyrighted font was found.</li>
    <li>You can scroll through the results using the scrollbar on the right.</li>
</ol>
-----------------------------------------------------------------
<h2>Technical boring stuff</h2>

<h2>Classes</h2>

<h3><code>SearchThread</code></h3>
<p>A subclass of <code>threading.Thread</code> that performs the search operation in a separate thread. This allows the GUI to remain responsive during the search.</p>

<h4>Constructor Parameters</h4>
<ul>
    <li><code>path</code> (string): The path to the directory to search in.</li>
    <li><code>search_mode</code> (string): The search mode to use ("monotype" or "copyright").</li>
    <li><code>exclude_string</code> (string): The string to exclude from the search results.</li>
    <li><code>progressbar</code> (ttk.Progressbar): The progress bar widget to update during the search.</li>
    <li><code>progress_text</code> (tk.StringVar): The string variable to update the progress label during the search.</li>
    <li><code>results_text</code> (tk.Text): The text widget to display the search results.</li>
</ul>

<h4>Methods</h4>
<ul>
    <li><code>run()</code>: Overrides the <code>run()</code> method of <code>threading.Thread</code> and starts the search process.</li>
    <li><code>search()</code>: Performs the search operation in the specified directory. It iterates over all files in the directory and its subdirectories, filters the files based on their extensions, checks their size, detects their encoding, and searches for the specified strings in the file content. The progress bar, progress label, and search results are updated during the search.</li>
</ul>

<h3><code>Application</code></h3>
<p>The main application class that creates the GUI window and handles user interactions.</p>

<h4>Constructor</h4>
<p>Initializes the GUI window and sets its properties.</p>

<h4>Methods</h4>
<ul>
    <li><code>select_folder()</code>: Opens a file dialog to select a folder and inserts the selected folder path into the entry field.</li>
    <li><code>start_search()</code>: Retrieves the folder path and search mode from the GUI elements and starts the search thread with the specified parameters.</li>
</ul>

<h2>GUI Elements</h2>
<ul>
    <li><code>dropzone_label</code> (tk.Label): Label widget that displays the instruction to select a folder.</li>
    <li><code>entry</code> (tk.Entry): Entry widget to manually enter the folder path.</li>
    <li><code>browse_button</code> (tk.Button): Button widget to open a file dialog and select a folder.</li>
    <li><code>radio_monotype</code> (tk.Radiobutton): Radiobutton widget for the "Only Monotype Fonts" search mode.</li>
    <li><code>radio_copyright</code> (tk.Radiobutton): Radiobutton widget for the "Any Copyright/Trademark" search mode.</li>
    <li><code>search_button</code> (tk.Button): Button widget to start the search process.</li>
    <li><code>progressbar</code> (ttk.Progressbar): Horizontal progress bar widget to display the progress of the search.</li>
    <li><code>progress_label</code> (tk.Label): Label widget to display the current progress, total number of files, and estimated remaining time.</li>
    <li><code>results_text</code> (tk.Text): Text widget to display the search results.</li>
    <li><code>scrollbar</code> (tk.Scrollbar): Scrollbar widget to scroll through the search results.</li>
    <li><code>credit_label</code> (tk.Label): Label widget to display the script's author.</li>
</ul>
