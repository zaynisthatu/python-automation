import os

items = os.listdir(".")
num = 34

for name in items:
    if name.endswith(".txt"):
        num += 1
        new_name = f"lec_{num}.txt"
        os.rename(name, new_name)
        print(f"Renamed '{name}' to '{new_name}'")

