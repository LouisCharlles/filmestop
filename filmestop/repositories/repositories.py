from filmestop.models import Filme,Nota,Aluguel,Usuario

class FilmeRepository:
    @staticmethod
    def get_filme_por_nome(nome):
        return Filme.objects.filter(nome__iexact=nome).values(
            'nome', 'genero', 'ano', 'sinopse', 'diretor', 'total_avaliacoes', 'nota_final'
        )
    
    @staticmethod
    def get_filme_por_genero(genero):
        return Filme.objects.filter(genero__iexact=genero).values('nome','genero', 'ano', 'sinopse', 'diretor','total_avaliacoes','nota_final')

 
class NotaRepository:
    @staticmethod
    def get_nota_by_usuario_e_filme(usuario,filme):
        return Nota.objects.filter(usuario=usuario,filme=filme)
    
    @staticmethod
    def create_nota(usuario,filme,nota_atribuida_ao_filme):

        return Nota.objects.create(usuario=usuario,filme=filme,nota_atribuida_ao_filme=nota_atribuida_ao_filme)

    
class AluguelRepository:

    @staticmethod
    def get_filmes_alugados(usuario):
        return Aluguel.objects.filter(usuario=usuario).select_related('filme','usuario')
   
class UsuarioRepository:

    @staticmethod
    def get_usuario_by_email(email):
        return Usuario.objects.filter(email__iexact=email)
