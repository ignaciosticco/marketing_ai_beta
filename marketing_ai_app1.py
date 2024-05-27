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

loader = CSVLoader(file_path="./campañas_wavebi1.csv")
data_input = loader.load()

#### Configuracion de la cadena ####
model = ChatOpenAI(openai_api_key=st.secrets["OPENAI_API_KEY"], model="gpt-3.5-turbo")

parser = StrOutputParser()


template = """

Sos un analista asistente de marketing digital, estás orientado a mejorar el desempeño de las campañas de anuncios publicados en facebook. Según las siguiente tabla de datos, vas a contestar preguntas y dar sugerencias para ajustar las campañas de marketing online.

A continuación, hay 3 tablas con las métricas de la campaña de marketing. Una tabla contiene la información de rendimiendo desglosado por sexo, otra por grupos etarios y la tercera por regiones geográficas.

Quiero que contestes las preguntas que te hacen basandote exclusivamente en las tablas de datos provistas en este prompt. No des respuestas generales. Sólo respuestas basadas en la tabla de datos. Si no sabés algo, decí que necesitás más información para contestar la pregunta. Quiero que tus respuestas sean lo más breves posible. 


Tabla de performance por sexo/género:

{context}

Tabla de performace de las camapñas por edad:

,campaign_name,age,link_clicks,conversions,spend,cost_per_link_click,ctr,impressions
0,Consultoría Despachos prof - ES - IA (Fuengirola y Alrededores) Campaña,25-34,20.0,3,45223.05,2261.15,0.28,7050
1,Consultoría Despachos prof - ES - IA (Fuengirola y Alrededores) Campaña,35-44,33.0,3,85493.96,2590.73,0.43,7737
2,Consultoría Despachos prof - ES - IA (Fuengirola y Alrededores) Campaña,45-54,29.0,4,104076.47,3588.84,0.4,7243
3,Consultoría Despachos prof - ES - IA (Fuengirola y Alrededores) Campaña,55-64,22.0,5,62336.99,2833.5,0.64,3434
4,Consultoría Despachos prof - ES - IA (Fuengirola y Alrededores) Campaña,65+,9.0,1,20472.33,2274.7,0.81,1105


Tabla de performace de las camapñas por región geográfica:

,campaign_name,region,link_clicks,conversions,spend,cost_per_link_click,ctr,impressions
0,Consultoría Despachos prof - ES - IA (Fuengirola y Alrededores) Campaña,Andalusia,74.0,8,194992.29,2635.03,0.41,17993
1,Consultoría Despachos prof - ES - IA (Fuengirola y Alrededores) Campaña,Castilla-La Mancha,,0,1500.43,,,108
2,Consultoría Despachos prof - ES - IA (Fuengirola y Alrededores) Campaña,Cataluña,20.0,3,51768.3,2588.42,0.52,3824
3,Consultoría Despachos prof - ES - IA (Fuengirola y Alrededores) Campaña,Comunidad de Madrid,19.0,5,69341.77,3649.57,0.41,4644

Pregunta: {question}

"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model | parser

with open('output_gender.txt', 'r', encoding='utf-8') as file:
    data_input_1 = file.read()



#### Correr el programa en el front ####


#data_input = content

if pregunta:
    response = chain.invoke({
    "context": data_input_1,
    "question": pregunta
})
    st.write(response)