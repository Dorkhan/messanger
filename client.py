import tkinter as tk
from threading import Thread
from socket import AF_INET, socket, SOCK_STREAM
from datetime import datetime

def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            formatted_msg = f"{datetime.now().strftime('%H:%M:%S')} {msg}"
            msg_list.insert(tk.END, formatted_msg)
        except OSError:
            break

def send(event=None):
    msg = my_msg.get()
    my_msg.set("")
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()

def on_closing(event=None):
    my_msg.set("{quit}")
    send()

def setup_connection():
    global client_socket

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    receive_thread = Thread(target=receive)
    receive_thread.start()

# Tkinter setup
top = tk.Tk()
top.title("Tkinter Chat")

messages_frame = tk.Frame(top)
my_msg = tk.StringVar()
my_msg.set("Введите ваше сообщение здесь")
scrollbar = tk.Scrollbar(messages_frame)
msg_list = tk.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tk.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tk.Button(top, text="Отправить", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

HOST = '127.0.0.1'
PORT = 33000
BUFSIZ = 1024

setup_connection()

tk.mainloop()
