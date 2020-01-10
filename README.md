# Resolvendo o Set Cover com OpenSolver e Pyomo

A ideia deste exercício é resolver o problema da cobertura de conjuntos, utilizando o Pyomo  (http://www.pyomo.org/) e o OpenSolver (www.opensolver.org).

O Set cover é o problema de cobertura de conjuntos.

Tenho uma quantidade de elementos, digamos 50.

E tenho uma quantidade de conjuntos, digamos 15.

Cada conjunto tem um preço (abaixo está como peso), e cada conjunto contém os elementos.

Algumas aplicações: imagine que há várias doenças, e uma série de vacinas. Cada vacina cobre um conjunto diferente de doenças, e cada vacina tem um custo. Minimizar o custo total, cobrindo todas as doenças.

![](https://forgottenmathhome.files.wordpress.com/2020/01/set01.jpg)

## Open Solver:

Variável de decisão binária: utilizo ou não o conjunto.

Função objetivo: se utilizo o conjunto, é o preço deste.

Restrição: devo cobrir todos os elementos.
![](https://forgottenmathhome.files.wordpress.com/2020/01/set02.jpg)

Resultado: FO de 223 e as escolhas pintadas em rosa.
![](https://forgottenmathhome.files.wordpress.com/2020/01/set03.jpg)

## Formulação Pyomo:

Leitura de dados utilizando o módulo pandas.

    df1 = pd.read_excel(io='SetCover_Instancia01.xlsm', sheet_name='Base', usecols = "B:P", skiprows = 1, nrows = 1,header = None)

    df2 = pd.read_excel(io='SetCover_Instancia01.xlsm', sheet_name='Base', usecols = "B:P", skiprows = 7, header = None)

    Nsets =  len(df1.columns)

    Nelementos =  len(df2)

Crio o model com o primeiro comando abaixo. Defino os índices (conjuntos e elementos).

   #---------------- Modelo Pyomo ------------#     

    model = ConcreteModel()

    model.S = list(range(0,Nsets)) #Num sets

    model.E = list(range(0,Nelementos)) #Num elementos

Defino a variável de decisão com o comando Var. O nome da variável é AtivaSet, ela é binária e inicializa com o valor zero.

    model.AtivaSet = Var(model.S, within=Binary, initialize=0)

Função objetivo.

Soma do produto entre a variável de decisão e o peso de cada conjunto.

def obj_rule(model):

        return sum(model.AtivaSet[s]*pesos[s] for s in model.S)

model.obj = Objective(rule = obj_rule, sense=minimize)

Restrição.

Para cada elemento, ele deve pertencer a um conjunto, ou seja, a soma do produto da matriz de alocação e a variável de decisão devem ser maior do que 1.

    def constrAlocacao(model, e):

        return sum(model.AtivaSet[s]*Malocacao[e][s] for s in model.S) >= 1

    model.restr1 = Constraint(model.E, rule = constrAlocacao)      

Algumas configurações do solver, e depois mando resolver

    SOLVER_NAME = 'cbc'

    TIME_LIMIT = 60*1   #Em segundos

    solver = SolverFactory(SOLVER_NAME)

    solver.options['seconds'] = TIME_LIMIT

    results  = solver.solve(model)

    results.write() #para mostrar o status da solucao

![](https://forgottenmathhome.files.wordpress.com/2020/01/set04.png)

O resultado obtido foi o mesmo do OpenSolver.

Além do CBC, outro solver free é o GLPK.

Todos os outros são pagos. O Pyomo pode chamar CPLEX, Gurobi, se tiver a licença destes.

Toda a manipulação de entrada de dados, matrizes, e saída de dados, é Python puro.

Vantagens: é free, e muito melhor que o Open Solver para manipular grande quantidade de dados.

Desvantagens: requer um grau maior de conhecimento que o OpenSolver. Não é tão fácil de manipular ou tão poderoso quanto um AIMMS + CPLEX.
