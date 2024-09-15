from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Usuario(models.Model):
    """
    Representa um usuário do sistema.

    Atributos:
        nome (CharField): Nome completo do usuário.
        celular (CharField): Número de celular do usuário, único.
        email (CharField): Endereço de e-mail do usuário, único e chave primária.
    """
    nome = models.CharField(verbose_name="Nome", max_length=1000, null=False, blank=False)
    celular = models.CharField(verbose_name="Celular", max_length=100, null=False, blank=False, unique=True)
    email = models.CharField(primary_key=True, verbose_name="Email", max_length=1000, null=False, blank=False, unique=True)


class Filme(models.Model):
    """
    Representa um filme disponível no sistema.

    Atributos:
        nome (CharField): Nome do filme, chave primária.
        genero (CharField): Gênero do filme.
        ano (DateField): Ano de lançamento do filme.
        sinopse (CharField): Sinopse do filme.
        diretor (CharField): Nome do diretor do filme.
        total_avaliacoes (IntegerField): Número total de avaliações recebidas, default é 0.
        nota_final (FloatField): Nota final média do filme, deve estar entre 0 e 10.

    Meta:
        unique_together: Garante que a combinação dos campos nome, genero, ano, sinopse, diretor, total_avaliacoes e nota_final seja única.
    """
    nome = models.CharField(primary_key=True, verbose_name="Nome", max_length=1000, null=False, blank=False, unique=True)
    genero = models.CharField(verbose_name="Gênero", max_length=1000, null=False, blank=False)
    ano = models.DateField(verbose_name="Ano", null=False, blank=False)
    sinopse = models.CharField(verbose_name="Sinopse", max_length=3000, null=False, blank=False)
    diretor = models.CharField(verbose_name="Diretor", max_length=1000, null=False, blank=False)
    total_avaliacoes = models.IntegerField(verbose_name="Total de avaliações", default=0, blank=True)
    nota_final = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)], verbose_name="Nota final", null=False, blank=False)

    class Meta:
        unique_together = ('nome', 'genero', 'ano', 'sinopse', 'diretor', 'total_avaliacoes', 'nota_final')

    def __str__(self):
        """
        Retorna o nome do filme.
        """
        return self.nome


class Aluguel(models.Model):
    """
    Representa um aluguel de filme feito por um usuário.

    Atributos:
        usuario (ForeignKey): Referência ao usuário que realizou o aluguel.
        filme (ForeignKey): Referência ao filme que foi alugado.
        data_de_locacao (DateField): Data em que o aluguel foi realizado, definida automaticamente.
    
    Meta:
        unique_together: Garante que a combinação dos campos usuario e filme seja única.
    """
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE)
    data_de_locacao = models.DateField(verbose_name="Data de locação", auto_now_add=True)

    def __str__(self):
        """
        Retorna uma string formatada com o nome do usuário e o nome do filme.
        """
        return f'{self.usuario.username} alugou {self.filme.nome}'

    class Meta:
        unique_together = ('usuario', 'filme')


class Nota(models.Model):
    """
    Representa uma nota atribuída a um filme por um usuário.

    Atributos:
        usuario (ForeignKey): Referência ao usuário que atribuiu a nota.
        filme (ForeignKey): Referência ao filme que recebeu a nota.
        nota_atribuida_ao_filme (FloatField): Nota atribuída ao filme pelo usuário, deve estar entre 0 e 10 e é única.

    Meta:
        unique_together: Garante que a combinação dos campos usuario, filme e nota_atribuida_ao_filme seja única.
    """
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE)
    nota_atribuida_ao_filme = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)], verbose_name="Nota atribuída ao filme", null=True, blank=True, unique=True)

    class Meta:
        unique_together = ('usuario', 'filme', 'nota_atribuida_ao_filme')
