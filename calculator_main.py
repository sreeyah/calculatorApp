import tkinter as tk
import math
import cmath
import sympy as sp
from tkinter import *
from tkinter import ttk,messagebox
from datetime import datetime
from dateutil.relativedelta import relativedelta
import cmath
import numpy as np
from numpy.linalg import inv, det, eig
from sympy import symbols, Eq, solve, expand, factor,diff, integrate, sin, cos, lambdify, sympify
from scipy.integrate import quad,dblquad
from scipy import stats
import time
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.special import gamma, beta, erf
import os
from scipy.stats import norm, t, chi2, f

# Create the main window
root = tk.Tk()
root.title("Calculator")

# Global variables
current_input = ""
current_mode = "Standard"
operation_pending = None
base_value = None  # To store the base value for the power operation

operation_pending = None
first_value = None




def clear_entry():
    entry.delete(0, tk.END)
# Function to handle button click events

def button_click(value):
    entry.insert(tk.END, value)

# Function to evaluate the expression


def evaluate():
    global first_value, operation_pending
    try:
        expression = entry.get()
        if operation_pending:
            # Handling power operation separately
            if operation_pending == 'power':
                result = float(first_value) ** float(expression)
                entry.delete(0, tk.END)
                entry.insert(tk.END, str(result))
                add_to_history(f"{first_value} ^ {expression}", result)
                operation_pending = None
                return
        
        result = str(eval(expression))  # Evaluates the expression
        entry.delete(0, tk.END)
        entry.insert(tk.END, result)
        add_to_history(expression, result)
    except Exception as e:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")



# Function to remove the last character

def backspace():
    entry.delete(len(entry.get())-1, tk.END)


def scientific_operation(operation):
    global first_value, operation_pending
    try:
        current_input = entry.get()
        if operation == '1/x':
            result = 1 / float(current_input)
        elif operation == 'x!':
            result = math.factorial(int(current_input))
        elif operation == 'sqrt':
            result = math.sqrt(float(current_input))
        elif operation == 'sin':
            result = math.sin(math.radians(float(current_input)))
        elif operation == 'cos':
            result = math.cos(math.radians(float(current_input)))
        elif operation == 'tan':
            result = math.tan(math.radians(float(current_input)))
        elif operation == 'log':
            result = math.log10(float(current_input))
        elif operation == 'ln':
            result = math.log(float(current_input))
        elif operation == 'exp':
            result = math.exp(float(current_input))

        
        elif operation == '^':
            # Handle power operation
            first_value = current_input
            operation_pending = 'power'
            entry.delete(0, tk.END)
            return
        
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
        add_to_history(f"{operation}({current_input})", result)
       
    except Exception as e:
        clear_entry()
        entry.insert(tk.END, "Error")

# Function to add expressions and results to history
def add_to_history(expression, result):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("history.txt", "a") as file:
        file.write(f"[{timestamp}] {expression} = {result}\n")

def show_history():
    history_window = tk.Toplevel(root)
    history_window.title("Calculation History")

    history_text = tk.Text(history_window, wrap=tk.WORD, font=('Arial', 14))
    history_text.pack(expand=True, fill='both')

    try:
        with open("history.txt", "r") as file:
            history_content = file.read()
        history_text.insert(tk.END, history_content)
    except FileNotFoundError:
        history_text.insert(tk.END, "No history available.")

def clear_history_button():
    if os.path.exists("history.txt"):
        os.remove("history.txt")
    messagebox.showinfo("History Cleared", "Calculation history has been cleared.")

def init_standard_mode():
    clear_window()
    entry.grid(row=0, column=0, columnspan=4)
    
    buttons =  [
        ('7', 1, 0), ('8', 1, 1),('9', 1, 2), ('(', 1, 3), (')', 1, 4), ('/', 1, 5),
        ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3), ('-', 2, 4), ('%', 2, 5),
        ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3), ('0', 3, 4), ('.', 3, 5),
        ('CE', 4, 0), ('=', 4, 1), ('Back', 4, 2)
    ]
      

    for text, row, col in buttons:
        if text == '=':
            button = tk.Button(root, text=text, width=5, height=2, font=('Arial', 18),
                               borderwidth=0, relief="solid", bg='#4CAF50', fg='white', command=evaluate)
        elif text == 'CE':
            button = tk.Button(root, text=text, width=5, height=2, font=('Arial', 18),
                               borderwidth=0, relief="solid", command=clear_entry)
        elif text == 'Back':
            button = tk.Button(root, text=text, width=5, height=2, font=('Arial', 18),
                               borderwidth=0, relief="solid", command=backspace)
        elif text == '(':
            button = tk.Button(root, text=text, width=5, height=2, font=('Arial', 18),
                               borderwidth=0, relief="solid", command=lambda: add_parenthesis('('))
        elif text == ')':
            button = tk.Button(root, text=text, width=5, height=2, font=('Arial', 18),
                               borderwidth=0, relief="solid", command=lambda: add_parenthesis(')'))
        elif text == '%':
            button = tk.Button(root, text=text, width=5, height=2, font=('Arial', 18),
                               borderwidth=0, relief="solid", command=lambda: button_click('%'))
        else:
            button = tk.Button(root, text=text, width=5, height=2, font=('Arial', 18),
                               borderwidth=0, relief="solid", command=lambda t=text: button_click(t))
        button.grid(row=row, column=col, padx=1, pady=1)

def init_scientific_mode():
    clear_window()
    entry.grid(row=0, column=0, columnspan=7)
    
    buttons = [
        ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('(', 1, 3), (')', 1, 4), ('/', 1, 5), ('sin', 1, 6),
        ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3), ('-', 2, 4), ('cos', 2, 5), ('x!', 2, 6),
        ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3), ('0', 3, 4), ('.', 3, 5), ('tan', 3, 6),
        ('CE', 4, 0), ('=', 4, 2), ('Back', 4, 3), ('log', 4, 4), ('ln', 4, 5),
        ('1/x', 5, 0), ('sqrt', 5, 1), ('exp', 5, 2), ('^', 5, 3)
    ]

    for text, row, col in buttons:
        if text in ('sin', 'cos', 'tan', 'log', 'ln', 'sqrt', 'exp', '1/x', 'x!', '^'):
            button = tk.Button(root, text=text, width=5, height=2, font=('Arial', 18),
                               borderwidth=0, relief="solid", command=lambda t=text: scientific_operation(t))
        elif text == '=':
            button = tk.Button(root, text=text, width=5, height=2, font=('Arial', 18),
                               borderwidth=0, relief="solid", bg='#4CAF50', fg='white', command=evaluate)
        elif text == 'CE':
            button = tk.Button(root, text=text, width=5, height=2, font=('Arial', 18),
                               borderwidth=0, relief="solid", command=clear_entry)
        elif text == 'Back':
            button = tk.Button(root, text=text, width=5, height=2, font=('Arial', 18),
                               borderwidth=0, relief="solid", command=backspace)
        elif text == '(':
            button = tk.Button(root, text=text, width=5, height=2, font=('Arial', 18),
                               borderwidth=0, relief="solid", command=lambda: add_parenthesis('('))
        elif text == ')':
            button = tk.Button(root, text=text, width=5, height=2, font=('Arial', 18),
                               borderwidth=0, relief="solid", command=lambda: add_parenthesis(')'))
        else:
            button = tk.Button(root, text=text, width=5, height=2, font=('Arial', 18),
                               borderwidth=0, relief="solid", command=lambda t=text: button_click(t))
        button.grid(row=row, column=col, padx=1, pady=1)

def clear_history():
    if os.path.exists("history.txt"):
        os.remove("history.txt")




def add_parenthesis(parenthesis):
    entry.insert(tk.END, parenthesis)

# Function to solve equations and find roots
def solve_equation():
    global current_input
    try:
        x = sp.symbols('x')
        equation = sp.sympify(current_input)
        solutions = sp.solve(equation, x)
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(solutions))
    except Exception as e:
        clear_entry()
        entry.insert(tk.END, "Error")

# Function to change modes
def change_mode(mode):
    global current_mode
    current_mode = mode
    clear_entry()
    entry.grid_forget()
    for widget in root.grid_slaves():
        widget.grid_forget()
    if mode == "Standard":
        init_standard_mode()
    elif mode == "Scientific":
        init_scientific_mode()
    elif mode == "Angle":
        init_angle_mode(root)
    elif mode=='Temperature':
        init_temperature_mode(root)
    elif mode=='Programming':
        init_prog_mode(root)
    elif mode=='Speed':
        init_speed_mode(root)
    elif mode=='Power':
        init_power_mode(root)
    elif mode=='Pressure':
        init_pressure_mode(root)
    elif mode=='Time':
        init_time_mode(root)
    elif mode=='Area':
        init_area_mode(root)
    elif mode=='Energy':
        init_energy_mode(root)
    elif mode == 'Weight and Mass':
        init_weight_mass_mode(root)
    elif mode=='Length':
        init_length_mode(root)
    elif mode=='Volume':
        init_volume_mode(root)
    elif mode=='Date Difference':
        init_date_calculation_mode(root)
    elif mode=='ComplexNumbers':
        init_complex_mode(root)
    elif mode=='Matrices and vectors':
        init_matrices_vectors_mode(root)
    elif mode=='Algebra':
        init_algebra_mode(root)
    elif mode=='Calculus':
        init_calculus_mode(root)
    elif mode=='Statistics and Probability':
        init_statistics_probability_mode(root)
    elif mode=='Financial':
        init_financial_calculations_mode(root)
    elif mode=='Data analysis and manipulation':
        init_data_analysis_manip_mode(root)
    elif mode=='Math consts and funcs':
        init_mathematical_constants_functions(root)
    elif mode=='Engineering and Scientific':
        init_scientific_engineering_mode(root)
    elif mode=='Currency':
        init_currency_mode(root)
    elif mode=='Statistics and Probability table':
        init_prob_stat_table_mode()
    elif mode == 'History':
          show_history()

    root.title(f"Calculator - {mode}")

# Function to initialize standard mode buttons


def clear_window():
    for widget in root.winfo_children():
        widget.pack_forget()
