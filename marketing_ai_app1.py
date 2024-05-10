import streamlit as st
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_openai.chat_models import ChatOpenAI

#### Configuracion de la pagina web ####

st.title("Asistente de Marketing virtual")
st.write("#### Pregunta:")
pregunta = st.text_input("Hacé tu pregunta")
st.write("#### Respuesta:")

loader = CSVLoader(file_path="./prueba2.csv")
data = loader.load()


st.write(data)