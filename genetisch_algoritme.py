import random
import json



#Gegevens lezen uit gegevens_werknemer.json
with open('gegevens_werknemer.json', 'r') as json_bestand:
    inhoud = json_bestand.read()

# Stap 2: Decodeer de JSON-gegevens naar een Python-dictionary
werknemers = json.loads(inhoud)


dagen_in_week = 7

populatie_grootte = 100
aantal_generaties = 1000
selectie_percentage = 0.5
kruising_kans = 0.8
mutatiekans = 0.001


def maak_individu(gewenst_personeel):
    """
    Maakt een individu (rooster) met willekeurige toewijzing van dagen aan werknemers.

    Paramaters:
        gewenst_personeel(dict): key= dag van de week, value= aantal gewenst personeel op die dag

    Returns:
        dict: Het gemaakte individu (rooster) waarbij de werknemers zijn gekoppeld aan de toegewezen dagen.
    """
    beschikbare_werknemers = list(werknemers.keys())
    beschikbare_dagen = list(range(1, dagen_in_week + 1))

    individu = {}
    for werknemer in beschikbare_werknemers:
        individu[werknemer] = []

    for dag in beschikbare_dagen:
        beschikbare_werknemers_dag = beschikbare_werknemers[:]
        random.shuffle(beschikbare_werknemers_dag)

        for werknemer in beschikbare_werknemers_dag:
            if len(individu[werknemer]) < 1:
                individu[werknemer].append(dag)
                beschikbare_werknemers_dag.remove(werknemer)

        for werknemer in beschikbare_werknemers_dag:
            if len(individu[werknemer]) < 1:
                individu[werknemer].append(dag)
            else:
                werknemers_op_dag = [w for w, d in individu.items() if dag in d]
                if len(set(werknemers_op_dag)) < gewenst_personeel[dag]:
                    individu[werknemer].append(dag)

    return individu


def maak_populatie(populatie_grootte, gewenst_personeel):
    """
    Maakt een populatie van individuen met de opgegeven grootte.

    Parameters:
        populatie_grootte (int): Het gewenste aantal individuen in de populatie.
        gewenst_personeel(dict): key= dag van de week, value= aantal gewenst personeel op die dag
    Returns:
        list: De gemaakte populatie van individuen (roosters).
    """
    populatie = []
    # Genereer het opgegeven aantal individuen en voeg ze toe aan de populatie
    for _ in range(populatie_grootte):  #exacte waarde is niet van belang, het wordt niet verder gebruikt.
        individu = maak_individu(gewenst_personeel)
        populatie.append(individu)
    return populatie



def bereken_fitness(individu, gewenst_personeel):
    """
    Berekent de fitnesswaarde van een individu (rooster).

    parameters:
        individu (dict): Het individu (rooster) waarvan de fitnesswaarde wordt berekend.
        gewenst_personeel(dict): key= dag van de week, value= aantal gewenst personeel op die dag

    Returns:
        float: De berekende fitnesswaarde van het individu.
    """
    overtreding = 0
    # Loop door elke dag in de week
    for dag in range(1, dagen_in_week + 1):
        personeel_beschikbaar = 0
        # Tel het aantal werknemers dat beschikbaar is op de huidige dag
        for werknemer in individu.keys():
            if dag in individu[werknemer]:
                personeel_beschikbaar += 1

        verschil = personeel_beschikbaar - gewenst_personeel[dag]

        if verschil < 0:
            overtreding += abs(verschil)  # Verhoog de overtreding als er te weinig personeel is
        elif verschil > 0 and dag not in individu[werknemer]:
            overtreding += verschil  # Verhoog de overtreding als werknemers werken op niet-beschikbare dagen

    if overtreding == 0:
        return 1e-10  # Retourneer een kleine waarde in plaats van nul om deling door nul te voorkomen

    return 1 / overtreding


def totaal_fitness(populatie, gewenst_personeel):
    """
    Berekent de totale fitnesswaarde van een populatie.

    Parameters:
        populatie (list): De populatie van individuen waarvan de totale fitnesswaarde wordt berekend.
        gewenst_personeel(dict): key= dag van de week, value= aantal gewenst personeel op die dag

    Returns:
        float: De berekende totale fitnesswaarde van de populatie.
    """
    totaal_fitness = 0
    # Loop door elk individu in de populatie
    for individu in populatie:
        # Bereken de totale fitnesswaarde
        totaal_fitness += bereken_fitness(individu, gewenst_personeel)
    return totaal_fitness


