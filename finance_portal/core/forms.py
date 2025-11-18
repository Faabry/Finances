# forms.py

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
    ('Cursos', 'Cursos'),
    ('Financiamento', 'Financiamento'),
    ('Lazer', 'Lazer'),
    ('Faturas', 'Faturas'),
    ('Advogado', 'Advogado'),
    ('Operadora', 'Operadora'),
    ('Mobilidade', 'Mobilidade'),
    ('Alimentação', 'Alimentação'),
    ('Outros', 'Outros'),
    ('Moradia', 'Moradia'),
    ('Cachorros', 'Cachorros'),
    ('Gastos Carro', 'Gastos Carro'),
    ('Gastos Moto', 'Gastos Moto'),
    ('Saúde', 'Saúde'),
    ('Viajem', 'Viajem'),
    ('Presentes', 'Presentes'),
    ('Roupas', 'Roupas'),
    ('Eletrônicos', 'Eletrônicos'),
    ('Faculdade', 'Faculdade'),
    ('Igreja', 'Igreja'),
    ('CNH', 'CNH'),
    ('Cosméticos', 'Cosméticos'),
    ('Bike', 'Bike'),
    ('igreja', 'igreja'),
    ('outros', 'outros'),
    ('Farmácia', 'Farmácia'),
    ('Psicologo', 'Psicologo'),
    ('Entretenimento', 'Entretenimento'),
    ('Assinaturas', 'Assinaturas'),
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
            attrs={'class': 'form-select'} # Use 'form-select' for Bootstrap 5 dropdowns
        )
    )
    descricao = forms.CharField(max_length=255)
    valor = forms.DecimalField(max_digits=10, decimal_places=2)
    data = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

class InvestmentForm(forms.Form):
    tipo = forms.CharField(max_length=255)
    instituicao = forms.CharField(max_length=255)
    ticker = forms.CharField(max_length=50)
    aporte = forms.BooleanField(required=False)
    quantidade = forms.DecimalField(max_digits=12, decimal_places=4)
    preco_unit = forms.DecimalField(max_digits=12, decimal_places=4)
    valor = forms.DecimalField(max_digits=12, decimal_places=2)
    data_investimento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    data_vencimento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    origem = forms.CharField(max_length=255)
    ativo = forms.BooleanField(required=False)