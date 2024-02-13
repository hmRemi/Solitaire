import random
import os
from time import sleep

try :
    import colorama
    from colorama import Fore
    colorama.init()
except ImportError:
    os.system('pip install colorama')
    import colorama
    from colorama import Fore
    colorama.init()


class Kort:
    """Representerer et spillkort."""

    def __init__(self, sort, verdi, norsk):
        """
        Oppretter et nytt kort.

        Args:
            sort (str): Sorten av kortet.
            verdi (int): Verdien til kortet.
            norsk (bool): Angir om kortene skal være på norsk.

        Attributes:
            sort (str): Sorten av kortet.
            verdi (int): Verdien til kortet.
            norsk (bool): Angir om kortene skal være på norsk.
            skjult (bool): Angir om kortet er skjult eller ikke.
        """
        self.sort = sort
        self.verdi = verdi
        self.norsk = norsk
        self.skjult = True

    def symbol(self):
        """
        Returnerer en streng som representerer kortets symbol.

        Returns:
            str: Streng som representerer kortets symbol.
        """
        kortverdier = {1: 'A' if not self.norsk else 'E',
                       11: 'J' if not self.norsk else 'Kn',
                       12: 'Q' if not self.norsk else 'D',
                       13: 'K' if not self.norsk else 'K'}

        if self.sort in ['hjerter', 'ruter']:
            symbol_color = Fore.RED
        else:
            symbol_color = Fore.LIGHTBLACK_EX

        return f"{symbol_color}{kortverdier.get(self.verdi, str(self.verdi))} {self.sort_symbol()}{Fore.RESET}"

    def sort_symbol(self):
        """
        Returnerer symbolet som representerer kortets sort.

        Returns:
            str: Symbolet for kortets sort.
        """
        symboler = {'kløver': f'♣', 'spar': f'♠', 'hjerter': f'♥', 'ruter': f'♦'}
        return symboler.get(self.sort, '?')

    def farge(self):
        """
        Returnerer fargen til kortet.

        Returns:
            str: "svart" hvis kortets sort er kløver eller spar, "rød" ellers.
        """
        return "svart" if self.sort in ['kløver', 'spar'] else "rød"

    def vis_kort(self):
        """Viser kortet ved å sette skjult-attributtet til False."""
        self.skjult = False


def lag_kortstokk(norsk):
    """
    Lager en kortstokk med 52 kort.

    Args:
        norsk (bool): Angir om kortene skal være på norsk.

    Returns:
        list: En liste med Kort-objekter som representerer en kortstokk.
    """
    kortstokk = []
    for sort in ['kløver', 'spar', 'hjerter', 'ruter']:
        for verdi in range(1, 14):
            kort = Kort(sort, verdi, norsk)
            kortstokk.append(kort)
    return kortstokk


