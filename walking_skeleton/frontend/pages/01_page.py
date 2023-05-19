import streamlit as st
import pandas as pd

# pelkkä teksti
st.header('Testisivu')
st.write('Pelkkää testiä')

# taulukko
st.write('This is my first table:')
st.write(pd.DataFrame({
    'first': [1,2,3,4],
    'second': [10, 20, 30, 40]
}))

# kuvaaja
st.write('The plot thickens:')
chart_data = pd.DataFrame({
    'first': [1,2,3,4],
    'second': [10, 20, 30, 40]
})

st.line_chart(chart_data)

if st.checkbox('Näytä interaktiivisuus'):
    # interaktiivisuutta
    x = st.slider('x')
    st.write(x, 'neliö on', x*x)