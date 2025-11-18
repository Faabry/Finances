from .db import get_conn

# region Revenues
def insert_transaction(data):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO public.Revenues (data,	receita, descricao, valor)
        Values (%s, %s, %s, %s)
        """,
        (data["data"], data["receita"], data["descricao"], data["valor"])
    )
    conn.commit()
    cur.close()
    conn.close()

def update_transaction(tid, data):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        UPdate public.Revenues
        SET data=%s, receita=%s, descricao=%s, valor=%s
        WHERE id=%s
        """,
        (data["data"], data["receita"], data["descricao"], data["valor"], tid)
    )
    conn.commit()
    cur.close()
    conn.close()

def delete_transaction(tid):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM public.Revenues WHERE id=%s", (tid,))
    conn.commit()
    cur.close()
    conn.close()

VALID_COLUMNS = {
    'data': 'data',
    'receita': 'Receita',
    'descricao': 'Descricao',
    'valor': 'Valor'
}

def list_transactions(sort_by='data', sort_order='asc'):
    conn = get_conn()
    cur = conn.cursor()
    
    # 1. Validate and sanitize the sort parameters
    
    # Default column is 'id' or 'data' if the provided sort_by is invalid
    column_name = VALID_COLUMNS.get(sort_by.lower(), 'data')
    
    # Validate sort order (must be 'ASC' or 'DESC')
    order = 'DESC' if sort_order.lower() == 'desc' else 'ASC'

    # 2. Construct the SQL query with the ORDER BY clause
    # NOTE: Since the column name is validated against a safe dictionary (VALID_COLUMNS) 
    # before being inserted, this method is safe against SQL injection in this context.
    
    sql_query = f"""
        SELECT 
            id, 
            data, 
            Receita, 
            Descricao, 
            Valor 
        FROM 
            public.Revenues 
        ORDER BY 
            {column_name} {order}
    """

    # 3. Execute the query
    cur.execute(sql_query)
    rows = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return rows

def get_transaction_by_id(tid):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, data, receita, descricao, valor 
        FROM public.Revenues 
        WHERE id=%s
    """, (tid,))

    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return None

    return {
        "data": row[1],
        "receita": row[2],
        "descricao": row[3],
        "valor": row[4],
    }
# endregion Revenues

# region Spents
def insert_spent(data):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO public.Spents (despesas, descricao, valor, data)
        VALUES (%s, %s, %s, %s)
        """,
        (data["despesas"], data["descricao"], data["valor"], data["data"])
    )
    conn.commit()
    cur.close()
    conn.close()


def update_spent(sid, data):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE public.Spents
        SET despesas=%s, descricao=%s, valor=%s, data=%s
        WHERE id=%s
        """,
        (data["despesas"], data["descricao"], data["valor"], data["data"], sid)
    )
    conn.commit()
    cur.close()
    conn.close()


def delete_spent(sid):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM public.Spents WHERE id=%s", (sid,))
    conn.commit()
    cur.close()
    conn.close()


VALID_COLUMNS_SPENTS = {
    'data': 'data',
    'despesas': 'despesas',
    'descricao': 'descricao',
    'valor': 'valor',
    'id': 'id'
}


def list_spents(sort_by='data', sort_order='asc'):
    conn = get_conn()
    cur = conn.cursor()

    column_name = VALID_COLUMNS_SPENTS.get(sort_by.lower(), 'data')
    order = 'DESC' if sort_order.lower() == 'desc' else 'ASC'

    sql = f"""
        SELECT id, despesas, descricao, valor, data
        FROM public.Spents
        ORDER BY {column_name} {order}
    """

    cur.execute(sql)
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows


def get_spent_by_id(sid):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, despesas, descricao, valor, data
        FROM public.Spents
        WHERE id=%s
    """, (sid,))

    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return None

    return {
        "despesas": row[1],
        "descricao": row[2],
        "valor": row[3],
        "data": row[4],
    }
# endregion Spents

# region Investments
def insert_investment(data):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO public.Investments 
            (tipo, instituicao, ticker, aporte, quantidade, preco_unit,
             valor, data_investimento, data_vencimento, origem, ativo)
        VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            data["tipo"], data["instituicao"], data["ticker"],
            data["aporte"], data["quantidade"], data["preco_unit"],
            data["valor"], data["data_investimento"], data["data_vencimento"],
            data["origem"], data["ativo"]
        )
    )
    conn.commit()
    cur.close()
    conn.close()


def update_investment(iid, data):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE public.Investments
        SET tipo=%s, instituicao=%s, ticker=%s, aporte=%s,
            quantidade=%s, preco_unit=%s, valor=%s,
            data_investimento=%s, data_vencimento=%s, origem=%s, ativo=%s
        WHERE id=%s
        """,
        (
            data["tipo"], data["instituicao"], data["ticker"],
            data["aporte"], data["quantidade"], data["preco_unit"],
            data["valor"], data["data_investimento"], data["data_vencimento"],
            data["origem"], data["ativo"], iid
        )
    )
    conn.commit()
    cur.close()
    conn.close()


def delete_investment(iid):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM public.Investments WHERE id=%s", (iid,))
    conn.commit()
    cur.close()
    conn.close()


VALID_COLUMNS_INVESTMENTS = {
    'tipo': 'tipo',
    'instituicao': 'instituicao',
    'ticker': 'ticker',
    'aporte': 'aporte',
    'quantidade': 'quantidade',
    'preco_unit': 'preco_unitario_medio',
    'valor': 'valor',
    'data_investimento': 'data_investimento',
    'data_vencimento': 'data_vencimento',
    'origem': 'origem',
    'ativo': 'ativo',
    'id': 'id'
}


def list_investments(sort_by='data_investimento', sort_order='asc'):
    conn = get_conn()
    cur = conn.cursor()

    column_name = VALID_COLUMNS_INVESTMENTS.get(sort_by.lower(), 'data_investimento')
    order = 'DESC' if sort_order.lower() == 'desc' else 'ASC'

    sql = f"""
        SELECT 
            id, tipo, instituicao, ticker, aporte, quantidade, 
            preco_unit, valor, data_investimento, 
            data_vencimento, origem, ativo
        FROM public.Investments
        ORDER BY {column_name} {order}
    """

    cur.execute(sql)
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows


def get_investment_by_id(iid):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            id, tipo, instituicao, ticker, aporte, quantidade,
            preco_unit, valor, data_investimento, 
            data_vencimento, origem, ativo
        FROM public.Investments
        WHERE id=%s
    """, (iid,))

    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return None

    return {
        "tipo": row[1],
        "instituicao": row[2],
        "ticker": row[3],
        "aporte": row[4],
        "quantidade": row[5],
        "preco_unit": row[6],
        "valor": row[7],
        "data_investimento": row[8],
        "data_vencimento": row[9],
        "origem": row[10],
        "ativo": row[11],
    }
# endregion Investments