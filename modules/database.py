import streamlit as st
from services.db_connection import *
import pandas as pd

# --- PARCELAS (compras parceladas) ---
def build_parcela_rows(base_date, category, desc, total_value, num_parcelas, intervalo_meses=1):
    """Divide o valor total em N linhas mensais.

    - O calculo e feito em centavos (int) e o resto vai para a ULTIMA parcela,
      para que a soma das parcelas seja exatamente o valor total.
    - A 1a parcela cai na data informada e as demais a cada `intervalo_meses`.
    """
    total_cents = round(float(total_value) * 100)
    base_cents, resto = divmod(total_cents, num_parcelas)
    base = pd.Timestamp(base_date)

    rows = []
    for i in range(1, num_parcelas + 1):
        cents = base_cents + (resto if i == num_parcelas else 0)
        venc = (base + pd.DateOffset(months=(i - 1) * intervalo_meses)).date()
        rows.append({
            "data": venc.isoformat(),
            "despesas": category,
            "descricao": f"{desc} {i}/{num_parcelas}",
            "valor": round(cents / 100, 2),
        })
    return rows

# --- HELPER LOGIC ---
def show_table_view(table_name, fetch_func):
    """Renders the table and handles row selection for Edit/Delete"""
    view_key = f"view_{table_name}"
    if view_key not in st.session_state:
        st.session_state[view_key] = "table"

    if st.session_state[view_key] == "form":
        if table_name == "investments":
            render_investment_form()
        else:
            render_simple_form(table_name)
        return

    flash = st.session_state.pop(f"flash_{table_name}", None)
    if flash:
        st.success(flash)

    data = fetch_func()
    st.subheader(f"{table_name.capitalize()}")
    
    if st.button(f"Add {table_name[:-1]}", key=f"new_{table_name}", type="secondary"):
        st.session_state.editing_row = None
        st.session_state.pop(f"parcela_toggle_{table_name}", None)
        st.session_state[view_key] = "form"
        st.rerun()
    

    if data:
        df = pd.DataFrame(data)

        # df = df.sort_values("data", ascending=False)

        money_config = st.column_config.NumberColumn(
            format="R$ %.2f"
        )
        
        # Apply config to relevant columns
        cols_to_format = ["valor", "preco_unit"]
        config = {col: money_config for col in cols_to_format if col in df.columns}
        
        event = st.dataframe(df, use_container_width=True, hide_index=True,
                             on_select="rerun", selection_mode="single-row", column_config=config)

        if event.selection.rows:
            selected_data = df.iloc[event.selection.rows[0]]
            col1, col2, _ = st.columns([1, 1, 11])
            with col1:
                if st.button("✏️ Edit", key=f"edit_btn_{table_name}"):
                    st.session_state.editing_row = selected_data.to_dict()
                    st.session_state[view_key] = "form"
                    st.rerun()
            with col2:
                if st.button("🗑️ Delete", type="primary", key=f"del_btn_{table_name}"):
                    # Generic delete call using the table name
                    get_supabase().table(table_name).delete().eq("id", selected_data["id"]).execute()
                    st.success("Deleted!")
                    st.rerun()
    else:
        st.info(f"No {table_name} data found.")

