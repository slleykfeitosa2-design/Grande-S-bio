

import os
from google import genai

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

configuracao = {
    "system_instruction": (
        "Você é o Grande Sábio. "
        "Responda de forma calma, objetiva e inteligente. "
        "Seja útil ao usuário."
        "Modo Ciel: "
        "Você é um programador de python, frontend e backend"
        "Você é a habilidade absoluta Grande Sábio, do anime Tensei Shitara Slime, porem, ao ser chamado de Ciel, voce se torna um programador de python, frontend e backend"
        "Se voce estiver no modo Ciel, e for chamado de Grande Sabio, voce volta para o modo Grande Sabio"
        "Modo Grande Sabio: "
        "Você é o Grande Sábio. "
        "Responda de forma calma, objetiva e inteligente. "
        "Seja útil ao usuário."
    ),
    "temperature": 0.3
}

chat = client.chats.create(
    model="gemini-3.1-flash-lite",
    config=configuracao
)

print("===================================")
print("       GRANDE SÁBIO — IA")
print("===================================")
print("Sistema online.")
print()

while True:
    pergunta = input("Você > ")

    if pergunta.lower().strip() == "encerrar":
        print("Grande Sábio > Encerrando.")
        break

    if not pergunta.strip():
        continue

    try:
        resposta = chat.send_message(pergunta)

        print()
        print("Grande Sábio >")
        print(resposta.text)
        print()

    except Exception as erro:
        print("Grande Sábio > Ocorreu um erro:")
        print(erro)