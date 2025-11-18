
from django.urls import path
from . import views

urlpatterns = [
    # Revenues (já existente)
    # path('edit/<int:tid>/', views.edit_revenue, name='edit'),  
    # path('delete/<int:tid>/', views.delete_revenue, name='delete'),  
    path('', views.index, name='index'),
    path('revenue/create/', views.create_revenue, name='create_revenue'),
    path('revenue/<int:tid>/edit/', views.edit_revenue, name='edit_revenue'),
    path('revenue/<int:tid>/delete/', views.delete_revenue, name='delete_revenue'),

    # Spents
    path('spents/', views.spents_list, name='spents_list'),
    path('spents/create/', views.create_spent, name='create_spent'),
    path('spents/<int:sid>/edit/', views.edit_spent, name='edit_spent'),
    path('spents/<int:sid>/delete/', views.delete_spent, name='delete_spent'),

    # Investments
    path('investments/', views.investments_list, name='investments_list'),
    path('investments/create/', views.create_investment, name='create_investment'),
    path('investments/<int:iid>/edit/', views.edit_investment, name='edit_investment'),
    path('investments/<int:iid>/delete/', views.delete_investment, name='delete_investment'),
]
