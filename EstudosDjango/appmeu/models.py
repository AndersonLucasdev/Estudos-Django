# models.py
from django.db import models
from django.contrib.auth.models import User

class Tarefa(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    prazo = models.DateField()
    concluida = models.BooleanField(default=False)
    favorito = models.BooleanField(default=False)
    prioridade = models.BooleanField(default=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    tarefa = models.ForeignKey('Tarefa', on_delete=models.CASCADE, related_name='comentarios')
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentário por {self.autor.username} em {self.data_criacao}'
    
