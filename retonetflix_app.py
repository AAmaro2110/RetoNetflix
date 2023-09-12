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


movies_ref = db.collection(u'movies').stream()
movies_dict = list(map(lambda x: x.to_dict(), movies_ref))
movies_dataframe = pd.DataFrame(movies_dict)

#Test


data = movies_dataframe


agree = st.sidebar.checkbox("Mostrar todos los filmes")
if agree:
  st.dataframe(data)



def loadbyName(movie):
  movies_ref1 = dbMovies.where(u'name',u'array_contains_any',movie)
  movies_dict1 = list(map(lambda x: x.to_dict(), movies_ref1))
  movies_dataframe1 = pd.DataFrame(movies_dict1)
  if movies_dataframe1 is None:
    st.sidebar.write("nombre no existe")
  else:
    return movies_dataframe1

st.sidebar.subheader("Titulo del filme:")
movieSearch = st.sidebar.text_input("nombre")
btnFiltrar = st.sidebar.button("Buscar")

if btnFiltrar:
  movies_list = loadbyName(movieSearch)
  if movies_list is None:
    st.sidebar.write("Nombre no existe")
  else:
    st.dataframe(movies_list)

st.sidebar.markdown("""-----""")

def load_data_bydirector(director):
  movies_ref1 = dbMovies.where(u'name',u'==',director)
  movies_dict1 = list(map(lambda x: x.to_dict(), movies_ref1))
  movies_dataframe1 = pd.DataFrame(movies_dict1)
  return movies_dataframe1

data = movies_dataframe
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
  doc_ref = db.collection("movies").document(name)
  doc_ref.set({
    "name": name,
    "company": company,
    "director": director,
    "genre": genre
  })
  st.sidebar.write ("registro insertado correctamente")

st.sidebar.markdown("""-----""")
