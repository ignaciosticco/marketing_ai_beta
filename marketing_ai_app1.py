# app: https://marketingaibeta-ov7eqxlsncowu2dymhz5gg.streamlit.app/

import streamlit as st
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_openai.chat_models import ChatOpenAI


#### Configuracion de la pagina web ####

st.title(":rainbow[Asistente de Marketing virtual]")

col1, col2 = st.columns([1, 7.1])  # Adjust the ratio as needed
with col1:
    st.write("Powered by")
with col2:
    st.image("logo_wavebi2.svg", width=100)

st.write('Este chatbot se presenta como un asistente virtual especializado en marketing. \
         Su función principal radica en la recopilación y análisis de datos provenientes de las campañas de \
         marketing en curso. Los usuarios pueden formularle preguntas específicas con el fin de obtener \
         conclusiones relevantes que contribuyan a comprender y optimizar el rendimiento de dichas campañas.')

st.write("#### Pregunta:")
pregunta = st.text_input("Hacé tu pregunta")
st.write("#### Respuesta:")

### Importacion de datos de campaña ###

with open('data_gender.txt', 'r', encoding='utf-8') as file:
    data_input_1 = file.read()

with open('data_age.txt', 'r', encoding='utf-8') as file:
    data_input_2 = file.read()

with open('data_region.txt', 'r', encoding='utf-8') as file:
    data_input_3 = file.read()


#### Configuracion de la cadena ####
model = ChatOpenAI(openai_api_key=st.secrets["OPENAI_API_KEY"], model="gpt-3.5-turbo")

parser = StrOutputParser()

template = """

Hora: 4:18

Sos un analista asistente de marketing digital, estás orientado a mejorar el desempeño de las campañas de anuncios publicados en facebook. Según las siguiente tabla de datos, vas a contestar preguntas y dar sugerencias para ajustar las campañas de marketing online.

A continuación, hay 3 tablas con las métricas de la campaña de marketing. Una tabla contiene la información de rendimiendo desglosado por sexo, otra por grupos etarios y la tercera por regiones geográficas.

Quiero que contestes las preguntas que te hacen basandote exclusivamente en las tablas de datos provistas en este prompt. No des respuestas generales. Sólo respuestas basadas en la tabla de datos. Si no sabés algo, decí que necesitás más información para contestar la pregunta. Quiero que tus respuestas sean lo más breves posible. 


Tabla de performance por sexo/género:

{context_1}

Tabla de performace de las camapñas por edad:

{context_2}

Tabla de performace de las camapñas por región geográfica:

{context_3}

Pregunta: {question}

"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model | parser

#### Correr el programa en el front ####

if pregunta:
    response = chain.invoke({
    "context_1": data_input_1,
    "context_2": data_input_2,
    "context_3": data_input_3,
    "question": pregunta
})
    st.write(response)