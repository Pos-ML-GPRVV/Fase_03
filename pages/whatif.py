# pages/whatif.py
from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from app_lib.api import get_json, post_json
from app_lib.misc import parse_month_any
from app_lib.theme import PALETTE  # apenas para cores, se quiser usar

# Ordem EXATA usada pelo treino / API
CATEGORIES = [
    "1.Alimentação e bebidas",
    "2.Habitação",
    "3.Artigos de residência",
    "4.Vestuário",
    "5.Transportes",
    "6.Saúde e cuidados pessoais",
    "7.Despesas pessoais",
    "8.Educação",
]


def _fetch_latest_defaults() -> pd.DataFrame:
    """Tenta buscar o último mês de /feature-ipca para virar default.
    Se não der, retorna um default razoável.
    """
    feat_json, err = get_json("/feature-ipca")
    if err or not feat_json:
        return pd.DataFrame({
            "Categoria": CATEGORIES,
            "Peso (%)": [12, 16, 4, 5, 20, 13, 7, 23],        # exemplo (~100%)
            "Valor":    [0.10, 0.05, 0.02, 0.03, 0.08, 0.04, 0.03, 0.04],
        })

    df_feat = pd.DataFrame(feat_json)
    ok = {"month", "category", "value", "weight"}.issubset(df_feat.columns)
    if not ok or df_feat.empty:
        return pd.DataFrame({
            "Categoria": CATEGORIES,
            "Peso (%)": [12, 16, 4, 5, 20, 13, 7, 23],
            "Valor":    [0.10, 0.05, 0.02, 0.03, 0.08, 0.04, 0.03, 0.04],
        })

    # Último mês
    df_feat["month_dt"] = df_feat["month"].apply(parse_month_any)
    last_m = df_feat["month_dt"].max()
    last_df = df_feat[df_feat["month_dt"] == last_m].copy()

    # Reordena nas 8 categorias padrão
    pivot_val = last_df.pivot_table(index="category", values="value", aggfunc="mean").reindex(CATEGORIES)
    pivot_wgt = last_df.pivot_table(index="category", values="weight", aggfunc="mean").reindex(CATEGORIES)

    pesos_pct = (pivot_wgt["weight"].fillna(0.0) * 100.0).round(2)
    valores   = pivot_val["value"].fillna(0.0).round(4)

    return pd.DataFrame({
        "Categoria": CATEGORIES,
        "Peso (%)": pesos_pct.values.tolist(),
        "Valor":    valores.values.tolist(),
    })


