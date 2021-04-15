from lib import *
import golden as P


# Instrukcja obsługi programu
def info():
    instr='Instrukcja wprowadzania danych:\n'
    instr=instr+'Wzór - zmienne należy wpisać jako: x1,x2,...x5\n'
    instr=instr+'operator potęgowania - ** \n'
    instr=instr+'funkcja pierwiastkowania kwadratowego - sqrt()\n'
    instr=instr+'funkcja logarytmu - log10(), log(), log2()\n'
    instr=instr+'funkcje trygonometryczne - sin(),cos(),tan()\n'
    instr=instr+'********************\n'
    instr=instr+'Akceptowalny format danych:\n'
    instr=instr+'punk startowy: x1,x2\n'
    instr=instr+'P.kierunek: a1,a2\n'
    instr=instr+'długość przedziału: liczba całkowita dodatnia\n'
    return instr

# Klasa odpowiedzialna za tworzenie i obsługę aplikacji okienkowej
class Window(QWidget):
    # konstruktor inicjujący nowy obiekt
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Metoda złotego podziału')
        width = 1000
        height = 200
        self.setMinimumSize(width, height)

        # Tworzenie pól edytowalnych
        self.Wzor = QLineEdit()
        self.Punkt_Startowy = QLineEdit()
        self.kierunek = QLineEdit()
        self.Dlugosc_Przedzialu = QLineEdit()
        self.Epsilon = QLineEdit()
        self.Ilosc_Iteracji = QLineEdit()

        # Tworzenie obiektu graficznego
        self.figure=plt.figure()
        self.canvas=FigureCanvas(self.figure)
        self.toolbar=NavigationToolbar(self.canvas,self)

        # Podłączenie przycisków
        self.Oblicz = QPushButton("Oblicz")
        self.Wykres = QPushButton("Wykres")
        self.HELP = QPushButton("Pomoc")
        self.Funkcja_1 = QPushButton("(x1-2)**2 + (x2-2)**2")
        self.Funkcja_2 = QPushButton("exp(x1-x2)*x2-2*x1")
        self.Funkcja_3 = QPushButton("sin(x1*x2)-cos(x1)")
        self.Funkcja_4 = QPushButton("log(x2*x1)")
        self.Wyjscie = QTextEdit()

        #  Podział okna aplikacji na sekcje
        self.create_Dane_Wejsciowe()
        self.create_Kryteria_Stopu()
        self.create_Przykladowe_Funkcje()
        self.create_Pole_terminalu()

        # Ustawienie elementów w aplikacji na podanych pozycjacj
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.Dane_Wejsciowe, 1, 0)
        mainLayout.addWidget(self.Kryteria_Stopu, 1, 1)
        mainLayout.addWidget(self.Przykladowe_Funkcje, 2, 0, 2, 2)
        mainLayout.addWidget(self.Pole_terminalu,4,0,2,2)
        mainLayout.addWidget(self.Oblicz,6,0)
        mainLayout.addWidget(self.HELP,6,1)
        mainLayout.addWidget(self.canvas,1,4,4,1)
        mainLayout.addWidget(self.toolbar,5,4)
        self.setLayout(mainLayout)

        # Dodanie funkcji wciśnięcia przycisku
        self.Oblicz.clicked.connect(self.Submit)
        self.Oblicz.clicked.connect(self.Rysuj_Wykres)
        self.Funkcja_1.clicked.connect(self.Przypisz1)
        self.Funkcja_2.clicked.connect(self.Przypisz2)
        self.Funkcja_3.clicked.connect(self.Przypisz3)
        self.Funkcja_4.clicked.connect(self.Przypisz4)
        self.HELP.clicked.connect(self.Przypisz5)

        # Początkowe wpisanie wartości w pola tekstowe
        self.Epsilon.setText("0.0001")
        self.Ilosc_Iteracji.setText("100")
        self.Punkt_Startowy.setText('0,0')
        self.kierunek.setText('1,1')
        self.Dlugosc_Przedzialu.setText('10')
        self.Wyjscie.setText(info())

    # Działanie przycisku "Oblicz"
    def Submit(self):
        P.Clear()
        P.Wczytaj_Funkcje(self.Wzor.text())
        P.Wczytaj_Punk_Poczatkowy(self.Punkt_Startowy.text())
        P.Wczytaj_Kierunek(self.kierunek.text())

        # Asercja sprawdzająca zgodnośc wymiarów
        if (len(P.x_start)!=len(P.kier))or(len(P.x_start)!=P.N)or(len(P.kier)!=P.N):
            self.Wyjscie.setText('Niezgodność wymiarów (wzór, punkt startowy, wektor P.kierunkowy)!')
            self.figure.clear()
            return

        P.Dlugosc_Przedzialu(int(self.Dlugosc_Przedzialu.text()))
        P.EPS = float(self.Epsilon.text())
        P.MAX_ITER = int(self.Ilosc_Iteracji.text())

        self.Wyjscie.setText(P.zwroc_wynik())

    # Tworzenie pól w sekcji danych wejściowych
    def create_Dane_Wejsciowe(self):
        self.Dane_Wejsciowe = QGroupBox("Dane Wejściowe")

        layout = QFormLayout()
        layout.addRow("Wzor funkcji", self.Wzor)
        layout.addRow("Punkt startowy", self.Punkt_Startowy)
        layout.addRow("kierunek", self.kierunek)
        layout.addRow("Dlugość przedziału", self.Dlugosc_Przedzialu)
        self.Dane_Wejsciowe.setLayout(layout)

    # Tworzenie pól w sekcji kryterii stopu
    def create_Kryteria_Stopu(self):
        self.Kryteria_Stopu = QGroupBox("Kryteria Stopu")

        layout = QFormLayout()
        layout.addRow("Epsilon", self.Epsilon)
        layout.addRow("Ilość iteracji", self.Ilosc_Iteracji)
        self.Kryteria_Stopu.setLayout(layout)

    # Tworzenie pól w sekcji przykładowych funkcji
    def create_Przykladowe_Funkcje(self):
        self.Przykladowe_Funkcje = QGroupBox("Przykładowe funkcje")

        layout = QFormLayout()
        layout.addWidget(self.Funkcja_1)
        layout.addWidget(self.Funkcja_2)
        layout.addWidget(self.Funkcja_3)
        layout.addWidget(self.Funkcja_4)
        self.Przykladowe_Funkcje.setLayout(layout)

    # Tworzenie pola wyjsciowego
    def create_Pole_terminalu(self):
        self.Pole_terminalu = QGroupBox("Wyjście")

        layout = QFormLayout()
        layout.addWidget(self.Wyjscie)
        self.Pole_terminalu.setLayout(layout)

    # Przypisane wzoru 1 do pola funkcji
    def Przypisz1(self):
        self.Wzor.setText("(x1-2)**2 + (x2-2)**2")

    # Przypisane wzoru 2 do pola funkcji
    def Przypisz2(self):
        self.Wzor.setText("exp(x1-x2)*x2-2*x1")

    # Przypisane wzoru 3 do pola funkcji
    def Przypisz3(self):
        self.Wzor.setText("sin(x1*x2)-cos(x1)")

    # Przypisane wzoru 4 do pola funkcji
    def Przypisz4(self):
        self.Wzor.setText("log(x2*x1)")

    # Przypisane isntrukcji do pola wyjścia
    def Przypisz5(self):
        self.Wyjscie.setText(info())

    # Rysowanie wykresu dla przypadku n=2
    def Rysuj_Wykres(self):
        # sprawdzenie warunku n=2
        if P.N!=2 or len(P.x_start)!=2 or len(P.kier)!=2:
            # asercja sprawdzająca zgodność rozmiarów
            if (len(P.x_start)!=len(P.kier))or(len(P.x_start)!=P.N)or(len(P.kier)!=P.N):
                self.canvas.draw()
                self.figure.clear()
                return
            ax1=self.figure.add_subplot(111)
            text = ax1.text(0.5, 0.5, 'Wizualizacja dostępna tylko\n dla problemów \nn=2',
                ha='center', va='center', size=20)
            self.canvas.draw()
            self.figure.clear()
            return
        else: # wykonanie rysowania wykresu
            self.figure.clear()

            #dlugosc wektora na podstawie punktu poczatkowego i punktu koncowego
            dl_wek=sqrt((P.x_start[0]-P.x_stop[0])**2+(P.x_start[1]-P.x_stop[1])**2)

            # okresla wektor rysowania na podstawie wartosci współczynników wektora kierunku
            WZ=[0]*4
            if P.kier[0]>=0 and P.kier[1]>=0:
                WZ[0]=dl_wek
                WZ[3]=dl_wek
            elif P.kier[0]>=0 and P.kier[1]<=0:
                WZ[3]=dl_wek
                WZ[1]=dl_wek
            elif P.kier[0]<=0 and P.kier[1]<=0:
                WZ[1]=dl_wek
                WZ[2]=dl_wek
            elif P.kier[0]<=0 and P.kier[1] >= 0:
                WZ[0]=dl_wek
                WZ[2]=dl_wek

            # Ilosc punktów do losowania próbek z rozkładu jednostajego
            npts = 50000

            # Zbiór losowych punktów do określenia wartości f(x)
            x1_pom = np.random.uniform(-WZ[2]-abs(P.x_start[0]-1),WZ[3]+abs(P.x_start[0]+1),npts)
            x2_pom = np.random.uniform(-WZ[1]-abs(P.x_start[1]-1),WZ[0]+abs(P.x_start[1]+1), npts)

            # wyliczenie wartosci z zbioru -x;x -y;y jako dane do warstiwcy
            z=[]
            for i in range(len(x1_pom)):
                x1=x1_pom[i]
                x2=x2_pom[i]
                z.append(eval(P.wzor))
            x1 = x1_pom
            x2 = x2_pom


            ax1=self.figure.add_subplot(111)

            # Zageszczenie punktów (dokładność warstwicy)
            ngridx = 200
            ngridy = 200

            # Tworzenie siatki punktów
            xi = np.linspace(-WZ[2]-abs(P.x_start[0]-1),WZ[3]+abs(P.x_start[0]+1), ngridx)
            yi = np.linspace(-WZ[1]-abs(P.x_start[1]-1),WZ[0]+abs(P.x_start[1]+1), ngridy)

            # przygotowanie danych do rysowania warstwicy
            triang = tri.Triangulation(x1, x2)
            interpolator = tri.LinearTriInterpolator(triang, z)
            Xi, Yi = np.meshgrid(xi, yi)
            zi = interpolator(Xi, Yi)

            # warstwica
            ax1.contour(xi, yi, zi, levels=100, linewidths=0.5, colors='k')
            cntr1 = ax1.contourf(xi, yi, zi, levels=100, cmap="RdBu_r")


            # punkt do prostej P.kierunkowej
            P.x_start_values=[P.x_start[0],P.x_stop[0]]
            P.x_stop_values=[P.x_start[1],P.x_stop[1]]

            # kolejne punkty iteracyjne
            xii=[]
            yii=[]
            for i in range(P.iter):
                xii.append(P.TAB_OUT[i][0])
                yii.append(P.TAB_OUT[i][1])

            # punkty X,Y minimalne
            x_min=xii[-1]
            y_min=yii[-1]

            ax1.plot(P.x_start_values,P.x_stop_values,'lime') #linia kierunku
            ax1.plot(P.x_start[0],P.x_start[1],'kx',markersize=12,label='punkt startowy') # punkt startowy
            ax1.plot(xii,yii,'kx') # punkty iteracyjne
            ax1.plot(x_min,y_min,color='lime', marker='.',markersize=12,label='punkt końcowy') #punkt minimalny

            ax1.legend()
            self.figure.colorbar(cntr1, ax=ax1)
            ax1.set(xlim=(-WZ[2]-abs(P.x_start[0]-1),WZ[3]+abs(P.x_start[0]+1)), ylim=(-WZ[1]-abs(P.x_start[1]-1),WZ[0]+abs(P.x_start[1]+1))) #to ustawia szerokosc plota
            self.canvas.draw()


################################################
#### Tworzenie obiketu i wyświetlenie go #######
################################################
app = QApplication([])
w = Window()
w.show()
app.exec()
