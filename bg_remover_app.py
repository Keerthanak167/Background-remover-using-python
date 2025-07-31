import os
import tkinter as tk
from tkinter import filedialog, messagebox
from rembg import remove
from PIL import Image, ImageTk
import io

OUTPUT_FOLDER = "output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

class BackgroundRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Background Remover")
        self.root.geometry("400x500")
        self.root.configure(bg="#1e1e1e")

        self.image_label = tk.Label(root, text="No Image Selected", bg="#1e1e1e", fg="#bbbbbb")
        self.image_label.pack(pady=20)

        self.preview_canvas = tk.Canvas(root, width=300, height=300, bg="#2e2e2e", bd=0, highlightthickness=0)
        self.preview_canvas.pack(pady=10)

        select_button = tk.Button(root, text="Choose Image", command=self.choose_image, bg="#3a3a3a", fg="white")
        select_button.pack(pady=10)

        remove_button = tk.Button(root, text="Remove Background", command=self.remove_background, bg="#007acc", fg="white")
        remove_button.pack(pady=10)

        self.selected_image_path = None
        self.preview_image = None

    def choose_image(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg")]
        )
        if filepath:
            self.selected_image_path = filepath
            self.display_preview(filepath)
            self.image_label.config(text=os.path.basename(filepath))

    def display_preview(self, image_path):
        img = Image.open(image_path)
        img.thumbnail((300, 300))
        self.preview_image = ImageTk.PhotoImage(img)
        self.preview_canvas.delete("all")
        self.preview_canvas.create_image(150, 150, image=self.preview_image)

    def remove_background(self):
        if not self.selected_image_path:
            messagebox.showwarning("No Image", "Please choose an image first.")
            return

        try:
            with open(self.selected_image_path, "rb") as i:
                input_data = i.read()
            output_data = remove(input_data)

            output_path = os.path.join(
                OUTPUT_FOLDER,
                f"no_bg_{os.path.basename(self.selected_image_path)}"
            )
            with open(output_path, "wb") as o:
                o.write(output_data)

            messagebox.showinfo("Success", f"Saved to: {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BackgroundRemoverApp(root)
    root.mainloop()
