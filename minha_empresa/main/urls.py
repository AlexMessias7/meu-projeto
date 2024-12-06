from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pedido/', views.pedido_view, name='pedido'),
    path('visualizar_pedidos/', views.visualizar_pedidos, name='visualizar_pedidos'),
    path('confirmar_pedido/', views.confirmar_pedido, name='confirmar_pedido'),
    path('confirmacao/', views.confirmacao_view, name='confirmacao'),
    path('confirmacao_view/', views.confirmacao_view, name='confirmacao_view'),
    path('menu/', views.menu_view, name='menu'),
    path('visualizar_pedidos/', views.visualizar_pedidos, name='visualizar_pedidos'),
    path('excluir_todos_pedidos/', views.excluir_todos_pedidos, name='excluir_todos_pedidos'),
    path('baixar_pedidos_excel/', views.baixar_pedidos_excel, name='baixar_pedidos_excel'),
    path('departamentos/', views.departamentos, name='departamentos'),
    path('excluir_departamento/<int:id>/', views.excluir_departamento, name='excluir_departamento'),
    path('produtos/', views.produtos, name='produtos'),
    path('excluir_produto/<int:id>/', views.excluir_produto, name='excluir_produto'),
    path('trocar_senha/', views.trocar_senha, name='trocar_senha'),
    path('obter_materiais_pedido/<int:pedido_id>/', views.obter_materiais_pedido, name='obter_materiais_pedido'),
    path('obter_produtos/', views.obter_produtos, name='obter_produtos'),
]




