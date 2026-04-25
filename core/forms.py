from django import forms

# Define the choices as a tuple of tuples: (value_stored_in_db, human_readable_label)
RECEITA_CHOICES = [
    ('', '--- Select Revenue Type ---'), # Optional empty choice    
    ('Salário', 'Salário'),
    ('Caju', 'Caju'), 
    ('Dividendos', 'Dividendos'),    
    ('Rendimentos', 'Rendimentos'),
    ('Extra', 'Extra'),
    ('Vendas', 'Vendas'), 
    ('Freelancer', 'Freelancer'),
    ('Aulas', 'Aulas'),         
    ('Restituicao', 'Restituição'), 
    ('Férias', 'Férias'),         
    ('FGTS', 'FGTS'),
    ('Seguro Desemprego', 'Seguro Desemprego'),
    ('Resgate', 'Resgate'),
    ('Décimo', 'Décimo'),
    ('Outros', 'Outros'),
]

class TransactionForm(forms.Form):
    data = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'} 
        )
    )
    
    # Key Change: Use a ChoiceField with the predefined choices
    receita = forms.ChoiceField(
        choices=RECEITA_CHOICES,
        widget=forms.Select(
            attrs={'class': 'form-select'} # Use 'form-select' for Bootstrap 5 dropdowns
        )
    )
    
    descricao = forms.CharField(max_length=255)
    valor = forms.DecimalField(max_digits=12, decimal_places=2)

SPENT_CHOICES = [
    ('', '--- Select Spent Type ---'),
    ('Alimentação', 'Alimentação'),
    ('Mobilidade', 'Mobilidade'), 
    ('Moradia', 'Moradia'),
    ('Operadora', 'Operadora'),
    ('Cachorros', 'Cachorros'),
    ('Igreja', 'Igreja'),
    ('Faculdade', 'Faculdade'),
    ('Gastos Carro', 'Gastos Carro'),
    ('Entretenimento', 'Entretenimento'),
    ('Assinaturas', 'Assinaturas'),
    ('Cursos', 'Cursos'),
    ('Financiamento', 'Financiamento'),
    ('Lazer', 'Lazer'),
    ('Faturas', 'Faturas'),
    ('Advogado', 'Advogado'),           
    ('Outros', 'Outros'),    
    ('Gastos Moto', 'Gastos Moto'),
    ('Saúde', 'Saúde'),
    ('Viajem', 'Viajem'),
    ('Presentes', 'Presentes'),
    ('Roupas', 'Roupas'),
    ('Eletrônicos', 'Eletrônicos'),    
    ('CNH', 'CNH'),
    ('Cosméticos', 'Cosméticos'),
    ('Bike', 'Bike'),
    ('igreja', 'igreja'),
    ('outros', 'outros'),
    ('Farmácia', 'Farmácia'),
    ('Psicologo', 'Psicologo'),    
    ('Cosméticos', 'Cosméticos'),
    ('Bebidas', 'Bebidas'),
    ('Impostos', 'Impostos'),
    ('Izy', 'Izy'),
    ('Milhas', 'Milhas')
]
class SpentForm(forms.Form):
    despesas = forms.ChoiceField(
        choices=SPENT_CHOICES,
        widget=forms.Select(
            attrs={'class': 'form-select'}
        )
    )
    descricao = forms.CharField(max_length=255)
    valor = forms.DecimalField(max_digits=10, decimal_places=2)
    data = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

INVESTMENT_TYPE_CHOICES = [
        ('', '--- Select Investment Type ---'),
        ('Tesouro Direto', 'Tesouro Direto'),
        ('LCI', 'LCI'),
        ('LCA', 'LCA'),
        ('Fundos', 'Fundos'),
        ('FIIs', 'FIIs'),
        ('ETF', 'ETF'),
        ('Ações', 'Ações'),
        ('Outros', 'Outros'),
        ('Cripto', 'Cripto'),
        ('Reserva Emergência', 'Reserva Emergência'),
        ('Internacional', 'Internacional')
    ]

INSTITUTION_CHOICES = [
        ('', '--- Select Institution ---'),
        ('Banco do Brasil', 'Banco do Brasil'),
        ('Caixa Econômica', 'Caixa Econômica'),
        ('Bradesco', 'Bradesco'),
        ('Itaú', 'Itaú'),
        ('Santander', 'Santander'),
        ('Nubank', 'Nubank'),
        ('Inter', 'Inter'),
        ('C6 Bank', 'C6 Bank'),
        ('XP Investimentos', 'XP Investimentos'),
        ('Rico', 'Rico'),
        ('Clear', 'Clear'),
        ('BTG Pactual', 'BTG Pactual'),
        ('Modalmais', 'Modalmais'),
        ('NuInvest', 'NuInvest'),
        ('Banco Original', 'Banco Original'),
        ('Nubank', 'Nubank'),
        ('Inter', 'Inter'),
        ('Mercado Pago', 'Mercado Pago'),
        ('Outros', 'Outros')
]


ORIGIN_CHOICES = [
    ('Salário', 'Salário'),
    ('Rendimentos', 'Rendimentos'),
    ('Reserva Emerg.', 'Reserva Emerg.')
]

class InvestmentForm(forms.Form):
    tipo = forms.ChoiceField(
        choices=INVESTMENT_TYPE_CHOICES,
        widget=forms.Select(
            attrs={'class': 'form-select'}
        )
    )
    instituicao = forms.ChoiceField(
        choices=INSTITUTION_CHOICES,
        widget=forms.Select(
            attrs={'class': 'form-select'}
        )
    )
    ticker = forms.CharField(max_length=50)
    aporte = forms.BooleanField(required=False)
    quantidade = forms.DecimalField(max_digits=12, decimal_places=4)
    preco_unit = forms.DecimalField(max_digits=12, decimal_places=4)
    valor = forms.DecimalField(max_digits=12, decimal_places=2)
    data_investimento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    data_vencimento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    origem = forms.ChoiceField(
        choices=ORIGIN_CHOICES,
        widget=forms.Select(
            attrs={'class': 'form-select'}
        )
    )
    ativo = forms.BooleanField(required=False)