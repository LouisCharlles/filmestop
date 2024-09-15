from django.test import TestCase, Client
from django.urls import reverse
from .models import Filme, Usuario
import json
from datetime import datetime

class FilmePorGeneroViewTest(TestCase):
    """
    Testes para a visualização de filmes por gênero.

    Métodos:
        setUp: Configura o ambiente de teste com filmes de diferentes gêneros.
        test_get_filme_por_genero: Testa a visualização de filmes por gênero quando filmes estão disponíveis.
        test_genero_nao_encontrado: Testa a visualização de filmes por gênero quando nenhum filme é encontrado.
    """
    
    def setUp(self):
        """
        Configura o ambiente de teste com filmes de diferentes gêneros.
        """
        self.filme1 = Filme.objects.create(nome='Filme A', genero='Ação', ano=datetime(2022, 3, 21), diretor='Diretor A', sinopse='Sinopse A')
        self.filme2 = Filme.objects.create(nome='Filme B', genero='Comédia', ano=datetime(2021, 8, 11), diretor='Diretor B', sinopse='Sinopse B')

    def test_get_filme_por_genero(self):
        """
        Testa a visualização de filmes por gênero quando filmes estão disponíveis.
        """
        client = Client()
        response = client.get(reverse('filmes_por_genero', kwargs={'genero': 'Ação'}))
        self.assertEqual(response.status_code, 200)

        filmes = json.loads(response.content)
        self.assertEqual(len(filmes), 1)
        self.assertEqual(filmes[0]['nome'], 'Filme A')

    def test_genero_nao_encontrado(self):
        """
        Testa a visualização de filmes por gênero quando nenhum filme é encontrado.
        """
        client = Client()
        response = client.get(reverse('filmes_por_genero', kwargs={'genero': 'Policial'}))
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertEqual(data['mensagem'], 'Nenhum filme encontrado no gênero Policial foi encontrado.')


class FilmePorNomeViewTest(TestCase):
    """
    Testes para a visualização de filmes por nome.

    Métodos:
        setUp: Configura o ambiente de teste com um filme.
        test_get_filme_por_nome: Testa a visualização de filme por nome quando o filme está disponível.
        test_nome_nao_encontrado: Testa a visualização de filme por nome quando o filme não é encontrado.
    """
    
    def setUp(self):
        """
        Configura o ambiente de teste com um filme.
        """
        self.filme = Filme.objects.create(nome='Filme C', genero='Drama', ano=datetime(2020, 3, 21), diretor='Diretor C', sinopse='Sinopse C')

    def test_get_filme_por_nome(self):
        """
        Testa a visualização de filme por nome quando o filme está disponível.
        """
        client = Client()
        response = client.get(reverse('filme_por_nome', kwargs={'nome': 'Filme C'}))
        self.assertEqual(response.status_code, 200)

        filme = json.loads(response.content)
        self.assertEqual(filme[0]['nome'], 'Filme C')

    def test_nome_nao_encontrado(self):
        """
        Testa a visualização de filme por nome quando o filme não é encontrado.
        """
        client = Client()
        response = client.get(reverse('filme_por_nome', kwargs={'nome': 'Filme Desconhecido'}))
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertEqual(data['mensagem'], 'Nenhum filme chamado Filme Desconhecido foi encontrado')


