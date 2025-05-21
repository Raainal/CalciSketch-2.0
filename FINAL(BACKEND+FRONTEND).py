import customtkinter as ctk
import tkinter as tk
from tkinter import Canvas, Button, Scale, HORIZONTAL, PhotoImage, filedialog, messagebox
from pathlib import Path
import pickle
import os
from tkinter import *
import webbrowser
from tkinter import filedialog
import tempfile
import os
import re
import ollama
from ollama import Client
import time
from PIL import Image, ImageTk, ImageDraw,ImageGrab
import google.generativeai as genai

ollama_client = ollama.Client(host="http://localhost:11450")

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")
class CalciSketchApp(ctk.CTk):
    def __init__(self):
        ollama_client = ollama.Client(host="http://localhost:11450")
        self.api_key = "AIzaSyCLMQuQich4jg7c4FzGx8OfIuUWU9KakHk"
        genai.configure(api_key=self.api_key)
        super().__init__()
        self.title("CalciSketch")
        self.geometry("1920x1080")
        self.minsize(1280, 720)
        self.configure(fg_color="white")
        
        # Load assets
        self.bg_image = Image.open("F:\\Temp USB Calcisketch\\Assets\\bg img.png").resize((1920, 1080))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        logo_img = Image.open("F:\\Temp USB Calcisketch\\Assets\\logo.png").resize((40, 40))
        self.logo = ImageTk.PhotoImage(logo_img)

        self.about_img = Image.open("F:\\Temp USB Calcisketch\\Assets\\ABOUT US!!.png").resize((280, 75))
        self.about_photo = ImageTk.PhotoImage(self.about_img)

        self.start_img = Image.open("F:\\Temp USB Calcisketch\\Assets\\START DRAWING.png").resize((280, 75))
        self.start_photo = ImageTk.PhotoImage(self.start_img)

       
        self.container = ctk.CTkFrame(self, fg_color="white")
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        self.create_navbar()

        for F in (HomePage, AboutPage, DrawingPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            frame.place(relwidth=1, relheight=1)
            self.frames[page_name] = frame

        self.show_frame("HomePage")
    

    def create_navbar(self):
        navbar_border = ctk.CTkFrame(self, height=72, fg_color="black")
        navbar_border.place(relx=0, rely=0, relwidth=1)

    # Inner actual white navbar
        navbar = ctk.CTkFrame(navbar_border, height=70, fg_color="white")
        navbar.place(relx=0, rely=0, relwidth=1)

        center_frame = ctk.CTkFrame(navbar, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        left_frame = ctk.CTkFrame(navbar, fg_color="transparent")
        left_frame.place(relx=0, rely=0.5, anchor="w")
        logo_label = tk.Label(center_frame, image=self.logo, bg="white", bd=0, cursor="hand2")
        logo_label.pack(side="left", padx=(0, 10))
        logo_label.bind("<Button-1>", lambda e: self.show_frame("HomePage"))

        app_name = tk.Label(center_frame, text="CalciSketch", font=("Helvetica Neue", 20, "bold"), fg="black", bg="white")
        app_name.pack(side="left")


    def show_frame(self, page_name):
        for name, frame in self.frames.items():
            frame.place_forget()
        self.frames[page_name].place(relwidth=1, relheight=1)

class HomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="white")
        self.controller = controller

        self.canvas = tk.Canvas(self, width=1920, height=1080, highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)
        self.bg_photo = controller.bg_photo
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        self.canvas.create_text(960, 440, text="CalciSketch", font=("Helvetica Neue", 48, "bold"), fill="black")
        self.canvas.create_text(960, 500, text="Draw. Solve. Understand. 🚀", font=("Helvetica Neue", 24), fill="black")

        about_btn_id = self.canvas.create_image(880, 570, image=controller.about_photo, anchor="center")
        start_btn_id = self.canvas.create_image(1040, 570, image=controller.start_photo, anchor="center")

        self.canvas.tag_bind(about_btn_id, "<Button-1>", lambda e: controller.show_frame("AboutPage"))
        self.canvas.tag_bind(start_btn_id, "<Button-1>", lambda e: controller.show_frame("DrawingPage"))

class AboutPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="white")
        self.controller = controller
        self.solution_text = ""
        # Background Image
        bg_image = Image.open(r"F:\\Temp USB Calcisketch\\Assets\\bg img.png").resize((1920, 1080))
        self.bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(self, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Creator Info
        image_paths = [
            r"F:\\Temp USB Calcisketch\\Assets\\amal_Card.png",
            r"F:\\Temp USB Calcisketch\\Assets\\shib_card.png",
            r"F:\\Temp USB Calcisketch\\Assets\\dharsh_Card.png",
            ]
        linkedin_urls = [
            "https://www.linkedin.com/in/raainal/",
            "https://www.linkedin.com/in/shib-sobhan-mohanty-53957b252/",
            "https://www.linkedin.com/in/dharshini-guruprasath/",
        
        ]
        profiles = [
            "Expert in model training and execution, ensuring robust machine learning performance.",
            "Versatile full stack developer, skilled in both frontend and backend, and seamless integration.",
            "UI specialist who transformed design concepts into functional, user-friendly code.",
        ]

        self.card_images = []
        card_width = 300
        card_height = 340
        spacing = 160
        corner_radius = 35

        total_width = len(image_paths) * card_width + (len(image_paths) - 1) * spacing
        start_x = (1920 - total_width) // 2
        y = 300

        for i, (img_path, linkedin_url, profile) in enumerate(zip(image_paths, linkedin_urls, profiles)):
            img = Image.open(img_path).resize((card_width, card_height))
            rounded_img = self.make_rounded_image(img, corner_radius)
            photo = ImageTk.PhotoImage(rounded_img)
            self.card_images.append(photo)

            card_container = tk.Canvas(self, width=card_width, height=card_height, bg="white", bd=0, highlightthickness=0)
            x = start_x + i * (card_width + spacing)
            card_container.place(x=x, y=y)

            self.round_rectangle(card_container, 0, 0, card_width, card_height, radius=corner_radius, fill="white", outline="")
            card_container.create_image(0, 0, anchor="nw", image=photo)

            profile_label = tk.Label(
                card_container,
                text=profile,
                font=("Arial", 12),
                bg="white",
                wraplength=card_width-20,
                justify="center"
            )
            profile_label.place(relx=0.5, rely=0.74, anchor="center")

            btn = tk.Button(
                card_container,
                text="LinkedIn",
                fg="white",
                bg="#0077b5",
                font=("Arial", 12, "bold"),
                cursor="hand2",
                relief="flat",
                command=lambda url=linkedin_url: webbrowser.open_new(url)
            )
            btn.place(relx=0.5, rely=0.90, anchor="center", width=100, height=30)

    def make_rounded_image(self, img, radius):
        img = img.convert("RGBA")
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([0, 0, img.size[0], img.size[1]], radius=radius, fill=255)
        img.putalpha(mask)
        return img

    def round_rectangle(self, canvas, x1, y1, x2, y2, radius=35, **kwargs):
        points = [
            x1+radius, y1, x2-radius, y1, x2, y1, x2, y1+radius,
            x2, y2-radius, x2, y2, x2-radius, y2, x1+radius, y2,
            x1, y2, x1, y2-radius, x1, y1+radius, x1, y1
        ]
        return canvas.create_polygon(points, **kwargs, smooth=True)
class DrawingPage(ctk.CTkFrame):
    
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="white")
        
        self.api_key = "AIzaSyCLMQuQich4jg7c4FzGx8OfIuUWU9KakHk"
        genai.configure(api_key=self.api_key)
        self.controller = controller

        self.brush_color = "black"
        self.brush_size = 5
        self.eraser_on = False
        self.last_x = None
        self.last_y = None
        self.solution_frame = None
        self.drawing_actions = []
        self.image_refs = {}
        
        self.create_canvas()
        self.create_toolbar()
        self.bind_canvas_events()
    def create_canvas(self):
        self.canvas = tk.Canvas(
            self,
            bg="#FFFFFF",
            height=880,
            width=1920,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.pack(side="top")

        # Optional: background image
        try:
            bg_img = tk.PhotoImage(file=self.relative_to_assets("F:\\Temp USB Calcisketch\\Assets\\image_1.png"))
            self.image_refs["bg"] = bg_img
            self.canvas.create_image(960.0, 440.0, image=bg_img)
        except Exception:
            pass

    def create_toolbar(self):
        from tkinter import Button, Scale, HORIZONTAL, filedialog, messagebox

        toolbar_bg = Button(self, image=self.load_image("F:\\Temp USB Calcisketch\\Assets\\button_1.png"), borderwidth=0, highlightthickness=0,
                            command=lambda: None, relief="flat")
        toolbar_bg.place(x=190.0, y=906.0, width=1600.0, height=123.0)

        colors = ["red", "yellow", "green", "blue", "white", "black"]
        x_positions = [224.0, 288.0, 353.0, 417.0, 481.0, 545.0]
        for i, color in enumerate(colors):
            Button(self, image=self.load_image(f"F:\\Temp USB Calcisketch\\Assets\\button_{i+2}.png"), borderwidth=0, highlightthickness=0,
                   command=lambda c=color: self.change_color(c), relief="flat").place(
                x=x_positions[i], y=937.0, width=63.0, height=63.0)

        Button(self, image=self.load_image("F:\\Temp USB Calcisketch\\Assets\\button_8.png"), borderwidth=0, highlightthickness=0,
               command=self.use_eraser, relief="flat").place(x=695.0, y=928.0, width=83.0, height=83.0)
        Button(self, image=self.load_image("F:\\Temp USB Calcisketch\\Assets\\button_9.png"), borderwidth=0, highlightthickness=0,
               command=self.use_brush, relief="flat").place(x=830.0, y=934.0, width=69.0, height=69.0)

        Button(self, image=self.load_image("F:\\Temp USB Calcisketch\\Assets\\button_12.png"), borderwidth=0, highlightthickness=0,
               command=self.save_work, relief="flat").place(x=1435.0, y=938.0, width=68.0, height=68.0)
        
        Button(self, image=self.load_image("F:\\Temp USB Calcisketch\\Assets\\button_11.png"), borderwidth=0, highlightthickness=0,
               command=self.clear_canvas, relief="flat").place(x=1300.0, y=938.0, width=68.0, height=68.0)

        Scale(self, from_=1, to=10, orient=HORIZONTAL, command=self.change_size).place(x=950, y=938.0, width=300, height=50)
        Button(self, image=self.load_image("F:\\Temp USB Calcisketch\\Assets\\button_13.png"), borderwidth=0, highlightthickness=0,
               command=self.load_work, relief="flat").place(x=1550.0, y=938.0, width=68.0, height=68.0)
        
        Button(
    self,
    image=self.load_image("F:\\Temp USB Calcisketch\\Assets\\button_10.png"),
    borderwidth=0,
    highlightthickness=0,
    command=self.on_calculate_click,
    relief="flat"
).place(x=1650.0, y=938.0, width=65.0, height=65.0)
        
    def on_calculate_click(self):
        self.evaluate_expression()
        
    def bind_canvas_events(self):
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

    def paint(self, event):
        x1, y1 = (event.x - self.brush_size), (event.y - self.brush_size)
        x2, y2 = (event.x + self.brush_size), (event.y + self.brush_size)
        color = "white" if self.eraser_on else self.brush_color

        self.drawing_actions.append({
            'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2,
            'color': color, 'size': self.brush_size
        })
        self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)
        self.last_x, self.last_y = event.x, event.y

    def reset(self, event):
        self.last_x = self.last_y = None

    def change_color(self, new_color):
        self.brush_color = new_color
        self.use_brush()

    def change_size(self, value):
        self.brush_size = int(value)

    def use_brush(self):
        self.eraser_on = False

    def use_eraser(self):
        self.eraser_on = True

    def clear_canvas(self):
        self.canvas.delete("all")
        self.drawing_actions.clear()
        if self.solution_frame:
            self.solution_frame.destroy()
            self.solution_frame = None
    def draw_solution_on_canvas(self, expression=None, result=None):
        if not result:
            return
        x, y = self.find_equal_sign_position()

    # Default fallback if '=' position not found
        if x is None or y is None:
            x, y = 1100, 600
        self.canvas.create_text(
        x -90, y-350,  # Minimal gap after '='
        text=result,
        fill="black",
        font=("Helvetica", 36, "bold"),
        anchor="w",
        tags="result_text"  # Optional: helps remove/update the text later
    )


    def save_work(self):
        from tkinter import filedialog, messagebox
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pkl",
            filetypes=[("Drawing Files", "*.pkl"), ("All Files", "*.*")],
            initialdir=os.path.expanduser("~\\Documents")
        )
        if file_path:
            try:
                with open(file_path, 'wb') as f:
                    pickle.dump(self.drawing_actions, f)
                messagebox.showinfo("Success", "Drawing saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    def display_solution_box(self, steps):
        
        self.solution_frame = Frame(self.canvas, bg="white", bd=2, relief="solid")
        self.canvas.create_window(960, 700, window=self.solution_frame, anchor="n", width=1820, height=180)

        text_widget = Text(self.solution_frame, wrap="word", height=65, font=("Helvetica", 25))
                           
                           
                           
                
        text_widget.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)

        scrollbar = Scrollbar(self.solution_frame, command=text_widget.yview)
        scrollbar.pack(side=ctk.RIGHT, fill=ctk.Y)

        text_widget.config(yscrollcommand=scrollbar.set)

        for step in steps:
            text_widget.insert(ctk.END, step + "\n")

    def evaluate_expression(self):
        x = self.winfo_rootx() + self.canvas.winfo_x()
        y = self.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        image = ImageGrab.grab().crop((x, y, x1, y1))

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            image.save(temp_file.name)
            temp_image_path = temp_file.name

        try:
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content([
            genai.upload_file(temp_image_path),
            "Identify the expression from the input image and rewrite it using standard mathematical symbols such as ∫, ×, ², ³, and fractions. Avoid LaTeX notation. Show clear and concise mathematical steps only. Do not include any explanation or descriptive text.The last step should be only the final numerical value on its own line during integration too"
        ])

            if response and response.text:
                parsed_expression = response.text.strip()

                ollama_response = ollama_client.chat(
                model='mistral',
                messages=[{
                    "role": "user",
                    "content": f"""Solve this expression step-by-step: {parsed_expression}. Provide a clear, concise breakdown of the solution, avoiding any LaTeX or verbose explanations. 
                                Rules:
                                1.Use only standard math symbols (no special formatting like LaTeX, markdown, etc.).

                                2.Show all intermediate steps clearly and sequentially (no step numbers).

                                3.Do not include labels like "The", "Answer:", "Final:", "Result:", "Output:" etc. anywhere.

                                4.Explanations are not allowed — only math operations and expressions at each step.

                                5.Each step should be concise and to the point, with no extra words.

                                6.The final step should be only the clean numerical value or expression without any surrounding text, symbols, boxes, parentheses, quotes, or step numbers.

                                7.Do not wrap the final answer inside boxes, parentheses, or quotes — just the number or expression                            .

                                8.The final value (after all steps) should be printed only on the canvas (not echoed again in the chat).

                                9.For indefinite integrals, write the evaluated expression + C directly (no words).

                                10.For definite integrals, show the evaluated numerical value directly in the last step."""
                }]
            )

                steps = ollama_response['message']['content'].split("\n")
                last_line = steps[-1].strip() if steps else ""

