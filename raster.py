import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
import rasterio
from rasterio.plot import show
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import geopandas as gpd

class RasterShapefileViewer:
    def __init__(self, master):
        self.master = master
        self.master.title("Raster and Shapefile Viewer")

        self.canvas_frame = tk.Frame(master)
        self.canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.toolbar_frame = tk.Frame(master)
        self.toolbar_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

        self.load_raster_button = tk.Button(self.toolbar_frame, text="Load Raster", command=self.load_raster)
        self.load_raster_button.pack(side=tk.LEFT)

        self.bands_label = tk.Label(self.toolbar_frame, text="Select Bands:")
        self.bands_label.pack(side=tk.LEFT)

        self.band_var = tk.StringVar()
        self.band_entry = tk.Entry(self.toolbar_frame, textvariable=self.band_var)
        self.band_entry.pack(side=tk.LEFT)

        self.display_raster_button = tk.Button(self.toolbar_frame, text="Display Raster", command=self.display_raster)
        self.display_raster_button.pack(side=tk.LEFT)

        self.load_shapefile_button = tk.Button(self.toolbar_frame, text="Load Shapefile", command=self.load_shapefile)
        self.load_shapefile_button.pack(side=tk.LEFT)

        self.attribute_label = tk.Label(self.toolbar_frame, text="Select Attribute:")
        self.attribute_label.pack(side=tk.LEFT)

        self.attribute_var = tk.StringVar()
        self.attribute_entry = tk.Entry(self.toolbar_frame, textvariable=self.attribute_var)
        self.attribute_entry.pack(side=tk.LEFT)

        self.plot_attribute_button = tk.Button(self.toolbar_frame, text="Plot Attribute", command=self.plot_attribute_chart)
        self.plot_attribute_button.pack(side=tk.LEFT)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def load_raster(self):
        file_path = filedialog.askopenfilename(title="Select Raster File", filetypes=[("TIFF Files", "*.tif")])
        if file_path:
            self.dataset = rasterio.open(file_path)
            self.num_bands = self.dataset.count
            self.band_var.set(f"1-{self.num_bands}")

    def display_raster(self):
        band_range = self.band_var.get().split('-')
        start_band, end_band = int(band_range[0]), int(band_range[1])

        raster_data = self.dataset.read(range(start_band, end_band + 1))
        show(raster_data, ax=self.ax, cmap='viridis')
        self.canvas.draw()

    def load_shapefile(self):
        file_path = filedialog.askopenfilename(title="Select Shapefile", filetypes=[("Shapefile Files", "*.shp")])
        if file_path:
            self.gdf = gpd.read_file(file_path)
            self.attributes = self.gdf.columns
            self.attribute_var.set(self.attributes[0])

    def plot_attribute_chart(self):
        attribute_name = self.attribute_var.get()
        if attribute_name in self.gdf.columns:
            plt.bar(self.gdf.index, self.gdf[attribute_name])
            plt.xlabel('Feature Index')
            plt.ylabel(attribute_name)
            plt.show()
        else:
            print(f"Attribute '{attribute_name}' not found in the shapefile.")


if __name__ == "__main__":
    root = tk.Tk()
    app = RasterShapefileViewer(root)
    root.mainloop()
