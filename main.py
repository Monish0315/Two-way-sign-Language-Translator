
import numpy as np
import cv2
import os
import PIL
from PIL import ImageTk
import PIL.Image
import speech_recognition as sr
import pyttsx3
from itertools import count
import string
from tkinter import *
import time
try:
    import Tkinter as tk
except:
    import tkinter as tk
import numpy as np
image_x, image_y = 64,64
from keras.models import load_model
classifier = load_model('model.h5')
import os

model_path = 'model.h5'
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at: {model_path}")
else:
    classifier = load_model(model_path)

from sklearn.decomposition import PCA
from keras.preprocessing import image
import numpy as np

def give_char():
    # Load and preprocess the image
    test_image = image.load_img('tmp1.png', target_size=(64, 64))  # Resize image to 64x64
    test_image = image.img_to_array(test_image)
    
    # Flatten the image to shape (1, 12288) and then reshape to (1, 32)
    test_image = test_image.flatten().reshape(1, 12288)  # Shape: (1, 12288)
    
    # Since the model expects an input of shape (1, 32), we will reduce the dimensions manually
    test_image_reduced = test_image[:, :32]  # Keep only the first 32 features
    
    try:
        # Pass the reduced input to the model
        result = classifier.predict(test_image_reduced)
        chars = "ABCDEFGHIJKMNOPQRSTUVWXYZ"
        indx = np.argmax(result[0])
        return chars[indx]
    except Exception as e:
        print(f"Error in prediction: {e}")
        return ''  # Return an empty string if there is an error

def create_button(parent, text, command, color, row, col, padx=10, pady=5):
    button = tk.Button(parent, text=text, command=command, 
                       bg=color, fg='white', font=("Arial", 12), borderwidth=0, padx=20)
    button.grid(row=row, column=col, padx=padx, pady=pady)
    return button

def check_sim(i,file_map):
       for item in file_map:
              for word in file_map[item]:
                     if(i==word):
                            return 1,item
       return -1,""

op_dest = r"C:\Users\pmoni\two-way-sign-language-translator\filtered_data"  # Update this to your actual path
alpha_dest = r"C:\Users\pmoni\two-way-sign-language-translator\alphabet"
#op_dest="/home/aniket/Desktop/Projects/gif_extract/filtered_data/"
#alpha_dest="/home/aniket/Desktop/Projects/gif_extract/alphabet/"
dirListing = os.listdir(op_dest)
editFiles = []
for item in dirListing:
       if ".webp" in item:
              editFiles.append(item)

file_map={}
for i in editFiles:
       tmp=i.replace(".webp","")
       #print(tmp)
       tmp=tmp.split()
       file_map[i]=tmp

def func(a):
    all_frames = []
    final = PIL.Image.new('RGB', (380, 260))
    words = a.split()
    for i in words:
        flag, sim = check_sim(i, file_map)
        if flag == -1:
            for j in i:
                try:
                    im = PIL.Image.open(os.path.join(alpha_dest, f"{j.lower()}_small.gif"))
                    frameCnt = im.n_frames
                    for frame_cnt in range(frameCnt):
                        im.seek(frame_cnt)
                        im.save("tmp.png")
                        img = cv2.imread("tmp.png")
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        img = cv2.resize(img, (380, 260))
                        im_arr = PIL.Image.fromarray(img)
                        all_frames.extend([im_arr] * 15)  # Repeat frames
                except Exception as e:
                    print(f"Error processing {j}: {e}")
        else:
            print(sim)
            im = PIL.Image.open(os.path.join(op_dest, sim))
            im.info.pop('background', None)
            im.save('tmp.gif', 'gif', save_all=True)
            im = PIL.Image.open("tmp.gif")
            frameCnt = im.n_frames
            for frame_cnt in range(frameCnt):
                im.seek(frame_cnt)
                im.save("tmp.png")
                img = cv2.imread("tmp.png")
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, (380, 260))
                im_arr = PIL.Image.fromarray(img)
                all_frames.append(im_arr)

    final.save("out.gif", save_all=True, append_images=all_frames, duration=100, loop=0)
    return all_frames

