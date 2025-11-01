import tkinter as tk
from tkinter import ttk
from math import pi
import time

# Calculate BMI
def calculate_bmi(weight, height):
    return weight / (height ** 2)

# Get BMI category
def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

# Main GUI app
class BMIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Age/BMI Checker")
        self.root.geometry("400x600")
        self.root.configure(bg="#1e1e2f")
        
        # Title with glowing font
        self.title_label = tk.Label(root, text="BMI & Age Checker", font=("Helvetica", 20, "bold"), fg="#00ffaa", bg="#1e1e2f")
        self.title_label.pack(pady=20)

        # Inputs (with glowing border)
        self.create_input_field("Age (years):", "age")
        self.create_input_field("Weight (kg):", "weight")
        self.create_input_field("Height (m):", "height")

        # Submit button with animation
        self.submit_btn = tk.Button(root, text="Calculate BMI", font=("Arial", 14, "bold"), bg="#00ffaa", fg="#1e1e2f",
                                    padx=20, pady=10, command=self.on_submit)
        self.submit_btn.pack(pady=20)
        self.animate_button(self.submit_btn)

        # Output label
        self.result_label = tk.Label(root, text="", font=("Helvetica", 12), fg="#fff", bg="#1e1e2f")
        self.result_label.pack(pady=10)

        # Circular progress (BMI level)
        self.canvas = tk.Canvas(root, width=200, height=200, bg="#1e1e2f", highlightthickness=0)
        self.canvas.pack()
        self.progress = 0
        self.arc = None

    def create_input_field(self, label, field_name):
        frame = tk.Frame(self.root, bg="#28293d", bd=2, relief="solid")
        frame.pack(pady=10, padx=20, fill='x')
        frame.bind("<Enter>", lambda e, frame=frame: self.glow(frame))
        frame.bind("<Leave>", lambda e, frame=frame: self.un_glow(frame))
        
        tk.Label(frame, text=label, font=("Arial", 12), bg="#28293d", fg="#00ffaa").pack(anchor='w', padx=10, pady=5)
        entry = tk.Entry(frame, font=("Arial", 14), bg="#2f3044", fg="white", bd=0, insertbackground="white")
        entry.pack(fill='x', padx=10, pady=5)
        
        setattr(self, f"{field_name}_entry", entry)

    def glow(self, frame):
        frame.config(bg="#00ffaa")

    def un_glow(self, frame):
        frame.config(bg="#28293d")

    def animate_button(self, widget):
        def pulse():
            current_color = widget.cget("bg")
            new_color = "#00ffcc" if current_color == "#00ffaa" else "#00ffaa"
            widget.config(bg=new_color)
            widget.after(700, pulse)
        pulse()

    def animate_progress(self, bmi):
        angle = (bmi / 40) * 360  # BMI from 0-40 mapped to 0-360
        if self.arc:
            self.canvas.delete(self.arc)
        self.arc = self.canvas.create_arc(10, 10, 190, 190, start=90, extent=0, style="arc", outline="#00ffaa", width=15)
        
        for i in range(int(angle), -1, -5):
            self.canvas.itemconfig(self.arc, extent=i)
            self.root.update()
            time.sleep(0.01)

    def on_submit(self):
        try:
            age = int(self.age_entry.get())
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            bmi = calculate_bmi(weight, height)
            category = get_bmi_category(bmi)

            message = f"BMI: {bmi:.2f}\nCategory: {category}"
            if age < 18:
                message += "\nNote: BMI may not apply to under 18."
            elif age > 65:
                message += "\nCaution: BMI less accurate for seniors."

            self.result_label.config(text=message)
            self.animate_progress(bmi)
        except ValueError:
            self.result_label.config(text="⚠️ Please enter valid numeric inputs.")

# Run app
if __name__ == "__main__":
    root = tk.Tk()
    app = BMIApp(root)
    root.mainloop()
