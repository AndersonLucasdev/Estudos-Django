from django.urls import path
from . import views

urlpatterns = [
    path('lista/', views.lista_itens, name='lista_itens'),
    path('cria/', views.cria_item, name='cria_item'),
    path('atualiza/<int:item_id>/', views.atualiza_item, name='atualiza_item'),
    path('exclui/<int:item_id>/', views.exclui_item, name='exclui_item'),
    path('login/', auth_views.LoginView.as_view(template_name='tarefas/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.registro, name='registro'),
]