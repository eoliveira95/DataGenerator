import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from paginas.home import pagina_inicial
from paginas.novaslinhas import pagina_novaslinhas
from paginas.qaptermx import pagina_qapter

# Carregar configurações do arquivo YAML
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

st.set_page_config(
    page_title="Data Generator",
    layout="wide",  
    initial_sidebar_state="expanded" 
)

# Autenticar usuário
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
    )

authenticator.login()

if st.session_state["authentication_status"]:
    authenticator.logout()

    st.sidebar.title('Navigation')
    st.sidebar.write(f'Welcome *{st.session_state["name"]}*')
    paginas = st.sidebar.selectbox("Select the Page:", ["Home", "New Lines", "Qapter"])
    if paginas == "Home":
        pagina_inicial()
    elif paginas == "Qapter":
        pass
        pagina_qapter()
    elif paginas == "New Lines":
        pass
        pagina_novaslinhas()
    
    
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')