import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import cv2
from ultralytics import YOLO
import os
import string
import numpy as np
from PIL import Image as PILImage


class SignLanguageApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Sign Language Translator")
        self.geometry("1200x800")

        # Initialize the main container frame
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        # Store frames in a dictionary
        self.frames = {}

        for F in (StartPage, SignToVoice, TextToSign):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the start page
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

        # Start camera only when SignToVoice page is shown
        if page_name == "SignToVoice":
            frame.start_camera()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg='#f0f0f0')

        # Title Label
        label = tk.Label(self, text="Sign Language Translator", font=("Bahnscript", 24, "bold"), bg='#f0f0f0')
        label.pack(pady=20)

        # Button frame for options
        button_frame = tk.Frame(self, bg='#f0f0f0')
        button_frame.pack(pady=10)

        button = tk.Button(button_frame, text="Sign to Voice", 
                           command=lambda: controller.show_frame("SignToVoice"),
                           bg='#4CAF50', fg='white', font=("Arial", 12), borderwidth=0, padx=20)
        button.grid(row=0, column=0, padx=10)

        button2 = tk.Button(button_frame, text="Text to Sign", 
                            command=lambda: controller.show_frame("TextToSign"),
                            bg='#2196F3', fg='white', font=("Arial", 12), borderwidth=0, padx=20)
        button2.grid(row=0, column=1, padx=10)

        # Load and display image
        load = Image.open(r"C:\Users\pmoni\project\Two-way-sign-Language-Translator-main\Two-way-sign-Language-Translator-main\Blue hand red hand.png")
        load = load.resize((620, 450), Image.LANCZOS)
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render, bg='#f0f0f0')
        img.image = render
        img.place(x=100, y=200)


class SignToVoice(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.cap = None  # Placeholder for the camera
        self.model = None  # Placeholder for the YOLO model

        # Create a label to display the video stream
        self.label = tk.Label(self)
        self.label.pack()

        # Button to go back to the start page
        back_button = tk.Button(self, text="Back", 
                                command=lambda: self.stop_camera(controller),
                                bg='#FF5733', fg='white', font=("Arial", 12))
        back_button.pack(pady=10)

    def start_camera(self):
        # Initialize the camera and YOLO model only when this page is shown
        if not self.cap:
            self.cap = cv2.VideoCapture(0)  # Open the camera
        if not self.model:
            self.model = YOLO(r'C:\Users\pmoni\project\sign_language_detection\best.pt')  # Load YOLO model
        
        # Start the video capturing process
        self.update_frame()

    def update_frame(self):
        success, frame = self.cap.read()
        if success:
            # Run inference and get results
            results = self.model.track(frame, persist=True)

            # Annotate the frame with detection results
            annotated_frame = results[0].plot()

            # Convert the frame to ImageTk format
            cv_img = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(cv_img)
            imgtk = ImageTk.PhotoImage(image=img_pil)

            # Update the Tkinter label with the new image
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)

        # Schedule the next frame update
        self.after(10, self.update_frame)

    def stop_camera(self, controller):
        if self.cap:
            self.cap.release()  # Release the camera when done
        controller.show_frame("StartPage")


class TextToSign(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#f0f0f0')
        self.controller = controller
        label = tk.Label(self, text="Text to Sign", font=("Verdana", 16, "bold"), bg='#f0f0f0')
        label.pack(pady=10)

        # Text input box for users to type in the text to be translated
        self.text_input = tk.Entry(self, width=50, font=("Arial", 14))
        self.text_input.pack(pady=10)

        # Button to trigger the translation
        translate_button = tk.Button(self, text="Translate to Sign", command=self.convert_text_to_sign, 
                                     bg='#4CAF50', fg='white', font=("Arial", 12), padx=20)
        translate_button.pack(pady=10)

        # Center GIF display box
        self.gif_box = tk.Label(self, bg='#f0f0f0')
        self.gif_box.pack(pady=10)

        # Back and Sign-to-Voice buttons
        button_frame = tk.Frame(self, bg='#f0f0f0')
        button_frame.pack(pady=10)

        button1 = tk.Button(button_frame, text="Back to Home", command=lambda: controller.show_frame("StartPage"), 
                            bg='#f44336', fg='white', font=("Arial", 12), borderwidth=0, padx=20)
        button1.grid(row=0, column=0, padx=10)

        button2 = tk.Button(button_frame, text="Sign to Voice", command=lambda: controller.show_frame("SignToVoice"), 
                            bg='#2196F3', fg='white', font=("Arial", 12), borderwidth=0, padx=20)
        button2.grid(row=0, column=1, padx=10)

    def convert_text_to_sign(self):
        input_text = self.text_input.get().lower()
        
        # Ensure there's input text
        if not input_text:
            print("Please enter some text.")
            return

        # Define the folder where alphabet GIFs are stored
        alpha_dest = r"C:\Users\pmoni\project\Two-way-sign-Language-Translator-main\Two-way-sign-Language-Translator-main\alphabet"  # Change this to your actual path

        # Initialize frames list for animation
        all_frames = []
        for char in input_text:
            if char in string.ascii_lowercase:  # Check if it's a letter
                gif_path = os.path.join(alpha_dest, f"{char}_small.gif")
                try:
                    im = PILImage.open(gif_path)
                    frameCnt = im.n_frames

                    # Loop through GIF frames and add to all_frames
                    for frame_num in range(frameCnt):
                        im.seek(frame_num)
                        img = PILImage.fromarray(np.array(im.convert('RGBA')))

                        # Resize the frame to 5cm x 5cm (189x189 pixels)
                        img = img.resize((189, 189), PILImage.LANCZOS)

                        all_frames.append(img)

                except Exception as e:
                    print(f"Error loading GIF for {char}: {e}")

        # Start displaying the GIF frames one by one
        self.display_gif_frames(all_frames)

    def display_gif_frames(self, all_frames):
        if not all_frames:
            print("No frames to display.")
            return

        def update_frame(idx):
            frame = all_frames[idx]
            img_tk = ImageTk.PhotoImage(frame)
            self.gif_box.configure(image=img_tk)
            self.gif_box.image = img_tk
            # Display the next frame after 100 ms (adjust as needed)
            idx = (idx + 1) % len(all_frames)
            self.after(2000, update_frame, idx)

        # Start updating frames
        update_frame(0)


if __name__ == "__main__":
    app = SignLanguageApp()
    app.mainloop()
