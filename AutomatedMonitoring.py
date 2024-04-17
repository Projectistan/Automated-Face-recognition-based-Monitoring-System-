import shutil
from functools import partial
from tkinter import *
from tkcalendar import *
from PIL import ImageTk, Image
from face_register import *
from Csvgenrator import *
import threading
from recognize_faces_video import *
import os
from imutils import paths
import tkinter as tk
from tkinter import font  as tkfont, ttk, messagebox
from encode_faces import  *
from datetime import datetime


# View records
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, "dataset")
logDIR = os.path.join(BASE_DIR, "logJson")



def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)



class GUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.title("Automated Face Monitoring")
        self.minsize(600, 400)
        self.geometry("900x700")
        self.tk_setPalette(background="#000000")
        self.tk.call('wm', 'iconphoto', self._w, tk.PhotoImage(file='gui_logo.png'))
        self.resizable(False,False)






        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (mainScreen, allLog, reg_face, viewFsces, faces_reg):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("mainScreen")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]

        frame.tkraise()



class mainScreen(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


        background_image = tk.PhotoImage(file="mainscreen.png")
        background_label = tk.Label(self, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = background_image


        tk.Label(self,text="Automated Face Monitoring", anchor=CENTER, bg="#626a6a",fg="#c7d2e6",
                 font=("Helvetica", 26)).grid(row=1, column=2, columnspan=4,sticky="w",padx=40,ipadx=200,pady=20,
                                              ipady=40)
        _separator = ttk.Separator(self, orient="horizontal")
        _separator.grid(row=2, columnspan=6, sticky="ew")

        reco=tk.Label(self,width=50,height=1,bg="#c7d2e6",fg="#050505",text=" Starts the video streaming.",
                      font=("Calibri", 12))
        reco.grid(row=3,column=1,columnspan=2)

        starRecognition_Button = Button(self, text="Start Recognition",fg="black",bg="#a6776d",width=20,height=2,
                                        font=("Calibri", 13),command=self.start_thread)
        starRecognition_Button.grid(row=3, column=2,columnspan=2, padx=400, pady=20)

        reco1 = tk.Label(self, width=52,bg="#c7d2e6",fg="#050505",text="It will look for all th Users DataSet.",
                         height=1,font=("Calibri", 12))
        reco1.grid(row=5, column=1, columnspan=2)


        register_button = Button(self, text="Users", fg="black",bg="#a6776d",width=20,height=2,font=("Calibri", 13)
                                 ,command=lambda: controller.show_frame("reg_face"))
        register_button.grid(row=5, column=2,columnspan=2, pady=20, padx=20)

        reco = tk.Label(self, bg="#c7d2e6",fg="#050505",text="Display the daily track.", width=52,
                        height=1,font=("Calibri", 12))
        reco.grid(row=4, column=1, columnspan=2)


        showResult_button = Button(self, text="Daily Record",fg="black",bg="#a6776d",width=20,
                                   height=2,font=("Calibri", 13)
                                   , command=lambda: controller.show_frame("allLog"))
        showResult_button.grid(row=4, column=2,columnspan=2, pady=20, padx=20)
        reco = tk.Label(self ,bg="#c7d2e6",fg="#050505",text="To Update all the properties of system.", width=52,
                        height=1,font=("Calibri", 12))
        reco.grid(row=6, column=1, columnspan=2)


        Restart_button = Button(self, text="Refresh",fg="black",bg="#a6776d", width=20,height=2,font=("Calibri", 13)
                                , command=restart_program)
        Restart_button.grid(row=6, column=2,columnspan=2, pady=20, padx=20)
        _separator = ttk.Separator(self, orient="horizontal")
        _separator.grid(row=7, columnspan=6, sticky="ew")



    def start_thread(self):
        self.no_thread = threading.Thread(target=startRecognition)
        self.no_thread.daemon = True
        self.no_thread.start()
        self.after(1, self.check_thread)

    def check_thread(self):
        if self.no_thread.is_alive():
            self.after(1, self.check_thread)


class viewFsces(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        background_image = tk.PhotoImage(file="mainscreen.png")
        background_label = tk.Label(self, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = background_image
        tk.Label(self, text="Automated Face Monitoring", anchor=CENTER,bg="#626a6a",fg="#c7d2e6",
                 font=("Helvetica", 26)).grid(row=1,
                                              column=2, columnspan=4, sticky="w", padx=40,
                                              ipadx=200, pady=20, ipady=40)
        _separator = ttk.Separator(self, orient="horizontal")
        _separator.grid(row=2, columnspan=6, sticky="ew")


        reco = tk.Label(self, text="List of all Users.",bg="#c7d2e6",fg="#050505",width=52,
                        height=1,font=("Calibri", 12))
        reco.grid(row=3, column=1, columnspan=2)

        allFace_list = Listbox(self,font=("Calibri", 12),bg="#c7d2e6",fg="#050505")
        allFace_list.grid(row=3, column=2,columnspan=2, padx=400, pady=20)
        imagePaths = os.listdir(image_dir)

        for file in imagePaths:
            allFace_list.insert(END, file)


        def remove_face():
            curent_Selection = allFace_list.get(allFace_list.curselection())


            allFace_list.delete(ANCHOR)

            removedir = os.path.join(image_dir, str(curent_Selection))

            shutil.rmtree(removedir)


        reco = tk.Label(self,text="Selected user are removed.",bg="#c7d2e6",fg="#050505", width=52,
                        height=1,font=("Calibri", 12))
        reco.grid(row=4, column=1, columnspan=2)

        removeFace_Button = Button(self, text="Remove User",fg="black",bg="#a6776d", width=20,
                                   height=2,font=("Calibri", 11),
                                   command=remove_face)
        removeFace_Button.grid(row=4, column=2,columnspan=2, pady=20, padx=20)


        _separator = ttk.Separator(self, orient="horizontal")
        _separator.grid(row=5, columnspan=6, sticky="ew")
        backButton = Button(self,text="back",fg="black",bg="#a4801c", width=20,height=2,font=("Calibri", 10),
                            command=lambda: controller.show_frame("reg_face"))
        backButton.grid(row=6, column =2,columnspan=2, pady=20, padx=20)


#registration  of faces page

class reg_face(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        background_image = tk.PhotoImage(file="mainscreen.png")
        background_label = tk.Label(self, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = background_image

        tk.Label(self, text="Automated Face Monitoring", anchor=CENTER, bg="#626a6a",fg="#c7d2e6",
                 font=("Helvetica", 26)).grid(row=1, column=2, columnspan=4, sticky="w", padx=40, ipadx=200, pady=20,
                                              ipady=40)

        _separator = ttk.Separator(self, orient="horizontal")
        _separator.grid(row=2, columnspan=6, sticky="ew")


        reco = tk.Label(self,text="Users are added and faces are Registered.",bg="#c7d2e6",fg="#050505", width=52,
                        height=1,font=("Calibri", 12))
        reco.grid(row=3, column=1, columnspan=2)


        captureFace_Button = Button(self, text="Capture faces",fg="black",bg="#a6776d",width=20,height=2,
                                    font=("Calibri", 13),command = lambda: controller.show_frame("faces_reg"))
        captureFace_Button.grid(row=3, column=2,padx=400, pady=20,columnspan=2)

        reco = tk.Label(self,text="Users are displayed and modified.", bg="#c7d2e6",fg="#050505",width=52,
                        height=1,font=("Calibri", 12))
        reco.grid(row=4, column=1, columnspan=2)


        viewRecord_Button = Button(self, text="View",fg="black",bg="#a6776d",width=20,height=2,font=("Calibri", 13),
                                   command=lambda: controller.show_frame("viewFsces"))
        viewRecord_Button.grid(row=4, column=2, columnspan=2, pady=20, padx=20)

        reco = tk.Label(self,text="All the features of user's faces are extracted \nand stored here. ",bg="#c7d2e6",
                        fg="#050505", width=52, height=2,font=("Calibri", 12))
        reco.grid(row=5, column=1, columnspan=2)

        encode_Button = Button(self, text="Encode",fg="black",bg="#a6776d",width=20,height=2,font=("Calibri", 13),
                               command=self.start_thread)
        encode_Button.grid(row=5, column=2,columnspan=2, pady=20, padx=20)


        self.processVar = tk.StringVar(value="")
        self.processsLabel = tk.Label(self, textvar=self.processVar,fg="black",bg="white")
        self.processsLabel.grid(row=6,column=2,columnspan=2, pady=20, padx=20)

        _separator = ttk.Separator(self, orient="horizontal")
        _separator.grid(row=7, columnspan=6, sticky="ew")

        backButton = Button(self, text="back",fg="black",bg="#a4801c",width=20,height=2,font=("Calibri", 10),
                            command=lambda: controller.show_frame("mainScreen"))
        backButton.grid(row=8,column=2,columnspan=2,  pady=20, padx=20)

    def start_thread(self):
        self.no_thread = threading.Thread(target=encodings, args=[self.processVar])
        self.no_thread.daemon = True
        self.no_thread.start()
        self.after(1, self.check_thread)

    def check_thread(self):
        if self.no_thread.is_alive():
            self.after(1, self.check_thread)


#capture faces

class faces_reg(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        background_image = tk.PhotoImage(file="mainscreen.png")
        background_label = tk.Label(self, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = background_image

        tk.Label(self, text="Automated Face Monitoring", anchor=CENTER, bg="#626a6a",fg="#c7d2e6",
                 font=("Helvetica", 26)).grid(row=1, column=2, columnspan=4, sticky="w", padx=40, ipadx=200, pady=20,
                                              ipady=40)


        _separator = ttk.Separator(self, orient="horizontal")
        _separator.grid(row=2, columnspan=6, sticky="ew")


        reco = tk.Label(self,text="Enter the name of user.", bg="#c7d2e6",fg="#050505",width=52, height=1,
                        font=("Calibri", 12))
        reco.grid(row=3, column=1, columnspan=2)




        inputUser=Entry(self,bg="white",fg="black",width="20",font=("Calibri", 15))
        inputUser.grid(row=3, column=2,columnspan=2, pady=20, padx=20)


        reco = tk.Label(self,text="Creation of user.", bg="#c7d2e6",fg="#050505",width=52, height=1,
                        font=("Calibri", 12))
        reco.grid(row=4, column=1, columnspan=2)

        creatUser_Button= Button(self, text="Create user",fg="black",bg="#a6776d",width=20,height=2,
                                 font=("Calibri", 11),command=lambda: createUser(str(inputUser.get())))
        creatUser_Button.grid(row=4, column=2, columnspan=2, pady=20, padx=400)


        reco = tk.Label(self,text="Registration of faces.", bg="#c7d2e6",fg="#050505",width=52, height=1,
                        font=("Calibri", 12))
        reco.grid(row=5, column=1, columnspan=2)

        capture_Button= Button(self, text="Capture Face",fg="black",bg="#a6776d",width=20,height=2,
                               font=("Calibri", 11),command=lambda: capture(str(inputUser.get())))
        capture_Button.grid(row=5, column=2, columnspan=2, pady=20, padx=20)


        _separator = ttk.Separator(self, orient="horizontal")
        _separator.grid(row=6, columnspan=6, sticky="ew")

        backButton = Button(self, text="back", fg="black",bg="#a4801c",width=20,height=2,
                            font=("Calibri", 10),command=lambda: controller.show_frame("reg_face"))
        backButton.grid(row=7, column=2, columnspan=2, pady=20, padx=20)


# all log files

class allLog(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


        background_image = tk.PhotoImage(file="mainscreen.png")
        background_label = tk.Label(self, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = background_image
        tk.Label(self, text="Automated Face Monitoring", anchor=CENTER,bg="#626a6a",fg="#c7d2e6",
                 font=("Helvetica", 26)).grid(row=1, column=2, columnspan=4, sticky="w", padx=40, ipadx=200, pady=20,
                                              ipady=40)

        _separator = ttk.Separator(self, orient="horizontal")
        _separator.grid(row=2, columnspan=6, sticky="ew")
        selectLabel = Label(self, text="Select Date:-", bg="#c7d2e6",fg="#050505",width=20,height=2,
                            font=("Calibri", 12)).grid(row=3, column=2,columnspan=2 )
        time_now = datetime.now()

        entrydate = DateEntry(self,font=("Calibri", 12), width=15, background="blue", foregronud="red", borderwidth=3,
                              date_pattern='dd-mm-yy')

        def date_check():

            calendar_date = datetime.strptime(entrydate.get(), "%d-%m-%y")

            if calendar_date > time_now:
                messagebox.showerror("Error", "Selected date must not exceed current date")

                entrydate.set_date(time_now)

            self.after(100, date_check)

        self.after(100, date_check)
        entrydate.grid(row=3, column=3)
        global dateValue
        dateValue = entrydate.get()


        nameLabel = Label(self, text="Enter name:-", bg="#c7d2e6",fg="#050505",
                          width=20,height=2,font=("Calibri", 12)).grid(row=4, column=2,columnspan=2 )
        inputName = Entry(self,font=("Calibri", 12), bg="#c7d2e6",fg="#050505")
        inputName.grid(row=4, column=3)

        global nameValue
        nameValue = inputName.get()


        getCsv = Button(self, text="show Record",fg="black",bg="#a6776d",width=20,height=2,
                        font=("Calibri", 11), command=lambda: parser_pr(str(inputName.get()), str(entrydate.get())))
        getCsv.grid(row=5, column=2 ,columnspan=2, pady=20, padx=400)

        tk.Label(self,text="All Log Files", bg="#c7d2e6",fg="#050505",font=("Calibri", 12)).grid(row=6,column=2)
        tk.Label(self, text="All Users", bg="#c7d2e6",fg="#050505",font=("Calibri", 12)).grid(row=6, column=3)
        def viewalllog():
            alllog_list = Listbox(self,font=("Calibri", 12), bg="#c7d2e6",fg="#050505",)
            alllog_list.grid(row=7, column=2)
            logPaths = os.listdir(logDIR)


            for file in logPaths:
                if file.endswith("json"):
                    alllog_list.insert(0, file)

        allFace_list = Listbox(self,font=("Calibri", 12), bg="#c7d2e6",fg="#050505",)
        allFace_list.grid(row=7, column=3)
        imagePaths = os.listdir(image_dir)


        for file in imagePaths:
            allFace_list.insert(0, file)
        viewalllog()

        _separator = ttk.Separator(self, orient="horizontal")
        _separator.grid(row=8, columnspan=6, sticky="ew")

        backButton = Button(self, text="back", fg="black",bg="#a4801c",width=20,height=2,
                            font=("Calibri", 10),command=lambda: controller.show_frame("mainScreen"))
        backButton.grid(row=9  , column=2,columnspan=2, pady=20, padx=400)




if __name__ == "__main__":
    app = GUI()
    app.mainloop()