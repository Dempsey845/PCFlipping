import tkinter
import time
from tkinter import messagebox, Entry, Label, Canvas, PhotoImage
from enum import Enum
from image_uploader import *
from PIL import Image, ImageTk
from image_uploader import open_image_uploader, resize_image

import os
import json
import random

def get_builds_list():
    file_path = os.path.join('..', 'data', 'Builds.json')
    # Open and load the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Access the list of builds
    builds = data['builds']
    return builds

def clean_unused_skus():
    builds = get_builds_list()

    file_path = os.path.join('..', 'data', 'SKUS.json')

    # Open and load the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Access the list of SKUs
    skus = data['SKUS']
    used_skus = set()  # Use a set for faster lookups

    # Collect all used SKUs
    for build in builds:
        for sku in skus:
            if build["sku"] == sku:
                used_skus.add(sku)

    # Filter the SKUs to keep only the used ones
    cleaned_skus = [sku for sku in skus if sku in used_skus]

    # Update the JSON data
    data['SKUS'] = cleaned_skus

    # Write back the cleaned data to the JSON file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

    print("Unused SKUs have been cleared from SKUS.json.")

def generate_unique_sku():
    file_path = os.path.join('..', 'data', 'SKUS.json')
    # Open and load the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Access the list of used SKUs
    used_skus = data['SKUS']

    # Generate a unique random SKU that isn't already used
    new_sku = random.randint(1000, 10000)

    # Check if the SKU is already used and keep generating until a unique one is found
    while new_sku in used_skus:
        new_sku = random.randint(1000, 10000)

    # Save the updated SKU list back to the JSON file
    used_skus.append(new_sku)
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

    return new_sku

