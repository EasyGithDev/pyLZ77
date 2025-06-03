# LZ77

Ce document a pour but de comprendre le fonctionnement d’un algorithme qui a marqué l’histoire du traitement de l’information.

En 1977, Abraham Lempel et Jacob Ziv ont inventé un algorithme basé sur la détection de séquences répétées dans un texte, permettant ainsi de réduire sa taille. Il s’agit donc d’un algorithme de compression de données.

## Principe général de l’algorithme

L’algorithme fonctionne de la manière suivante :
On parcourt linéairement le texte à compresser, caractère par caractère.
À chaque étape, on recherche dans une fenêtre virtuelle (appelée parfois « fenêtre glissante ») le plus long motif correspondant au début du texte restant à parcourir (appelé suffixe).

Cette recherche permet de construire un triplet :

* la distance (ou position) entre le motif trouvé et la position actuelle,
* la longueur du motif trouvé,
* et le caractère suivant ce motif.

Le résultat de la compression est donc une suite de triplets.

---

## Exemple

Chaîne initiale :

```
Texte :     A B A B C A B C D
Indices :   0 1 2 3 4 5 6 7 8
```

On note :

* `S` : la chaîne de caractères à compresser
* `I` : l’indice courant dans la chaîne

L’indice `I` prend successivement les valeurs de 0 à 8, ce qui formalise notre parcours du texte.

### Étape 1

`I = 0`
Caractère courant : A
Fenêtre virtuelle (FV) : ""
Suffixe à venir (SC) : A B A B C A B C D

À cette étape, on recherche dans la fenêtre virtuelle FV ("") le motif le plus long du suffixe à venir SC (A B A B C A B C D).

Aucun motif n’est trouvé car la fenêtre est vide.

Triplet : (0, 0, A)

---

### Étape 2

`I = 1`
Caractère courant : B
Fenêtre virtuelle : A
Suffixe : B A B C A B C D

À cette étape, on recherche dans la fenêtre virtuelle FV (A) le motif le plus long du suffixe à venir SC (B A B C A B C D).

Aucun motif "B", "BA", etc. n’est trouvé dans A.

Triplet : (0, 0, B)

---

### Étape 3

`I = 2`
Caractère courant : A
Fenêtre : A B
Suffixe : A B C A B C D

À cette étape, on recherche dans la fenêtre virtuelle FV (A B) le motif le plus long du suffixe à venir SC (A B C A B C D).

Le motif "A B" est trouvé dans la fenêtre (à partir de l’indice J = 0).

Longueur = 2
Distance = 2 - (0 + 0) = 2
Caractère suivant le motif = C

Triplet : (2, 2, C)

---

### Étape 4

Puisque le motif trouvé est de longueur 2, on effectue un saut de 2 + 1 = 3.
I = 2 + 3 = 5

`I = 5`
Caractère courant : A
Fenêtre virtuelle (FV) : A B A B C
Suffixe à venir (SC) : A B C D

À cette étape, on recherche dans la fenêtre virtuelle FV (A B A B C) le motif le plus long du suffixe à venir SC (A B C D).

Le motif "A B C" est trouvé dans la fenêtre, à partir de l’indice 0.

Longueur = 3
Distance = 5 - (0 + 0) = 5
Caractère suivant = D

Triplet : (5, 3, D)

---

## Tableau synthétique de l'exemple

| Étape | I | Fenêtre virtuelle (FV) | Suffixe à venir (SC) | Motif trouvé | Distance | Longueur | Caractère suivant | Triplet   |
| ----- | - | ---------------------- | -------------------- | ------------ | -------- | -------- | ----------------- | --------- |
| 1     | 0 | ""                     | A B A B C A B C D    | –            | 0        | 0        | A                 | (0, 0, A) |
| 2     | 1 | A                      | B A B C A B C D      | –            | 0        | 0        | B                 | (0, 0, B) |
| 3     | 2 | A B                    | A B C A B C D        | A B          | 2        | 2        | C                 | (2, 2, C) |
| 4     | 5 | A B A B C              | A B C D              | A B C        | 5        | 3        | D                 | (5, 3, D) |

---

## Récapitulatif : Comprendre LZ77

L’algorithme LZ77 (Lempel-Ziv 1977) permet de compresser un texte en repérant les motifs répétitifs.

### Fonctionnement général

* On lit la chaîne caractère par caractère.
* À chaque position, on cherche le motif le plus long déjà rencontré dans ce qu’on appelle la fenêtre virtuelle (les caractères précédents).
* On encode ce motif sous la forme d’un triplet :
  (distance, longueur, caractère suivant)

---

### Les variables utilisées

| Nom | Signification                                                                     |
| --- | --------------------------------------------------------------------------------- |
| S   | Chaîne de caractères à compresser                                                 |
| I   | Indice courant dans la chaîne                                                     |
| FV  | Fenêtre virtuelle (les caractères déjà parcourus, pouvant être de taille limitée) |
| SC  | Suffixe à venir, c’est-à-dire la partie de la chaîne encore non traitée           |
| J   | Indice dans la fenêtre où le motif a été trouvé                                   |
| D   | Distance entre la position actuelle et la position du motif dans la fenêtre       |
| L   | Longueur du motif trouvé                                                          |
| C   | Caractère suivant le motif                                                        |

---

### Formules importantes

* Distance :
  `D = I - (start + J)`
  où `start` est l’indice réel du début de la fenêtre virtuelle.

* Triplet :
  `(distance, longueur, caractère suivant)`
  Il représente l’information compressée.

