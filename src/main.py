"""
A simple program to keep track of my pc flipping
"""

import json
import random
import os

import gui

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
    """Base class for a PC component."""
    def __init__(self, name: str, brand: str, price: float):
        self.name = name
        self.brand = brand
        self.price = price

    def convert_component_to_string(self):
        return f"{self.__class__.__name__}({self.name},{self.brand},{self.price})"

    def __str__(self):
        return self.convert_component_to_string()


# CPU class inheriting from Component
class CPU(Component):
    def __init__(self, name: str, brand: str, price: float, cores: int, threads: int, clock_speed: float):
        super().__init__(name, brand, price)
        self.cores = cores
        self.threads = threads
        self.clock_speed = clock_speed  # in GHz

    def convert_component_to_string(self):
        return f"CPU({self.name},{self.brand},{self.price},{self.cores},{self.threads},{self.clock_speed})"

    def __str__(self):
        return self.convert_component_to_string()


# GPU class inheriting from Component
class GPU(Component):
    def __init__(self, name: str, brand: str, price: float, memory_size: int, clock_speed: float):
        super().__init__(name, brand, price)
        self.memory_size = memory_size  # in GB
        self.clock_speed = clock_speed  # in MHz

    def convert_component_to_string(self):
        return f"GPU({self.name},{self.brand},{self.price},{self.memory_size},{self.clock_speed})"

    def __str__(self):
        return self.convert_component_to_string()


# RAM class inheriting from Component
class RAM(Component):
    def __init__(self, name: str, brand: str, price: float, capacity: int, speed: int):
        super().__init__(name, brand, price)
        self.capacity = capacity  # in GB
        self.speed = speed  # in MHz

    def convert_component_to_string(self):
        return f"RAM({self.name},{self.brand},{self.price},{self.capacity},{self.speed})"

    def __str__(self):
        return self.convert_component_to_string()


# SSD class inheriting from Component
class SSD(Component):
    def __init__(self, name: str, brand: str, price: float, capacity: int, read_speed: int, write_speed: int):
        super().__init__(name, brand, price)
        self.capacity = capacity  # in GB
        self.read_speed = read_speed  # in MB/s
        self.write_speed = write_speed  # in MB/s

    def convert_component_to_string(self):
        return f"SSD({self.name},{self.brand},{self.price},{self.capacity},{self.read_speed},{self.write_speed})"

    def __str__(self):
        return self.convert_component_to_string()


# Hard Drive class inheriting from Component
class HardDrive(Component):
    def __init__(self, name: str, brand: str, price: float, capacity: int, rpm: int):
        super().__init__(name, brand, price)
        self.capacity = capacity  # in GB or TB
        self.rpm = rpm  # Revolutions per minute (RPM)

    def convert_component_to_string(self):
        return f"HardDrive({self.name},{self.brand},{self.price},{self.capacity},{self.rpm})"

    def __str__(self):
        return self.convert_component_to_string()


# NVMe class inheriting from Component
class NVMe(Component):
    def __init__(self, name: str, brand: str, price: float, capacity: int, read_speed: int, write_speed: int):
        super().__init__(name, brand, price)
        self.capacity = capacity  # in GB
        self.read_speed = read_speed  # in MB/s
        self.write_speed = write_speed  # in MB/s

    def convert_component_to_string(self):
        return f"NVMe({self.name},{self.brand},{self.price},{self.capacity},{self.read_speed},{self.write_speed})"

    def __str__(self):
        return self.convert_component_to_string()


# PSU class inheriting from Component
class PSU(Component):
    def __init__(self, name: str, brand: str, price: float, wattage: int, efficiency: str):
        super().__init__(name, brand, price)
        self.wattage = wattage  # in Watts
        self.efficiency = efficiency  # Efficiency rating (e.g., 80+ Bronze, Gold)

    def convert_component_to_string(self):
        return f"PSU({self.name},{self.brand},{self.price},{self.wattage},{self.efficiency})"

    def __str__(self):
        return self.convert_component_to_string()


# Case class inheriting from Component
class Case(Component):
    def __init__(self, name: str, brand: str, price: float, form_factor: str, color: str):
        super().__init__(name, brand, price)
        self.form_factor = form_factor  # e.g., ATX, MicroATX, Mini-ITX
        self.color = color  # Color of the case

    def convert_component_to_string(self):
        return f"Case({self.name},{self.brand},{self.price},{self.form_factor},{self.color})"

    def __str__(self):
        return self.convert_component_to_string()


