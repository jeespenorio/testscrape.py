from bs4 import BeautifulSoup
import requests
import tkinter as tk
from tkinter import Entry, Button, Text, Scrollbar, Label, OptionMenu, StringVar, Radiobutton, filedialog
import csv

# Function to retrieve and parse HTML content
def get_and_parse_html():
    url = url_entry.get()
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Get the selected HTML element and class name
        element_to_find = element_var.get()
        
        found_elements = soup.find_all(element_to_find)
        
        if found_elements:
            result_text.config(state=tk.NORMAL)
            result_text.delete(1.0, tk.END)
            
            if element_to_find == "th":
                # Display data by columns for <th> elements
                headers = [header.text for header in found_elements]
                result_text.insert(tk.END, "Data displayed by columns:\n")
                result_text.insert(tk.END, "\t".join(headers) + "\n")
            elif element_to_find == "tr":
                # Display data by rows for <tr> elements
                data = []
                for element in found_elements:
                    row_data = [cell.text for cell in element.find_all(["th", "td"])]
                    data.append(row_data)
                result_text.insert(tk.END, "Data displayed by rows:\n")
                for row in data:
                    result_text.insert(tk.END, "\t".join(row) + "\n")
                
            result_text.config(state=tk.DISABLED)
        else:
            result_text.config(state=tk.NORMAL)
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"No '{element_to_find}' elements found in the HTML.")
            result_text.config(state=tk.DISABLED)
    except requests.exceptions.RequestException as e:
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Failed to retrieve and parse HTML: {e}")
        result_text.config(state=tk.DISABLED)

# Function to save displayed data to a CSV file
def save_to_csv():
    data_to_save = result_text.get("1.0", "end-1c").split('\n')
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if file_path:
        with open(file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerows([line.split('\t') for line in data_to_save])
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Data saved to '{file_path}'.")
        result_text.config(state=tk.DISABLED)

# Function to exit the application
def exit_application():
    root.destroy()

# Create a tkinter window
root = tk.Tk()
root.title("HTML Parsing with BeautifulSoup")

# Entry widget for user to input URL
url_label = Label(root, text="Enter URL:")
url_label.pack()
url_entry = Entry(root, width=40)
url_entry.pack()

# Dropdown menu for selecting HTML element to find
element_var = tk.StringVar()
element_var.set("th")  # Default selection for <th> elements
element_label = Label(root, text="Select HTML Element to Find:")
element_label.pack()
element_menu = OptionMenu(root, element_var, "th", "tr")
element_menu.pack()

# Button to trigger HTML retrieval and parsing
parse_button = Button(root, text="Retrieve and Parse HTML", command=get_and_parse_html)
parse_button.pack()

# Text widget to display parsed HTML content
result_text = Text(root, wrap=tk.WORD, width=80, height=20)
result_text.pack()
result_text.config(state=tk.DISABLED)

# Radio buttons for choosing display method
display_option = tk.StringVar()
display_option.set("columns")  # Default display by columns

columns_radio = Radiobutton(root, text="Display by Columns", variable=display_option, value="columns")
columns_radio.pack()
rows_radio = Radiobutton(root, text="Display by Rows", variable=display_option, value="rows")
rows_radio.pack()

# Button to save data to CSV
save_button = Button(root, text="Save to CSV", command=save_to_csv)
save_button.pack()

# Button to exit the application
exit_button = Button(root, text="Exit", command=exit_application)
exit_button.pack()

root.mainloop()
