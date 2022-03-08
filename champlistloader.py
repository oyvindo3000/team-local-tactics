from core import Champion

def _parse_champ(champ_text: str) -> Champion:
    name, rock, paper, scissors = champ_text.split(sep=',')
    return Champion(name, float(rock), float(paper), float(scissors))

def from_csv(filename: str) -> dict[str, Champion]:
    champions = {}
    with open(filename, 'r') as f:
        for line in f.readlines():
            champ = _parse_champ(line)
            champions[champ.name] = champ
    return champions

def load_some_champs():
    return from_csv('champs.txt')

# A functions which returns a list with the names of available 
# champions, used to validate input of champs.

def getChampNames():
    champnames = []
    with open("champs.txt", 'r') as f:
        for line in f.readlines():
            attributes = line.split(sep=",")
            champnames.append(attributes[0])
    return champnames