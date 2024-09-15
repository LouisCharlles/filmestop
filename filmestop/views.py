"""
Views para o gerenciamento de filmes.

Estas views são responsáveis por lidar com as solicitações HTTP para diferentes operações relacionadas a filmes e usuários. Cada view é baseada em uma classe e utiliza métodos específicos para processar as solicitações e retornar as respostas apropriadas.

1. **Classe: `FilmePorGeneroView`**
   - **Método:** `get`
   - **URL:** `filmes/genero/<str:genero>/`
   - **Parâmetro da URL:**
     - `genero` (do tipo `str`): O gênero dos filmes a serem retornados. Deve ser passado como uma string na URL.
   - **Lógica de Negócio:**
     - Recupera o gênero da URL e usa o `FilmeRepository` para buscar filmes que correspondem ao gênero fornecido.
     - Converte a consulta em uma lista de filmes.
     - Se nenhum filme for encontrado, retorna uma resposta JSON com status 404 e uma mensagem de erro indicando que nenhum filme foi encontrado para o gênero especificado.
     - Se filmes forem encontrados, retorna uma resposta JSON com a lista de filmes e status 200.
     - Em caso de exceção, retorna uma resposta JSON com status 400 e a mensagem de erro.
   - **Nome da URL:** `filmes_por_genero`

2. **Classe: `FilmePorNomeView`**
   - **Método:** `get`
   - **URL:** `filmes/nome/<str:nome>/`
   - **Parâmetro da URL:**
     - `nome` (do tipo `str`): O nome do filme a ser retornado. Deve ser passado como uma string na URL.
   - **Lógica de Negócio:**
     - Recupera o nome do filme da URL e usa o `FilmeRepository` para buscar o filme com o nome exato.
     - Converte a consulta em uma lista com o filme encontrado.
     - Se o filme não for encontrado, retorna uma resposta JSON com status 404 e uma mensagem de erro indicando que nenhum filme foi encontrado com o nome fornecido.
     - Se o filme for encontrado, retorna uma resposta JSON com os detalhes do filme e status 200.
     - Em caso de exceção, retorna uma resposta JSON com status 400 e a mensagem de erro.
   - **Nome da URL:** `filme_por_nome`

3. **Classe: `AlugarFilmePorNomeView`**
   - **Método:** `post`
   - **URL:** `filmes/alugar/<str:email>/`
   - **Parâmetro da URL:**
     - `email` (do tipo `str`): O email do usuário que está tentando alugar o filme. Deve ser passado como uma string na URL.
   - **Corpo da Requisição (Payload JSON):**
     - Um JSON contendo o nome do filme a ser alugado. Exemplo: `{"nome": "Filme X"}`
   - **Lógica de Negócio:**
     - Recupera o email do usuário da URL e o nome do filme do corpo da requisição.
     - Verifica se o usuário existe. Se não existir, retorna uma resposta JSON com status 404 e uma mensagem de erro indicando que o usuário não foi encontrado.
     - Verifica se o filme existe. Se não existir, retorna uma resposta JSON com status 404 e uma mensagem de erro indicando que o filme não foi encontrado.
     - Verifica se o usuário já alugou o filme. Se não, cria um novo aluguel e retorna uma resposta JSON com status 201 e uma mensagem de sucesso.
     - Se o usuário já alugou o filme, retorna uma resposta JSON com status 400 e uma mensagem indicando que o filme já foi alugado.
     - Em caso de exceção, retorna uma resposta JSON com status 400 e a mensagem de erro.
   - **Nome da URL:** `alugar_filme`

4. **Classe: `DarNotaAoFilmeAlugadoView`**
   - **Método:** `post`
   - **URL:** `filmes/nota/<str:email>/<str:nome>/`
   - **Parâmetros da URL:**
     - `email` (do tipo `str`): O email do usuário que está atribuindo a nota. Deve ser passado como uma string na URL.
     - `nome` (do tipo `str`): O nome do filme ao qual a nota será atribuída. Deve ser passado como uma string na URL.
   - **Corpo da Requisição (Payload JSON):**
     - Um JSON contendo a nota atribuída ao filme. Exemplo: `8.5`
   - **Lógica de Negócio:**
     - Recupera o email do usuário e o nome do filme da URL e a nota do corpo da requisição.
     - Verifica se o usuário e o filme existem. Se algum deles não existir, retorna uma resposta JSON com status 404 e uma mensagem de erro apropriada.
     - Verifica se a nota está dentro do intervalo permitido (0.0 a 10.0). Se a nota estiver fora desse intervalo, retorna uma resposta JSON com status 400 e uma mensagem indicando que a nota não é permitida.
     - Verifica se o usuário já atribuiu uma nota ao filme. Se não, cria uma nova nota e atualiza o total de avaliações e a nota final do filme.
     - Se o usuário já atribuiu uma nota, retorna uma resposta JSON com status 400 e uma mensagem indicando que a nota já foi atribuída.
     - Em caso de exceção, retorna uma resposta JSON com status 400 e a mensagem de erro.
   - **Nome da URL:** `dar_nota_ao_filme`

5. **Classe: `VerFilmesAlugadosView`**
   - **Método:** `get`
   - **URL:** `filmes/alugados/<str:email>/`
   - **Parâmetro da URL:**
     - `email` (do tipo `str`): O email do usuário para recuperar a lista de filmes que ele alugou. Deve ser passado como uma string na URL.
   - **Lógica de Negócio:**
     - Recupera o email do usuário da URL e usa o `AluguelRepository` para buscar todos os filmes alugados pelo usuário.
     - Verifica se o usuário existe. Se não existir, retorna uma resposta JSON com status 404 e uma mensagem de erro indicando que o usuário não foi encontrado.
     - Constrói uma lista de filmes alugados, incluindo detalhes do filme e da nota atribuída (se disponível).
     - Retorna uma resposta JSON com a lista de filmes alugados e status 200.
     - Em caso de exceção, retorna uma resposta JSON com status 400 e a mensagem de erro.
   - **Nome da URL:** `filmes_alugados`
"""

