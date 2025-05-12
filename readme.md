# 🔮 Oráculo

O **Oráculo** é um assistente de inteligência artificial multimodal, capaz de analisar conteúdo de diversas fontes (sites, PDFs, arquivos TXT, CSV e vídeos do YouTube) e responder de forma contextualizada e interativa através de uma interface criada com Streamlit.

![Screenshot](./docs/oraculo_screenshot.png)

## ✨ Funcionalidades

* ⭐ Chat com IA baseado em Groq ou OpenAI
* 📄 Upload de arquivos PDF, CSV, TXT para análise
* 🎬 Suporte a vídeos do YouTube (via transcrição)
* 🔗 Leitura e interpretação de páginas da web
* ⚙ Memória de conversa com rastreamento de histórico
* 🌍 Interface web local e responsiva (Streamlit)

## ⚡ Como usar

1. Clone este repositório
2. Crie e ative o ambiente virtual:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # ou .venv\Scripts\activate no Windows
   ```
3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```
4. Rode o app:

   ```bash
   streamlit run app.py
   ```
5. Acesse `http://localhost:8501` no navegador.

## 👁️ Exemplos de uso

* Pergunte qualquer coisa para o Oráculo sem documentos carregados
* Carregue uma URL ou PDF e extraia respostas contextualizadas
* Faça upload de um CSV e interaja com os dados

## 🏆 Modelos Suportados

* **Groq:** `llama3-70b-8192`, `mixtral-8x7b-32768`, `gemma-7b-it`
* **OpenAI:** `gpt-4o`, `gpt-4o-mini`, `o1-preview`, `o1-mini`

## 📘 Requisitos

* Python 3.10+
* API keys da Groq e/ou OpenAI

## 📕 Agradecimentos

Este projeto foi desenvolvido como parte de uma série de estudos da **Asimov Academy**, uma plataforma educacional que oferece cursos e trilhas práticas em IA, dados e automação.

Acesse: [asimov.academy](https://asimov.academy)

---

> "Nada há que não possa ser discutido ou perguntado. Estou aqui para ajudar!" — Oráculo
