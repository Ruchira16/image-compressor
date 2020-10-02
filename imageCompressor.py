from tkinter import *
from tkinter import filedialog,messagebox
import pathlib
from PIL import Image
import os
from tkinter import ttk


class Compressor:
    def __init__(self,root):
        self.root = root
        self.path = ''
        self.total = 0
        path = pathlib.Path.home()
        path = os.path.join(path,'Desktop')
        dir = 'ImageCompressor'
        self.save_path = os.path.join(path, dir)
        if os.path.isdir(self.save_path):
            pass
        else:
            os.mkdir(self.save_path, 0o666)

        scroll_y = ttk.Scrollbar(self.root)
        scroll_x = ttk.Scrollbar(self.root,orient=HORIZONTAL)
        self.image_list = Listbox(self.root,font=("arial",10),yscrollcommand=scroll_y.set,xscrollcommand=scroll_x.set)
        self.image_list.place(x=10,y=20,width=200,height=200)
        scroll_y.config(command=self.image_list.yview)
        scroll_x.config(command=self.image_list.xview)
        scroll_y.place(x=210,y=20,height=200)
        scroll_x.place(x=10,y=220,width=213)

        ttk.Button(self.root,text="Browse",command=self.browse).place(x=255,y=20)
        ttk.Button(self.root, text="Folder", command=self.open_folder).place(x=255, y=60)
        ttk.Button(self.root, text="Remove", command=lambda :self.image_list.delete(ACTIVE)).place(x=255, y=100)
        ttk.Button(self.root, text="Clear", command=lambda :self.image_list.delete(0,END)).place(x=255, y=140)
        ttk.Button(self.root, text="Compress", command=self.compress).place(x=255, y=180)
        ttk.Button(self.root, text="Save At", command=self.save_at).place(x=255, y=220)


        scale_frame = ttk.LabelFrame(self.root,text="Adjust Quality",)
        scale_frame.place(x=10,y=240,width=210,height=80)
        self.scale = Scale(scale_frame,from_ =0 ,to= 100,length=200,orient=HORIZONTAL)
        self.scale.set(50)
        self.scale.place(x=0,y=5)

        self.total_size = ttk.Label(self.root,text="Size: 00",font=('times',11,'bold'))
        self.total_size.place(x=240,y=260)

        self.new_size = ttk.Label(self.root, text="New: ?",  font=('times', 11, 'bold'))
        self.new_size.place(x=240, y=300)




    def compress(self):
        new = 0
        images = self.image_list.get(0,END)
        for image in images:
            new_img = f"{self.path}/{str(image)}".split(" | ")[0]
            com_img = f"{str(image)}".split(" | ")[0]
            com_img = os.path.splitext(com_img)[0]+".png"
            com_img = f"{self.save_path}\\{com_img}"


            try:
                im = Image.open(new_img)
                im.save(com_img, optimize=True, quality=self.scale.get())
                size = os.path.getsize(com_img)
                new += size

            except Exception as e:
                print(e)
                messagebox.showerror("Compressor says",e)
                break
        if(new):
            self.new_size['text'] = 'New: ' + self.humanbytes(new)




    def humanbytes(size,B):
        'Return the given bytes as a human friendly KB, MB, GB, or TB string'
        B = float(B)
        KB = float(1024)
        MB = float(KB ** 2)  # 1,048,576
        GB = float(KB ** 3)  # 1,073,741,824
        TB = float(KB ** 4)  # 1,099,511,627,776

        if B < KB:
            return '{0} {1}'.format(B, 'Bytes' if 0 == B > 1 else 'Byte')
        elif KB <= B < MB:
            return '{0:.2f} KB'.format(B / KB)
        elif MB <= B < GB:
            return '{0:.2f} MB'.format(B / MB)
        elif GB <= B < TB:
            return '{0:.2f} GB'.format(B / GB)
        elif TB <= B:
            return '{0:.2f} TB'.format(B / TB)

    def list_insert(self,image):
        size = os.path.getsize(image)
        self.total += size
        image = image.split(self.path+"/")
        self.image_list.insert(END,f"{image[1]} | {self.humanbytes(size)}")


    def open_folder(self):
        self.path = ''
        self.path = filedialog.askdirectory()
        if(self.path):
            images = os.listdir(self.path)
            for image in images:
                if image.endswith('.png') or image.endswith('.JPG'):
                    size = os.path.getsize(f"{self.path}\\{image}")
                    self.total+=size
                    self.image_list.insert(END,f"{image} | {self.humanbytes(size)}")
            self.total_size['text'] = 'Size: ' + self.humanbytes(self.total)





    def browse(self):

        self.images = filedialog.askopenfilenames(defaultextension = ".png",
                                                    filetypes = [("All Files" , "*.*"),
                                                                 ("PNG" , "*.png"),
                                                                 ("JPEG" , "*.jpg"),
                                                                 ])

        if(self.images):
            self.path = os.path.dirname(self.images[0])
            for image in self.images:
                self.list_insert(image)

        self.total_size['text'] = 'Size: '+self.humanbytes(self.total)


    def save_at(self):
        save = self.save_path
        self.save_path = filedialog.askdirectory()
        if(self.save_path):
            pass
        else:
            self.save_path = save







root = Tk()
s = ttk.Style(root)
s.theme_use('clam')
root.title("Image Compressor")
#root.configure(bg="silver")
root.geometry("360x330")
Compressor(root)
root.mainloop()