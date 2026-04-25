import streamlit as st
import pandas as pd
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode, JsCode, StAggridTheme
from modules.database import *
from services.db_connection import get_revenues, get_spents

from datetime import date

today = date.today()
start_month = today.replace(day=1)

st.set_page_config(layout="wide", page_title="FinancesV2", page_icon="💰")

def get_unified_spents(df_spents, df_investments):
    # 1. Prepare Spents (SELECTCOLUMNS equivalent)
    # We create a copy to avoid modifying the original dataframe
    spents_part = df_spents[['data', 'despesas', 'descricao', 'valor']].copy()
    spents_part.columns = ['data', 'category', 'descricao', 'valor']
    spents_part['Type'] = 'Spent'

    # 2. Prepare Investments (FILTER + SELECTCOLUMNS equivalent)
    # Filter: Origem != "Reserva Emerg." AND Ativo == True
    invest_filter = (df_investments['origem'] != 'Reserva Emerg.') & (df_investments['ativo'] == True)
    
    invest_part = df_investments[invest_filter][['data_investimento', 'tipo', 'ticker', 'valor']].copy()
    invest_part.columns = ['data', 'category', 'descricao', 'valor']
    invest_part['Type'] = 'Investment'

    # 3. Union the tables (UNION equivalent)
    unified_df = pd.concat([spents_part, invest_part], ignore_index=True)
    
    return unified_df

def load_data():
    # Date Picker, consider only the current month by default
    date_range = st.date_input(
    "Select period",
    value=(start_month, today)
    )

    start_date, end_date = date_range

    df_rev = pd.DataFrame(get_revenues())
    # df_spent = pd.DataFrame(get_spents())

    raw_spents = get_spents()
    df_raw_spents = pd.DataFrame(raw_spents)
    raw_investments = get_investments()
    df_raw_investments = pd.DataFrame(raw_investments)

    df_spent = pd.DataFrame(get_unified_spents(df_raw_spents, df_raw_investments))

    if not df_rev.empty:
        df_rev["data"] = pd.to_datetime(df_rev["data"])    

    if not df_spent.empty:
        df_spent["data"] = pd.to_datetime(df_spent["data"])    

    # Get current month filter
    df_rev_current = df_rev[
        (df_rev["data"] >= pd.to_datetime(start_date)) &
        (df_rev["data"] <= pd.to_datetime(end_date))
    ]

    df_spent_current = df_spent[
        (df_spent["data"] >= pd.to_datetime(start_date)) &
        (df_spent["data"] <= pd.to_datetime(end_date))
    ]

    return df_rev, df_spent, df_rev_current, df_spent_current


def add_calendar(df):
    df["year"] = df["data"].dt.year
    df["month"] = df["data"].dt.month
    df["day"] = df["data"].dt.day
    return df


def calc_kpis(df_rev, df_spent, df_rev_current, df_spent_current):
    today = pd.Timestamp.today()        
    current_month = today.month
    current_year = today.year
    
    # Calculate Previous Month / Year targets
    # Using DateOffset is safer for January/December transitions
    last_month_date = today - pd.DateOffset(months=1)
    pm_m, pm_y = last_month_date.month, last_month_date.year
    py_y = current_year - 1

    # CURRENT
    rev_c = df_rev_current["valor"].sum()
    spent_c = df_spent_current["valor"].sum()
    bal_c = rev_c - spent_c

    # PREVIOUS MONTH
    rev_pm = df_rev[(df_rev["month"] == pm_m) & (df_rev["year"] == pm_y)]["valor"].sum()
    spent_pm = df_spent[(df_spent["month"] == pm_m) & (df_spent["year"] == pm_y)]["valor"].sum()
    bal_pm = rev_pm - spent_pm

    # PREVIOUS YEAR (Same month, last year)
    rev_py = df_rev[(df_rev["month"] == current_month) & (df_rev["year"] == py_y)]["valor"].sum()
    spent_py = df_spent[(df_spent["month"] == current_month) & (df_spent["year"] == py_y)]["valor"].sum()
    bal_py = rev_py - spent_py

    # YTD
    # rev_ytd = df_rev[df_rev["year"] == current_year]["valor"].sum()
    # spent_ytd = df_spent[df_spent["year"] == current_year]["valor"].sum()
    rev_ytd = df_rev[
        (df_rev["year"] == current_year) & 
        (df_rev["data"] <= today)
    ]["valor"].sum()

    spent_ytd = df_spent[
        (df_spent["year"] == current_year) & 
        (df_spent["data"] <= today)
    ]["valor"].sum()
    bal_ytd = rev_ytd - spent_ytd        
    
    return {
        "revenues": rev_c, "revenue_pm": rev_pm, "revenues_py": rev_py, "revenues_ytd": rev_ytd,
        "spents": spent_c, "spents_pm": spent_pm, "spents_py": spent_py, "spents_ytd": spent_ytd,
        "balance": bal_c, "balance_pm": bal_pm, "balance_py": bal_py, "balance_ytd": bal_ytd
    }

