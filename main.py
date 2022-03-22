import tkinter as tk
import random


class Komputer:
    def __init__(self):
        self.plansza = losujPlansze()
        self.lista_ruchow = [x + str(y) for x in "ABCDEFGHIJ" for y in range(1, 11)]
        random.shuffle(self.lista_ruchow)

    def ruch(self, plansza):
        x = self.lista_ruchow[-1]
        self.lista_ruchow.pop()
        while not sprawdz(plansza, x):
            x = self.lista_ruchow[-1]
            self.lista_ruchow.pop()
        if (w := strzal(plansza, x)) == 1:
            self.dodajruchy(x)
        return x, w

    def dodajruchy(self, x):
        x, y = rozloz(x)
        wyn = []
        if x > 0:
            wyn.append(zloz(x - 1, y))
        if x < 9:
            wyn.append(zloz(x + 1, y))
        if y > 0:
            wyn.append(zloz(x, y - 1))
        if y < 9:
            wyn.append(zloz(x, y + 1))
        random.shuffle(wyn)
        self.lista_ruchow.extend(wyn)


def ogwiazdkuj(M, x, y):
    for i in range(-1, 2):
        for ii in range(-1, 2):
            if 0 <= x + i <= 9 and 0 <= y + ii <= 9:
                if M[x + i][y + ii] == 0:
                    M[x + i][y + ii] = 8


def losStatek(M, x, y, rozmiar, krok):
    M[x][y] = rozmiar
    if krok == 1:
        ogwiazdkuj(M, x, y)
        return True
    nast = []
    if x > 0:
        if M[x - 1][y] == 0:
            nast.append([x - 1, y])
    if y > 0:
        if M[x][y - 1] == 0:
            nast.append([x, y - 1])
    if x < 9:
        if M[x + 1][y] == 0:
            nast.append([x + 1, y])
    if y < 9:
        if M[x][y + 1] == 0:
            nast.append([x, y + 1])
    if nast:
        random.shuffle(nast)

    for i in nast:
        if losStatek(M, i[0], i[1], rozmiar, krok - 1):
            ogwiazdkuj(M, x, y)
            return True

    M[x][y] = 0
    return False


def pustaPlansza():
    return [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0] for _ in range(0, 10)]


def losujPlansze():
    M = pustaPlansza()
    Statki = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    for i in Statki:
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        while M[x][y] != 0:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
        while not losStatek(M, x, y, i, i):
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            while M[x][y] != 0:
                x = random.randint(0, 9)
                y = random.randint(0, 9)
    for i in range(0, 10):
        for ii in range(0, 10):
            if M[i][ii] == 8:
                M[i][ii] = 0
    return M


def sprawdz(plansza, wspol):
    x, y = rozloz(wspol)
    if plansza[x][y] in (7, 8, 9):
        return False
    return True


def czyCaly(plansza, wx, wy):
    temp = [(wx, wy)]
    dodane = [(wx, wy)]
    plansza[wx][wy] = 9
    while temp:
        x = temp[0][0]
        y = temp[0][1]
        temp.pop(0)
        for i, ii in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            if 0 <= x + i <= 9 and 0 <= y + ii <= 9:
                if plansza[x + i][y + ii] in (1, 2, 3, 4):
                    return False
                if plansza[x + i][y + ii] == 9:
                    if (x + i, y + ii) not in dodane:
                        dodane.append((x + i, y + ii))
                        temp.append((x + i, y + ii))
    for i in dodane:
        ogwiazdkuj(plansza, i[0], i[1])
    return True


def strzal(plansza, wspol):
    x, y = rozloz(wspol)
    w = plansza[x][y]
    if w == 0:
        plansza[x][y] = 7
        return 0
    if czyCaly(plansza, x, y):
        return 2
    return 1


def rozloz(wspol):
    x = wspol[0]
    x = 'ABCDEFGHIJ'.index(x)
    y = int(wspol[1:]) - 1
    return y, x


def zloz(wy, wx):
    x = 'ABCDEFGHIJ'[wx]
    y = str(wy + 1)
    return x + y


def wypiszWspolrzedne(i, j):
    def func():
        wyn = zloz(i, j)
        global labInfo
        labInfo["text"] = wyn + '\n'

    return func


