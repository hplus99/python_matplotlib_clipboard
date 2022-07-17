from tkinter import *
from PIL import Image, ImageTk
import platform
import io
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure


class TkPlot2D():
    def __init__(self, tk_parent_window, np_data_x : np.ndarray, np_data_y : np.ndarray) -> None:
        self.fig = Figure(figsize=(5, 4), dpi = 150)
        self.canvas_plot = FigureCanvasAgg(self.fig)

        ax = self.fig.add_subplot()
        ax.plot(np_data_x, np_data_y)
        self.canvas_plot.draw()
        self.rgba = np.asarray(self.canvas_plot.buffer_rgba())

        self.plot_dim_y, self.plot_dim_x, _ = self.rgba.shape
        self.img_plot = Image.fromarray(self.rgba)
        self.imgTk_plot = ImageTk.PhotoImage(image=self.img_plot)

        self.margin_x = 100
        self.margin_y = 100

        self.window_dim_x = self.plot_dim_x + 2 * self.margin_x
        self.window_dim_y = self.plot_dim_y + 2 * self.margin_y
        self.window_pos_x = 100
        self.window_pos_y = 100

        self.window_title = 'Plot 2D'

        self.toplevel = Toplevel(tk_parent_window)
        self.toplevel.title(self.window_title)
        self.toplevel.geometry(
            '{}x{}+{}+{}'.format(self.window_dim_x, self.window_dim_y, self.window_pos_x, self.window_pos_y))
        
        # create a canvas
        self.canvas = Canvas(self.toplevel, width=self.plot_dim_x, height=self.plot_dim_y, bg='black', bd=1)
        self.canvas.place(x=self.margin_x, y=self.margin_y)
        self.canvas.create_image(0, 0, image=self.imgTk_plot, anchor=NW)
        

        # create a label
        self.label_path = Label(self.toplevel, text='2D Plot')
        self.label_path.place(x=20, y=20)


        # create buttons
        self.button_1 = Button(self.toplevel, padx=10, pady=10, text='Copy to Clipboard', command=self.copy_to_clipboard)
        self.button_1.place(x=int(self.window_dim_x / 2 - 120), y=(self.plot_dim_y + self.margin_y + 30))

        self.button_2 = Button(self.toplevel, padx=10, pady=10, text='Exit', command=self.toplevel.destroy)
        self.button_2.place(x=int(self.window_dim_x / 2 + 50), y=(self.plot_dim_y + self.margin_y + 30))

        
        # loop for toplevel
        self.toplevel.grab_set()
        pass

    def copy_to_clipboard(self):
        self.os_platform = platform.system()
        if self.os_platform == 'Darwin':
            import pasteboard        
            self.pb = pasteboard.Pasteboard()
            self.data_bytes = io.BytesIO()
            self.img_plot.save(self.data_bytes, format='TIFF', quality=90)
            self.bytes = self.data_bytes.getvalue()
            self.pb.set_contents(data=self.bytes, type=pasteboard.TIFF)
            self.data_bytes.close()
            pass

        elif self.os_platform == 'Windows':
            import win32clipboard
            self.data_bytes = io.BytesIO()
            self.img_plot.convert('RGB').save(self.data_bytes, format='BMP')
            self.data_clipboard = self.data_bytes.getvalue()[14:]
            # self.data_bytes.close()

            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, self.data_clipboard)
            win32clipboard.CloseClipboard()
            self.data_bytes.close()
            pass
        pass