---

### Traduction en langage clair

* Distance : combien de caractères en arrière il faut reculer pour retrouver le motif
* Longueur : combien de caractères du motif on a retrouvés
* Caractère suivant : ce qui suit immédiatement le motif (le premier caractère nouveau)


Parfait. Voici une section spécifique à insérer dans ton cours, qui vise à **clarifier la notion de "distance"** dans LZ77. Elle est conçue pour être placée **juste après la section "Récapitulatif"**, avant d’éventuellement aborder la décompression.

---

## Comprendre la notion de distance dans LZ77

Lors de la compression avec LZ77, l’un des éléments les plus difficiles à comprendre est la **distance**, c’est-à-dire le premier élément du triplet : `(distance, longueur, caractère)`.

En effet, tant que l'on n'a pas vu comment se déroule la **décompression**, cette notion peut sembler abstraite. Voici donc quelques explications pour mieux la saisir.

### 1. Ce que signifie la distance

La distance représente **combien de caractères il faut "reculer"** depuis la position actuelle dans le texte pour retrouver le **début d’un motif déjà rencontré**.

Autrement dit, lorsque l’on se trouve à la position `I` dans le texte :

* on regarde dans la fenêtre virtuelle (qui contient les caractères déjà lus),
* si un motif du suffixe à venir est présent dans cette fenêtre,
* alors on mesure la distance qui nous sépare de ce motif dans la fenêtre.

On utilise cette distance **pendant la décompression** pour dire :
**« Va X caractères en arrière dans ce que tu as déjà reconstruit, et copie Y caractères »**.

C’est donc une **instruction**, mais son effet **ne devient évident qu’au moment de la relecture ou de la reconstruction du texte**.

### 2. Un exemple visuel

Prenons cette chaîne :

```
Texte :     A B A B C A B C D
Indices :   0 1 2 3 4 5 6 7 8
```

À l’indice `I = 5`, on a :

* Suffixe à venir : `A B C D`
* Fenêtre virtuelle : `A B A B C`

On remarque que le motif `A B C` est déjà dans la fenêtre (à partir de l’indice 0 dans la fenêtre).

La distance se calcule comme :

```
distance = I - (start + j)
```

où :

* `I` est la position actuelle,
* `start` est le début réel de la fenêtre (dans le texte),
* `j` est la position du motif trouvé dans la fenêtre.

Dans notre cas :
`distance = 5 - (0 + 0) = 5`

Cela signifie :
**« Pour reconstituer ce passage plus tard, il suffira de reculer de 5 caractères dans ce qui a déjà été écrit, et de recopier 3 caractères. »**

### 3. Pourquoi ce n’est pas intuitif au début

Lorsqu’on compresse, on ne voit pas encore le texte compressé se reconstruire.
On encode une "référence" vers l’arrière, sans voir ce que cela va produire.

Ce n’est qu’en **décompressant** qu’on comprend réellement :

* ce que cette distance désigne,
* et ce qu’elle permet de reconstruire.

Tu as tout à fait raison : la gestion de la **fenêtre glissante** est un **élément fondamental** de LZ77, et elle mérite une section à part entière.

Voici une section que tu peux ajouter juste **avant** la section "Comprendre la notion de distance dans LZ77", dans ton document :

---

## La fenêtre virtuelle est glissante et de taille fixe

Dans l’algorithme LZ77, la **fenêtre virtuelle** (ou "fenêtre glissante") joue un rôle central. Elle contient les caractères **déjà lus** dans le texte, et sert de référence pour retrouver des motifs répétitifs.

### 1. Une fenêtre de taille limitée

Dans la plupart des implémentations, la fenêtre virtuelle n’est pas infinie :
elle est limitée à une taille maximale (par exemple, 4096 caractères).

Cela signifie que **seuls les derniers caractères lus** peuvent être utilisés pour rechercher des répétitions. Les caractères les plus anciens **sortent de la fenêtre** au fur et à mesure de l’avancée dans le texte.

### 2. Déplacement de la fenêtre

À chaque saut dans le texte (lorsqu’un triplet a été produit), l’indice courant `I` avance. Si `I` dépasse la taille de la fenêtre, alors on **fait glisser la fenêtre vers la droite** d’un caractère.

Cela revient à **ajuster l’indice de début de fenêtre**, souvent noté `start`.
On a donc :

```python
start = max(0, i - window_size)
```

Concrètement, cela signifie que la fenêtre contient toujours au plus `window_size` caractères :

* Si `i < window_size`, alors `start = 0`
* Si `i ≥ window_size`, alors `start` augmente avec `i` (la fenêtre glisse)

### 3. Exemple

Si on lit une chaîne très courte, la fenêtre reste souvent vide ou partiellement remplie :

```
Texte : A B A B C A
i = 0 → fenêtre = ""
i = 1 → fenêtre = A
i = 2 → fenêtre = A B
```

Mais dès que `i` dépasse la taille fixée (ex. : 4096), on ne garde plus que les derniers 4096 caractères dans la fenêtre.

### 4. Pour les petits exemples

Dans les exemples pédagogiques (comme ceux utilisés avec des chaînes de 10 ou 20 caractères), on considère que la fenêtre virtuelle est **aussi grande que nécessaire**, donc `start = 0` tout au long de l'exécution.

Cela simplifie les calculs et la compréhension.
Dans ce cas, la distance se calcule simplement par :

```math
distance = i - j
```

où `j` est l’indice du motif dans la fenêtre virtuelle.