# Motherboard class inheriting from Component
class Motherboard(Component):
    def __init__(self, name: str, brand: str, price: float, chipset: str, form_factor: str):
        super().__init__(name, brand, price)
        self.chipset = chipset  # e.g., Intel Z490, AMD B450
        self.form_factor = form_factor  # e.g., ATX, MicroATX, Mini-ITX

    def convert_component_to_string(self):
        return f"Motherboard({self.name},{self.brand},{self.price},{self.chipset},{self.form_factor})"

    def __str__(self):
        return self.convert_component_to_string()


def string_to_component(component_str: str):
    """
    Convert a string representation of a component back to a Component object.
    Format: ClassName(attr1, attr2, attr3, ...)
    """
    if component_str[0:3] == "RAM":
        print("Ram")


    component_type, attrs = component_str.split('(', 1)
    attrs = attrs.rstrip(')').split(',')

    if component_type == "CPU":
        return CPU(attrs[0], attrs[1], float(attrs[2]), int(attrs[3]), int(attrs[4]), float(attrs[5]))
    elif component_type == "GPU":
        return GPU(attrs[0], attrs[1], float(attrs[2]), int(attrs[3]), float(attrs[4]))
    elif component_type == "SSD":
        return SSD(attrs[0], attrs[1], float(attrs[2]), int(attrs[3]), int(attrs[4]), int(attrs[5]))
    elif component_type == "HardDrive":
        return HardDrive(attrs[0], attrs[1], float(attrs[2]), int(attrs[3]), int(attrs[4]))
    elif component_type == "NVMe":
        return NVMe(attrs[0], attrs[1], float(attrs[2]), int(attrs[3]), int(attrs[4]), int(attrs[5]))
    elif component_type == "PSU":
        return PSU(attrs[0], attrs[1], float(attrs[2]), int(attrs[3]), attrs[4])
    elif component_type == "Case":
        return Case(attrs[0], attrs[1], float(attrs[2]), attrs[3], attrs[4])
    elif component_type == "Motherboard":
        return Motherboard(attrs[0], attrs[1], float(attrs[2]), attrs[3], attrs[4])
    else:
        raise ValueError(f"Unknown component type: {component_type}")


