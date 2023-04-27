from tkinter import *
import sys
root = Tk()
class WindowDraggable():
    def __init__(self, label):
        self.label = label
        label.bind('<ButtonPress-1>', self.StartMove)
        label.bind('<ButtonRelease-1>', self.StopMove)
        label.bind('<B1-Motion>', self.OnMotion)
    def StartMove(self, event):
        self.x = event.x
        self.y = event.y
    def StopMove(self, event):
        self.x = None
        self.y = None
    def OnMotion(self, event):
        x = (event.x_root - self.x - self.label.winfo_rootx() + self.label.winfo_rootx())
        y = (event.y_root - self.y - self.label.winfo_rooty() + self.label.winfo_rooty())
        root.geometry("+%s+%s" %(x, y))
class Menu:
    def __init__(self, parent, title):
        self.parent = parent
        self.parent.title(title)
        self.parent.protocol("WM_DELETE_WINDOWS", self.keluar)
        lebar = 290
        tinggi = 180
        setTengahX = (self.parent.winfo_screenwidth() - lebar) // 2
        setTengahY = (self.parent.winfo_screenheight() - tinggi) // 2
        self.parent.geometry("%ix%i+%i+%i" %(lebar, tinggi, setTengahX, setTengahY))
        # self.parent.overrideredirect(1)
        self.parent.resizable(False, False)
        self.parent.iconbitmap(r"C:\Users\admin\Documents\Python\EncDec\Encrypt-Decrypt-v1.3\enc&dec.ico")
        self.parent.configure(bg = "#75a3a3")
        self.aturKomponen()
        
    def keluar(self, event = None):
        self.parent.quit()
        sys.exit()

    def encryptSatuFile(self):
        from proses import encryptFile
        encryptFile.main()
        
    def dekripsiSatuFile(self):
        from proses import decryptFile
        decryptFile.main()

    def enkripsiSatuFolder(self):
        from proses import encryptFolder
        encryptFolder.main()
    
    def dekripsiSatuFolder(self):
        from proses import decryptFolder
        decryptFolder.main()

    def aturKomponen(self):
        frameUtama = Frame(root, width=400, height=300, bg="#75a3a3")
        frameUtama.grid(row=0, column=1)
        WindowDraggable(frameUtama)
        self.buttonX = Button(frameUtama, text="RAMA", fg="white", bg="#75a3a3", width=6, height=2, bd=0, activebackground="#fb8072", activeforeground="white", command=self.keluar, relief=FLAT)
        self.buttonX.grid(row=0, column=0)

        self.encrypt = Button(frameUtama, text="Encrypt File", command=self.encryptSatuFile, fg="white", bg="#0066ff", width=13, height=2, bd=0, activebackground="whitesmoke", activeforeground="#444")
        self.encrypt.grid(row=3, column=2, pady=6, padx=2, sticky="e")
        self.decrypt = Button(frameUtama, text="Decrypt File", command=self.dekripsiSatuFile, fg="white", bg="#0066ff", width=13, height=2, bd=0, activebackground="whitesmoke", activeforeground="#444")
        self.decrypt.grid(row=3, column=6, pady=6, padx=2, sticky="e")

        self.decrypt = Button(frameUtama, text="Encrypt Folder", command=self.enkripsiSatuFolder, fg="white", bg="#0066ff", width=13, height=2, bd=0, activebackground="whitesmoke", activeforeground="#444")
        self.decrypt.grid(row=6, column=2, pady=6, padx=2, sticky="e")
        self.decrypt = Button(frameUtama, text="Decrypt Folder", command=self.dekripsiSatuFolder, fg="white", bg="#0066ff", width=13, height=2, bd=0, activebackground="whitesmoke", activeforeground="#444")
        self.decrypt.grid(row=6, column=6, pady=6, padx=2, sticky="e")

        root.protocol("WM_DELETE_WINDOW", self.keluar)
        
def main():
    Menu(root, "Encrypt & Decrypt")
    root.mainloop()