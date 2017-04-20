import sys
import Algorithmia
import datetime
import os
import getpass
from PyQt4.QtCore import *
from PyQt4.QtGui import *



class Data:
   input_image =""
   output_image =""
   filters = 0

client = Algorithmia.client("API_KEY")

#style filters 
Fil = [ 
         'alien_goggles', 'aqua','blue_brush', 'blue_granite', 'bright_sand', 
         'cinnamon_rolls', 'clean_view', 'colorful_blocks', 'colorful_dream', 
         'crafty_painting', 'creativity', 'crunch_paper', 'dark_rain', 
         'dark_soul', 'deep_connections', 'dry_skin', 'far_away', 
         'gan_vogh', 'gred_mash', 'green_zuma', 'hot_spicy', 
         'neo_instinct', 'oily_mcoilface', 'plentiful', 'post_modern', 
         'purp_paper', 'purple_pond', 'purple_storm', 'rainbow_festival', 
         'really_hot', 'sand_paper', 'smooth_ride', 'space_pizza', 
         'spagetti_accident', 'sunday', 'yellow_collage', 'yellow_paper'
      ]

def write(file_, bytes_):
    file_.write(bytes_)

class filedialogdemo(QWidget):
   def __init__(self, parent = None):
      super(filedialogdemo, self).__init__(parent)

      #open image file
      layout = QVBoxLayout()

      self.de = QLabel("Defaut image name is image.jpg")
      layout.addWidget(self.de)

      self.op = QPushButton("Open Image")
      self.op.move(150, 50)
      self.op.clicked.connect(self.getfile)
      layout.addWidget(self.op)
      
      #filter dropdown
      self.cb = QComboBox()
      for x in range(0,37):
         self.cb.addItem(Fil[x])
      layout.addWidget(self.cb)
      self.cb.currentIndexChanged.connect(self.selectionchange)

      #process image button
      self.proc = QPushButton("Process....")
      self.proc.move(150, 50)
      self.proc.clicked.connect(self.process)
      layout.addWidget(self.proc)

        #save Button
      self.save = QPushButton("Save")
      self.save.move(150, 50)
      self.save.clicked.connect(self.selectDirectory)
      layout.addWidget(self.save)

      #image label
      self.le = QLabel("Click Open Image to choose and image .......")
      layout.addWidget(self.le)
      
      self.setGeometry(50,50,500,100)
      self.setLayout(layout)
      self.setWindowTitle("Awesome Style demo")
      
   def getfile(self):
      fname = QFileDialog.getOpenFileName(self, 'Ahmed-khaled', 'c:\\',"Image files (*.jpg *.gif *.png *.bmp)")
      pixmap = QPixmap(fname).scaled(500, 500, Qt.KeepAspectRatio)
      self.le.setPixmap(pixmap)
      Data.input_image = fname

   def selectionchange(self, i):
      Data.filters = i

   def process(self):

      #the file you are going to upload to the server
      image_to_upload = Data.input_image
      #filename, file_extension = os.path.splitext(image_to_upload)
      #the file name you are going to upload to the Data Collection
      unique_name=getpass.getuser()+".jpg"

      imag_to_style = "data://ahmedkhd/DeepFilterTest/"+unique_name

      #upload the file to the Data Collection
      client.file(imag_to_style).putFile(image_to_upload)

      #style options
      input = {
      "images": ["data://ahmedkhd/DeepFilterTest/"+unique_name],
      "savePaths": ["data://ahmedkhd/DeepFilterTest/"+"123456"+unique_name],
      "filterName": Fil[Data.filters]
      }

      if not client.dir("data://ahmedkhd/DeepFilterTest").exists():
         client.dir("data://ahmedkhd/DeepFilterTest").create()

      result = client.algo("deeplearning/DeepFilter").pipe(input).result

      self.f = client.file("data://ahmedkhd/DeepFilterTest/"+"123456"+unique_name).getBytes()
      file = open("temp","wb")
      write(file,self.f)
      self.le.setPixmap(QPixmap("temp").scaled(500, 500, Qt.KeepAspectRatio))

   def save_image(self,dir):
   	  image_path = dir+"/image.jpg"
   	  file = open(image_path,"wb")
   	  write(file,self.f)

   def selectDirectory(self):
   	selected_directory =QFileDialog.getExistingDirectory()
   	self.save_image(selected_directory)
   	

def main():
   app = QApplication(sys.argv)
   ex = filedialogdemo()
   ex.show()
   sys.exit(app.exec_())
   
if __name__ == '__main__':
   main()