def strzalEkran(tabPrzecWartosci, tabPrzecPrzyciski, x, y, przeciwnik, tabGraczWart, tabGraczPrzyc):
    def func(*args):
        btnLosuj["text"] = "   Nowa gra   "
        global kompuStatkiZatopione
        global mojeStatkiZatopione
        if not kompuStatkiZatopione == 20 and not mojeStatkiZatopione == 20:
            if tabPrzecWartosci[x][y] > 4:
                labInfo["text"] = "Wybierz\ninne pole"
                return False

            z = zloz(x, y)
            wyn = strzal(tabPrzecWartosci, z)
            if wyn == 1:
                labInfo["text"] = "Trafiony!\n"
                tabPrzecPrzyciski[x][y]['text'] = 'X'
                tabPrzecPrzyciski[x][y]['background'] = 'red'
                tabPrzecPrzyciski[x][y]['activebackground'] = 'red4'
            else:
                if wyn == 0:
                    labInfo["text"] = "Pudło :c\n"
                else:
                    labInfo["text"] = "Trafiony...\n i zatopiony!"
                for b in range(10):
                    for bb in range(10):
                        if tabPrzecWartosci[b][bb] == 7:
                            tabPrzecPrzyciski[b][bb]['text'] = 'O'
                        elif tabPrzecWartosci[b][bb] == 8:
                            tabPrzecPrzyciski[b][bb]['text'] = '*'
                        elif tabPrzecWartosci[b][bb] == 9:
                            tabPrzecPrzyciski[b][bb]['text'] = 'X'
                            tabPrzecPrzyciski[b][bb]['background'] = 'gray19'
                            tabPrzecPrzyciski[b][bb]['foreground'] = 'white'
                            tabPrzecPrzyciski[b][bb]['activebackground'] = 'gray'
            if wyn > 0:
                kompuStatkiZatopione += 1
                if kompuStatkiZatopione == 20:
                    labInfo["text"] = "WYGRANA ^^"

                return
            wyn = 1
            while wyn:
                wyn = przeciwnik.ruch(tabGraczWart)
                wyn = wyn[1]
                for b in range(10):
                    for bb in range(10):
                        if tabGraczWart[b][bb] == 7:
                            tabGraczPrzyc[b][bb]['text'] = 'O'
                        elif tabGraczWart[b][bb] == 8:
                            tabGraczPrzyc[b][bb]['text'] = '*'
                        elif tabGraczWart[b][bb] == 9:
                            tabGraczPrzyc[b][bb]['text'] = 'X'
                            tabGraczPrzyc[b][bb]['background'] = 'gray19'
                            tabGraczPrzyc[b][bb]['foreground'] = 'white'
                            tabGraczPrzyc[b][bb]['activebackground'] = 'gray'
                if wyn:
                    mojeStatkiZatopione += 1
                    if mojeStatkiZatopione == 20:
                        labInfo["text"] = "Przegrałeś ;-;"
                        return

    return func


def nowaGra():
    btnLosuj["text"] = "Losuj plansze"
    btnLosuj.flash()
    print("LOS")
    tab = losujPlansze()
    global K
    K = Komputer()
    btb = pustaPlansza()
    global mojeStatkiZatopione
    mojeStatkiZatopione = 0
    global kompuStatkiZatopione
    kompuStatkiZatopione = 0
    for i in range(10):
        for j in range(10):
            t = tab[i][j]
            btb[i][j] = tk.Button(master=frameTwojaPlansza, background=kolor[t], activebackground=bgkol[t],
                                  command=wypiszWspolrzedne(i, j),
                                  width=3, height=1, text=' ', font=10)
            btb[i][j].grid(row=i, column=j)

    tab2 = K.plansza
    btb2 = pustaPlansza()
    for i in range(10):
        for j in range(10):
            t = tab2[i][j]
            btb2[i][j] = tk.Button(master=framePlanszaPrzeciwnika, background=kolor[0], activebackground=bgkol[0],
                                   width=3, height=1, text=' ', font=10)
            btb2[i][j]['command'] = strzalEkran(tab2, btb2, i, j, K, tab, btb)
            btb2[i][j].grid(row=i, column=j)
    labInfo["text"] = "Kliknij przycisk\n->"


window = tk.Tk()
window.title("Gra w Statki")
frameTwojaPlansza = tk.Frame(master=window)
framePodpisTwoja = tk.Frame(master=window)
framePlanszaPrzeciwnika = tk.Frame(master=window)
framePrzyciski = tk.Frame(master=window)
framePodpisPrzeciwnika = tk.Frame(master=window)

labTwojaPlansza = tk.Label(text="TWOJA PLANSZA", font=20, master=framePodpisTwoja)
labPlanszaPrzec = tk.Label(text="PLANSZA PRZECIWNIKA", font=20, master=framePodpisPrzeciwnika)
labVS = tk.Label(text='VS', font=('Arial', 40), master=framePrzyciski, width=5, height=5)
labInfo = tk.Label(text='Kliknij przycisk\n->', font=15, master=framePrzyciski)

labInfo.pack()
labVS.pack()
labTwojaPlansza.pack()
labPlanszaPrzec.pack()

tab = losujPlansze()
K = Komputer()
btb = pustaPlansza()
mojeStatkiZatopione = 0
kompuStatkiZatopione = 0
kolor = ('dodger blue', 'green2', 'yellow', 'dark orange', 'red')
bgkol = ['blue4', 'forest green', 'goldenrod', 'tomato2', 'red4']
for i in range(10):
    for j in range(10):
        t = tab[i][j]
        btb[i][j] = tk.Button(master=frameTwojaPlansza, background=kolor[t], activebackground=bgkol[t],
                              command=wypiszWspolrzedne(i, j), width=3, height=1, text=' ', font=10)
        btb[i][j].grid(row=i, column=j)

tab2 = K.plansza
btb2 = pustaPlansza()
for i in range(10):
    for j in range(10):
        t = tab2[i][j]
        btb2[i][j] = tk.Button(master=framePlanszaPrzeciwnika, background=kolor[0], activebackground=bgkol[0],
                               width=3, height=1, text=' ', font=10)
        btb2[i][j]['command'] = strzalEkran(tab2, btb2, i, j, K, tab, btb)
        btb2[i][j].grid(row=i, column=j)


btnLosuj = tk.Button(master=framePrzyciski, text="Losuj plansze", background=kolor[0], activebackground=bgkol[0],
                     font=15, command=nowaGra)
btnLosuj.pack()

frameTwojaPlansza.grid(row=1, column=0)
framePodpisTwoja.grid(row=0, column=0)
framePrzyciski.grid(row=1, column=1)
framePlanszaPrzeciwnika.grid(row=1, column=2)
framePodpisPrzeciwnika.grid(row=0, column=2)

window.mainloop()
