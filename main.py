import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import os
import webbrowser

base_image = None
converted_image = None

def paste_image(base_image, overlay_image, position):
    """
    base_image: Ana resim (PIL Image nesnesi)
    overlay_image: Üzerine yapıştırılacak resim (PIL Image nesnesi)
    position: Yapıştırılacak konum (x, y)
    """
    if overlay_image.mode != 'RGBA':
        overlay_image = overlay_image.convert('RGBA')
    base_image.paste(overlay_image, position, overlay_image)
    return base_image

def open_image():
    global img, img_display, base_image, converted_image
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    if file_path:
        overlay_image = Image.open(file_path)
        overlay_image = overlay_image.resize((240, 320))  # Üzerine yapıştırılacak resmin boyutunu ayarla
        converted_image = overlay_image.copy()

        # Ana resmi yükle veya oluştur
        base_image = Image.open("s500.png")
        screen_position = (37, 96)  # Ekran kısmının konumu (x, y)

        # Resmi belirli bir konumda yapıştır
        base_image = paste_image(base_image, overlay_image, screen_position)

        img_display = ImageTk.PhotoImage(base_image)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_display)
        save_button.config(state=tk.NORMAL)

def save_image():
    global base_image, converted_image
    preview_name = 'Preview'
    wallpaper_name = 'DuvarKagidi'
    extension = '.jpg'
    preview_image_path = preview_name + extension
    wallpaper_image_path = wallpaper_name + extension
    counter = 1

    # Preview dosya adı mevcutsa yeni bir ad oluştur
    while os.path.exists(preview_image_path):
        preview_image_path = f"{preview_name}{counter}{extension}"
        counter += 1

    # DuvarKagidi dosya adı mevcutsa yeni bir ad oluştur
    counter_converted = 1
    while os.path.exists(wallpaper_image_path):
        wallpaper_image_path = f"{wallpaper_name}{counter_converted}{extension}"
        counter_converted += 1

    # Dönüştürülen resmi kaydet (DuvarKagidi olarak)
    if converted_image.mode in ('RGBA', 'P'):
        converted_image = converted_image.convert('RGB')
    converted_image.save(wallpaper_image_path, 'JPEG')
    print(f"Dönüştürülen resim başarıyla {wallpaper_image_path} olarak kaydedildi.")

    # Ana resmi kaydet (Preview olarak)
    if base_image.mode in ('RGBA', 'P'):
        base_image = base_image.convert('RGB')
    base_image.save(preview_image_path, 'JPEG')
    print(f"Resim başarıyla {preview_image_path} olarak kaydedildi.")

    # İşlem başarılı mesajı göster
    messagebox.showinfo("Başarılı", "İşlem başarıyla tamamlandı!")

def show_main_screen():
    loading_frame.pack_forget()  # Yükleniyor ekranını gizle
    main_frame.pack(fill='both', expand=True)  # Ana ekranı göster

def open_blog():
    webbrowser.open_new("https://digiphone-s500.blogspot.com")

def open_youtube():
    webbrowser.open_new("https://www.youtube.com/channel/UCaUQMNxNK7GuEpi4TnXPrIg")

# Tkinter arayüzü oluştur
root = tk.Tk()
root.title("Digiphone S500 Duvar Kağıdı Oluşturucu")
root.geometry("400x1000")  # Pencere boyutunu ayarla
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
canvas = tk.Canvas(main_frame, width=305, height=775, bg='black', highlightthickness=0)
canvas.pack(pady=10)

# Gözat butonu
browse_button = ttk.Button(main_frame, text="Gözat", command=open_image)
browse_button.pack(pady=5)

# Kaydet butonu
save_button = ttk.Button(main_frame, text="Dönüştür", command=save_image, state=tk.DISABLED)
save_button.pack(pady=5)

# Blog linki
blog_link = tk.Label(main_frame, text="digiphone-s500.blogspot.com", fg="blue", cursor="hand2", bg='black')
blog_link.pack(pady=5)
blog_link.bind("<Button-1>", lambda e: open_blog())

# YouTube linki
youtube_link = tk.Label(main_frame, text="Digiphone S500 YouTube Kanalı", fg="blue", cursor="hand2", bg='black')
youtube_link.pack(pady=5)
youtube_link.bind("<Button-1>", lambda e: open_youtube())

# Yükleniyor ekranını 2 saniye sonra gizle ve ana ekranı göster
root.after(2000, show_main_screen)

# İkonu ayarla
icon_image = Image.open("loading.jpg")
icon_image.save("loading.ico", format='ICO')
root.iconbitmap("loading.ico")

root.mainloop()