from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .repositories.repositories import FilmeRepository, NotaRepository, AluguelRepository, UsuarioRepository
from .models import Filme, Usuario, Aluguel, Nota
from django.db.models import Avg
import json

class FilmePorGeneroView(View):
    
    def get(self, request, *args, **kwargs):
        
        genero = kwargs.get('genero')
        try:
            filmes = FilmeRepository.get_filme_por_genero(genero=genero)
            filmes_list = list(filmes)

            if not filmes_list:
                return JsonResponse({'status': 'erro', 'mensagem': f'Nenhum filme encontrado no gênero {genero} foi encontrado.'}, status=404)
            
            return JsonResponse(filmes_list, safe=False, status=200)
        except Exception as e:
            return JsonResponse({'status': 'erro', 'mensagem': str(e)}, status=400)

class FilmePorNomeView(View):

    def get(self, request, *args, **kwargs):
       
        nome = kwargs.get('nome')
        try:
            filme = FilmeRepository.get_filme_por_nome(nome=nome)
            filmes_list = list(filme)

            if not filmes_list:
                return JsonResponse({'status': 'erro', 'mensagem': f'Nenhum filme chamado {nome} foi encontrado'}, status=404)
            
            return JsonResponse(filmes_list, safe=False, status=200)
        
        except Exception as e:
            return JsonResponse({'status': 'erro', 'mensagem': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class AlugarFilmePorNomeView(View):
    
    def post(self, request, *args, **kwargs):
      
        try:
            email_usuario = kwargs.get('email')
            usuario = Usuario.objects.get(email=email_usuario)
            filme_para_alugar = json.loads(request.body)
            filme = Filme.objects.filter(nome__iexact=filme_para_alugar).first()

            if not filme:
                return JsonResponse({'status': 'erro', 'mensagem': 'Filme não encontrado'}, status=404)

            if not Aluguel.objects.filter(usuario=usuario, filme=filme).exists():
                Aluguel.objects.create(usuario=usuario, filme=filme)
                return JsonResponse({'status': 'sucesso', 'mensagem': f'Filme {filme.nome} alugado com sucesso!'}, status=201)
            else:
                return JsonResponse({'status': 'erro', 'mensagem': f'Você já alugou o filme {filme.nome}'}, status=400)
            
        except Usuario.DoesNotExist:
            return JsonResponse({'status': 'erro', 'mensagem': 'Usuário não encontrado'}, status=404)
        except Filme.DoesNotExist:
            return JsonResponse({'status': 'erro', 'mensagem': 'Filme não encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'erro', 'mensagem': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class DarNotaAoFilmeAlugadoView(View):
    
    def post(self, request, *args, **kwargs):
       
        try:
            email_usuario = kwargs.get('email')
            nome_filme = kwargs.get('nome')
            usuario = Usuario.objects.get(email=email_usuario)
            filme = Filme.objects.get(nome=nome_filme)
            
            nota_atribuida_ao_filme = json.loads(request.body)

            if nota_atribuida_ao_filme < 0 or nota_atribuida_ao_filme > 10:
                return JsonResponse({'status': 'erro', 'mensagem': f'A nota que você digitou ({nota_atribuida_ao_filme}) não é permitida. A nota deve ser entre 0.0 a 10.0.'}, status=400)
            
            if not NotaRepository.get_nota_by_usuario_e_filme(usuario=usuario, filme=filme).exists():
                NotaRepository.create_nota(usuario=usuario, filme=filme, nota_atribuida_ao_filme=nota_atribuida_ao_filme)

                total_avaliacoes = Nota.objects.filter(filme=filme).count()
                nota_final = Nota.objects.filter(filme=filme).aggregate(Avg('nota_atribuida_ao_filme'))['nota_atribuida_ao_filme__avg']

                filme.total_avaliacoes = total_avaliacoes
                filme.nota_final = nota_final
                filme.save()

                return JsonResponse({'status': 'sucesso', 'mensagem': f'Nota {nota_atribuida_ao_filme} atribuída ao filme: {filme.nome}'}, status=201)
            else:
                return JsonResponse({'status': 'erro', 'mensagem': f'Você já atribuiu uma nota ao filme {filme.nome}'}, status=400)
        
        except Usuario.DoesNotExist:
            return JsonResponse({'status': 'erro', 'mensagem': 'Usuário não encontrado'}, status=404)
        except Filme.DoesNotExist:
            return JsonResponse({'status': 'erro', 'mensagem': 'Filme não encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'erro', 'mensagem': str(e)}, status=400)
   
class VerFilmesAlugadosView(View):
    
    def get(self, request, *args, **kwargs):
       
        try:
            usuario = kwargs.get('email')
            alugueis = AluguelRepository.get_filmes_alugados(usuario=usuario)

            if not UsuarioRepository.get_usuario_by_email(email=usuario).exists():
                return JsonResponse({'status': 'erro', 'mensagem': 'Usuário não encontrado'}, status=404)

            filmes_data = []
            for aluguel in alugueis:
                try:
                    nota_do_filme = Nota.objects.get(filme=aluguel.filme, usuario=aluguel.usuario).nota_atribuida_ao_filme
                except Nota.DoesNotExist:
                    nota_do_filme = None

                filmes_data.append({
                    'id': aluguel.id,
                    'nome_filme': aluguel.filme.nome,
                    'genero_filme': aluguel.filme.genero,
                    'lancamento_filme': aluguel.filme.ano,
                    'diretor_filme': aluguel.filme.diretor,
                    'sinopse_filme': aluguel.filme.sinopse,
                    'email_usuario': aluguel.usuario.email,
                    'nota_do_filme': nota_do_filme,
                    'data_de_locacao': aluguel.data_de_locacao
                })
            return JsonResponse(filmes_data, safe=False)
        except Exception as e:
            return JsonResponse({'status': 'erro', 'mensagem': str(e)}, status=400)
