import subprocess
import signal
import time

# Rodar o Base_de_dados primeiro
subprocess.run(["python", "Base_de_dados.py"])

# Iniciar recupera_dados e app como subprocessos
recupera_dados_process = subprocess.Popen(["python", "recupera_dados.py"])
app_process = subprocess.Popen(["python", "app.py"])

try:
    while True:
        time.sleep(1)  # Mantenha o script rodando, pode ser interrompido com Ctrl+C
except KeyboardInterrupt:
    # Encerra os subprocessos ao interromper o script principal
    recupera_dados_process.send_signal(signal.SIGINT)
    app_process.send_signal(signal.SIGINT)
    print("Processos encerrados.")