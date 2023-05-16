import requests
import json
import sqlite3
from cadastro import visualizar_clientes
import time

def perguntar_gpt(conversa):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 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"
    }
    data = {
        "model": "gpt-4",
        "messages": conversa
    }

    backoff_time = 1  # Começamos com um tempo de espera de 1 segundo
    while True:
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()

            return response.json()['choices'][0]['message']['content']
        except requests.exceptions.HTTPError as e:
            if e.response.status_code in (429, 520):  # Limite de requisições atingido ou erro de servidor
                print(f"Erro {e.response.status_code} atingido. Aguardando antes de tentar novamente...")
                time.sleep(backoff_time)  # Aguarda antes de tentar novamente
                backoff_time *= 2  # Aumenta o tempo de espera
            else:
                raise

def criar_tabela_respostas():
    conn = sqlite3.connect('clientes.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS respostas (
            id_cliente INTEGER,
            pergunta TEXT,
            resposta TEXT,
            FOREIGN KEY(id_cliente) REFERENCES clientes(id)
        )
    ''')
    conn.close()

def planejamento_midias_sociais(id_cliente, descricao):
    perguntas = [
        f"Agora você é um especialista de redes sociais dessa empresa: {descricao}",
        "você consegue montar uma persona para esse negocio com a dores, objetivos e interesses?",
        "você consegue me passar um entendimento de como esse perfil se comportam nas redes sociais e como eles consomem conteudo?",
        "agora você consegue criar o publico alvo para as redes sociais desse negocio?",
        "Com essas informações você consegue definir quais são os objetivos desse negocio para as redes sociais?",
        "E quais redes sociais e as estrategias que vamos usar em cada uma para essa empresa?",
        "você consegue criar KPI de acompanhamento para essa rede para os proximos 3 meses para essas redes com os seus objetivos a serem alcançados ?"
    ]
    conn = sqlite3.connect('clientes.db')
    c = conn.cursor()

    conversa = [{"role": "system", "content": "You are a helpful assistant."}]

    for pergunta in perguntas:
        aprovado = False
        while not aprovado:
            conversa.append({"role": "user", "content": pergunta})
            resposta = perguntar_gpt(conversa)
            print('Resposta do GPT-4:', resposta)

            opcao = input('Você aprova a resposta? (s/n): ')
            if opcao.lower() == 's':
                c.execute('INSERT INTO respostas (id_cliente, pergunta, resposta) VALUES (?, ?, ?)', (id_cliente, pergunta, resposta))
                conn.commit()
                conversa.append({"role": "assistant", "content": resposta})
                aprovado = True
            else:
                feedback = input('Por favor, forneça seu feedback: ')
                conversa[-1] = {"role": "user", "content": feedback}
    print('Planejamento de mídia social concluído com sucesso!')


if __name__ == '__main__':
    criar_tabela_respostas()

    # Mostrar todos os clientes cadastrados.
    print('Clientes cadastrados:')
    visualizar_clientes()

    # Solicitar o ID do cliente.
    id_cliente = input('ID do Cliente que você deseja selecionar: ')

    # Abrir a conexão com o banco de dados.
    conn = sqlite3.connect('clientes.db')
    c = conn.cursor()

    # Selecionar o cliente.
    c.execute('SELECT * FROM clientes WHERE id = ?', (id_cliente,))
    cliente = c.fetchone()

    # Verificar se o cliente existe.
    if cliente is None:
        print('Cliente não encontrado.')
    else:
        descricao = cliente[3]  # A descrição está no campo 3
        planejamento_midias_sociais(id_cliente, descricao)

