try:
      import Image
except ImportError:
      from PIL import Image
import pytesseract
from translate import translator
import cv2
import requests
import json
import winsound
import goslate
import user_in

Freq = 2500 # Set Frequency To 2500 Hertz
Dur = 1000 # Set Duration To 1000 ms == 1 second
gs = goslate.Goslate()

trans_api='trnsl.1.1.20170115T060722Z.869d84285ba38270.d16d401a64dd70623184f1ef7b715d605c49bdac'
api_key='22007382f988957'
def ocr_space_file(filename, overlay=False, language='eng'):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.content.decode()


def get_image():
 retval, im = camera.read()
 return im

print("How do you want to translate text?-\n\
      1) Upload an image\n\
      2) Take a picture\n\
      Enter the choice. Eg: '1' or '2'")
x=int(input())
while(x not in [1,2]):
     print("Wrong input. Enter again")
     x=input()

def main():
      ob=user_in.InputApplication()
      ob.start()                  #Asks for User Input
      l = ob.l                    #List has the user input
      self._root_window=tkinter.Tk()
      if (x==2):
            camera_port = 0
            ramp_frames = 30
            camera = cv2.VideoCapture(camera_port)
            for i in range(ramp_frames):
                  temp = get_image()
            print("Taking image...")
            camera_capture = get_image()
            file = "test_image.png"
            winsound.Beep(Freq,Dur)
            cv2.imwrite(file, camera_capture)
            del(camera)
            
      elif (x==1):
            print("Enter the file source to upload")
            file=input()
            


      down=ocr_space_file(file)
      x=down.find("ParsedText")
      y=down.find("ErrorMessage")
      to_print=""
      if not(y-16==x):
            to_print=down[x+13:y-3]
            to_print=to_print.replace(r"\r\n", "\n")
            print(to_print)
            #language_id = gs.detect(to_print)
            #print("TRANSLATION: ",gs.translate(to_print, 'en'))
            
            print("Translation: ",translator('en','hi',to_print.strip(' \t\n\r'))[0][0][0])
      else:
            print("Unable to parse the image. Please check if the image is malformed \
            or too blurry and if you have specified correct language with the image.")

      #english=pytesseract.image_to_string(Image.open('test_image.png'))

      #print(pytesseract.image_to_string(Image.open('test-european.jpg'), lang='fra'))