def selecteer_individuen(populatie, aantal_te_selecteren, gewenst_personeel):
    """
    Selecteert individuen uit een populatie op basis van hun fitnesswaarden.

    Paramaters:
        populatie (list): De populatie van individuen waaruit geselecteerd wordt.
        aantal_te_selecteren (int): Het aantal individuen dat geselecteerd moet worden.
        gewenst_personeel(dict): key= dag van de week, value= aantal gewenst personeel op die dag

    Returns:
        list: Een lijst van geselecteerde individuen.

    Raises:
        ValueError: Als het aantal te selecteren individuen groter is dan de populatiegrootte.
    """
    fitness_scores = [bereken_fitness(individu, gewenst_personeel) for individu in populatie]
    # Gebruik de fitnesswaarden als gewichten om individuen te selecteren
    geselecteerde_individuen = random.choices(populatie, weights=fitness_scores, k=aantal_te_selecteren)
    return geselecteerde_individuen


def kruising(vader, moeder):
    """
    Kruist twee individuen door genetische informatie uit te wisselen.

    Parameters:
        vader (dict): Het individu dat als vader heet.
        moeder (dict): Het individu dat als moeder heet.

    Returns:
        tuple: Een tuple bestaande uit twee kinderen gegenereerd door de kruising.

    """
    # Kies een willekeurig punt om de genetische informatie uit te wisselen
    willekeurig_punt = random.choice(list(vader.keys()))

    kind1 = {}
    kind2 = {}

    for werknemer, dagen in vader.items():
        if werknemer < willekeurig_punt:
            # Kopieer de genetische informatie van de vader voor werknemers voor het willekeurige punt
            kind1[werknemer] = dagen
            kind2[werknemer] = moeder[werknemer]
        else:
            # Kopieer de genetische informatie van de moeder voor werknemers na het willekeurige punt
            kind1[werknemer] = moeder[werknemer]
            kind2[werknemer] = dagen

    return kind1, kind2


