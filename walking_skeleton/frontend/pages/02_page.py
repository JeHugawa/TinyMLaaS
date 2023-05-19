import streamlit as st 
import requests

backend_url = "http://backend:8000/"


if st.button("hae"):
  response = requests.get(f"{backend_url}/models/somenet")
  st.write(response.text)

if st.button("lähetä"):
  request_body = {
    "name": "Arduino",
    "description": "New",
    "price": 200,
    "tax": 0.20
  }
  
  response = requests.post(f"{backend_url}/item/", json=request_body)
  
  st.write(response.text)
