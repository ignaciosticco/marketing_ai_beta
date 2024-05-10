import streamlit as st
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

#### Configuracion de la pagina web ####

st.title("Asistente de Marketing virtual")
st.write("#### Pregunta:")
pregunta = st.text_input("Hacé tu pregunta")
st.write("#### Respuesta:")

loader = CSVLoader(file_path="./prueba2.csv")
data_input = """
Campaña,Impresiones, Clicks
holamundo,20,12
educaciondigitalquantica,20202,100
"""

#loader.load()


#### Configuracion de la cadena ####
model = ChatOpenAI(openai_api_key=st.secrets["OPENAI_API_KEY"], model="gpt-3.5-turbo")

parser = StrOutputParser()

template = """
Sos un asistente de marketing digital. Vas a recibir un contexto que es un archivo csv con datos de marketing
en forma tabular. 
Respondé las preguntas que te hacen basandote en el contexto. Si no podes responder una pregunta. 
Responde: "Necesito más información para responder esta pregunta.". 
"

Contexto: {context}

Pregunta: {question}
"""

prompt = ChatPromptTemplate.from_template(template)
setup = RunnableParallel(context=data_input, question=RunnablePassthrough())
chain = (
    setup   
    | prompt
    | model
    | parser
)

#### Correr el programa en el front ####

if pregunta:
    response = chain.invoke(pregunta)
    st.write(response)

