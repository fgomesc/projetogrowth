import tkinter as tk
from tkinter import filedialog
import sqlite3
import pandas as pd
import requests
import json
from datetime import datetime, timedelta
import dateparser

def perguntar_gpt(mensagens):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer APY_KEY_CHATGPT"
    }
    data = {
        "model": "gpt-4",
        "messages": mensagens
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']

def analise_post_instagram(id_cliente):
    print('Análise de Post Instagram')

    conn = sqlite3.connect('clientes.db')
    c = conn.cursor()

    c.execute('SELECT * FROM clientes WHERE id = ?', (id_cliente,))
    cliente = c.fetchone()

    if cliente is None:
        print('Cliente não encontrado.')
        return

    print('Cliente:')
    print(f"ID: {cliente[0]}, Nome: {cliente[1]}")

    root = tk.Tk()
    root.withdraw()
    caminho_arquivo_excel = filedialog.askopenfilename()

    print(f"Caminho do arquivo selecionado: {caminho_arquivo_excel}")

    df = pd.read_excel(caminho_arquivo_excel)

    print(f"Colunas no DataFrame: {df.columns}")

    df['Engajamento'] = df['LikeCount'] + df['CommentsCount']
    df['id_cliente'] = id_cliente

    c.execute('''
        CREATE TABLE IF NOT EXISTS posts_instagram (
            id_cliente INTEGER,
            PostName TEXT,
            Date TEXT,
            MediaReach INTEGER,
            LikeCount INTEGER,
            CommentsCount INTEGER,
            Engajamento REAL,
            ReelPlays INTEGER,
            FOREIGN KEY(id_cliente) REFERENCES clientes(id)
        )
    ''')

    df.to_sql('posts_instagram', conn, if_exists='append', index=False)

    analisar_base(caminho_arquivo_excel, id_cliente, conn)
    conn.close()



def analisar_base(caminho_arquivo_excel, id_cliente, conn):
    df = pd.read_excel(caminho_arquivo_excel)

    df.columns = ['PostName', 'Date', 'MediaReach', 'LikeCount', 'CommentsCount', 'Engajamento', 'ReelPlays']
    df['Date'] = df['Date'].apply(dateparser.parse)

    df = df.sort_values(by='Date', ascending=False)
    df = df.head(15)

    todos_posts_dict = df.to_dict('records')

    todos_posts_str = ""
    for i, post in enumerate(todos_posts_dict, start=1):
        todos_posts_str += f"\nPost {i}:\n"
        todos_posts_str += f"Nome do Post: {post['PostName']}\n"
        todos_posts_str += f"Data: {post['Date']}\n"
        todos_posts_str += f"Audiência: {post['MediaReach']}\n"
        todos_posts_str += f"Número de likes: {post['LikeCount']}\n"
        todos_posts_str += f"Número de comentários: {post['CommentsCount']}\n"
        todos_posts_str += f"Engajamento: {post['Engajamento']}\n"
        todos_posts_str += f"Número de reproduções (reels): {post['ReelPlays']}\n"

    pergunta = [{"role": "system", "content": "Você está conversando com um assistente de IA. Como posso ajudá-lo?"},
                {"role": "user",
                 "content": f"Aqui estão todos os posts dos últimos 15 dias:{todos_posts_str}\nPreciso que você analise de acordo com o engajamento e Audiencia esses posts e me diga: 1 - os 3 posts com melhores resultados, a data e porquê 2 - os 3 posts com piores resultados, a data e porquê. 4 - insights do mês (o que temos que melhorar, o que fizemos bem)"}]

    resposta_gpt = perguntar_gpt(pergunta)

    print(resposta_gpt)

    confirmacao = input("Deseja salvar essa análise? (s/n): ")

    if confirmacao.lower() == 's':
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS analise_instagram (
                id_cliente INTEGER,
                analise TEXT,
                FOREIGN KEY(id_cliente) REFERENCES clientes(id)
            )
        ''')
        c.execute('INSERT INTO analise_instagram (id_cliente, analise) VALUES (?, ?)', (id_cliente, resposta_gpt))
        conn.commit()
