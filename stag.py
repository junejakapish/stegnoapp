import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

def encode_image():
    image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", ".jpg .jpeg .png .bmp")])
    if not image_path:
        return
    text = text_entry.get("1.0", "end-1c")
    image = Image.open(image_path)

    if image.mode != "RGB":
        image = image.convert("RGB")

    width, height = image.size

    if len(text) > width * height:
        messagebox.showerror("Error", "Text is too long to be encoded in the image.")
        return

    encoded_image = image.copy()
    x, y = 0, 0
    for char in text:

        ascii_val = ord(char)
        pixel_val = encoded_image.getpixel((x, y))
        pixel_val = (pixel_val[0], pixel_val[1], ascii_val)
        encoded_image.putpixel((x, y), pixel_val)
        x += 1
        if x >= width:
            x = 0
            y += 1

    encoded_image_path = filedialog.asksaveasfilename(title="Save Encoded Image", defaultextension=".png", filetypes=[("PNG Image", ".png")])
    if encoded_image_path:
        encoded_image.save(encoded_image_path)

def decode_image():

    image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", ".jpg .jpeg .png .bmp")])
    if not image_path:
        return
    image = Image.open(image_path)
    if image.mode != "RGB":
        image = image.convert("RGB")

    width, height = image.size
    decoded_text = ""
    x, y = 0, 0
    for _ in range(width * height):
        pixel_val = image.getpixel((x, y))
        ascii_val = pixel_val[2]
        decoded_text += chr(ascii_val)
        x += 1
        if x >= width:
            x = 0
            y += 1
        if y >= height:
            break

    decoded_text = decoded_text.rstrip("\x00")

    decoded_text_entry.delete("1.0", "end")
    decoded_text_entry.insert("1.0", decoded_text)

root = tk.Tk()
root.title("Stegano Application")
encode_frame = tk.Frame(root)
encode_frame.pack(padx=10, pady=10)

text_label = tk.Label(encode_frame, text="Enter text to encode:")
text_label.pack()
text_entry = tk.Text(encode_frame, height=10, width=40)
text_entry.pack()

encode_button = tk.Button(encode_frame, text="Encode Image", command=encode_image)
encode_button.pack()

decode_frame = tk.Frame(root)
decode_frame.pack(padx=10, pady=10)

decode_button = tk.Button(decode_frame, text="Decode Image", command=decode_image)
decode_button.pack()

decoded_text_label = tk.Label(decode_frame, text="Decoded text:")
decoded_text_label.pack()
decoded_text_entry = tk.Text(decode_frame, height=10, width=40)
decoded_text_entry.pack()

root.mainloop()