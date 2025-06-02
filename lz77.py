
def find_str(s1: str, s2: str) -> int:
    """_summary_

    Args:
        s1 (str): De caractère dans laquelle on recherche
        s2 (str): Le motif de recherche

    Returns:
        int: Retourne lundi à laquelle le motif a été trouvé sinon retourne -1
    """

    ind = -1
    l1 = len(s1)
    l2 = len(s2)

    for i in range(l1-l2+1):
        tmp = ""
        for j in range(i, i+l2):
            tmp += s1[j]

        if tmp == s2:
            ind = i
            break
    return ind


def find_str_reverse(s1: str, s2: str) -> int:
    """Recherche la dernière occurrence de s2 dans s1 (reverse find)

    Args:
        s1 (str): Chaîne dans laquelle on recherche
        s2 (str): Motif à rechercher

    Returns:
        int: Dernier indice où le motif a été trouvé, sinon -1
    """
    ind = -1
    l1 = len(s1)
    l2 = len(s2)

    for i in range(l1 - l2, -1, -1):  # boucle à l'envers
        tmp = ""
        for j in range(i, i + l2):
            tmp += s1[j]

        if tmp == s2:
            ind = i
            break

    return ind


def lz77_encode(s: str) -> list:
    """création de l'encadage d'une chaine sous la forme de triplet

    Args:
        s (str): la chaine à compresser

    Returns:
        []: un tableau de triplet
    """

    i = 0
    encoded = []
    window_size = 4096
    start = 0
    s_len = len(s)

    while i < s_len:
        window = s[max(0, i - window_size):i]
        start = i - len(window)
        jump = 1
        next_char = ""

        suffix_len = s_len - i
        triplet = triplet = (0, 0, s[i])
        for l in range(suffix_len):
            suffix = s[i:i+l+1]

            # pour être optimal il faut un reverse find
            # [(0, 0, 'A'), (1, 1, 'B'), (0, 0, 'C'), (4, 4, 'A'), (9, 2, 'D')]
            # [(0, 0, 'A'), (1, 1, 'B'), (0, 0, 'C'), (4, 4, 'A'), (5, 2, 'D')]
            # Les deux sont corrects, mais la meilleure pratique est de prendre la plus récente occurrence (distance minimale) pour optimiser la compression.
            
            # ind = find_str_reverse(window, suffix)
            # utilisasation de la fonction interne
            ind = window.rfind(suffix)
            if ind != -1:

                if i + len(suffix) < s_len:
                    next_char = s[i + len(suffix)]
                else:
                    next_char = ""

                triplet = (i - (start + ind), len(suffix), next_char)
                jump = len(suffix) + 1
            # on s'arrête dès que la fonction a retouné -1
            # c'est un choix qui permet d'accélérer le traitement
            else:
                break
        # print(triplet)
        encoded.append(triplet)
        i += jump

    return encoded


def lz77_decode(encoded: list) -> str:

    s = ""
    # pour chaque tuple faire
    for i in encoded:

        # de combien en arrière je dois revenir
        reverse = i[0]
        ind_start = len(s) - reverse
        # copie combien de caractère
        ncopy = i[1]
        ind_end = ind_start + ncopy
        # le caratère à écrire
        last_char = i[2]

        copy = s[ind_start:ind_end]
        s += copy + last_char

    return s


def ratio(original: str, encoded: list) -> float:
    """calcul le ratio de compression
    on part du pricipe que :
    - distance et longueur sont souvent codés en 2 octets (16 bits) chacun
    - caractère en 1 octet (ASCII)
    donc 1 triplet est codé sur 5 octets

    Args:
        original (str): chaine original
        encoded (list): la liste des triplets

    Returns:
        float: le taux de compression
    """
    original_size = len(original)
    encodded_size = len(encoded) * 5
    taux = 100 * (1 - encodded_size / original_size)
    return round(taux, 2)

def load_text_file(filepath: str) -> str:
    """
    Charge le contenu d'un fichier texte et le retourne sous forme de chaîne.

    Args:
        filepath (str): Chemin du fichier à lire.

    Returns:
        str: Contenu complet du fichier.
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


def main():
    # assert find_str("ABABCABABCD", "AB") == 0
    # assert find_str("ABABCABABCD", "ABC") == 2
    # assert find_str("ABABCABABCD", "CAB") == 4
    # assert find_str("ABABCABABCD", "D") == 10
    # assert find_str("ABABCABABCD", "E") == -1
    # assert find_str("AAAAAA", "AAA") == 0
    # assert find_str("ABCDEFG", "EFG") == 4
    # # convention : une chaîne vide se trouve au début
    # assert find_str("ABCDEFG", "") == 0
    # assert find_str("", "A") == -1
    # assert find_str("", "") == 0
    text = load_text_file("../tartuffe.txt")
    test_cases = {
        "court_non_repetitif": "ABCDEFG",
        "court_repetitif": "ABCABCABC",
        "long_repetitif": "AABCAABCAAABCAABCAAABCAABC",
        "texte_humain": """Bonjour, comment ça va ?
Bonjour, comment ça va ?
Bonjour, comment vas-tu ?
Bonjour, moi ça va très bien.
Et toi, comment ça va ?""",
        "tres_repetitif": "A" * 100,
        "mix_random_repetitif": "ABXABYABZABXABYABZ",
        "doublon_simple": "ABAB",
        "palindrome": "ABCBAABCBA",
        "phrase_avec_variantes": "Le chat dort. Le chien dort. Le chat mange. Le chien mange.",
        "livre": text
    }

    for name, original in test_cases.items():
        encoded = lz77_encode(original)
        decoded = lz77_decode(encoded)
        rate = ratio(original, encoded)

        print(f"🧪 Test: {name}")
        print(f"  Original length : {len(original)}")
        print(f"  Encoded length  : {len(encoded)} triplets")
        print(f"  Taux de compression : {rate:.2f} %")
        if rate < 0:
            print(
                f"  ⚠️ Compression défavorable : la version compressée est plus lourde.")
        print(f"  ✅ Décodage correct : {decoded == original}")
        print("-" * 50)


if __name__ == "__main__":
    main()