# -----------------------------
# KPI COMPONENT (CUSTOM)
# -----------------------------
def kpi_card(title, value, value_pm=None, value_py=None, delta=None, ytd=None):
    with st.container(border=True):
        st.markdown(f"### {title}")

        # main_col handles the left side, ytd_col handles the right side
        main_col, ytd_col = st.columns([3, 1])

        with main_col:
            # 1. Show the main value first
            st.markdown(f"## R$ {value:,.0f}")

            # 2. Logic for Deltas
            pm_value = value_pm # 'delta' input seems to be used as PM value
            
            diff_pm = ((value - pm_value) / pm_value) * 100
            diff_py = ((value - value_py) / value_py) * 100

            # Determine colors based on "Spents" (Inverted logic)
            if title == "Spents":
                color_pm = "red" if diff_pm > 0 else "green"
                color_py = "red" if diff_py > 0 else "green"
            else:
                color_pm = "green" if diff_pm > 0 else "red"
                color_py = "green" if diff_py > 0 else "red"

            # 3. Create the delta columns AT THE BOTTOM
            aux_col1, aux_col2 = st.columns([1, 1])
            
            with aux_col1:
                symbol = "▲" if diff_pm > 0 else "▼"
                st.markdown(
                    f"<span style='color:{color_pm}; font-weight:bold;'>{symbol} {abs(diff_pm):.1f}% vs PM</span>",
                    unsafe_allow_html=True
                )
            with aux_col2:
                symbol = "▲" if diff_py > 0 else "▼"
                st.markdown(
                    f"<span style='color:{color_py}; font-weight:bold;'>{symbol} {abs(diff_py):.1f}% vs PY</span>",
                    unsafe_allow_html=True
                )

            # 4. Show the footer labels
            st.markdown(f"<span style='color:grey'>Previous Month: R$ {pm_value:,.0f}</span>", unsafe_allow_html=True)
            st.markdown(f"<span style='color:grey'>Previous Year: R$ {value_py:,.0f}</span>", unsafe_allow_html=True)

        with ytd_col:
            if ytd is not None:
                st.write("") # Add some padding
                st.markdown("**YTD**")
                st.markdown(f"R$ {ytd:,.0f}")


def prepare_chart_data(df, year, month, label):
    # Filter for the specific month/year
    filtered = df[(df["year"] == year) & (df["month"] == month)].copy()
    
    # Group by day to get total per day
    daily = filtered.groupby("day")["valor"].sum().reset_index()
    daily.columns = ["Day", label]
    
    # We want a full 31-day range even if some days have no data
    full_days = pd.DataFrame({"Day": range(1, 32)})
    daily = full_days.merge(daily, on="Day", how="left").fillna(0)
    
    # Cumulative sum (Standard for financial "burn" or "gain" charts)
    daily[label] = daily[label].cumsum()
    return daily

