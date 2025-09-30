# pages/overview.py
import pandas as pd
import plotly.express as px
import streamlit as st

from app_lib.api import get_json, post_json
from app_lib.misc import parse_month_any, metric_card
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

def render_overview():
    # Ação de treino (mostra só aqui)
    st.subheader("Atualizar modelo")
    st.caption("Executa treinamento e grava predições + métricas no banco.")
    if st.button("Treinar Modelo", key="train_btn"):
        _, err = post_json("/training-model")
        if err:
            st.error(err)
        else:
            st.success("Treino concluído!")

    st.markdown("---")

    # Métricas
    st.subheader("Métricas do Modelo")
    metrics_json, err_m = get_json("/errors-metrics")
    rmse = mse = mape = None
    if err_m:
        st.error(err_m)
    else:
        metrics = None
        if isinstance(metrics_json, dict):
            metrics = metrics_json
        elif isinstance(metrics_json, list) and metrics_json:
            try:
                metrics = sorted(metrics_json, key=lambda x: x.get("created_at"))[-1]
            except Exception:
                metrics = metrics_json[-1]
        if metrics:
            rmse = float(metrics.get("rmse", 0.0))
            mse  = float(metrics.get("mse", 0.0))
            mape = float(metrics.get("mape", 0.0))

    # Série geral
    series, err_s = get_json("/general-index-ipca")
    if err_s:
        st.error(err_s)
        return

    df = pd.DataFrame(series)
    needed = {"month", "real_value", "prediction_value"}
    if not needed.issubset(df.columns):
        st.warning(f"Formato inesperado. Esperado: {needed}")
        st.dataframe(df, use_container_width=True)
        return
    df["month_dt"] = df["month"].apply(parse_month_any)
    df = df.dropna(subset=["month_dt"]).sort_values("month_dt")
    df["year"] = df["month_dt"].dt.year

    # layout 20% / 80%
    left, right = st.columns([1, 4])

    with left:
        if rmse is None:
            st.info("Nenhuma métrica encontrada.")
        else:
            metric_card("RMSE", f"{rmse:0.4f}")
            metric_card("MSE",  f"{mse:0.4f}")
            metric_card("MAPE", f"{mape:0.4f}")

    with right:
        st.subheader("Índice Geral — Real vs. Previsão")
        if not df.empty:
            st.caption(f"Período disponível: **{df['month_dt'].min():%Y-%m} → {df['month_dt'].max():%Y-%m}**")

        years = sorted(df["year"].unique().tolist())
        sel_years = st.multiselect("Filtro por ano", options=years, default=years)
        df_plot = df[df["year"].isin(sel_years)].copy() if sel_years else df.copy()

        df_long = df_plot.melt(
            id_vars=["month_dt"],
            value_vars=["real_value", "prediction_value"],
            var_name="Série",
            value_name="IPCA"
        ).replace({"Série": {"real_value": "Valor Real", "prediction_value": "Valor da Predição"}})

        fig = px.line(df_long, x="month_dt", y="IPCA", color="Série", markers=True,
                      labels={"month_dt": "Mês", "IPCA": "IPCA", "Série": "Série"})
        if not df_plot.empty:
            end_dt = df_plot["month_dt"].max()
            start_dt = end_dt - pd.DateOffset(months=11)
            fig.update_xaxes(range=[start_dt, end_dt])
        fig.update_traces(hovertemplate="%{x|%Y-%m}<br>%{y:.3f}")
        fig.update_xaxes(tickformat="%Y-%m", dtick="M1")
        fig = _style_fig(fig, with_rangeslider=True)
        st.plotly_chart(fig, use_container_width=True)

        # tabela
        table1 = df_plot[["month_dt", "real_value", "prediction_value"]].copy()
        table1 = table1.sort_values("month_dt", ascending=False)
        table1["Ano Mês"] = table1["month_dt"].dt.strftime("%Y-%m")
        table1 = table1.drop(columns=["month_dt"])
        table1 = table1.rename(columns={"real_value": "Valor Real", "prediction_value": "Valor da Predição"})
        st.dataframe(table1[["Ano Mês", "Valor Real", "Valor da Predição"]],
                     use_container_width=True, height=320)
