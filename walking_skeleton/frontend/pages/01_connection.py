import streamlit as st 
import requests
import os

from dotenv import load_dotenv
load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")#"http://backend:8000/"


if st.button("GET"):
  response = requests.get(f"{BACKEND_URL}/models/somenet")
  st.write(response.text)

if st.button("POST"):
  request_body = {
    "name": "Arduino",
    "description": "New",
    "price": 200,
    "tax": 0.20
  }
  
  response = requests.post(f"{BACKEND_URL}/item/", json=request_body)
  
  st.write(response.text)
