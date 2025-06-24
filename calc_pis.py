import streamlit as st

# --- Funções de Cálculo ---

def calcular_custo_liquido(custo_bruto, regime):
    """
    Calcula o custo líquido de um produto após a apropriação de créditos de PIS/COFINS.
    """
    if regime == "Não Cumulativo (Lucro Real)":
        aliquota_pis = 0.0165
        aliquota_cofins = 0.076
        aliquota_total = aliquota_pis + aliquota_cofins

        credito_pis = custo_bruto * aliquota_pis
        credito_cofins = custo_bruto * aliquota_cofins
        credito_total = custo_bruto * aliquota_total

        custo_liquido = custo_bruto - credito_total

        return {
            "custo_bruto": custo_bruto,
            "custo_liquido": custo_liquido,
            "credito_pis": credito_pis,
            "credito_cofins": credito_cofins,
            "credito_total": credito_total,
            "aliquota_aplicada": aliquota_total
        }
    else: # Regime Cumulativo ou outros sem crédito
        return {
            "custo_bruto": custo_bruto,
            "custo_liquido": custo_bruto, # Custo líquido é igual ao bruto
            "credito_pis": 0,
            "credito_cofins": 0,
            "credito_total": 0,
            "aliquota_aplicada": 0
        }

# --- Interface da Aplicação com Streamlit ---

st.set_page_config(page_title="Custo com PIS/COFINS", layout="centered")

st.title("💸 Calculadora de Custo Líquido com PIS/COFINS")
st.markdown("Embuta o crédito de PIS e COFINS no seu custo médio de aquisição.")
st.markdown("---")

# --- Inputs do Usuário ---
st.header("1. Insira os Dados da Compra")

regime_tributario = st.selectbox(
    "Qual o regime de tributação da sua empresa?",
    ("Não Cumulativo (Lucro Real)", "Cumulativo (Lucro Presumido)")
)

custo_aquisicao = st.number_input(
    "Valor de aquisição do produto/insumo (R$)",
    min_value=0.0,
    format="%.2f",
    help="Informe o valor total pago ao fornecedor, conforme a nota fiscal de compra."
)

# --- Botão e Lógica de Cálculo ---
if st.button("Calcular Custo Médio Líquido"):
    if custo_aquisicao > 0:
        resultado = calcular_custo_liquido(custo_aquisicao, regime_tributario)

        st.markdown("---")
        st.header("2. Resultados")

        col1, col2 = st.columns(2)
        col1.metric(
            "Custo de Aquisição (Bruto)",
            f"R$ {resultado['custo_bruto']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )
        col2.metric(
            "Crédito Total de PIS/COFINS",
            f"R$ {resultado['credito_total']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            help=f"PIS (1.65%): R$ {resultado['credito_pis']:.2f} | COFINS (7.6%): R$ {resultado['credito_cofins']:.2f}"
        )
        
        st.divider()

        st.metric(
            label="✅ CUSTO MÉDIO LÍQUIDO (CUSTO REAL)",
            value=f"R$ {resultado['custo_liquido']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )
        st.caption("Este é o custo que você deve usar para formar seu preço de venda.")

        if regime_tributario == "Não Cumulativo (Lucro Real)":
            st.info(
                f"O cálculo considerou a apropriação de um crédito de **{resultado['aliquota_aplicada']:.2%}** "
                f"sobre o custo de aquisição. Esse crédito reduz seu custo efetivo."
            )
        else:
            st.warning(
                "No Regime Cumulativo, não há apropriação de créditos de PIS/COFINS sobre as compras. "
                "Portanto, o custo líquido é igual ao custo bruto de aquisição."
            )

    else:
        st.error("Por favor, insira um valor de aquisição válido para calcular.")

st.markdown("---")
st.markdown("_Desenvolvido por BI BCMED._")