def mutatie(individu, mutatiekans, gewenst_personeel):
    """
    Voert mutatie uit op een individu met een gegeven mutatiekans.

    Parameters:
        individu (dict): Het individu om te muteren.
        mutatiekans (float): De kans op mutatie per werknemer.
        gewenst_personeel(dict): key= dag van de week, value= aantal gewenst personeel op die dag


    Returns:
        dict: Het gemuteerde individu.
    """
    gemuteerd_individu = individu.copy()

    # Zorg ervoor dat elke werknemer minimaal één dag werkt
    for werknemer in gemuteerd_individu:
        dagen = gemuteerd_individu[werknemer]
        if len(dagen) == 0:
            # Als werknemer niet werkt, voeg een willekeurige beschikbare dag toe
            beschikbare_dagen = werknemers[werknemer]["beschikbare_dagen"]
            willekeurige_dag = random.choice(beschikbare_dagen)
            dagen.append(willekeurige_dag)

    # Zorg ervoor dat het aantal werknemers op een dag overeenkomt met het gewenste aantal werknemers
    for dag in range(1, dagen_in_week + 1):
        werknemers_aanwezig = sum(1 for werknemer in gemuteerd_individu if dag in gemuteerd_individu[werknemer])

        if werknemers_aanwezig < gewenst_personeel[dag]:
            # Voeg werknemers toe als er te weinig zijn op de dag
            beschikbare_werknemers = [werknemer for werknemer in gemuteerd_individu if dag not in gemuteerd_individu[werknemer]]
            if beschikbare_werknemers:
                random.shuffle(beschikbare_werknemers)
                aantal_toevoegen = gewenst_personeel[dag] - werknemers_aanwezig
                for i in range(aantal_toevoegen):
                    werknemer_toevoegen = beschikbare_werknemers[i]
                    gemuteerd_individu[werknemer_toevoegen].append(dag)
        elif werknemers_aanwezig > gewenst_personeel[dag]:
            # Verwijder willekeurige werknemers als er te veel zijn op de dag
            aanwezige_werknemers = [werknemer for werknemer in gemuteerd_individu if dag in gemuteerd_individu[werknemer]]
            random.shuffle(aanwezige_werknemers)
            aantal_verwijderen = werknemers_aanwezig - gewenst_personeel[dag]
            for i in range(aantal_verwijderen):
                werknemer_verwijderen = aanwezige_werknemers[i]
                gemuteerd_individu[werknemer_verwijderen].remove(dag)

    # Sorteer de werknemers op basis van het aantal gewerkte dagen in oplopende volgorde
    werknemers_sorted = sorted(gemuteerd_individu.keys(), key=lambda x: len(gemuteerd_individu[x]))

    # Herverdeel de beschikbare dagen aan werknemers die minder werken
    for dag in range(1, dagen_in_week + 1):
        werknemers_aanwezig = sum(1 for werknemer in gemuteerd_individu if dag in gemuteerd_individu[werknemer])

        if werknemers_aanwezig < gewenst_personeel[dag]:
            # Voeg werknemers toe als er te weinig zijn op de dag
            beschikbare_werknemers = [werknemer for werknemer in gemuteerd_individu if dag not in gemuteerd_individu[werknemer]]
            if beschikbare_werknemers:
                random.shuffle(beschikbare_werknemers)
                aantal_toevoegen = gewenst_personeel[dag] - werknemers_aanwezig
                for i in range(aantal_toevoegen):
                    werknemer_toevoegen = beschikbare_werknemers[i]
                    gemuteerd_individu[werknemer_toevoegen].append(dag)
        elif werknemers_aanwezig > gewenst_personeel[dag]:
            # Verwijder willekeurige werknemers als er te veel zijn op de dag
            aanwezige_werknemers = [werknemer for werknemer in gemuteerd_individu if dag in gemuteerd_individu[werknemer]]
            random.shuffle(aanwezige_werknemers)
            aantal_verwijderen = werknemers_aanwezig - gewenst_personeel[dag]
            for i in range(aantal_verwijderen):
                werknemer_verwijderen = aanwezige_werknemers[i]
                gemuteerd_individu[werknemer_verwijderen].remove(dag)

    # Zorg ervoor dat elke werknemer minimaal één dag werkt na de herverdeling
    for werknemer in gemuteerd_individu:
        dagen = gemuteerd_individu[werknemer]
        if len(dagen) == 0:
            # Als werknemer niet werkt, voeg een willekeurige beschikbare dag toe
            beschikbare_dagen = werknemers[werknemer]["beschikbare_dagen"]
            willekeurige_dag = random.choice(beschikbare_dagen)
            dagen.append(willekeurige_dag)

    # Voer mutatie uit op individuele werknemers met een gegeven mutatiekans
    for werknemer in gemuteerd_individu:
        if random.random() < mutatiekans:
            dagen = gemuteerd_individu[werknemer]
            if dagen:
                # Selecteer willekeurige dag en vervang deze door een andere willekeurige beschikbare dag
                willekeurige_index = random.randint(0, len(dagen) - 1)
                willekeurige_dag = random.choice(werknemers[werknemer]["beschikbare_dagen"])
                dagen[willekeurige_index] = willekeurige_dag

    return gemuteerd_individu


def genetisch_algoritme(gewenst_personeel):
    """
    Voert het genetisch algoritme uit om de generatie van het rooster te optimaliseren.

    Het genetisch algoritme evolueert een populatie van roosters gedurende een aantal generaties,
    waarbij selectie-, crossover- en mutatiebewerkingen worden toegepast om de fitness van de roosters
    te verbeteren.

    Paramaters:
        gewenst_personeel(dict): key= dag van de week, value= aantal gewenst personeel op die dag

    Returns:
        dict: Het beste individu gevonden door het genetisch algoritme.
        float: De fitnesswaarde van het beste individu.
    """

    # Initialiseer de populatie
    populatie = maak_populatie(populatie_grootte, gewenst_personeel)

    for generatie in range(aantal_generaties):
        # Selectie: Selecteer individuen uit de populatie op basis van fitnessscores
        aantal_te_selecteren = int(selectie_percentage * populatie_grootte)
        geselecteerde_individuen = selecteer_individuen(populatie, aantal_te_selecteren, gewenst_personeel)

        nieuwe_populatie = []
        for i in range(0, len(geselecteerde_individuen), 2):
            vader = geselecteerde_individuen[i]
            moeder = geselecteerde_individuen[i + 1]

            # Crossover: Maak nakomelingen door crossover tussen ouders
            kind1, kind2 = kruising(vader, moeder)
            nieuwe_populatie.append(kind1)
            nieuwe_populatie.append(kind2)

        for i in range(len(nieuwe_populatie)):
            # Mutatie: Pas mutatie toe op de nakomelingen
            nieuwe_populatie[i] = mutatie(nieuwe_populatie[i], mutatiekans, gewenst_personeel)

        # Voeg toe aan de populatie
        populatie += nieuwe_populatie

        # Verminder de grootte van de populatie tot de gewenste populatiegrootte
        fitness_scores = [bereken_fitness(individu, gewenst_personeel) for individu in populatie]
        populatie = [populatie[i] for i in sorted(range(len(fitness_scores)),
                                                  key=lambda k: fitness_scores[k],
                                                  reverse=True)[:populatie_grootte]]

    # Vind het beste individu in de uiteindelijke populatie
    beste_individu = max(populatie, key=lambda x: bereken_fitness(x, gewenst_personeel))
    beste_fitness = bereken_fitness(beste_individu, gewenst_personeel)

    # Pas het aantal toegewezen werknemers aan om aan het gewenste aantal te voldoen
    aangepast_individu = pas_aantal_werknemers_aan(beste_individu, gewenst_personeel)

    # Retourneer het beste individu en zijn fitness
    return aangepast_individu, beste_fitness