# Function to initialize angle mode buttons
def init_angle_mode(root):
    clear_window()
    """Initialize the angle conversion mode interface."""
    
    conversion_factors = {
        'Degrees (°)': 1,
        'Radians (rad)': 57.2958,
        'Gradians (gon)': 0.9
    }

    def convert_angle(value, from_unit, to_unit):
        value = float(value)
        if from_unit == to_unit:
            return value
        value_in_degrees = value * conversion_factors[from_unit]
        return value_in_degrees / conversion_factors[to_unit]

    def update_conversion():
        try:
            value = angle_input.get()
            from_unit = from_unit_var.get()
            to_unit = to_unit_var.get()
            result = convert_angle(value, from_unit, to_unit)
            result_label.config(text=f"Converted Angle: {result:.4f} {to_unit}")
        except ValueError:
            result_label.config(text="Invalid input. Please enter a valid number.")

    angle_frame = ttk.Frame(root, padding="10")
    angle_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(angle_frame, text="Input Angle:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    global angle_input
    angle_input = ttk.Entry(angle_frame, width=15)
    angle_input.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(angle_frame, text="From Unit:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    global from_unit_var
    from_unit_var = tk.StringVar(value='Degrees (°)')
    from_unit_menu = ttk.Combobox(angle_frame, textvariable=from_unit_var, values=list(conversion_factors.keys()), state='readonly')
    from_unit_menu.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(angle_frame, text="To Unit:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
    global to_unit_var
    to_unit_var = tk.StringVar(value='Radians (rad)')
    to_unit_menu = ttk.Combobox(angle_frame, textvariable=to_unit_var, values=list(conversion_factors.keys()), state='readonly')
    to_unit_menu.grid(row=2, column=1, padx=5, pady=5)

    convert_button = ttk.Button(angle_frame, text="Convert", command=update_conversion)
    convert_button.grid(row=3, column=0, columnspan=2, pady=10)

    global result_label
    result_label = ttk.Label(angle_frame, text="Converted Angle: ")
    result_label.grid(row=4, column=0, columnspan=2, pady=5)

def init_temperature_mode(root):
    clear_window() 
    """Initialize the temperature conversion mode interface."""
    
    def convert_temperature(value, from_unit, to_unit):
        value = float(value)
        if from_unit == to_unit:
            return value
        
        if from_unit == 'Celsius (°C)':
            if to_unit == 'Fahrenheit (°F)':
                return (value * 9/5) + 32
            elif to_unit == 'Kelvin (K)':
                return value + 273.15
        
        if from_unit == 'Fahrenheit (°F)':
            if to_unit == 'Celsius (°C)':
                return (value - 32) * 5/9
            elif to_unit == 'Kelvin (K)':
                return (value - 32) * 5/9 + 273.15
        
        if from_unit == 'Kelvin (K)':
            if to_unit == 'Celsius (°C)':
                return value - 273.15
            elif to_unit == 'Fahrenheit (°F)':
                return (value - 273.15) * 9/5 + 32

    def update_conversion():
        try:
            value = temperature_input.get()
            from_unit = from_unit_var.get()
            to_unit = to_unit_var.get()
            result = convert_temperature(value, from_unit, to_unit)
            result_label.config(text=f"Converted Temperature: {result:.2f} {to_unit}")
        except ValueError:
            result_label.config(text="Invalid input. Please enter a valid number.")

    temperature_frame = ttk.Frame(root, padding="10")
    temperature_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(temperature_frame, text="Input Temperature:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    global temperature_input
    temperature_input = ttk.Entry(temperature_frame, width=15)
    temperature_input.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(temperature_frame, text="From Unit:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    global from_unit_var
    from_unit_var = tk.StringVar(value='Celsius (°C)')
    from_unit_menu = ttk.Combobox(temperature_frame, textvariable=from_unit_var, values=['Celsius (°C)', 'Fahrenheit (°F)', 'Kelvin (K)'], state='readonly')
    from_unit_menu.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(temperature_frame, text="To Unit:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
    global to_unit_var
    to_unit_var = tk.StringVar(value='Fahrenheit (°F)')
    to_unit_menu = ttk.Combobox(temperature_frame, textvariable=to_unit_var, values=['Celsius (°C)', 'Fahrenheit (°F)', 'Kelvin (K)'], state='readonly')
    to_unit_menu.grid(row=2, column=1, padx=5, pady=5)

    convert_button = ttk.Button(temperature_frame, text="Convert", command=update_conversion)
    convert_button.grid(row=3, column=0, columnspan=2, pady=10)

    global result_label
    result_label = ttk.Label(temperature_frame, text="Converted Temperature: ")
    result_label.grid(row=4, column=0, columnspan=2, pady=5)


# Function to initialize prog mode buttons
def init_prog_mode(root):
    clear_window()
    """Initialize the programming mode interface."""

    def convert_prog(prog_unit):
        try:
            temp_value = int(entry.get(), 0)  # Automatically handles 0x (hex), 0o (oct), and 0b (bin)
            if prog_unit == 'hexa':
                result = hex(temp_value)[2:].upper()
            elif prog_unit == 'dec':
                result = str(temp_value)
            elif prog_unit == 'oct':
                result = oct(temp_value)[2:]
            elif prog_unit == 'bin':
                result = bin(temp_value)[2:]
            else:
                result = "Select a valid unit"

            entry.delete(0, tk.END)
            entry.insert(tk.END, result)
        except ValueError:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")

    def clear_entry():
        entry.delete(0, tk.END)

    def backspace():
        entry.delete(len(entry.get()) - 1)

    def button_click(value):
        entry.insert(tk.END, value)

    prog_frame = ttk.Frame(root, padding="10")
    prog_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    global entry
    entry = ttk.Entry(prog_frame, width=30, font=('Arial', 18))
    entry.grid(row=0, column=0, columnspan=5)

    buttons = [
        ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('CE', 1, 3),
        ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('BACK', 2, 3),
        ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('0', 3, 3),
        ('Hexa', 4, 0), ('Dec', 4, 1), ('Oct', 4, 2), ('Bin', 4, 3)
    ]

    for (text, row, col) in buttons:
        if text in ('Hexa', 'Dec', 'Oct', 'Bin'):
            button = ttk.Button(prog_frame, text=text, command=lambda t=text: convert_prog(t.lower()))
        elif text == 'CE':
            button = ttk.Button(prog_frame, text=text, command=clear_entry)
        elif text == 'BACK':
            button = ttk.Button(prog_frame, text=text, command=backspace)
        else:
            button = ttk.Button(prog_frame, text=text, command=lambda t=text: button_click(t))

        button.grid(row=row, column=col, padx=5, pady=5, sticky=tk.W + tk.E + tk.N + tk.S)

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)


# Function to initialize speed mode buttons
def init_speed_mode(root):
    clear_window()
    """Initialize the speed conversion mode interface."""
    
    conversion_factors = {
        'Meters per second (m/s)': 1,
        'Kilometers per hour (km/h)': 0.277778,
        'Miles per hour (mph)': 0.44704,
        'Feet per second (ft/s)': 0.3048,
        'Knots (kn)': 0.514444
    }

    def convert_speed(value, from_unit, to_unit):
        value = float(value)
        if from_unit == to_unit:
            return value
        value_in_mps = value * conversion_factors[from_unit]
        return value_in_mps / conversion_factors[to_unit]

    def update_conversion():
        try:
            value = speed_input.get()
            from_unit = from_unit_var.get()
            to_unit = to_unit_var.get()
            result = convert_speed(value, from_unit, to_unit)
            result_label.config(text=f"Converted Speed: {result:.4f} {to_unit}")
        except ValueError:
            result_label.config(text="Invalid input. Please enter a valid number.")

    speed_frame = ttk.Frame(root, padding="10")
    speed_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(speed_frame, text="Input Speed:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    global speed_input
    speed_input = ttk.Entry(speed_frame, width=15)
    speed_input.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(speed_frame, text="From Unit:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    global from_unit_var
    from_unit_var = tk.StringVar(value='Meters per second (m/s)')
    from_unit_menu = ttk.Combobox(speed_frame, textvariable=from_unit_var, values=list(conversion_factors.keys()), state='readonly')
    from_unit_menu.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(speed_frame, text="To Unit:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
    global to_unit_var
    to_unit_var = tk.StringVar(value='Kilometers per hour (km/h)')
    to_unit_menu = ttk.Combobox(speed_frame, textvariable=to_unit_var, values=list(conversion_factors.keys()), state='readonly')
    to_unit_menu.grid(row=2, column=1, padx=5, pady=5)

    convert_button = ttk.Button(speed_frame, text="Convert", command=update_conversion)
    convert_button.grid(row=3, column=0, columnspan=2, pady=10)

    global result_label
    result_label = ttk.Label(speed_frame, text="Converted Speed: ")
    result_label.grid(row=4, column=0, columnspan=2, pady=5)

def init_power_mode(root):
    clear_window()
    """Initialize the power conversion mode interface."""
    
    conversion_factors = {
        'Watts (W)': 1,
        'Kilowatts (kW)': 1000,
        'Horsepower (hp)': 745.7,
        'British Thermal Units per hour (BTU/h)': 0.293071,
        'Calories per second (cal/s)': 4.184
    }

    def convert_power(value, from_unit, to_unit):
        value = float(value)
        if from_unit == to_unit:
            return value
        value_in_watts = value * conversion_factors[from_unit]
        return value_in_watts / conversion_factors[to_unit]

    def update_conversion():
        try:
            value = power_input.get()
            from_unit = from_unit_var.get()
            to_unit = to_unit_var.get()
            result = convert_power(value, from_unit, to_unit)
            result_label.config(text=f"Converted Power: {result:.4f} {to_unit}")
        except ValueError:
            result_label.config(text="Invalid input. Please enter a valid number.")

    power_frame = ttk.Frame(root, padding="10")
    power_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(power_frame, text="Input Power:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    global power_input
    power_input = ttk.Entry(power_frame, width=15)
    power_input.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(power_frame, text="From Unit:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    global from_unit_var
    from_unit_var = tk.StringVar(value='Watts (W)')
    from_unit_menu = ttk.Combobox(power_frame, textvariable=from_unit_var, values=list(conversion_factors.keys()), state='readonly')
    from_unit_menu.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(power_frame, text="To Unit:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
    global to_unit_var
    to_unit_var = tk.StringVar(value='Kilowatts (kW)')
    to_unit_menu = ttk.Combobox(power_frame, textvariable=to_unit_var, values=list(conversion_factors.keys()), state='readonly')
    to_unit_menu.grid(row=2, column=1, padx=5, pady=5)

    convert_button = ttk.Button(power_frame, text="Convert", command=update_conversion)
    convert_button.grid(row=3, column=0, columnspan=2, pady=10)

    global result_label
    result_label = ttk.Label(power_frame, text="Converted Power: ")
    result_label.grid(row=4, column=0, columnspan=2, pady=5)

def init_pressure_mode(root):
    clear_window()
    """Initialize the pressure conversion mode interface."""
    
    conversion_factors = {
        'Pascals (Pa)': 1,
        'Kilopascals (kPa)': 1000,
        'Bars': 1e5,
        'Atmospheres (atm)': 101325,
        'Pounds per square inch (psi)': 6894.76,
        'Torr': 133.322
    }

    def convert_pressure(value, from_unit, to_unit):
        value = float(value)
        if from_unit == to_unit:
            return value
        value_in_pa = value * conversion_factors[from_unit]
        return value_in_pa / conversion_factors[to_unit]

    def update_conversion():
        try:
            value = pressure_input.get()
            from_unit = from_unit_var.get()
            to_unit = to_unit_var.get()
            result = convert_pressure(value, from_unit, to_unit)
            result_label.config(text=f"Converted Pressure: {result:.4f} {to_unit}")
        except ValueError:
            result_label.config(text="Invalid input. Please enter a valid number.")

    pressure_frame = ttk.Frame(root, padding="10")
    pressure_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(pressure_frame, text="Input Pressure:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    global pressure_input
    pressure_input = ttk.Entry(pressure_frame, width=15)
    pressure_input.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(pressure_frame, text="From Unit:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    global from_unit_var
    from_unit_var = tk.StringVar(value='Pascals (Pa)')
    from_unit_menu = ttk.Combobox(pressure_frame, textvariable=from_unit_var, values=list(conversion_factors.keys()), state='readonly')
    from_unit_menu.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(pressure_frame, text="To Unit:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
    global to_unit_var
    to_unit_var = tk.StringVar(value='Kilopascals (kPa)')
    to_unit_menu = ttk.Combobox(pressure_frame, textvariable=to_unit_var, values=list(conversion_factors.keys()), state='readonly')
    to_unit_menu.grid(row=2, column=1, padx=5, pady=5)

    convert_button = ttk.Button(pressure_frame, text="Convert", command=update_conversion)
    convert_button.grid(row=3, column=0, columnspan=2, pady=10)

    global result_label
    result_label = ttk.Label(pressure_frame, text="Converted Pressure: ")
    result_label.grid(row=4, column=0, columnspan=2, pady=5)

def init_time_mode(root):
    clear_window()
    """Initialize the time conversion mode interface."""
    
    conversion_factors = {
        'Seconds (s)': 1,
        'Minutes (min)': 60,
        'Hours (h)': 3600,
        'Days (d)': 86400,
        'Weeks (wk)': 604800,
        'Months (mo)': 2.628e6,  # assuming 30.44 days in a month
        'Years (yr)': 3.154e7
    }

    def convert_time(value, from_unit, to_unit):
        value = float(value)
        if from_unit == to_unit:
            return value
        value_in_seconds = value * conversion_factors[from_unit]
        return value_in_seconds / conversion_factors[to_unit]

    def update_conversion():
        try:
            value = time_input.get()
            from_unit = from_unit_var.get()
            to_unit = to_unit_var.get()
            result = convert_time(value, from_unit, to_unit)
            result_label.config(text=f"Converted Time: {result:.4f} {to_unit}")
        except ValueError:
            result_label.config(text="Invalid input. Please enter a valid number.")

    time_frame = ttk.Frame(root, padding="10")
    time_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(time_frame, text="Input Time:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    global time_input
    time_input = ttk.Entry(time_frame, width=15)
    time_input.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(time_frame, text="From Unit:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    global from_unit_var
    from_unit_var = tk.StringVar(value='Seconds (s)')
    from_unit_menu = ttk.Combobox(time_frame, textvariable=from_unit_var, values=list(conversion_factors.keys()), state='readonly')
    from_unit_menu.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(time_frame, text="To Unit:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
    global to_unit_var
    to_unit_var = tk.StringVar(value='Minutes (min)')
    to_unit_menu = ttk.Combobox(time_frame, textvariable=to_unit_var, values=list(conversion_factors.keys()), state='readonly')
    to_unit_menu.grid(row=2, column=1, padx=5, pady=5)

    convert_button = ttk.Button(time_frame, text="Convert", command=update_conversion)
    convert_button.grid(row=3, column=0, columnspan=2, pady=10)

    global result_label
    result_label = ttk.Label(time_frame, text="Converted Time: ")
    result_label.grid(row=4, column=0, columnspan=2, pady=5)

def init_area_mode(root):
    clear_window()
    """Initialize the area conversion mode interface."""
    
    conversion_factors = {
        'Square Meters (m²)': 1,
        'Square Kilometers (km²)': 1e6,
        'Square Centimeters (cm²)': 1e-4,
        'Square Millimeters (mm²)': 1e-6,
        'Hectares (ha)': 1e4,
        'Square Miles (mi²)': 2.59e6,
        'Acres': 4046.86,
        'Square Yards (yd²)': 0.836127,
        'Square Feet (ft²)': 0.092903,
        'Square Inches (in²)': 6.4516e-4
    }

    def convert_area(value, from_unit, to_unit):
        value = float(value)
        if from_unit == to_unit:
            return value
        value_in_sqm = value * conversion_factors[from_unit]
        return value_in_sqm / conversion_factors[to_unit]

    def update_conversion():
        try:
            value = area_input.get()
            from_unit = from_unit_var.get()
            to_unit = to_unit_var.get()
            result = convert_area(value, from_unit, to_unit)
            result_label.config(text=f"Converted Area: {result:.4f} {to_unit}")
        except ValueError:
            result_label.config(text="Invalid input. Please enter a valid number.")

    area_frame = ttk.Frame(root, padding="10")
    area_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(area_frame, text="Input Area:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    global area_input
    area_input = ttk.Entry(area_frame, width=15)
    area_input.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(area_frame, text="From Unit:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    global from_unit_var
    from_unit_var = tk.StringVar(value='Square Meters (m²)')
    from_unit_menu = ttk.Combobox(area_frame, textvariable=from_unit_var, values=list(conversion_factors.keys()), state='readonly')
    from_unit_menu.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(area_frame, text="To Unit:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
    global to_unit_var
    to_unit_var = tk.StringVar(value='Square Kilometers (km²)')
    to_unit_menu = ttk.Combobox(area_frame, textvariable=to_unit_var, values=list(conversion_factors.keys()), state='readonly')
    to_unit_menu.grid(row=2, column=1, padx=5, pady=5)

    convert_button = ttk.Button(area_frame, text="Convert", command=update_conversion)
    convert_button.grid(row=3, column=0, columnspan=2, pady=10)

    global result_label
    result_label = ttk.Label(area_frame, text="Converted Area: ")
    result_label.grid(row=4, column=0, columnspan=2, pady=5)

def init_energy_mode(root):
    clear_window()
    """Initialize the energy conversion mode interface."""
    
    conversion_factors = {
        'Joules (J)': 1,
        'Kilojoules (kJ)': 1000,
        'Calories (cal)': 4.184,
        'Kilocalories (kcal)': 4184,
        'Watt-hours (Wh)': 3600,
        'Kilowatt-hours (kWh)': 3.6e6,
        'British Thermal Units (BTU)': 1055.06,
        'Foot-pounds (ft-lb)': 1.35582
    }

    def convert_energy(value, from_unit, to_unit):
        value = float(value)
        if from_unit == to_unit:
            return value
        value_in_joules = value * conversion_factors[from_unit]
        return value_in_joules / conversion_factors[to_unit]

    def update_conversion():
        try:
            value = energy_input.get()
            from_unit = from_unit_var.get()
            to_unit = to_unit_var.get()
            result = convert_energy(value, from_unit, to_unit)
            result_label.config(text=f"Converted Energy: {result:.4f} {to_unit}")
        except ValueError:
            result_label.config(text="Invalid input. Please enter a valid number.")

    energy_frame = ttk.Frame(root, padding="10")
    energy_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(energy_frame, text="Input Energy:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    global energy_input
    energy_input = ttk.Entry(energy_frame, width=15)
    energy_input.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(energy_frame, text="From Unit:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    global from_unit_var
    from_unit_var = tk.StringVar(value='Joules (J)')
    from_unit_menu = ttk.Combobox(energy_frame, textvariable=from_unit_var, values=list(conversion_factors.keys()), state='readonly')
    from_unit_menu.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(energy_frame, text="To Unit:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
    global to_unit_var
    to_unit_var = tk.StringVar(value='Kilojoules (kJ)')
    to_unit_menu = ttk.Combobox(energy_frame, textvariable=to_unit_var, values=list(conversion_factors.keys()), state='readonly')
    to_unit_menu.grid(row=2, column=1, padx=5, pady=5)

    convert_button = ttk.Button(energy_frame, text="Convert", command=update_conversion)
    convert_button.grid(row=3, column=0, columnspan=2, pady=10)

    global result_label
    result_label = ttk.Label(energy_frame, text="Converted Energy: ")
    result_label.grid(row=4, column=0, columnspan=2, pady=5)

def init_weight_mass_mode(root):
    clear_window()
    """Initialize the weight and mass conversion mode interface."""
    
    conversion_factors = {
        'Carats (ct)': 0.0002,
        'Milligrams (mg)': 1e-6,
        'Centigrams (cg)': 1e-5,
        'Decigrams (dg)': 1e-4,
        'Grams (g)': 0.001,
        'Decagrams (dag)': 0.01,
        'Hectograms (hg)': 0.1,
        'Kilograms (kg)': 1,
        'Metric Tons (t)': 1000,
        'Ounces (oz)': 0.0283495,
        'Pounds (lb)': 0.453592,
        'Stones (st)': 6.35029,
        'Short Tons (US)': 907.185
    }

    def convert_weight_mass(value, from_unit, to_unit):
        value = float(value)
        if from_unit == to_unit:
            return value
        value_in_kg = value * conversion_factors[from_unit]
        return value_in_kg / conversion_factors[to_unit]

    def update_conversion():
        try:
            value = weight_input.get()
            from_unit = from_unit_var.get()
            to_unit = to_unit_var.get()
            result = convert_weight_mass(value, from_unit, to_unit)
            result_label.config(text=f"Converted Weight: {result:.4f} {to_unit}")
        except ValueError:
            result_label.config(text="Invalid input. Please enter a valid number.")

    weight_frame = ttk.Frame(root, padding="10")
    weight_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(weight_frame, text="Input Weight:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    global weight_input
    weight_input = ttk.Entry(weight_frame, width=15)
    weight_input.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(weight_frame, text="From Unit:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    global from_unit_var
    from_unit_var = tk.StringVar(value='Grams (g)')
    from_unit_menu = ttk.Combobox(weight_frame, textvariable=from_unit_var, values=list(conversion_factors.keys()), state='readonly')
    from_unit_menu.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(weight_frame, text="To Unit:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
    global to_unit_var
    to_unit_var = tk.StringVar(value='Kilograms (kg)')
    to_unit_menu = ttk.Combobox(weight_frame, textvariable=to_unit_var, values=list(conversion_factors.keys()), state='readonly')
    to_unit_menu.grid(row=2, column=1, padx=5, pady=5)

    convert_button = ttk.Button(weight_frame, text="Convert", command=update_conversion)
    convert_button.grid(row=3, column=0, columnspan=2, pady=10)

    global result_label
    result_label = ttk.Label(weight_frame, text="Converted Weight: ")
    result_label.grid(row=4, column=0, columnspan=2, pady=5)

def init_length_mode(root):
    clear_window()
    """Initialize the length conversion mode interface."""
    
    conversion_factors = {
        'Millimeters (mm)': 1e-3,
        'Centimeters (cm)': 1e-2,
        'Meters (m)': 1,
        'Kilometers (km)': 1e3,
        'Inches (in)': 0.0254,
        'Feet (ft)': 0.3048,
        'Yards (yd)': 0.9144,
        'Miles (mi)': 1609.34,
        'Nautical Miles (nmi)': 1852
    }

    def convert_length(value, from_unit, to_unit):
        value = float(value)
        if from_unit == to_unit:
            return value
        value_in_meters = value * conversion_factors[from_unit]
        return value_in_meters / conversion_factors[to_unit]

    def update_conversion():
        try:
            value = length_input.get()
            from_unit = from_unit_var.get()
            to_unit = to_unit_var.get()
            result = convert_length(value, from_unit, to_unit)
            result_label.config(text=f"Converted Length: {result:.4f} {to_unit}")
        except ValueError:
            result_label.config(text="Invalid input. Please enter a valid number.")

    length_frame = ttk.Frame(root, padding="10")
    length_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(length_frame, text="Input Length:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    global length_input
    length_input = ttk.Entry(length_frame, width=15)
    length_input.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(length_frame, text="From Unit:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    global from_unit_var
    from_unit_var = tk.StringVar(value='Meters (m)')
    from_unit_menu = ttk.Combobox(length_frame, textvariable=from_unit_var, values=list(conversion_factors.keys()), state='readonly')
    from_unit_menu.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(length_frame, text="To Unit:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
    global to_unit_var
    to_unit_var = tk.StringVar(value='Kilometers (km)')
    to_unit_menu = ttk.Combobox(length_frame, textvariable=to_unit_var, values=list(conversion_factors.keys()), state='readonly')
    to_unit_menu.grid(row=2, column=1, padx=5, pady=5)

    convert_button = ttk.Button(length_frame, text="Convert", command=update_conversion)
    convert_button.grid(row=3, column=0, columnspan=2, pady=10)

    global result_label
    result_label = ttk.Label(length_frame, text="Converted Length: ")
    result_label.grid(row=4, column=0, columnspan=2, pady=5)

def init_volume_mode(root):
    clear_window()
    """Initialize the volume conversion mode interface."""
    
    conversion_factors = {
        'Milliliters (mL)': 1e-6,
        'Liters (L)': 1e-3,
        'Cubic Meters (m³)': 1,
        'Cubic Centimeters (cm³)': 1e-6,
        'Gallons (US)': 3.78541e-3,
        'Gallons (UK)': 4.54609e-3,
        'Quarts (US)': 9.46353e-4,
        'Quarts (UK)': 1.13652e-3,
        'Pints (US)': 4.73177e-4,
        'Pints (UK)': 5.68261e-4,
        'Fluid Ounces (US)': 2.95735e-5,
        'Fluid Ounces (UK)': 2.84131e-5,
        'Cubic Inches': 1.63871e-5,
        'Cubic Feet': 0.0283168,
        'Barrels': 0.158987
    }

    def convert_volume(value, from_unit, to_unit):
        value = float(value)
        if from_unit == to_unit:
            return value
        value_in_m3 = value * conversion_factors[from_unit]
        return value_in_m3 / conversion_factors[to_unit]

    def update_conversion():
        try:
            value = volume_input.get()
            from_unit = from_unit_var.get()
            to_unit = to_unit_var.get()
            result = convert_volume(value, from_unit, to_unit)
            result_label.config(text=f"Converted Volume: {result:.4f} {to_unit}")
        except ValueError:
            result_label.config(text="Invalid input. Please enter a valid number.")

    volume_frame = ttk.Frame(root, padding="10")
    volume_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(volume_frame, text="Input Volume:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    global volume_input
    volume_input = ttk.Entry(volume_frame, width=15)
    volume_input.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(volume_frame, text="From Unit:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    global from_unit_var
    from_unit_var = tk.StringVar(value='Milliliters (mL)')
    from_unit_menu = ttk.Combobox(volume_frame, textvariable=from_unit_var, values=list(conversion_factors.keys()), state='readonly')
    from_unit_menu.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(volume_frame, text="To Unit:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
    global to_unit_var
    to_unit_var = tk.StringVar(value='Liters (L)')
    to_unit_menu = ttk.Combobox(volume_frame, textvariable=to_unit_var, values=list(conversion_factors.keys()), state='readonly')
    to_unit_menu.grid(row=2, column=1, padx=5, pady=5)

    convert_button = ttk.Button(volume_frame, text="Convert", command=update_conversion)
    convert_button.grid(row=3, column=0, columnspan=2, pady=10)

    global result_label
    result_label = ttk.Label(volume_frame, text="Converted Volume: ")
    result_label.grid(row=4, column=0, columnspan=2, pady=5)

import cmath


def init_complex_mode(root):
    clear_window()
    """Initialize the complex numbers mode interface."""
    
    def perform_complex_operation():
        """Perform operations with complex numbers including arithmetic and conversions."""
        try:
            operation = operation_var.get()
            
            if operation in ['Addition', 'Subtraction', 'Multiplication', 'Division']:
                real1 = float(real1_entry.get())
                imag1 = float(imag1_entry.get())
                real2 = float(real2_entry.get())
                imag2 = float(imag2_entry.get())
                
                complex1 = complex(real1, imag1)
                complex2 = complex(real2, imag2)
                
                if operation == 'Addition':
                    result = complex1 + complex2
                elif operation == 'Subtraction':
                    result = complex1 - complex2
                elif operation == 'Multiplication':
                    result = complex1 * complex2
                elif operation == 'Division':
                    result = complex1 / complex2
                
                result_label.config(text=f"Result: {result.real:.4f} + {result.imag:.4f}j")
            
            elif operation == 'Cartesian to Polar':
                real = float(real1_entry.get())
                imag = float(imag1_entry.get())
                result = cmath.polar(complex(real, imag))
                result_label.config(text=f"Polar Coordinates: (r={result[0]:.4f}, θ={cmath.phase(result[1]):.4f} radians)")
            
            elif operation == 'Polar to Cartesian':
                r = float(real1_entry.get())
                theta = float(imag1_entry.get())
                result = cmath.rect(r, theta)
                result_label.config(text=f"Cartesian Coordinates: (x={result.real:.4f}, y={result.imag:.4f})")
                
        except ValueError:
            result_label.config(text="Invalid input. Please enter valid numbers.")
        except ZeroDivisionError:
            result_label.config(text="Error: Division by zero.")

    # Frame for complex operations
    complex_frame = ttk.Frame(root, padding="10")
    complex_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    # Input fields for the first complex number or Cartesian coordinates
    ttk.Label(complex_frame, text="Real Part / r:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    global real1_entry
    real1_entry = ttk.Entry(complex_frame, width=15)
    real1_entry.grid(row=0, column=1, padx=5, pady=5)
    
    ttk.Label(complex_frame, text="Imaginary Part / θ (radians):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    global imag1_entry
    imag1_entry = ttk.Entry(complex_frame, width=15)
    imag1_entry.grid(row=1, column=1, padx=5, pady=5)
    
    # Input fields for the second complex number (for arithmetic operations)
    ttk.Label(complex_frame, text="Second Real Part:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
    global real2_entry
    real2_entry = ttk.Entry(complex_frame, width=15)
    real2_entry.grid(row=2, column=1, padx=5, pady=5)
    
    ttk.Label(complex_frame, text="Second Imaginary Part:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
    global imag2_entry
    imag2_entry = ttk.Entry(complex_frame, width=15)
    imag2_entry.grid(row=3, column=1, padx=5, pady=5)
    
    # Operation selection
    ttk.Label(complex_frame, text="Operation:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
    global operation_var
    operation_var = tk.StringVar(value='Addition')
    operation_menu = ttk.Combobox(complex_frame, textvariable=operation_var, values=['Addition', 'Subtraction', 'Multiplication', 'Division', 'Cartesian to Polar', 'Polar to Cartesian'], state='readonly')
    operation_menu.grid(row=4, column=1, padx=5, pady=5)
    
    # Calculate button
    calculate_button = ttk.Button(complex_frame, text="Calculate", command=perform_complex_operation)
    calculate_button.grid(row=5, column=0, columnspan=2, pady=10)
    
    # Result label
    global result_label
    result_label = ttk.Label(complex_frame, text="Result: ")
    result_label.grid(row=6, column=0, columnspan=2, pady=5)


from datetime import datetime
from dateutil.relativedelta import relativedelta
import tkinter as tk

def init_date_calculation_mode(root):
    clear_window()
    root.title("Calculator - Date Calculation")

    # Entry boxes for user input
    date1_entry = tk.Entry(root, width=20, borderwidth=5)
    date1_entry.grid(row=1, column=0, padx=10, pady=10)
    date1_entry.insert(0, "dd-mm-yyyy")  # Placeholder text

    date2_entry = tk.Entry(root, width=20, borderwidth=5)
    date2_entry.grid(row=1, column=1, padx=10, pady=10)
    date2_entry.insert(0, "dd-mm-yyyy")  # Placeholder text

    # Result label
    result_label = tk.Label(root, text="", font=("Arial", 14))
    result_label.grid(row=2, column=0, columnspan=2, pady=10)

    def calculate_date_difference():
        try:
            date_format = "%d-%m-%Y"
            date1 = datetime.strptime(date1_entry.get(), date_format)
            date2 = datetime.strptime(date2_entry.get(), date_format)

            # Calculate the difference using relativedelta
            if date2 > date1:
                delta = relativedelta(date2, date1)
            else:
                delta = relativedelta(date1, date2)

            years = delta.years
            months = delta.months
            days = delta.days
            weeks = days // 7  # Number of complete weeks
            remaining_days = days % 7  # Days left after complete weeks

            # Display the result
            result_label.config(
                text=f"Difference: {years} years, {months} months, {weeks} week(s), {remaining_days} day(s)"
            )
        except ValueError:
            result_label.config(text="Error: Invalid Date Format")

    # Calculate button
    calculate_button = tk.Button(root, text="Calculate", command=calculate_date_difference)
    calculate_button.grid(row=3, column=0, columnspan=2, pady=10)



def init_matrices_vectors_mode(root):
    clear_window()
    """Initialize the matrices and vectors mode interface."""

    def create_matrix_input(frame, rows, cols, matrix_var, label):
        """Create matrix input fields in the given frame."""
        for i in range(rows):
            for j in range(cols):
                ttk.Label(frame, text=f"({i+1},{j+1}):").grid(row=i, column=j*2, padx=5, pady=5)
                entry = ttk.Entry(frame, width=10)
                entry.grid(row=i, column=j*2+1, padx=5, pady=5)
                matrix_var[i][j] = entry

    def get_matrix_from_entries(entries, rows, cols):
        """Retrieve matrix data from entry widgets."""
        matrix = []
        for i in range(rows):
            row = []
            for j in range(cols):
                try:
                    value = float(entries[i][j].get())
                except ValueError:
                    value = 0
                row.append(value)
            matrix.append(row)
        return np.array(matrix)

    def perform_operation():
        """Perform the selected matrix/vector operation."""
        try:
            operation = operation_var.get()
            rows1 = int(rows1_entry.get())
            cols1 = int(cols1_entry.get())
            rows2 = int(rows2_entry.get())
            cols2 = int(cols2_entry.get())
            
            matrix1 = get_matrix_from_entries(matrix1_entries, rows1, cols1)
            matrix2 = get_matrix_from_entries(matrix2_entries, rows2, cols2)
            
            if operation == "Add Matrices":
                if rows1 == rows2 and cols1 == cols2:
                    result = matrix1 + matrix2
                else:
                    result = "Matrices must be of the same dimensions."
            elif operation == "Multiply Matrices":
                if cols1 == rows2:
                    result = np.dot(matrix1, matrix2)
                else:
                    result = "Matrix dimensions do not match for multiplication."
            elif operation == "Invert Matrix":
                if rows1 == cols1:
                    result = inv(matrix1)
                else:
                    result = "Matrix must be square for inversion."
            elif operation == "Determinant":
                if rows1 == cols1:
                    result = det(matrix1)
                else:
                    result = "Matrix must be square for determinant."
            elif operation == "Eigenvalues and Eigenvectors":
                if rows1 == cols1:
                    eigenvalues, eigenvectors = eig(matrix1)
                    result = f"Eigenvalues:\n{eigenvalues}\nEigenvectors:\n{eigenvectors}"
                else:
                    result = "Matrix must be square for eigenvalues and eigenvectors."
            else:
                result = "Select a valid operation."
            
            result_label.config(text=f"Result:\n{result}")
        except Exception as e:
            result_label.config(text=f"Error: {e}")

    # Frame for matrices and vectors
    matrices_vectors_frame = ttk.Frame(root, padding="10")
    matrices_vectors_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    # Operation selection
    ttk.Label(matrices_vectors_frame, text="Select Operation:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    global operation_var
    operation_var = tk.StringVar(value="Add Matrices")
    operation_menu = ttk.Combobox(matrices_vectors_frame, textvariable=operation_var,
                                 values=["Add Matrices", "Multiply Matrices", "Invert Matrix", "Determinant", "Eigenvalues and Eigenvectors"],
                                 state='readonly')
    operation_menu.grid(row=0, column=1, padx=5, pady=5)
    
    # Matrix 1 dimensions
    ttk.Label(matrices_vectors_frame, text="Matrix 1 - Rows:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    global rows1_entry
    rows1_entry = ttk.Entry(matrices_vectors_frame, width=10)
    rows1_entry.grid(row=1, column=1, padx=5, pady=5)
    
    ttk.Label(matrices_vectors_frame, text="Columns:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
    global cols1_entry
    cols1_entry = ttk.Entry(matrices_vectors_frame, width=10)
    cols1_entry.grid(row=1, column=3, padx=5, pady=5)
    
    # Matrix 2 dimensions
    ttk.Label(matrices_vectors_frame, text="Matrix 2 - Rows:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
    global rows2_entry
    rows2_entry = ttk.Entry(matrices_vectors_frame, width=10)
    rows2_entry.grid(row=2, column=1, padx=5, pady=5)
    
    ttk.Label(matrices_vectors_frame, text="Columns:").grid(row=2, column=2, sticky=tk.W, padx=5, pady=5)
    global cols2_entry
    cols2_entry = ttk.Entry(matrices_vectors_frame, width=10)
    cols2_entry.grid(row=2, column=3, padx=5, pady=5)
    
    # Matrix 1 input fields
    ttk.Label(matrices_vectors_frame, text="Matrix 1 Entries:").grid(row=3, column=0, columnspan=4, sticky=tk.W, padx=5, pady=5)
    global matrix1_entries
    matrix1_entries = [[None for _ in range(10)] for _ in range(10)]  # Max 10x10 matrix
    matrix1_frame = ttk.Frame(matrices_vectors_frame)
    matrix1_frame.grid(row=4, column=0, columnspan=4)
    matrix1_entries_frame = matrix1_frame
    
    # Matrix 2 input fields
    ttk.Label(matrices_vectors_frame, text="Matrix 2 Entries:").grid(row=5, column=0, columnspan=4, sticky=tk.W, padx=5, pady=5)
    global matrix2_entries
    matrix2_entries = [[None for _ in range(10)] for _ in range(10)]  # Max 10x10 matrix
    matrix2_frame = ttk.Frame(matrices_vectors_frame)
    matrix2_frame.grid(row=6, column=0, columnspan=4)
    matrix2_entries_frame = matrix2_frame
    
    # Perform button
    perform_button = ttk.Button(matrices_vectors_frame, text="Perform", command=perform_operation)
    perform_button.grid(row=7, column=0, columnspan=4, pady=10)
    
    # Result label
    global result_label
    result_label = ttk.Label(matrices_vectors_frame, text="Result:")
    result_label.grid(row=8, column=0, columnspan=4, pady=5)
    
    # Update matrix input fields when dimensions change
    def update_matrix_inputs():
        """Update matrix input fields based on dimensions."""
        for widget in matrix1_entries_frame.winfo_children():
            widget.destroy()
        for widget in matrix2_entries_frame.winfo_children():
            widget.destroy()
        
        rows1 = int(rows1_entry.get())
        cols1 = int(cols1_entry.get())
        rows2 = int(rows2_entry.get())
        cols2 = int(cols2_entry.get())
        
        create_matrix_input(matrix1_entries_frame, rows1, cols1, matrix1_entries, "Matrix 1")
        create_matrix_input(matrix2_entries_frame, rows2, cols2, matrix2_entries, "Matrix 2")
    
    rows1_entry.bind("<FocusOut>", lambda e: update_matrix_inputs())
    cols1_entry.bind("<FocusOut>", lambda e: update_matrix_inputs())
    rows2_entry.bind("<FocusOut>", lambda e: update_matrix_inputs())
    cols2_entry.bind("<FocusOut>", lambda e: update_matrix_inputs())


def init_algebra_mode(root):
    clear_window()
    """Initialize the advanced algebra mode interface."""
    x = symbols('x') 
    y=symbols('y')  

    def find_polynomial_roots():
        """Find and display the roots of a polynomial."""
        try:
            poly_str = polynomial_input.get()
            poly = eval(poly_str)
            roots = solve(poly, x)
            roots_label.config(text=f"Roots: {roots}")
        except Exception as e:
            roots_label.config(text=f"Error: {str(e)}")

    def symbolic_algebra():
        """Perform symbolic algebra operations."""
        try:
            expr_str = expression_input.get()
            operation = operation_var.get()
            x, y = symbols('x y')
            expr = eval(expr_str)
            if operation == 'Expand':
                result = expand(expr)
            elif operation == 'Factor':
                result = factor(expr)
            else:
                result = "Invalid Operation"
            symbolic_label.config(text=f"Result: {result}")
        except Exception as e:
            symbolic_label.config(text=f"Error: {str(e)}")

    def solve_equations():
        """Solve a system of nonlinear equations."""
        try:
            eq1_str = eq1_input.get()
            eq2_str = eq2_input.get()
            x, y = symbols('x y')
            eq1 = eval(eq1_str)
            eq2 = eval(eq2_str)
            equations = [Eq(eq1, 0), Eq(eq2, 0)]
            solutions = solve(equations, (x, y))
            eq_solutions_label.config(text=f"Solutions: {solutions}")
        except Exception as e:
            eq_solutions_label.config(text=f"Error: {str(e)}")

    # Frame for advanced algebra
    algebra_frame = ttk.Frame(root, padding="10")
    algebra_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Polynomial root finder
    ttk.Label(algebra_frame, text="Polynomial (e.g., x**2 - 4*x + 4):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    global polynomial_input
    polynomial_input = ttk.Entry(algebra_frame, width=30)
    polynomial_input.grid(row=0, column=1, padx=5, pady=5)
    roots_button = ttk.Button(algebra_frame, text="Find Roots", command=find_polynomial_roots)
    roots_button.grid(row=1, column=0, columnspan=2, pady=10)
    global roots_label
    roots_label = ttk.Label(algebra_frame, text="Roots: ")
    roots_label.grid(row=2, column=0, columnspan=2, pady=5)

    # Symbolic algebra
    ttk.Label(algebra_frame, text="Expression (e.g., x**2 - 4*x + 4):").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
    global expression_input
    expression_input = ttk.Entry(algebra_frame, width=30)
    expression_input.grid(row=3, column=1, padx=5, pady=5)
    ttk.Label(algebra_frame, text="Operation:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
    global operation_var
    operation_var = tk.StringVar(value='Expand')
    operation_menu = ttk.Combobox(algebra_frame, textvariable=operation_var, values=['Expand', 'Factor'], state='readonly')
    operation_menu.grid(row=4, column=1, padx=5, pady=5)
    symbolic_button = ttk.Button(algebra_frame, text="Perform Operation", command=symbolic_algebra)
    symbolic_button.grid(row=5, column=0, columnspan=2, pady=10)
    global symbolic_label
    symbolic_label = ttk.Label(algebra_frame, text="Result: ")
    symbolic_label.grid(row=6, column=0, columnspan=2, pady=5)

    # Nonlinear equations solver
    ttk.Label(algebra_frame, text="Equation 1 (e.g., x**2 + y**2 - 1):").grid(row=7, column=0, sticky=tk.W, padx=5, pady=5)
    global eq1_input
    eq1_input = ttk.Entry(algebra_frame, width=30)
    eq1_input.grid(row=7, column=1, padx=5, pady=5)
    ttk.Label(algebra_frame, text="Equation 2 (e.g., x - y - 0.5):").grid(row=8, column=0, sticky=tk.W, padx=5, pady=5)
    global eq2_input
    eq2_input = ttk.Entry(algebra_frame, width=30)
    eq2_input.grid(row=8, column=1, padx=5, pady=5)
    solve_button = ttk.Button(algebra_frame, text="Solve Equations", command=solve_equations)
    solve_button.grid(row=9, column=0, columnspan=2, pady=10)
    global eq_solutions_label
    eq_solutions_label = ttk.Label(algebra_frame, text="Solutions: ")
    eq_solutions_label.grid(row=10, column=0, columnspan=2, pady=5)

def init_calculus_mode(root):
    clear_window()
    """Initialize the calculus mode interface."""
    
    # Define the variables
    global x, y
    x, y = symbols('x'), symbols('y')
    
    def symbolic_differentiation():
        """Perform symbolic differentiation."""
        try:
            expr_str = derivative_input.get()
            expr = eval(expr_str, {"x": x, "y": y})
            variable = differentiation_var.get()
            
            if variable == 'x':
                derivative = diff(expr, x)
            elif variable == 'y':
                derivative = diff(expr, y)
            else:
                result_label_diff.config(text="Error: Invalid variable for differentiation.")
                return
            
            result_label_diff.config(text=f"Derivative with respect to {variable}: {derivative}")
        except Exception as e:
            result_label_diff.config(text=f"Error: {str(e)}")
    
    def numerical_integration():
        """Perform numerical integration."""
        try:
            func_str = integral_input.get()
            variable_selected = variable.get()
            
            if variable_selected == 'x':
                func = lambda x: eval(func_str, {"x": x})
                a = float(lower_bound_x.get())
                b = float(upper_bound_x.get())
                result, _ = quad(func, a, b)
                result_label_int.config(text=f"Integral: {result:.4f}")
                
            elif variable_selected == 'y':
                func = lambda y: eval(func_str, {"y": y})
                a = float(lower_bound_y.get())
                b = float(upper_bound_y.get())
                result, _ = quad(func, a, b)
                result_label_int.config(text=f"Integral: {result:.4f}")
                
            elif variable_selected == 'both':
                func = lambda x, y: eval(func_str, {"x": x, "y": y})
                a = float(lower_bound_x.get())
                b = float(upper_bound_x.get())
                c = float(lower_bound_y.get())
                d = float(upper_bound_y.get())
                result, _ = dblquad(func, a, b, lambda x: c, lambda x: d)
                result_label_int.config(text=f"Integral: {result:.4f}")
                
        except Exception as e:
            result_label_int.config(text=f"Error: {str(e)}")

    # Frame for calculus
    calculus_frame = ttk.Frame(root, padding="10")
    calculus_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    # Variable selection for differentiation and integration
    ttk.Label(calculus_frame, text="Select Variable for Differentiation:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    global differentiation_var
    differentiation_var = tk.StringVar(value='x')
    var_menu_diff = ttk.Combobox(calculus_frame, textvariable=differentiation_var, values=['x', 'y'], state='readonly')
    var_menu_diff.grid(row=0, column=1, padx=5, pady=5)
    
    ttk.Label(calculus_frame, text="Select Variable for Integration:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    global variable
    variable = tk.StringVar(value='x')
    var_menu_int = ttk.Combobox(calculus_frame, textvariable=variable, values=['x', 'y', 'both'], state='readonly')
    var_menu_int.grid(row=1, column=1, padx=5, pady=5)
    
    # Symbolic differentiation
    ttk.Label(calculus_frame, text="Function for Differentiation:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
    global derivative_input
    derivative_input = ttk.Entry(calculus_frame, width=30)
    derivative_input.grid(row=2, column=1, padx=5, pady=5)
    
    diff_button = ttk.Button(calculus_frame, text="Differentiate", command=symbolic_differentiation)
    diff_button.grid(row=3, column=0, columnspan=2, pady=10)
    
    global result_label_diff
    result_label_diff = ttk.Label(calculus_frame, text="Derivative: ")
    result_label_diff.grid(row=4, column=0, columnspan=2, pady=5)
    
    # Numerical integration
    ttk.Label(calculus_frame, text="Function for Integration:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
    global integral_input
    integral_input = ttk.Entry(calculus_frame, width=30)
    integral_input.grid(row=5, column=1, padx=5, pady=5)
    
    ttk.Label(calculus_frame, text="Variable Bounds:").grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
    
    # Bounds for x
    ttk.Label(calculus_frame, text="Lower Bound x:").grid(row=7, column=0, sticky=tk.W, padx=5, pady=5)
    global lower_bound_x
    lower_bound_x = ttk.Entry(calculus_frame, width=15)
    lower_bound_x.grid(row=7, column=1, padx=5, pady=5)
    
    ttk.Label(calculus_frame, text="Upper Bound x:").grid(row=8, column=0, sticky=tk.W, padx=5, pady=5)
    global upper_bound_x
    upper_bound_x = ttk.Entry(calculus_frame, width=15)
    upper_bound_x.grid(row=8, column=1, padx=5, pady=5)
    
    # Bounds for y
    ttk.Label(calculus_frame, text="Lower Bound y:").grid(row=9, column=0, sticky=tk.W, padx=5, pady=5)
    global lower_bound_y
    lower_bound_y = ttk.Entry(calculus_frame, width=15)
    lower_bound_y.grid(row=9, column=1, padx=5, pady=5)
    
    ttk.Label(calculus_frame, text="Upper Bound y:").grid(row=10, column=0, sticky=tk.W, padx=5, pady=5)
    global upper_bound_y
    upper_bound_y = ttk.Entry(calculus_frame, width=15)
    upper_bound_y.grid(row=10, column=1, padx=5, pady=5)
    
    int_button = ttk.Button(calculus_frame, text="Integrate", command=numerical_integration)
    int_button.grid(row=11, column=0, columnspan=2, pady=10)
    
    global result_label_int
    result_label_int = ttk.Label(calculus_frame, text="Integral: ")
    result_label_int.grid(row=12, column=0, columnspan=2, pady=5)

def init_statistics_probability_mode(root):
    clear_window()
    root.title("Calculator - Statistics and Probability")

    # Entry box for user input (data points)
    data_entry = tk.Entry(root, width=50, borderwidth=5)
    data_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
    data_entry.insert(0, "Enter data points separated by commas")

    # Result label
    result_label = tk.Label(root, text="", font=("Arial", 14))
    result_label.grid(row=2, column=0, columnspan=2, pady=10)

    def calculate_statistics(data_entry, result_label):
    
      try:
        # Retrieve and process the input data
        data = list(map(float, data_entry.get().split(',')))

        # Statistical calculations
        mean = np.mean(data)
        median = np.median(data)

        # Mode calculation
        mode_result = stats.mode(data, keepdims=True)
        if mode_result.count[0] > 0:
            mode = mode_result.mode[0]
        else:
            mode = "N/A"  # No mode found

        variance = np.var(data)
        std_dev = np.std(data)

        # Display results
        result_label.config(
            text=(
                f"Mean: {mean}\n"
                f"Median: {median}\n"
                f"Mode: {mode}\n"
                f"Variance: {variance}\n"
                f"Standard Deviation: {std_dev}"
            )
        )
      except Exception as e:
        result_label.config(text=f"Error: {str(e)}")


    def calculate_probability_distribution():
      try:
        data = list(map(float, data_entry.get().split(',')))

        # Example: Calculate normal distribution
        mean = np.mean(data)
        std_dev = np.std(data)
        probabilities = stats.norm.pdf(data, mean, std_dev)

        result_label.config(
            text=f"Probability Distribution (Normal):\n{probabilities}"
        )
      except Exception as e:
        result_label.config(text=f"Error: {str(e)}")
    def perform_hypothesis_testing():
      try:
        data = list(map(float, data_entry.get().split(',')))

        # Example: Perform t-test against a population mean (e.g., 0)
        t_statistic, p_value = stats.ttest_1samp(data, 0)

        result_label.config(
            text=(
                f"Hypothesis Testing (t-test):\n"
                f"T-Statistic: {t_statistic}\n"
                f"P-Value: {p_value}"
            )
        )
      except Exception as e:
        result_label.config(text=f"Error: {str(e)}")

    def perform_regression_analysis():
      try:
        data = list(map(float, data_entry.get().split(',')))
        if len(data) % 2 != 0:
                raise ValueError("Please enter an equal number of x and y values for paired data.")
        if len(data) % 2 != 0:
            raise ValueError("Please enter an even number of values for paired data (x,y).")

        x = np.array(data[::2])  # Even-indexed elements
        y = np.array(data[1::2])  # Odd-indexed elements

        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

        result_label.config(
            text=(
                f"Regression Analysis:\n"
                f"Slope: {slope}\n"
                f"Intercept: {intercept}\n"
                f"R-Value: {r_value}\n"
                f"P-Value: {p_value}\n"
                f"Standard Error: {std_err}"
            )
        )
      except Exception as e:
        result_label.config(text=f"Error: {str(e)}")



    # Buttons for different operations
    stats_button = tk.Button(root, text="Calculate Statistics", command=lambda: calculate_statistics(data_entry, result_label))
    stats_button.grid(row=3, column=0, pady=10)

    prob_button = tk.Button(root, text="Probability Distribution", command=calculate_probability_distribution)
    prob_button.grid(row=3, column=1, pady=10)

    hypo_button = tk.Button(root, text="Hypothesis Testing", command=perform_hypothesis_testing)
    hypo_button.grid(row=4, column=0, pady=10)

    reg_button = tk.Button(root, text="Regression Analysis", command=perform_regression_analysis)
    reg_button.grid(row=4, column=1, pady=10)

def init_financial_calculations_mode(root):
    clear_window()
    root.title("Calculator - Financial Calculations")
    
    # Frame for Loan Calculations
    loan_frame = tk.LabelFrame(root, text="Loan Calculations", padx=10, pady=10)
    loan_frame.pack(padx=10, pady=10, fill="x")

    # Entry boxes for loan calculations
    principal_label = tk.Label(loan_frame, text="Principal ($):")
    principal_label.pack(side="left", padx=5)
    principal_entry = tk.Entry(loan_frame, width=20)
    principal_entry.pack(side="left", padx=5)

    rate_label = tk.Label(loan_frame, text="Annual Rate (%):")
    rate_label.pack(side="left", padx=5)
    rate_entry = tk.Entry(loan_frame, width=20)
    rate_entry.pack(side="left", padx=5)

    years_label = tk.Label(loan_frame, text="Years:")
    years_label.pack(side="left", padx=5)
    years_entry = tk.Entry(loan_frame, width=20)
    years_entry.pack(side="left", padx=5)

    # Result label for loan calculations
    loan_result_label = tk.Label(loan_frame, text="", font=("Arial", 12))
    loan_result_label.pack(pady=10)

    def calculate_loan():
        try:
            P = float(principal_entry.get())
            r = float(rate_entry.get()) / 100 / 12
            n = int(years_entry.get()) * 12

            # Calculate monthly payment
            M = P * r * pow(1 + r, n) / (pow(1 + r, n) - 1)
            total_payment = M * n
            total_interest = total_payment - P

            loan_result_label.config(
                text=f"Monthly Payment: ${M:.2f}\nTotal Payment: ${total_payment:.2f}\nTotal Interest: ${total_interest:.2f}"
            )
        except ValueError:
            loan_result_label.config(text="Error: Invalid Input")

    # Calculate button for loan calculations
    calculate_loan_button = tk.Button(loan_frame, text="Calculate Loan", command=calculate_loan)
    calculate_loan_button.pack(pady=10)

    # Frame for Financial Ratios
    ratio_frame = tk.LabelFrame(root, text="Financial Ratios", padx=10, pady=10)
    ratio_frame.pack(padx=10, pady=10, fill="x")

    # Entry boxes for financial ratios
    earnings_label = tk.Label(ratio_frame, text="Earnings ($):")
    earnings_label.pack(side="left", padx=5)
    earnings_entry = tk.Entry(ratio_frame, width=20)
    earnings_entry.pack(side="left", padx=5)

    assets_label = tk.Label(ratio_frame, text="Assets ($):")
    assets_label.pack(side="left", padx=5)
    assets_entry = tk.Entry(ratio_frame, width=20)
    assets_entry.pack(side="left", padx=5)

    liabilities_label = tk.Label(ratio_frame, text="Liabilities ($):")
    liabilities_label.pack(side="left", padx=5)
    liabilities_entry = tk.Entry(ratio_frame, width=20)
    liabilities_entry.pack(side="left", padx=5)

    # Result label for financial ratios
    ratio_result_label = tk.Label(ratio_frame, text="", font=("Arial", 12))
    ratio_result_label.pack(pady=10)

    def calculate_ratios():
        try:
            earnings = float(earnings_entry.get())
            assets = float(assets_entry.get())
            liabilities = float(liabilities_entry.get())

            # Calculate financial ratios
            if assets != 0:
                return_on_assets = earnings / assets
            else:
                return_on_assets = 0

            if liabilities != 0:
                debt_to_equity = liabilities / (assets - liabilities)
            else:
                debt_to_equity = 0

            ratio_result_label.config(
                text=f"Return on Assets: {return_on_assets:.2%}\nDebt to Equity Ratio: {debt_to_equity:.2f}"
            )
        except ValueError:
            ratio_result_label.config(text="Error: Invalid Input")

    # Calculate button for financial ratios
    calculate_ratios_button = tk.Button(ratio_frame, text="Calculate Ratios", command=calculate_ratios)
    calculate_ratios_button.pack(pady=10)

def init_data_analysis_manip_mode(root):
    clear_window()
    root.title("Data Analysis and Manipulation")

    # Frame for data import/export
    import_export_frame = tk.Frame(root)
    import_export_frame.pack(pady=10)

    def import_data():
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])
        if file_path:
            try:
                if file_path.endswith(".csv"):
                    global data
                    data = pd.read_csv(file_path)
                elif file_path.endswith(".xlsx"):
                    data = pd.read_excel(file_path)
                messagebox.showinfo("Success", "Data imported successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import data: {e}")

    def export_data():
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                global data
                data.to_csv(file_path, index=False)
                messagebox.showinfo("Success", "Data exported successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export data: {e}")

    import_button = tk.Button(import_export_frame, text="Import Data", command=import_data)
    import_button.pack(side=tk.LEFT, padx=5)

    export_button = tk.Button(import_export_frame, text="Export Data", command=export_data)
    export_button.pack(side=tk.LEFT, padx=5)

    # Frame for data visualization
    visualization_frame = tk.Frame(root)
    visualization_frame.pack(pady=10)

    def plot_data():
        try:
            if data is not None:
                fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
                data.plot(kind='scatter', x=data.columns[0], y=data.columns[1], ax=ax)
                ax.set_title('Scatter Plot')
                
                canvas = FigureCanvasTkAgg(fig, master=visualization_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            else:
                messagebox.showerror("Error", "No data to visualize")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to plot data: {e}")

    plot_button = tk.Button(visualization_frame, text="Plot Data", command=plot_data)
    plot_button.pack(padx=5)

    # Frame for data filtering and aggregation
    filter_agg_frame = tk.Frame(root)
    filter_agg_frame.pack(pady=10)

    def filter_and_aggregate():
        try:
            if data is not None:
                # Example: Filter data where the first column values are greater than 10
                filtered_data = data[data[data.columns[0]] > 10]

                # Example: Aggregate data by calculating the mean of the second column
                aggregated_data = filtered_data.groupby(data.columns[0]).mean()

                messagebox.showinfo("Success", f"Filtered and Aggregated Data:\n{aggregated_data}")
            else:
                messagebox.showerror("Error", "No data to process")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to filter and aggregate data: {e}")

    filter_agg_button = tk.Button(filter_agg_frame, text="Filter and Aggregate", command=filter_and_aggregate)
    filter_agg_button.pack(padx=5)  

def init_mathematical_constants_functions(root):
    clear_window()
    root.title("Mathematical Constants and Functions")

    # Frame for predefined constants
    constants_frame = tk.Frame(root)
    constants_frame.pack(pady=10)

    # Display constants
    def display_constants():
        pi = math.pi
        e = math.e
        result_label.config(
            text=f"π (Pi): {pi}\ne (Euler's Number): {e}"
        )

    constants_button = tk.Button(constants_frame, text="Show Constants", command=display_constants)
    constants_button.pack(padx=5)

    # Frame for advanced functions
    functions_frame = tk.Frame(root)
    functions_frame.pack(pady=10)

    # Entry boxes for advanced functions
    x_entry = tk.Entry(functions_frame, width=20, borderwidth=5)
    x_entry.grid(row=0, column=1, padx=10, pady=10)
    x_entry.insert(0, "x")

    y_entry = tk.Entry(functions_frame, width=20, borderwidth=5)
    y_entry.grid(row=1, column=1, padx=10, pady=10)
    y_entry.insert(0, "y")

    # Result label
    global result_label
    result_label = tk.Label(root, text="", font=("Arial", 14))
    result_label.pack(pady=10)

    def compute_functions():
        try:
            x = float(x_entry.get())
            y = float(y_entry.get())

            gamma_x = gamma(x)
            beta_xy = beta(x, y)
            erf_x = erf(x)

            result_label.config(
                text=(
                    f"Gamma({x}): {gamma_x}\n"
                    f"Beta({x}, {y}): {beta_xy}\n"
                    f"Error Function erf({x}): {erf_x}"
                )
            )
        except ValueError:
            result_label.config(text="Error: Invalid Input")

    compute_button = tk.Button(functions_frame, text="Compute Functions", command=compute_functions)
    compute_button.grid(row=2, column=0, columnspan=2, pady=10)  

def init_scientific_engineering_mode(root):
    clear_window()
    root.title("Scientific and Engineering Tools")

    # Frame for chemical calculations
    chemical_frame = tk.Frame(root)
    chemical_frame.pack(pady=10)

    # Chemical Calculations
    def calculate_chemical():
        try:
            # Stoichiometry calculation
            reactant1 = float(reactant1_entry.get())
            reactant2 = float(reactant2_entry.get())
            product = float(product_entry.get())

            # Example: Simple stoichiometry calculation assuming 1:1:1 ratio
            result = min(reactant1, reactant2) / product
            stoichiometry_label.config(text=f"Stoichiometry Ratio: {result}")

            # Molar mass calculation (Placeholder)
            molar_mass = reactant1 * 2 + reactant2 * 3  # Example calculation
            molar_mass_label.config(text=f"Molar Mass: {molar_mass} g/mol")

            # Concentration calculation (Placeholder)
            concentration = reactant1 / product  # Example calculation
            concentration_label.config(text=f"Concentration: {concentration} mol/L")
        except ValueError:
            messagebox.showerror("Error", "Invalid input")

    reactant1_label = tk.Label(chemical_frame, text="Reactant 1:")
    reactant1_label.grid(row=0, column=0, padx=10, pady=5)
    reactant1_entry = tk.Entry(chemical_frame, width=20, borderwidth=5)
    reactant1_entry.grid(row=0, column=1, padx=10, pady=5)

    reactant2_label = tk.Label(chemical_frame, text="Reactant 2:")
    reactant2_label.grid(row=1, column=0, padx=10, pady=5)
    reactant2_entry = tk.Entry(chemical_frame, width=20, borderwidth=5)
    reactant2_entry.grid(row=1, column=1, padx=10, pady=5)

    product_label = tk.Label(chemical_frame, text="Product:")
    product_label.grid(row=2, column=0, padx=10, pady=5)
    product_entry = tk.Entry(chemical_frame, width=20, borderwidth=5)
    product_entry.grid(row=2, column=1, padx=10, pady=5)

    stoichiometry_label = tk.Label(chemical_frame, text="Stoichiometry Ratio:", font=("Arial", 12))
    stoichiometry_label.grid(row=3, column=0, columnspan=2, pady=5)

    molar_mass_label = tk.Label(chemical_frame, text="Molar Mass:", font=("Arial", 12))
    molar_mass_label.grid(row=4, column=0, columnspan=2, pady=5)

    concentration_label = tk.Label(chemical_frame, text="Concentration:", font=("Arial", 12))
    concentration_label.grid(row=5, column=0, columnspan=2, pady=5)

    calculate_button = tk.Button(chemical_frame, text="Calculate", command=calculate_chemical)
    calculate_button.grid(row=6, column=0, columnspan=2, pady=10)

    # Frame for engineering calculations
    engineering_frame = tk.Frame(root)
    engineering_frame.pack(pady=10)

    # Engineering Calculations
    def calculate_engineering():
        try:
            # Ohm's Law
            voltage = float(voltage_entry.get())
            current = float(current_entry.get())
            resistance = float(resistance_entry.get())

            # Example calculations
            ohms_law_result = voltage / current
            power_result = voltage * current
            stress_result = voltage / resistance  # Placeholder for mechanical stress calculation

            ohms_law_label.config(text=f"Calculated Resistance: {ohms_law_result} Ohms")
            power_label.config(text=f"Power: {power_result} Watts")
            stress_label.config(text=f"Mechanical Stress: {stress_result} Pa")
        except ValueError:
            messagebox.showerror("Error", "Invalid input")

    voltage_label = tk.Label(engineering_frame, text="Voltage (V):")
    voltage_label.grid(row=0, column=0, padx=10, pady=5)
    voltage_entry = tk.Entry(engineering_frame, width=20, borderwidth=5)
    voltage_entry.grid(row=0, column=1, padx=10, pady=5)

    current_label = tk.Label(engineering_frame, text="Current (I):")
    current_label.grid(row=1, column=0, padx=10, pady=5)
    current_entry = tk.Entry(engineering_frame, width=20, borderwidth=5)
    current_entry.grid(row=1, column=1, padx=10, pady=5)

    resistance_label = tk.Label(engineering_frame, text="Resistance (R):")
    resistance_label.grid(row=2, column=0, padx=10, pady=5)
    resistance_entry = tk.Entry(engineering_frame, width=20, borderwidth=5)
    resistance_entry.grid(row=2, column=1, padx=10, pady=5)

    ohms_law_label = tk.Label(engineering_frame, text="Calculated Resistance:", font=("Arial", 12))
    ohms_law_label.grid(row=3, column=0, columnspan=2, pady=5)

    power_label = tk.Label(engineering_frame, text="Power:", font=("Arial", 12))
    power_label.grid(row=4, column=0, columnspan=2, pady=5)

    stress_label = tk.Label(engineering_frame, text="Mechanical Stress:", font=("Arial", 12))
    stress_label.grid(row=5, column=0, columnspan=2, pady=5)

    calculate_eng_button = tk.Button(engineering_frame, text="Calculate", command=calculate_engineering)
    calculate_eng_button.grid(row=6, column=0, columnspan=2, pady=10)    

def init_currency_mode(root):
    clear_window()
    """Initialize the currency conversion mode interface with country names in dropdowns and real conversion rates."""

    # Currency to Country mapping
    currencies = {
        'USD': 'United States Dollar',
        'EUR': 'Euro',
        'HKD': 'Hong Kong Dollar',
        'JPY': 'Japanese Yen',
        'CNY': 'Chinese Yuan',
        'AFN': 'Afghan Afghani',
        'DZD': 'Algerian Dinar',
        'ARS': 'Argentine Peso',
        'AUD': 'Australian Dollar',
        'AZN': 'Azerbaijani Manat',
        'BSD': 'Bahamian Dollar',
        'BHD': 'Bahraini Dinar',
        'BYN': 'Belarusian Ruble',
        'BMD': 'Bermudian Dollar',
        'BTN': 'Bhutanese Ngultrum',
        'BOB': 'Bolivian Boliviano',
        'BWP': 'Botswana Pula',
        'BRL': 'Brazilian Real',
        'GBP': 'British Pound Sterling',
        'BND': 'Brunei Dollar',
        'BGN': 'Bulgarian Lev',
        'MMK': 'Burmese Kyat',
        'CAD': 'Canadian Dollar',
        'CLP': 'Chilean Peso',
        'COP': 'Colombian Peso',
        'CDF': 'Congolese Franc',
        'CRC': 'Costa Rican Colón',
        'HRK': 'Croatian Kuna',
        'CZK': 'Czech Koruna',
        'DKK': 'Danish Krone',
        'EGP': 'Egyptian Pound',
        'ETB': 'Ethiopian Birr',
        'FJD': 'Fijian Dollar',
        'GEL': 'Georgian Lari',
        'GHS': 'Ghanaian Cedi',
        'GNF': 'Guinean Franc',
        'HUF': 'Hungarian Forint',
        'ISK': 'Icelandic Króna',
        'INR': 'Indian Rupee',
        'IDR': 'Indonesian Rupiah',
        'IRR': 'Iranian Rial',
        'IQD': 'Iraqi Dinar',
        'ILS': 'Israeli New Shekel',
        'JMD': 'Jamaican Dollar',
        'JOD': 'Jordanian Dinar',
        'KZT': 'Kazakhstani Tenge',
        'KES': 'Kenyan Shilling',
        'KWD': 'Kuwaiti Dinar',
        'KGS': 'Kyrgyzstani Som',
        'LAK': 'Laotian Kip',
        'LBP': 'Lebanese Pound',
        'LRD': 'Liberian Dollar',
        'LYD': 'Libyan Dinar',
        'MOP': 'Macanese Pataca',
        'MYR': 'Malaysian Ringgit',
        'MVR': 'Maldivian Rufiyaa',
        'MUR': 'Mauritian Rupee',
        'MDL': 'Moldovan Leu',
        'MXN': 'Mexican Peso',
        'MNT': 'Mongolian Tugrik',
        'MAD': 'Moroccan Dirham',
        'NAD': 'Namibian Dollar',
        'TWD': 'New Taiwan Dollar',
        'NZD': 'New Zealand Dollar',
        'NGN': 'Nigerian Naira',
        'NOK': 'Norwegian Krone',
        'CNH': 'Chinese Yuan Offshore',
        'OMR': 'Omani Rial',
        'PKR': 'Pakistani Rupee',
        'PYG': 'Paraguayan Guarani',
        'PEN': 'Peruvian Nuevo Sol',
        'PHP': 'Philippine Peso',
        'PLN': 'Polish Zloty',
        'QAR': 'Qatari Rial',
        'RON': 'Romanian Leu',
        'RUB': 'Russian Ruble',
        'SAR': 'Saudi Riyal',
        'RSD': 'Serbian Dinar',
        'SCR': 'Seychellois Rupee',
        'SGD': 'Singapore Dollar',
        'ZAR': 'South African Rand',
        'KRW': 'South Korean Won',
        'LKR': 'Sri Lankan Rupee',
        'SDG': 'Sudanese Pound',
        'SEK': 'Swedish Krona',
        'CHF': 'Swiss Franc',
        'SYP': 'Syrian Pound',
        'TZS': 'Tanzanian Shilling',
        'THB': 'Thai Baht',
        'TND': 'Tunisian Dinar',
        'TRY': 'Turkish Lira',
        'TMT': 'Turkmenistani Manat',
        'UGX': 'Ugandan Shilling',
        'UAH': 'Ukrainian Hryvnia',
        'AED': 'United Arab Emirates Dirham',
        'UYU': 'Uruguayan Peso',
        'UZS': 'Uzbekistani Som',
        'VND': 'Vietnamese Dong',
        'YER': 'Yemeni Rial',
        'ZMW': 'Zambian Kwacha'
    }

    # Dummy conversion rates relative to USD (1 USD = 1 USD)
    conversion_rates = {
        'USD': 1.0,
        'EUR': 0.93,
        'HKD': 7.85,
        'JPY': 149.75,
        'CNY': 7.16,
        'AFN': 85.52,
        'DZD': 135.65,
        'ARS': 365.24,
        'AUD': 1.48,
        'AZN': 1.70,
        'BSD': 1.00,
        'BHD': 0.38,
        'BYN': 2.55,
        'BMD': 1.00,
        'BTN': 82.60,
        'BOB': 6.87,
        'BWP': 13.05,
        'BRL': 4.92,
        'GBP': 0.76,
        'BND': 1.35,
        'BGN': 1.68,
        'MMK': 2083.21,
        'CAD': 1.37,
        'CLP': 801.64,
        'COP': 3982.90,
        'CDF': 2086.00,
        'CRC': 606.34,
        'HRK': 7.02,
        'CZK': 22.89,
        'DKK': 6.94,
        'EGP': 30.70,
        'ETB': 54.82,
        'FJD': 2.25,
        'GEL': 2.66,
        'GHS': 12.30,
        'GNF': 8691.84,
        'HUF': 329.21,
        'ISK': 139.26,
        'INR': 83.09,
        'IDR': 15324.60,
        'IRR': 42000.00,
        'IQD': 1290.00,
        'ILS': 3.65,
        'JMD': 154.05,
        'JOD': 0.71,
        'KZT': 456.09,
        'KES': 135.67,
        'KWD': 0.31,
        'KGS': 87.54,
        'LAK': 18296.00,
        'LBP': 15122.00,
        'LRD': 160.00,
        'LYD': 4.76,
        'MOP': 8.07,
        'MYR': 4.62,
        'MVR': 15.41,
        'MUR': 45.09,
        'MDL': 18.61,
        'MXN': 17.67,
        'MNT': 3403.52,
        'MAD': 10.09,
        'NAD': 18.77,
        'TWD': 31.21,
        'NZD': 1.60,
        'NGN': 778.20,
        'NOK': 10.25,
        'CNH': 7.16,
        'OMR': 0.38,
        'PKR': 282.51,
        'PYG': 7100.00,
        'PEN': 3.72,
        'PHP': 56.09,
        'PLN': 4.32,
        'QAR': 3.64,
        'RON': 4.68,
        'RUB': 83.54,
        'SAR': 3.75,
        'RSD': 104.85,
        'SCR': 12.76,
        'SGD': 1.35,
        'ZAR': 19.14,
        'KRW': 1353.72,
        'LKR': 254.27,
        'SDG': 1364.09,
        'SEK': 10.20,
        'CHF': 0.91,
        'SYP': 2511.00,
        'TZS': 2330.00,
        'THB': 35.08,
        'TND': 3.11,
        'TRY': 27.23,
        'TMT': 3.50,
        'UGX': 3750.00,
        'UAH': 36.30,
        'AED': 3.67,
        'UYU': 37.55,
        'UZS': 11980.00,
        'VND': 23780.00,
        'YER': 250.00,
        'ZMW': 21.90
    }

    def convert_currency():
        """Convert the amount from one currency to another."""
        amount = amount_entry.get()
        from_currency = from_currency_combobox.get().split(' - ')[0]
        to_currency = to_currency_combobox.get().split(' - ')[0]
        
        if not amount or not from_currency or not to_currency:
            result_label.config(text="Please enter amount and select currencies.")
            return
        
        try:
            amount = float(amount)
            # Conversion calculation
            if from_currency == to_currency:
                result = amount
            else:
                result = amount * (conversion_rates[to_currency] / conversion_rates[from_currency])
            result_label.config(text=f"{amount} {from_currency} = {result:.2f} {to_currency}")
        except ValueError:
            result_label.config(text="Invalid amount. Please enter a number.")
        except KeyError:
            result_label.config(text="Currency not found.")

    # Create and place widgets for the currency conversion mode
    from_currency_label = tk.Label(root, text="From Currency:")
    from_currency_label.pack(pady=5)

    from_currency_combobox = ttk.Combobox(root, values=[f"{code} - {name}" for code, name in currencies.items()])
    from_currency_combobox.pack(pady=5)

    to_currency_label = tk.Label(root, text="To Currency:")
    to_currency_label.pack(pady=5)

    to_currency_combobox = ttk.Combobox(root, values=[f"{code} - {name}" for code, name in currencies.items()])
    to_currency_combobox.pack(pady=5)

    amount_label = tk.Label(root, text="Amount:")
    amount_label.pack(pady=5)

    amount_entry = tk.Entry(root)
    amount_entry.pack(pady=5)

    convert_button = tk.Button(root, text="Convert", command=convert_currency)
    convert_button.pack(pady=5)

    result_label = tk.Label(root, text="")
    result_label.pack(pady=10)

def init_prob_stat_table_mode():
    clear_window()
    root.title("Probability & Statistic Tables Mode")
    label = tk.Label(root, text="Probability & Statistic Tables")
    label.pack()

    def show_table_content():
        test_type = dropdown_var.get()

        if test_type == "Z-Test":
            try:
                z_value = z_entry.get()
                area_value = area_entry.get()

                if z_value:  # If Z-value is provided
                    z_value = float(z_value)
                    area = z_test_area(z_value)
                    table_label.config(text=f"Area between Z = 0 and Z = {z_value}: {area:.4f}")
                elif area_value:  # If area is provided
                    area_value = float(area_value)
                    z_value = z_from_area(area_value)
                    table_label.config(text=f"Z-value for area {area_value}: {z_value:.4f}")
                else:
                    table_label.config(text="Please enter either a Z value or an area.")
            except ValueError:
                table_label.config(text="Please enter valid numbers for Z or area.")

        elif test_type == "T-Test":
            try:
                df_value = int(df_entry.get())
                alpha_value = float(alpha_entry.get())
                tail_type = tail_var.get()

                if tail_type == "One-Tailed":
                    t_value = t.ppf(1 - alpha_value, df_value)
                elif tail_type == "Two-Tailed":
                    t_value = t.ppf(1 - alpha_value / 2, df_value)
                else:
                    table_label.config(text="Please select the type of tail.")
                    return

                table_label.config(text=f"T-value for df = {df_value}, alpha = {alpha_value}: {t_value:.4f}")
            except ValueError:
                table_label.config(text="Please enter valid numbers for degrees of freedom and alpha.")

        elif test_type == "Chi-Square Test":
            try:
                df_value = int(df_entry.get())
                alpha_value = float(alpha_entry.get())

                chi2_value = chi2.ppf(1 - alpha_value, df_value)
                table_label.config(text=f"Chi-Square value for df = {df_value}, alpha = {alpha_value}: {chi2_value:.4f}")
            except ValueError:
                table_label.config(text="Please enter valid numbers for degrees of freedom and alpha.")

        elif test_type == "F-Test":
            try:
                df1_value = int(df1_entry.get())
                df2_value = int(df2_entry.get())
                alpha_value = float(alpha_entry.get())

                f_value = f.ppf(1 - alpha_value, df1_value, df2_value)
                table_label.config(text=f"F-value for df1 = {df1_value}, df2 = {df2_value}, alpha = {alpha_value}: {f_value:.4f}")
            except ValueError:
                table_label.config(text="Please enter valid numbers for degrees of freedom and alpha.")

    def z_test_area(z):
        area_cumulative = norm.cdf(z)
        area_from_zero = area_cumulative - 0.5  # Since CDF at Z=0 is 0.5
        return area_from_zero

    def z_from_area(area):
        area_cumulative = area + 0.5  # Adjust to get the cumulative area
        z_value = norm.ppf(area_cumulative)
        return z_value

    def on_test_type_change(*args):
        test_type = dropdown_var.get()
        hide_all_inputs()

        if test_type == "Z-Test":
            z_entry_label.pack()
            z_entry.pack()
            area_entry_label.pack()
            area_entry.pack()
            show_button.pack()
        elif test_type == "T-Test":
            df_entry_label.pack()
            df_entry.pack()
            alpha_entry_label.pack()
            alpha_entry.pack()
            tail_menu.pack()
            show_button.pack()
        elif test_type == "Chi-Square Test":
            df_entry_label.pack()
            df_entry.pack()
            alpha_entry_label.pack()
            alpha_entry.pack()
            show_button.pack()
        elif test_type == "F-Test":
            df1_entry_label.pack()
            df1_entry.pack()
            df2_entry_label.pack()
            df2_entry.pack()
            alpha_entry_label.pack()
            alpha_entry.pack()
            show_button.pack()

    def hide_all_inputs():
        z_entry_label.pack_forget()
        z_entry.pack_forget()
        area_entry_label.pack_forget()
        area_entry.pack_forget()
        df_entry_label.pack_forget()
        df_entry.pack_forget()
        df1_entry_label.pack_forget()
        df1_entry.pack_forget()
        df2_entry_label.pack_forget()
        df2_entry.pack_forget()
        alpha_entry_label.pack_forget()
        alpha_entry.pack_forget()
        tail_menu.pack_forget()
        show_button.pack_forget()
        table_label.config(text="")

    dropdown_var = tk.StringVar(value="Select Test")
    dropdown_var.trace("w", on_test_type_change)
    dropdown_menu = tk.OptionMenu(root, dropdown_var, "Z-Test", "T-Test", "Chi-Square Test", "F-Test")
    dropdown_menu.pack()

    # Z-Test inputs
    z_entry_label = tk.Label(root, text="Enter Z value (leave blank if unknown):")
    z_entry = tk.Entry(root)

    area_entry_label = tk.Label(root, text="Enter Area (leave blank if unknown):")
    area_entry = tk.Entry(root)

    # T-Test inputs
    df_entry_label = tk.Label(root, text="Enter Degrees of Freedom (df):")
    df_entry = tk.Entry(root)

    alpha_entry_label = tk.Label(root, text="Enter Alpha Significance Level:")
    alpha_entry = tk.Entry(root)

    tail_var = tk.StringVar(value="One-Tailed")
    tail_menu = tk.OptionMenu(root, tail_var, "One-Tailed", "Two-Tailed")

    # F-Test inputs
    df1_entry_label = tk.Label(root, text="Enter Degrees of Freedom 1 (df1):")
    df1_entry = tk.Entry(root)

    df2_entry_label = tk.Label(root, text="Enter Degrees of Freedom 2 (df2):")
    df2_entry = tk.Entry(root)

    show_button = tk.Button(root, text="Compute", command=show_table_content)

    table_label = tk.Label(root, text="", justify="left", font=("Courier", 10))
    table_label.pack()
 

# Initialize the entry widget
entry = tk.Entry(root, width=25, font=('Arial', 24), borderwidth=2, relief="solid")
entry.grid(row=0, column=0, columnspan=6)


# Create the mode selection menu
menu = tk.Menu(root)
root.config(menu=menu)
mode_var = tk.StringVar(value="Standard")

root.protocol("WM_DELETE_WINDOW", lambda: [clear_history(), root.destroy()])

mode_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Mode", menu=mode_menu)
mode_menu.add_command(label="Standard", command=lambda: change_mode("Standard"))
mode_menu.add_command(label="Scientific", command=lambda: change_mode("Scientific"))
mode_menu.add_command(label="Angle", command=lambda: change_mode("Angle"))
mode_menu.add_command(label="Temperature", command=lambda: change_mode("Temperature"))
mode_menu.add_command(label="Programming", command=lambda: change_mode("Programming"))
mode_menu.add_command(label="Speed", command=lambda: change_mode("Speed"))
mode_menu.add_command(label="Power", command=lambda: change_mode("Power"))
mode_menu.add_command(label="Pressure", command=lambda: change_mode("Pressure"))
mode_menu.add_command(label="Time", command=lambda: change_mode("Time"))
mode_menu.add_command(label="Area", command=lambda: change_mode("Area"))
mode_menu.add_command(label="Energy", command=lambda: change_mode("Energy"))
mode_menu.add_command(label="Weight and Mass", command=lambda: change_mode("Weight and Mass"))
mode_menu.add_command(label="Length", command=lambda: change_mode("Length"))
mode_menu.add_command(label="Volume", command=lambda: change_mode("Volume"))
mode_menu.add_command(label="Date Difference", command=lambda: change_mode("Date Difference"))
mode_menu.add_command(label="ComplexNumbers", command=lambda: change_mode("ComplexNumbers"))
mode_menu.add_command(label="Matrices and vectors", command=lambda: change_mode("Matrices and vectors"))
mode_menu.add_command(label="Algebra", command=lambda: change_mode("Algebra"))
mode_menu.add_command(label="Calculus", command=lambda: change_mode("Calculus"))
mode_menu.add_command(label="Statistics and Probability", command=lambda: change_mode("Statistics and Probability"))
mode_menu.add_command(label="Financial", command=lambda: change_mode("Financial"))
mode_menu.add_command(label="Data analysis and manipulation", command=lambda: change_mode("Data analysis and manipulation"))
mode_menu.add_command(label="Math consts and funcs", command=lambda: change_mode("Math consts and funcs"))
mode_menu.add_command(label="Engineering and Scientific", command=lambda: change_mode("Engineering and Scientific"))
mode_menu.add_command(label="Currency", command=lambda: change_mode("Currency"))
mode_menu.add_command(label="Statistics and Probability table", command=lambda: change_mode("Statistics and Probability table"))
mode_menu.add_command(label="History", command=lambda: change_mode("History"))

# Start in Standard mode
init_standard_mode()


# Start the main event loop
root.mainloop()