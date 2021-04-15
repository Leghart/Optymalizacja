from lib import *


#================= zmienne globalne ===============
MAX_ITER=100
EPS=0.0001 #epsilon

# poczatkowe zmienne
x1=0
x2=0
x3=0
x4=0
x5=0

wzor = ''
N = 0 # wymiar zadania
x_start =[]
x_stop = []
kier = [] #kieruek
dl_przedzialu = 0
iter = 0
out_dekompoz=[]
TAB_OUT=[] # lsta wynków ze złotego podziału
ACC=7 #dokładność wyświetlania danych

# czyszcenie zmiennych do ponowego użycia programu
def Clear():
    global wzor,N,x_start,x_stop,kier,dl_przedzialu,out_dekompoz,TAB_OUT

    wzor = ''
    N = 0
    x_start =[]
    x_stop = []
    kier = []
    dl_przedzialu = 0
    iter = 0
    out_dekompoz=[]
    TAB_OUT=[]

# Funkcja licząca zmienne we wzorze, zwraca wymiar zadania
def Roz_wzor(string):
    data=[]
    for i in range(len(string)):
        if string[i]=='x':
            if string[i+1]!='p':
                data.append(string[i+1])

    odp=[]
    for i in data:
        if i not in odp:
            odp.append(i)

    return len(odp)

# Wczytanie funkcji z aplikacji oraz okreslenie wymiaru zadania
def Wczytaj_Funkcje(F):
    global wzor,N
    wzor = F
    N=Roz_wzor(wzor)

# Wczytanie do zmiennej globalenj punktu początkowego
def Wczytaj_Punk_Poczatkowy(P):
    global N,string,x_start
    string=P.split(',')
    for i in string:
        x_start.append(float(i))

# Wczytanie do zmiennej globalenj wektora kierunku
def Wczytaj_Kierunek(K):
    global kier
    string=K.split(',')
    for i in string:
        kier.append(float(i))

# Wczytanie do zmiennej globalenj dlugosci przedzialu
def Dlugosc_Przedzialu(DP):
    global dl_przedzialu,x_stop
    dl_przedzialu = DP

    for i in range(N):
        x_stop.append(x_start[i]+kier[i]*dl_przedzialu)



def f(kier,x0,alfa):
    global x1,x2,x3,x4,x5,out_dekompoz
    out_dekompoz=dekompozycja(kier,x0,alfa)

    ustaw_x(out_dekompoz)
    exe=eval(wzor)
    return exe

# funkcja zmieniająca problem n wymiarowy w jeden wymiar
def dekompozycja(kier,x0,alfa):
    odp=[]
    for i in range(len(kier)):
        odp.append(x0[i]+kier[i]*alfa)
    return odp

# ustawia do zmiennych globalnych wartosci x z dostępnego wektora
def ustaw_x(x):
    global x1,x2,x3,x4,x5,x6
    try:
        x1=x[0]
        x2=x[1]
        x3=x[2]
        x4=x[3]
        x5=x[4]
        x6=x[5]
    except IndexError:
        pass

# Algorytm złotego podziału
def golden_method(a,b):
    global kier,x_start,TAB_OUT

    x0=x_start
    k=(sqrt(5)-1)/2

    alfa_L=b-k*(b-a)
    alfa_R=a+k*(b-a)
    iter=0
    while((alfa_R-alfa_L)>EPS and MAX_ITER>=iter):
        iter+=1
        if f(kier,x0,alfa_L) < f(kier,x0,alfa_R):
            f(kier,x0,alfa_L)
            TAB_OUT.append(out_dekompoz)
            b=alfa_R
            alfa_R=alfa_L
            alfa_L=b-k*(b-a)
        else:
            f(kier,x0,alfa_R)
            TAB_OUT.append(out_dekompoz)
            a=alfa_L
            alfa_L=alfa_R
            alfa_R=a+k*(b-a)

    return (a+b)/2 , iter



def zwroc_wynik():
    global iter
    wynik,iter=golden_method(0,dl_przedzialu)
    odp=[]
    for i in range(N):
        odp.append(round(x_start[i]+kier[i]*wynik,ACC))

    pom=''
    string = ''
    wek = []
    for i in range(iter):
        wek = (TAB_OUT[i])
        ustaw_x(wek)
        pom = pom+'('+str(i+1)+') '+"f("+str(np.around(TAB_OUT[i],decimals=ACC))+")= "+str(round(eval(wzor),ACC))+'\n'
    ustaw_x(odp)
    pom=pom+"\n######## Rozwiązanie optymalne ##########\n"
    for i in range(N):
        string = string + "x"+str(i+1)+"*= "+str(round(odp[i],ACC))+"\n"
    string = string + "f("
    for i in range(N):
        string = string + "x"+str(i+1)+"*, "
    string = string[:-2]
    string = string + ")= "+str(round(eval(wzor),12))
    return pom + string
