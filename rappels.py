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