def render_comparison_chart(df_rev, df_spent):
    st.subheader("Performance Comparison")
    
    # 1. User Inputs
    col1, col2 = st.columns(2)
    with col1:
        data_type = st.radio("Visualize:", ["Revenues", "Spents"], horizontal=True)
    with col2:
        comparison_type = st.selectbox("Compare with:", ["Previous Month", "Previous Year"])

    # 2. Select the correct base DataFrame
    target_df = df_rev if data_type == "Revenues" else df_spent
    
    # 3. Define Dates
    today = pd.Timestamp.today()
    curr_m, curr_y = today.month, today.year
    
    if comparison_type == "Previous Month":
        comp_date = today - pd.DateOffset(months=1)
        comp_m, comp_y = comp_date.month, comp_date.year
        comp_label = "Previous Month"
    else:
        comp_m, comp_y = curr_m, curr_y - 1
        comp_label = "Previous Year"

    # 4. Prepare Data for Plotly
    df_curr = prepare_chart_data(target_df, curr_y, curr_m, "Current Month")
    df_comp = prepare_chart_data(target_df, comp_y, comp_m, comp_label)
    
    # Merge for plotting
    plot_df = df_curr.merge(df_comp, on="Day")

    labels_curr = [
        f"R$ {val:,.0f}" if (i + 1) % 5 == 0 or (i + 1) == len(plot_df) else "" 
        for i, val in enumerate(plot_df["Current Month"])
    ]

    labels_comp = [
        f"R$ {val:,.0f}" if (i + 1) % 5 == 0 or (i + 1) == len(plot_df) else "" 
        for i, val in enumerate(plot_df[comp_label])
    ]

    # 5. Build Plotly Chart
    fig = px.line(
        plot_df, 
        x="Day", 
        y=["Current Month", comp_label],
        template="plotly_dark",
        markers=True,
        # Add text labels. We format them to 'R$ 1.2k' style for better fit
        text=plot_df.apply(lambda x: f"R$ {x['Current Month']:,.0f}", axis=1), 
        color_discrete_map={
            "Current Month": "#008000", 
            comp_label: "#A3A3A3" if data_type == "Spents" else "#6B6B6B" 
        },        
        title=f"Cumulative {data_type}: Current vs {comp_label}"
    )

    # Show label every 5 days + last day
    labels = [f"R$ {v:,.0f}" if i % 5 == 0 or i == 30 else "" 
            for i, v in enumerate(plot_df["Current Month"])]
    fig.data[0].text = labels
    fig.data[1].text = ""
    # Clean up axes and text positioning
    fig.update_traces(
        textposition="top center",
        # Optional: Only show text for the last day to avoid clutter
        # selector=lambda t: t.name == "Current Month", 
    )

    fig.update_layout(
        hovermode="x unified",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="right", x=1),
        # Remove margins to make the chart feel bigger
        margin=dict(l=20, r=20, t=60, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    # Hide the X and Y axis entirely (lines, ticks, and scales)
    fig.update_xaxes(
        showgrid=False, 
        showticklabels=True, 
        zeroline=True, 
        title=None, 
        fixedrange=True
    )
    fig.update_yaxes(
        showgrid=False, 
        showticklabels=False, 
        zeroline=True, 
        title=None, 
        fixedrange=True
    )

    st.plotly_chart(fig, use_container_width=True)


def get_comparison_table(df, data_type, comparison_type):
    today = pd.Timestamp.today()
    curr_m, curr_y = today.month, today.year
    
    # 1. Define periods
    if comparison_type == "Previous Month":
        comp_date = today - pd.DateOffset(months=1)
        comp_m, comp_y = comp_date.month, comp_date.year
        comp_col_name = "Previous Month"
    else:
        comp_m, comp_y = curr_m, curr_y - 1
        comp_col_name = "Previous Year"

    # 2. Filter and Group Data
    # Identify the correct category column name from your unified function
    # 2. Fix the variable assignment (remove the brackets)
    if data_type == "Spents":
        cat_col = "category"  # From your unified_spents function
    else:
        # Check your image: the column is named 'receita' in the DB
        # Make sure your load_data() didn't rename it to 'Category'
        cat_col = "receita"
    
    curr_data = df[(df["year"] == curr_y) & (df["month"] == curr_m)]
    curr_grouped = curr_data.groupby(cat_col)["valor"].sum().reset_index()
    curr_grouped.columns = [cat_col, "Current Month"]

    comp_data = df[(df["year"] == comp_y) & (df["month"] == comp_m)]
    comp_grouped = comp_data.groupby(cat_col)["valor"].sum().reset_index()
    comp_grouped.columns = [cat_col, comp_col_name]

    # 3. Merge and Calculate Diff
    final_df = pd.merge(curr_grouped, comp_grouped, on=cat_col, how="outer").fillna(0)
    
    # Calculation: (Current / Previous) * 100 to match your image style (e.g., 109%)
    # Or (Current - Previous) / Previous for percentage change. 
    # Let's use your image logic: (Current / Previous)
    final_df["Diff"] = final_df.apply(
        lambda x: (x["Current Month"] / x[comp_col_name]) * 100 if x[comp_col_name] != 0 else 0, 
        axis=1
    )

    # 4. Add Total Row
    total_row = pd.DataFrame({
        cat_col: ["Total"],
        "Current Month": [final_df["Current Month"].sum()],
        comp_col_name: [final_df[comp_col_name].sum()],
        "Diff": [(final_df["Current Month"].sum() / final_df[comp_col_name].sum()) * 100 
                 if final_df[comp_col_name].sum() != 0 else 0]
    })
    
    return pd.concat([final_df, total_row], ignore_index=True), comp_col_name

def get_drilldown_table(df, data_type, comparison_type):
    today = pd.Timestamp.today()
    curr_m, curr_y = today.month, today.year
    
    # Define periods
    if comparison_type == "Previous Month":
        comp_date = today - pd.DateOffset(months=1)
        comp_m, comp_y = comp_date.month, comp_date.year
        comp_col_name = "Prev. Period"
    else:
        comp_m, comp_y = curr_m, curr_y - 1
        comp_col_name = "Prev. Period"

    # Set dynamic column name based on data_type
    cat_col = "category" if data_type == "Spents" else "receita"
    
    # We group by [Category, Description]
    # 'descricao' is common to both tables based on your screenshots
    group_cols = [cat_col, "descricao"]

    curr_data = df[(df["year"] == curr_y) & (df["month"] == curr_m)]
    curr_grouped = curr_data.groupby(group_cols)["valor"].sum().reset_index()
    
    comp_data = df[(df["year"] == comp_y) & (df["month"] == comp_m)]
    comp_grouped = comp_data.groupby(group_cols)["valor"].sum().reset_index()

    # Merge
    final_df = pd.merge(curr_grouped, comp_grouped, on=group_cols, how="outer").fillna(0)
    final_df.columns = ["Category", "Description", "Current", comp_col_name]
    
    # Calculate Diff
    final_df["Diff %"] = final_df.apply(
        lambda x: (x["Current"] / x[comp_col_name]) * 100 if x[comp_col_name] != 0 else 0, 
        axis=1
    )

    return final_df.sort_values(["Category", "Current"], ascending=[True, False]), comp_col_name

def style_diff(val, data_type):
    """
    Logic:
    Revenues: < 100% is Bad (Red), >= 100% is Good (Green)
    Spents: < 100% is Good (Green), >= 100% is Bad (Red)
    """
    if data_type == "Revenues":
        color = 'red' if val < 100 else '#008000' # Neon Green
    else:
        color = '#008000' if val < 100 else 'red'
        
    return f'color: {color}; font-weight: bold'

def render_summary_table(df_rev, df_spent):
    st.subheader("Category Breakdown")
    
    # These can be the same widgets used for the chart to keep them in sync
    col1, col2 = st.columns(2)
    with col1:
        data_type = st.radio("View Table:", ["Revenues", "Spents"], key="table_type", horizontal=True)
    with col2:
        comparison_type = st.selectbox("Comparison criteria:", ["Previous Month", "Previous Year"], key="table_comp")

    target_df = df_rev if data_type == "Revenues" else df_spent
    table_data, comp_col = get_comparison_table(target_df, data_type, comparison_type)

    styled_df = table_data.style.map(
        lambda val: style_diff(val, data_type), 
        subset=['Diff']
    )
    # Formatting the display
    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Current Month": st.column_config.NumberColumn("Current Month", format="R$ %d"),
            comp_col: st.column_config.NumberColumn(comp_col, format="R$ %d"),
            "Diff": st.column_config.NumberColumn("Diff (%)", format="%.0f%%"),
        }
    )


