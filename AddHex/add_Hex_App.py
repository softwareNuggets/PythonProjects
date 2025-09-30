#YT Title: Master Hex Addition: Interactive Step-by-Step App + 1000+ Practice Problems
#YT Channel:  @SoftwareNuggets
#Programmer:  Scott Johnson  -- email: softwareNugget65@gmail.com

#YT video link:
#GITHUB source code link:

#Please take the time to write a comment about this video and like.

import tkinter as tk
from tkinter import messagebox, ttk
import random
import webbrowser
from PIL import Image, ImageTk  # add at the top with other imports

# Global font settings
ENTRY_FONT = ("Courier", 24)
LABEL_FONT = ("Arial", 14)
INFO_FONT = ("Arial", 12)
BUTTON_FONT = ("Arial", 12, "bold")
INDEX_FONT = ("Arial", 9)

class HexAdderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hexadecimal Adder by YT:SoftwareNuggets channel")
        self.root.geometry("1100x780")
        self.root.resizable(False, False)
        self.reference_frame = None
        self.reference_visible = False  # Track state
        
        self.step_index = 6  # start from rightmost digit (7 columns)

        # Storage for entry boxes
        self.num1_row = []
        self.num2_row = []
        self.result_row = []
        self.carry_row = []
        self.add_base10_row = []  # New row for decimal addition
        self.test_carry_row = []  # New row for carry test

        # Create style for professional buttons
        self.style = ttk.Style()
        self.style.configure("TButton",
                             font=BUTTON_FONT,
                             padding=6,
                             relief="raised")
        self.style.map("TButton",
                       background=[("active", "#4CAF50")],
                       foreground=[("active", "white")])

        self.create_widgets()
        self.toggle_hex_reference()

    # ----------------------------
    # UI Setup
    # ----------------------------
    def create_widgets(self):
        validate_hex = self.root.register(self.validate_hex_input)

        # Instruction message at the top
        instructions = tk.Label(
            self.root,
            text="Enter hexadecimal digits (0–9, A–F)",
            font=INFO_FONT,
            fg="blue"
        )
        instructions.grid(row=0, column=0, columnspan=8, pady=10)

        # Column Index header
        tk.Label(self.root, text="Index", font=LABEL_FONT).grid(row=1, column=0, sticky="e", padx=5)
        for col in range(7):
            index = 7 - col   # Gives 7 down to 1
            tk.Label(self.root, text=str(index), font=INDEX_FONT).grid(row=1, column=col + 1, padx=3, pady=3)

        # Row labels
        tk.Label(self.root, text="Carry:", font=LABEL_FONT).grid(row=2, column=0, sticky="e", padx=5)
        tk.Label(self.root, text="Num_1:", font=LABEL_FONT).grid(row=4, column=0, sticky="e", padx=5)
        tk.Label(self.root, text="+ Num_2:", font=LABEL_FONT).grid(row=5, column=0, sticky="e", padx=5)
        tk.Label(self.root, text="Add Base 10:", font=LABEL_FONT).grid(row=6, column=0, sticky="e", padx=5)
        tk.Label(self.root, text="Test Carry:", font=LABEL_FONT).grid(row=7, column=0, sticky="e", padx=5)
        tk.Label(self.root, text="Sum:", font=LABEL_FONT).grid(row=9, column=0, sticky="e", padx=5)

        # Carry row
        for col in range(7):
            entry = tk.Entry(self.root, width=4, font=ENTRY_FONT, justify="left", state="readonly")
            entry.grid(row=2, column=col + 1, padx=3, pady=3)
            self.carry_row.append(entry)

        # Separator line (after Carry)
        separatorCarry = tk.Frame(self.root, height=2, bd=1, relief="sunken")
        separatorCarry.grid(row=3, column=1, columnspan=7, sticky="we", padx=5, pady=5)

        # Row_1 
        for col in range(7):
            if col == 0:
                e1 = tk.Entry(self.root, width=4, font=ENTRY_FONT, justify="left",
                              state="readonly", readonlybackground="lightgray")
            else:
                e1 = tk.Entry(self.root, width=4, font=ENTRY_FONT, justify="left",
                              validate="key", validatecommand=(validate_hex, "%P"),
                              bg="white")
                e1.bind("<KeyRelease>", self.auto_advance)
            e1.grid(row=4, column=col + 1, padx=3, pady=3)
            self.num1_row.append(e1)

        # Row_2
        for col in range(7):
            if col == 0:
                e2 = tk.Entry(self.root, width=4, font=ENTRY_FONT, justify="left",
                              state="readonly", readonlybackground="lightgray")
            else:
                e2 = tk.Entry(self.root, width=4, font=ENTRY_FONT, justify="left",
                              validate="key", validatecommand=(validate_hex, "%P"),
                              bg="white")
                e2.bind("<KeyRelease>", self.auto_advance)
            e2.grid(row=5, column=col + 1, padx=3, pady=3)
            self.num2_row.append(e2)

        # Add Base 10 row
        for col in range(7):
            entry = tk.Entry(self.root, width=10, font=INDEX_FONT, justify="left", state="readonly")
            entry.grid(row=6, column=col + 1, padx=3, pady=3)
            self.add_base10_row.append(entry)

        # Test Carry row
        for col in range(7):
            entry = tk.Entry(self.root, width=10, font=INDEX_FONT, justify="left", state="readonly")
            entry.grid(row=7, column=col + 1, padx=3, pady=3)
            self.test_carry_row.append(entry)

        # Separator line (before Sum)
        separator = tk.Frame(self.root, height=2, bd=1, relief="sunken")
        separator.grid(row=8, column=1, columnspan=7, sticky="we", padx=5, pady=5)

        # Result row
        for col in range(7):
            er = tk.Entry(self.root, width=4, font=ENTRY_FONT, justify="left", state="readonly")
            er.grid(row=9, column=col + 1, padx=3, pady=3)
            self.result_row.append(er)

        # Step button under the Sum row
        self.step_button = tk.Button(self.root, text="Enter a Problem or press Generate Sample",
                                      bg="lightGreen", fg="black", font="ENTRY_FONT",
                                      command=self.step)
        self.step_button.grid(row=10, column=1, columnspan=7, sticky="we", padx=5, pady=5)

        # Top buttons: Generate Sample & Clear All
        self.top_button_frame = tk.Frame(self.root)
        self.top_button_frame.place(x=910, y=40, width=170, height=160)
        tk.Button(self.top_button_frame, text="Generate Sample",
                  width=19, height=3, bg="orange", fg="black", font=LABEL_FONT,
                  command=self.generate_sample).pack(side="top", padx=2, pady=4)
        tk.Button(self.top_button_frame, text="Clear All",
                  width=19, height=3, bg="skyblue", fg="black", font=LABEL_FONT,
                  command=self.clear_all).pack(side="top", padx=2, pady=4)

        # Step-by-step log area
        self.how_to_steps = tk.Text(self.root, width=88, height=21, wrap="word", font=("Courier", 12))
        self.how_to_steps.grid(row=11, column=0, columnspan=8, pady=10,padx=5)
        self.how_to_steps.insert(tk.END, "Step-by-step instructions will be displayed here.\n")

    # ----------------------------
    # Input Validation
    # ----------------------------
    def validate_hex_input(self, value):
        if value == "":
            return True
        return all(c in "0123456789ABCDEFabcdef" for c in value) and len(value) <= 1

    def auto_advance(self, event):
        widget = event.widget
        if len(widget.get()) == 1:
            for row in [self.num1_row, self.num2_row]:
                if widget in row:
                    idx = row.index(widget)
                    if idx < 6:
                        row[idx + 1].focus()
                    break

    # ----------------------------
    # Utility Functions
    # ----------------------------
    def get_values(self, row):
        values = []
        for box in row:
            text = box.get().upper()
            values.append(int(text, 16) if text else 0)
        return values

    def _set_readonly_value(self, entry, value_str):
        entry.config(state="normal")
        entry.delete(0, tk.END)
        if value_str:
            entry.insert(0, str(value_str).upper())
        entry.config(state="readonly")

    def _set_value(self, entry, value_str):
        entry.delete(0, tk.END)
        if value_str:
            entry.insert(0, str(value_str).upper())

    # ----------------------------
    # Right-align helpers
    # ----------------------------
    def right_align_row(self, row):
        """
        Shift digits in a row of Entry boxes (indices 1..6) to the right-most editable cells.
        The leftmost cell (index 0) is readonly and preserved.
        """
        digits = []
        for i in range(1, len(row)):
            v = row[i].get().strip().upper()
            if v:
                digits.append(v)

        for i in range(1, len(row)):
            row[i].delete(0, tk.END)

        if not digits:
            return

        start_index = len(row) - len(digits)
        if start_index < 1:
            start_index = 1

        for i, d in enumerate(digits):
            row[start_index + i].insert(0, d)

    def align_inputs(self):
        """Align both Num_1 and Num_2 rows (called before stepping)."""
        self.right_align_row(self.num1_row)
        self.right_align_row(self.num2_row)

    # ----------------------------
    # Sample Generator
    # ----------------------------
    def generate_sample(self):
        self.clear_all()
        self.reset_backgrounds()
        
        len_a = random.randint(1, 5)
        len_b = random.randint(1, len_a)
        digits = "0123456789ABCDEF"
        num_a = [random.choice(digits) for _ in range(len_a)]
        num_b = [random.choice(digits) for _ in range(len_b)]

        start_a = 7 - len_a
        start_b = 7 - len_b

        for i, digit in enumerate(num_a):
            self._set_value(self.num1_row[start_a + i], digit)
        for i, digit in enumerate(num_b):
            self._set_value(self.num2_row[start_b + i], digit)

        self.how_to_steps.insert(tk.END, f"Generated sample:\nNum_1 = {''.join(num_a)}\nNum_2 = {''.join(num_b)}\n\n")

    # ----------------------------
    # Toggle Hex Reference
    # ----------------------------
    def toggle_hex_reference(self):
        if self.reference_visible:
            self.reference_frame.place_forget()
            self.reference_visible = False
        else:
            if not self.reference_frame:
                self.create_hex_reference_frame()
            self.reference_frame.place(x=910, y=210, width=170, height=450)
            self.reference_visible = True

    def create_hex_reference_frame(self):
        self.reference_frame = tk.Frame(self.root, bd=2, relief="groove", bg="#f9f9f9")
        tk.Label(self.reference_frame, text="Hex Reference", font=("Arial", 13, "bold"),
                 bg="#f9f9f9", fg="black").pack(pady=(10, 5))

        header = tk.Frame(self.reference_frame, bg="#dddddd")
        header.pack(fill="x", padx=10)
        tk.Label(header, text="Dec", font=("Arial", 11, "bold"),
                 bg="#dddddd", width=6).pack(side="left")
        tk.Label(header, text="Hex", font=("Arial", 11, "bold"),
                 bg="#dddddd", width=6).pack(side="left")

        for i in range(16):
            row_bg = "#ffffff" if i % 2 == 0 else "#f0f0f0"
            row = tk.Frame(self.reference_frame, bg=row_bg)
            row.pack(fill="x", padx=10)
            tk.Label(row, text=str(i), font=("Courier", 11),
                     width=6, anchor="center", bg=row_bg).pack(side="left")
            tk.Label(row, text=hex(i)[2:].upper(), font=("Courier", 11),
                     width=6, anchor="center", bg=row_bg).pack(side="left")

        # --- Logo below the frame (lower right corner) ---
        logo_img_raw = Image.open("software_nuggets.png")
        logo_img_raw = logo_img_raw.resize((100, 100), Image.LANCZOS)  # resize to 20x20
        self.logo_img = ImageTk.PhotoImage(logo_img_raw)

        logo_label = tk.Label(self.root, image=self.logo_img, bg="#f9f9f9", cursor="hand2")
        logo_label.place(x=1050, y=770, anchor="se")  # adjust coords for your window size
        logo_label.bind("<Button-1>", lambda e: webbrowser.open("https://www.youtube.com/watch?v=rF8eKBQNXDc"))


    # ----------------------------
    # Core Addition Logic
    # ----------------------------
    def step(self):
        self.align_inputs()

        if self.step_index < 0:
            self.reset_backgrounds()
            messagebox.showinfo("Done", "All digits have been added.")
            return

        self.how_to_steps.delete("1.0", tk.END)
        
        num1 = self.get_values(self.num1_row)
        num2 = self.get_values(self.num2_row)
        carry_in_str = self.carry_row[self.step_index].get()
        carry_in = int(carry_in_str, 16) if carry_in_str else 0

        num1_str = self.num1_row[self.step_index].get().strip()
        num2_str = self.num2_row[self.step_index].get().strip()
        carry_in_str = self.carry_row[self.step_index].get().strip()

        if num1_str == "" and num2_str == "" and carry_in_str == "":
            self.reset_backgrounds()
            messagebox.showinfo("Done", "All digits have been added.")
            return
    
        total = num1[self.step_index] + num2[self.step_index] + carry_in
        carry_out = total // 16
        digit = total % 16

        self.highlight_cells(self.step_index)

        # Update result row
        self._set_readonly_value(self.result_row[self.step_index], hex(digit)[2:])
        # Update carry row
        if self.step_index - 1 >= 0:
            carry_text = hex(carry_out)[2:] if carry_out > 0 else ""
            self._set_readonly_value(self.carry_row[self.step_index - 1], carry_text)
        else:
            if carry_out > 0:
                self.how_to_steps.insert(tk.END, f"Overflow: carry {hex(carry_out)[2:].upper()} past leftmost digit.\n")

        # Update Add Base 10 row
        self._set_readonly_value(self.add_base10_row[self.step_index], 
                                f"{num1[self.step_index]}+{num2[self.step_index]}+{carry_in}={total}")

        # Update Test Carry row
        carry_text = f"{total}>=16? {'Y' if total >= 16 else 'N'}"
        self._set_readonly_value(self.test_carry_row[self.step_index], carry_text)

        step_no = 7 - self.step_index
        step_text = self.build_step_text(step_no, self.step_index,
                                         num1[self.step_index], num2[self.step_index],
                                         carry_in, total, carry_out, digit)

        self.step_button.config(text=f"Process Step {step_no}")
        
        self.how_to_steps.insert(tk.END, step_text)
        self.step_index -= 1

    def build_step_text(self, step_no, idx, a_val, b_val, carry_in, total, carry_out, digit):
        a_hex = hex(a_val)[2:].upper()
        b_hex = hex(b_val)[2:].upper()
        carry_in_hex = hex(carry_in)[2:].upper() if carry_in else "0"
        digit_hex = hex(digit)[2:].upper()
        col_num = 7 - idx
        remainder = total % 16

        line1a = f"Add column [{col_num}] of hexadecimal number: {a_hex} + {b_hex}\n\n"
        line1a += f"1. Write the two hex digits and the carry on a piece of paper.\n"
        line1a += f"    Num_1 = {a_hex}\n"
        line1a += f"    Num_2 = {b_hex}\n"
        line1a += f"    Carry = {carry_in_hex}   (if the carry box is blank, treat it as 0)\n\n"

        line2a = f"2. Change each hex digit to a decimal number using the Hex Reference box\n"
        line2a += f"    Num_1 = {a_hex} (hex) → {a_val} (decimal)\n"
        line2a += f"    Num_2 = {b_hex} (hex) → {b_val} (decimal)\n\n"

        line3a = f"3. Add the two decimal numbers and the carry (see Add Base 10 row)\n"
        line3a += f"    {a_val} + {b_val} + {carry_in} = {total} (decimal total)\n\n"

        line4a = f"4. Decide whether a carry is necessary (see Test Carry row)\n"
        if total < 16:
            line4a += f"    The decimal total for this column = {total}\n"
            line4a += f"    No carry for this column, set next Carry Column[{col_num+1}] to Zero or Blank\n\n"
        else:
            line4a += f"    The decimal total for this column = {total}\n"
            line4a += f"    Is the decimal total ({total} >= 16)? Yes\n"
            line4a += f"    Subtract the Decimal Total {total} - 16 = Remainder {remainder}\n"
            line4a += f"    We HAVE TO carry 1 to the next Carry Column[{col_num+1}]\n\n"

        line5a = f"5. Convert the decimal result (the remainder) back to hex and write it in the SUM cell\n"
        line5a += f"    Decimal {remainder} maps to hex {digit_hex}\n"
        line5a += f"    So write {digit_hex} in the SUM cell for this column\n\n"

        line6a = f"6. Result for this column: SUM = {digit_hex}\n"
        if total >= 16:
            line6a += f"    We have to carry 1 to the Carry Column[{col_num+1}]\n\n"
             
        return line1a + line2a + line3a + line4a + line5a + line6a

    def highlight_cells(self, idx):
        self.reset_backgrounds()
        self.num1_row[idx].config(bg="lightyellow")
        self.num2_row[idx].config(bg="lightyellow")
        self.result_row[idx].config(bg="lightyellow")
        self.add_base10_row[idx].config(bg="lightyellow")
        self.test_carry_row[idx].config(bg="lightyellow")
        if idx > 0:
            self.carry_row[idx - 1].config(bg="lightyellow")

    def reset_backgrounds(self):
        for row in [self.num1_row, self.num2_row, self.result_row, self.carry_row, self.add_base10_row, self.test_carry_row]:
            for i, box in enumerate(row):
                if row in [self.num1_row, self.num2_row] and i == 0:
                    box.config(readonlybackground="lightgray")
                else:
                    box.config(bg="white")

    def clear_results(self):
        for row in [self.result_row, self.carry_row, self.add_base10_row, self.test_carry_row]:
            for box in row:
                box.config(state="normal")
                box.delete(0, tk.END)
                box.config(state="readonly")

    def clear_all(self):
        for row in [self.num1_row, self.num2_row, self.result_row, self.carry_row, self.add_base10_row, self.test_carry_row]:
            for i, box in enumerate(row):
                box.config(state="normal")
                box.delete(0, tk.END)
                if row in [self.result_row, self.carry_row, self.add_base10_row, self.test_carry_row]:
                    box.config(state="readonly")
                elif row in [self.num1_row, self.num2_row] and i == 0:
                    box.config(state="readonly", readonlybackground="lightgray")
                else:
                    box.config(state="normal", bg="white")
        self.step_index = 6
        self.how_to_steps.delete("1.0", tk.END)
        self.how_to_steps.insert(tk.END, "Step-by-step execution will be displayed here.\n")
        self.reset_backgrounds()
        self.step_button.config(text="Enter a Problem or press Generate Sample")

if __name__ == "__main__":
    root = tk.Tk()
    app = HexAdderApp(root)
    root.mainloop()