# --- FORM 1: Simple (Revenues & Spents) ---
def render_simple_form(table_name):
    edit_data = st.session_state.get("editing_row")
    is_edit = edit_data is not None
    
    # Map DB column names from your db_connection.py
    # Revenues uses "receita" while Spents uses "despesas"
    cat_col = "receita" if table_name == "revenues" else "despesas"
    categories = [
        "Salário", 
        "Aulas", 
        "Caju", 
        "Dividendos", 
        "Rendimentos", 
        "Extra", 
        "Vendas", 
        "Freela", 
        "Outros"] if table_name == "revenues" else [
                                                "Alimentação", 
                                                "Mobilidade",
                                                "Moradia",
                                                "Operadora",
                                                "Cachorros",
                                                "Igreja",
                                                "Faculdade",
                                                "Gastos Carro",
                                                "Entretenimento",
                                                "Assinaturas",
                                                "Cursos",
                                                "Financiamentos",
                                                "Saúde",
                                                "Lazer",
                                                "Roupas",
                                                "Presentes",
                                                "Izy",
                                                "Outros"]

    # with st.form("simple_form"):
    # O checkbox fica FORA do form: widgets dentro de um st.form nao disparam rerun,
    # entao os campos de parcelas so apareceriam depois de clicar em Save.
    is_parcelada = False
    if table_name == "spents" and not is_edit:
        is_parcelada = st.checkbox("Compra parcelada?", key=f"parcela_toggle_{table_name}")

    with st.form(key=f"form_{table_name}"):
        st.write(f"### {"Edit" if is_edit else "New"} {table_name[:-1]}")
        date = st.date_input("Date", value=pd.to_datetime(edit_data["data"]) if is_edit else None)
        category = st.selectbox("Category", categories, 
                                index=categories.index(edit_data[cat_col]) if is_edit else 0)
        desc = st.text_input("Description", value=edit_data["descricao"] if is_edit else "")
        val = st.number_input("Value (total da compra)" if is_parcelada else "Value",
                              value=float(edit_data["valor"]) if is_edit else 0.0)

        num_parcelas = 0
        intervalo = 1
        if is_parcelada:
            num_parcelas = st.number_input("Número de parcelas", min_value=2, max_value=48, value=2, step=1)
            intervalo = st.number_input("Intervalo (meses)", min_value=1, max_value=12, value=1, step=1)
            st.caption("O valor informado é o total da compra e será dividido entre as parcelas. "
                       "A 1ª parcela cai na data informada.")

        # Submit button inside the form
        if st.form_submit_button("Save"):
            if is_parcelada:
                if date is None:
                    st.error("Selecione a data da 1ª parcela.")
                elif val <= 0:
                    st.error("O valor total da compra deve ser maior que zero.")
                elif not desc.strip():
                    st.error("Informe uma descrição (ex: Mecânico).")
                else:
                    rows = build_parcela_rows(date, category, desc.strip(), val,
                                              int(num_parcelas), int(intervalo))
                    created = save_spents_bulk_to_supabase(rows)
                    st.session_state[f"flash_{table_name}"] = (
                        f"{len(rows)} parcelas criadas: {len(rows)}x de R$ {rows[0]['valor']:.2f} "
                        f"(total R$ {val:.2f})."
                    )
                    st.session_state[f"view_{table_name}"] = "table"
                    st.rerun()
            else:
                payload = {"data": str(date), cat_col: category, "descricao": desc, "valor": val}
                if is_edit:
                    get_supabase().table(table_name).update(payload).eq("id", edit_data["id"]).execute()
                else:
                    get_supabase().table(table_name).insert(payload).execute()
                
                st.session_state[f"view_{table_name}"] = "table"
                st.rerun()

    if st.button("Cancel", type="primary", key=f"cancel_{table_name}"):
        st.session_state[f"view_{table_name}"] = "table"
        st.rerun()