def get_aggrid_matrix_data(df, data_type, comparison_type, start_date, end_date):
    # 1. Column Mapping
    cat_col = "category" if data_type == "Spents" else "receita"
    
    # 2. Define Periods
    curr_start, curr_end = pd.to_datetime(start_date), pd.to_datetime(end_date)
    
    if comparison_type == "Previous Month":
        prev_start = curr_start - pd.DateOffset(months=1)
        prev_end = curr_end - pd.DateOffset(months=1)
    else:
        prev_start = curr_start - pd.DateOffset(years=1)
        prev_end = curr_end - pd.DateOffset(years=1)

    # 3. Create Filtered Slices
    df_curr = df[(df["data"] >= curr_start) & (df["data"] <= curr_end)]
    df_prev = df[(df["data"] >= prev_start) & (df["data"] <= prev_end)]

    # 4. Group both by [Category, Description]
    curr_grouped = df_curr.groupby([cat_col, "descricao"])["valor"].sum().reset_index()
    curr_grouped.columns = ["Category", "Description", "Current"]

    prev_grouped = df_prev.groupby([cat_col, "descricao"])["valor"].sum().reset_index()
    prev_grouped.columns = ["Category", "Description", "Previous"]

    # 5. Merge and calculate Diff at the leaf level
    matrix_df = pd.merge(curr_grouped, prev_grouped, on=["Category", "Description"], how="outer").fillna(0)
    
    # This column is for display at the leaf level
    matrix_df["Diff %"] = (matrix_df["Current"] / matrix_df["Previous"]) * 100
    # Replace infinity (division by zero) with 0 or 100
    matrix_df["Diff %"] = matrix_df["Diff %"].replace([float('inf'), -float('inf')], 0).fillna(0)

    return matrix_df

