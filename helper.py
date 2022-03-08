from rich.table import Table
from core import Champion, Match, Shape

# The functions in this file is from the team-local-tactics.py 
# with some modifications to fit the db-server-client setup.
# The functions only take data sent from the server and make the text look nice.
# We could also place the functions in the server-file, but was more
# clean to make a helper.py to help out the server...

def match_summary(match: Match) -> None:

    EMOJI = {
        Shape.ROCK: ':raised_fist-emoji:',
        Shape.PAPER: ':raised_hand-emoji:',
        Shape.SCISSORS: ':victory_hand-emoji:'
    }

    summary = []
    results = ""

    # For each round print a table with the results
    for index, round in enumerate(match.rounds):

        # Create a table containing the results of the round
        round_summary = Table(title=f'Round {index+1}')

        # Add columns for each team
        round_summary.add_column("Red",
                                 style="red",
                                 no_wrap=True)
        round_summary.add_column("Blue",
                                 style="blue",
                                 no_wrap=True)

        # Populate the table
        for key in round:
            red, blue = key.split(', ')
            round_summary.add_row(f'{red} {EMOJI[round[key].red]}',
                                  f'{blue} {EMOJI[round[key].blue]}')
        summary.append(round_summary)

    red_score, blue_score = match.score
    results += f"Red: {red_score}\nBlue: {blue_score}"

    if red_score > blue_score:
        results += '\n[red]Red victory! :grin:'
    elif red_score < blue_score:
        results += '\n[blue]Blue victory! :grin:'
    else:
        results += '\nDraw :expressionless:'
    
    summary.append(results)

    return summary


def available_champs(champions: dict[Champion]) -> None:

    # Create a table containing available champions
    available_champs = Table(title='Available champions')

    # Add the columns Name, probability of rock, probability of paper and
    # probability of scissors
    available_champs.add_column("Name", style="cyan", no_wrap=True)
    available_champs.add_column("prob(:raised_fist-emoji:)", justify="center")
    available_champs.add_column("prob(:raised_hand-emoji:)", justify="center")
    available_champs.add_column("prob(:victory_hand-emoji:)", justify="center")

    # Populate the table
    for champion in champions.values():
        available_champs.add_row(*champion.str_tuple)

    return available_champs