from django.contrib import admin
from .models import Produto, Departamento, Pedido, PedidoItem

# Registrar modelos para o admin
admin.site.register(Produto)
admin.site.register(Departamento)
admin.site.register(Pedido)
admin.site.register(PedidoItem)

# Register your models here.
