import streamlit as st
from modules.database import *
from modules.dashboard import *
import plotly.express as px

st.set_page_config(layout="wide", page_title="FinancesV2", page_icon="💰")

st.divider() # Adds a clean horizontal line like an <hr> tag

tab1, tab2, tab3, tab4 = st.tabs(["Revenues", "Spents", "Investments", "Metrics"])

with tab1:
    show_revenue_table()

with tab2:
    show_spent_table()

with tab3:
    show_investments_table()

# -----------------------------
# with tab4:
#     st.components.v1.iframe(
#         "https://app.powerbi.com/view?r=eyJrIjoiNzQ4MWNlNGYtOTk4OS00YjI5LTllNmItMDhlZjI1ODhmMjdjIiwidCI6Ijg1YWI4ZjE2LTY3YjMtNDhhNS05OTM4LTNhNGQ3YzYwNDM0MSJ9",
#         height = 700,
#         width = 1200
#     )

with tab4:
    # Your Power BI URL
    pbi_url = "https://app.powerbi.com/view?r=eyJrIjoiNzQ4MWNlNGYtOTk4OS00YjI5LTllNmItMDhlZjI1ODhmMjdjIiwidCI6Ijg1YWI4ZjE2LTY3YjMtNDhhNS05OTM4LTNhNGQ3YzYwNDM0MSJ9"

    # HTML and CSS for a responsive iframe
    responsive_iframe = f"""
    <style>
        /* Container holding the iframe */
        .responsive-iframe-container {{
            position: relative;
            width: 100%;
            /* Default aspect ratio for Desktop (16:9) */
            padding-bottom: 56.25%; 
            height: 0;
            overflow: hidden;
        }}

        /* The iframe itself */
        .responsive-iframe-container iframe {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: none;
        }}

        /* Media query for Mobile Devices (screens smaller than 768px) */
        @media screen and (max-width: 768px) {{
            .responsive-iframe-container {{
                /* Adjust this percentage to make it taller or shorter on mobile */
                padding-bottom: 65%; 
            }}
        }}
    </style>

    <div class="responsive-iframe-container">
        <iframe src="{pbi_url}" allowFullScreen="true"></iframe>
    </div>
    """

    # Render the HTML/CSS in Streamlit
    st.markdown(responsive_iframe, unsafe_allow_html=True)
#     df_rev, df_spent, df_rev_current, df_spent_current = load_data()

# #     rev_ytd, spent_ytd = calc_ytd(df_rev, df_spent)

# #     if df_rev.empty and df_spent.empty:
# #         st.warning("No data available")
# #         st.stop()

#     df_rev = add_calendar(df_rev)
#     df_spent = add_calendar(df_spent)

#     kpis_current = calc_kpis(df_rev, df_spent, df_rev_current, df_spent_current)         

#     # -------- KPI ROW --------
#     col1, col2, col3 = st.columns(3)

#     with col1:
#         kpi_card(
#             "Revenues",
#             kpis_current["revenues"],
#             value_pm=kpis_current["revenue_pm"],
#             delta=kpis_current["revenue_pm"],
#             value_py=kpis_current["revenues_py"],
#             ytd=kpis_current["revenues_ytd"]
#         )

#     with col2:
#         kpi_card(
#             "Spents",
#             kpis_current["spents"],
#             value_pm=kpis_current["spents_pm"],
#             delta=kpis_current["spents_pm"],
#             value_py=kpis_current["spents_py"],
#             ytd=kpis_current["spents_ytd"]
#         )

#     with col3:
#         kpi_card(
#             "Balance",
#             kpis_current["balance"],
#             value_pm=kpis_current["balance_pm"],
#             delta=kpis_current["balance_pm"],
#             value_py=kpis_current["balance_py"],
#             ytd=kpis_current["balance_ytd"]
#         )

#     st.divider()

#     render_comparison_chart(df_rev=df_rev, df_spent=df_spent)

#     st.divider()

#     render_powerbi_matrix(df_rev=df_rev, df_spent=df_spent)