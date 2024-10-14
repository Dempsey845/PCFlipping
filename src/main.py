"""
A simple program to keep track of my pc flipping
"""

import json
import random
import os
import gui

from gui import ComponentEntry
from tkinter import END

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


class Component:
    """Base class for a PC component with only name, brand, and price."""
    def __init__(self, name: str, brand: str, price: float):
        self.name = name
        self.brand = brand
        self.price = price

    def __str__(self):
        return f"{self.__class__.__name__}({self.name}, {self.brand}, {self.price})"


class CPU(Component):
    pass


class GPU(Component):
    pass


class RAM(Component):
    pass


class SSD(Component):
    pass


class HardDrive(Component):
    pass


class NVMe(Component):
    pass


class PSU(Component):
    pass


class Case(Component):
    pass


class Motherboard(Component):
    pass


def string_to_component(component_str: str):
    """
    Convert a string representation of a component back to a Component object.
    Format: ClassName(name, brand, price)
    """

    if not component_str:
        print("No component string provided.")
        return None  # or raise ValueError("component_str must not be None or empty")

    try:
        component_type, attrs = component_str.split('(', 1)
        attrs = attrs.rstrip(')').split(',')

        # Check if we have the right number of attributes
        if len(attrs) != 3:
            raise ValueError(f"Incorrect number of attributes for {component_type}: {component_str}")

        name = attrs[0].strip()
        brand = attrs[1].strip()
        price = float(attrs[2].strip())

        if component_type == "CPU":
            return CPU(name, brand, price)
        elif component_type == "GPU":
            return GPU(name, brand, price)
        elif component_type == "SSD":
            return SSD(name, brand, price)
        elif component_type == "RAM":
            return RAM(name, brand, price)
        elif component_type == "HardDrive":
            return HardDrive(name, brand, price)
        elif component_type == "NVMe":
            return NVMe(name, brand, price)
        elif component_type == "PSU":
            return PSU(name, brand, price)
        elif component_type == "Case":
            return Case(name, brand, price)
        elif component_type == "Motherboard":
            return Motherboard(name, brand, price)
        else:
            raise ValueError(f"Unknown component type: {component_type} in {component_str}")

    except Exception as e:
        print(f"Error parsing component string '{component_str}': {e}")
        return None


