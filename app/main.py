import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk, ImageFilter
import requests
from io import BytesIO
import threading
import os

class AppleInspiredAIImageGenerator:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("VerboVisions")
        self.root.geometry("900x1000")
        self.root.configure(fg_color="#F5F5F5")

        self.colors = {
            "background": "#F5F5F5",
            "primary": "#007AFF",
            "secondary": "#5856D6",
            "accent": "#FF2D55",
            "text_primary": "#000000",
            "text_secondary": "#8E8E93"
        }

        self.current_image = None
        self.is_generating = False

        self.main_container = ctk.CTkFrame(
            self.root, 
            corner_radius=20, 
            fg_color="white", 
            border_width=1, 
            border_color="#E0E0E0"
        )
        self.main_container.pack(padx=20, pady=20, fill="both", expand=True)

        self.header_frame = ctk.CTkFrame(
            self.main_container, 
            fg_color="transparent"
        )
        self.header_frame.pack(pady=(30, 20), padx=20, fill="x")

        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="Image Forge", 
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=self.colors["text_primary"]
        )
        self.title_label.pack(side="left")

        self.theme_toggle = ctk.CTkSwitch(
            self.header_frame, 
            text="Dark Mode", 
            command=self.toggle_theme,
            switch_width=60,
            switch_height=30
        )
        self.theme_toggle.pack(side="right")

        self.prompt_frame = ctk.CTkFrame(
            self.main_container, 
            fg_color="transparent"
        )
        self.prompt_frame.pack(pady=20, padx=20, fill="x")

        self.prompt_entry = ctk.CTkEntry(
            self.prompt_frame, 
            width=700, 
            height=50, 
            corner_radius=25,
            border_width=1,
            border_color=self.colors["text_secondary"],
            font=ctk.CTkFont(size=16),
            placeholder_text="Describe the image you want to create...",
            placeholder_text_color=self.colors["text_secondary"]
        )
        self.prompt_entry.pack(side="left", expand=True, padx=(0, 10))

        self.generate_button = ctk.CTkButton(
            self.prompt_frame, 
            text="Generate", 
            width=120,
            height=50,
            corner_radius=25,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.generate_image_request,
            fg_color=self.colors["primary"],
            hover_color=self.colors["secondary"]
        )
        self.generate_button.pack(side="right")

        self.image_frame = ctk.CTkFrame(
            self.main_container, 
            width=700, 
            height=700,
            fg_color="transparent",
            corner_radius=20
        )
        self.image_frame.pack(pady=20, padx=20)
        self.image_frame.pack_propagate(False)

        self.image_label = ctk.CTkLabel(
            self.image_frame, 
            text="Your AI-generated image will appear here",
            font=ctk.CTkFont(size=18),
            text_color=self.colors["text_secondary"]
        )
        self.image_label.pack(expand=True)

        self.status_frame = ctk.CTkFrame(
            self.main_container, 
            fg_color="transparent"
        )
        self.status_frame.pack(pady=10, padx=20, fill="x")

        self.progress_bar = ctk.CTkProgressBar(
            self.status_frame, 
            width=700,
            height=10,
            corner_radius=5,
            fg_color="#E0E0E0",
            progress_color=self.colors["primary"]
        )
        self.progress_bar.set(0)

        self.status_label = ctk.CTkLabel(
            self.status_frame, 
            text="", 
            font=ctk.CTkFont(size=14),
            text_color=self.colors["text_secondary"]
        )
        self.status_label.pack(pady=(10, 0))

        self.action_frame = ctk.CTkFrame(
            self.main_container, 
            fg_color="transparent"
        )
        self.action_frame.pack(pady=20, padx=20, fill="x")

        self.save_button = ctk.CTkButton(
            self.action_frame, 
            text="Save Image", 
            width=200,
            height=50,
            corner_radius=25,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.save_image,
            fg_color=self.colors["accent"],
            hover_color=self.colors["secondary"],
            state="disabled"
        )
        self.save_button.pack(expand=True)

        self.prompt_entry.bind('<Return>', lambda event: self.generate_image_request())

    def generate_image_request(self):
        prompt = self.prompt_entry.get().strip()
        if not prompt:
            messagebox.showwarning("Prompt Needed", "Please enter an image description.")
            return

        if self.is_generating:
            return

        self.is_generating = True
        self.generate_button.configure(state="disabled")
        self.save_button.configure(state="disabled")
        self.status_label.configure(text="Generating image...")
        
        self.progress_bar.pack(pady=(0, 10))
        self.animate_progress()

        def generate_thread():
            try:
                image_bytes = self.call_image_generation_api(prompt)
                self.root.after(0, self.process_generated_image, image_bytes)
            except Exception as e:
                self.root.after(0, self.handle_generation_error, str(e))

        threading.Thread(target=generate_thread, daemon=True).start()

    def animate_progress(self):
        if not self.is_generating:
            return
        
        current_progress = self.progress_bar.get()
        next_progress = (current_progress + 0.1) % 1.1
        self.progress_bar.set(next_progress)
        
        self.root.after(100, self.animate_progress)

    def process_generated_image(self, image_bytes):
        self.is_generating = False
        self.progress_bar.pack_forget()
        self.progress_bar.set(0)

        if image_bytes:
            try:
                pil_image = Image.open(BytesIO(image_bytes))
                pil_image = pil_image.resize((700, 700), Image.Resampling.LANCZOS)
                
                blurred = pil_image.filter(ImageFilter.GaussianBlur(radius=1))
                
                ctk_image = ctk.CTkImage(
                    light_image=pil_image, 
                    dark_image=pil_image, 
                    size=(700, 700)
                )
                
                self.image_label.configure(image=ctk_image, text="")
                self.save_button.configure(state="normal")
                self.generate_button.configure(state="normal")
                
                self.current_image = pil_image
                
                self.status_label.configure(
                    text="Image generated successfully!", 
                    text_color=self.colors["primary"]
                )
            except Exception as e:
                self.handle_generation_error(str(e))
        else:
            self.handle_generation_error("Failed to generate image")

    def handle_generation_error(self, error_message):
        self.is_generating = False
        self.progress_bar.pack_forget()
        self.progress_bar.set(0)
        
        self.generate_button.configure(state="normal")
        self.status_label.configure(
            text=f"Error: {error_message}", 
            text_color=self.colors["accent"]
        )
        messagebox.showerror("Generation Error", error_message)

    def save_image(self):
        if not self.current_image:
            messagebox.showerror("No Image", "No image to save")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG", "*.png"), 
                ("JPEG", "*.jpg"), 
                ("WebP", "*.webp")
            ]
        )
        
        if file_path:
            try:
                self.current_image.save(file_path)
                messagebox.showinfo("Saved", f"Image saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Save Error", str(e))

    def toggle_theme(self):
        current_mode = ctk.get_appearance_mode()
        new_mode = "Light" if current_mode == "Dark" else "Dark"
        ctk.set_appearance_mode(new_mode)

    def call_image_generation_api(self, prompt):
        API_URL = "https://ai-api.magicstudio.com/api/ai-art-generator"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://magicstudio.com",
            "Referer": "https://magicstudio.com/ai-art-generator/",
        }

        data = {
            "prompt": prompt,
            "output_format": "bytes",
            "user_profile_id": "null",
            "anonymous_user_id": "user_" + str(hash(prompt))
        }

        try:
            response = requests.post(API_URL, headers=headers, data=data)
            response.raise_for_status()
            return response.content
        except requests.RequestException:
            return None

    def run(self):
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")
        self.root.mainloop()

if __name__ == "__main__":
    app = AppleInspiredAIImageGenerator()
    app.run()
