# app: https://marketingaibeta-ov7eqxlsncowu2dymhz5gg.streamlit.app/

import streamlit as st
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_openai.chat_models import ChatOpenAI


#### Configuracion de la pagina web ####

st.title(":rainbow[Asistente de Marketing virtual]")

col1, col2 = st.columns([1, 6])  # Adjust the ratio as needed
with col1:
    st.write("Powered by")
with col2:
    st.image("logo_wavebi2.svg", width=100)

#st.write('Powered by')
#st.image('logo_wavebi2.svg', width=80)

st.write('Este chatbot se presenta como un asistente virtual especializado en marketing. \
         Su función principal radica en la recopilación y análisis de datos provenientes de las campañas de \
         marketing en curso. Los usuarios pueden formularle preguntas específicas con el fin de obtener \
         conclusiones relevantes que contribuyan a comprender y optimizar el rendimiento de dichas campañas.')

st.write("#### Pregunta:")
pregunta = st.text_input("Hacé tu pregunta")
st.write("#### Respuesta:")

loader = CSVLoader(file_path="./campañas_wavebi1.csv")
data_input = loader.load()

#### Configuracion de la cadena ####
model = ChatOpenAI(openai_api_key=st.secrets["OPENAI_API_KEY"], model="gpt-3.5-turbo")

parser = StrOutputParser()

template = """
Sos un asistente de marketing digital. Vas a recibir un contexto que es un archivo csv con datos de marketing
en forma tabular. 
Respondé las preguntas que te hacen basandote en el contexto. Si no podes responder una pregunta,
responde: "Necesito más información para responder esta pregunta.". 
"

Contexto: {context}

Pregunta: {question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model | parser


#### Correr el programa en el front ####

if pregunta:
    response = chain.invoke({
    "context": data_input,
    "question": pregunta
})
    st.write(response)