class AlugarFilmePorNomeViewTest(TestCase):
    """
    Testes para a funcionalidade de alugar filme por nome.

    Métodos:
        setUp: Configura o ambiente de teste com um usuário e um filme.
        test_alugar_filme_sucesso: Testa o sucesso ao alugar um filme.
        test_filme_nao_encontrado: Testa a tentativa de alugar um filme que não existe.
        test_usuario_nao_encontrado: Testa a tentativa de alugar um filme para um usuário que não existe.
    """
    
    def setUp(self):
        """
        Configura o ambiente de teste com um usuário e um filme.
        """
        self.usuario = Usuario.objects.create(email='usuario@test.com', nome='Usuário Teste')
        self.filme = Filme.objects.create(nome='Filme X', genero='Aventura', ano=datetime(2022, 9, 12), diretor='Diretor X', sinopse='Sinopse X')

    def test_alugar_filme_sucesso(self):
        """
        Testa o sucesso ao alugar um filme.
        """
        client = Client()
        response = client.post(reverse('alugar_filme', kwargs={'email': self.usuario.email}), json.dumps(self.filme.nome), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertEqual(data['mensagem'], 'Filme Filme X alugado com sucesso!')

    def test_filme_nao_encontrado(self):
        """
        Testa a tentativa de alugar um filme que não existe.
        """
        client = Client()
        response = client.post(reverse('alugar_filme', kwargs={'email': self.usuario.email}), json.dumps('Filme Inexistente'), content_type='application/json')

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertEqual(data['mensagem'], 'Filme não encontrado')

    def test_usuario_nao_encontrado(self):
        """
        Testa a tentativa de alugar um filme para um usuário que não existe.
        """
        client = Client()
        response = client.post(reverse('alugar_filme', kwargs={'email': 'email_invalido@test.com'}), json.dumps(self.filme.nome), content_type='application/json')

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertEqual(data['mensagem'], 'Usuário não encontrado')


class DarNotaAoFilmeAlugadoViewTest(TestCase):
    """
    Testes para a funcionalidade de dar nota a um filme alugado.

    Métodos:
        setUp: Configura o ambiente de teste com um usuário e um filme.
        test_dar_nota_ao_filme_sucesso: Testa o sucesso ao atribuir uma nota ao filme.
        test_dar_nota_menor_que_0: Testa a tentativa de atribuir uma nota menor que 0.
        test_dar_nota_maior_que_10: Testa a tentativa de atribuir uma nota maior que 10.
        test_usuario_nao_encontrado: Testa a tentativa de atribuir uma nota quando o usuário não existe.
        test_filme_nao_encontrado: Testa a tentativa de atribuir uma nota quando o filme não existe.
    """
    
    def setUp(self):
        """
        Configura o ambiente de teste com um usuário e um filme.
        """
        self.usuario = Usuario.objects.create(email='usuario@test.com', nome='Usuário Teste')
        self.filme = Filme.objects.create(nome='Filme X', genero='Aventura', ano=datetime(2022, 9, 12), diretor='Diretor X', sinopse='Sinopse X')

    def test_dar_nota_ao_filme_sucesso(self):
        """
        Testa o sucesso ao atribuir uma nota ao filme.
        """
        client = Client()
        nota = 8.5
        response = client.post(reverse('dar_nota_ao_filme', kwargs={'email': self.usuario.email, 'nome': self.filme.nome}), json.dumps(nota), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertEqual(data['mensagem'], f'Nota {nota} atribuída ao filme: {self.filme.nome}')

    def test_dar_nota_menor_que_0(self):
        """
        Testa a tentativa de atribuir uma nota menor que 0.
        """
        client = Client()
        nota = -5.4
        response = client.post(reverse('dar_nota_ao_filme', kwargs={'email': self.usuario.email, 'nome': self.filme.nome}), json.dumps(nota), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['mensagem'], f'A nota que você digitou({nota}) não é permitida. A nota deve ser entre 0.0 a 10.0.')

    def test_dar_nota_maior_que_10(self):
        """
        Testa a tentativa de atribuir uma nota maior que 10.
        """
        client = Client()
        nota = 12
        response = client.post(reverse('dar_nota_ao_filme', kwargs={'email': self.usuario.email, 'nome': self.filme.nome}), json.dumps(nota), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['mensagem'], f'A nota que você digitou({nota}) não é permitida. A nota deve ser entre 0.0 a 10.0.')

    def test_usuario_nao_encontrado(self):
        """
        Testa a tentativa de atribuir uma nota quando o usuário não existe.
        """
        client = Client()
        nota = 7.5
        response = client.post(reverse('dar_nota_ao_filme', kwargs={'email': 'email_invalido@test.com', 'nome': self.filme.nome}), json.dumps(nota), content_type='application/json')

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertEqual(data['mensagem'], 'Usuário não encontrado')

    def test_filme_nao_encontrado(self):
        """
        Testa a tentativa de atribuir uma nota quando o filme não existe.
        """
        client = Client()
        nota = 7.1
        response = client.post(reverse('dar_nota_ao_filme', kwargs={'email': self.usuario.email, 'nome': 'Filme Inexistente'}), json.dumps(nota), content_type='application/json')

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertEqual(data['mensagem'], 'Filme não encontrado')


class VerFilmesAlugadosViewTest(TestCase):
    """
    Testes para a visualização dos filmes alugados por um usuário.

    Métodos:
        setUp: Configura o ambiente de teste com um usuário e um filme.
        test_get_lista_filmes_alugados_com_sucesso: Testa a obtenção da lista de filmes alugados com sucesso.
        test_usuario_nao_encontrado: Testa a tentativa de obter a lista de filmes alugados para um usuário que não existe.
    """
    
    def setUp(self):
        """
        Configura o ambiente de teste com um usuário e um filme.
        """
        self.usuario = Usuario.objects.create(email='usuario@test.com', nome='Usuário Teste', celular="(98)93233-4221")
        self.filme = Filme.objects.create(nome='Filme X', genero='Aventura', ano=datetime(2022, 9, 12), diretor='Diretor X', sinopse='Sinopse X')

    def test_get_lista_filmes_alugados_com_sucesso(self):
        """
        Testa a obtenção da lista de filmes alugados com sucesso.
        """
        client = Client()
        response = client.get(reverse('filmes_alugados', kwargs={'email': 'usuario@test.com'}))
        self.assertEqual(response.status_code, 200)

        filmes_alugados = json.loads(response.content)
        filmes_alugados.append(self.filme)
        self.assertIsInstance(filmes_alugados, list)

    def test_usuario_nao_encontrado(self):
        """
        Testa a tentativa de obter a lista de filmes alugados para um usuário que não existe.
        """
        client = Client()
        response = client.get(reverse('filmes_alugados', kwargs={'email': 'email_invalido@test.com'}))

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertEqual(data['mensagem'], 'Usuário não encontrado')
