from django.urls import path,include
from . import views

urlpatterns = [

    path('createUser/',views.create_user,name = 'create_user'),
    path('createExpense/',views.create_expense,name='create_expense'),
    path('getUserExpense/<int:user_id>',views.get_user_expenses,name='user_expense'),
    path('getBalances/',views.get_balances,name='get_balances'),
    path('calculateBalances/',views.calculate_balances,name='calculate_balances'),
    
]
