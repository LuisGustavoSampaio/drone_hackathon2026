import airsim
import time
import socket
import json
import threading
import numpy as np

# ================= SOCKET =================
HOST = "0.0.0.0"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Aguardando conexão...")
conn, addr = server.accept()
print(f"Conectado por {addr}")

estado_recebido = {}

def receber_dados():
    global estado_recebido
    while True:
        try:
            data = conn.recv(4096)
            if not data:
                continue
            estado_recebido = json.loads(data.decode())
        except:
            print("Erro ao receber dados")

threading.Thread(target=receber_dados, daemon=True).start()

# ================= AIRSIM =================
client = airsim.MultirotorClient()
client.confirmConnection()

drones = ['Drone1', 'Drone2', 'Drone3_0', 'Drone4']

# ================= FORMAÇÕES =================
offsets_v = {
    'Drone1': (0, 0, 0),
    'Drone2': (-3, -3, 0),
    'Drone3_0': (-3, 3, 0),
    'Drone4': (-6, 0, 0)
}

offsets_linha = {
    'Drone1': (0, -6, 0),
    'Drone2': (0, -2, 0),
    'Drone3_0': (0, 2, 0),
    'Drone4': (0, 6, 0)
}

formations_map = {
    "V_FORMATION": offsets_v,
    "LINE_FORMATION": offsets_linha
}

offsets = offsets_v

# ================= CONVERSÃO ROTACIONADA 90° =================
ESCALA = 3

def converter_coordenadas(destino):
    x_plot, y_plot = destino

    # Rotação 90 graus
    x_air = y_plot * ESCALA
    y_air = x_plot * ESCALA

    return x_air, y_air

# ================= DECOLAGEM =================
for d in drones:
    client.enableApiControl(True, d)
    client.armDisarm(True, d)
    client.takeoffAsync(vehicle_name=d)

time.sleep(5)

state = client.getMultirotorState(vehicle_name='Drone1')
pos = state.kinematics_estimated.position

print("Posição inicial AirSim:", pos.x_val, pos.y_val)

# Fazer pairar (não se mover)
for d in drones:
    client.hoverAsync(vehicle_name=d)

print("Drones parados, aguardando destino...")

# ================= LOOP PRINCIPAL =================
while True:

    if not estado_recebido:
        time.sleep(0.1)
        continue

    try:
        formation_name = estado_recebido.get("formations", {}).get("alpha", "V_FORMATION")
        offsets = formations_map.get(formation_name, offsets_v)

        destino = estado_recebido.get("destinations", {}).get("alpha")

        # Não se move se não tem destino
        if destino is None:
            time.sleep(0.1)
            continue

        destino_x, destino_y = converter_coordenadas(destino)

        for d in drones:
            ox, oy, oz = offsets[d]

            target_x = destino_x + ox
            target_y = destino_y + oy
            target_z = -5 + oz

            state = client.getMultirotorState(vehicle_name=d)
            pos = state.kinematics_estimated.position


            dx = target_x - pos.x_val
            dy = target_y - pos.y_val
            dz = target_z - pos.z_val

            dist = np.linalg.norm([dx, dy, dz])

            if dist > 0.3:
                vel = min(6, dist)
                vx = dx / dist * vel
                vy = dy / dist * vel
                vz = dz / dist * vel
            else:
                vx, vy, vz = 0, 0, 0

            client.moveByVelocityAsync(
                vx, vy, vz,
                duration=0.1,
                vehicle_name=d
            )

    except Exception as e:
        print("Erro:", e)

    time.sleep(0.05)