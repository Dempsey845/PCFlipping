"""
A simple program to keep track of my pc flipping
"""

class Component:
    """Base class for a PC component."""
    def __init__(self, name: str, brand: str, price: float):
        self.name = name
        self.brand = brand
        self.price = price

    def __str__(self):
        return f"{self.name} ({self.brand}) - £{self.price}"


# CPU class inheriting from Component
class CPU(Component):
    def __init__(self, name: str, brand: str, price: float, cores: int, threads: int, clock_speed: float):
        super().__init__(name, brand, price)
        self.cores = cores
        self.threads = threads
        self.clock_speed = clock_speed  # in GHz

    def __str__(self):
        return f"{super().__str__()} | {self.cores} cores, {self.threads} threads @ {self.clock_speed}GHz"


# GPU class inheriting from Component
class GPU(Component):
    def __init__(self, name: str, brand: str, price: float, memory_size: int, clock_speed: float):
        super().__init__(name, brand, price)
        self.memory_size = memory_size  # in GB
        self.clock_speed = clock_speed  # in MHz

    def __str__(self):
        return f"{super().__str__()} | {self.memory_size}GB VRAM @ {self.clock_speed}MHz"


# RAM class inheriting from Component
class RAM(Component):
    def __init__(self, name: str, brand: str, price: float, capacity: int, speed: int):
        super().__init__(name, brand, price)
        self.capacity = capacity  # in GB
        self.speed = speed  # in MHz

    def __str__(self):
        return f"{super().__str__()} | {self.capacity}GB @ {self.speed}MHz"


# SSD class inheriting from Component
class SSD(Component):
    def __init__(self, name: str, brand: str, price: float, capacity: int, read_speed: int, write_speed: int):
        super().__init__(name, brand, price)
        self.capacity = capacity  # in GB
        self.read_speed = read_speed  # in MB/s
        self.write_speed = write_speed  # in MB/s

    def __str__(self):
        return f"{super().__str__()} | {self.capacity}GB, {self.read_speed}MB/s read, {self.write_speed}MB/s write"


# Hard Drive class inheriting from Component
class HardDrive(Component):
    def __init__(self, name: str, brand: str, price: float, capacity: int, rpm: int):
        super().__init__(name, brand, price)
        self.capacity = capacity  # in GB or TB
        self.rpm = rpm  # Revolutions per minute (RPM)

    def __str__(self):
        return f"{super().__str__()} | {self.capacity}GB @ {self.rpm} RPM"


# NVMe class inheriting from Component
class NVMe(Component):
    def __init__(self, name: str, brand: str, price: float, capacity: int, read_speed: int, write_speed: int):
        super().__init__(name, brand, price)
        self.capacity = capacity  # in GB
        self.read_speed = read_speed  # in MB/s
        self.write_speed = write_speed  # in MB/s

    def __str__(self):
        return f"{super().__str__()} | {self.capacity}GB, {self.read_speed}MB/s read, {self.write_speed}MB/s write"


# PSU class inheriting from Component
class PSU(Component):
    def __init__(self, name: str, brand: str, price: float, wattage: int, efficiency: str):
        super().__init__(name, brand, price)
        self.wattage = wattage  # in Watts
        self.efficiency = efficiency  # Efficiency rating (e.g., 80+ Bronze, Gold)

    def __str__(self):
        return f"{super().__str__()} | {self.wattage}W, {self.efficiency} efficiency"


# Case class inheriting from Component
class Case(Component):
    def __init__(self, name: str, brand: str, price: float, form_factor: str, color: str):
        super().__init__(name, brand, price)
        self.form_factor = form_factor  # e.g., ATX, MicroATX, Mini-ITX
        self.color = color  # Color of the case

    def __str__(self):
        return f"{super().__str__()} | {self.form_factor} form factor, {self.color} color"


