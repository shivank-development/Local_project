import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
import random
import json
import pyperclip

# ---------- Main Application Class ----------
class ConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("All-in-One Unit Converter & RGB Color Toolkit")
        self.geometry("850x550")
        self.resizable(False, False)
        self.configure(bg="#f0f0f0")

        # Tabs: Unit Converter and RGB Color
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, expand=True)

        self.unitConverterTab = UnitConverterTab(self.notebook)
        self.rgbColorTab = RGBColorTab(self.notebook)

        self.notebook.add(self.unitConverterTab, text="Unit Converter")
        self.notebook.add(self.rgbColorTab, text="RGB Color Toolkit")

# ---------- Unit Converter Tab ----------
class UnitConverterTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f8f8f8")
        self.categories = {
            "Length": ["Meter", "Kilometer", "Feet", "Mile"],
            "Weight": ["Gram", "Kilogram", "Pound", "Ounce"],
            "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
            "Time": ["Second", "Minute", "Hour"]
        }
        self.conversion_history = []

        # Dropdown for category
        tk.Label(self, text="Category:", bg="#f8f8f8", font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.category_var = tk.StringVar(value="Length")
        self.category_menu = ttk.Combobox(self, textvariable=self.category_var, values=list(self.categories.keys()), state="readonly")
        self.category_menu.grid(row=0, column=1)
        self.category_menu.bind("<<ComboboxSelected>>", self.update_units)

        # Units selection
        tk.Label(self, text="From:", bg="#f8f8f8", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=10)
        self.from_unit_var = tk.StringVar(value="Meter")
        self.from_unit_menu = ttk.Combobox(self, textvariable=self.from_unit_var, state="readonly")
        self.from_unit_menu.grid(row=1, column=1)

        tk.Label(self, text="To:", bg="#f8f8f8", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=10)
        self.to_unit_var = tk.StringVar(value="Kilometer")
        self.to_unit_menu = ttk.Combobox(self, textvariable=self.to_unit_var, state="readonly")
        self.to_unit_menu.grid(row=2, column=1)

        self.update_units()

        # Entry for value
        tk.Label(self, text="Value:", bg="#f8f8f8", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=10)
        self.value_entry = tk.Entry(self, width=10)
        self.value_entry.grid(row=3, column=1)

        # Convert button
        self.convert_btn = tk.Button(self, text="Convert", command=self.convert, bg="#4caf50", fg="white", width=12)
        self.convert_btn.grid(row=4, column=1, pady=10)

        # Output label
        self.output_label = tk.Label(self, text="", bg="#f8f8f8", font=("Arial", 14, "bold"))
        self.output_label.grid(row=5, column=0, columnspan=2, pady=10)

        # History section
        self.history_label = tk.Label(self, text="Conversion History", bg="#f8f8f8", font=("Arial", 10, "underline"))
        self.history_label.grid(row=6, column=0, sticky="w", padx=10)

        self.history_listbox = tk.Listbox(self, height=10, width=45)
        self.history_listbox.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

    def update_units(self, event=None):
        units = self.categories[self.category_var.get()]
        self.from_unit_menu.config(values=units)
        self.to_unit_menu.config(values=units)
        self.from_unit_var.set(units[0])
        self.to_unit_var.set(units[1])

    def convert(self):
        try:
            value = float(self.value_entry.get())
            from_unit = self.from_unit_var.get()
            to_unit = self.to_unit_var.get()
            category = self.category_var.get()

            converted_value = self.unit_conversion(value, from_unit, to_unit, category)
            result = f"{value} {from_unit} = {converted_value:.4f} {to_unit}"

            self.output_label.config(text=result)
            self.conversion_history.append(result)
            self.history_listbox.insert(0, result)

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")

    def unit_conversion(self, value, from_unit, to_unit, category):
        if category == "Length":
            factors = {"Meter": 1, "Kilometer": 1000, "Feet": 0.3048, "Mile": 1609.34}
        elif category == "Weight":
            factors = {"Gram": 1, "Kilogram": 1000, "Pound": 453.592, "Ounce": 28.3495}
        elif category == "Temperature":
            return self.convert_temperature(value, from_unit, to_unit)
        elif category == "Time":
            factors = {"Second": 1, "Minute": 60, "Hour": 3600}

        return value * (factors[from_unit] / factors[to_unit])

    @staticmethod
    def convert_temperature(value, from_unit, to_unit):
        if from_unit == "Celsius":
            if to_unit == "Fahrenheit": return (value * 9 / 5) + 32
            if to_unit == "Kelvin": return value + 273.15
        elif from_unit == "Fahrenheit":
            if to_unit == "Celsius": return (value - 32) * 5 / 9
            if to_unit == "Kelvin": return (value - 32) * 5 / 9 + 273.15
        elif from_unit == "Kelvin":
            if to_unit == "Celsius": return value - 273.15
            if to_unit == "Fahrenheit": return (value - 273.15) * 9 / 5 + 32
        return value

# ---------- RGB Color Toolkit ----------
class RGBColorTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f8f8f8")
        self.palette = []

        self.create_rgb_sliders()
        self.create_color_preview()
        self.create_palette_section()

    def create_rgb_sliders(self):
        self.red = tk.IntVar(value=128)
        self.green = tk.IntVar(value=128)
        self.blue = tk.IntVar(value=128)

        # Red Slider
        tk.Label(self, text="R:", bg="#f8f8f8").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.red_slider = tk.Scale(self, from_=0, to=255, orient='horizontal', variable=self.red, command=self.update_color)
        self.red_slider.grid(row=0, column=1)

        # Green Slider
        tk.Label(self, text="G:", bg="#f8f8f8").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.green_slider = tk.Scale(self, from_=0, to=255, orient='horizontal', variable=self.green, command=self.update_color)
        self.green_slider.grid(row=1, column=1)

        # Blue Slider
        tk.Label(self, text="B:", bg="#f8f8f8").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.blue_slider = tk.Scale(self, from_=0, to=255, orient='horizontal', variable=self.blue, command=self.update_color)
        self.blue_slider.grid(row=2, column=1)

        # Hex value
        tk.Label(self, text="HEX:", bg="#f8f8f8").grid(row=3, column=0, padx=10)
        self.hex_entry = tk.Entry(self, width=10)
        self.hex_entry.grid(row=3, column=1)
        self.hex_entry.bind("<KeyRelease>", self.update_from_hex)

        # Copy HEX or RGB
        self.copy_rgb_btn = tk.Button(self, text="Copy RGB", command=lambda: self.copy_to_clipboard(self.get_rgb()), bg="#1976d2", fg="white", width=10)
        self.copy_rgb_btn.grid(row=0, column=2, padx=10)
        self.copy_hex_btn = tk.Button(self, text="Copy HEX", command=lambda: self.copy_to_clipboard(self.hex_entry.get()), bg="#1976d2", fg="white", width=10)
        self.copy_hex_btn.grid(row=1, column=2, padx=10)

        # Random Color Button
        self.random_btn = tk.Button(self, text="Random", command=self.random_color, bg="#e65100", fg="white", width=10)
        self.random_btn.grid(row=2, column=2, padx=10)

        # Save to palette
        self.save_palette_btn = tk.Button(self, text="Save Color", command=self.save_color, bg="#4caf50", fg="white", width=10)
        self.save_palette_btn.grid(row=3, column=2, padx=10)

    def create_color_preview(self):
        self.color_preview = tk.Label(self, text="Color Preview", bg=self.get_hex(), width=20, height=10, relief="sunken")
        self.color_preview.grid(row=4, column=0, columnspan=3, pady=10)

    def create_palette_section(self):
        tk.Label(self, text="Palette", bg="#f8f8f8", font=("Arial", 12, "bold")).grid(row=5, column=0, pady=10)
        self.palette_frame = tk.Frame(self, bg="#f8f8f8")
        self.palette_frame.grid(row=6, column=0, columnspan=3)

    def update_color(self, event=None):
        hex_value = self.get_hex()
        self.color_preview.config(bg=hex_value)
        self.hex_entry.delete(0, tk.END)
        self.hex_entry.insert(0, hex_value)

    def update_from_hex(self, event=None):
        hex_value = self.hex_entry.get()
        if len(hex_value) == 7 and hex_value.startswith("#"):
            try:
                r = int(hex_value[1:3], 16)
                g = int(hex_value[3:5], 16)
                b = int(hex_value[5:], 16)
                self.red.set(r)
                self.green.set(g)
                self.blue.set(b)
                self.update_color()
            except ValueError:
                pass

    def random_color(self):
        self.red.set(random.randint(0, 255))
        self.green.set(random.randint(0, 255))
        self.blue.set(random.randint(0, 255))
        self.update_color()

    def save_color(self):
        hex_value = self.get_hex()
        self.palette.append(hex_value)
        color_label = tk.Label(self.palette_frame, text=hex_value, bg=hex_value, width=10, relief="raised", cursor="hand2")
        color_label.pack(side="left", padx=5, pady=5)
        color_label.bind("<Button-1>", lambda e: self.load_color(hex_value))

    def load_color(self, hex_value):
        self.hex_entry.delete(0, tk.END)
        self.hex_entry.insert(0, hex_value)
        self.update_from_hex()

    def copy_to_clipboard(self, content):
        pyperclip.copy(content)
        messagebox.showinfo("Copied", f"Copied to clipboard: {content}")

    def get_rgb(self):
        return f"rgb({self.red.get()}, {self.green.get()}, {self.blue.get()})"

    def get_hex(self):
        return f"#{self.red.get():02x}{self.green.get():02x}{self.blue.get():02x}"


# ---------- Launch App ----------
if __name__ == "__main__":
    app = ConverterApp()
    app.mainloop()
