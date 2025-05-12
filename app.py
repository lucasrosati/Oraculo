import tempfile
import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from loaders import *

TIPOS_ARQUIVOS_VALIDOS = ['Site', 'Youtube', 'Pdf', 'Csv', 'Txt']

CONFIG_MODELOS = {
    'Groq': {
        'modelos': ['llama3-70b-8192', 'mixtral-8x7b-32768', 'gemma-7b-it'],
        'chat': ChatGroq
    },
    'OpenAI': {
        'modelos': ['gpt-4o-mini', 'gpt-4o', 'o1-preview', 'o1-mini'],
        'chat': ChatOpenAI
    }
}

MEMORIA = ConversationBufferMemory()

def carrega_arquivos(tipo_arquivo, arquivo):
    if tipo_arquivo == 'Site':
        return carrega_site(arquivo)
    if tipo_arquivo == 'Youtube':
        return carrega_youtube(arquivo)
    if tipo_arquivo == 'Pdf':
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp:
            temp.write(arquivo.read())
            return carrega_pdf(temp.name)
    if tipo_arquivo == 'Csv':
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp:
            temp.write(arquivo.read())
            return carrega_csv(temp.name)
    if tipo_arquivo == 'Txt':
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp:
            temp.write(arquivo.read())
            return carrega_txt(temp.name)

def carrega_modelo(provedor, modelo, api_key, tipo_arquivo, arquivo):
    if arquivo:
        documento = carrega_arquivos(tipo_arquivo, arquivo)
        system_message = f'''Você é um assistente amigável chamado Oráculo.
Você possui acesso às seguintes informações vindas de um documento {tipo_arquivo}:

####
{documento}
####

Utilize as informações fornecidas para basear as suas respostas.
Sempre que houver $ na sua saída, substitua por S.
Se a informação do documento for algo como "Just a moment...Enable JavaScript and cookies to continue",
sugira ao usuário carregar novamente o Oráculo.'''
    else:
        system_message = '''Você é um assistente amigável chamado Oráculo.
Responda às perguntas do usuário de forma clara e objetiva, mesmo sem acesso a documentos.
Sempre que houver $ na sua saída, substitua por S.'''

    template = ChatPromptTemplate.from_messages([
        ('system', system_message),
        ('placeholder', '{chat_history}'),
        ('user', '{input}')
    ])

    chat = CONFIG_MODELOS[provedor]['chat'](model=modelo, api_key=api_key)
    chain = template | chat
    st.session_state['chain'] = chain

def pagina_chat():
    st.header('🤖 Bem-vindo ao Oráculo', divider=True)

    chain = st.session_state.get('chain')
    if not chain:
        st.error('Carregue o Oráculo na barra lateral.')
        st.stop()

    memoria = st.session_state.get('memoria', MEMORIA)
    for mensagem in memoria.buffer_as_messages:
        chat = st.chat_message(mensagem.type)
        chat.markdown(mensagem.content)

    input_usuario = st.chat_input('Fale com o Oráculo')
    if input_usuario:
        st.chat_message('human').markdown(input_usuario)
        resposta = st.chat_message('ai').write_stream(chain.stream({
            'input': input_usuario,
            'chat_history': memoria.buffer_as_messages
        }))
        memoria.chat_memory.add_user_message(input_usuario)
        memoria.chat_memory.add_ai_message(resposta)
        st.session_state['memoria'] = memoria

def sidebar():
    tabs = st.tabs(['Upload de Arquivos', 'Seleção de Modelos'])
    with tabs[0]:
        tipo_arquivo = st.selectbox('Selecione o tipo de arquivo', TIPOS_ARQUIVOS_VALIDOS)
        arquivo = None
        if tipo_arquivo == 'Site':
            arquivo = st.text_input('Digite a URL do site')
        elif tipo_arquivo == 'Youtube':
            arquivo = st.text_input('Digite a URL do vídeo')
        elif tipo_arquivo == 'Pdf':
            arquivo = st.file_uploader('Faça o upload do PDF', type=['pdf'])
        elif tipo_arquivo == 'Csv':
            arquivo = st.file_uploader('Faça o upload do CSV', type=['csv'])
        elif tipo_arquivo == 'Txt':
            arquivo = st.file_uploader('Faça o upload do TXT', type=['txt'])

    with tabs[1]:
        provedor = st.selectbox('Selecione o provedor dos modelos', list(CONFIG_MODELOS.keys()))
        modelo = st.selectbox('Selecione o modelo', CONFIG_MODELOS[provedor]['modelos'])
        api_key = st.text_input(
            f'Adicione a API key para o provedor {provedor}',
            value=st.session_state.get(f'api_key_{provedor}', '')
        )
        st.session_state[f'api_key_{provedor}'] = api_key

    if st.button('Inicializar Oráculo', use_container_width=True):
        carrega_modelo(provedor, modelo, api_key, tipo_arquivo, arquivo)

    if st.button('Apagar Histórico de Conversa', use_container_width=True):
        st.session_state['memoria'] = ConversationBufferMemory()

def main():
    with st.sidebar:
        sidebar()
    pagina_chat()

if __name__ == '__main__':
    main()
