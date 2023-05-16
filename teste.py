import pandas as pd
import requests
import json
from datetime import datetime, timedelta
import dateparser
def perguntar_gpt(mensagens):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer APY_KEY_CHATGPT"  # substitua "SEU_TOKEN_AQUI" pela sua chave de API
    }
    data = {
        "model": "gpt-4",  # nome do modelo, ajuste conforme necessário
        "messages": mensagens
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']


def analisar_base():
    df = pd.read_excel('base_redes_sociais.xlsx')

    # Converter a coluna 'Date' para o tipo datetime
    df['Date'] = df['Date'].apply(dateparser.parse)

    # Data atual
    now = datetime.now()

    # Data 15 dias atrás
    fifteen_days_ago = now - timedelta(days=15)

    # Filtrar os posts dos últimos 15 dias
    df = df[df['Date'] >= fifteen_days_ago]

    # Transformar todas as linhas em uma lista de dicionários
    todos_posts_dict = df.to_dict('records')

    # Formatar a string com os dados dos melhores posts
    todos_posts_str = ""
    for i, post in enumerate(todos_posts_dict, start=1):
        todos_posts_str += f"\nPost {i}:\n"
        todos_posts_str += f"Nome do Post: {post['Post Name']}\n"
        todos_posts_str += f"Data: {post['Date']}\n"
        todos_posts_str += f"Audiência: {post['Media reach']}\n"
        todos_posts_str += f"Número de likes: {post['Like count']}\n"
        todos_posts_str += f"Número de comentários: {post['Comments count']}\n"
        todos_posts_str += f"Engajamento: {post['Engajamento']}\n"
        todos_posts_str += f"Número de reproduções (reels): {post['Reel plays']}\n"

    pergunta = [
        {
            "role": "system",
            "content": "Você está conversando com um assistente de IA. Como posso ajudá-lo?"
        },
        {
            "role": "user",
            "content": f"Aqui estão todos os posts dos últimos 15 dias:{todos_posts_str}\nPreciso que você analise de acordo com o engajamento e Audiencia esses posts e me diga: 1 - os 3 posts com melhores resultados, a data e porquê 2 - os 3 posts com piores resultados, a data e porquê. 4 - insights do mês (o que temos que melhorar, o que fizemos bem)"
        }
    ]
    print(perguntar_gpt(pergunta))


if __name__ == "__main__":
    analisar_base()