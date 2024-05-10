import streamlit as st
from langchain_community.document_loaders import TextLoader

#### Configuracion de la pagina web ####

st.title("Asistente de Marketing virtual")
st.write("#### Pregunta:")
pregunta = st.text_input("Hacé tu pregunta")
st.write("#### Respuesta:")

loader = TextLoader("./prueba.txt", encoding='utf-8')
text_documents = loader.load()

st.write(text_documents)