class PCBuild:
    def __init__(self, sku, cpu, gpu, ram, motherboard,
                 ssd=None, hdd=None, nvme=None, psu=None, case=None,
                 target_sell_price=0.0, extra_costs=0.0, extra_profit=0.0,
                 list_date="01/01/2024", sell_date="02/01/2024"):

        # Validate and set components
        self.cpu = self.validate_component(cpu, "CPU")
        self.gpu = self.validate_component(gpu, "GPU")
        self.ram = self.validate_component(ram, "RAM")
        self.motherboard = self.validate_component(motherboard, "Motherboard")
        self.ssd = self.validate_component(ssd, "SSD", allow_none=True)
        self.hdd = self.validate_component(hdd, "HDD", allow_none=True)
        self.nvme = self.validate_component(nvme, "NVMe", allow_none=True)
        self.psu = self.validate_component(psu, "PSU")
        self.case = self.validate_component(case, "Case")

        # Other build attributes
        self.extra_costs = extra_costs
        self.target_sell_price = target_sell_price
        self.extra_profit = extra_profit
        self.list_date = list_date
        self.sell_date = sell_date
        self.sold = False
        self.sell_price = 0

        # Image and SKU management
        self.image_file_name = f"{sku}.png"
        self.image_path = None

        self.sku = sku
        self.components = [self.cpu, self.gpu, self.ram, self.ssd, self.hdd, self.nvme, self.psu, self.case]

        # Update the build in a persistent storage (e.g., JSON)
        self.update_build_in_json(self.sku, self.to_dict())

    @staticmethod
    def validate_component(component, expected_type, allow_none=False):
        """Helper function to validate component types."""
        if allow_none and component is None:
            return None
        if not isinstance(component, Component):
            raise TypeError(f"Expected {expected_type}, but got {type(component).__name__}")
        return component

    def total_price(self):
        """Calculate the total price of the build including extra costs."""
        total = 0
        for component in self.components:
            if component is not None:
                total += component.price
        return total + self.extra_costs

    def target_profit(self):
        """Calculate profit based on the target sell price."""
        return (self.target_sell_price - self.total_price()) + self.extra_profit

    def update_extra_costs(self, new_extra_costs):
        """Update the extra costs, e.g., for shipping, labor, etc."""
        self.extra_costs = new_extra_costs
        self.update_build_in_json(self.sku, self.to_dict())

    def set_to_sold(self, sell_price, sell_date):
        """Mark the build as sold and update the selling information."""
        self.sold = True
        self.sell_price = sell_price
        self.sell_date = sell_date

        self.update_build_in_json(self.sku, self.to_dict())

    def update_build(self, extra_costs, sold, sell_price, sell_date):
        """Update the entire build, use this when reading a build from Build.json."""
        self.update_extra_costs(extra_costs)
        if sold:
            self.set_to_sold(sell_price, sell_date)

    def to_dict(self):
        """Serialize the PCBuild object to a dictionary for JSON storage."""
        return {
            "cpu": str(self.cpu),
            "gpu": str(self.gpu),
            "motherboard": str(self.motherboard),
            "ram": str(self.ram),
            "ssd": str(self.ssd) if self.ssd else None,
            "hdd": str(self.hdd) if self.hdd else None,
            "nvme": str(self.nvme) if self.nvme else None,
            "psu": str(self.psu),
            "case": str(self.case),
            "extra_costs": self.extra_costs,
            "target_sell_price": self.target_sell_price,
            "extra_profit": self.extra_profit,
            "list_date": self.list_date,
            "sell_date": self.sell_date,
            "sold": self.sold,
            "sell_price": self.sell_price,
            "sku": self.sku,
            "image_file_name": self.image_file_name
        }

    def to_dict_name(self):
        """Serialize the PCBuild object to a dictionary with component names."""
        return {
            "sku": self.sku,
            "CPU": self.cpu.name,
            "GPU": self.gpu.name,
            "RAM": self.ram.name,
            "Motherboard": self.motherboard.name,
            "SSD": self.ssd.name if self.ssd else None,
            "HDD": self.hdd.name if self.hdd else None,
            "NVME": self.nvme.name if self.nvme else None,
            "PSU": self.psu.name,
            "Case": self.case.name,
            "Extra Costs": self.extra_costs,
            "Target Sell Price": self.target_sell_price,
            "Extra Profit": self.extra_profit,
            "List Date": self.list_date,
            "Sell Date": self.sell_date,
            "Sell Price": self.sell_price,
            "Total Price": self.total_price(),
            "Total Profit": (self.sell_price - self.total_price()) + self.extra_profit
        }

    def set_sku(self, sku):
        """Set the SKU for the build."""
        self.sku = sku

    def add_image(self, image_file_name):
        """Set the image file name and compute the image path."""
        self.image_file_name = image_file_name
        self.image_path = os.path.join('..', 'images', image_file_name)

    @staticmethod
    def update_build_in_json(sku, updated_data):
        """
        Update an existing build in Builds.json based on the given SKU.
        If the build doesn't exist, add the new build to the file.

        :param sku: The SKU of the build to update or add.
        :param updated_data: A dictionary containing the updated fields for the build.
        """
        file_path = os.path.join('..', 'data', 'Builds.json')

        try:
            # Load existing builds from JSON file
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    data = json.load(file)

                    # Ensure 'builds' key exists and is a list
                    if 'builds' not in data or not isinstance(data['builds'], list):
                        raise ValueError("'builds' key is missing or is not a list in the JSON file.")
            else:
                # If the file doesn't exist, create an empty builds structure
                data = {"builds": []}

            #  Try to find the build with the matching SKU (handle both int and str types)
            build_found = False
            for build in data['builds']:
                if str(build['sku']) == str(sku):
                    # Step 3: Update the build if it exists
                    build.update(updated_data)
                    build_found = True
                    break

            if not build_found:
                # If no build found, append the new build with the given SKU
                updated_data['sku'] = sku  # Ensure the SKU is added to the new build
                data['builds'].append(updated_data)
                print(f"No build found with SKU {sku}. Adding a new build.")

            # Write the updated list back to the file
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)

            print(f"Build with SKU {sku} has been successfully updated or added.")

        except Exception as e:
            print(f"Error updating or adding build: {e}")

    def __str__(self):
        """Return a detailed string representation of the PC build."""
        build_info = "PC Build Components:\n"
        for component in self.components:
            if isinstance(component, list):  # For components like RAM (list of sticks)
                for stick in component:
                    build_info += f" - {stick}\n"
            elif component is not None:
                build_info += f" - {component}\n"
        build_info += f"SKU: {self.sku}\n"
        build_info += f"List Date: {self.list_date}\n"
        build_info += f"Extra Costs: £{self.extra_costs}\n"
        build_info += f"Total Price: £{self.total_price()}\n"
        build_info += f"Target Sell Price: £{self.target_sell_price}\n"
        build_info += f"Extra Profit: £{self.extra_profit}\n"
        build_info += f"Target Profit (includes extra profit): £{self.target_profit()}\n"
        build_info += f"Has Sold: {self.sold}\n"
        if self.sold:
            build_info += f"Sell Price: £{self.sell_price} "
            build_info += f"Total Profit: £{(self.sell_price - self.total_price()) + self.extra_profit}\n"
            build_info += f"Sell Date: {self.sell_date}"

        return build_info


