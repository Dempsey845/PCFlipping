import tkinter
import time
from tkinter import messagebox, Entry, Label
from enum import Enum

class PCBuildUI:
    def __init__(self, pc_dict, sku):
        self.description_label = None
        self.packed = False
        self.pc_dict = pc_dict
        self.build_sku_label = tkinter.Label(text=sku, font=("Arial", 14))
        self.build_sku_label.pack()
        self.pc_str = ""

        for key, value in pc_dict.items():
            if value is not None and key != "ram" and key != "sku":
                self.pc_str += f"{key}: {value}\n"
            elif key == "RAM":
                self.pc_str += f"{key}: {"".join(value)}\n"

    def pack(self):
        if not self.packed:
            self.description_label = tkinter.Label(text=self.pc_str, font=("Arial", 12))
            self.description_label.pack()
            self.packed = True

    def get_sku(self):
        return self.pc_dict["sku"]

    def destroy(self):
        self.description_label.destroy()
        self.build_sku_label.destroy()

class Scene(Enum):
    START_SCENE = 1
    ADD_BUILD_SCENE = 2

class GUI:
    """
    TODO - LIST OF BUILDS FROM Builds.json ON THE GUI (scrollable)
    TODO - IMPLEMENT PHOTOS FOR EACH BUILD
    TODO - IMPLEMENT ADDING A BUILD AND REMOVING A BUILD
    TODO - IMPLEMENT SORTING BUILDS BY DIFFERENT TYPES E.G list-date, profit, cpu, cpu-brand, etc...
    """
    def __init__(self):
        self.running = True
        self.scene = Scene.START_SCENE
        self.window = tkinter.Tk()
        self.window.title("PC Flipping")
        self.window.minsize(width=800, height=1000)

        self.title_label = tkinter.Label(text="PC Flipping", font=("Arial", 26, "bold"))
        self.title_label.pack()

        # Start Scene Variables
        self.add_build_button = tkinter.Button(text="Add Build", command=self.go_to_add_build_scene)
        self.show_all_button = tkinter.Button(text="Show All Builds")
        self.visible_builds = []

        # Add Build Scene Variables
        self.go_back_to_start_scene_button = tkinter.Button(text="<-Go Back", command=self.go_to_start_scene)
        self.show_all_button.pack()
        self.add_build_button.pack()

        self.all_buttons = [self.add_build_button, self.show_all_button, self.go_back_to_start_scene_button]
        self.all_build_labels = []
        self.all_build_entries = []

        # TODO - CREATE A CLASS TO CLEAN UP THIS REPEATED CODE
        # Cpu Name Entry
        self.cpu_name_entry_label = Label(text="Cpu Name", font=("Arial", 12, "bold"))
        self.all_build_labels.append(self.cpu_name_entry_label)
        self.cpu_name_entry = Entry()
        self.all_build_entries.append(self.cpu_name_entry)

        # Cpu Brand Entry
        self.cpu_brand_entry_label = Label(text="Cpu Brand", font=("Arial", 12, "bold"))
        self.all_build_labels.append(self.cpu_brand_entry_label)
        self.cpu_brand_entry = Entry()
        self.all_build_entries.append(self.cpu_brand_entry)

        # Cpu Price Entry
        self.cpu_price_entry_label = Label(text="Cpu Price", font=("Arial", 12, "bold"))
        self.all_build_labels.append(self.cpu_price_entry_label)
        self.cpu_price_entry = Entry()
        self.all_build_entries.append(self.cpu_price_entry)

        self.all_labels = self.all_build_labels + []
        self.all_entries = self.all_build_entries + []

        self.go_to_start_scene()

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def clear_scene(self):
        for button in self.all_buttons:
            button.pack_forget()
        for label in self.all_labels:
            label.pack_forget()
        for entry in self.all_entries:
            entry.pack_forget()
        self.clear_visible_builds()
        self.window.update()

    def change_scene(self, scene):
        self.clear_scene()

        match scene:
            case Scene.START_SCENE:
                self.add_build_button.pack()
                self.show_all_button.pack()
            case Scene.ADD_BUILD_SCENE:
                self.go_back_to_start_scene_button.pack()
                for i in range(len(self.all_build_entries)):
                    self.all_build_labels[i].pack()
                    self.all_build_entries[i].pack()

    def go_to_start_scene(self):
        self.change_scene(Scene.START_SCENE)

    def go_to_add_build_scene(self):
        self.change_scene(Scene.ADD_BUILD_SCENE)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.window.destroy()

    def update_labels(self):
        for build in self.visible_builds:
            build.pack()

    def add_pc_build(self, pc_dict, sku):
        new_build = PCBuildUI(pc_dict, sku)
        self.visible_builds.append(new_build)
        self.update_labels()

    def remove_build(self, sku):
        for build in self.visible_builds:
            for key, value in build.pc_dict.items():
                if key == "sku" and value == sku:
                    time.sleep(0.1)
                    build.destroy()
                    self.visible_builds.remove(build)
        print(self.visible_builds)

    def clear_visible_builds(self):
        if self.visible_builds is None:
            return

        print(self.visible_builds)
        for build in self.visible_builds:
            self.remove_build(build.get_sku())
        try:
            self.remove_build(self.visible_builds[0].get_sku())
        except IndexError:
            print("clear_visible_builds is empty")

    def start(self):
        self.window.mainloop()