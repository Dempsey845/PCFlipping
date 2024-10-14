import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import shutil
import random
import string


class ImageUploaderApp:
    def __init__(self, parent_window, display_callback, sku):
        """
        Initialize the ImageUploader class and set up the UI elements.

        :param parent_window: The root Tkinter window.
        :param display_callback: A callback function to send the selected image path to another window.
        """
        self.parent_window = parent_window
        self.display_callback = display_callback

        self.sku = sku

        # Create UI elements
        self.frame = tk.Frame(self.parent_window)
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.path_entry = tk.Entry(self.frame, width=40)
        self.path_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.select_btn = tk.Button(self.frame, text="Browse Image", command=self.select_image)
        self.select_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.upload_btn = tk.Button(self.frame, text="Upload", command=self.upload_image)
        self.upload_btn.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        self.preview_label = tk.Label(self.frame, bg="lightblue", width=300, height=200)
        self.preview_label.grid(row=1, column=0, columnspan=3, pady=10, sticky="nsew")

        self.image_path = None

        # Grid configuration
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

    def set_preview_image(self, filepath):
        """
        Display a preview of the selected image.
        :param filepath: Path to the image file.
        """
        img = Image.open(filepath)
        img = img.resize((300, 200), Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(img)

        self.preview_label.configure(image=self.tk_image)
        self.preview_label.image = self.tk_image  # Keep a reference to avoid garbage collection
        self.path_entry.delete(0, 'end')
        self.path_entry.insert(0, filepath)

    def select_image(self):
        """
        Open a file dialog to select an image and display it in the preview.
        """
        filename = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title="Select Image",
            filetypes=[("PNG images", "*.png"), ("JPG images", "*.jpg"), ("JPEG images", "*.jpeg")]
        )

        if filename:
            self.image_path = filename
            self.set_preview_image(self.image_path)

    def upload_image(self):
        """
        Save the selected image and pass the image path to the main display window.
        """
        if self.image_path:
            file_extension = os.path.splitext(self.image_path)[1]
            random_filename = str(self.sku)
            destination_path = f"../images/{random_filename}{file_extension}"

            shutil.copy(self.image_path, destination_path)
            messagebox.showinfo("Success", "Image uploaded successfully!")

            # Pass the path to the display callback for showing the image in another window
            self.display_callback(destination_path)
        else:
            messagebox.showwarning("No Image", "Please select an image first.")


def open_image_uploader(display_callback, sku):
    root = tk.Toplevel()  # Use Toplevel to open a new window
    root.geometry("650x300")
    root.resizable(False, False)
    app = ImageUploaderApp(root, display_callback, sku)
    root.mainloop()


def resize_image(image_path, width, height):
    '''Returns a tkinter PhotoImage resized to the specified width and height'''
    # Open the image using Pillow
    original_image = Image.open(image_path)

    # Resize the image to the given width and height
    resized_image = original_image.resize((width, height))

    # Convert the resized image to a Tkinter-compatible PhotoImage object
    tk_image = ImageTk.PhotoImage(resized_image)

    return tk_image