def pas_aantal_werknemers_aan(individu, gewenst_personeel):
    """
    Past het aantal toegewezen werknemers aan om aan het gewenste aantal te voldoen.

    Parameters:
        individu (dict): Het individu (rooster) om aan te passen.
        gewenst_personeel(dict): key= dag van de week, value= aantal gewenst personeel op die dag

    Returns:
        dict: Het aangepaste individu met het juiste aantal werknemers per dag.
    """
    aangepast_individu = individu.copy()

    for dag, gewenst_aantal in gewenst_personeel.items():
        # Verkrijg de werknemers die op de huidige dag ingepland zijn
        werknemers_op_dag = [werknemer for werknemer, dagen in individu.items() if dag in dagen]
        huidig_aantal = len(werknemers_op_dag)

        if huidig_aantal < gewenst_aantal:
            # Bereken het aantal ontbrekende werknemers
            ontbrekende_aantal = gewenst_aantal - huidig_aantal
            # Verkrijg de beschikbare werknemers die nog niet zijn ingepland op deze dag
            beschikbare_werknemers = [werknemer for werknemer in individu if dag not in individu[werknemer]]
            # Selecteer een willekeurige subset van beschikbare werknemers om toe te voegen
            toe_te_voegen = random.sample(beschikbare_werknemers, min(ontbrekende_aantal, len(beschikbare_werknemers)))
            # Voeg de werkdag toe aan de individuen die worden toegevoegd
            aangepast_individu.update({werknemer: individu[werknemer] + [dag] for werknemer in toe_te_voegen})
        elif huidig_aantal > gewenst_aantal:
            # Bereken het aantal overbodige werknemers
            extra_aantal = huidig_aantal - gewenst_aantal
            # Verkrijg de overbodige werknemers die al zijn ingepland op deze dag
            overbodige_werknemers = [werknemer for werknemer in individu if dag in individu[werknemer]]
            # Selecteer een willekeurige subset van overbodige werknemers om te verwijderen
            te_verwijderen = random.sample(overbodige_werknemers, min(extra_aantal, len(overbodige_werknemers)))
            # Verwijder de werkdag van de individuen die worden verwijderd
            aangepast_individu.update({werknemer: [d for d in individu[werknemer] if d != dag] for werknemer in te_verwijderen})

    return aangepast_individu

def maak_rooster(individu):
    """
    Maakt een rooster op basis van het gegeven individu.

    Parameters:
        individu (dict): Het individu (rooster) om te converteren.

    Returns:
        list: Een lijst met dagroosters. Elk dagrooster bevat de dagnaam en de werknemers die op die dag werken.
    """
    # Een woordenboek met de dagnummers en bijbehorende dagnamen
    dagen = {1: 'maandag', 2: 'dinsdag', 3: 'woensdag', 4: 'donderdag', 5: 'vrijdag', 6: 'zaterdag', 7: 'zondag'}
    # Een lege lijst om de dagroosters op te slaan
    rooster = []


    # Itereer over de dagnummers en dagnamen
    for dag_num, dag_naam in dagen.items():
        # Een lege lijst om de werknemers van de huidige dag op te slaan
        werknemers = []
        # Itereer over het individu (rooster) om werknemers te vinden die op de huidige dag werken
        for werknemer, werkdagen in individu.items():
            if dag_num in werkdagen:
                # Voeg de werknemer toe aan de lijst van werknemers voor de huidige dag
                werknemers.append(werknemer)
        # Maak een dagrooster bestaande uit de dagnaam en de werknemers van die dag
        dag_rooster = [dag_naam] + werknemers
        # Voeg het dagrooster toe aan het rooster
        rooster.append(dag_rooster)
    return rooster


