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
    st.image("logo_wavebi2.svg", width=80)

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

Sexo	Clics en el enlace	Resultados	Importe gastado (ARS)	Costo por clics (al enlace)	CTR	Impresiones
0	female	18.0	2.0	62766.73	3487.04	0.36	4993
1	male	81.0	13.0	213272.51	2632.99	0.45	18084


Tabla de performace de las camapñas por edad:

	Edad	Clics en el enlace	Resultados	Importe gastado (ARS)	Costo por clics (al enlace)	CTR	Impresiones
0	25-34	18.0	3.0	39105.12	2172.51	0.29	6214
1	35-44	30.0	3.0	75667.51	2522.25	0.44	6892
2	45-54	26.0	3.0	90596.09	3484.47	0.41	6302
3	55-64	19.0	5.0	56200.96	2957.95	0.64	2986
4	65+	6.0	1.0	17835.98	2972.66	0.64	938


Tabla de performace de las camapñas por región geográfica:

Región	Clics en el enlace	Resultados	Importe gastado (ARS)	Costo por clics (al enlace)	CTR	Impresiones
0	Andalusia	60.0	7.0	156784.18	2613.07	0.41	14755
1	Castilla-La Mancha	0.0	0.0	1500.50	NaN	0.00	108
2	Cataluña	20.0	3.0	51770.62	2588.53	0.52	3824
3	Comunidad de Madrid	19.0	5.0	69344.65	3649.72	0.41	4644 

Pregunta: {question}

"""



prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model | parser


#### Correr el programa en el front ####

if pregunta:
    response = chain.invoke({
    #"context": data_input,
    "question": pregunta
})
    st.write(response)

