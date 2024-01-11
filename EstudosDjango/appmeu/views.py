from django.shortcuts import render, get_object_or_404, redirect
from .models import Tarefa
from .forms import TarefaForm

def lista_itens(request):
    itens = Tarefa.objects.all()
    return render(request, 'lista_itens.html', {'itens': itens})

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
    item = get_object_or_404(Tarefa, pk=item_id)

    if request.method == 'POST':
        form = TarefaForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('alguma_pagina')  # Redirecione para a página desejada após a atualização
    else:
        form = TarefaForm(instance=item)

    return render(request, 'template_atualiza_item.html', {'form': form})

def exclui_Tarefa(request, Tarefa_id):
    Tarefa = get_object_or_404(Tarefa, pk=Tarefa_id)
    if request.method == 'POST':
        Tarefa.delete()
        return redirect('lista_itens')
    return render(request, 'exclui_Tarefa.html', {'Tarefa': Tarefa})