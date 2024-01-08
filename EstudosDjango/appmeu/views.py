from django.shortcuts import render, get_object_or_404, redirect
from .models import Item
from .forms import ItemForm

def lista_itens(request):
    itens = Item.objects.all()
    return render(request, 'lista_itens.html', {'itens': itens})

def cria_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_itens')
    else:
        form = ItemForm()
    return render(request, 'cria_item.html', {'form': form})

def atualiza_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('lista_itens')
    else:
        form = ItemForm(instance=item)
    return render(request, 'atualiza_item.html', {'form': form, 'item': item})

def exclui_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('lista_itens')
    return render(request, 'exclui_item.html', {'item': item})