img_counter = 0
img_text=''
class Tk_Manage(tk.Tk):
       def __init__(self, *args, **kwargs):     
              tk.Tk.__init__(self, *args, **kwargs)
              container = tk.Frame(self)
              container.pack(side="top", fill="both", expand = True)
              container.grid_rowconfigure(0, weight=1)
              container.grid_columnconfigure(0, weight=1)
              self.frames = {}
              for F in (StartPage, VtoS, StoV):
                     frame = F(container, self)
                     self.frames[F] = frame
                     frame.grid(row=0, column=0, sticky="nsew")
              self.show_frame(StartPage)

       def show_frame(self, cont):
              frame = self.frames[cont]
              frame.tkraise()

        
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#f0f0f0')  # Light background
        label = tk.Label(self, text="Two Way Sign Language Translator", font=("Verdana", 16, "bold"), bg='#f0f0f0')
        label.pack(pady=20)

        button_frame = tk.Frame(self, bg='#f0f0f0')
        button_frame.pack(pady=10)

        button = tk.Button(button_frame, text="Voice to Sign", command=lambda: controller.show_frame(VtoS), 
                           bg='#4CAF50', fg='white', font=("Arial", 12), borderwidth=0, padx=20)
        button.grid(row=0, column=0, padx=10)

        button2 = tk.Button(button_frame, text="Sign to Voice", command=lambda: controller.show_frame(StoV), 
                            bg='#2196F3', fg='white', font=("Arial", 12), borderwidth=0, padx=20)
        button2.grid(row=0, column=1, padx=10)

        load = PIL.Image.open("Two Way Sign Language Translator.png")
        load = load.resize((620, 450), PIL.Image.LANCZOS)

        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render, bg='#f0f0f0')
        img.image = render
        img.place(x=100, y=200)


class VtoS(tk.Frame):
       def __init__(self, parent, controller):
              tk.Frame.__init__(self, parent, bg='#f0f0f0')
              label = tk.Label(self, text="Voice to Sign", font=("Verdana", 16, "bold"), bg='#f0f0f0')
              label.pack(pady=10)
              self.gif_box = tk.Label(self)
              self.gif_box.place(x=400, y=160)
              button_frame = tk.Frame(self, bg='#f0f0f0')
              button_frame.pack(pady=10)

              button1 = tk.Button(button_frame, text="Back to Home", command=lambda: controller.show_frame(StartPage), 
                                   bg='#f44336', fg='white', font=("Arial", 12), borderwidth=0, padx=20)
              button1.grid(row=0, column=0, padx=10)

              button2 = tk.Button(button_frame, text="Sign to Voice", command=lambda: controller.show_frame(StoV), 
                                   bg='#2196F3', fg='white', font=("Arial", 12), borderwidth=0, padx=20)
              button2.grid(row=0, column=1, padx=10)

        # Existing code for gif_box, input text, and recording button here

              def gif_stream():
                     global cnt
                     global gif_frames
                     if cnt == len(gif_frames):
                            return
                     img = gif_frames[cnt]
                     cnt += 1
                     imgtk = ImageTk.PhotoImage(image=img)
                     self.gif_box.imgtk = imgtk  # Use self.gif_box
                     self.gif_box.configure(image=imgtk)
                     self.gif_box.after(100, gif_stream)  # Adjusting the delay to 100 ms for smoother playback

              def hear_voice():
                     global inputtxt
                     store = sr.Recognizer()
                     with sr.Microphone() as s:
                            inputtxt.delete("1.0", END)  # Clear previous input
                            try:
                                   audio_input = store.record(s, duration=10)
                                   text_output = store.recognize_google(audio_input)
                                   inputtxt.insert(END, text_output)
                            except sr.UnknownValueError:
                                   print("Could not understand audio")
                                   inputtxt.insert(END, 'Could not understand audio')
                            except sr.RequestError as e:
                                   print(f"Error with request: {e}")
                                   inputtxt.insert(END, 'Service unavailable')

              def Take_input():
                     INPUT = inputtxt.get("1.0", "end-1c")
                     print(INPUT)
                     global gif_frames
                     gif_frames=func(INPUT)
                     global cnt
                     cnt=0
                     gif_stream()
                     self.gif_box.place(x=400, y=160) 
              
              l = tk.Label(self,text = "Enter Text or Voice:")
              l1 = tk.Label(self,text = "OR")
              inputtxt = tk.Text(self, height = 4,width = 25)
              voice_button= tk.Button(self,height = 2,width = 20, text="Record Voice",command=lambda: hear_voice())
              voice_button.place(x=50,y=180)
              Display = tk.Button(self, height = 2,width = 20,text ="Convert",command = lambda:Take_input())
              l.place(x=50, y=160)
              l1.place(x=115, y=230)
              inputtxt.place(x=50, y=250)
              Display.pack()


