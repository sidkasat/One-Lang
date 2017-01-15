from tkinter import Tk, Label, Button, Entry, W, E, StringVar, Frame
try:
      import Image
except ImportError:
      from PIL import Image
import pytesseract
from translate import translator
import cv2
import requests
import json
import user_in
import os.path
import time



class MyFirstGUI:
    def __init__(self, master):
        self.path=""
        self.upld_text = StringVar()
        self.cam_text = StringVar()
        self.Freq = 2500 # Set Frequency To 2500 Hertz
        self.Dur = 1000 # Set Duration To 1000 ms == 1 second
        self.master = master
        master.title("One Lang")

        self.frame=Frame(self.master)
        self.frame.pack()

        self.label = Label(self.frame, text="Welcome to One Lang!")
        self.label.pack()

        self.who_label = Label(
            self.frame, text = "How do you want to translate text?-\n\
      1) Upload an image\n\
      2) Take a picture\n\
      Enter the choice. Eg: '1' or '2'")
        self.who_label.pack()
        
        self._row_entry = Entry(self.frame, width = 20)
        self._row_entry.pack()
        #self._row_entry.grid(row = 1, column = 1, padx = 10, pady = 1,
        #    sticky = W + E)

        self.greet_button = Button(self.frame, text="Enter", command=self.enter)
        self.greet_button.pack()

        self._input_text = StringVar()
        self._input_text.set('No input yet!')
        self.input_label = Label(
            self.frame , textvariable = self._input_text)
        self.input_label.pack()
        

        self.close_button = Button(self.frame, text="Close", command=master.quit)
        self.close_button.pack()

        self.camera_port = 0
        self.ramp_frames = 30
        

    def enter(self):
        n=self._row_entry.get()
        if n not in ['1','2']:
            self._input_text.set('INVALID INPUT. Enter Again')
            self._row_entry.delete(0,'end')
        else:
            self.frame.destroy()
            self.new_toplevel=Frame(self.master, takefocus=True)
            self.new_toplevel.pack()
            lbl=Label(self.new_toplevel, text="Option {}:".format(n))
            lbl.pack()
            if(n=='1'):
                
                #self.upld_text.set("Path to File/ File name:")
                self.upload=Label(self.new_toplevel, text="PATH")
                self.upload.pack()
                self.path_entry = Entry(self.new_toplevel, width = 40)
                self.path_entry.pack()
                self.upload_button = Button(self.new_toplevel, text="UPLOAD", command=self.upload_func)
                self.upload_button.pack()
            elif(n=='2'):
                upload=Label(self.new_toplevel, text="Click camera button to click picture")
                upload.pack()
                self.camera_button = Button(self.new_toplevel, text="CAPTURE", command=self.camera)
                self.camera_button.pack()

    
    def upload_func(self):     
        self.path=self.path_entry.get()
        if not(os.path.isfile(self.path)):
            self.fail=Label(self.new_toplevel, text="TRY AGAIN")
            self.fail.pack()
            self.path_entry.delete(0,'end')
            
        #self.upld_text.set("Invalid file path. Enter again")
        else:
            self.success=Label(self.new_toplevel, text="SUCCESS")
            self.success.pack()
            self.convert()
        
        
    
    def camera(self):
        self.cam = cv2.VideoCapture(self.camera_port)
        
        self.cam_text.set('Taking Image in 3')
        self.cam_label = Label(
            self.new_toplevel , textvariable = self.cam_text)
        self.cam_label.pack()
        
        for i in range(self.ramp_frames):
              temp = self.get_image()

        
        #winsound.Beep(self.Freq,self.Dur)
        camera_capture = self.get_image()
        self.path = "test_image.png"
        self.cam_text.set('Picture Taken')
        cv2.imwrite(self.path, camera_capture)
        del(self.cam)
        self.convert()

    def get_image(self):
        
        retval, im = self.cam.read()
        return im

    def convert(self):
        overlay=False
        language='eng'
        api_key='22007382f988957'
        payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
        with open(self.path, 'rb') as f:
            r = requests.post('https://api.ocr.space/parse/image',
                              files={self.path: f},
                              data=payload,
                              )
        down= r.content.decode()
        self.new=Frame(self.master, takefocus=True)
        self.new.pack()
        x=down.find("ParsedText")
        y=down.find("ErrorMessage")
        to_print=""
        if not(y-16==x):
            to_print=down[x+13:y-3]
            to_print=to_print.replace(r"\r\n", "\n")
            self.pre=Label(self.new, text="PREVIEW TEXT OF IMAGE")
            self.pre.pack()
            self.print=Label(self.new, text=to_print)
            self.print.pack()
            #language_id = gs.detect(to_print)
            #print("TRANSLATION: ",gs.translate(to_print, 'en'))
            try:
                  trans="Translation: "+translator('en','hi',to_print.strip(' \t\n\r'))[0][0][0]
            except:
                  trans="TRANSLATION\n\
            Translation API Error"
            self.trans=Label(self.new, text=trans)
            self.trans.pack()
        else:
            err="Unable to parse the image. Please check if the image is malformed \
            or too blurry and if you have specified correct language with the image."
            self.err=Label(self.new, text=err)
            self.err.pack()
        

root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()
