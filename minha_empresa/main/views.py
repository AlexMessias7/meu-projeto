from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .models import Pedido, Produto,  PedidoItem, Departamento
import json
import pandas as pd

def home(request):
    return render(request, 'main/home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('menu')
        else:
            messages.error(request, 'Nome de usuário ou senha inválidos.')
    return render(request, 'main/login.html')

def pedido_view(request):
    departamentos = Departamento.objects.all()
    produtos = Produto.objects.all()
    context = {
        'departamentos': departamentos,
        'produtos': produtos
    }
    return render(request, 'main/pedido.html', context)

@csrf_exempt
def confirmar_pedido(request):
    if request.method == 'POST':
        try:
            dados = json.loads(request.body)
            print("Dados recebidos:", dados)

            numero_pedido = dados.get('numero')
            dentista = dados.get('dentista')
            asb = dados.get('asb')
            consultorio_nome = dados.get('consultorioNome')
            data_pedido = dados.get('data')
            itens = dados.get('itens', [])

            if not all([numero_pedido, dentista, asb, consultorio_nome, data_pedido, itens]):
                print("Erro: Dados incompletos")
                return JsonResponse({'error': 'Dados incompletos'}, status=400)

            try:
                departamento = Departamento.objects.get(nome=consultorio_nome)
                print(f"Departamento encontrado: {departamento.nome}")
            except Departamento.DoesNotExist:
                print("Erro: Departamento não encontrado")
                return JsonResponse({'error': 'Departamento não encontrado'}, status=400)

            pedido = Pedido.objects.create(
                numero=numero_pedido,
                dentista=dentista,
                asb=asb,
                departamento=departamento,
                data=data_pedido
            )
            print(f"Pedido criado: {pedido}")

            for item in itens:
                material_nome = item.get('materialNome')
                quantidade = item.get('quantidade')

                if not all([material_nome, quantidade]):
                    print("Erro: Dados incompletos dos itens")
                    return JsonResponse({'error': 'Dados incompletos dos itens'}, status=400)

                try:
                    material = Produto.objects.get(nome=material_nome)
                    print(f"Material encontrado: {material.nome}, ID: {material.id}")
                except Produto.DoesNotExist:
                    print(f"Erro: Material {material_nome} não encontrado")
                    return JsonResponse({'error': f"Material {material_nome} não encontrado"}, status=400)

                pedido_item = PedidoItem(
                    pedido=pedido,
                    material=material,
                    quantidade=quantidade
                )
                try:
                    pedido_item.save()
                    print(f"Item criado: Material {material.nome}, Quantidade {quantidade}")
                except Exception as e:
                    print(f"Erro ao salvar PedidoItem: {str(e)}")
                    return JsonResponse({'error': f"Erro ao salvar PedidoItem: {str(e)}"}, status=400)

            return JsonResponse({'message': 'Pedido enviado com sucesso!'}, status=200)
        except json.JSONDecodeError:
            print("Erro: Erro ao decodificar JSON")
            return JsonResponse({'error': 'Erro ao decodificar JSON'}, status=400)
        except Exception as e:
            print(f"Erro: {str(e)}")
            return JsonResponse({'error': str(e)}, status=400)
    print("Erro: Método não permitido")
    return JsonResponse({'error': 'Método não permitido'}, status=405)

def obter_materiais_pedido(request, pedido_id):
    try:
        pedido = Pedido.objects.get(id=pedido_id)
        itens = PedidoItem.objects.filter(pedido=pedido).values('material__nome', 'quantidade')
        materiais = [{'nome': item['material__nome'], 'quantidade': item['quantidade']} for item in itens]
        return JsonResponse({'materiais': materiais}, safe=False)
    except Pedido.DoesNotExist:
        return JsonResponse({'error': 'Pedido não encontrado'}, status=404)

def confirmacao_view(request):
    return render(request, 'main/confirmacao.html')

def menu_view(request):
    return render(request, 'main/menu.html')

def visualizar_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'main/visualizar_pedidos.html', {'pedidos': pedidos})

def obter_produtos(request):
    produtos = Produto.objects.all().values('id', 'nome')
    return JsonResponse(list(produtos), safe=False)

@csrf_exempt
def excluir_todos_pedidos(request):
    if request.method == 'POST':
        Pedido.objects.all().delete()
        return redirect('visualizar_pedidos')
    return redirect('visualizar_pedidos')

def baixar_pedidos_excel(request):
    pedidos = Pedido.objects.all()
    data = []

    if not pedidos:
        print("Nenhum pedido encontrado.")

    for i, pedido in enumerate(pedidos):
        itens = PedidoItem.objects.filter(pedido=pedido)

        if not itens:
            print(f"Pedido {i+1} ({pedido.id}) não tem itens.")

        for item in itens:
            data.append({
                'Pedido': i+1,
                'Dentista': pedido.dentista,
                'ASB': pedido.asb,
                'Consultório': pedido.departamento.nome,  # Corrigindo aqui
                'Data': pedido.data,
                'Material': item.material.nome,
                'Quantidade': item.quantidade
            })

    if not data:
        print("Nenhum dado coletado para exportação.")

    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="pedidos.xlsx"'
    df.to_excel(response, index=False)
    return response

# View para Departamentos
def departamentos(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        Departamento.objects.create(nome=nome)
    departamentos = Departamento.objects.all()
    return render(request, 'main/departamentos.html', {'departamentos': departamentos})

def excluir_departamento(request, id):
    departamento = get_object_or_404(Departamento, id=id)
    departamento.delete()
    return redirect('departamentos')

# View para Produtos
def produtos(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        Produto.objects.create(nome=nome)
    produtos = Produto.objects.all()
    return render(request, 'main/produtos.html', {'produtos': produtos})

def excluir_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    produto.delete()
    return redirect('produtos')

# Adicione esta função
@login_required
def trocar_senha(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Impede que o usuário seja desconectado após a alteração da senha
            messages.success(request, 'Sua senha foi alterada com sucesso!')
            return redirect('menu')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'main/trocar_senha.html', {'form': form})