class StoV(tk.Frame):
       def __init__(self, parent, controller):
              tk.Frame.__init__(self, parent, bg='#f0f0f0')
              label = tk.Label(self, text="Sign to Voice", font=("Verdana", 16, "bold"), bg='#f0f0f0')
              label.pack(pady=10)

              button_frame = tk.Frame(self, bg='#f0f0f0')
              button_frame.pack(pady=10)

              button1 = tk.Button(button_frame, text="Back to Home", command=lambda: controller.show_frame(StartPage), 
                                   bg='#f44336', fg='white', font=("Arial", 12), borderwidth=0, padx=20)
              button1.grid(row=0, column=0, padx=10)

              button2 = tk.Button(button_frame, text="Voice to Sign", command=lambda: controller.show_frame(VtoS), 
                                   bg='#2196F3', fg='white', font=("Arial", 12), borderwidth=0, padx=20)
              button2.grid(row=0, column=1, padx=10)

        # Existing code for video stream button and text display here

              def start_video():
                     video_frame = tk.Label(self)
                     cam = cv2.VideoCapture(0)
                     
                     global img_counter
                     img_counter = 0
                     global img_text
                     img_text = ''
                     def video_stream():
                            global img_text
                            global img_counter
                            if(img_counter>200):
                                   return None
                            img_counter+=1
                            ret, frame = cam.read()
                            frame = cv2.flip(frame,1)
                            img=cv2.rectangle(frame, (425,100),(625,300), (0,255,0), thickness=2, lineType=8, shift=0)
                            lower_blue = np.array([35,10,0])
                            upper_blue = np.array([160,230,255])
                            imcrop = img[102:298, 427:623]
                            hsv = cv2.cvtColor(imcrop, cv2.COLOR_BGR2HSV)
                            mask = cv2.inRange(hsv, lower_blue, upper_blue)
                            cv2.putText(frame, img_text, (30, 400), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 255, 0))
                            img_name = "tmp1.png"
                            save_img = cv2.resize(mask, (image_x, image_y))  # Already resizing to 64x64, so this is fine
                            cv2.imwrite(img_name, save_img)

                            tmp_text=img_text[0:]
                            img_text = give_char()
                            if(tmp_text!=img_text):
                                   print(tmp_text)
                                   disp_txt.insert(END, tmp_text)
                            img = PIL.Image.fromarray(frame)
                            imgtk = ImageTk.PhotoImage(image=img)
                            video_frame.imgtk = imgtk
                            video_frame.configure(image=imgtk)
                            video_frame.after(1, video_stream)
                     video_stream()
                     disp_txt.pack()
                     video_frame.pack()
              
              start_vid = tk.Button(self,height = 2,width = 20, text="Start Video",command=lambda: start_video())
              start_vid.pack()


app = Tk_Manage()
app.geometry("800x750")
app.mainloop()