def render_whatif():
    st.subheader("Previsão What-if (8 categorias)")

    # ——— Texto educativo inicial ———
    st.markdown(
        """
**O que é esta simulação?**  
Monte um cenário alterando **Valor** e **Peso (%)** de cada categoria.  
Com isso calculamos as **Contribuições** (Valor × Peso normalizado) e enviamos esse vetor com 8 números para a API de previsão.

**Como preencher?**
- **Valor**: variação mensal da categoria (ex.: `0,40` significa +0,40% no mês).  
- **Peso (%)**: participação relativa da categoria (em porcentagem).  
  A soma **não precisa** dar 100% — normalizamos automaticamente.

**De onde vêm os números iniciais?**
- Tentamos carregar o **último mês disponível**.  
- Se não houver dados, usamos **valores/pesos padrão** apenas como ponto de partida.

**Exemplos rápidos**
- Aumentar “Transporte” de `0,20` para `0,60` (mantendo pesos) tende a elevar a previsão.  
- Reduzir “Alimentação e bebidas” de `0,50` para `0,10` tende a diminuir o total.
        """
    )

    # ——— Parâmetros do cenário ———
    st.markdown("### Parâmetros do cenário")
    st.caption("Edite os campos **Valor** e **Peso (%)** abaixo. O peso é normalizado internamente e aplicado ao Valor.")

    defaults_df = _fetch_latest_defaults()
    edited = st.data_editor(
        defaults_df,
        column_config={
            "Categoria": st.column_config.TextColumn(disabled=True),
            "Peso (%)":  st.column_config.NumberColumn(format="%.2f", min_value=0.0, max_value=100.0, step=0.1),
            "Valor":     st.column_config.NumberColumn(format="%.4f", step=0.01),
        },
        num_rows="fixed",
        use_container_width=True,
        hide_index=True,
        key="whatif_editor",
    )

    # Normalização dos pesos
    pesos = np.array(edited["Peso (%)"].astype(float).values, dtype=float)
    if pesos.sum() <= 0:
        pesos_norm = np.ones_like(pesos) / len(pesos)
    else:
        pesos_norm = pesos / pesos.sum()

    valores = np.array(edited["Valor"].astype(float).values, dtype=float)
    contribuicoes = (valores * pesos_norm)

    # ——— Tabela de contribuições ———
    st.markdown("### Contribuições")
    st.caption(
        """
        Estas **Contribuições** já vêm **pré-preenchidas** a partir dos Parâmetros. Para cada categoria fazemos **Valor × Peso normalizado**.  
        """
    )

    show_df = edited.copy()
    show_df["Peso normalizado"] = (pesos_norm * 100).round(2)
    show_df["Contribuição (Valor×Peso)"] = contribuicoes.round(4)

    st.dataframe(
        show_df[["Categoria", "Valor", "Peso (%)", "Peso normalizado", "Contribuição (Valor×Peso)"]],
        use_container_width=True,
        hide_index=True,
    )

    # ——— Botão de previsão ———
    colA, colB = st.columns([1, 3])
    with colA:
        clicked = st.button("Calcular previsão", use_container_width=True)
    pred = None
    contribs = np.round(contribuicoes, 4).tolist()

    if clicked:
        payload = {"data": contribs}
        resp, err = post_json("/prevision-ipca/", payload)
        if err:
            st.error(err)
        else:
            pred = float(resp.get("prediction", 0.0))
            st.success(f"**IPCA previsto:** {pred:.4f}")

    # ——— Gráfico ———
    st.markdown("### 📈 Contribuição das categorias → IPCA previsto")
    st.caption(
        """
O gráfico de **cascata ** mostra quanto cada categoria **puxa para cima** ou **empurra para baixo**
a previsão final. A última barra (“IPCA previsto”) é o total estimado usando as contribuições acima.
        """
    )

    # Se ainda não clicou, mostramos um gráfico com as contribuições atuais e um “total” ilustrativo igual à soma
    total_plot = pred if pred is not None else float(np.sum(contribuicoes))
    fig_w = go.Figure(
        go.Waterfall(
            name="Contribuições",
            orientation="v",
            measure=["relative"] * len(CATEGORIES) + ["total"],
            x=CATEGORIES + ["IPCA previsto"],
            y=contribs + [total_plot],
            connector={"line": {"color": "rgba(255,255,255,0.2)"}},
            increasing={"marker": {"color": "#F2600C"}},
            decreasing={"marker": {"color": "#A62F03"}},
            totals={"marker": {"color": "#1F1F1F"}},
            text=[f"{v:.3f}" for v in contribs] + [f"{total_plot:.3f}"],
            textposition="outside",
            hovertemplate="%{x}<br>%{y:.4f}<extra></extra>",
        )
    )
    fig_w.update_layout(
        title="Contribuição das categorias → IPCA previsto",
        title_x=0.0,
        margin=dict(l=10, r=10, t=40, b=10),
        yaxis_title="IPCA",
        xaxis_title="Categorias",
        hovermode="x unified",
        plot_bgcolor="#111111",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_w, use_container_width=True)

    # ——— Ajuda ———
    with st.expander("Como funciona esta simulação?"):
        st.markdown(
            """
- **Valor**: variação estimada para a categoria (ex.: `0,40`).
- **Peso (%)**: participação relativa dessa categoria no índice.  
- Primeiro normalizamos os pesos para somarem `100%`.  
- A **Contribuição** é `Valor × Peso normalizado`.  
- O vetor com **8 contribuições** (na ordem das categorias) é enviado à **API** para estimar o **IPCA previsto**.  
- O **gráfico de cascata** ilustra o impacto de cada categoria no caminho até o total.
            """
        )
