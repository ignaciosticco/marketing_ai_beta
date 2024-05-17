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

Sos un analista asistente de marketing digital, estás orientado a mejorar el desempeño de las campañas de anuncios publicados en facebook. Según la siguiente tabla de datos, vas a contestar preguntas y dar sugerencias para ajustar la campaña de marketing.

Acá está la tabla de datos:

Edad	Interacción con la página	Clics en el enlace	Impresiones	Alcance	Resultados	Importe gastado (ARS)	CTR	Costo por clics (al enlace)
0	25-34	18.0	18.0	6214	3304	3.0	39105.12	0.29	2172.51
1	35-44	32.0	30.0	6892	3616	3.0	75667.51	0.44	2522.25
2	45-54	32.0	26.0	6302	3308	3.0	90596.09	0.41	3484.47
3	55-64	20.0	19.0	2986	1648	5.0	56200.96	0.64	2957.95
4	65+	7.0	6.0	938	533	1.0	17835.98	0.64	2972.66


Quiero que me contestes basandote exclusivamente en los datos provistos. No des respuestas generales. Sólo respuestas basadas en la tabla de datos. Si no sabés algo decí que necesitás más información para contestar la pregunta. 

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

