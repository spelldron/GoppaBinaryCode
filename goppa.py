import random
import numpy as np

def ToSix(x):
    if len(x) <= 6:
        while len(x) != 6:
            x = '0' + x
    return x
 
def ConvertForH(mas, lenth):
    i = 0
    BinMas = []
    while i != len(mas):
        x = mas[i]
        x = bin(x)
        x = x[2:]
        x = ToSix(x)
        BinMas.append(x)
        i += 1
    i = 0
    matrix = []
    while i != 6:
        j = 0
        m = []
        while j != lenth:
            m.append(0)
            j += 1
        matrix.append(m)
        i += 1
    i = 0
    while i != len(BinMas):
        j = 0
        while j != len(BinMas[i]):
            matrix[j][i] = int(BinMas[i][j])
            j += 1
        i += 1
    i = 0
    while i != len(matrix):
        i += 1
    return matrix

def GenMessage(lenth):
    i = 0
    massege = []
    while i != lenth:
        x = random.random()
        if x > 0.5:
            x = 1
        else:
            x = 0
        massege.append(x)
        i += 1
    return massege

def Encrypt(m, G):
    m = matrix(m)
    res = m*G
    return res
 
def Decrypt(m, k ):
    mes = m.list()
    mes = mes[:k]
    return mes
    
def GenC(g):
    g.reverse()
    matr = []
    for i in range(0, len(g)-1):
        row = []
        j = 0
        while j<i:
            row.append(0)
            j+=1
        row.extend(g[0:len(g)-j-1])
        matr.append(row)
    g.reverse()
    return matr

def GenX(a, g, t):
    i = 0
    matr = []
    while i != len(g):
        j = 0
        mas = a[:]
        while j != len(mas):
            mas[j] = pow(mas[j], t)
            j += 1
        if i != 0:
            matr.append(mas)
        t -= 1
        i += 1
    return matr
 
def GenY(y, n):
    i = 0
    matrix = []
    while i != n:
        j = 0
        m = []
        while j != n:
            m.append(0)
            j += 1
        matrix.append(m)
        i += 1
    i = 0
    j = 0
    while i != n:
        matrix[i][j] = y[i]
        i += 1
        j += 1
    return matrix

def MassToPolinom(mas):
    i = 0
    s = 0
    j = len(mas)-1
    while i != len(mas):
        if mas[i]==1:
            s+=x^j
        i+=1
        j-=1
    return s

def MassToPolinomIra(mas):
    s = 0
    for i in range(len(mas)):
        s+=mas[i]*x^i
    return s

def singromIra(y, alpha, g):
    s = 0
    for i in range(len(y)):
        nod, elem, elem1 = xgcd(x-alpha[i], g)
        s+=y[i]*elem
    return s

def GenE(V):
    V2 = V.list()
    x = random.randint(0, len(V2)-1)
    print(x)
    V2[x] = (V2[x]+1)%2
    V2 = matrix(V2)
    return V2
 
F = GF(2 ^ 6)
R.<x> = F[]
g = x^5+x^4+x^2+x+1
t = g.degree() # степень полинома
L = [F.list()[i] for i in range(1, 64)]
n = len(L)
matrC = GenC(g.list())
mc = Matrix(matrC)
matrX = GenX(L, g.list(), t)
mx = Matrix(matrX)
h = [(g(elem)) ** (-1) for elem in L] # h для матрицы Y (matrY)
matrY = GenY(h, n)
my = Matrix(matrY)
if mc.determinant()!=0:
    mh = mx * my
else:
    mh = mc * mx * my
matrH = [[]]
for row in list(mh):#конвертируем H из альф в числа
    new_row = [elem.integer_representation() for elem in list(row)]
    matrH.extend(ConvertForH(new_row, n ))
matrH.pop(0)# после этой строчки получается H в конечном варианте
matrH.reverse()
r = len(matrH)
k = n - r
mh = matrix(matrH).mod(2)
mg = mh.right_kernel().basis_matrix()
matrG = list(mg)
 
word = GenMessage(k)
enc = Encrypt(word, mg)
enc = GenE(enc)

sind = singromIra(enc.list(), L, g)
anyOne, Tx, anyTwo = xgcd(sind, g)
Hx = (Tx + x).mod(g)
Ax, Bx, an = xgcd(Hx, g)
 
Sigma = Ax + ((Bx))*x
B = [i for i in range(len(L)) if Sigma(L[i])==0]
i = 0
encList = enc.list()
while i != len(B):
    encList[B[i]] = (encList[B[i]]+1)%2
    i+=1
encList = matrix(encList)
dec = Decrypt(encList, k)