def load_build_from_sku(sku):
    file_path = os.path.join('..', 'data', 'Builds.json')

    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
        else:
            print(f"No builds file found at {file_path}.")
            return None

        if 'builds' not in data or not data['builds']:
            print("No builds found in the data.")
            return None

        for build in data['builds']:
            print(build)  # Debugging line to see what's being processed
            if str(build.get('sku')) == str(sku):
                # Load components safely
                print(f"Cpu from {sku} is {build["cpu"]}")
                cpu = string_to_component(build["cpu"])
                gpu = string_to_component(build["gpu"])
                ram = string_to_component(build["ram"])
                ssd = string_to_component(build["ssd"]) if build.get("ssd") else None
                hdd = string_to_component(build["hdd"]) if build.get("hdd") else None
                nvme = string_to_component(build["nvme"]) if build.get("nvme") else None
                psu = string_to_component(build["psu"])
                case = string_to_component(build["case"])
                motherboard = string_to_component(build["motherboard"])

                pc_build = PCBuild(
                    sku=sku, cpu=cpu, gpu=gpu, ram=ram,
                    ssd=ssd, hdd=hdd, nvme=nvme,
                    psu=psu, case=case, motherboard=motherboard,
                    target_sell_price=build.get("target_sell_price", 0),
                    extra_costs=build.get("extra_costs", 0),
                    extra_profit=build.get("extra_profit", 0),
                    list_date=build.get("list_date", "01/01 2024"),
                    sell_date=build.get("sell_date", "02/01 2024")
                )

                pc_build.update_build(
                    build.get("extra_costs", 0),
                    build.get("sold", False),
                    build.get("sell_price", 0),
                    build.get("sell_date", None)
                )
                return pc_build
        print(f"No build found with SKU {sku}.")
        return None
    except Exception as e:
        print(f"Error reading a build with SKU {sku}: {e}")
        return None

def add_build_to_window(sku_):
    pc_build = load_build_from_sku(sku_)
    pc_dict = pc_build.to_dict_name()
    full_pc_dict = pc_build.to_dict()
    gui_.window.after(100, gui_.add_pc_build(pc_dict=pc_dict, sku=sku_, full_pc_dict=full_pc_dict))
    return pc_dict

def show_all_builds():
    gui_.clear_visible_builds()
    file_path = os.path.join('..', 'data', 'SKUS.json')
    with open(file_path) as file:
        data = json.load(file)

    skus = data["SKUS"]

    for sku in skus:
        pc_build = load_build_from_sku(sku)
        if pc_build is not None:
            pc_dict = pc_build.to_dict_name()
            pc_dict_full = pc_build.to_dict()
            gui_.window.after(100, gui_.add_pc_build(pc_dict, pc_dict_full, sku, pc_build))

    gui_.update_photos()
    gui_.update_labels()

    gui_.window.update()
    gui_.window.update_idletasks()

