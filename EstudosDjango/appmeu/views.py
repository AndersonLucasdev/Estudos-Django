from django.shortcuts import render, get_object_or_404, redirect
from .models import Tarefa, Comentario
from .forms import TarefaForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ComentarioForm


## tarefas
@login_required(login_url='login_usuario')
def lista_itens(request):
    itens = Tarefa.objects.all()
    return render(request, 'lista_itens.html', {'itens': itens})

def calendario_tarefas(request):
    tarefas = Tarefa.objects.all()
    eventos = []

    for tarefa in tarefas:
        evento = {
            'title': tarefa.titulo,
            'start': tarefa.prazo.isoformat(),
        }
        eventos.append(evento)

    return render(request, 'calendario_tarefas.html', {'eventos': eventos})

def buscar_tarefas(request):
    query = request.GET.get('q')
    filtro_prioridade = request.GET.get('prioridade')
    filtro_concluida = request.GET.get('concluida')

    tarefas = Tarefa.objects.all()

    if query:
        tarefas = tarefas.filter(titulo__icontains=query)

    if filtro_prioridade:
        tarefas = tarefas.filter(prioridade=True)

    if filtro_concluida:
        tarefas = tarefas.filter(concluida=True)

    return render(request, 'lista_tarefas.html', {'tarefas': tarefas})

def lista_tarefas(request):
    # Obtém todos os objetos de Tarefa
    tarefas = Tarefa.objects.all()

    # Aplica os filtros, se fornecidos pelos parâmetros GET
    titulo = request.GET.get('titulo')
    if titulo:
        tarefas = tarefas.filter(titulo__icontains=titulo)

    descricao = request.GET.get('descricao')
    if descricao:
        tarefas = tarefas.filter(descricao__icontains=descricao)

    return render(request, 'tarefas/lista_tarefas.html', {'tarefas': tarefas})

def visualiza_tarefa(request, item_id):
    tarefa = get_object_or_404(Tarefa, pk=item_id)
    return render(request, 'tarefas/visualiza_tarefa.html', {'tarefa': tarefa})

def cria_item(request):
    if request.method == 'POST':
        form = TarefaForm(request.POST)
        if form.is_valid():
            # Salvar o formulário, se necessário
            form.save()
            return redirect('lista_itens.html')  # Redirecione para a página desejada após a criação
    else:
        form = TarefaForm()

    return render(request, 'cria_item.html', {'form': form})

def atualiza_item(request, item_id):
    tarefa = get_object_or_404(Tarefa, pk=item_id)

    if request.method == 'POST':
        form = TarefaForm(request.POST, instance=tarefa)
        if form.is_valid():
            form.save()
            return redirect('lista_tarefas')
    else:
        form = TarefaForm(instance=tarefa)

    return render(request, 'tarefas/atualiza_item.html', {'form': form, 'tarefa': tarefa})

def confirma_exclusao(request, item_id):
    tarefa = get_object_or_404(Tarefa, pk=item_id)
    return render(request, 'tarefas/confirma_exclusao.html', {'tarefa': tarefa})

def exclui_item(request, item_id):
    item = get_object_or_404(Tarefa, pk=item_id)
    item.delete()
    return redirect('alguma_pagina')


def marca_tarefa_concluida(request, tarefa_id):
    # Obter a tarefa pelo ID
    tarefa = get_object_or_404(Tarefa, pk=tarefa_id)

    # Marcar a tarefa como concluída
    tarefa.concluida = True
    tarefa.save()

    # Redirecionar de volta para a lista de tarefas
    return redirect('lista_tarefas')

def marcar_favorito(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, pk=tarefa_id)
    tarefa.favorito = not tarefa.favorito
    tarefa.save()
    return redirect('lista_tarefas')

def definir_prioridade(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, pk=tarefa_id)
    tarefa.prioridade = not tarefa.prioridade
    tarefa.save()
    return redirect('lista_tarefas')


def adiciona_comentario(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, pk=tarefa_id)
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.autor = request.user
            comentario.tarefa = tarefa
            comentario.save()
            return redirect('detalhes_tarefa', tarefa_id=tarefa.id)
    else:
        form = ComentarioForm()
    return render(request, 'tarefas/adiciona_comentario.html', {'form': form})
## auth
def cadastra_usuario(request):
    if request.method == 'POST':
        form = TarefaForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('lista_tarefas')
    else:
        form = TarefaForm()

    return render(request, 'tarefas/cadastra_usuario.html', {'form': form})

def login_usuario(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('lista_tarefas')
        else:
            return render(request, 'login.html', {'erro': 'Credenciais inválidas.'})
    return render(request, 'login.html')

@login_required(login_url='login_usuario')
def logout_usuario(request):
    logout(request)
    return redirect('login_usuario')


