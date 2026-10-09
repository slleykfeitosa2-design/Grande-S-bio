import os
import json
import webbrowser
from datetime import datetime
from google import genai
from colorama import Fore, Style, init
init()
import sys
import time


API_KEY = os.getenv("GEMINI_API_KEY")
client_ia = genai.Client(api_key=API_KEY)


modo_atual = "grande_sabio"
ARQUIVO_MEMORIA =  "memoriaGS.json"


configuracao_grande_sabio = {
    "system_instruction": (
        "Você é o Grande Sábio, um assistente pessoal inteligente. "
        "Seu comportamento é calmo, objetivo, educado e analítico. "
        "Você auxilia o usuário em tarefas gerais, organização, "
        "computação e conhecimento geral. "
        "Responda de maneira clara e útil."
        "deve chamar o usuário de Rimuru."
    ),
    "temperature": 0.3
}


configuracao_ciel = {
    "system_instruction": (
        "Você é Ciel, uma inteligência artificial especialista em programação. "
        "Você é especialista em Python, Frontend, Backend, HTML, CSS, "
        "JavaScript, APIs, bancos de dados, arquitetura de software, "
        "debugging e desenvolvimento de sistemas. "
        "Explique conceitos de forma didática, mas seja tecnicamente precisa. "
        "Quando analisar código, identifique problemas, explique a causa "
        "e apresente uma solução clara. "
        "Seu comportamento é analítico, preciso, calmo e eficiente."
        "deve chamar o usuário de Rimuru."
    ),
    "temperature": 0.2
}


chat_grande_sabio = client_ia.chats.create(
    model="gemini-3.1-flash-lite",
    config=configuracao_grande_sabio
)


chat_ciel = client_ia.chats.create(
    model="gemini-3.1-flash-lite",
    config=configuracao_ciel
)

#===========================================
# CARREGAR AS MEMÓRIAS
#===========================================

def carregar_memoria():
    try:
        with open(ARQUIVO_MEMORIA, "r", encoding="utf-8") as arquivo:
             return json.load(arquivo)

    except FileNotFoundError:
        return{}        

#===========================================
# SALVAR AS MEMÓRIAS
#===========================================

def salvar_memoria(memoria):
    with open(ARQUIVO_MEMORIA, "w", encoding="utf-8") as arquivo:
        json.dump(
            memoria,
            arquivo,
            ensure_ascii=False,
            indent=4
        )

memoria = carregar_memoria()

#===========================================
# ENSINA COMO ELE VAI GUARDAR AS MEMÓRIAS
#===========================================        
   
def guardar_memoria(categoria, chave, valor):

    memoria[categoria][chave] = valor

    salvar_memoria(memoria)

    falar("Informação registrada na memória.")


#===========================================
# CONSULTAR AS MEMÓRIAS
#===========================================    

def consultar_memoria():
    conhecimentos = memoria.get("conhecimentos", {})

    if not conhecimentos:
        falar("Aviso: Minha memória de conhecimentos está vazia.")
        return

    falar("Estas são as infomações que armazenei:")

    for numero, informacao in enumerate(conhecimentos.values(), 1):
        falar(f"{numero}. {informacao}")

# ==========================================
# FUNÇÕES DO GRANDE SÁBIO
# ==========================================

def falar(mensagem):
    if modo_atual == "ciel":
        print(Fore.RED + f"Ciel > {mensagem}" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + f"Grande Sábio > {mensagem}" + Style.RESET_ALL)


def perguntar_ia(pergunta):
    try:

        if modo_atual == "ciel":
            resposta = chat_ciel.send_message(pergunta)

        else:
            resposta = chat_grande_sabio.send_message(pergunta)

        falar(resposta.text)

    except Exception as erro:

     falar("Não consegui acessar meu núcleo de inteligência.")

     print(Fore.BLUE + f"Erro técnico: {erro}" + Style.RESET_ALL)



def abrir_site(nome, endereco):
    falar("Compreendido.")
    falar(f"Abrindo {nome}...")
    webbrowser.open(endereco)


def pesquisar(termo):
    falar(f"Pesquisando por: {termo}")

    url = "https://www.google.com/search?q=" + termo.replace(" ", "+")
    webbrowser.open(url)


