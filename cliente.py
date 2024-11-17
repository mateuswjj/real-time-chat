import socket as sock
import tkinter as tk
from tkinter import scrolledtext
import threading

HOST = "127.0.0.1" 
PORT = 9999

s = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
print(f"Conectando a {HOST}:{PORT}")
s.connect((HOST, PORT))

name = input("Digite seu npme: ")
s.send(name.encode('utf-8')) #Envia o name para o servidor

def send_message():
    message = text_input.get()  
    if message.lower() == 'sair':
        s.send(f"{name} saiu do chat.".encode('utf-8'))
        window.quit() 
    else:
        try:
            s.send(message.encode('utf-8')) #Envia a message para o servidor
            text_input.delete(0, tk.END) 
        except sock.error as e:
            print(f"Erro de socket: {str(e)}")

def receive_messages():
    while True:
        try:
            data = s.recv(2048)  # Recebe mensagens do servidor
            if data:
                text_area.config(state=tk.NORMAL)  
                text_area.insert(tk.END, f"{data.decode('utf-8')}\n\n")
                text_area.config(state=tk.DISABLED) 
                text_area.yview(tk.END) 
        except sock.error as e:
            print(f"Erro ao receber message: {e}")
            break

# Interface
window = tk.Tk()
window.title(f"Chat Cliente - {name}")
text_area = scrolledtext.ScrolledText(window, width=50, height=15, wrap=tk.WORD, state=tk.DISABLED)
text_area.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
text_input = tk.Entry(window, width=40)
text_input.grid(row=1, column=0, padx=10, pady=10)
send_button = tk.Button(window, text="Enviar", command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10)

# Inicia a thread
thread_get = threading.Thread(target=receive_messages)
thread_get.daemon = True
thread_get.start()

# Inicia a interface gráfica
window.mainloop()

# Fechar a conexão com o servidor
s.close()
