import random

# Een dictionary met het aantal dagen die de medewerkers willen werken en de beschikbare dagen.
werknemers = {
    "Sanne": {"aantal_dagen": 3, "beschikbare_dagen": [1, 4, 6]},
    "Noah": {"aantal_dagen": 2, "beschikbare_dagen": [6, 7]},
    "Sacha": {"aantal_dagen": 2, "beschikbare_dagen": [5, 6]},
    "Brian": {"aantal_dagen": 3, "beschikbare_dagen": [2, 3, 6]},
    "Charissa": {"aantal_dagen": 2, "beschikbare_dagen": [1, 2]},
    "Joris": {"aantal_dagen": 3, "beschikbare_dagen": [3, 5, 7]},
    "Kyra": {"aantal_dagen": 4, "beschikbare_dagen": [1, 3, 5, 7]},
    "Niek": {"aantal_dagen": 3, "beschikbare_dagen": [1, 2, 6]}
}

dagen_in_week = 7
min_personeel = 2
max_personeel = 4

# Algemene parameters
populatie_grootte = 100
aantal_generaties = 100
selectie_percentage = 0.5
kruising_kans = 0.8
mutatie_kans = 0.1


# Stap 1: maak individu m.b.v. random choice
def maak_individu():
    individu = {}
    for werknemer, gegevens in werknemers.items():
        individu[werknemer] = random.sample(gegevens["beschikbare_dagen"], gegevens["aantal_dagen"])
    return individu


# populatie wordt gemaakt en in een lijst gezet.
def maak_populatie(populatie_grootte):
    populatie = []
    for _ in range(populatie_grootte):  # exacte waarde is niet van belang, het wordt niet verder gebruikt.
        individu = maak_individu()
        populatie.append(individu)
    return populatie
print(maak_populatie(populatie_grootte))

# Stap 3: Evalueer de fitness
def bereken_fitness(individu):
    overtredingen = 0
    # Voor elke werknemer in het individu controleren we of de werknemer op de huidige dag aanwezig is.
    for dag in range(1, dagen_in_week + 1):
        personeel_beschikbaar= 0
        for werknemer in individu:
            for beschikbare_dag in individu[werknemer]:
                if dag == beschikbare_dag:
                    personeel_beschikbaar += 1
        if personeel_beschikbaar < min_personeel or personeel_beschikbaar > max_personeel:
            overtredingen += 1
    # individuen met minder overtredingen krijgen een hogere fitnesswaarde door inverse van overtreding te nemen
    return 1 / (overtredingen + 1)  # Hoe hoger de fitness, hoe beter het individu


#hierbij wordt het totaal fitness bepaald van alle individu in de populatie
def totaal_fitness(populatie):
    totaal_fitness = 0
    for individu in populatie:
        totaal_fitness += bereken_fitness(individu)
    return totaal_fitness

def selecteer_individuen(populatie, fitness_scores):
    cumulatieve_kanslijst = []  # cumulatieve kansen voor elk individu worden berekend
    cumulatieve_kans = 0
    for fitness in fitness_scores:
        cumulatieve_kans += fitness / totaal_fitness(populatie) #de selectiekansen wordt opgebouwd foor elk individu op te tellen
        cumulatieve_kanslijst.append(cumulatieve_kans)
    #random getal nemen tussen 0 en 1
    willekeurige_getal = random.uniform(0, 1)
    individu = None #geselecteerde individu

    for i in range(len(cumulatieve_kanslijst)):
        if cumulatieve_kanslijst[i] >  willekeurige_getal:
            individu = populatie[i]
            break
    return individu

def kruiding(vader, moeder):
    # een willekeurig punt kiezen voor de eenpuntkruising
    willekeurig_punt = random.randint(1, len(vader) - 1)

    #kinderen zijn de copies van de ouders
    kind1 = vader.copy()
    kind2 = moeder.copy()

    kind1[willekeurig_punt:] = vader[willekeurig_punt:]
    kind2[willekeurig_punt:] = moeder[willekeurig_punt:]

    return kind1, kind2






