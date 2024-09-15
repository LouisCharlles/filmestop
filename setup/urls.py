"""
Configuração de URLs para o projeto de gerenciamento de filmes.

Esta configuração define as rotas para a aplicação de gerenciamento de filmes, associando cada rota a uma view baseada em classe. Cada URL possui um padrão específico e parâmetros que são utilizados pelas views para retornar os dados apropriados. Abaixo está a descrição de cada rota, os parâmetros esperados e a lógica de negócio implementada:

1. **URL: `filmes/genero/<str:genero>/`**
   - **View Associada:** `FilmePorGeneroView`
   - **Parâmetro:** `genero` (do tipo `str`)
     - Descrição: O gênero dos filmes a serem retornados. Deve ser passado como uma string na URL.
   - **Lógica de Negócio:**
     - Recebe o gênero passado na URL e utiliza o `FilmeRepository` para buscar todos os filmes que correspondem a esse gênero.
     - Retorna uma lista de filmes no formato JSON. Se nenhum filme for encontrado, retorna um erro 404 com uma mensagem apropriada.
   - **Nome da URL:** `filmes_por_genero`

2. **URL: `filmes/nome/<str:nome>/`**
   - **View Associada:** `FilmePorNomeView`
   - **Parâmetro:** `nome` (do tipo `str`)
     - Descrição: O nome do filme a ser retornado. Deve ser passado como uma string na URL.
   - **Lógica de Negócio:**
     - Recebe o nome do filme e utiliza o `FilmeRepository` para buscar o filme com esse nome exato.
     - Retorna o filme no formato JSON. Se o filme não for encontrado, retorna um erro 404 com uma mensagem apropriada.
   - **Nome da URL:** `filme_por_nome`

3. **URL: `filmes/alugar/<str:email>/`**
   - **View Associada:** `AlugarFilmePorNomeView`
   - **Parâmetro:** `email` (do tipo `str`)
     - Descrição: O email do usuário que está tentando alugar o filme. Deve ser passado como uma string na URL.
   - **Lógica de Negócio:**
     - Recebe o email do usuário e o nome do filme (passado no corpo da requisição em formato JSON).
     - Verifica se o usuário existe e se o filme está disponível. Se o filme não estiver alugado pelo usuário, cria um novo aluguel.
     - Retorna uma mensagem de sucesso ou erro dependendo do resultado da operação. Se o filme já estiver alugado pelo usuário, retorna um erro 400.
   - **Nome da URL:** `alugar_filme`

4. **URL: `filmes/alugados/<str:email>`**
   - **View Associada:** `VerFilmesAlugadosView`
   - **Parâmetro:** `email` (do tipo `str`)
     - Descrição: O email do usuário para recuperar a lista de filmes que ele alugou. Deve ser passado como uma string na URL.
   - **Lógica de Negócio:**
     - Recebe o email do usuário e utiliza o `AluguelRepository` para buscar todos os filmes alugados pelo usuário.
     - Retorna uma lista de filmes no formato JSON, incluindo detalhes sobre cada aluguel. Se o usuário não for encontrado, retorna um erro 404.
   - **Nome da URL:** `filmes_alugados`

5. **URL: `filmes/nota/<str:email>/<str:nome>`**
   - **View Associada:** `DarNotaAoFilmeAlugadoView`
   - **Parâmetros:**
     - `email` (do tipo `str`): O email do usuário que está atribuindo a nota. Deve ser passado como uma string na URL.
     - `nome` (do tipo `str`): O nome do filme ao qual a nota será atribuída. Deve ser passado como uma string na URL.
   - **Lógica de Negócio:**
     - Recebe o email do usuário e o nome do filme, além da nota (passada no corpo da requisição em formato JSON).
     - Verifica se o usuário e o filme existem e se a nota está dentro do intervalo permitido (0.0 a 10.0). Se o filme ainda não tiver uma nota atribuída por esse usuário, cria uma nova nota.
     - Atualiza o total de avaliações e a nota final do filme com base nas notas atribuídas.
     - Retorna uma mensagem de sucesso ou erro dependendo do resultado da operação. Se o usuário ou o filme não forem encontrados ou se a nota estiver fora do intervalo permitido, retorna um erro apropriado.
   - **Nome da URL:** `dar_nota_ao_filme`
"""

from django.contrib import admin
from django.urls import path
from filmestop.views import (
    FilmePorGeneroView,
    FilmePorNomeView,
    AlugarFilmePorNomeView,
    VerFilmesAlugadosView,
    DarNotaAoFilmeAlugadoView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('filmes/genero/<str:genero>/', FilmePorGeneroView.as_view(), name='filmes_por_genero'),
    path('filmes/nome/<str:nome>/', FilmePorNomeView.as_view(), name='filme_por_nome'),
    path('filmes/alugar/<str:email>/', AlugarFilmePorNomeView.as_view(), name='alugar_filme'),
    path('filmes/alugados/<str:email>/', VerFilmesAlugadosView.as_view(), name='filmes_alugados'),
    path('filmes/nota/<str:email>/<str:nome>/', DarNotaAoFilmeAlugadoView.as_view(), name='dar_nota_ao_filme')
]
