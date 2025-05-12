import os
from time import sleep
import streamlit as st
from fake_useragent import UserAgent
from langchain_community.document_loaders import (
    WebBaseLoader,
    YoutubeLoader,
    CSVLoader,
    PyPDFLoader,
    TextLoader
)

def carrega_site(url):
    documento = ''
    for i in range(5):
        try:
            os.environ['USER_AGENT'] = UserAgent().random
            loader = WebBaseLoader(url, raise_for_status=True)
            lista_documentos = loader.load()
            documento = '\n\n'.join([doc.page_content for doc in lista_documentos])
            break
        except Exception as e:
            print(f'Erro ao carregar o site {i+1}: {e}')
            sleep(3)
    if not documento:
        st.error('❌ Não foi possível carregar o site após múltiplas tentativas.')
        st.stop()
    return documento

def carrega_youtube(video_id):
    try:
        loader = YoutubeLoader(video_id=video_id, add_video_info=False, language=['pt'])
        documentos = loader.load()
        return '\n\n'.join([doc.page_content for doc in documentos])
    except Exception as e:
        st.error(f'❌ Erro ao carregar o vídeo do YouTube: {e}')
        st.stop()

def carrega_csv(caminho):
    try:
        loader = CSVLoader(file_path=caminho)
        documentos = loader.load()
        return '\n\n'.join([doc.page_content for doc in documentos])
    except Exception as e:
        st.error(f'❌ Erro ao carregar CSV: {e}')
        st.stop()

def carrega_pdf(caminho):
    try:
        loader = PyPDFLoader(file_path=caminho)
        documentos = loader.load()
        return '\n\n'.join([doc.page_content for doc in documentos])
    except Exception as e:
        st.error(f'❌ Erro ao carregar PDF: {e}')
        st.stop()

def carrega_txt(caminho):
    try:
        loader = TextLoader(file_path=caminho)
        documentos = loader.load()
        return '\n\n'.join([doc.page_content for doc in documentos])
    except Exception as e:
        st.error(f'❌ Erro ao carregar TXT: {e}')
        st.stop()
