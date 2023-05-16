import sqlite3
import subprocess
from cadastro import visualizar_clientes
import planejamento_midias
from analise_post_instagram import analise_post_instagram
from pautas_semana import sugestoes_pautas_semana


def planejamento_midias_sociais_cliente(id_cliente, descricao):
    while True:
        print('1. Criar novo planejamento')
        print('2. Ver planejamento atual')
        print('3. Voltar')
        opcao = input('Escolha uma opção: ')

        if opcao == '1':
            planejamento_midias.planejamento_midias_sociais(id_cliente, descricao)
        elif opcao == '2':
            ver_planejamento_atual(id_cliente)
        elif opcao == '3':
            break
        else:
            print('Opção inválida. Tente novamente.')


def ver_ultima_analise(id_cliente):
    conn = sqlite3.connect('clientes.db')
    c = conn.cursor()
    c.execute('SELECT * FROM analise_instagram WHERE id_cliente = ? ORDER BY rowid DESC LIMIT 1', (id_cliente,))
    analise = c.fetchone()

    if analise:
        print(f'Última Análise: {analise[1]}')
    else:
        print('Nenhuma análise encontrada para este cliente.')

    conn.close()

def menu_analise_post_instagram(id_cliente):
    while True:
        print('1. Fazer análise dos posts')
        print('2. Ver última análise')
        print('3. Voltar')
        opcao = input('Escolha uma opção: ')

        if opcao == '1':
            analise_post_instagram(id_cliente)
        elif opcao == '2':
            ver_ultima_analise(id_cliente)
        elif opcao == '3':
            break
        else:
            print('Opção inválida. Tente novamente.')


def ver_planejamento_atual(id_cliente):
    conn = sqlite3.connect('clientes.db')
    c = conn.cursor()
    c.execute('SELECT * FROM respostas WHERE id_cliente = ?', (id_cliente,))
    respostas = c.fetchall()

    if respostas:
        for resposta in respostas:
            print(f'Pergunta: {resposta[1]}')
            print(f'Resposta: {resposta[2]}')
    else:
        print('Nenhum planejamento encontrado para este cliente.')

    conn.close()

def sugestoes_pautas_semana(id_cliente):
    print('Sugestões de Pautas para a semana')
    subprocess.run(['python', 'pautas_semana.py', str(id_cliente)])


def menu_cliente():
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
        return

    while True:
        print('1. Planejamento de Mídias Sociais')
        print('2. Análise de Post Instagram')
        print('3. Sugestões de Pautas para a semana')
        print('4. Voltar ao menu anterior')
        opcao = input('Escolha uma opção: ')

        if opcao == '1':
            planejamento_midias_sociais_cliente(cliente[0], cliente[3])
        elif opcao == '2':
            menu_analise_post_instagram(cliente[0])
        elif opcao == '3':
            sugestoes_pautas_semana(cliente[0])
        elif opcao == '4':
            break
        else:
            print('Opção inválida. Tente novamente.')

if __name__ == "__main__":
    menu_cliente()