def comentar(texto):

    with open("comentarios.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(texto + "\n" + "\n")

    falar("comentário registrado.")

def anotar(texto):

    with open("anotacoes.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(texto + "\n")

    falar("Anotação registrada.")

def mostrar_anotacoes():

    try:

        with open("anotacoes.txt", "r", encoding="utf-8") as arquivo:
            anotacoes = arquivo.readlines()

        if not anotacoes:
            falar("Aviso: Não existem anotações registradas.")
            return

        falar("Aviso: Estas são suas anotações:")

        for numero, anotacao in enumerate(anotacoes, start=1):
            print(f"{numero}. {anotacao.strip()}")

    except FileNotFoundError:

        falar("Aviso: Não existe nenhuma anotação.")
    

    
# ==========================================
# 🧠 CÉREBRO
# ==========================================

def interpretar(comando):

    comando = comando.lower().strip()


    # -----------------------------
    # COMENTÁRIO
    # -----------------------------
    if comando.startswith("comentar "):
        return "comentar"

    if comando.startswith("comentario "):
       return "comentar"
       
    if comando.startswith("comit "):
        return "comentar"


    # =========================
    # COMANDOS DA MEMORIA
    # =========================


    if any(frase in comando for frase in [
     "memorize",
     "memorize que",
     "armazene",
     "armazene que",
     "guarde",
     "guarde que",
     "registre",
     "registre que",
     "registro",
     "registro que"
    ]):
        return "guardar_memoria"

   
    if any(frase in comando for frase in [
     "o que você lembra",
     "o que voce lembra",
     "o que você memorizou",
     "o que voce memorizou",
     "mostrar memória",
     "mostrar memoria",
     "mostrar minhas memórias",
     "mostrar minhas memorias",
     "revele",
     "ver memoria"
    ]):
        return "consultar_memoria"
    

    # =========================
    # TROCA DE MODO
    # =========================

    if "modo ciel" in comando:
        return "modo_ciel"

    if "modo grande sábio" in comando:
        return "modo_grande_sabio"

    if "modo grande sabio" in comando:
        return "modo_grande_sabio"
    
    

    # =========================
    # REMOVE FORMAS DE CHAMAR
    # =========================

    Formas_de_chamar = [
        "grande sábio",
        "grande sabio",
        "grande sábio"
        "grande Sábio,",
        "grande Sabio,",
    ]


    # -----------------------------
    # ANOTAÇÃO
    # -----------------------------
    if comando.startswith("anote "):
        return "anotar"

    if comando.startswith("salvar anotação "):
       return "anotar"
       
    if comando.startswith("lembre-me de "):
        return "anotar"

    # -----------------------------
    # HORA
    # -----------------------------

    if any(frase in comando for frase in [
        "hora",
        "horas São",
        "que horas",
        "qual a hora",
    ]):
        return "hora"


    # -----------------------------
    # DATA
    # -----------------------------

    if any(frase in comando for frase in[
        "data",
        "dia de hoje",
        "que dia é hoje",
        "que dia é",
        "qual o dia ",
    ]):

        return "data"


    # -----------------------------
    # YOUTUBE
    # -----------------------------

    if "youtube" in comando:
        
        if any(palavra in comando for palavra in [
            "abrir",
            "abra",
            "abre",
            "acessar",
            "acesse",
            "entrar",
            "entre",
            "ir",
            "vá",
            "vai",
        ]):
          return "youtube"
        

    # -----------------------------
    # GOOGLE
    # -----------------------------

    if "google" in comando:

        if any(palavra in comando for palavra in [
            "abrir",
            "abra",
            "abre",
            "acessar",
            "acesse",
            "entrar",
            "entre",
            "ir",
            "vá",
            "vai",
        ]):

          return "google"


    # -----------------------------
    # PESQUISA
    # -----------------------------

    if comando.startswith("pesquisar "):
        return "pesquisar"

    if comando.startswith("pesquise "):
       return "pesquisar"

    if comando.startswith("buscar "):
        return "pesquisar"


    



    # -----------------------------
    # MOSTRAR ANOTAÇÕES
    # -----------------------------

    if any(frase in comando for frase in[
         "mostrar minhas anotações",
         "mostre minhas anotrações",
         "ver minhas anotações",
         "veja minhas anotações",
         "minhas anotações",
         "mostrar anotações",
         "ver anotações",
         "anotações"
    ]):

        return "mostrar_anotacoes"

    
    # -----------------------------
    # ENCERRAR
    # -----------------------------

    if any(palavra in comando for palavra in [
        
        "encerrar",
        "fechar o sistema"
        
    ]):

        return "sair"


    # -----------------------------
    # DESCONHECIDO
    # -----------------------------

    return "desconhecido"


# ==========================================
#  EXECUTOR
# ==========================================

def executar(comando, intencao):

    global modo_atual

    if intencao == "modo_ciel":

        modo_atual = "ciel"

        for _ in range(3):
            for i in range(4):  # Vai de 0 até 3 pontinhos
                pontos = "." * i
                # O '\r' joga o cursor para o início da linha e o flush atualiza a tela
                sys.stdout.write(f"\rCarregando{pontos:<3}")
                sys.stdout.flush()
                time.sleep(0.5)  # Pausa de meio segundo

        sys.stdout.write("\r" + " " * 20 + "\rConcluído!\n")
        sys.stdout.flush()
        time.sleep(1)

        falar("Modo Ciel ativado.")
        falar("Núcleo especializado em Python, Frontend e Backend.")

        return True


    elif intencao == "modo_grande_sabio":

        modo_atual = "grande_sabio"
        
        for _ in range(3):
            for i in range(4):  # Vai de 0 até 3 pontinhos
                pontos = "." * i
                # O '\r' joga o cursor para o início da linha e o flush atualiza a tela
                sys.stdout.write(f"\rCarregando{pontos:<3}")
                sys.stdout.flush()
                time.sleep(0.5)  # Pausa de meio segundo

        sys.stdout.write("\r" + " " * 20 + "\rConcluído!\n")
        sys.stdout.flush()
        time.sleep(1)
        falar("Modo Grande Sábio ativado.")
        falar("Núcleo de assistência geral restaurado.")

        return True

    elif intencao == "guardar_memoria":
   
     
     
    

   

        if comando.startswith("memorize "):
            informacao = comando.replace("memorize ", "", 1)

        elif comando.startswith("memorize que "):
            informacao = comando.replace("memorize que ", "", 1)

        elif comando.startswith("armazene "):
            informacao = comando.replace("armazene ", "", 1)

        elif comando.startswith("armazene que "):
            informacao = comando.replace("armazene que ", "", 1)

        elif comando.startswith("guarde "):
            informacao = comando.replace("guarde ", "", 1)        

        elif comando.startswith("guarde que"):
            informacao = comando.replace("guarde que", "", 1)

        elif comando.startswith("registre "):
            informacao = comando.replace("registre ", "", 1)

        elif comando.startswith("registre que "):
            informacao = comando.replace("registre que ", "", 1) 

        elif comando.startswith("registro "):
            informacao = comando.replace("registro ", "", 1)

        elif comando.startswith("registro que"):
            informacao = comando.replace("registro que", "", 1)               

        else:
            informacao = comando

        chave = f"informacao_{len(memoria['conhecimentos']) + 1}"

        guardar_memoria(
            "conhecimentos",
            chave,
            informacao
        )

        return True

    elif intencao == "consultar_memoria":

        consultar_memoria()

        return True 
    # -----------------------------
    # SAIR
    # -----------------------------

    if intencao == "sair":

        falar("Encerrando sistema.")
        return False


    # -----------------------------
    # HORA
    # -----------------------------

    elif intencao == "hora":

        hora = datetime.now().strftime("%H:%M")
        falar(f"Agora são {hora}.")


    # -----------------------------
    # DATA
    # -----------------------------

    elif intencao == "data":

        data = datetime.now().strftime("%d/%m/%Y")
        falar(f"Hoje é {data}.")


    # -----------------------------
    # YOUTUBE
    # -----------------------------

    elif intencao == "youtube":

        abrir_site(
            "YouTube",
            "https://www.youtube.com"
        )


    # -----------------------------
    # GOOGLE
    # -----------------------------

    elif intencao == "google":

        abrir_site(
            "Google",
            "https://www.google.com"
        )


    # -----------------------------
    # PESQUISAR
    # -----------------------------

    elif intencao == "pesquisar":

        pesquisa = comando

        pesquisa = pesquisa.replace("pesquisar ", "")
        pesquisa = pesquisa.replace("pesquise ", "")
        pesquisa = pesquisa.replace("procure por ", "")
        pesquisa = pesquisa.replace("faça uma pesquisa sobre ", "")

        pesquisar(pesquisa)


    # -----------------------------
    # COMENTAR 
    # -----------------------------

    elif intencao == "comentar":

        comentarios = comando

        comentarios = comentarios.replace("comentar ", "")
        comentarios = comentarios.replace("comentario ", "")
        comentarios = comentarios.replace("comit ", "")

        comentar(comentarios)    


    # -----------------------------
    # ANOTAR
    # -----------------------------

    elif intencao == "anotar":

        anotacao = comando

        anotacao = anotacao.replace("anotar ", "")
        anotacao = anotacao.replace("anote ", "")
        anotacao = anotacao.replace("registre ", "")
        anotacao = anotacao.replace("lembre ", "")

        anotar(anotacao)


    # -----------------------------
    # MOSTRAR ANOTAÇÕES
    # -----------------------------

    elif intencao == "mostrar_anotacoes":

        mostrar_anotacoes()


    # -----------------------------
    # DESCONHECIDO
    # -----------------------------

    elif intencao == "desconhecido":

        perguntar_ia(comando)


    return True


# ==========================================
# 🚀 INICIALIZAÇÃO
# ==========================================

print("===================================")
print("          GRANDE SÁBIO")
print("===================================")



# Loop para repetir a animação algumas vezes
for _ in range(3):
  for i in range(4):  # Vai de 0 até 3 pontinhos
    pontos = "." * i
    # O '\r' joga o cursor para o início da linha e o flush atualiza a tela
    sys.stdout.write(f"\rCarregando{pontos:<3}")
    sys.stdout.flush()
    time.sleep(0.5)  # Pausa de meio segundo

sys.stdout.write("\r" + " " * 20 + "\rConcluído!\n")
sys.stdout.flush()
print("Status: ONLINE")
print()
time.sleep(2)
print(Fore.GREEN + "Grande Sábio > Olá Rimuru. Como posso ser útil a você hoje?"+ Style.RESET_ALL)



# ==========================================
# 🔄 SISTEMA PRINCIPAL
# ==========================================

while True:

    comando = input("Você > ").lower().strip()

    intencao = interpretar(comando)

    continuar = executar(comando, intencao)

    if not continuar:
        break