import random

werknemers = {
    "Sanne": {"aantal_dagen": 2, "beschikbare_dagen": [1, 6]},
    "Noah": {"aantal_dagen": 4, "beschikbare_dagen": [6, 7, 2, 4]},
    "Sacha": {"aantal_dagen": 4, "beschikbare_dagen": [5, 7, 2, 1]},
    "Brian": {"aantal_dagen": 4, "beschikbare_dagen": [2, 3, 6, 1]},
    "Charissa": {"aantal_dagen": 2, "beschikbare_dagen": [1, 2]},
    "Joris": {"aantal_dagen": 4, "beschikbare_dagen": [3, 5, 6, 7]},
    "Kyra": {"aantal_dagen": 3, "beschikbare_dagen": [1, 5, 7]},
    "Niek": {"aantal_dagen": 3, "beschikbare_dagen": [1, 2, 6]}
}

dagen_in_week = 7
min_personeel = 2
max_personeel = 4

populatie_grootte = 100
aantal_generaties = 1000
selectie_percentage = 0.5
kruising_kans = 0.8
mutatiekans = 0.001

def maak_individu():
    individu = {}
    for werknemer, gegevens in werknemers.items():
        beschikbare_dagen = gegevens["beschikbare_dagen"]
        aantal_dagen = gegevens["aantal_dagen"]
        individu[werknemer] = random.sample(beschikbare_dagen, min(aantal_dagen, len(beschikbare_dagen)))

    # Zorg ervoor dat elke werknemer minimaal één dag werkt
    for werknemer in individu:
        beschikbare_dagen = werknemers[werknemer]["beschikbare_dagen"]
        while len(individu[werknemer]) < 1 or set(individu[werknemer]) != set(beschikbare_dagen):
            extra_dag = random.choice(beschikbare_dagen)
            if extra_dag not in individu[werknemer]:
                individu[werknemer].append(extra_dag)

    return individu


def maak_populatie(populatie_grootte):
    populatie = []
    for _ in range(populatie_grootte):
        individu = maak_individu()
        populatie.append(individu)
    return populatie



def bereken_fitness(individu):
    kosten = 0
    for dag in range(1, dagen_in_week + 1):
        personeel_beschikbaar = 0
        for werknemer in individu.keys():
            if dag in individu[werknemer]:
                personeel_beschikbaar += 1

        gewenst_personeel = {
            1: 2,
            2: 2,
            3: 3,
            4: 3,
            5: 4,
            6: 4,
            7: 3
        }

        kosten += abs(personeel_beschikbaar - gewenst_personeel[dag])

    return 1 / kosten


def totaal_fitness(populatie):
    totaal_fitness = 0
    for individu in populatie:
        totaal_fitness += bereken_fitness(individu)
    return totaal_fitness


def selecteer_individuen(populatie, aantal_te_selecteren):
    fitness_scores = [bereken_fitness(individu) for individu in populatie]
    geselecteerde_individuen = random.choices(populatie, weights=fitness_scores, k=aantal_te_selecteren)
    return geselecteerde_individuen


def kruising(vader, moeder):
    willekeurig_punt = random.choice(list(vader.keys()))

    kind1 = {}
    kind2 = {}

    for werknemer, dagen in vader.items():
        if werknemer < willekeurig_punt:
            kind1[werknemer] = dagen
            kind2[werknemer] = moeder[werknemer]
        else:
            kind1[werknemer] = moeder[werknemer]
            kind2[werknemer] = dagen

    return kind1, kind2



def mutatie(individu, mutatiekans):
    gemuteerd_individu = {}
    for werknemer, dagen in individu.items():
        dagen_list = []
        for dag in dagen:
            if mutatiekans > random.random():
                dagen_beschikbaar = [dag_beschikbaar for dag_beschikbaar in werknemers[werknemer]["beschikbare_dagen"]
                                     if dag_beschikbaar not in dagen]
                if dagen_beschikbaar:
                    dagen_list.append(random.choice(dagen_beschikbaar))
            else:
                dagen_list.append(dag)
        gemuteerd_individu[werknemer] = dagen_list
    return gemuteerd_individu



populatie = maak_populatie(populatie_grootte)

for generatie in range(aantal_generaties):
    aantal_te_selecteren = int(selectie_percentage * populatie_grootte)
    geselecteerde_individuen = selecteer_individuen(populatie, aantal_te_selecteren)

    nieuwe_populatie = []
    for i in range(0, len(geselecteerde_individuen), 2):
        vader = geselecteerde_individuen[i]
        moeder = geselecteerde_individuen[i + 1]
        kind1, kind2 = kruising(vader, moeder)
        nieuwe_populatie.append(kind1)
        nieuwe_populatie.append(kind2)

    for i in range(len(nieuwe_populatie)):
        nieuwe_populatie[i] = mutatie(nieuwe_populatie[i], mutatiekans)

    populatie += nieuwe_populatie

    fitness_scores = [bereken_fitness(individu) for individu in populatie]
    print(totaal_fitness(nieuwe_populatie))
    populatie = [populatie[i] for i in sorted(range(len(fitness_scores)),
                                              key=lambda k: fitness_scores[k],
                                              reverse=True)[:populatie_grootte]]

beste_individu = max(populatie, key=bereken_fitness)
beste_fitness = bereken_fitness(beste_individu)
print(f"Uiteindelijk resultaat: Beste individu = {beste_individu}, Beste fitness = {beste_fitness}")

def print_rooster(individu):
    for werknemer, dagen in individu.items():
        print(werknemer + ": " + ", ".join(str(dag) for dag in dagen))

print("\nNieuw rooster voor het beste individu:")
print_rooster(beste_individu)
