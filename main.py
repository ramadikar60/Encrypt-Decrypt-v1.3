import tkinter as Tk
from tkinter import *
from tkinter import ttk
class SplashScreen:
    # membuat funtion memulai untuk membuat tampilan GUI untuk loading
    def __init__(self, parent):
        self.parent = parent
        self.aturWindow()
    # membuat function untuk mengatur lebar dan tinggi dari GUI loading
    def aturWindow(self):
        # ambil ukuran dari file image
        lebar = 300
        tinggi = 100
        setengahLebar = (self.parent.winfo_screenwidth() - lebar) // 2
        setengahTinggi = (self.parent.winfo_screenheight() - tinggi) // 2
        self.parent.geometry("%ix%i+%i+%i" %(lebar, tinggi, setengahLebar, setengahTinggi))

        # atur image via komponen label
        Label(self.parent, text = "Loading", bg = "#0077b3", fg = "white", font = ("Helvetica", 20), width = 9, height = 2).pack(side = TOP, anchor = N, fill = X)
        s = ttk.Style()
        s.theme_use('alt')
        s.configure("red.Horizontal.TProgressbar", background = "#444", foreground = "white", relief = FLAT, bd = 0, height = 2)
        self.progress = ttk.Progressbar(self.parent, style="red.Horizontal.TProgressbar", orient = "horizontal", length = 600, mode = "determinate")
        self.progress.pack(side = TOP, anchor = N, padx = 10)
        self.bytes = 0
        self.maxbytes = 0
        self.start()
    # membuat function untuk memulai bar untuk loading 
    def start(self):
        self.progress["value"] = 0
        self.maxbytes = 50000
        self.progress["maximum"] = 50000
        self.read_bytes()
        if self.progress["value"] == 60000:
            self.parent.destroy()
            if self.parent.destroy:
                # jika bar di loading sudah penuh maka akan di redirect ke file lain yaitu login 
                import login
                login.main()
    def read_bytes(self):
        '''simulate reading 500 bytes, update progress bar'''
        # self.bytes += 40 + self.bytes
        self.bytes += 1000
        self.progress["value"] = self.bytes
        self.progress.after(100, self.start)
# selanjutnya membuat function main untuk menjalankan semua perintah/menjalankan class di atas agar berjalan membuat GUI loading
def main():
    root = Tk()
    root.configure(bg = "#0077b3")
    # menghilangkan judul dan batas frame window
    root.overrideredirect(True)
    SplashScreen(root)
    root.mainloop()
main()