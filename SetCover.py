# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 16:38:39 2020

@author: asgun
"""
import pandas as pd
import numpy as np
from pyomo.environ import *


def SetCover():
    #---------------- Leitura de  Dados ------------#
    df1 = pd.read_excel(io='SetCover_Instancia01.xlsm', sheet_name='Base', usecols = "B:P", skiprows = 1, nrows = 1,header = None)
    df2 = pd.read_excel(io='SetCover_Instancia01.xlsm', sheet_name='Base', usecols = "B:P", skiprows = 7, header = None)
    
    Nsets =  len(df1.columns)
    Nelementos =  len(df2)

    pesos = []
    Malocacao =[]

    #Lê pesos e joga numa lista
    for j in range(Nsets):
        pesos.append(df1.iloc[0,j])

    #Popula matriz de alocacao
    for i in range(Nelementos):
        m1=[]
        for j in range(Nsets):
            m1.append(df2.iloc[i,j])
        Malocacao.append(m1)
        
    #print(Malocacao[0][0])
    
    
    #Parametros do solver
#    SOLVER_NAME = 'glpk'
    SOLVER_NAME = 'cbc'
    TIME_LIMIT = 60*1   #Em segundos

      #---------------- Modelo Pyomo ------------#      
    model = ConcreteModel()
    
    model.S = list(range(0,Nsets)) #Num sets
    model.E = list(range(0,Nelementos)) #Num elementos
    
        
    #Variável de alocação binária
    #Qual Set será escolhido ou não
    model.AtivaSet = Var(model.S, within=Binary, initialize=0)
       
    def obj_rule(model):
        return sum(model.AtivaSet[s]*pesos[s] for s in model.S)
    model.obj = Objective(rule = obj_rule, sense=minimize)
#    
#    #Cada elemento deve estar num set
    def constrAlocacao(model, e):
        return sum(model.AtivaSet[s]*Malocacao[e][s] for s in model.S) >= 1
    model.restr1 = Constraint(model.E, rule = constrAlocacao)


    #Configuracoes do solver   
    solver = SolverFactory(SOLVER_NAME)
    
    if SOLVER_NAME == 'cplex':
        solver.options['timelimit'] = TIME_LIMIT
    elif SOLVER_NAME == 'glpk':         
        solver.options['tmlim'] = TIME_LIMIT
    elif SOLVER_NAME == 'gurobi':           
        solver.options['TimeLimit'] = TIME_LIMIT
    elif SOLVER_NAME == 'cbc':
        solver.options['seconds'] = TIME_LIMIT
        
        
    results  = solver.solve(model)
    results.write() #para mostrar o status da solucao
#    print("pprint")
#    model.Aloc.pprint()
    
    print("---------------")
#    
    
#    #---------------- Exportação de resultados ------------#      
    dfOut = pd.DataFrame()
    count = 0

    xOut = np.zeros([Nsets])

    for s in model.S:
        xOut[s] = value(model.AtivaSet[s])

    dfOut = pd.DataFrame(xOut)
    dfOut = dfOut.fillna(0)
    dfOut = dfOut.astype(int)
    dfOut.to_csv (r'C:\CombOpt\Exercicios\SetCover\sol.csv', index = None, sep=';', header=False)

    
    print("Concluído")
    
    
if __name__ == "__main__":    
    SetCover()

