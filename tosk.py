#from math import sum
# f = open("00-example.txt", "r")
#f = open("01-the-cloud-abyss.txt", "r")
#f = open("02-iot-island-of-terror.txt", "r")
# f = open("03-etheryum.txt", "r")
# f = open("04-the-desert-of-autonomous-machines.txt", "r")
f = open("05-androids-armageddon.txt", "r")
output = open("outputFile-05.txt", "w")

# read first line
first_line = f.readline().split()

stamina_I = int(first_line[0])
max_stamina = int(first_line[1])
turn = int(first_line[2])
deamon_D = int(first_line[3])

#stamina corrente
stamina_Corrente = stamina_I

# non si possono risfidare
lista_sfidati = []

#score totale
total_score = 0

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

f.close() # chiudo file input dopo parsing dati
# calcolo punteggio finale
# Given a list E of N defeated enemies, 
# T -> number of turns in the simulation
# E = [E0, E1, ..., En-1] -> enemy
# T = [T0, T1, ..., Tn-1] -> turn in which the Ei enemy is defeated
# AE0 = [A0, A1, ..., An] -> reward array for enemy E0
# AE1 = [A0, A1, ..., Am] -> reward array for enemy E1

# En nemico
def punteggio_parziale(En, T, Tn): # An --> list of fragments for the n-th enemy
    An = En.punti_int 
    partial_score = 0
    upperParameter = min(len(An), (T-Tn))-1
    # int(len(An)) < int(T-Tn) if int(len(An)) else int(T - Tn)

    # print("upper "+str(upperParameter))

    # total reward R is the sum of all the scores:
    for i in range(upperParameter):
        partial_score += An[i]
        
    return partial_score
    
################# METODI PER SCEGLIERE DEMONE


def find_best_fit(lista_sfidabili, stamina_Corrente):
    
    max_score = 0

    bestDemon = lista_sfidabili[0]

    for sfidabile in lista_sfidabili:
        #stima valore del demone
        score = sfidabile.stamina_recuperata / sfidabile.turni_recupero * sum(sfidabile.punti_int)
        if(score > max_score):
            bestDemon = sfidabile
        
    return bestDemon

def find_sfidabili():

    lista_sfidabili = []

    for sfidabile in demons:
        if(sfidabile.stamina_consumata <= stamina_Corrente ):# and (sfidabile not in lista_sfidati)):
            lista_sfidabili.append(sfidabile)

    return lista_sfidabili


def chooseBestDemon(stamina_Corrente):
    sfidabili = find_sfidabili()

    if(sfidabili == []) :
        return None
    
    bestDemon = find_best_fit(sfidabili, stamina_Corrente)

    return bestDemon


###################### SISTEMA GIOCO

def calcola_Stamina(stamina_recovers, t, stamina_Corrente):
    
    new_stamina_recovers = []

    for stamina_recover in stamina_recovers:
        if(stamina_recover[0] == t):
            stamina_Corrente += stamina_recover[1]
        else:
            new_stamina_recovers.append(stamina_recover)

    if(stamina_Corrente > max_stamina):
        return max_stamina, new_stamina_recovers
    else:
        return stamina_Corrente, new_stamina_recovers



stamina_recovers = []
# for over all the turns
for t in range(turn):
    
    print("TURNO:"+ str(t))

    demon = chooseBestDemon(stamina_Corrente)

    if(demon):
        #lista_sfidati.append(demon)

        # print("DEMON INDEX "+ str(demon.index))
        #print(lista_sfidati)

        stamina_Corrente = stamina_Corrente - demon.stamina_consumata
        # print("stamina consumata"+ str(demon.stamina_consumata))
        #stampo demone
        output.write(str(demon.index)+"\n")

        stamina_recovers.append([t+demon.turni_recupero, demon.stamina_recuperata])
        #print(stamina_recovers)
        partial_score = punteggio_parziale(demon, turn, t)
        total_score += partial_score
        demons.remove(demon)
    
     print("SCORE: "+str(total_score))
    print("stamina corrente: "+ str(stamina_Corrente))
    stamina_Corrente, stamina_recovers = calcola_Stamina(stamina_recovers, t, stamina_Corrente)

output.flush()  
output.close()
