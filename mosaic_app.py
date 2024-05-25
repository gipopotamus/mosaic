import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
from tkinter import ttk
from PIL import Image, ImageTk

from mosaic import load_image, create_mosaic
from colors import recommend_colors, rgb_to_hex


class MosaicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mosaic Generator")
        self.root.geometry("1000x800")
        self.root.configure(bg="#F0F0F0")

        self.image_path = ""
        self.chip_colors = []

        self.setup_ui()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10 10 10 10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configuration of grid layout
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # Image Selection
        image_frame = ttk.LabelFrame(main_frame, text="Image Selection", padding="10 10 10 10")
        image_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)

        ttk.Label(image_frame, text="Select Image:").grid(row=0, column=0, sticky=tk.W)
        self.image_entry = ttk.Entry(image_frame, width=50)
        self.image_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(image_frame, text="Browse", command=self.browse_image).grid(row=0, column=2, sticky=tk.W)

        # Dimension settings
        dim_frame = ttk.LabelFrame(main_frame, text="Mosaic Dimensions", padding="10 10 10 10")
        dim_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)

        ttk.Label(dim_frame, text="Wall Width:").grid(row=0, column=0, sticky=tk.W)
        self.wall_width_entry = ttk.Entry(dim_frame)
        self.wall_width_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)

        ttk.Label(dim_frame, text="Wall Height:").grid(row=1, column=0, sticky=tk.W)
        self.wall_height_entry = ttk.Entry(dim_frame)
        self.wall_height_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)

        ttk.Label(dim_frame, text="Chip Width:").grid(row=2, column=0, sticky=tk.W)
        self.chip_width_entry = ttk.Entry(dim_frame)
        self.chip_width_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5)

        ttk.Label(dim_frame, text="Chip Height:").grid(row=3, column=0, sticky=tk.W)
        self.chip_height_entry = ttk.Entry(dim_frame)
        self.chip_height_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5)

        # Chip Colors
        color_frame = ttk.LabelFrame(main_frame, text="Chip Colors", padding="10 10 10 10")
        color_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)

        ttk.Button(color_frame, text="Add Color", command=self.add_color).grid(row=0, column=0, sticky=tk.W)
        ttk.Button(color_frame, text="Recommend Colors", command=self.recommend_colors).grid(row=0, column=1,
                                                                                             sticky=tk.W)
        self.colors_frame = ttk.Frame(color_frame)
        self.colors_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        # Action Buttons
        action_frame = ttk.Frame(main_frame, padding="10 10 10 10")
        action_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)

        ttk.Button(action_frame, text="Generate Mosaic", command=self.generate_mosaic).grid(row=0, column=0, padx=5)
        ttk.Button(action_frame, text="Update Dimensions", command=self.update_dimensions).grid(row=0, column=1, padx=5)

        # Canvas for displaying the mosaic
        canvas_frame = ttk.LabelFrame(main_frame, text="Mosaic Display", padding="10 10 10 10")
        canvas_frame.grid(row=0, column=1, rowspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        canvas_frame.columnconfigure(0, weight=1)
        canvas_frame.rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(canvas_frame, bg="white", width=800, height=600)
        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    def browse_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        self.image_entry.delete(0, tk.END)
        self.image_entry.insert(0, self.image_path)

    def add_color(self):
        color = colorchooser.askcolor()[0]
        if color:
            self.chip_colors.append([int(color[0]), int(color[1]), int(color[2])])
            self.update_colors_display()

    def update_colors_display(self):
        for widget in self.colors_frame.winfo_children():
            widget.destroy()
        for index, color in enumerate(self.chip_colors):
            color_frame = tk.Frame(self.colors_frame, bg=rgb_to_hex(color), width=20, height=20)
            color_frame.pack(side=tk.LEFT, padx=5, pady=5)
            color_frame.bind("<Button-1>", lambda e, idx=index: self.delete_color(idx))

    def recommend_colors(self):
        if not self.image_path:
            messagebox.showerror("Error", "No image selected.")
            return
        image = load_image(self.image_path)
        recommended_colors = recommend_colors(image)
        for color in recommended_colors:
            self.chip_colors.append([int(c) for c in color])
        self.update_colors_display()

    def generate_mosaic(self):
        try:
            wall_width = int(self.wall_width_entry.get())
            wall_height = int(self.wall_height_entry.get())
            chip_width = int(self.chip_width_entry.get())
            chip_height = int(self.chip_height_entry.get())

            if not self.image_path:
                raise ValueError("No image selected.")
            if not self.chip_colors:
                raise ValueError("No chip colors selected.")

            image = load_image(self.image_path)
            mosaic = create_mosaic(image, wall_width, wall_height, chip_width, chip_height, self.chip_colors)

            self.display_mosaic(mosaic)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_mosaic(self, mosaic):
        mosaic_image = Image.fromarray(mosaic)
        mosaic_image.thumbnail((800, 600))
        self.mosaic_photo = ImageTk.PhotoImage(mosaic_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.mosaic_photo)

    def update_dimensions(self):
        try:
            wall_width = int(self.wall_width_entry.get())
            wall_height = int(self.wall_height_entry.get())
            chip_width = int(self.chip_width_entry.get())
            chip_height = int(self.chip_height_entry.get())

            if not self.image_path:
                raise ValueError("No image selected.")
            if not self.chip_colors:
                raise ValueError("No chip colors selected.")

            image = load_image(self.image_path)
            mosaic = create_mosaic(image, wall_width, wall_height, chip_width, chip_height, self.chip_colors)

            self.display_mosaic(mosaic)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_color(self, index):
        if self.chip_colors:
            del self.chip_colors[index]
            self.update_colors_display()
        else:
            messagebox.showerror("Error", "No colors to delete.")
