#!/usr/bin/python
import socket, threading, Crypto
from Crypto.PublicKey import RSA
from tkinter import *

nick = []
chuncks = []

def out():
    root.destroy()
    sock.close()
    quit()

def getNick(event, e):
    s = e.get()
    nick.append(s)
    sock.send(s.encode())
    e.delete(0, END)
    root.bind('<Return>', lambda event: getInput(event, e))
    for widget in root.winfo_children():
        if widget != e:
            widget.destroy()

def getInput(event, e):
    s = e.get()
    if s != '':
        chuncks = []
        chunck(s, 50, chuncks)
        if len(root.winfo_children()) >= 13 or s == '/online':
            for widget in root.winfo_children():
                if widget != e:
                    widget.destroy()
        if s != '/online':
            w = Label(root, text='You > ' + chuncks[0])
            w.pack()
            del chuncks[0]
            for c in chuncks:
                w = Label(root, text=c)
                w.pack()
            s = nick[0] + ' > ' + s
        s = s.encode()
        s = servkey.encrypt(s, 32)[0]
        sock.send(s)
        e.delete(0, END)

def clear():
    for widget in root.winfo_children():
        widget.destroy()

    e = Entry(root)
    e.place(x=125, y=275)

def rMsg(e):
    while True:
        try:
            chuncks = []
            msg = sock.recv(1024)
            try:
                msg = key.decrypt(msg).decode()
            except:
                msg = msg.decode()
            if msg == '\x00':
                continue
            chunck(msg, 50, chuncks)
            if len(root.winfo_children()) + len(chuncks) >= 14:
                for widget in root.winfo_children():
                    if widget != e:
                        widget.destroy()
            for c in chuncks:
                w = Label(root, text=c)
                w.pack()
        except:
            sock.close()
            sock.send('disconnect'.encode())
            quit()

def chunck(string, size, lst):
    for i in range(0, len(string), size):
        lst.append(string[i:i+size])

root = Tk()
root.geometry('400x300')
root.resizable(False, False)
app = Frame(root)
app.master.title('PyChat')
app.pack()

root.protocol('WM_DELETE_WINDOW', out)
root.bind('<Return>', lambda event: getNick(event, e))

key = RSA.generate(1024)
public = key.publickey()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = ('localhost', 4444)
print('Connecting to %s on port %s' %server)
sock.connect(server)
print('Connected!')

servkey = sock.recv(1024)
servkey = RSA.importKey(servkey)
sock.send(public.exportKey())

e = Entry(root)
w = Label(root, text='Enter You nickname')
w.pack()
e.place(relx=0.5, rely=0.9, anchor=CENTER)

t = threading.Thread(target=rMsg, args=(e,))
t.start()

root.mainloop()


