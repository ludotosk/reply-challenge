f = open("00-example.txt", "r")

# read first line
first_line = f.readline().split()

stamina_I = int(first_line[0])
max_stamina = int(first_line[1])
turn = int(first_line[2])
deamon_D = int(first_line[3])

# classe demoni
class Deamon:
    def __init__(self, index, stamina_consumata, turni_recupero, stamina_recuperata, turni_guadagno_frammenti, punti):
        self.index = int(index)
        self.stamina_consumata = int(stamina_consumata)
        self.turni_recupero = int(turni_recupero)
        self.stamina_recuperata = int(stamina_recuperata)
        self.turni_guadagno_frammenti = int(turni_guadagno_frammenti)
        self.punti_int = []
        frammenti_demone = 0 # contralla di non aver più frammenti dei turni disponibili
        for p in punti:
            print(frammenti_demone)
            if (frammenti_demone < turn - 1):
                self.punti_int.append(int(p))
                frammenti_demone += 1
            else:
                break

# create list of deamons
demons = []
for i in range(deamon_D):
    elements = f.readline().split()
    demons.append(Deamon(i, elements[0], elements[1], elements[2], elements[3], elements[4:]))