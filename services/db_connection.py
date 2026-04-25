from supabase import create_client, Client
import streamlit as st

def get_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)
        
# region revenues     
def get_revenues():
    response = get_supabase().table("revenues")\
                .select("*").order("id", desc=True).execute()
    return response.data

def save_revenue_to_supabase(date, revenue, description, value):
    # Supabase .insert() needs a dictionary: {"column_name": value}
    # Ensure these keys match your Supabase column names exactly!
    data = {
        "data": str(date), 
        "receita": revenue, 
        "descricao": description, 
        "valor": value
    }
    response = get_supabase().table("revenues").insert(data).execute()
    return response.data

def update_revenue_to_supabase(date, revenue, description, value):
    # Supabase .insert() needs a dictionary: {"column_name": value}
    # Ensure these keys match your Supabase column names exactly!
    data = {
        "data": str(date), 
        "receita": revenue, 
        "descricao": description, 
        "valor": value
    }
    response = get_supabase().table("revenues").update(data).execute()
    return response.data

def delete_revenue(row_id):
    get_supabase().table("revenues").delete().eq("id", row_id).execute()

#endregion revenues


# region spents
def get_spents():
    response = get_supabase().table("spents")\
                .select("*").order("id", desc=True)\
                .limit(2000).execute()
    return response.data

def save_spents_to_supabase(date, spent, description, value):
    # Supabase .insert() needs a dictionary: {"column_name": value}
    # Ensure these keys match your Supabase column names exactly!
    data = {
        "data": str(date), 
        "despesas": spent, 
        "descricao": description, 
        "valor": value
    }
    response = get_supabase().table("spents").insert(data).execute()
    return response.data

def update_revenue_to_supabase(date, spent, description, value):
    # Supabase .insert() needs a dictionary: {"column_name": value}
    # Ensure these keys match your Supabase column names exactly!
    data = {
        "data": str(date), 
        "despesas": spent, 
        "descricao": description, 
        "valor": value
    }
    response = get_supabase().table("spents").update(data).execute()
    return response.data

def delete_revenue(row_id):
    get_supabase().table("spents").delete().eq("id", row_id).execute()

# endregion spents


# region investments
def get_investments():
    response = get_supabase().table("investments").select("*").execute()
    return response.data

def save_revenue_to_supabase(investiment_type:str, 
                               institution:str, 
                               ticker:str,
                               contribution:str,
                               amount:float,
                               unit_price:float,
                               value:float,                               
                               investment_date,
                               expiration_date,
                               origin,
                               active:bool):
    # Supabase .insert() needs a dictionary: {"column_name": value}
    # Ensure these keys match your Supabase column names exactly!
    data = {
        "tipo": investiment_type, 
        "instituicao": institution, 
        "ticker": ticker, 
        "aporte": contribution,
        "quantidade": amount, 
        "preco_unit": unit_price, 
        "valor": value, 
        "data_investimento": investment_date,
        "data_vencimento": expiration_date,
        "origem": origin,
        "ativo": active,
    }
    response = get_supabase().table("investments").insert(data).execute()
    return response.data

def update_revenue_to_supabase(investiment_type:str, 
                               institution:str, 
                               ticker:str,
                               contribution:str,
                               amount:int,
                               unit_price:float,
                               value:float,
                               investment_date,
                               expiration_date,
                               origin,
                               active:bool):
    # Supabase .insert() needs a dictionary: {"column_name": value}
    # Ensure these keys match your Supabase column names exactly!
    data = {
        "tipo": investiment_type, 
        "instituicao": institution, 
        "ticker": ticker, 
        "aporte": contribution,
        "quantidade": amount, 
        "preco_unit": unit_price, 
        "valor": value, 
        "data_investimento": investment_date,
        "data_vencimento": expiration_date,
        "origem": origin,
        "ativo": active,
    }
    response = get_supabase().table("investments").update(data).execute()
    return response.data

def delete_revenue(row_id):
    get_supabase().table("investments").delete().eq("id", row_id).execute()

# endregion investments