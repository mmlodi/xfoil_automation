import os
import numpy as np
from pyDOE import *



#Cria um sampling baseado no método Latin Hyper-Cube para M e P variando de 1-8 e 
def criaSampling():
    lb = np.array([0.5,0.5,6.5])
    ub = np.array([9.5,9.5,15.5])

    sampling = lhs(3,9,criterion="center")*(ub-lb) + lb
    sampling = np.around(sampling)
    sampling = sampling.astype(int)
    print(sampling)

    return sampling

#Cria um arquivo para ser executado dentro do XFoil
def escreveCodigo(Re, M, P, T):
    alfa_ini = -5
    alfa_fim = 20
    if T < 10:
        cmd = ["naca\n",str(M),str(P),"0",str(T),"\n","oper\n","visc ", str(Re),"\n","pacc\n","reslXfoil/","result.","naca.",str(M),str(P),"0",str(T),".",str("{:.1e}".format(Re)),"\n\n","aseq ", str(alfa_ini)+" ", str(alfa_fim)+" ", "1 ", " \n\n\n","quit()\n"]
        nome = "Naca"+str(M)+str(P)+"0"+str(T)
    else:
        cmd = ["naca\n",str(M),str(P),str(T),"\n","oper\n","visc ", str(Re),"\n","pacc\n","reslXfoil/","result.","naca.",str(M),str(P),str(T),".",str("{:.1e}".format(Re)),"\n\n","aseq ", str(alfa_ini)+" ", str(alfa_fim)+" ", "1 ", " \n\n\n","quit()\n"]
        nome = "Naca"+str(M)+str(P)+str(T)

    with open(dirNameCmd+"/"+"cmd"+nome,'a') as f:
        for line in cmd:
            f.write(line)
    f.close()

    return "cmd"+nome

#Executa todos os códigos gerados na pasta "cmdsXfoil"
def executaCodigo(Re): 
    sampl = criaSampling()

    for i in range(len(sampl)-1):
        nomeCmd = escreveCodigo(Re,sampl[i][0],sampl[i][1],sampl[i][2])
        os.system("xfoil < "+dirNameCmd+"/"+nomeCmd)

#Essa função encontra o Cl máximo de um dado arquivo na pasta "reslXfoil"
def encontraClMax(file):
    f = open("reslXfoil/"+file,"r")
    lines = f.readlines()
    f.close()

    del lines[0:12]

    result = []

    for x in lines:
        result.append(x.split('  ')[2])

    result = np.array(result)
    res = result.astype(float)

    return np.amax(res)

#remove a pasta gerada com os últimos arquivos !!! Cuidado apaga tudo
try:
    os.system("rm -r cmdsXfoil")
    os.system("rm -r reslXfoil")
except:
    print("A(s) pasta(s) não existem")


dirNameCmd = "cmdsXfoil"
dirNameRes = "reslXfoil"

#Cria novos diretórios e confere se os ultimos foram apagados
try:
    # Create target Directory
    os.mkdir(dirNameCmd)
    os.mkdir(dirNameRes)
    print("Directory " , dirNameCmd," and ", dirNameRes ,  " Created ") 
except FileExistsError:
    print("Directory " , dirNameCmd," or ", dirNameRes ,  " already exists")



executaCodigo(1e7)