from datetime import datetime
import tkinter as tk
import psutil
import getpass
import socket

def exibir_data_hora():
    agora = datetime.now()
    data_hora = agora.strftime("%d/%m/%Y %H:%M:%S")
    label_data_hora.config(text=f"Data e Hora: {data_hora}")
    root.after(1000, exibir_data_hora)  # Atualiza a cada segundo

def exibir_info_sistema():
    # Obter informações do sistema
    mem = psutil.virtual_memory()
    disco = psutil.disk_usage("/")
    cpu_percent = psutil.cpu_percent(interval=1)
    usuario = getpass.getuser()
    bateria = psutil.sensors_battery()
    wifi = bool(psutil.net_if_stats().get('Wi-Fi'))
    programas_memoria = get_top_programas_memoria(3)
    
    # Montar a string com as informações do sistema
    info = f"Usuário: {usuario}\n"
    info += f"CPU: {cpu_percent}%  Memória: {mem.percent}%  Disco: {disco.percent}%\n"
    info += f"Carregando: {bateria.power_plugged}\n"
    info += f"Wi-Fi: {'Conectado' if wifi else 'Desconectado'}\n"
    info += f"Top 3 Programas em Memória: {', '.join(programas_memoria)}"

    info_label.config(text=info)
    
    # Atualizar as informações a cada segundo
    root.after(10000, exibir_info_sistema)

def get_top_programas_memoria(n):
    processos = [(p.name(), p.memory_info().rss) for p in psutil.process_iter(['name', 'memory_info'])]
    processos_ordenados = sorted(processos, key=lambda x: x[1], reverse=True)
    programas_memoria = [p[0] for p in processos_ordenados[:n]]
    return programas_memoria

def toggle_dark_mode():
    global dark_mode_enabled
    dark_mode_enabled = not dark_mode_enabled
    update_colors()

def update_colors():
    if dark_mode_enabled:
        root.config(bg="#333333")
        label_data_hora.config(bg="#333333", fg="white")
        info_label.config(bg="#333333", fg="white")
    else:
        root.config(bg="white")
        label_data_hora.config(bg="white", fg="black")
        info_label.config(bg="white", fg="black")

root = tk.Tk()
root.title("Exibição de Informações do Sistema")

dark_mode_enabled = False

# Botão para alternar o modo escuro
dark_mode_button = tk.Button(root, text="Modo Escuro", command=toggle_dark_mode)
dark_mode_button.pack(padx=20, pady=10)

# Label para exibir a data e hora
label_data_hora = tk.Label(root, font=("Arial", 14))
label_data_hora.pack(padx=20, pady=10)

# Label para exibir as informações do sistema
info_label = tk.Label(root, font=("Arial", 12), justify=tk.LEFT)
info_label.pack(padx=20, pady=10)

# Chamada inicial das funções
exibir_data_hora()
exibir_info_sistema()
update_colors()

root.mainloop()