def clear():
    """Tømmer konsollvinduet."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_brett(stabler, trekkbunke, foundation):
    """
    Skriver ut spillbrettet.

    Args:
        stabler (list): En liste med lister av Kort-objekter som representerer stablene på spillbrettet.
        trekkbunke (list): En liste med Kort-objekter som representerer trekkbunken.
        foundation (dict): En ordbok med lister av Kort-objekter som representerer foundation-pilene.
    """
    clear()
    print(f"{Fore.LIGHTBLACK_EX}--------------------------------------------------{Fore.RESET}")
    print("Foundation Piles:")
    for sort, bunke in foundation.items():
        print(f"{Fore.LIGHTRED_EX}| {Fore.RESET}{sort.capitalize()} Foundation: {bunke[-1].symbol() if bunke else 'Empty'}")

    print("\nTableau Piles:")
    for i, stabel in enumerate(stabler):
        print(
            f"{Fore.LIGHTRED_EX}| {Fore.RESET}Stabel {i + 1}: {', '.join([kort.symbol() if not kort.skjult else 'X' for kort in stabel]) if stabel else 'Empty'}")

    print("\nStock Pile:")
    print(f"{Fore.LIGHTRED_EX}| {Fore.RESET}Antall kort: {len(trekkbunke)}")

    top_3_cards = [f"{kort.symbol()}" for kort in trekkbunke[:1]]
    top_3_formatted = [Fore.LIGHTBLACK_EX + card + Fore.RESET if card[-4:] == 'svart' else Fore.RED + card + Fore.RESET for card in top_3_cards]
    print(f"{Fore.LIGHTRED_EX}| {Fore.RESET}Trekkbunke topp 1: ", ", ".join(top_3_formatted))
    print(f"{Fore.LIGHTBLACK_EX}--------------------------------------------------{Fore.RESET}")


def initialiser_spill():
    """
    Initialiserer et nytt spill.

    Returns:
        tuple: En tuple med stabler, trekkbunke og foundation-piler.
    """
    norsk_valg = input(
        f"{Fore.LIGHTBLACK_EX}[{Fore.LIGHTRED_EX}?{Fore.LIGHTBLACK_EX}] {Fore.RESET}Norsk {Fore.LIGHTBLACK_EX}> {Fore.RESET}(ja/nei): ")
    norsk = True if norsk_valg.lower() == 'ja' else False
    kortstokk = lag_kortstokk(norsk)
    random.shuffle(kortstokk)

    stabler = [[] for _ in range(7)]
    for i in range(1, 8):
        stabler[i - 1] = kortstokk[:i]
        kortstokk = kortstokk[i:]

    trekkbunke = kortstokk
    foundation = {sort: [] for sort in ['kløver', 'spar', 'hjerter', 'ruter']}

    for stabel in stabler:
        if stabel:
            stabel[-1].vis_kort()

    return stabler, trekkbunke, foundation


def gyldig_flytt_sekvens(kortsekvens):
    """
    Sjekker om en gitt sekvens av kort er en gyldig sekvens for å flytte.

    Args:
        kortsekvens (list): En liste med Kort-objekter.

    Returns:
        bool: True hvis sekvensen er gyldig, ellers False.
    """
    for i in range(len(kortsekvens) - 1):
        if kortsekvens[i].verdi != kortsekvens[i + 1].verdi + 1 or kortsekvens[i].farge() == kortsekvens[i + 1].farge():
            return False
    return True


def gyldig_flytt(stabel, kort, dest_type="stabel"):
    """
    Sjekker om et gitt kort kan flyttes til en destinasjon.

    Args:
        stabel (list): En liste med Kort-objekter som representerer destinasjonsstabelen.
        kort (Kort): Et Kort-objekt som representerer kortet som skal flyttes.
        dest_type (str): Typen av destinasjon ("stabel" eller "foundation").

    Returns:
        bool: True hvis flyttet er gyldig, ellers False.
    """
    if dest_type == "stabel":
        if not stabel:
            return kort.verdi == 13
        topp_kort = stabel[-1]
        return (topp_kort.verdi == kort.verdi + 1) and (topp_kort.farge() != kort.farge())
    elif dest_type == "foundation":
        if not stabel:
            return kort.verdi == 1
        topp_kort = stabel[-1] if stabel else None
        return (topp_kort and topp_kort.verdi + 1 == kort.verdi) and (topp_kort.sort == kort.sort)
    else:
        return False


def flytt_kort(stabler, source_idx, dest_idx, antall_kort=1):
    """
    Flytter kort fra en kildestabel til en destinasjonsstabel.

    Args:
        stabler (list): En liste med lister av Kort-objekter som representerer stablene på spillbrettet.
        source_idx (int): Indeks for kildestabelen.
        dest_idx (int): Indeks for destinasjonsstabelen.
        antall_kort (int): Antall kort som skal flyttes.

    Returns:
        bool: True hvis flyttingen var vellykket, ellers False.
    """
    if antall_kort > 1:
        if not gyldig_flytt_sekvens(stabler[source_idx][-antall_kort:]):
            print("Ugyldig trekk. Sekvensen bryter med reglene.")
            return False

    kortene = stabler[source_idx][-antall_kort:]
    del stabler[source_idx][-antall_kort:]

    if stabler[source_idx]:
        stabler[source_idx][-1].vis_kort()

    stabler[dest_idx].extend(kortene)
    for kort in kortene:
        kort.vis_kort()


def flytt_kort_til_foundation(kort, foundation):
    """
     Flytter et kort til foundation-pilen.

     Args:
         kort (Kort): Kortet som skal flyttes.
         foundation (dict): Ordbok med lister av Kort-objekter som representerer foundation-pilene.
     """
    foundation[kort.sort].append(kort)


def main():
    """
    Hovedfunksjonen som kjører spillet.
    """
    stabler, trekkbunke, foundation = initialiser_spill()

    while True:
        print_brett(stabler, trekkbunke, foundation)
        print(f"{Fore.LIGHTBLACK_EX}[{Fore.LIGHTRED_EX}1{Fore.LIGHTBLACK_EX}] {Fore.RESET}Flytt kort fra trekkbunke til stabel")
        print(f"{Fore.LIGHTBLACK_EX}[{Fore.LIGHTRED_EX}2{Fore.LIGHTBLACK_EX}] {Fore.RESET}Flytt kort mellom stabler")
        print(f"{Fore.LIGHTBLACK_EX}[{Fore.LIGHTRED_EX}3{Fore.LIGHTBLACK_EX}] {Fore.RESET}Flytt kort til foundation pile")
        print(f"{Fore.LIGHTBLACK_EX}[{Fore.LIGHTRED_EX}4{Fore.LIGHTBLACK_EX}] {Fore.RESET}Trekk kort fra trekkbunken")
        print(f"{Fore.LIGHTBLACK_EX}[{Fore.LIGHTRED_EX}5{Fore.LIGHTBLACK_EX}] {Fore.RESET}Flytt kort fra trekkbunke til foundation pile")
        print(f"{Fore.LIGHTBLACK_EX}[{Fore.LIGHTRED_EX}6{Fore.LIGHTBLACK_EX}] {Fore.RESET}Avslutt\n")

        valg = input(f"{Fore.LIGHTBLACK_EX}[{Fore.LIGHTRED_EX}?{Fore.LIGHTBLACK_EX}] {Fore.RESET}Option {Fore.LIGHTBLACK_EX}> {Fore.RESET}(1-6): ")

        if valg == '1':
            if trekkbunke:
                neste_kort = trekkbunke[0]
                print(f"Neste kort i trekkbunke: {neste_kort.symbol()}")
                valgt_stabel = int(input("Velg stabel (1-7): ")) - 1
                if valgt_stabel in range(7) and gyldig_flytt(stabler[valgt_stabel], neste_kort, "stabel"):
                    flyttet_kort = trekkbunke.pop(0)
                    stabler[valgt_stabel].append(flyttet_kort)
                    flyttet_kort.vis_kort()
                else:
                    print("Ugyldig trekk. Prøv igjen.")
                    sleep(1)

        elif valg == '2':
            stabel_fra = int(input("Velg stabel å flytte fra (1-7): ")) - 1
            stabel_til = int(input("Velg stabel å flytte til (1-7): ")) - 1

            if stabler[stabel_fra]:
                antall_kort = int(input("Hvor mange kort vil du flytte?: "))
                if antall_kort > len(stabler[stabel_fra]):
                    print("Feil: Antall kort angitt er større enn antallet tilgjengelige kort i stabelen.")
                    sleep(1)
                elif gyldig_flytt(stabler[stabel_til], stabler[stabel_fra][-antall_kort],
                                "stabel") and gyldig_flytt_sekvens(stabler[stabel_fra][-antall_kort:]):
                    flytt_kort(stabler, stabel_fra, stabel_til, antall_kort)
                else:
                    print("Ugyldig trekk. Prøv igjen.")
                    sleep(1)
            else:
                print("Stabelen er tom.")
                sleep(1)

        elif valg == '3':
            stabel_nr = int(input("Velg stabel å flytte fra (1-7): ")) - 1
            if stabler[stabel_nr]:
                kort = stabler[stabel_nr][-1]
                if gyldig_flytt(foundation[kort.sort], kort, "foundation"):
                    flytt_kort_til_foundation(stabler[stabel_nr].pop(), foundation)
                    if stabler[stabel_nr]:
                        stabler[stabel_nr][-1].vis_kort()
                else:
                    print("Ugyldig trekk. Prøv igjen.")
                    sleep(1)
            else:
                print("Stabelen er tom.")
                sleep(1)

        elif valg == '4':
            if trekkbunke:
                trekkbunke = trekkbunke[-1:] + trekkbunke[:-1]
            else:
                print("Trekkbunken er tom.")
                sleep(1)

        elif valg == '5':
            if trekkbunke:
                kort = trekkbunke[0]
                if gyldig_flytt(foundation[kort.sort], kort, "foundation"):
                    flytt_kort_til_foundation(trekkbunke.pop(0), foundation)
                else:
                    print("Ugyldig trekk. Prøv igjen.")
                    sleep(1)
            else:
                print("Trekkbunken er tom.")
                sleep(1)

        elif valg == '6':
            print("Spillet avsluttet.")
            break
        else:
            print("Ugyldig valg. Prøv igjen.")
            sleep(1)

        if all(len(bunke) == 13 for bunke in foundation.values()):
            print("Gratulerer! Du har vunnet!")
            break


if __name__ == "__main__":
    main()
