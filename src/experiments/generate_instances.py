import argparse
import json
import os
import random

# Instance uji yang dibuat ulang dengan seed tetap supaya hasilnya selalu sama.
# Format tiap entri: (seed, ships, jumlah vehicle, rentang w, rentang l, rentang berat).
INSTANCES = {
    "instance_small": (11, [{"id": 0, "w": 8, "l": 10, "capacity": 30}], 8, (2, 4), (2, 5), (3, 9)),
    "instance_tight_space": (12, [{"id": 0, "w": 8, "l": 12, "capacity": 200}], 14, (2, 4), (2, 6), (3, 9)),
    "instance_tight_weight": (13, [{"id": 0, "w": 12, "l": 16, "capacity": 45}], 14, (2, 4), (2, 5), (4, 14)),
    "instance_multiship_hard": (14, [{"id": 0, "w": 10, "l": 20, "capacity": 70},
                                     {"id": 1, "w": 8, "l": 12, "capacity": 40},
                                     {"id": 2, "w": 6, "l": 10, "capacity": 30}], 30, (2, 4), (2, 6), (3, 10)),
}


# Membuat daftar vehicle random. Fee kira-kira sebanding dengan luas dan berat,
# lalu diberi variasi acak 0,7 sampai 1,3 dan dibulatkan ke kelipatan 5.
def random_vehicles(rng, count, w_range, l_range, weight_range):
    vehicles = []
    for i in range(count):
        w, l = rng.randint(*w_range), rng.randint(*l_range)
        weight = rng.randint(*weight_range)
        fee = round((w * l * 2.5 + weight * 3) * rng.uniform(0.7, 1.3) / 5) * 5
        vehicles.append({"id": f"V{i + 1:02d}", "w": w, "l": l, "fee": fee, "weight": weight,
                         "eta": rng.randint(1, 7)})
    return vehicles


# Membuat daftar ship random untuk instance custom: lebar 6 sampai 12, panjang 8 sampai 20,
# dan kapasitas sepertiga luas deck supaya berat ikut membatasi.
def random_ships(rng, count):
    ships = []
    for ship_id in range(count):
        w, l = rng.randint(6, 12), rng.randint(8, 20)
        ships.append({"id": ship_id, "w": w, "l": l, "capacity": w * l // 3})
    return ships


# Menulis satu instance ke file json.
def write_instance(path, ships, vehicles):
    with open(path, "w", encoding="utf-8") as out_file:
        json.dump({"ships": ships, "vehicles": vehicles}, out_file, indent=2)
    print(path)


# Tanpa argumen: menulis ulang semua instance di INSTANCES ke data/.
# Dengan --ships dan --vehicles: membuat satu instance custom, misalnya untuk demo
#   python -m src.experiments.generate_instances --ships 4 --vehicles 40 --seed 1 --out data/demo.json
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ships", type=int)
    parser.add_argument("--vehicles", type=int)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--out", default=os.path.join("data", "instance_custom.json"))
    args = parser.parse_args()

    if args.ships or args.vehicles:
        rng = random.Random(args.seed)
        ships = random_ships(rng, args.ships or 1)
        write_instance(args.out, ships, random_vehicles(rng, args.vehicles or 10, (2, 4), (2, 6), (3, 10)))
        return

    for name, (seed, ships, count, w_range, l_range, weight_range) in INSTANCES.items():
        rng = random.Random(seed)
        write_instance(os.path.join("data", f"{name}.json"), ships,
                       random_vehicles(rng, count, w_range, l_range, weight_range))


if __name__ == "__main__":
    main()
