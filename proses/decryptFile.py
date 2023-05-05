from tkinter import *
from tkinter import filedialog, messagebox
import pathlib
import os
from cryptography.fernet import Fernet
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

class DecryptFile:
    def __init__(self, parent, title):
        self.parent = parent
        self.parent.title(title)
        self.parent.protocol("WM_DELETE_WINDOWS", self.tutup)
        lebar = 660
        tinggi = 250
        setTengahX = (self.parent.winfo_screenwidth() - lebar) // 2
        setTengahY = (self.parent.winfo_screenheight() - tinggi) // 2
        self.parent.geometry("%ix%i+%i+%i" %(lebar, tinggi, setTengahX, setTengahY))
        # self.parent.overrideredirect(1)
        self.parent.resizable(False, False)
        self.parent.iconbitmap(r"C:\Users\user\Encrypt-Decrypt-v1.3\enc&dec.ico")
        self.parent.configure(bg = "#75a3a3")
        self.aturKomponen()

    def tutup(self, event = None):
        self.parent.withdraw()
 
    def buka(self, event = None):
        self.deiconify()
 
    def proses(self, event = None):
        def generate_key(keyfile):
            """Generate a new key and save it to a file."""
            key = Fernet.generate_key()
            with open(keyfile, 'wb') as f:
                f.write(key)
            return key

        def load_key(keyfile):
            """Load a key from the given file."""
            with open(keyfile, 'rb') as f:
                return f.read()

        def decrypt_file(filename, key):
            """Decrypt the given file using the given key."""
            f = Fernet(key)
            with open(filename, 'rb') as file:
                encrypted_data = file.read()
            try:
                decrypted_data = f.decrypt(encrypted_data)
            except:
                messagebox.showerror("Error", "Key dekripsi tidak sama dengan key enkripsi. File gagal didekripsi.")
                return False
            with open(filename[:-5], 'wb') as file:
                file.write(decrypted_data)
            os.remove(filename)
            return True

        # Input dari user
        path = self.entryDecryptFile.get()
        keyfile = self.entryKeyFile.get()

        # Generate atau load key
        if pathlib.Path(keyfile).is_file():
            key = load_key(keyfile)
        else:
            key = generate_key(keyfile)

        root.withdraw()

        # Dekripsi file/folder
        if os.path.isfile(path):
            if decrypt_file(path, key):
                print("Berhasil mendekripsi file.")
                messagebox.showinfo("Berhasil", "File berhasil didekripsi.")
            else:
                print("Folder gagal didekripsi.")
                messagebox.showerror("Error", "Folder gagal didekripsi.")
        else:
            print("File atau direktori tidak ditemukan.")
            messagebox.showerror("Error", "File gagal didekripsi.")
        
        # Hapus keyfile jika file/folder sudah didekripsi
        if pathlib.Path(keyfile).is_file():
            os.remove(keyfile)
            print("File key berhasil dihapus.")
        else:
            print("File key tidak ditemukan.")

    def browse_file(self):
        filetypes = (
            ('all files', '*.*'),
            ('text files', '*.txt'),
            ('Python files', '*.py'),
            ('Image files', '*.jpg;*.png'),
        )

        filename = filedialog.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes
        )

        if filename:
            self.entryDecryptFile.delete(0, END)
            self.entryDecryptFile.insert(0, filename)

    def pro(self, event):
        self.proses()

    def aturKomponen(self):
        frameUtama = Frame(root, width=400, height=300, bg="#75a3a3")
        frameUtama.grid(row=0, column=1)
        WindowDraggable(frameUtama)
        self.buttonX = Button(frameUtama, text="RAMA", fg="white", bg="#75a3a3", width=6, height=2, bd=0, activebackground="#fb8072", activeforeground="white", command=self.tutup, relief=FLAT)
        self.buttonX.grid(row=0, column=0)

        self.labelDecryptFile = Label(frameUtama, text="Encrypt File: ", bg="#c2d6d6", fg="black", font=("Helvetica", 12), width=12, height=2)
        self.labelDecryptFile.grid(row=1, column=1, pady=6)

        self.fileButton = Button(frameUtama, text="Browse", command=self.browse_file, fg="white", bg="#0066ff", width=10, height=2, bd=0, activebackground="whitesmoke", activeforeground="#444")
        self.fileButton.grid(row=1, column=3, pady=6, sticky="w")

        self.labelKeyFile = Label(frameUtama, text="Key Encrypt: ", bg="#c2d6d6", fg="black", font=("Helvetica", 12), width=12, height=2)
        self.labelKeyFile.grid(row=2, column=1, )

        self.labelNote = Label(frameUtama, text="Note: ", bg="#75a3a3", fg="red", font=("Helvetica", 12), width=12, height=2)
        self.labelNote.grid(row=3, column=1)

        self.entryDecryptFile = Entry(frameUtama, fg="black", bg="#c2d6d6", font=("Helvetica", 12), width=40, bd=11, relief=FLAT)
        self.entryDecryptFile.grid(row=1, column=2)
        self.entryDecryptFile.focus_set()

        self.entryKeyFile = Entry(frameUtama, show="*", fg="black", bg="#c2d6d6", font=("Helvetica", 12), width=40, bd=11, relief=FLAT)
        self.entryKeyFile.grid(row=2, column=2)
        self.entryKeyFile.bind('<Return>', self.pro)

        self.labelNote = Label(frameUtama, text="Key Decrypt will be same from Key Encrypt", fg="red", bg="#75a3a3", font=("Helvetica", 12), width=40, bd=11, relief=FLAT)
        self.labelNote.grid(row=3, column=2, pady=6)

        self.buttonDecryptFile = Button(frameUtama, text="Encrypt File", command=self.proses, fg="white", bg="#0066ff", width=10, height=2, bd=0, activebackground="whitesmoke", activeforeground="#444")
        self.buttonDecryptFile.grid(row=4, column=2, pady=6, sticky="e")

        root.protocol("WM_DELETE_WINDOW", self.tutup)

def main():
    DecryptFile(root, ":: Encrypt & Decrypt ::")
    DecryptFile.buka(root)
    root.mainloop()
main()
