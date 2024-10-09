import tkinter
import time
from tkinter import messagebox, Entry, Label, Canvas, PhotoImage
from enum import Enum

class ScrollableFrame(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Create a canvas
        self.canvas = tkinter.Canvas(self, bg='lightblue')
        self.scrollable_frame = tkinter.Frame(self.canvas, bg='lightblue')

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

        self.pc_str = ""

        self.build_image = None


        for key, value in pc_dict.items():
            if value is not None and key != "ram" and key != "sku":
                self.pc_str += f"{key}: {value}\n"
            elif key == "RAM":
                self.pc_str += f"{key}: {"".join(value)}\n"

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

class GUI:
    """
    TODO - IMPLEMENT PHOTOS FOR EACH BUILD
    TODO - IMPLEMENT ADDING A BUILD AND REMOVING A BUILD
    TODO - IMPLEMENT SORTING BUILDS BY DIFFERENT TYPES E.G list-date, profit, cpu, cpu-brand, etc...
    """
    def __init__(self):
        self.running = True
        self.scene = "START_SCENE"

        # Create main window
        self.window = tkinter.Tk()
        self.window.title("PC Flipping")

        # Set the window size explicitly
        self.window.geometry("600x1000")  # Set the initial size of the window
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
        self.build_grid_frame = tkinter.Frame(self.window, bg="lightblue", width=600, height=800)
        self.build_grid_frame.pack_propagate(False)  # Prevent resizing to fit contents
        self.build_grid_frame.pack(fill="x")  # Fill horizontally but fixed width

        # Create scrollable frame within the light blue frame
        self.build_scrollable_frame = ScrollableFrame(self.build_grid_frame)
        self.build_scrollable_frame.pack(fill="both", expand=True)

        # Start Scene Variables
        self.add_build_button = tkinter.Button(text="Add Build", command=self.go_to_add_build_scene, bg="black")
        self.show_all_button = tkinter.Button(text="Show All Builds", bg="black")
        self.visible_builds = []

        # Add Build Scene Variables
        self.go_back_to_start_scene_button = tkinter.Button(text="Go Back", command=self.go_to_start_scene, height=2, width=6, bg="black")
        self.show_all_button.pack()
        self.add_build_button.pack()

        self.all_buttons = [self.add_build_button, self.show_all_button, self.go_back_to_start_scene_button]
        self.all_build_labels = []
        self.all_build_entries = []

        # TODO - CREATE A CLASS TO CLEAN UP THIS REPEATED CODE
        self.cpu_title_label = Label(text="CPU", font=("Arial", 16, "bold"))
        self.all_build_labels.append(self.cpu_title_label)
        # Cpu Name Entry
        self.cpu_name_entry_label = Label(text="CPU Name", font=("Arial", 12, "bold"))
        self.all_build_labels.append(self.cpu_name_entry_label)
        self.cpu_name_entry = Entry(width=12)
        self.all_build_entries.append(self.cpu_name_entry)

        # Cpu Brand Entry
        self.cpu_brand_entry_label = Label(text="CPU Brand", font=("Arial", 12, "bold"))
        self.all_build_labels.append(self.cpu_brand_entry_label)
        self.cpu_brand_entry = Entry(width=12)
        self.all_build_entries.append(self.cpu_brand_entry)

        # Cpu Price Entry
        self.cpu_price_entry_label = Label(text="CPU Price", font=("Arial", 12, "bold"))
        self.all_build_labels.append(self.cpu_price_entry_label)
        self.cpu_price_entry = Entry(width=12)
        self.all_build_entries.append(self.cpu_price_entry)

        self.all_labels = self.all_build_labels + []
        self.all_entries = self.all_build_entries + []

        self.go_to_start_scene()

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def hide_build_grid_frame(self):
        """Hide the build grid frame."""
        self.build_grid_frame.grid_forget()

    def show_build_grid_frame(self):
        """Show the build grid frame."""
        self.build_grid_frame.pack(fill="x")

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

        match scene:
            case Scene.START_SCENE:
                self.add_build_button.grid(in_=self.navigation_grid_frame, column=0, row=1)
                self.show_all_button.grid(in_=self.navigation_grid_frame, column=1, row=1)
            case Scene.ADD_BUILD_SCENE:
                self.go_back_to_start_scene_button.grid(in_=self.navigation_grid_frame, column=1, row=1, pady=5)

                # Layout CPU Entries and Labels
                self.cpu_title_label.grid(in_=self.navigation_grid_frame, column=1, row=2, pady=5)
                self.cpu_name_entry_label.grid(in_=self.navigation_grid_frame, column=0, row=3)
                self.cpu_name_entry.grid(in_=self.navigation_grid_frame, column=0, row=4)
                self.cpu_brand_entry_label.grid(in_=self.navigation_grid_frame, column=1, row=3)
                self.cpu_brand_entry.grid(in_=self.navigation_grid_frame, column=1, row=4)
                self.cpu_price_entry_label.grid(in_=self.navigation_grid_frame, column=2, row=3)
                self.cpu_price_entry.grid(in_=self.navigation_grid_frame, column=2, row=4)

    def go_to_start_scene(self):
        self.show_build_grid_frame()
        self.change_scene(Scene.START_SCENE)
        self.build_scrollable_frame.show()

    def go_to_add_build_scene(self):
        self.change_scene(Scene.ADD_BUILD_SCENE)
        self.build_scrollable_frame.hide()
        self.hide_build_grid_frame()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.window.destroy()

    def update_labels(self):
        total_builds = len(self.visible_builds)
        for i in range(total_builds):
            self.visible_builds[i].build_sku_label = tkinter.Label(self.build_scrollable_frame.scrollable_frame, text=f"SKU: {self.visible_builds[i].get_sku()}", bg='lightblue')
            self.visible_builds[i].build_sku_label.grid(in_=self.build_scrollable_frame.scrollable_frame, column = 1, row=i)
            self.visible_builds[i].description_label = tkinter.Label(self.build_scrollable_frame.scrollable_frame, text=self.visible_builds[i].pc_str, bg='lightblue')
            self.visible_builds[i].description_label.grid(in_=self.build_scrollable_frame.scrollable_frame, column=2, row=i)

    def update_photos(self):
        total_builds = len(self.visible_builds)
        for i in range(total_builds):
            image_file_path = self.visible_builds[i].full_pc_dict["image_file_name"]
            self.visible_builds[i].build_image = Canvas(width=250, height=250)
            build_img = PhotoImage(file=f"../images/{image_file_path}")
            self.visible_builds[i].build_image.create_image(125, 125, image=build_img)
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
            build.build_image.grid_forget()
        self.visible_builds = []
        print(self.visible_builds)

    def start(self):
        self.window.mainloop()