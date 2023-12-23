import tmdbsimple as tmdb
import textwrap
from googletrans import Translator

# Substitua '637be11ed63ff436f5435f576973d0a2' pela sua chave de API do TMDb
tmdb.API_KEY = '637be11ed63ff436f5435f576973d0a2'

# Consulta à API para obter os 50 melhores filmes
top_50_filmes = []

for page in range(1, 4):  # 3 páginas para obter 60 filmes (20 por página)
    try:
        top_rated_movies = tmdb.Movies().top_rated(page=page)
        top_50_filmes.extend(top_rated_movies['results'])
    except Exception as e:
        print(f"Erro ao obter filmes da página {page}: {e}")

# Inicializa o tradutor do Google
translator = Translator()

if top_50_filmes:
    for i, movie in enumerate(top_50_filmes[:50], start=1):
        titulo = movie['title']  # Título em inglês

        # Tente traduzir o título para o português
        titulo_portugues = translator.translate(titulo, src='en', dest='pt').text

        # Obtém a data de lançamento do filme
        lancamento = movie['release_date']

        # Inverte a data no formato 'aaaa-mm-dd' para 'dd/mm/aaaa'
        parts = lancamento.split('-')
        inverte_data = "/".join(reversed(parts)) if len(parts) == 3 else "Data não disponível"

        # Obtém a sinopse em inglês
        overview = movie['overview']

        # Traduz a sinopse para o português
        overview_translated = translator.translate(overview, src='en', dest='pt').text

        # Quebra o overview traduzido em linhas de 60 caracteres
        overview_lines = textwrap.wrap(overview_translated, width=60)

        print("\033[33m{}.\033[32m Título: \033[36m{}".format(i, titulo_portugues))
        print("   \033[32mData de lançamento: \033[36m{}".format(inverte_data))
        print("   \033[32mClassificação média: \033[36m{}".format(movie['vote_average']))
        print("   \033[32mSinopse:")
        for line in overview_lines:
            print("   \033[37m{}".format(line))
        print("-" * 40)
else:
    print("\033[31mErro ao acessar a lista dos 50 melhores filmes no TMDb.\033[m")
