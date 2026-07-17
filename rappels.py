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


# %% ---------- exception custom -------------------

class MyCustomException(Exception):
    def __init__(self, msg, **options):
        super().__init__(f"{msg} - options: {options}")

try:
  raise MyCustomException("mon message", option1="value1", option2="value2")
except MyCustomException as e:
  print(e)


class RangeError(Exception):
    def __init__(self, val, min_val, max_val) -> None:
        self.val = val
        self.min_val = min_val
        self.max_val = max_val
    
    # générer le message de l'exception
    def __str__(self) -> str:
        return f"{self.val} not in [{self.min_val}, {self.max_val}]"
    
limits = (1, 10)
try:
    val = 20
    if not (limits[0] <= val <= limits[1]):
        raise RangeError(val, *limits)
except RangeError as e:
    print(e)  # 20 not in [1, 10]

# %% ------------ notion de générateur -----------------

from sys import getsizeof

def my_range(n):
    i = 0
    while i < n:
        yield i
        i += 1

n = 5
# g = my_range(n) # appeler la fonction génératrice créé un objet de type générateur
# for j in g:
#     print(j)

for j in my_range(n):  # on peut aussi directement itérer sur le générateur
    print(j)

# for _ in range(n):
#   print(next(g))

# intérêt du générateur : il ne stocke pas tous les éléments en mémoire, il les génère à la demande.
lst = list(range(1000))
# ---------------------  10   1000
print(getsizeof(lst))  # 856, 8056
gen = my_range(1000)
print(getsizeof(gen))  # 192, 192
r = range(1000)
print(getsizeof(r))    # 48, 48

# ------------------- getattr et setattr -------------------

class Truc:
    pass

t = Truc()
setattr(t, "param", 10)

print(t.param)  # 10
print(getattr(t, "param"))  # 10

print("-"*20)

fields = {"opt1": 1, "opt2": 2, "opt3": 3}
for key, value in fields.items():
    setattr(t, key, value)

print(t.opt1)  # 1
print(t.opt2)  # 2  