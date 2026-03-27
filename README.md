🚁 Drone Swarm Formation Control – AirSim
Sistema de controle de múltiplos drones em formação utilizando AirSim, Python e comunicação via Socket (TCP).

📌 Sobre o projeto
Este projeto implementa um sistema de enxame (swarm) de drones em ambiente de simulação AirSim.
Os drones conseguem decolar juntos, se mover até um destino e manter formações durante o voo, podendo trocar a formação em tempo real através de comandos enviados pela rede.

O sistema utiliza o conceito de Leader–Follower, onde um drone líder define o destino e os outros drones seguem mantendo offsets de formação.

🧠 Arquitetura do sistema
O sistema funciona da seguinte forma:

Cliente de Controle
        ↓
      Socket TCP
        ↓
Servidor Python (AirSim)
        ↓
Destino do grupo
        ↓
Offsets de formação
        ↓
Movimento dos drones
O cliente envia o destino e a formação

O servidor calcula as posições usando offsets

Cada drone se move para sua posição na formação

🖥️ Tecnologias utilizadas

Python

AirSim

Unreal Engine

Socket TCP/IP

JSON

Multithreading

📂 Estrutura do projeto
AirSimProject/
│
├── controle_formacao.py
├── settings.json
├── README.md
└── airsim/
⚙️ Instalação
Criar ambiente virtual
python -m venv venv
venv\Scripts\activate
Instalar dependências
pip install msgpack-rpc-python
pip install numpy
pip install opencv-python
pip install pillow
Ou:

pip install msgpack-rpc-python numpy opencv-python pillow
▶️ Como executar o projeto
1. Abrir o Unreal Engine
Abrir o mapa com AirSim

Clicar em Play

2. Rodar o servidor (AirSim)
python controle_formacao.py
3. Rodar o cliente (controle)
python cliente_controle.py
📡 Comunicação via Socket
O cliente envia mensagens em JSON para o servidor:

Exemplo:

{
  "destino": [10, 5],
  "formacao": "V_FORMATION"
}
Formações disponíveis:

V_FORMATION
LINE_FORMATION
🚀 Funcionalidades
Decolagem simultânea de múltiplos drones

Movimento em grupo

Formação em V

Formação em linha

Troca de formação durante o voo

Controle remoto via socket

Multithreading

Movimento contínuo e suave

⚙️ Parâmetros importantes
No código você pode ajustar:

velocity = 8
time.sleep(0.02)
altura = -5
Regra importante:

Quanto maior a velocidade, maior deve ser a distância entre os drones.
Tabela recomendada:

Velocidade	Distância entre drones
3	3
6	5
10	8
⚠️ Problemas comuns
Erro msgpackrpc
Instalar:

pip install msgpack-rpc-python
Drones não respondem
Verificar arquivo settings.json

Drones colidindo
Aumentar distância dos offsets

Diminuir velocidade

Movimento travando
Não usar:

.join()
em moveToPositionAsync

🧠 Conceitos utilizados
Swarm Robotics

Multi-Agent Systems

Formation Control

Leader-Follower Algorithm

Comunicação distribuída

Controle de múltiplos drones

🚀 Melhorias futuras
Evitar colisões automaticamente

Rotação da formação

Waypoints

Path planning

Múltiplos grupos de drones

Interface gráfica

Controle por joystick

Integração com ROS

Navegação autônoma

👨‍💻 Autores
Projeto desenvolvido por:
Luís Gustavo Sampaio Coêlho
Nicoly Paschoa
Daniel Dias
Gabriela

Luís Gustavo
(Adicionar outros membros aqui)