class ScrollableFrame(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Create a canvas
        self.canvas = tkinter.Canvas(self, bg=master["bg"])
        self.scrollable_frame = tkinter.Frame(self.canvas, bg=master["bg"])

        # Add a scrollbar
        self.scrollbar = tkinter.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        # Configure the canvas
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Configure the scrollbar and canvas
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Prevent the canvas from resizing to fit the frame
        self.canvas.pack_propagate(False)
        self.pack_propagate(False)

    def on_frame_configure(self, event):
        # Update the scroll region of the canvas
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def clear(self):
        # Destroy all widgets inside the scrollable frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def print_widgets(self):
        for widget in self.scrollable_frame.winfo_children():
            print(widget)

    def hide(self):
        """Hide the scrollable frame."""
        self.pack_forget()

    def show(self):
        """Show the scrollable frame."""
        self.pack(side="left", fill="both", expand=True)

class PCBuildUI:
    def __init__(self, pc_dict, full_pc_dict, sku):
        self.description_label = None
        self.packed = False
        self.full_pc_dict = full_pc_dict
        self.pc_dict = pc_dict
        self.build_sku_label = None
        self.update_build_button = None


        self.pc_str = ""

        self.build_image = None

        counter = 0

        for key, value in pc_dict.items():
            if value is not None and key != "ram" and key != "sku":
                self.pc_str += f"{key}: {value}\n"
                counter += 1
            elif key == "RAM":
                self.pc_str += f"{key}: {"".join(value)}\n"
                counter += 1

            if counter == 4:
                self.pc_str += "\n"
                counter = 0

            if key == "image_path":
                self.image_path = value

    def pack(self):
        if not self.packed:
            self.packed = True

    def get_sku(self):
        return self.pc_dict["sku"]

    def destroy(self):
        if self.description_label is not None:
            self.description_label.grid_forget()
            self.build_sku_label.grid_forget()
        del self

class Scene(Enum):
    START_SCENE = 1
    ADD_BUILD_SCENE = 2

class ComponentEntry:
    def __init__(self, parent, text, font=("Arial", 12, "bold"), entry_width=12, is_title=False, is_checkbox=False):
        self.label = None
        if not is_checkbox:
            self.label = tkinter.Label(parent, text=text, font=font)
            self.label.grid(sticky='w', pady=1)  # Align the label to the left
        self.is_title = is_title

        if not is_title and not is_checkbox:
            self.entry = tkinter.Entry(parent, width=entry_width, )
            self.entry.grid(sticky='w', pady=1)  # Align the entry to the left
        else:
            self.entry = None

        if is_checkbox:
            self.is_checked = tk.BooleanVar()
            self.checkbox = tkinter.Checkbutton(parent, variable=self.is_checked)

    def get_value(self):
        return self.entry.get()  # Return the text from the entry

    def clear(self):
        self.entry.delete(0, tkinter.END)  # Clear the entry

    def clear_title(self):
        self.label.grid_forget()
        self.label.destroy()

class GUI:
    """
    TODO - IMPLEMENT ADDING A BUILD AND REMOVING A BUILD
    TODO - IMPLEMENT SORTING BUILDS BY DIFFERENT TYPES E.G list-date, profit, cpu, cpu-brand, etc...
    """
    def __init__(self):
        self.update_build_buttons = []
        self.has_image = False
        self.edit_build_frame = None
        self.new_sku_label = None
        self.new_build_sku = None
        self.tk_image = None
        self.upload_btn = None
        self.display_label = None
        self.image_upload_frame = None
        self.scene = "START_SCENE"

        # Create main window
        self.window = tkinter.Tk()
        self.window.title("PC Flipping")

        # Set the window size explicitly
        self.window.geometry("1300x900")  # Set the initial size of the window
        self.window.configure(bg="black")

        # Create title grid frame
        self.title_grid_frame = tkinter.Frame(self.window, bg="black")
        self.title_grid_frame.pack()

        self.title_label = Label(text="PC Flipping", font=("Arial", 24), bg="black")
        self.title_label.grid(in_=self.title_grid_frame, row=0, column=0, columnspan=3, pady=10, sticky="n")

        # Create navigation frame
        self.navigation_grid_frame = tkinter.Frame(self.window, bg="black")
        self.navigation_grid_frame.pack()

        # Create build grid frame with fixed width and allow height expansion
        self.build_grid_frame = tkinter.Frame(self.window, bg="lightblue", width=850, height=850)
        self.build_grid_frame.pack_propagate(False)  # Prevent resizing to fit contents
        self.build_grid_frame.pack(fill="x")  # Fill horizontally but fixed width

        # Create scrollable frame within the build frame
        self.build_scrollable_frame = ScrollableFrame(self.build_grid_frame)
        self.build_scrollable_frame.pack(fill="both", expand=True)

        # Create add build grid frame with fixed width and allow height expansion
        self.add_build_grid_frame = tkinter.Frame(self.window, bg="red", width=850, height=1200)
        self.add_build_grid_frame.pack_propagate(False)  # Prevent resizing to fit contents
        self.add_build_grid_frame.pack(fill="x")  # Fill horizontally but fixed width

        # Create scrollable frame within the add build frame
        self.add_build_scrollable_frame = ScrollableFrame(self.add_build_grid_frame)
        self.add_build_scrollable_frame.pack(fill="both", expand=True)

        self.add_build_scrollable_frame.columnconfigure(0, weight=1)
        self.add_build_scrollable_frame.columnconfigure(1, weight=1)
        self.add_build_scrollable_frame.columnconfigure(2, weight=1)
        self.add_build_scrollable_frame.canvas.configure(scrollregion=self.add_build_grid_frame.bbox("all"))

        # Start Scene Variables
        self.add_build_button = tkinter.Button(text="Add Build", command=self.go_to_add_build_scene, bg="black")
        self.show_all_button = tkinter.Button(text="Show All Builds", bg="black")
        self.visible_builds = []

        # Add Build Scene Variables
        self.go_back_to_start_scene_button = tkinter.Button(text="Go Back", command=self.go_back_button, height=2, width=6, bg="black")
        self.save_build_button = tkinter.Button(text="Save Build", height=2, width=6, bg="black")
        self.show_all_button.pack()
        self.add_build_button.pack()

        self.all_buttons = [self.add_build_button, self.show_all_button, self.go_back_to_start_scene_button, self.save_build_button]
        self.all_build_labels = []
        self.all_build_entries = []

        self.extras_label = None

        # Lists to store all the Entry Components
        self.cpu_components = []
        self.gpu_components = []
        self.ram_components = []
        self.motherboard_components = []
        self.ssd_components = []
        self.nvme_components = []
        self.hdd_components = []
        self.psu_components = []
        self.case_components = []
        self.extra_costs_components = None
        self.target_sell_price_component = None
        self.extra_profit_component = None
        self.list_date_component = None
        self.sell_date_component = None
        self.sell_price_component = None

        self.all_extra_components = [self.extra_costs_components , self.target_sell_price_component , self.extra_profit_component, self.list_date_component,
                                     self.sell_date_component, self.sell_price_component]

        self.all_components = (self.cpu_components + self.gpu_components + self.ram_components + self.motherboard_components + self.ssd_components +
                               self.nvme_components + self.hdd_components + self.psu_components + self.case_components + self.all_extra_components)

        print(self.all_components)

        self.all_labels = self.all_build_labels + []
        self.all_entries = self.all_build_entries + []

        self.go_to_start_scene()

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def go_back_button(self):
        if messagebox.askokcancel("Go Back?", "Are you sure you want to go back? Make sure to save your build."):
            self.go_to_start_scene()

    def add_all_entry_components(self):
        self.add_all_cpu_components()
        self.add_all_gpu_components()
        self.add_all_ram_components()
        self.add_all_motherboard_components()
        self.add_all_ssd_components()
        self.add_all_hdd_components()
        self.add_all_nvme_components()
        self.add_all_psu_components()
        self.add_all_case_components()
        self.add_target_sell_price()
        self.add_extra_profit()
        self.add_list_date()
        self.add_sell_date()
        self.add_sell_price()
        self.add_extra_costs()

    def add_all_cpu_components(self):
        self.add_cpu_component("CPU", font=("Arial", 16, "bold"), title=True)  # Title
        self.add_cpu_component("Name")
        self.add_cpu_component("Brand")
        self.add_cpu_component("Price")

    def add_all_gpu_components(self):
        self.add_gpu_component("GPU", font=("Arial", 16, "bold"), title=True)  # Title
        self.add_gpu_component("Name")
        self.add_gpu_component("Brand")
        self.add_gpu_component("Price")

    def add_all_ram_components(self):
        self.add_ram_component("RAM", font=("Arial", 16, "bold"), title=True)  # Title
        self.add_ram_component("Name")
        self.add_ram_component("Brand")
        self.add_ram_component("Price")

    def add_all_motherboard_components(self):
        self.add_motherboard_component("Motherboard", font=("Arial", 16, "bold"), title=True)  # Title
        self.add_motherboard_component("Name")
        self.add_motherboard_component("Brand")
        self.add_motherboard_component("Price")


    def add_all_ssd_components(self):
        self.add_ssd_component("SSD", font=("Arial", 16, "bold"), title=True)  # Title
        self.add_ssd_component("Name")
        self.add_ssd_component("Brand")
        self.add_ssd_component("Price")
        self.add_ssd_component("Checkbox", is_checkbox=True)

    def add_all_hdd_components(self):
        self.add_hdd_component("HDD", font=("Arial", 16, "bold"), title=True)  # Title
        self.add_hdd_component("Name")
        self.add_hdd_component("Brand")
        self.add_hdd_component("Price")
        self.add_hdd_component("Checkbox", is_checkbox=True)


    def add_all_nvme_components(self):
        self.add_nvme_component("NVME", font=("Arial", 16, "bold"), title=True)  # Title
        self.add_nvme_component("Name")
        self.add_nvme_component("Brand")
        self.add_nvme_component("Price")
        self.add_nvme_component("Checkbox", is_checkbox=True)

    def add_all_psu_components(self):
        self.add_psu_component("PSU", font=("Arial", 16, "bold"), title=True)  # Title
        self.add_psu_component("Name")
        self.add_psu_component("Brand")
        self.add_psu_component("Price")

    def add_all_case_components(self):
        self.add_case_component("Case", font=("Arial", 16, "bold"), title=True)  # Title
        self.add_case_component("Name")
        self.add_case_component("Brand")
        self.add_case_component("Price")

    def add_cpu_component(self, text, font=("Arial", 12, "bold"), title=False):
        component = ComponentEntry(self.add_build_scrollable_frame.scrollable_frame, text, font, is_title=title)

        # Position the title differently from the others
        if title:
            component.label.grid(column=1, row=1, pady=5)
        else:
            component.label.grid(column=len(self.cpu_components)+1, row=1, sticky="ew")
            component.entry.grid(column=len(self.cpu_components)+1, row=2, sticky="ew")

        self.cpu_components.append(component)  # Store the component for later use

    # Similar methods for GPU, RAM, Motherboard, etc.
    def add_gpu_component(self, text, font=("Arial", 12, "bold"), title=False):
        component = ComponentEntry(self.add_build_scrollable_frame.scrollable_frame, text, font, is_title=title)

        if title:
            component.label.grid(column=1, row=3, pady=5)
        else:
            component.label.grid(column=len(self.gpu_components) + 1, row=3, sticky="ew")
            component.entry.grid(column=len(self.gpu_components) + 1, row=4, sticky="ew")

        self.gpu_components.append(component)

    def add_ram_component(self, text, font=("Arial", 12, "bold"), title=False):
        component = ComponentEntry(self.add_build_scrollable_frame.scrollable_frame, text, font, is_title=title)

        if title:
            component.label.grid(column=1, row=5, pady=5)
        else:
            component.label.grid(column=len(self.ram_components) + 1, row=5, sticky="ew")
            component.entry.grid(column=len(self.ram_components) + 1, row=6, sticky="ew")

        self.ram_components.append(component)

    def add_motherboard_component(self, text, font=("Arial", 12, "bold"), title=False):
        component = ComponentEntry(self.add_build_scrollable_frame.scrollable_frame, text, font, is_title=title,)


        if title:
            component.label.grid(column=1, row=7, pady=5, padx=(0, 5))

        else:
            component.label.grid(column=len(self.motherboard_components) + 1, row=7, sticky="ew")
            component.entry.grid(column=len(self.motherboard_components) + 1, row=8, sticky="ew")

        self.motherboard_components.append(component)

    def add_ssd_component(self, text, font=("Arial", 12, "bold"), title=False, is_checkbox=False):
        component = ComponentEntry(self.add_build_scrollable_frame.scrollable_frame, text, font, is_title=title, is_checkbox=is_checkbox)

        if title:
            component.label.grid(column=1, row=9, pady=5)
        elif is_checkbox:
            component.checkbox.grid(column=len(self.ssd_components)+1, row=9, padx=5)
        else:
            component.label.grid(column=len(self.ssd_components) + 1, row=9, sticky="ew")
            component.entry.grid(column=len(self.ssd_components) + 1, row=10, sticky="ew")

        self.ssd_components.append(component)

    def add_hdd_component(self, text, font=("Arial", 12, "bold"), title=False, is_checkbox=False):
        component = ComponentEntry(self.add_build_scrollable_frame.scrollable_frame, text, font, is_title=title, is_checkbox=is_checkbox)

        if title:
            component.label.grid(column=1, row=11, pady=5)
        elif is_checkbox:
            component.checkbox.grid(column=len(self.hdd_components)+1, row=11, padx=5)
        else:
            component.label.grid(column=len(self.hdd_components) + 1, row=11, sticky="ew")
            component.entry.grid(column=len(self.hdd_components) + 1, row=12, sticky="ew")

        self.hdd_components.append(component)

    def add_nvme_component(self, text, font=("Arial", 12, "bold"), title=False, is_checkbox=False):
        component = ComponentEntry(self.add_build_scrollable_frame.scrollable_frame, text, font, is_title=title, is_checkbox=is_checkbox)

        if title:
            component.label.grid(column=1, row=13, pady=5)
        elif is_checkbox:
            component.checkbox.grid(column=len(self.nvme_components)+1, row=13, padx=5)
        else:
            component.label.grid(column=len(self.nvme_components) + 1, row=13, sticky="ew")
            component.entry.grid(column=len(self.nvme_components) + 1, row=14, sticky="ew")

        self.nvme_components.append(component)

    def add_psu_component(self, text, font=("Arial", 12, "bold"), title=False):
        component = ComponentEntry(self.add_build_scrollable_frame.scrollable_frame, text, font, is_title=title)

        if title:
            component.label.grid(column=1, row=15, pady=5)
        else:
            component.label.grid(column=len(self.psu_components) + 1, row=15, sticky="ew")
            component.entry.grid(column=len(self.psu_components) + 1, row=16, sticky="ew")

        self.psu_components.append(component)

    def add_case_component(self, text, font=("Arial", 12, "bold"), title=False):
        component = ComponentEntry(self.add_build_scrollable_frame.scrollable_frame, text, font, is_title=title)

        if title:
            component.label.grid(column=1, row=17, pady=5)
        else:
            component.label.grid(column=len(self.case_components) + 1, row=17, sticky="ew")
            component.entry.grid(column=len(self.case_components) + 1, row=18, sticky="ew")

        self.case_components.append(component)

    def clear_cpu_components(self):
        if self.cpu_components is None:
            return

        """Clear CPU component entries and labels."""
        for component in self.cpu_components:
            if not component.is_title:
                component.label.destroy()
                component.entry.destroy()
            else:
                component.clear_title()
        self.cpu_components.clear()

    def clear_gpu_components(self):
        if self.gpu_components is None:
            return

        """Clear GPU component entries and labels."""
        for component in self.gpu_components:
            if not component.is_title:
                component.label.destroy()
                component.entry.destroy()
            else:
                component.clear_title()
        self.gpu_components.clear()

    def clear_ram_components(self):
        if self.ram_components is None:
            return

        """Clear RAM component entries and labels."""
        for component in self.ram_components:
            if not component.is_title:
                component.label.destroy()
                component.entry.destroy()
            else:
                component.clear_title()
        self.ram_components.clear()

    def clear_motherboard_components(self):
        if self.motherboard_components is None:
            return

        """Clear Motherboard component entries and labels."""
        for component in self.motherboard_components:
            if not component.is_title:
                component.label.destroy()
                component.entry.destroy()
            else:
                component.clear_title()
        self.motherboard_components.clear()

    def clear_ssd_components(self):
        if self.ssd_components is None:
            return

        """Clear SSD component entries and labels."""
        for component in self.ssd_components:
            if not component.is_title:
                component.label.destroy()
                component.entry.destroy()
            else:
                component.clear_title()
        self.ssd_components.clear()

    def clear_hdd_components(self):
        if self.hdd_components is None:
            return

        """Clear HDD component entries and labels."""
        for component in self.hdd_components:
            if not component.is_title:
                component.label.destroy()
                component.entry.destroy()
            else:
                component.clear_title()
        self.hdd_components.clear()

    def clear_nvme_components(self):
        if self.nvme_components is None:
            return

        """Clear NVME component entries and labels."""
        for component in self.nvme_components:
            if not component.is_title:
                component.label.destroy()
                component.entry.destroy()
            else:
                component.clear_title()
        self.nvme_components.clear()

    def clear_psu_components(self):
        if self.psu_components is None:
            return

        """Clear PSU component entries and labels."""
        for component in self.psu_components:
            if not component.is_title:
                component.label.destroy()
                component.entry.destroy()
            else:
                component.clear_title()
        self.psu_components.clear()

    def clear_case_components(self):
        if self.case_components is None:
            return

        """Clear Case component entries and labels."""
        for component in self.case_components:
            if not component.is_title:
                component.label.destroy()
                component.entry.destroy()
            else:
                component.clear_title()
        self.case_components.clear()

    def clear_extra_costs_components(self):
        if self.extra_costs_components is None:
            return
        if hasattr(self, 'extra_costs_components'):
            self.extra_costs_components.label.destroy()
            self.extra_costs_components.entry.destroy()

    def clear_target_sell_price(self):
        """Clear Target Sell Price component entries and labels."""
        if self.target_sell_price_component is None:
            return
        if hasattr(self, 'target_sell_price_component'):
            self.target_sell_price_component.label.destroy()
            self.target_sell_price_component.entry.destroy()

    def clear_extra_profit(self):
        if self.extra_profit_component is None:
            return

        """Clear Extra Profit component entries and labels."""
        if hasattr(self, 'extra_profit_component'):
            self.extra_profit_component.label.destroy()
            self.extra_profit_component.entry.destroy()

    def clear_list_date(self):
        if self.list_date_component is None:
            return

        """Clear List Date component entries and labels."""
        if hasattr(self, 'list_date_component'):
            self.list_date_component.label.destroy()
            self.list_date_component.entry.destroy()

    def clear_sell_date(self):
        if self.sell_date_component is None:
            return

        """Clear Sell Date component entries and labels."""
        if hasattr(self, 'sell_date_component'):
            self.sell_date_component.label.destroy()
            self.sell_date_component.entry.destroy()

    def clear_sell_price(self):
        if self.sell_price_component is None:
            return

        """Clear Sell Price component entries and labels."""
        if hasattr(self, 'sell_price_component'):
            self.sell_price_component.label.destroy()
            self.sell_price_component.entry.destroy()

    def clear_all_components(self):
        """Call clear methods for all components."""
        self.cpu_components = []
        self.gpu_components = []
        self.ram_components = []
        self.motherboard_components = []
        self.ssd_components = []
        self.nvme_components = []
        self.hdd_components = []
        self.psu_components = []
        self.case_components = []
        self.extra_costs_components = None
        self.target_sell_price_component = None
        self.extra_profit_component = None
        self.list_date_component = None
        self.sell_date_component = None
        self.sell_price_component = None
        """
        self.clear_cpu_components()
        self.clear_gpu_components()
        self.clear_ram_components()
        self.clear_motherboard_components()
        self.clear_ssd_components()
        self.clear_hdd_components()
        self.clear_nvme_components()
        self.clear_psu_components()
        self.clear_case_components()
        self.clear_extra_costs_components()
        self.clear_target_sell_price()
        self.clear_extra_profit()
        self.clear_list_date()
        self.clear_sell_date()
        self.clear_sell_price()
        self.clear_extra_costs_components()
        """

    # Specific methods for other extra fields
    def add_target_sell_price(self):
        self.extras_label = Label(self.add_build_scrollable_frame.scrollable_frame, font=("Arial", 16, "bold"), text="Extras")
        self.extras_label.grid(column=1, row=27, pady=10, padx=(0, 5), sticky="w")

        self.target_sell_price_component = ComponentEntry(self.add_build_scrollable_frame.scrollable_frame, "Target Sell Price")
        self.target_sell_price_component.label.grid(column=2, row=27, sticky="ew")
        self.target_sell_price_component.entry.grid(column=2, row=28, sticky="ew")

        self.target_sell_price_component.entry.insert(0, "0.00")

    def add_extra_profit(self):
        self.extra_profit_component = ComponentEntry(self.add_build_scrollable_frame.scrollable_frame, "Extra Profit")
        self.extra_profit_component.label.grid(column=3, row=27, sticky="ew")
        self.extra_profit_component.entry.grid(column=3, row=28, sticky="ew")
        self.extra_profit_component.entry.insert(0, "0.00")

    def add_list_date(self):
        self.list_date_component = ComponentEntry(self.add_build_scrollable_frame.scrollable_frame, "List Date")
        self.list_date_component.label.grid(column=4, row=27,sticky="ew")
        self.list_date_component.entry.grid(column=4, row=28, sticky="ew")

    def add_sell_date(self):
        self.sell_date_component = ComponentEntry(self.add_build_scrollable_frame.scrollable_frame, "Sell Date")
        self.sell_date_component.label.grid(column=2, row=29,sticky="ew")
        self.sell_date_component.entry.grid(column=2, row=30,sticky="ew")

    def add_sell_price(self):
        self.sell_price_component = ComponentEntry(self.add_build_scrollable_frame.scrollable_frame, "Sell Price")
        self.sell_price_component.label.grid(column=3, row=29,sticky="ew")
        self.sell_price_component.entry.grid(column=3, row=30,sticky="ew")
        self.sell_price_component.entry.insert(0, "0.00")

    def add_extra_costs(self):
        self.extra_costs_components = ComponentEntry(self.add_build_scrollable_frame.scrollable_frame, "Extra Costs")
        self.extra_costs_components.label.grid(column=4, row=29, sticky="ew")
        self.extra_costs_components.entry.grid(column=4, row=30, sticky="ew")
        self.extra_costs_components.entry.insert(0, "0.00")

    def hide_build_grid_frame(self):
        """Hide the build grid frame."""
        print("Hidden")
        self.build_scrollable_frame.hide()
        self.build_grid_frame.pack_forget()

    def show_build_grid_frame(self):
        """Show the build grid frame."""
        self.build_grid_frame.pack(fill="x")

    def hide_add_build_grid_frame(self):
        self.add_build_scrollable_frame.hide()
        self.add_build_grid_frame.pack_forget()

    def show_add_build_grid_frame(self):
        self.add_build_grid_frame.pack(fill="x")

    def clear_scene(self):
        for button in self.all_buttons:
            button.grid_forget()
        for label in self.all_labels:
            label.grid_forget()
        for entry in self.all_entries:
            entry.grid_forget()
        self.navigation_grid_frame.grid_forget()
        self.clear_visible_builds()
        self.window.update()

    def change_scene(self, scene):
        self.clear_scene()
        self.build_scrollable_frame.clear()
        self.add_build_scrollable_frame.clear()
        self.clear_all_components()
        clean_unused_skus()

        match scene:
            case Scene.START_SCENE:
                self.add_build_button.grid(in_=self.navigation_grid_frame, column=0, row=1)
                self.show_all_button.grid(in_=self.navigation_grid_frame, column=1, row=1)
            case Scene.ADD_BUILD_SCENE:
                self.add_build_scrollable_frame.show()
                self.go_back_to_start_scene_button.grid(in_=self.navigation_grid_frame, column=1, row=1, pady=5)
                self.save_build_button.grid(in_=self.navigation_grid_frame, column=2, row=1, pady=5)

                # Layout CPU Entries and Labels
                self.add_all_entry_components()
                self.all_extra_components = [self.extra_costs_components, self.target_sell_price_component,
                                             self.extra_profit_component, self.list_date_component,
                                             self.sell_date_component, self.sell_price_component]

                self.all_components = (
                            self.cpu_components + self.gpu_components + self.ram_components + self.motherboard_components + self.ssd_components +
                            self.nvme_components + self.hdd_components + self.psu_components + self.case_components + self.all_extra_components)
                print(self.all_components)

    def go_to_start_scene(self):
        self.hide_add_build_grid_frame()
        self.show_build_grid_frame()
        self.change_scene(Scene.START_SCENE)
        self.build_scrollable_frame.show()

    def go_to_add_build_scene(self):
        self.hide_build_grid_frame()
        self.show_add_build_grid_frame()
        self.change_scene(Scene.ADD_BUILD_SCENE)
        self.add_build_scrollable_frame.show()

        self.new_build_sku = generate_unique_sku()

        self.image_upload_frame = tkinter.Frame(self.add_build_scrollable_frame, bg="lightblue", width=500, height=500)
        self.image_upload_frame.grid(column=2, row=0, pady=20, sticky="nsew", padx=(0, 50))

        self.edit_build_frame = tkinter.Frame(self.add_build_scrollable_frame, bg="lightblue", width=500, height=300)
        self.edit_build_frame.grid(column=2, row=1, pady=20, sticky="nsew", padx=(0, 50))

        self.display_label = tk.Label(self.image_upload_frame, text="No Image Uploaded", bg="lightblue", width=40, height=15)
        self.display_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Set row/column weights so the label can expand
        self.image_upload_frame.grid_columnconfigure(0, weight=1)
        self.image_upload_frame.grid_rowconfigure(0, weight=1)

        self.upload_btn = tk.Button(
            self.image_upload_frame,
            text="Upload Image",
            command=self.open_uploader,
            bg="lightblue",  # Button background color
            activebackground="lightblue",  # Background when active
            relief="flat",  # Remove the button outline
            borderwidth=0,  # No border around the button
            highlightthickness=0  # No highlight outline
        )
        self.upload_btn.grid(row=1, column=0, pady=10, sticky="ew")

        self.new_sku_label = tk.Label(self.image_upload_frame, text=f"Builds SKU: {self.new_build_sku}", bg="lightblue", font=("Arial", 16, "bold"))
        self.new_sku_label.grid(row=2, column=0, stick="ew")

        for component in self.all_components:
            if component is not None and component.label is not None:
                if component.label.cget("text") == "Price":
                    component.entry.insert(0, "0.00")

    @staticmethod
    def show_message_has_no_image():
        messagebox.showinfo("No Image Uploaded!", "Unable to save due to no image uploaded.")

    def open_uploader(self):
        """
        Open the image uploader window and provide a callback to display the selected image.
        """
        open_image_uploader(self.display_image, self.new_build_sku)

    def display_image(self, image_path):
        """
        Display the selected and uploaded image in the display window.

        :param image_path: The file path of the uploaded image.
        """
        img = Image.open(image_path)

        # Resize the image to the desired size (300x250)
        img = img.resize((300, 250), Image.Resampling.LANCZOS)

        self.tk_image = ImageTk.PhotoImage(img)

        self.display_label.configure(image=self.tk_image, text="")

        # Keep a reference to avoid the image being garbage collected
        self.display_label.image = self.tk_image

        # Make sure the label is large enough to display the image
        self.display_label.config(width=300, height=250)

        self.has_image = True

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            clean_unused_skus()
            self.window.destroy()

    def update_labels(self):
        total_builds = len(self.visible_builds)
        for i in range(total_builds):
            self.visible_builds[i].update_build_button = tkinter.Button(text="Update", bg="lightblue", width=4, height=2,
                                                      font=("Arial", 10), borderwidth=0, highlightbackground="white")
            self.visible_builds[i].update_build_button.configure(text=f"{self.visible_builds[i].get_sku()}")
            self.visible_builds[i].update_build_button.grid(in_=self.build_scrollable_frame.scrollable_frame, column=1, row=i, padx=(5, 0))
            self.visible_builds[i].description_label = tkinter.Label(
                self.build_scrollable_frame.scrollable_frame, text=self.visible_builds[i].pc_str, bg='lightblue',
                font=("Arial", 13),
                fg="white",
                anchor="w",  # Align text to the left
                justify="left",  # Left-align multi-line text
                padx=10,  # Add padding on the x-axis
                pady=10,  # Add padding on the y-axis
                wraplength=200
            )
            self.visible_builds[i].description_label.grid(in_=self.build_scrollable_frame.scrollable_frame, column=2, row=i, pady=(25,0))

    def update_photos(self):
        total_builds = len(self.visible_builds)
        for i in range(total_builds):
            image_file_path = self.visible_builds[i].full_pc_dict["image_file_name"]
            self.visible_builds[i].build_image = Canvas(width=350, height=300)
            build_img = resize_image(image_path=f"../images/{image_file_path}", width=350, height=300)
            self.visible_builds[i].build_image.create_image(175, 150, image=build_img)
            self.visible_builds[i].build_image.grid(in_=self.build_scrollable_frame.scrollable_frame, column = 0, row=i)
            self.visible_builds[i].build_image.image = build_img

    def add_pc_build(self, pc_dict, full_pc_dict, sku):
        print(self.visible_builds)
        new_build = PCBuildUI(pc_dict, full_pc_dict, sku)
        self.visible_builds.append(new_build)

    def remove_build(self, sku):
        for build in self.visible_builds:
            for key, value in build.pc_dict.items():
                if key == "sku" and value == sku:
                    build.destroy()
                    self.window.update()
                    self.window.update_idletasks()
                    self.visible_builds.remove(build)
        print(self.visible_builds)

    def clear_visible_builds(self):
        print(self.visible_builds)
        self.build_scrollable_frame.clear()
        for build in self.visible_builds:
            if build is not None:
                build.build_image.grid_forget()
        self.visible_builds = []
        print(self.visible_builds)

    def start(self):
        self.window.mainloop()