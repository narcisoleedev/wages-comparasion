import numpy as np

def tributacao_rv(valor: float) -> dict:
    "Aplica a tributação de PLR sobre o valor da renda variável. Retorna bruto e líquido."
    if valor <= 7407.11:
        imposto = 0.0
    elif valor <= 9922.28:
        imposto = valor * 0.075 - 555.53
    elif valor <= 13167.00:
        imposto = valor * 0.15 - 1299.70
    elif valor <= 16380.38:
        imposto = valor * 0.225 - 2287.23
    else:
        imposto = valor * 0.275 - 3106.25

    return {"bruto": valor, "liquido": valor - imposto}

def calcular_clt(salario_bruto: float, beneficios: float, renda_variavel: list) -> pd.DataFrame:
    "Retorna um DataFrame com a remuneração acumulada para um período de 12 meses."

    mes_atual = np.datetime64('today', 'M')
    to_return = []

    def calcular_inss(salario_bruto: float) -> float:
        # Cálculo do INSS
        if salario_bruto <= 1621.00:
            inss = salario_bruto * 0.075
        elif salario_bruto <= 2902.84:
            inss = salario_bruto * 0.09 - 24.32
        elif salario_bruto <= 4354.27:
            inss = salario_bruto * 0.12 - 111.41
        elif salario_bruto <= 8475.55:
            inss = salario_bruto * 0.14 - 198.50
        else: 
            inss = 1002.26
        return inss

    # Cálculo do IRRF
    def calcular_irrf(salario_bruto: float) -> float:
        base_calculo_irrf = salario_bruto - calcular_inss(salario_bruto)
        if base_calculo_irrf <= 5000:
            irrf = 0
        elif base_calculo_irrf <= 7350:
            irrf = base_calculo_irrf * 0.275 - 908.73 - (978.62 - (0.133145 * base_calculo_irrf))
        else:
            irrf = base_calculo_irrf * 0.275 - 908.73
        return irrf

    salario_liquido = salario_bruto - calcular_inss(salario_bruto) - calcular_irrf(salario_bruto) 

    acum_bruto = 0.0
    acum_inss = 0.0
    acum_irrf = 0.0
    acum_beneficios = 0.0
    acum_rv = 0.0
    acum_decimo = 0.0
    acum_liquido = 0.0

    for i in range(12):
        mes = mes_atual + np.timedelta64(i, 'M')
        mes_periodo = mes.astype('datetime64[M]')
        mes_numero = mes_periodo.item().month

        # 13º salário pago em dezembro, proporcional aos meses trabalhados no ano
        decimo_bruto = salario_bruto * (i + 1) / 12
        decimo_terceiro = (decimo_bruto - calcular_inss(decimo_bruto) - calcular_irrf(decimo_bruto)) if mes_numero == 12 else 0.0

        # Soma das bonificações cujo mês de recebimento coincide com o mês atual do loop
        rvs_mes = [
            tributacao_rv(rv["Valor"])
            for rv in renda_variavel
            if np.datetime64(rv["Data"].strftime('%Y-%m')) == mes_periodo
        ]
        bonificacoes_bruto = sum(rv["bruto"] for rv in rvs_mes)
        bonificacoes_liquido = sum(rv["liquido"] for rv in rvs_mes)

        acum_bruto += salario_bruto + bonificacoes_bruto if mes_numero != 12 else salario_bruto + decimo_bruto + bonificacoes_bruto
        acum_inss += calcular_inss(salario_bruto) if mes_numero != 12 else calcular_inss(salario_bruto) + calcular_inss(decimo_bruto)
        acum_irrf += calcular_irrf(salario_bruto) if mes_numero != 12 else calcular_irrf(salario_bruto) + calcular_irrf(decimo_bruto)
        acum_beneficios += beneficios
        acum_rv += bonificacoes_liquido
        acum_decimo += decimo_terceiro
        acum_liquido += salario_liquido + decimo_terceiro + bonificacoes_liquido

        to_return.append({
            "Mês": mes_periodo.item().strftime('%Y-%m'),
            "Salário Bruto": acum_bruto,
            "INSS": acum_inss,
            "IRRF": acum_irrf,
            "Benefícios": acum_beneficios,
            "Renda Variável": acum_rv,
            "13º Salário": acum_decimo,
            "Salário Líquido": acum_liquido,
        })

    return pd.DataFrame(to_return)