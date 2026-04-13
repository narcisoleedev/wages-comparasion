import streamlit as st

from src.logic.calcular_clt import calcular_clt
#from src.logic.calcular_estagio import calcular_estagio

if "renda_variavel" not in st.session_state:
    st.session_state["renda_variavel"] = []

if "mostrar_renda_variavel" not in st.session_state:
    st.session_state["mostrar_renda_variavel"] = False

st.title("Calculadora de Remuneração 2026")

st.header("Remuneração")

cargo = st.text_input("Cargo")
regime = st.selectbox("Regime de Trabalho", ["CLT", "Estágio"])
salario = st.number_input("Salário", min_value=0.0)
beneficios = st.text_input("Benefícios (Ex: Vale Transporte, Vale Refeição, etc.)")

if st.button("Adicionar Renda Variável (Ex: Comissões, Bônus, etc.)?"):
    st.session_state["mostrar_renda_variavel"] = not st.session_state["mostrar_renda_variavel"]

if st.session_state["mostrar_renda_variavel"]:
    with st.form("renda_variavel_form"):
        nome_renda_variavel = st.text_input("Nome da Renda Variável")
        valor_renda_variavel = st.number_input("Valor da Renda Variável", min_value=0.0)
        data_renda_variavel = st.date_input("Data de Recebimento da Renda Variável")
        add = st.form_submit_button("Adicionar")
        if add:
            st.session_state["renda_variavel"].append({
                "Cargo": cargo,
                "Nome": nome_renda_variavel,
                "Valor": valor_renda_variavel,
                "Data": data_renda_variavel
            })
            st.success("Renda Variável adicionada com sucesso!")

if st.button("Calcular"):
    resultado = None
    if regime == "CLT":
        resultado = calcular_clt(float(salario), float(beneficios), st.session_state["renda_variavel"])

    st.header("Resultado")
    st.subheader("Evolução da Remuneração ao Longo do Ano para o cargo de {}".format(cargo))
    chart_data = resultado.copy()
    chart_data["Líquido + Benefícios"] = chart_data["Salário Líquido"] + chart_data["Benefícios"]
    st.area_chart(
        chart_data[["Mês", "Líquido + Benefícios", "Salário Bruto"]],
        x="Mês",
        y=["Salário Bruto", "Líquido + Benefícios"],
        x_label="Mês",
        y_label="Remuneração (R$)",
        color=["#e05c5c", "#4c9be8"],
        stack=False,
    )

    st.divider()

    st.markdown(
        f"""
        - Remuneração Média Bruta: R$ {resultado["Salário Bruto"][11]/12:.2f}
        - Remuneração Média Líquida + Benefícios: R$ {resultado["Salário Líquido"][11]/12 + resultado["Benefícios"][11]/12:.2f}
        """
    )

    with st.expander("Tabela dos Rendimentos"):
        st.dataframe(resultado)
