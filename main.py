import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import os

def open_image():
    global img, img_display
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    if file_path:
        img = Image.open(file_path)
        img.thumbnail((240, 320))
        img_display = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_display)
        save_button.config(state=tk.NORMAL)

def save_image():
    base_name = 'DuvarKagidi'
    extension = '.jpg'
    output_image_path = base_name + extension
    counter = 1

    # Dosya adı mevcutsa yeni bir ad oluştur
    while os.path.exists(output_image_path):
        output_image_path = f"{base_name}{counter}{extension}"
        counter += 1

    img_resized = img.resize((240, 320))
    if img_resized.mode in ('RGBA', 'P'):
        img_resized = img_resized.convert('RGB')
    img_resized.save(output_image_path, 'JPEG')
    print(f"Resim başarıyla {output_image_path} olarak kaydedildi.")

# Tkinter arayüzü oluştur
root = tk.Tk()
root.title("Digiphone S500 Duvar Kağıdı Oluşturucu")

# Stil oluştur
style = ttk.Style()
style.theme_use('alt')  # 'clam', 'alt', 'default', 'classic' gibi temalar kullanılabilir

# Resim önizleme alanı
canvas = tk.Canvas(root, width=240, height=320)
canvas.pack(pady=10)

# Gözat butonu
browse_button = ttk.Button(root, text="Gözat", command=open_image)
browse_button.pack(pady=5)

# Kaydet butonu
save_button = ttk.Button(root, text="Dönüştür", command=save_image, state=tk.DISABLED)
save_button.pack(pady=5)

root.mainloop()
