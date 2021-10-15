import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image, ImageOps, ImageDraw, UnidentifiedImageError

class Application(ttk.Frame):

    ''' The main GUI frame '''

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        # get the arduino port number
        # self.arduino = ArduinoPort()
        # create an array of pixel values
        self.pixel_vals = []
        # create any widgets to display in the frame
        self.create_widgets()
        # display self on the parent window
        self.grid()

    def create_widgets(self):
        
        ## IMAGES
        # display input image
        self.lif_input = LabeledImageFrame(self, "Input Image")
        self.lif_input.grid(row=0, column=0, padx=10, pady=10)
        # display grayscale version of input image
        self.lif_grayscale = LabeledImageFrame(self, "Grayscale Image")
        self.lif_grayscale.grid(row=0, column=1, padx=10, pady=10)
        # display pixelized version of grayscale image
        self.lif_pixelize = LabeledImageFrame(self, "Pixelized Image")
        self.lif_pixelize.grid(row=0, column=2, padx=10, pady=10)        
        # display pattern preview with labeled pixel brightness values
        self.lif_pattern = LabeledImageFrame(self, "Pattern Preview")
        self.lif_pattern.grid(row=1, column=0, padx=10, pady=10,
                              columnspan=2, rowspan=4)
        # initial image on application load
        init_img = Image.open("Abstract_art.png")
        init_img = init_img.resize((130, 130), Image.ANTIALIAS)
        self.set_input_image(init_img)

    ''' Updates all images and pixel data after importing a new input image '''
    def set_input_image(self, image):
        # input image
        img = ImageTk.PhotoImage(image)
        self.lif_input.set_image(img)

        # grayscale image
        gray_img = ImageOps.grayscale(image)
        img = ImageTk.PhotoImage(gray_img)
        self.lif_grayscale.set_image(img)

        # pixelized image
        pattern_img = gray_img.resize((8, 8))
        pixelize_img = pattern_img.resize(gray_img.size, Image.NEAREST)
        img = ImageTk.PhotoImage(pixelize_img)
        self.lif_pixelize.set_image(img)

        # pattern preview
        self.pixel_vals = list(pattern_img.getdata())
        preview_img = self.draw_pattern_preview(pattern_img)
        img = ImageTk.PhotoImage(preview_img)
        self.lif_pattern.set_image(img)

    ''' Generate the pattern preview '''
    def draw_pattern_preview(self, pattern_img):
        scaling_factor = 37
        width, height = pattern_img.size
        preview_img = pattern_img.resize((width*scaling_factor, height*scaling_factor), Image.NEAREST)
        draw = ImageDraw.Draw(preview_img)
        for row in range(height):
            for col in range(width):
                val = pattern_img.getpixel((col, row))
                if val > 127:
                    draw.text((col*scaling_factor, row*scaling_factor), str(val), fill=0)
                else:
                    draw.text((col*scaling_factor, row*scaling_factor), str(val), fill=255)
        return preview_img


class LabeledImageFrame(ttk.LabelFrame):

    ''' A labeled frame containing an image '''
    
    def __init__(self, parent, text, photo_image=None):
        ttk.LabelFrame.__init__(self, parent, text=text)
        self["labelanchor"] = tk.N
        self.img = photo_image
        self.create_widgets()
    
    ''' Display the image in a label '''
    def create_widgets(self):
        self.lbl_img = ttk.Label(self, image=self.img)
        self.lbl_img.grid(padx=5, pady=5)

    ''' Set the image to display '''
    def set_image(self, photo_image):
        self.img = photo_image
        self.lbl_img["image"] = self.img


def main():
    root = tk.Tk()
    root.title("LED Matrix Configurator")
    app = Application(root)
    root.mainloop()

if __name__ == '__main__': main()