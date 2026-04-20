import streamlit as st

from src.utils.pages import Pages

states = {
    "page": Pages.CALCULADORA_REMUNERACAO.value,
    "renda_variavel": [],
    "mostrar_renda_variavel": False
}

def init_state():
    for key, val in states.items():
        if key not in st.session_state:
            st.session_state[key] = val

if __name__ == "__main__":
    init_state()

    with st.sidebar:
        st.title("Navegação")
        page = st.selectbox("Selecione a página", [Pages.HOME.value, Pages.CALCULADORA_REMUNERACAO.value])
        st.session_state["page"] = page

    if st.session_state["page"] == Pages.CALCULADORA_REMUNERACAO.value:
        from src.pages.calculadora_remuneracao import calculadora_remuneracao
        calculadora_remuneracao()