class PCBuild:
    def __init__(self, cpu, gpu, ram, motherboard, create_new_sku=True, sku=-1, ssd=None, hdd=None, nvme=None, psu=None, case=None, target_sell_price=0, extra_costs=0, extra_profit=0, list_date="01/01 2024", sell_date="02/01 2024"):
        self.cpu = self.validate_component(cpu, "CPU")
        self.gpu = self.validate_component(gpu, "GPU")
        self.ram = self.validate_ram(ram)  # Could be a single RAM component or a list of RAM
        self.motherboard = motherboard
        self.ssd = self.validate_component(ssd, "SSD", allow_none=True)
        self.hdd = self.validate_component(hdd, "HardDrive", allow_none=True)
        self.nvme = self.validate_component(nvme, "NVMe", allow_none=True)
        self.psu = self.validate_component(psu, "PSU")
        self.case = self.validate_component(case, "Case")
        self.extra_costs = extra_costs
        self.target_sell_price = target_sell_price
        self.extra_profit = extra_profit # E.g selling old components that were replaced

        self.list_date = list_date
        self.sell_date = sell_date
        self.sold = False
        self.sell_price = 0

        if create_new_sku:
            self.sku = generate_unique_sku()
        else:
            self.sku = sku
        self.components = [self.cpu, self.gpu, self.ram, self.ssd, self.hdd, self.nvme, self.psu, self.case]
        self.update_build_in_json(self.sku, self.to_dict())

    @staticmethod
    def validate_component(component, expected_type, allow_none=False):
        """Helper function to validate component types."""
        if allow_none and component is None:
            return None
        if not isinstance(component, Component):
            raise TypeError(f"Expected {expected_type}, but got {type(component).__name__}")
        return component

    @staticmethod
    def validate_ram(ram):
        """Validate if the RAM is a single component or a list of RAM components."""
        if isinstance(ram, list):
            for stick in ram:
                if not isinstance(stick, RAM):
                    raise TypeError(f"All RAM sticks must be of type RAM, got {type(stick).__name__}")
            return ram
        elif isinstance(ram, RAM):
            return [ram]  # Wrap single RAM in a list
        else:
            raise TypeError(f"Expected RAM or a list of RAM, but got {type(ram).__name__}")

    def total_price(self):
        """Calculate the total price of the build including extra costs."""
        total = 0
        for component in self.components:
            if isinstance(component, list):  # Handle list of components like RAM
                total += sum([comp.price for comp in component])
            elif component is not None:
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
        self.sold = True
        self.sell_price = sell_price
        self.sell_date = sell_date

        self.update_build_in_json(self.sku, self.to_dict())

    def update_build(self, extra_cots, sold, sell_price, sell_date):
        """Update the entire build, use this when reading a build from Build.json"""
        """Make sure to update load_build_from_sku() when updating this function"""
        self.update_extra_costs(extra_cots)
        if sold:
            self.set_to_sold(sell_price, sell_date)

    def to_dict(self):
        """Serialize the PCBuild object to a dictionary."""
        return {
            "cpu": str(self.cpu),
            "gpu": str(self.gpu),
            "ram": [str(ram) for ram in self.ram],
            "motherboard": str(self.motherboard),
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
            "sku": self.sku
        }

    def to_dict_name(self):
        """Serialize the PCBuild object (names) to a dictionary."""
        return {
            "CPU": self.cpu.name,
            "GPU": self.gpu.name,
            "RAM": [self.ram.name for self.ram in self.ram],
            "Motherboard": self.motherboard.name,
            "SSD": self.ssd.name if self.ssd else None,
            "HDD": self.hdd.name if self.hdd else None,
            "NVME": self.nvme.name if self.nvme else None,
            "PSU": self.psu.name,
            "Case": self.case.name,
            "Extra Costs": self.extra_costs,
            "Targets Sell Price": self.target_sell_price,
            "Extra Profit": self.extra_profit,
            "List Date": self.list_date,
            "Sell Date": self.sell_date,
            "Sell Price": self.sell_price,
        }

    def set_sku(self, sku):
        self.sku = sku

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
        # Load existing builds from JSON file
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
        else:
            # If the file doesn't exist, create an empty builds structure
            data = {"builds": []}

        #  Try to find the build with the matching SKU
        build_found = False
        for build in data['builds']:
            if str(build['sku']) == str(sku):
                build_found = True

                cpu = string_to_component(build["cpu"])
                gpu = string_to_component(build["gpu"])
                #ram = string_to_component(build["ram"])

                ssd = None
                if build["ssd"] is not None:
                    ssd = string_to_component(build["ssd"])

                hdd = None
                if build["hdd"] is not None:
                    hdd = string_to_component(build["hdd"])

                nvme = None
                if build["nvme"] is not None:
                    nvme = string_to_component(build["nvme"])

                psu = string_to_component(build["psu"])
                case = string_to_component(build["case"])
                motherboard = string_to_component(build["motherboard"])

                ram = RAM(name="Kingston FURY Beast RGB (2x8GB)", brand="Kingston", price=48, capacity=16, speed=3200)

                pc_build = PCBuild(create_new_sku=False, sku=sku, cpu=cpu, gpu=gpu, ram=ram, ssd=ssd, hdd=hdd, nvme=nvme,
                                   psu=psu, case=case, motherboard=motherboard, target_sell_price=build["target_sell_price"], extra_costs=build["extra_costs"],
                                   extra_profit=build["extra_profit"], list_date=build["list_date"], sell_date=build["sell_date"])

                pc_build.update_build(build["extra_costs"], build["sold"], build["sell_price"], build["sell_date"])
                return pc_build
        if not build_found:
            print(f"No build found with SKU {sku}.")
            return None
    except Exception as e:
        print(f"Error reading a build with SKU {sku}: {e}")
        return None

# Create a PC Build which gets added to Builds.json
"""
cpu = CPU(name="Ryzen 5 3600", brand="AMD", price=55, cores=6, threads=12, clock_speed=3.6)
gpu = GPU(name="RTX 2060 Super", brand="NVIDIA", price=175, memory_size=8, clock_speed=1750)
ram = RAM(name="Kingston FURY Beast RGB (2x8GB)", brand="Kingston", price=48, capacity=16, speed=3200)
ssd = SSD(name="Samsung 970 EVO", brand="Samsung", price=0, capacity=1000, read_speed=3500, write_speed=2500)
hdd = HardDrive(name="Seagate 3.5\" ", brand="Seagate", price=0, capacity=1000, rpm=1200)
psu = PSU(name="CORSAIR CX650", brand="Corsair", price=0, wattage=650, efficiency="80+ Gold")
case = Case(name="Corsair 220T White", brand="Corsair", price=0, form_factor="ATX", color="White")
motherboard = Motherboard(name="A320M-A", brand="ASUS", price=0, chipset="A320", form_factor="uATX")

pc_build = PCBuild(cpu=cpu, gpu=gpu, ram=ram, motherboard=motherboard, ssd=ssd, psu=psu, case=case, extra_costs=180, target_sell_price=600, extra_profit=60)
pc_build.set_to_sold(600, "10/10 2024")
print(pc_build)
"""

# Load build from Build.json using its SKU
pc_build = load_build_from_sku(3201)

gui_ = gui.GUI(pc_build)