def add_build_from_entries():
    if not gui_.has_image:
        gui_.show_message_has_no_image()
        return

    for component in gui_.all_components:
        print(component)

    # Extract CPU data
    cpu_name = gui_.cpu_components[1].entry.get()  # Use .get() to retrieve text
    cpu_brand = gui_.cpu_components[2].entry.get()
    cpu_price = float(gui_.cpu_components[3].entry.get())  # Convert to float after getting the text

    # Extract GPU data
    gpu_name = gui_.gpu_components[1].entry.get()
    gpu_brand = gui_.gpu_components[2].entry.get()
    gpu_price = float(gui_.gpu_components[3].entry.get())

    # Extract RAM data
    ram_name = gui_.ram_components[1].entry.get()
    ram_brand = gui_.ram_components[2].entry.get()
    ram_price = float(gui_.ram_components[3].entry.get())

    # Check if an SSD is included and extract data if so
    has_a_ssd = gui_.ssd_components[4].is_checked.get()
    print(f"Has a ssd: {gui_.ssd_components[4].is_checked}")
    if has_a_ssd:
        ssd_name = gui_.ssd_components[1].entry.get()
        ssd_brand = gui_.ssd_components[2].entry.get()
        ssd_price = float(gui_.ssd_components[3].entry.get())
    else:
        ssd_name = ssd_brand = ssd_price = None

    # Check if an HDD is included and extract data if so
    has_a_hdd = gui_.hdd_components[4].is_checked.get()
    if has_a_hdd:
        hdd_name = gui_.hdd_components[1].entry.get()
        hdd_brand = gui_.hdd_components[2].entry.get()
        hdd_price = float(gui_.hdd_components[3].entry.get())
    else:
        hdd_name = hdd_brand = hdd_price = None

    # Check if an NVMe is included and extract data if so
    has_a_nvme = gui_.nvme_components[4].is_checked.get()
    if has_a_nvme:
        nvme_name = gui_.nvme_components[1].entry.get()
        nvme_brand = gui_.nvme_components[2].entry.get()
        nvme_price = float(gui_.nvme_components[3].entry.get())
    else:
        nvme_name = nvme_brand = nvme_price = None

    # Extract PSU data
    psu_name = gui_.psu_components[1].entry.get()
    psu_brand = gui_.psu_components[2].entry.get()
    psu_price = float(gui_.psu_components[3].entry.get())

    # Extract Case data
    case_name = gui_.case_components[1].entry.get()
    case_brand = gui_.case_components[2].entry.get()
    case_price = float(gui_.case_components[3].entry.get())

    # Extract Motherboard data
    motherboard_name = gui_.motherboard_components[1].entry.get()
    motherboard_brand = gui_.motherboard_components[2].entry.get()
    motherboard_price = float(gui_.motherboard_components[3].entry.get())

    # Extract additional costs and pricing details
    extra_costs = float(gui_.extra_costs_components.entry.get())
    sell_price = float(gui_.sell_price_component.entry.get())
    sell_date = gui_.sell_date_component.entry.get()  # Assuming this is a date string in the appropriate format
    target_sell_price = float(gui_.target_sell_price_component.entry.get())
    extra_profit = float(gui_.extra_profit_component.entry.get())
    list_date = gui_.list_date_component.entry.get()

    # Create the components for the build with the extracted data
    cpu = CPU(name=cpu_name, brand=cpu_brand, price=cpu_price)
    gpu = GPU(name=gpu_name, brand=gpu_brand, price=gpu_price)
    ram = RAM(name=ram_name, brand=ram_brand, price=ram_price)
    ssd = SSD(name=ssd_name, brand=ssd_brand, price=ssd_price) if has_a_ssd else None
    hdd = HardDrive(name=hdd_name, brand=hdd_brand, price=hdd_price) if has_a_hdd else None
    nvme = NVMe(name=nvme_name, brand=nvme_brand, price=nvme_price) if has_a_nvme else None
    psu = PSU(name=psu_name, brand=psu_brand, price=psu_price)
    case = Case(name=case_name, brand=case_brand, price=case_price)
    motherboard = Motherboard(name=motherboard_name, brand=motherboard_brand, price=motherboard_price)

    # Create the PCBuild object
    pc_build = PCBuild(
        sku=gui_.new_build_sku,
        cpu=cpu,
        gpu=gpu,
        ram=ram,
        motherboard=motherboard,
        ssd=ssd,
        hdd=hdd,
        nvme=nvme,
        psu=psu,
        case=case,
        extra_costs=extra_costs,
        target_sell_price=target_sell_price,
        extra_profit=extra_profit,
        list_date=list_date
    )

    # Mark the build as sold
    pc_build.set_to_sold(sell_price, sell_date)

    # Print or store the build object as needed
    print(pc_build)

gui_ = gui.GUI()
gui_.show_all_button["command"] = show_all_builds
gui_.clear_visible_builds()
gui_.save_build_button.configure(command=add_build_from_entries)

gui_.start()