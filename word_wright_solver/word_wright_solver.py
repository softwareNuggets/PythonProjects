import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import webbrowser

class WordFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WORD WRIGHT SOLVER")
        self.root.geometry("400x728")
        
        # Variables
        self.mandatory_char = tk.StringVar()
        self.additional_chars = tk.StringVar()
        self.word_length = tk.IntVar(value=7)  # Default total length
        self.font_size = tk.IntVar(value=12)
        
        # Word list
        self.words = []
        
        # Store references to all widgets that need font updates
        self.font_widgets = []
        
        # Create custom styles for ttk widgets
        self.style = ttk.Style()
        
        # Bind validation
        self.mandatory_char.trace('w', self.validate_mandatory_char)
        self.additional_chars.trace('w', self.validate_additional_chars)
        self.font_size.trace('w', self.update_fonts)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Row 0: Load File Button
        load_button = ttk.Button(main_frame, text="Load Word File", command=self.load_file)
        load_button.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky=tk.W)
        self.font_widgets.append(('ttk_button', load_button))
        
        # Row 1: Mandatory Character
        label1 = ttk.Label(main_frame, text="Mandatory Character:")
        label1.grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.font_widgets.append(('label', label1))
        
        self.mandatory_entry = ttk.Entry(main_frame, textvariable=self.mandatory_char, width=5)
        self.mandatory_entry.grid(row=1, column=1, sticky=tk.W, pady=(0, 10))
        self.font_widgets.append(('entry', self.mandatory_entry))
        
        # Row 2: Additional Characters
        label2 = ttk.Label(main_frame, text="Additional Characters:")
        label2.grid(row=2, column=0, sticky=tk.W, padx=(0, 10))
        self.font_widgets.append(('label', label2))
        
        self.additional_entry = ttk.Entry(main_frame, textvariable=self.additional_chars, width=10)
        self.additional_entry.grid(row=2, column=1, sticky=tk.W, pady=(0, 10))
        self.font_widgets.append(('entry', self.additional_entry))
        
        # Row 3: Word Length Slider
        label3 = ttk.Label(main_frame, text="Word Length:")
        label3.grid(row=3, column=0, sticky=tk.W, padx=(0, 10))
        self.font_widgets.append(('label', label3))
        
        length_frame = ttk.Frame(main_frame)
        length_frame.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.length_slider = tk.Scale(length_frame, from_=4, to=15, orient=tk.HORIZONTAL, 
                                    variable=self.word_length, length=120)
        self.length_slider.pack(side=tk.LEFT)
        self.font_widgets.append(('scale', self.length_slider))
        
        
        # Row 4: Find Words Button (using tk.Button for color customization)
        self.find_button = tk.Button(main_frame, text="Find Words", command=self.find_words, 
                                   state="disabled", bg="lightgreen", fg="gray", 
                                   activebackground="darkgreen", activeforeground="white")
                                   
        self.find_button.grid(row=4, column=0, columnspan=2, pady=(0, 10), sticky=tk.W)
        self.font_widgets.append(('tk_button', self.find_button))
        
        # Row 5: Status Bar
        self.status_label = ttk.Label(main_frame, text="Load a word file to begin", 
                                     relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        self.status_label.bind("<Button-1>", self.open_wiktionary)
        self.font_widgets.append(('label', self.status_label))
        
        # Row 6: Found Words Label
        label6 = ttk.Label(main_frame, text="Found Words (Search Results)")
        label6.grid(row=6, column=0, columnspan=2, sticky=tk.W)
        self.font_widgets.append(('label', label6))
        
        # Row 7: Listbox with scrollbar
        listbox_frame = ttk.Frame(main_frame)
        listbox_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        listbox_frame.columnconfigure(0, weight=1)
        listbox_frame.rowconfigure(0, weight=1)
        
        self.results_listbox = tk.Listbox(listbox_frame, height=15)
        self.results_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.results_listbox.bind('<Button-1>', self.on_word_click)
        self.font_widgets.append(('listbox', self.results_listbox))
        
        scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=self.results_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.results_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Row 8: Count Label
        self.count_label = ttk.Label(main_frame, text="0 words found")
        self.count_label.grid(row=8, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        self.font_widgets.append(('label', self.count_label))
        
        # Row 9: Font Size Controls
        font_frame = ttk.Frame(main_frame)
        font_frame.grid(row=9, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        font_label = ttk.Label(font_frame, text="Font Size:")
        font_label.pack(side=tk.LEFT, padx=(0, 10))
        self.font_widgets.append(('label', font_label))
        
        # Using tk.Button for font control buttons to enable color customization
        self.minus_button = tk.Button(font_frame, text="-", command=self.decrease_font, 
                                     width=3, bg="lightgray", activebackground="gray")
        self.minus_button.pack(side=tk.LEFT, padx=(0, 5))
        self.font_widgets.append(('tk_button', self.minus_button))
        
        self.font_size_label = ttk.Label(font_frame, text="12")
        self.font_size_label.pack(side=tk.LEFT, padx=(0, 5))
        self.font_widgets.append(('label', self.font_size_label))
        
        self.plus_button = tk.Button(font_frame, text="+", command=self.increase_font, 
                                    width=3, bg="lightgray", activebackground="gray")
        self.plus_button.pack(side=tk.LEFT)
        self.font_widgets.append(('tk_button', self.plus_button))
        
        # Row 10: Exit Button (using tk.Button for color customization)
        exit_button = tk.Button(main_frame, text="Exit", command=self.exit_app,
                               bg="orange", fg="black", activebackground="darkorange", 
                               activeforeground="black")
        exit_button.grid(row=10, column=0, columnspan=2, pady=(10, 0), sticky=tk.W)
        self.font_widgets.append(('tk_button', exit_button))
        
        # Configure grid weights for resizing
        main_frame.rowconfigure(7, weight=1)
        
        # Initialize fonts
        self.update_fonts()
        
    def exit_app(self):
        self.root.quit()  # Stops the main loop
        self.root.destroy()  # Destroys the window and frees resources
        
    def load_file(self):
        """Load a word file"""
        file_path = filedialog.askopenfilename(
            title="Select Word File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    self.words = [word.strip().lower() for word in file.readlines() if word.strip()]
                
                if not self.words:
                    messagebox.showerror("Error", "The selected file is empty!")
                    return
                
                self.status_label.config(text=f"Loaded {len(self.words)} words from file")
                self.update_button_state()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
        
    def validate_mandatory_char(self, *args):
        """Validate mandatory character input"""
        value = self.mandatory_char.get()
        if len(value) > 1:
            self.mandatory_char.set(value[0])
        elif len(value) == 1 and not value.isalpha():
            self.mandatory_char.set("")
        else:
            self.mandatory_char.set(value.lower())
        self.update_button_state()
        
    def validate_additional_chars(self, *args):
        """Validate additional characters input"""
        value = self.additional_chars.get()
        # Keep only letters and remove duplicates
        cleaned = ''.join(c.lower() for c in value if c.isalpha())
        seen = set()
        unique_chars = []
        for c in cleaned:
            if c not in seen:
                seen.add(c)
                unique_chars.append(c)
        
        # Limit to 6 characters
        if len(unique_chars) > 6:
            unique_chars = unique_chars[:6]
            
        # Remove mandatory character if it appears in additional chars
        mandatory = self.mandatory_char.get()
        if mandatory:
            unique_chars = [c for c in unique_chars if c != mandatory]
            
        self.additional_chars.set(''.join(unique_chars))
        self.update_button_state()
        
    def update_button_state(self):
        """Enable/disable find button based on input validity"""
        mandatory = self.mandatory_char.get()
        additional = self.additional_chars.get()
        has_words = len(self.words) > 0
        
        if len(mandatory) == 1 and len(additional) == 6 and has_words:
            self.find_button.config(state="normal")
        else:
            self.find_button.config(state="disabled")
            
    def update_length_label(self, *args):
        """Update the word length display label"""
        length = self.word_length.get()
        self.length_label.config(text=f"{length} characters")
        
    def find_words(self):
        """Find words matching the criteria"""
        mandatory = self.mandatory_char.get().lower()
        additional = self.additional_chars.get().lower()
        target_length = self.word_length.get()
        allowed_chars = set(mandatory + additional)
        
        # Clear previous results
        self.results_listbox.delete(0, tk.END)
        self.status_label.config(text="Searching...")
        
        matching_words = []
        for word in self.words:
            if len(word) != target_length:
                continue
            if mandatory not in word:
                continue
            if all(char in allowed_chars for char in word):
                matching_words.append(word)
        
        # Sort and display results
        matching_words.sort()
        for word in matching_words:
            self.results_listbox.insert(tk.END, word)
        
        count = len(matching_words)
        self.count_label.config(text=f"{count} words found")
        self.status_label.config(text=f"Search complete - {count} words found")
        
    def on_word_click(self, event):
        """Handle word selection in listbox"""
        selection = self.results_listbox.curselection()
        if selection:
            word = self.results_listbox.get(selection[0])
            wiktionary_url = f"https://en.wiktionary.org/wiki/{word}"
            self.status_label.config(text=f"Click to view '{word}' on Wiktionary: {wiktionary_url}",
                                   foreground="blue", cursor="hand2")
            self.current_word = word
            
    def open_wiktionary(self, event):
        """Open Wiktionary link in browser"""
        if hasattr(self, 'current_word') and self.current_word:
            webbrowser.open(f"https://en.wiktionary.org/wiki/{self.current_word}")
            
    def increase_font(self):
        """Increase font size"""
        current_size = self.font_size.get()
        if current_size < 24:
            self.font_size.set(current_size + 1)
            
    def decrease_font(self):
        """Decrease font size"""
        current_size = self.font_size.get()
        if current_size > 10:
            self.font_size.set(current_size - 1)
            
    def update_fonts(self, *args):
        """Update fonts for all widgets"""
        size = self.font_size.get()
        self.font_size_label.config(text=str(size))
        
        default_font = ("TkDefaultFont", size)
        entry_font = ("TkTextFont", size)
        listbox_font = ("TkFixedFont", size)
        
        # Update TTK styles first
        self.style.configure('TLabel', font=default_font)
        self.style.configure('TButton', font=default_font)
        
        for widget_type, widget in self.font_widgets:
            try:
                if widget_type == 'label':
                    widget.configure(font=default_font)
                elif widget_type == 'ttk_button':
                    # TTK buttons use style-based font configuration
                    pass  # Already handled by style.configure above
                elif widget_type == 'tk_button':
                    # TK buttons can have font configured directly
                    widget.configure(font=default_font)
                elif widget_type == 'entry':
                    widget.configure(font=entry_font)
                elif widget_type == 'listbox':
                    widget.configure(font=listbox_font)
                elif widget_type == 'scale':
                    widget.configure(font=default_font)
            except Exception as e:
                print(f"Font update error for {widget}: {e}")

def main():
    root = tk.Tk()
    app = WordFinderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