def render_powerbi_matrix(df_rev, df_spent):
    st.subheader("Interactive Analysis Matrix")
    
    # Inputs
    col1, col2 = st.columns(2)
    with col1:
        data_type = st.radio("Metric:", ["Revenues", "Spents"], horizontal=True, key="matrix_type")
    with col2:
        comp_type = st.selectbox("Compare vs:", ["Previous Month", "Previous Year"], key="matrix_comp")

    target_df = df_rev if data_type == "Revenues" else df_spent
    
    end_date = date.today()
    start_date = today.replace(day=1)

    # Get filtered & processed data
    grid_data = get_aggrid_matrix_data(target_df, data_type, comp_type, start_date, end_date)

    gb = GridOptionsBuilder.from_dataframe(grid_data)

    # 1. Configura as colunas de dados normalmente (sem esconder ainda)
    gb.configure_column("Current", aggFunc="sum", headerName="Spents",
                        valueFormatter="x.toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'})")
    gb.configure_column("Previous", aggFunc="sum", headerName="Previous Month",
                        valueFormatter="x.toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'})")

    # 2. Ativa o Agrupamento e define o que esconder
    # Para funcionar como o Power BI, agrupamos pela Categoria
    gb.configure_column("Category", rowGroup=True, hide=False) 
    gb.configure_column("Description", hide=True) # Mantenha a descrição visível para ser o "filho"

    # 3. O Pulo do Gato: Configurar o comportamento do Grupo
    gb.configure_grid_options(
        # 'groupDefaultExpanded': 0 faz começar fechado como no BI
        groupDefaultExpanded=0,
        # 'groupDisplayType': 'groupRows' ou 'singleColumn'
        groupDisplayType='singleColumn', 
        autoGroupColumnDef={
            "headerName": "Category",
            "minWidth": 250,
            "cellRendererParams": {
                "suppressCount": True, # Remove o (4) ao lado do nome
                "innerRenderer": JsCode("""
                    function(params) {
                        return params.value;
                    }
                """)
            }
        },
        # Garante que os totais apareçam na linha do pai
        suppressAggFuncInHeader=True 
    )
        
    # --- Custom Logic for Diff % (Average of children or recalculate at group level) ---
    # In AgGrid, for percentages in groups, it's best to use a Value Getter 
    # so the Total row calculates (Total Curr / Total Prev) instead of summing percentages.
    
    diff_jscode = JsCode(f"""
    function(params) {{
        // 1. Identifica se estamos em uma linha de Grupo (Categoria) ou Detalhe (Descrição)
        let isGroup = params.node.group;
        let curr = isGroup ? params.node.aggData.Current : params.data.Current;
        let prev = isGroup ? params.node.aggData.Previous : params.data.Previous;

        // 2. Lógica de exibição estilo Power BI:
        // Se for detalhe e um dos valores for zero, o BI geralmente esconde o Diff 
        // para não poluir, focando na variação do GRUPO.
        if (!isGroup) {{
            if (curr === 0 || prev === 0) return ""; 
        }}

        // 3. Cálculo da variação (Usando a lógica de Proporção 106% da sua imagem)
        if (prev === 0) return "0%";
        let pct = (curr / prev) * 100;

        return pct.toFixed(0) + "%";
    }}
    """)

    color_jscode = JsCode(f"""
    function(params) {{
        let curr = params.data ? params.data.Current : params.node.aggData.Current;
        let prev = params.data ? params.data.Previous : params.node.aggData.Previous;
        let isRev = "{data_type}" === "Revenues";
        
        // Calcula a variação
        let pct = (prev === 0) ? (curr > 0 ? 100 : 0) : ((curr / prev) - 1) * 100;
        
        if (isRev) {{
            // Receita: Aumentar é bom (verde), diminuir é ruim (vermelho)
            return (pct >= 0) ? {{'color': '#008000', 'font-weight': 'bold'}} : {{'color': '#FF4B4B', 'font-weight': 'bold'}};
        }} else {{
            // Despesa: Aumentar é ruim (vermelho), diminuir é bom (verde)
            // Se curr é 0 e prev > 0, pct será -100 (Verde)
            return (pct <= 0) ? {{'color': '#008000', 'font-weight': 'bold'}} : {{'color': '#FF4B4B', 'font-weight': 'bold'}};
        }}
    }}
    """)

    gb.configure_column("Current", aggFunc="sum", headerName="Spents",
                    valueFormatter="x.toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'})")

    gb.configure_column("Previous", aggFunc="sum", headerName="Previous Month",
                        valueFormatter="x.toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'})")

    # Aplicamos o Value Getter novo na coluna Diff
    gb.configure_column("Diff %", valueGetter=diff_jscode, cellStyle=color_jscode)    

    # --- Grid UI Options ---
    gb.configure_grid_options(
        groupDefaultExpanded=0,
        animateRows=True,
        enableCellTextSelection=True,
        suppressAggFuncInHeader=True
    )
    
    gridOptions = gb.build()

    st.markdown("""
    <style>
    /* Target the specific AgGrid theme parameter variable you found */
    :where(.ag-theme-alpine-dark, .ag-theme-params-1) {
        --ag-background-color: rgba(0,0,0,0) !important;
        --ag-header-background-color: rgba(30,30,30,0.5) !important;
        --ag-control-panel-background-color: rgba(0,0,0,0) !important;
    }

    /* Target the root wrapper and all internal containers */
    .ag-root-wrapper, .ag-root, .ag-body-viewport, .ag-row {
        background-color: transparent !important;
        background: transparent !important;
    }

    /* Remove the default border if you want a floating look */
    .ag-root-wrapper {
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # 1. Define your colors as variables to keep it clean
    BG_COLOR = "#0e1117"  # Streamlit Dark Background
    TEXT_COLOR = "#FFFFFF"

    # 2. In your AgGrid call, use 'alpine-dark' and override via custom_css
    AgGrid(
        grid_data,
        gridOptions=gridOptions,
        allow_unsafe_jscode=True, 
        theme='alpine', # Use a base theme
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
        height=500,
        custom_css={
            # This targets the internal AG Grid variables directly
            ".ag-theme-alpine": {
                "--ag-background-color": f"{BG_COLOR} !important",
                "--ag-header-background-color": "#1e1e1e !important",
                "--ag-odd-row-background-color": f"{BG_COLOR} !important",
                "--ag-row-border-color": "transparent !important",
                "--ag-foreground-color": f"{TEXT_COLOR} !important",
                "--ag-header-foreground-color": f"{TEXT_COLOR} !important",
                "--ag-font-size": "15px !important"
            },
            ".ag-root-wrapper": {
                "border": "none !important",
                "background-color": f"{BG_COLOR} !important"
            }
        }
    )