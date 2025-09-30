# pages/decomposition.py
import textwrap
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from app_lib.api import get_json
from app_lib.misc import parse_month_any
from app_lib.theme import PALETTE

def _style_fig(fig, with_rangeslider=True):
    fig.update_layout(
        paper_bgcolor=PALETTE["panel"],
        plot_bgcolor=PALETTE["panel"],
        font=dict(color=PALETTE["text"]),
        legend_title=dict(font=dict(color=PALETTE["text"])),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=10, r=10, t=40, b=10),
        hovermode="x unified",
    )
    fig.update_xaxes(
        showgrid=True, gridcolor=PALETTE["grid"], zeroline=False, linecolor=PALETTE["border"],
        tickfont=dict(color=PALETTE["text"]),
        rangeslider=(dict(visible=True, thickness=0.10, bgcolor="rgba(40,40,40,0.55)",
                          bordercolor="rgba(255,255,255,0.15)", borderwidth=1) if with_rangeslider else None)
    )
    fig.update_yaxes(showgrid=True, gridcolor=PALETTE["grid"], zeroline=False, linecolor=PALETTE["border"],
                     tickfont=dict(color=PALETTE["text"]))
    return fig

def render_decomposition():
    st.subheader("Decomposição por Categorias (com pesos)")
    feat, err_f = get_json("/feature-ipca")
    if err_f:
        st.error(err_f)
        return

    df_feat = pd.DataFrame(feat)
    expected = {"month", "category", "value", "weight"}
    if not expected.issubset(df_feat.columns):
        st.warning(f"Formato inesperado. Colunas esperadas: {expected}")
        st.dataframe(df_feat, use_container_width=True)
        return

    df_feat["month_dt"] = df_feat["month"].apply(parse_month_any)
    df_feat = df_feat.dropna(subset=["month_dt"]).sort_values(["month_dt", "category"])
    pivot = (df_feat.pivot_table(index="month_dt", columns="category", values="value", aggfunc="mean")
             .fillna(0.0).sort_index())

    fig2 = px.area(pivot, x=pivot.index, y=pivot.columns)
    fig2.update_traces(hovertemplate="%{x|%Y-%m}<br>%{y:.3f}")
    if not pivot.empty:
        end_dt2 = pivot.index.max()
        start_dt2 = end_dt2 - pd.DateOffset(months=11)
        fig2.update_xaxes(range=[start_dt2, end_dt2])
    fig2.update_xaxes(tickformat="%Y-%m", dtick="M1")
    fig2.update_layout(title="Decomposição por Categoria — Valores Mensais",
                       xaxis_title="Mês", yaxis_title="Valor",
                       legend_title_text="Categorias:")
    fig2 = _style_fig(fig2, with_rangeslider=True)
    st.plotly_chart(fig2, use_container_width=True)

    # Tabela estilizada (aberta por padrão)
    table_df = pivot.copy().sort_index(ascending=False)
    table_df.index = table_df.index.strftime("%Y-%m")
    table_df.index.name = "Ano Mês"
    table_df = table_df.reset_index()

    def wrap_hdr(s: str, width: int = 18) -> str:
        return "<br>".join(textwrap.wrap(str(s), width=width))

    header_values = ["<b>Ano Mês</b>"] + [f"<b>{wrap_hdr(c)}</b>" for c in table_df.columns[1:]]
    zebra = ["rgba(255,255,255,0.02)" if i % 2 == 0 else "rgba(255,255,255,0.00)" for i in range(len(table_df))]

    fig_table = go.Figure(
        data=[go.Table(
            header=dict(values=header_values,
                        fill_color=PALETTE["panel"],
                        line_color=PALETTE["border"],
                        font=dict(color=PALETTE["text"], size=14),
                        align="left", height=48),
            cells=dict(values=[table_df[c] for c in table_df.columns],
                       fill_color=[zebra],
                       line_color=PALETTE["border"],
                       font=dict(color=PALETTE["text"], size=12),
                       align="left", height=28),
            columnwidth=[110] + [170] * (len(table_df.columns) - 1),
        )]
    )
    fig_table.update_layout(margin=dict(l=0, r=0, t=0, b=0),
                            paper_bgcolor=PALETTE["panel"],
                            height=min(460, 70 + 28 * len(table_df)) if len(table_df) else 220)
    st.plotly_chart(fig_table, use_container_width=True)
