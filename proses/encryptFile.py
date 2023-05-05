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

class EncryptFile:
    def __init__(self, parent, title):
        self.parent = parent
        self.parent.title(title)
        self.parent.protocol("WM_DELETE_WINDOWS", self.tutup)
        lebar = 660
        tinggi = 260
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

        def save_key_to_file(key, keyfile):
            """Save the given key to a file."""
            with open(keyfile, 'wb') as f:
                f.write(key)

        def encrypt_file(filename, key):
            """Encrypt the given file using the given key."""
            f = Fernet(key)
            with open(filename, 'rb') as file:
                file_data = file.read()
            encrypted_data = f.encrypt(file_data)
            with open(filename + '.rama', 'wb') as file:
                file.write(encrypted_data)
            os.remove(filename)

        # Input dari user
        path = self.entryEncryptFile.get()
        keyfile = self.entryKeyFile.get()
        key_dir = self.entryKeyDir.get()

        # Generate atau load key
        if pathlib.Path(keyfile).is_file():
            key = load_key(keyfile)
        else:
            key = generate_key(keyfile)
            key_filename = os.path.basename(keyfile)
            with open(os.path.join(key_dir, key_filename + '.txt'), 'wb') as f:
                f.write(key)

            save_key_to_file(key, keyfile)

        root.withdraw()

        # Enkripsi file/folder
        if os.path.isfile(path):
            encrypt_file(path, key)
            print("Berhasil mengenkripsi file.")
            messagebox.showinfo("Berhasil", "File berhasil dienkripsi.")
        else:
            print("File atau direktori tidak ditemukan.")
            messagebox.showerror("Error", "File gagal dienkripsi.")
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
            self.entryEncryptFile.delete(0, END)
            self.entryEncryptFile.insert(0, filename)

    def browse_folder(self):
        foldername = filedialog.askdirectory(
            title='Select a folder',
            initialdir='/'
        )

        if foldername:
            self.entryKeyDir.delete(0, END)
            self.entryKeyDir.insert(0, foldername)

    def pro(self, event):
        self.proses()

    def aturKomponen(self):
        self.windowBerhasil = Toplevel(root)
        self.windowBerhasil.withdraw()
        frameUtama = Frame(root, width=400, height=300, bg="#75a3a3")
        frameUtama.grid(row=0, column=1)
        WindowDraggable(frameUtama)
        self.buttonX = Button(frameUtama, text="RAMA", fg="white", bg="#75a3a3", width=6, height=2, bd=0, activebackground="#fb8072", activeforeground="white", command=self.tutup, relief=FLAT)
        self.buttonX.grid(row=0, column=0)

        self.labelEncryptFile = Label(frameUtama, text="Encrypt File: ", bg="#c2d6d6", fg="black", font=("Helvetica", 12), width=12, height=2)
        self.labelEncryptFile.grid(row=1, column=1, pady=6)

        self.fileButtonX = Button(frameUtama, text="Browse", command=self.browse_file, fg="white", bg="#0066ff", width=10, height=2, bd=0, activebackground="whitesmoke", activeforeground="#444")
        self.fileButtonX.grid(row=1, column=3, pady=6, sticky="w")

        self.labelKeyFile = Label(frameUtama, text="Key Encrypt: ", bg="#c2d6d6", fg="black", font=("Helvetica", 12), width=12, height=2)
        self.labelKeyFile.grid(row=2, column=1)

        self.labelKeyDir = Label(frameUtama, text="Key Directory: ", bg="#c2d6d6", fg="black", font=("Helvetica", 12), width=12, height=2)
        self.labelKeyDir.grid(row=3, column=1)

        self.fileButtonY = Button(frameUtama, text="Browse", command=self.browse_folder, fg="white", bg="#0066ff", width=10, height=2, bd=0, activebackground="whitesmoke", activeforeground="#444")
        self.fileButtonY.grid(row=3, column=3, pady=6, sticky="w")

        self.entryEncryptFile = Entry(frameUtama, fg="black", bg="#c2d6d6", font=("Helvetica", 12), width=40, bd=11, relief=FLAT)
        self.entryEncryptFile.grid(row=1, column=2)
        self.entryEncryptFile.focus_set()

        self.entryKeyFile = Entry(frameUtama, show="*", fg="black", bg="#c2d6d6", font=("Helvetica", 12), width=40, bd=11, relief=FLAT)
        self.entryKeyFile.grid(row=2, column=2, pady=6)
        self.entryKeyFile.bind('<Return>', self.pro)

        self.entryKeyDir = Entry(frameUtama, fg="black", bg="#c2d6d6", font=("Helvetica", 12), width=40, bd=11, relief=FLAT)
        self.entryKeyDir.grid(row=3, column=2)
        self.entryKeyDir.focus_set()

        self.buttonEncryptFile = Button(frameUtama, text="Encrypt File", command=self.proses, fg="white", bg="#0066ff", width=10, height=2, bd=0, activebackground="whitesmoke", activeforeground="#444")
        self.buttonEncryptFile.grid(row=4, column=2, pady=6, sticky="e")

        root.protocol("WM_DELETE_WINDOW", self.tutup)

def main():
    EncryptFile(root, ":: Encrypt & Decrypt ::")
    EncryptFile.buka(root)
    root.mainloop()
main()
