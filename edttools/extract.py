from collections import namedtuple
import re

EDT = namedtuple("EDT", ("login", "semestre", "nom", "prenom", "uvs", "items"))
EDTItem = namedtuple("EDTItem", ("uv", "type", "num", "jour", "debut", "fin", "frequence", "salle"))

aliases = {'XQ03': 'MQ03'}

def extract(stream):
    ligne1 = stream.readline()
    if not(ligne1.startswith(" --")):
        return None

    resume = stream.readline().split()
    if len(resume) < 2:
        return None
    login = resume[0]
    semestre = resume[1]

    uvs = []
    if len(resume) >= 3:
        uvs = resume[4:]

    items = []
    ligne = stream.readline()
    while ligne:
        if ligne != " \n":
            edt_items = parse_edt_item(ligne)
            items.extend(edt_items)
        ligne = stream.readline()

    return EDT(login, semestre, '', '', uvs, items)

jours_remplacement = {"LUNDI...": "Lundi",
                      "MARDI...": "Mardi",
                      "MERCREDI": "Mercredi",
                      "JEUDI...": "Jeudi",
                      "VENDREDI": "Vendredi",
                      "SAMEDI..": "Samedi",
                      "DIMANCHE": "Dimanche"} # par acquis de conscience

def parse_edt_item(ligne):
    "Parse une ligne d'emploie du temps et renvoie une liste d'éléments"
    edt_item = ligne.split()
    items = []

    if len(edt_item) >= 2:
        uv = edt_item[0]
        type_item = edt_item[1]
        if type_item == 'T' or type_item == 'D':
            # GE20       D 1    LUNDI... 14:15-16:15,F1,S=FA420
            # SPJE       D 1    JEUDI... 14:15-18:15,F1,S=     *
            # AP53       T 1    LUNDI... 14:30-18:30,F1,S=RI207   /MERCREDI  9:00-13:00,F1,S=RI207
            num_tdtp = edt_item[2]
            jour = jours_remplacement[edt_item[3]]
            infos = parse_infos(edt_item[4])

            items.append(EDTItem(uv, type_item, num_tdtp, jour,
                                 infos[0], infos[1], infos[2], infos[3]))

            if len(edt_item) >= 7:
                jour2 = jours_remplacement[edt_item[5][1:]] # enleve le / en début du nom de jour
                infos2 = parse_infos(edt_item[6])

                items.append(EDTItem(uv, type_item, num_tdtp, jour2,
                                     infos2[0], infos2[1], infos2[2], infos2[3]))

        elif type_item == 'C':
            # GE20       C      LUNDI... 13:00-14:00,F1,S=FA106
            # MT90       C      LUNDI... 10:15-11:15,F1,S=FA205   /JEUDI... 10:15-12:15,F1,S=FA205
            jour = jours_remplacement[edt_item[2]]
            infos = parse_infos(edt_item[3])

            items.append(EDTItem(uv, type_item, 0, jour,
                                 infos[0], infos[1], infos[2], infos[3]))
            if len(edt_item) >= 6:
                jour2 = jours_remplacement[edt_item[4][1:]] # enleve le / en début du nom de jour
                infos2 = parse_infos(edt_item[5])

                items.append(EDTItem(uv, type_item, 0, jour2,
                                     infos2[0], infos2[1], infos2[2], infos2[3]))

    return items

horaires_reg = re.compile(r"\s?(\d+):(\d{2})")
def parse_infos(infos):
    # 13:00-14:00,F1,S=FA106
    horaires, frequence, salle = infos.split(",")
    horaires = horaires_reg.findall(horaires)
    intify_horaire = lambda x: (int(x[0]), int(x[1]))
    debut = intify_horaire(horaires[0])
    fin = intify_horaire(horaires[1])

    frequence = int(frequence[1:])
    salle = salle[2:]

    return (debut, fin, frequence, salle)
