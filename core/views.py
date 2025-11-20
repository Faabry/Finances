from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .forms import TransactionForm, SpentForm, InvestmentForm
from .repository import (
    insert_transaction, update_transaction, delete_transaction, list_transactions, get_transaction_by_id,
    insert_spent, update_spent, delete_spent as del_spent, list_spents, get_spent_by_id,
    insert_investment, update_investment, delete_investment as del_investment, list_investments, get_investment_by_id,
    list_investments_active
)

# region Revenues
def index(request):
    sort_by = request.GET.get('sort', 'id')
    sort_order = request.GET.get('order', 'asc')

    all_transactions = list_transactions(sort_by=sort_by, sort_order=sort_order)

    COLUMN_MAP_LIST = ['data', 'receita', 'descricao', 'valor']

    paginator = Paginator(all_transactions, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'transactions': page_obj,
        'current_sort': sort_by,
        'current_order': sort_order,
        'column_list': COLUMN_MAP_LIST,
        'page_title': 'Revenues',
        'entity': 'revenue',
    }
    
    return render(request, "index.html", context)

def create_revenue(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            insert_transaction(form.cleaned_data)
            return redirect("index")
    else:
        form = TransactionForm()
    return render(request, "form.html", {"form": form, "is_edit": False, "page_title": "New Revenue"})

def edit_revenue(request, tid):
    try:
        transaction_data = get_transaction_by_id(tid)
    except Exception:
        return redirect("index")
    
    if request.method == "POST":
        form = TransactionForm(request.POST, initial=transaction_data)
        if form.is_valid():
            update_transaction(tid, form.cleaned_data)
            return redirect("index")
    else:
        form = TransactionForm(initial=transaction_data)
        
    return render(request, "form.html", {"form": form, "is_edit": True, "tid": tid, "page_title": "Edit Revenue"})

def delete_revenue(request, tid):
    delete_transaction(tid)
    return redirect("index")
# endregion Revenues

# region Spents
def spents_list(request):
    sort_by = request.GET.get('sort', 'data')
    sort_order = request.GET.get('order', 'asc')

    all_spents = list_spents(sort_by=sort_by, sort_order=sort_order)

    COLUMN_MAP_LIST = ['data', 'despesas', 'descricao', 'valor']

    paginator = Paginator(all_spents, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'transactions': page_obj,  # pode renomear para 'spents' se quiser trocar no template
        'current_sort': sort_by,
        'current_order': sort_order,
        'column_list': COLUMN_MAP_LIST,
        'page_title': 'Spents',
        'entity': 'spents',
    }
    
    return render(request, "spents.html", context)  # pode reutilizar index.html se parametrizar

def create_spent(request):
    if request.method == "POST":
        form = SpentForm(request.POST)
        if form.is_valid():
            insert_spent(form.cleaned_data)
            return redirect("spents_list")
    else:
        form = SpentForm()
    return render(request, "form_spents.html", {"form": form, "is_edit": False, "page_title": "New Spent"})

def edit_spent(request, sid):
    try:
        spent_data = get_spent_by_id(sid)
    except Exception:
        return redirect("spents_list")
    
    if request.method == "POST":
        form = SpentForm(request.POST, initial=spent_data)
        if form.is_valid():
            update_spent(sid, form.cleaned_data)
            return redirect("spents_list")
    else:
        form = SpentForm(initial=spent_data)
        
    return render(request, "form_spents.html", {"form": form, "is_edit": True, "sid": sid, "page_title": "Edit Spent"})

def delete_spent(request, sid):
    del_spent(sid)
    return redirect("spents_list")
# endregion Spents

# region Investments
def investments_list(request):
    # --- Filter governance ---
    active_param = request.GET.get('active', '').lower()

    if active_param == 'true':
        active = True
    elif active_param == 'false':
        active = False
    else:
        active = None

    # --- Sorting governance ---
    sort_by = request.GET.get('sort', 'data_investimento')
    sort_order = request.GET.get('order', 'asc')

    # --- Query execution with filtering + sorting ---
    all_investments = list_investments_active(
        active=active,
        sort_by=sort_by,
        sort_order=sort_order
    )

    COLUMN_MAP_LIST = [
        'data_investimento', 'tipo', 'instituicao', 'ticker',
        'aporte', 'quantidade', 'preco_unitario_medio', 'valor',
        'data_vencimento', 'origem', 'ativo'
    ]

    # --- Pagination governance ---
    paginator = Paginator(all_investments, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # --- Context ---
    context = {
        'transactions': page_obj,      # aligns with your template
        'current_sort': sort_by,
        'current_order': sort_order,
        'current_active': active,      # NEW: required for <th> links
        'column_list': COLUMN_MAP_LIST,
        'page_title': 'Investments',
        'entity': 'investments',
    }

    return render(request, "investments.html", context)

def create_investment(request):
    if request.method == "POST":
        form = InvestmentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data["ativo"] = True  # hard set
            insert_investment(data)
            return redirect("investments_list")
    else:
        form = InvestmentForm()
    return render(request, "form_investments.html", {"form": form, "is_edit": False, "page_title": "New Investment"})

def edit_investment(request, iid):
    try:
        investment_data = get_investment_by_id(iid)
    except Exception:
        return redirect("investments_list")
    
    if request.method == "POST":
        form = InvestmentForm(request.POST, initial=investment_data)
        if form.is_valid():
            data = form.cleaned_data
            data["ativo"] = True  # hard set
            insert_investment(data)
            return redirect("investments_list")
    else:
        form = InvestmentForm(initial=investment_data)
        
    return render(request, "form_investments.html", {"form": form, "is_edit": True, "iid": iid, "page_title": "Edit Investment"})

def delete_investment(request, iid):
    del_investment(iid)
    return redirect("investments_list")
# endregion Investments

# region Dashboard
def dashboard(request):
    return render(request, "dashboard.html")
# endregion Dashboard