# Clean common filler words inline
                for prefix in ["So the answer is","So","the","answer","Therefore", "Hence", "Answer:", "Result:", "=", "⇒", "=>", "is"]:
                    if last_line.lower().startswith(prefix.lower()):
                         last_line = last_line[len(prefix):].strip()
                    break

                final_result = last_line
                self.display_solution_box(steps)
                self.solution_text = final_result
                self.draw_solution_on_canvas(parsed_expression, final_result)

        except Exception as e:
            print(f"Error during API call: {e}")
        finally:
            os.remove(temp_image_path)

    def update_brush_size(self, value):
        self.brush_size = int(float(value))
    def find_equal_sign_position(self):
        for item in self.canvas.find_all():
            if self.canvas.type(item) == "text":
                text = self.canvas.itemcget(item, "text")
                if "=" in text:
                    return tuple(self.canvas.coords(item))
        return None, None

    def load_work(self):
        from tkinter import filedialog, messagebox
        file_path = filedialog.askopenfilename(
            filetypes=[("Drawing Files", "*.pkl"), ("All Files", "*.*")],
            initialdir=os.path.expanduser("~\\Documents")
        )
        if file_path:
            try:
                with open(file_path, 'rb') as f:
                    loaded_actions = pickle.load(f)
                self.clear_canvas()
                for action in loaded_actions:
                    self.canvas.create_oval(
                        action['x1'], action['y1'],
                        action['x2'], action['y2'],
                        fill=action['color'],
                        outline=action['color']
                    )
                    self.drawing_actions.append(action)
                messagebox.showinfo("Success", "Drawing loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")

    def load_image(self, path):
        try:
            image = tk.PhotoImage(file=path)
            self.image_refs[path] = image  # Keep a reference so it's not garbage collected
            return image
        except Exception as e:
            print(f"Failed to load {path}: {e}")
            blank = tk.PhotoImage(width=68, height=68)
            self.image_refs[path] = blank
            return blank


if __name__ == "__main__":
    app = CalciSketchApp()
    app.mainloop()