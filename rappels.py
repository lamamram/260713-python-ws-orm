# %% --------- dictionnaire : get() --------------

d = {"a": 1, "b": 2, "c": 3}
d["a"] # 1
# d["z"] # KeyError
d.get("z")  # None
d.get("z", 0)  # 0