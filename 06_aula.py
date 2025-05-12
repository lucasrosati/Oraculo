import tempfile

import streamlit as st
from langchain.memory import ConversationBufferMemory

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from loaders import *


TIPOS_ARQUIVOS_VALIDOS = [
    'Site', 'Youtube', 'Pdf', 'Csv', 'Txt'
]

CONFIG_MODELOS = {'Groq': 
                        {'modelos': ['llama-3.1-70b-versatile', 'gemma2-9b-it', 'mixtral-8x7b-32768'],
                         'chat': ChatGroq},
                  'OpenAI': 
                        {'modelos': ['gpt-4o-mini', 'gpt-4o', 'o1-preview', 'o1-mini'],
                         'chat': ChatOpenAI}}

MEMORIA = ConversationBufferMemory()

def carrega_modelo(provedor, modelo, api_key, tipo_arquivo, arquivo):

    if tipo_arquivo == 'Site':
        documento = carrega_site(arquivo)
    if tipo_arquivo == 'Youtube':
        documento = carrega_youtube(arquivo)
    if tipo_arquivo == 'Pdf':
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp:
            temp.write(arquivo.read())
            nome_temp = temp.name
        documento = carrega_pdf(nome_temp)
    if tipo_arquivo == 'Csv':
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp:
            temp.write(arquivo.read())
            nome_temp = temp.name
        documento = carrega_csv(nome_temp)
    if tipo_arquivo == 'Txt':
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp:
            temp.write(arquivo.read())
            nome_temp = temp.name
        documento = carrega_txt(nome_temp)

    chat = CONFIG_MODELOS[provedor]['chat'](model=modelo, api_key=api_key)
    st.session_state['chat'] = chat

def pagina_chat():
    st.header('🤖Bem-vindo ao Oráculo', divider=True)

    chat_model = st.session_state.get('chat')
    memoria = st.session_state.get('memoria', MEMORIA)
    for mensagem in memoria.buffer_as_messages:
        chat = st.chat_message(mensagem.type)
        chat.markdown(mensagem.content)

    input_usuario = st.chat_input('Fale com o oráculo')
    if input_usuario:
        chat = st.chat_message('human')
        chat.markdown(input_usuario)

        chat = st.chat_message('ai')
        resposta = chat.write_stream(chat_model.stream(input_usuario))
        
        memoria.chat_memory.add_user_message(input_usuario)
        memoria.chat_memory.add_ai_message(resposta)
        st.session_state['memoria'] = memoria


def sidebar():
    tabs = st.tabs(['Upload de Arquivos', 'Seleção de Modelos'])
    with tabs[0]:
        tipo_arquivo = st.selectbox('Selecione o tipo de arquivo', TIPOS_ARQUIVOS_VALIDOS)
        if tipo_arquivo == 'Site':
            arquivo = st.text_input('Digite a url do site')
        if tipo_arquivo == 'Youtube':
            arquivo = st.text_input('Digite a url do vídeo')
        if tipo_arquivo == 'Pdf':
            arquivo = st.file_uploader('Faça o upload do arquivo pdf', type=['.pdf'])
        if tipo_arquivo == 'Csv':
            arquivo = st.file_uploader('Faça o upload do arquivo csv', type=['.csv'])
        if tipo_arquivo == 'Txt':
            arquivo = st.file_uploader('Faça o upload do arquivo txt', type=['.txt'])
    with tabs[1]:
        provedor = st.selectbox('Selecione o provedor dos modelo', CONFIG_MODELOS.keys())
        modelo = st.selectbox('Selecione o modelo', CONFIG_MODELOS[provedor]['modelos'])
        api_key = st.text_input(
            f'Adicione a api key para o provedor {provedor}',
            value=st.session_state.get(f'api_key_{provedor}'))

        st.session_state[f'api_key_{provedor}'] = api_key
    
    if st.button('Inicializar Oráculo', use_container_width=True):
        carrega_modelo(provedor, modelo, api_key, tipo_arquivo, arquivo)


def main():
    pagina_chat()
    with st.sidebar:
        sidebar()


if __name__ == '__main__':
    main()