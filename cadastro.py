import sqlite3

def criar_banco_de_dados():
    # Criar a conexão com o banco de dados.
    conn = sqlite3.connect('clientes.db')

    # Criar o cursor para executar comandos SQL.
    c = conn.cursor()

    # Criar a tabela de clientes.
    c.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY,
            nome TEXT,
            instagram TEXT,
            descricao TEXT,
            site TEXT,
            facebook TEXT,
            celular TEXT,
            email TEXT
        )
    ''')

    # Fechar a conexão com o banco de dados.
    conn.close()

def cadastrar_cliente():
    # Abrir a conexão com o banco de dados.
    conn = sqlite3.connect('clientes.db')
    c = conn.cursor()

    # Solicitar as informações do cliente.
    nome = input('Nome do Cliente: ')
    instagram = input('Instagram: ')
    descricao = input('Breve descrição: ')
    site = input('Site: ')
    facebook = input('Facebook: ')
    celular = input('Celular: ')
    email = input('Email: ')

    # Inserir o cliente no banco de dados.
    c.execute('''
        INSERT INTO clientes (nome, instagram, descricao, site, facebook, celular, email)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (nome, instagram, descricao, site, facebook, celular, email))

    # Salvar as alterações e fechar a conexão.
    conn.commit()
    conn.close()

def visualizar_clientes():
    # Abrir a conexão com o banco de dados.
    conn = sqlite3.connect('clientes.db')
    c = conn.cursor()

    # Selecionar todos os clientes.
    c.execute('SELECT * FROM clientes')

    # Imprimir os clientes.
    for cliente in c.fetchall():
        print(cliente)

    # Fechar a conexão.
    conn.close()

def atualizar_cliente():
    # Abrir a conexão com o banco de dados.
    conn = sqlite3.connect('clientes.db')
    c = conn.cursor()

    # Mostrar todos os clientes cadastrados.
    print('Clientes cadastrados:')
    visualizar_clientes()

    # Solicitar o ID do cliente.
    id_cliente = input('ID do Cliente que você deseja atualizar: ')

    # Selecionar o cliente.
    c.execute('SELECT * FROM clientes WHERE id = ?', (id_cliente,))
    cliente = c.fetchone()

    # Verificar se o cliente existe.
    if cliente is None:
        print('Cliente não encontrado.')
        return

    # Mostrar as informações atuais do cliente.
    print('Informações atuais do cliente:')
    print(cliente)

    # Solicitar as novas informações do cliente.
    nome = input('Nome do Cliente: ')
    instagram = input('Instagram: ')
    descricao = input('Breve descrição: ')
    site = input('Site: ')
    facebook = input('Facebook: ')
    celular = input('Celular: ')
    email = input('Email: ')

    # Atualizar o cliente no banco de dados.
    c.execute('''
        UPDATE clientes
        SET nome = ?, instagram = ?, descricao = ?, site = ?, facebook = ?, celular = ?, email = ?
        WHERE id = ?
    ''', (nome, instagram, descricao, site, facebook, celular, email, id_cliente))

    # Salvar as alterações e fechar a conexão.
    conn.commit()
    conn.close()

def menu():
    while True:
        print('1. Cadastrar novo cliente')
        print('2. Visualizar clientes cadastrados')
        print('3. Atualizar um cliente')
        print('4. Sair')
        opcao = input('Escolha uma opção: ')

        if opcao == '1':
            cadastrar_cliente()
        elif opcao == '2':
            visualizar_clientes()
        elif opcao == '3':
            atualizar_cliente()
        elif opcao == '4':
            break
        else:
            print('Opção inválida. Tente novamente.')

    # Criar o banco de dados e executar o menu.
    criar_banco_de_dados()
    menu()


if __name__ == '__main__':
    # Criar o banco de dados e executar o menu.
    criar_banco_de_dados()
    menu()
