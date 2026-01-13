"""Glavne komande prilagođene srpskom jeziku i dodatne funkcije za unos podataka."""

ispiši = print
napiši = print

unos_broj = lambda prompt='': int(input(prompt))
unesi_broj = lambda prompt='': int(input(prompt))
input_broj = lambda prompt='': int(input(prompt))

unos_tekst = input
unesi_tekst = input
input_tekst = input

unos_lista_sa_razmacima = lambda prompt='': input(prompt).split()
unos_tuple_sa_razmacima = lambda prompt='': tuple(input(prompt).split())
unos_set_sa_razmacima = lambda prompt='': set(input(prompt).split())
unos_dict_sa_razmacima = lambda prompt='': dict(
    (par.split(':') for par in input(prompt).split())
)

"""More coming soon...
More coming soon...

Još dolazi uskoro...

"""