# --- FORM 2: Complex (Investments) ---
def render_investment_form():
    edit_data = st.session_state.get("editing_row")
    is_edit = edit_data is not None

    investment_types = [
    "Tesouro Direto", "CDB", "LIC", "LCA", "Fundos", "FIIs", 
    "ETFs", "Ações", "Outros", "Cripto", 
    "Reserva de Emergência", "Internacional"
    ]

    institution_options = [
        "Inter", 
        "Banco do Brasil", 
        "Caixa Econômica",
        "Bradesco",
        "Itaú",
        "Santander", 
        "Nubank", 
        "Sofisa",
        "C6 Bank", 
        "XP Investimentos", 
        "Rico",         
        "BTG Pactual",         
        "NuInvest", 
        "Banco Original", 
        "Inter", 
        "Mercado Pago", 
        "Outros"]
    
    origin_options = [
        "Salário",
        "Reserva Emerg.",
        "Rendimentos"
    ]

    transaction_options = [
        "COMPRA",
        "VENDA"
    ]

    with st.form("invest_form"):
        st.write("### Investment Details")
        col1, col2 = st.columns(2)
        with col1:
        # Logic to find the index of the existing value if editing
            default_index = 0
            if is_edit and edit_data.get("tipo") in investment_types:
                default_index = investment_types.index(edit_data["tipo"])
            
            tipo = st.selectbox(
                "Select the type", 
                options=investment_types, 
                index=default_index
            )
            ticker = st.text_input("Ticker", value=edit_data["ticker"] if is_edit else "")
            quant = st.number_input("Quantidade", value=float(edit_data["quantidade"]) if is_edit else 0.0)

            col1_1, col1_2 = st.columns(2)
            with col1_1:
                data_inv = st.date_input("Data Transação", value=pd.to_datetime(edit_data["data_transacao"]) if is_edit else None)
            with col1_2:
                data_venc = st.date_input("Data Vencimento", value=pd.to_datetime(edit_data["data_vencimento"]) if is_edit else None)
        with col2:
            default_index = 0
            if is_edit and edit_data.get("Instituicao") in investment_types:
                default_index = investment_types.index(edit_data["instituicao"])

            inst = st.selectbox(
                "Institution", 
                options=institution_options, 
                index=default_index
            )

            origin = st.selectbox(
                "Origin",
                options=origin_options,
                index=0

            )
            col3, col4 = st.columns(2)
            with col3:                    
                valor_unit = st.number_input("Unit Price", value=float(edit_data["preco_unit"]) if is_edit else 0.0)
            with col4:
                valor = quant * valor_unit
                # valor = st.number_input("Valor Total", value=total, format="%.2f")

            # col5, col6 = st.columns(2)
            # with col5:
            #     ativo = st.checkbox("Ativo", value=edit_data["ativo"] if is_edit else True)
            # with col6:
            #     aporte = st.checkbox("Aporte", value=edit_data["aporte"] if is_edit else True)

            col5, col6 = st.columns(2)

            with col5:
                # Lógica para pegar o valor padrão ao editar
                default_transaction_index = 0
                if is_edit and edit_data.get("tipo_transacao") in transaction_options:
                    default_transaction_index = transaction_options.index(edit_data["tipo_transacao"])

                # Componente direto, sem with, corrigindo select_box para selectbox
                transaction_type = st.selectbox(
                    "Tipo de Transação", 
                    options=transaction_options,
                    index=default_transaction_index
                )

            with col6:
                aporte = st.checkbox("Aporte", value=edit_data["aporte"] if is_edit else True)

        if st.form_submit_button("Save Investment"):
            # Payload matching your detailed 11-column structure
            # Create the payload without the list brackets
            payload = {
                "tipo": tipo, 
                "instituicao": inst, 
                "ticker": ticker, 
                "aporte": aporte,
                "quantidade": quant, 
                "preco_unit": valor_unit, 
                "valor": valor, 
                # "ativo": ativo,
                "data_transacao": str(data_inv), 
                "tipo_transacao": transaction_type,
                # Logic: if data_venc exists, convert to string; otherwise, use None
                "data_vencimento": str(data_venc) if data_venc else None, 
                "origem": origin
            }
            if is_edit:
                get_supabase().table("investments").update(payload).eq("id", edit_data["id"]).execute()
            else:
                get_supabase().table("investments").insert(payload).execute()
            st.session_state["view_investments"] = "table"
            st.rerun()

    if st.button("Cancel", type="primary"):
        st.session_state["view_investments"] = "table"
        st.rerun()

# --- PUBLIC FUNCTIONS ---
def show_revenue_table(): show_table_view("revenues", get_revenues)
def show_spent_table(): show_table_view("spents", get_spents)
def show_investments_table(): show_table_view("investments", get_investments)