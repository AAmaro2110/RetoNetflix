import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account
#import firebase_admin
#from firebase_admin import credentials, firestore

import json
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="retonetflix-5717f")
#path = '/content/'

#cred = credentials.Certificate(path + "retonetflix.json")
#firebase_admin.initialize_app(cred)
#db = firestore.client()

dbMovies = db.collection("movies")
st.header("Netflix app")
@st.cache_data
def cargarDatos():
  movies_ref = list(db.collection(u'movies').stream())
  movies_dict = list(map(lambda x: x.to_dict(), movies_ref))
  movies_dataframe = pd.DataFrame(movies_dict)
  return movies_dataframe

data = cargarDatos()

agree = st.sidebar.checkbox("Mostrar todos los filmes")
if agree:
  st.dataframe(data)

def loadbyName(movie):
  filtered_data_byname = data[data['name'].str.contains(movie, na=False, case=False)]
  return filtered_data_byname

st.sidebar.subheader("Titulo del filme:")
movieSearch = st.sidebar.text_input("nombre")
btnFiltrar = st.sidebar.button("Buscar")
#
if btnFiltrar:
  movies_byName = loadbyName(movieSearch)
  count_row = movies_byName.shape[0]
  st.write (f"Total items: {count_row}")
  st.dataframe(movies_byName)

st.sidebar.markdown("""-----""")

def load_data_bydirector(director):
  movies_filtered = data[data['director'] == director]
  return movies_filtered


selected_director = st.sidebar.selectbox("Select director", data['director'].unique())
btnFilterbyDirector = st.sidebar.button('Filter by director')

if (btnFilterbyDirector):
  filterbydirector = load_data_bydirector(selected_director)
  count_row = filterbydirector.shape[0]
  st.write (f"Total items: {count_row}")
  st.dataframe(filterbydirector)

st.sidebar.markdown("""-----""")

st.sidebar.header ("Nuevo Filme")
name = st.sidebar.text_input("Name")
company = st.sidebar.selectbox("Company", data['company'].unique())
director = st.sidebar.selectbox("Director", data['director'].unique())
genre = st.sidebar.selectbox("Genre", data['genre'].unique())

submit = st.sidebar.button("Crear nuevo registro")
if name and company and director and genre and submit:
  doc_ref = db.collection("movies").document()
  doc_ref.set({
    "name": name,
    "company": company,
    "director": director,
    "genre": genre,
    "id": doc_ref.id
  })
  st.sidebar.write ("registro insertado correctamente")

st.sidebar.markdown("""-----""")
