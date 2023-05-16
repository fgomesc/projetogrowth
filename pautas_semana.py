import sqlite3
import pandas as pd
import requests
import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor

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

def sugestoes_pautas_semana(id_cliente):
    conn = sqlite3.connect('clientes.db')
    c = conn.cursor()

    # Selecionar os dados das tabelas
    c.execute('SELECT * FROM respostas WHERE id_cliente = ?', (id_cliente,))
    respostas = pd.DataFrame(c.fetchall(), columns=['id_cliente', 'pergunta', 'resposta'])
    c.execute('SELECT * FROM posts_instagram WHERE id_cliente = ?', (id_cliente,))
    posts_instagram = pd.DataFrame(c.fetchall(), columns=['id_cliente', 'post'])
    c.execute('SELECT * FROM analise_instagram WHERE id_cliente = ?', (id_cliente,))
    analise_instagram = pd.DataFrame(c.fetchall(), columns=['id_cliente', 'analise'])

    # Unir os dataframes
    data = pd.concat([respostas, posts_instagram, analise_instagram], axis=1)

    # Limpar o dataframe
    data = data.dropna()

    # Preparar os dados para a rede neural
    X = data.drop('analise', axis=1)
    y = data['analise']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    scaler.fit(X_train)

    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    # Criar a rede neural
    mlp = MLPRegressor(hidden_layer_sizes=(10, 10, 10), max_iter=1000)
    mlp.fit(X_train, y_train)

    # Prever a análise da próxima semana
    previsao = mlp.predict(X_test)

    # Passar a previsão para o GPT-4
    mensagens = [
        {"role": "system", "content": "Você é um assistente de planejamento de pautas."},
        {"role": "user", "content": f"Quais são as sugestões de pautas para a próxima semana? A previsão é: {previsao}"}]

    resposta_gpt = perguntar_gpt(mensagens)
    return resposta_gpt
