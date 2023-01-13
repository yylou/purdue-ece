import os

timing = {}
path = "./result"
runs = os.listdir(path)
for each_run in sorted(runs):
    results = os.listdir(f"{path}/{each_run}/")
    for result in sorted(results):
        abs_path = f"{path}/{each_run}/{result}"
        with open(abs_path, "r") as FILE:
            content = FILE.read().split("\n")
            version = content[1].split()[-1]
            threads = content[2].split()[-1][:-1]

            init = float(content[-4].split()[-1])
            algo = float(content[-3].split()[-1])
            done = float(content[-2].split()[-1])

            if (version, threads) not in timing: timing[(version, threads)] = [.0, .0, .0]
            timing[(version, threads)][0] += init
            timing[(version, threads)][1] += algo
            timing[(version, threads)][2] += done

for k, v in timing.items():
    print(k, [f"{_/10:.5f}" for _ in v])
    