import streamlit as st
import requests

# Base URL do backend Flask
BASE_URL = "https://streamlit-aps3-enzo-perego.onrender.com/"

# Função para buscar um item pelo ID
def get_one_item(endpoint, item_id):
    url = f"{BASE_URL}/{endpoint}/{item_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Erro: {response.status_code} - {response.json().get('erro')}")
        return None

# Função para buscar todos os itens
def get_all_items(endpoint):
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Erro: {response.status_code} - {response.json().get('erro')}")
        return None

# Função para criar um novo item (POST)
def create_item(endpoint, data):
    url = f"{BASE_URL}/{endpoint}"
    response = requests.post(url, json=data)
    if response.status_code == 201:
        st.success("Item criado com sucesso!")
        return response.json()
    else:
        st.error(f"Erro: {response.status_code} - {response.json().get('erro')}")
        return None

# Função para deletar um item pelo ID
def delete_item(endpoint, item_id):
    url = f"{BASE_URL}/{endpoint}/{item_id}"
    response = requests.delete(url)
    if response.status_code == 200:
        st.success("Item deletado com sucesso!")
    else:
        st.error(f"Erro: {response.status_code} - {response.json().get('erro')}")

# Interface para gerenciar usuários
def manage_users():
    st.subheader("Gerenciar Usuários")

    # Buscar todos os empréstimos
    if st.button("Buscar Todos os Usuários"):
        loans = get_all_items("usuarios")
        if loans:
            st.json(loans)

    # Buscar um usuário pelo ID
    user_id = st.text_input("ID do Usuário para buscar:")
    if st.button("Buscar Usuário"):
        user = get_one_item("usuarios", user_id)
        if user:
            st.json(user)

    # Criar um novo usuário
    st.write("### Criar Novo Usuário")
    new_user_data = {
        "nome_usuario": st.text_input("Nome do usuário:"),
        "data_nascimento": st.text_input("Data de nascimento:"),
        "cpf": st.text_input("CPF:")
    }
    if st.button("Criar Usuário"):
        create_item("usuarios", new_user_data)

    # Deletar um usuário pelo ID
    delete_user_id = st.text_input("ID do Usuário para deletar:")
    if st.button("Deletar Usuário"):
        delete_item("usuarios", delete_user_id)

# Interface para gerenciar bicicletas
def manage_bikes():
    st.subheader("Gerenciar Bicicletas")

    # Buscar todos os empréstimos
    if st.button("Buscar Todos as Bicicletas"):
        loans = get_all_items("bikes")
        if loans:
            st.json(loans)

    # Buscar uma bicicleta pelo ID
    bike_id = st.text_input("ID da Bicicleta para buscar:")
    if st.button("Buscar Bicicleta"):
        bike = get_one_item("bikes", bike_id)
        if bike:
            st.json(bike)

    # Criar uma nova bicicleta
    st.write("### Criar Nova Bicicleta")
    new_bike_data = {
        "marca": st.text_input("Marca da bicicleta:"),
        "modelo": st.text_input("Modelo da bicicleta:"),
        "cidade": st.text_input("Cidade:")
    }
    if st.button("Criar Bicicleta"):
        create_item("bikes", new_bike_data)

    # Deletar uma bicicleta pelo ID
    delete_bike_id = st.text_input("ID da Bicicleta para deletar:")
    if st.button("Deletar Bicicleta"):
        delete_item("bikes", delete_bike_id)

# Interface para gerenciar empréstimos
def manage_loans():
    st.subheader("Gerenciar Empréstimos")

    # Buscar todos os empréstimos
    if st.button("Buscar Todos os Empréstimos"):
        loans = get_all_items("emprestimos")
        if loans:
            st.json(loans)

    # Criar um novo empréstimo
    st.write("### Criar Novo Empréstimo")
    usuario_id = st.text_input("ID do Usuário:")
    bike_id = st.text_input("ID da Bicicleta:")
    
    if st.button("Criar Empréstimo"):
        if usuario_id and bike_id:
            response = requests.post(f"{BASE_URL}/emprestimos/usuarios/{usuario_id}/bikes/{bike_id}")
            if response.status_code == 201:
                st.success(response.json().get("message"))
            else:
                st.error(f"Erro: {response.status_code} - {response.json().get('erro')}")
        else:
            st.error("Por favor, preencha os IDs do Usuário e da Bicicleta.")

    # Deletar um empréstimo pelo ID
    delete_loan_id = st.text_input("ID do Empréstimo para deletar:")
    if st.button("Deletar Empréstimo"):
        delete_item("emprestimos", delete_loan_id)

# Layout principal
st.title("Sistema de Gerenciamento de Bicicletas e Usuários")

# Navegação entre as seções
st.sidebar.title("Opções")
option = st.sidebar.selectbox("Escolha uma opção:", ["Usuários", "Bicicletas", "Empréstimos"])

if option == "Usuários":
    manage_users()
elif option == "Bicicletas":
    manage_bikes()
elif option == "Empréstimos":
    manage_loans()
