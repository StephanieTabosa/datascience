#Autor: Stèphanie Rêgo Barreto Tabosa -> projeto de bottle
#Conjunto de importacoes
from bottle import default_app, template, request, post, get
from sklearn.svm import SVC
import joblib

#Definição das possíveis rotas para a função de callback

@get('/')
@get('/form/')
def index():
     #Definição de valores iniciais para as expressões animal, classificação e probabilidade
     return template('/home/stephanierbt/mysite/formulario.html', intencao = "-", classificacao = "-", probabilidade = "-")

#Definição da rota e função de callback
@post('/form/')
def index_resposta():
    #Pega os valores informados no formulário e atribui a variaveis locais
    intencao = request.forms.get('intencao')
    valor = request.forms.get('valor')
    consumo_por_litro = request.forms.get('consumo_por_litro')
    tempo_transito = request.forms.get('tempo_transito')
    seguranca = request.forms.get('seguranca')
    viagem_familia = request.forms.get('viagem_familia')
    impacto_clima = request.forms.get('impacto_clima')



    modelo_SVM = SVC(kernel = 'linear', random_state = 42, probability=True)
    #Carrega o modelo gerado
    modelo_SVM = joblib.load('/home/stephanierbt/mysite/modelo_carroMoto_MSVM.pkl')
    #Executa a classificação
    res = modelo_SVM.predict([[int(valor), float(consumo_por_litro), int(tempo_transito), int(seguranca),
                            int(viagem_familia), int(impacto_clima)]])

    #Encontra o valor da confidência
    probabilidade = modelo_SVM.predict_proba([[int(valor), float(consumo_por_litro), int(tempo_transito), int(seguranca),
                            int(viagem_familia), int(impacto_clima)]])

    if res == 0:
        classificacao = "Carro"
    elif res == 1:
        classificacao = "Moto"
    else:
        classificacao = "Especificações não foram corretamente preenchidas. Valor não calculado."

    #Renderiza o template com os valores passados como argumento
    return template('/home/stephanierbt/mysite/formulario.html', intencao = intencao, classificacao = classificacao, probabilidade = probabilidade)
    #return template('/home/stephanieml/mysite/formulario.html', animal = animal, classificacao = classificacao)

application = default_app()