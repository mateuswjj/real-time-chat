import socket as sock
import threading

HOST = "26.84.106.82"
PORT = 9999
data_payload = 2048


connected_clients = [] # Armazena apenas os sockets
client_names = {}# Relaciona o socket ao name do cliente

def send_to_all(message):
    for cliente in connected_clients:
        try:
            cliente.send(message) # Envia a message para todos os clientes
        except Exception as e:
            print(f"Erro ao enviar message para um cliente: {e}")


def handle_client(client, address):
    try:
        client.send("Digite seu nome: ".encode('utf-8'))
        name = client.recv(data_payload).decode('utf-8')
        
        connected_clients.append(client) # Armazena apenas o socket
        client_names[client] = name # Relaciona o socket ao name
        
        print(f"{name} ({address}) entrou no chat.")
        send_to_all(f"{name} entrou no chat! No endereço {address}.".encode('utf-8'))
        
        while True:
            data = client.recv(data_payload)
            if not data:
                break
            
            message = data.decode('utf-8')
            print(f"{name}: {message}")
            
            if message.startswith("@"):  # message privada
                recipient, private_message = message[1:].split(" ", 1)
                send_private_message(client, recipient, private_message)
                
            elif message == "/sair":
                connected_clients.remove(client)
                del client_names[client]
                client.close()
                print(f"{name} ({address}) desconectou.")
                send_to_all(f"{name} saiu do chat.".encode('utf-8'))
            else:  # message pública
                send_to_all(f"{name}: {message}".encode('utf-8'))
    except Exception as e:
        print(f"Erro com o cliente {address}: {e}")
    finally:
        connected_clients.remove(client)
        del client_names[client]
        client.close()
        print(f"{name} ({address}) desconectou.")
        send_to_all(f"{name} saiu do chat.".encode('utf-8'))



def send_private_message(sender_socket, recipient, message):
    remetente = client_names[sender_socket]
    for cliente, name in client_names.items():
        if name == recipient:
            try:
                cliente.send(f"[Privado de {remetente}]: {message}".encode('utf-8'))
                return
            except Exception as e:
                print(f"Erro ao enviar message privada: {e}")
                return
    sender_socket.send(f"{recipient} não está no chat.".encode('utf-8'))



# Cria o socket do servidor
s = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
s.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(3)

print(f"Servidor esperando conexões em {HOST}:{PORT}...")

# Aguardar conexões de clientes
while True:
    client, address = s.accept()
    print(f"Cliente conectado: {address}")

    # Cria uma nova thread para lidar com o cliente
    thread = threading.Thread(target=handle_client, args=(client, address))
    thread.start()

s.close()
