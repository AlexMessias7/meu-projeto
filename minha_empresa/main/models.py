from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Departamento(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Pedido(models.Model):
    numero = models.IntegerField(unique=True)
    dentista = models.CharField(max_length=100)
    asb = models.CharField(max_length=100)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    data = models.DateField()

    def __str__(self):
        return f'Pedido {self.numero}'

class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE)
    material = models.ForeignKey(Produto, on_delete=models.CASCADE)  # Garantir que usamos Produto
    quantidade = models.IntegerField()

    def __str__(self):
        return f'{self.quantidade} x {self.material.nome}'
