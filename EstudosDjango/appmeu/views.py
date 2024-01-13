from django.shortcuts import render, get_object_or_404, redirect
from .models import Tarefa
from .forms import TarefaForm

def lista_itens(request):
    itens = Tarefa.objects.all()
    return render(request, 'lista_itens.html', {'itens': itens})

def visualiza_tarefa(request, item_id):
    tarefa = get_object_or_404(Tarefa, pk=item_id)
    return render(request, 'tarefas/visualiza_tarefa.html', {'tarefa': tarefa})

def cria_item(request):
    if request.method == 'POST':
        form = TarefaForm(request.POST)
        if form.is_valid():
            # Salvar o formulário, se necessário
            form.save()
            return redirect('alguma_pagina')  # Redirecione para a página desejada após a criação
    else:
        form = TarefaForm()

    return render(request, 'template_cria_item.html', {'form': form})

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