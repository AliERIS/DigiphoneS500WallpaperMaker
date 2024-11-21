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

def show_main_screen():
    loading_frame.pack_forget()  # Yükleniyor ekranını gizle
    main_frame.pack(fill='both', expand=True)  # Ana ekranı göster

# Tkinter arayüzü oluştur
root = tk.Tk()
root.title("Digiphone S500 Duvar Kağıdı Oluşturucu")
root.geometry("400x500")  # Pencere boyutunu ayarla
root.configure(bg='black')  # Arka plan rengini siyah yap

# Stil oluştur
style = ttk.Style()
style.theme_use('clam')  # 'clam', 'alt', 'default', 'classic' gibi temalar kullanılabilir

# ttk bileşenlerinin arka plan rengini siyah yap
style.configure('TFrame', background='black')
style.configure('TLabel', background='black', foreground='white')
style.configure('TButton', background='black', foreground='white')
style.configure('TProgressbar', background='black')

# Yükleniyor ekranı oluştur
loading_frame = ttk.Frame(root)
loading_frame.pack(fill='both', expand=True)

# Yükleniyor resmi ekle
loading_image = Image.open("loading.jpg")
loading_image = loading_image.resize((200, 200), Image.LANCZOS)
loading_image_tk = ImageTk.PhotoImage(loading_image)
loading_label_image = ttk.Label(loading_frame, image=loading_image_tk)
loading_label_image.pack(pady=10)

# Yükleniyor metni ekle
loading_label = ttk.Label(loading_frame, text="Yükleniyor...")
loading_label.pack(pady=10)

# Yükleme çubuğu ekle
progress = ttk.Progressbar(loading_frame, orient="horizontal", length=200, mode="indeterminate")
progress.pack(pady=10)
progress.start()

# Ana ekranı oluştur
main_frame = ttk.Frame(root)

# Resim önizleme alanı
canvas = tk.Canvas(main_frame, width=240, height=320, bg='black', highlightthickness=0)
canvas.pack(pady=10)

# Gözat butonu
browse_button = ttk.Button(main_frame, text="Gözat", command=open_image)
browse_button.pack(pady=5)

# Kaydet butonu
save_button = ttk.Button(main_frame, text="Dönüştür", command=save_image, state=tk.DISABLED)
save_button.pack(pady=5)

# Yükleniyor ekranını 2 saniye sonra gizle ve ana ekranı göster
root.after(2000, show_main_screen)

# İkonu ayarla
icon_image = Image.open("loading.jpg")
icon_image.save("loading.ico", format='ICO')
root.iconbitmap("loading.ico")

root.mainloop()
