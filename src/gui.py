import tkinter

class PCBuildUI:
    def __init__(self, pc_build):
        build_sku_label = tkinter.Label(text=pc_build.sku, font=("Arial", 14))
        build_sku_label.pack()
        pc_dict = pc_build.to_dict_name()
        pc_str = ""

        for key, value in pc_dict.items():
            if value is not None and key != "ram" and key != "sku":
                pc_str += f"{key}: {value}\n"
            elif key == "RAM":
                pc_str += f"{key}: {"".join(value)}\n"

        print(f"pc_str = {pc_str}")
        new_label = tkinter.Label(text=pc_str, font=("Arial", 12))
        new_label.pack()

class GUI:
    """
    TODO - LIST OF BUILDS FROM Builds.json ON THE GUI (scrollable)
    TODO - IMPLEMENT PHOTOS FOR EACH BUILD
    TODO - IMPLEMENT ADDING A BUILD AND REMOVING A BUILD
    TODO - IMPLEMENT SORTING BUILDS BY DIFFERENT TYPES E.G list-date, profit, cpu, cpu-brand, etc...
    """
    def __init__(self, test_build):
        self.running = True
        self.window = tkinter.Tk()
        self.window.title("PC Flipping")
        self.window.minsize(width=800, height=1000)

        self.title_label = tkinter.Label(text="PC Flipping", font=("Arial", 26, "bold"))
        self.title_label.pack()

        self.visible_builds = []

        self.add_pc_build(test_build)

        self.window.mainloop()

    def add_pc_build(self, pc_build):
        new_build = PCBuildUI(pc_build)
        self.visible_builds.append(new_build)
