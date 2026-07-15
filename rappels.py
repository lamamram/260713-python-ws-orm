# %% --------- dictionnaire : get() --------------

d = {"a": 1, "b": 2, "c": 3}
d["a"] # 1
# d["z"] # KeyError
d.get("z")  # None
d.get("z", 0)  # 0

# %% --------- utilisation du ** sur un dictionnaire pour injecter des paramètres -----------

d = {"a": 1, "b": 2, "c": 3}
def f(a, b, c):
    return a + b + c

f(**d)  # 6

other_d = { **d, "x": 10, "y": 20, "z": 30}
other_d  # {'a': 1, 'b': 2, 'c': 3, 'x': 10, 'y': 20, 'z': 30}