# Motherboard class inheriting from Component
class Motherboard(Component):
    def __init__(self, name: str, brand: str, price: float, chipset: str, form_factor: str):
        super().__init__(name, brand, price)
        self.chipset = chipset  # e.g., Intel Z490, AMD B450
        self.form_factor = form_factor  # e.g., ATX, MicroATX, Mini-ITX

    def __str__(self):
        return f"{super().__str__()} | {self.chipset} chipset, {self.form_factor} form factor"


class PCBuild:
    def __init__(self, cpu, gpu, ram, ssd=None, hdd=None, nvme=None, psu=None, case=None, target_sell_price=0, extra_costs=0, extra_profit=0):
        self.cpu = self.validate_component(cpu, "CPU")
        self.gpu = self.validate_component(gpu, "GPU")
        self.ram = self.validate_ram(ram)  # Could be a single RAM component or a list of RAM
        self.ssd = self.validate_component(ssd, "SSD", allow_none=True)
        self.hdd = self.validate_component(hdd, "HardDrive", allow_none=True)
        self.nvme = self.validate_component(nvme, "NVMe", allow_none=True)
        self.psu = self.validate_component(psu, "PSU")
        self.case = self.validate_component(case, "Case")
        self.extra_costs = extra_costs
        self.target_sell_price = target_sell_price
        self.extra_profit = extra_profit # E.g selling old components that were replaced

        self.sold = False
        self.sell_price = 0

        # All components in the build
        self.components = [self.cpu, self.gpu, self.ram, self.ssd, self.hdd, self.nvme, self.psu, self.case]

    def validate_component(self, component, expected_type, allow_none=False):
        """Helper function to validate component types."""
        if allow_none and component is None:
            return None
        if not isinstance(component, Component):
            raise TypeError(f"Expected {expected_type}, but got {type(component).__name__}")
        return component

    def validate_ram(self, ram):
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

    def set_to_sold(self, sell_price):
        #Todo: Write build to text file when sold
        self.sold = True
        self.sell_price = sell_price

    def __str__(self):
        """Return a detailed string representation of the PC build."""
        build_info = "PC Build Components:\n"
        for component in self.components:
            if isinstance(component, list):  # For components like RAM (list of sticks)
                for stick in component:
                    build_info += f" - {stick}\n"
            elif component is not None:
                build_info += f" - {component}\n"
        build_info += f"Extra Costs: £{self.extra_costs}\n"
        build_info += f"Total Price: £{self.total_price()}\n"
        build_info += f"Target Sell Price: £{self.target_sell_price}\n"
        build_info += f"Extra Profit: £{self.extra_profit}\n"
        build_info += f"Target Profit (includes extra profit): £{self.target_profit()}\n"
        build_info += f"Has sold: {self.sold}\n"
        if self.sold:
            build_info += f"Sell price: £{self.sell_price} "
            build_info += f"Total profit: £{(self.sell_price - self.total_price()) + self.extra_profit}"

        return build_info


# Example (one of my builds)
cpu = CPU(name="Ryzen 5 3600", brand="AMD", price=55, cores=6, threads=12, clock_speed=3.6)
gpu = GPU(name="RTX 2060 Super", brand="NVIDIA", price=175, memory_size=8, clock_speed=1750)
ram = RAM(name="Kingston FURY Beast RGB (2x8GB)", brand="Kingston", price=48, capacity=16, speed=3200)
ssd = SSD(name="Samsung 970 EVO", brand="Samsung", price=0, capacity=1000, read_speed=3500, write_speed=2500)
psu = PSU(name="CORSAIR CX650", brand="Corsair", price=0, wattage=650, efficiency="80+ Gold")
case = Case(name="Corsair 220T White", brand="Corsair", price=0, form_factor="ATX", color="White")
motherboard = Motherboard(name="A320M-A", brand="ASUS", price=0, chipset="A320", form_factor="uATX")

pc_build = PCBuild(cpu, gpu, ram, ssd, psu=psu, case=case, extra_costs=180, target_sell_price=600, extra_profit=60)
pc_build.set_to_sold(600)
print(pc_build)

#Todo: take input and save build to a text file