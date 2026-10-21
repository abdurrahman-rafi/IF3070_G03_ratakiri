from .base import SearchRecorder
from ..model.instance import OUTSIDE
from ..model.objective import evaluate
from ..model.state import DockState
from ..model.constraints import can_place


# Crossover satu titik: gen [0, k) dari parent_a dan gen [k, n) dari parent_b.
# Masukan: dua chromosome (list gen, urut sesuai state.order), rng.
# Keluaran: chromosome anak.
def one_point_crossover(parent_a, parent_b, rng):
    k = rng.randrange(1, len(parent_a))
    return [dict(g) for g in parent_a[:k]] + [dict(g) for g in parent_b[k:]]


# Memperbaiki chromosome supaya pasti feasible (repair)
# Crossover/mutasi sering menghasilkan overlap, keluar geladak, atau overweight.
# Padahal state yang melanggar bernilai 0 di evaluate sehingga populasi mudah penuh nilai 0 (plateau).
# Cara kerja: mulai dari state kosong (semua OUTSIDE),
# lalu tiap gen yang minta masuk ship dicoba ditaruh dengan can_place sesuai urutan gen;
# yang gagal tetap OUTSIDE.
# Masukan: template (DockState acuan), chromosome.
# Keluaran: DockState feasible.
def repair(template, chromosome):
    state = template.from_chromosome(chromosome)
    for vid in state.order:
        state.placement[vid] = {
            "ship": OUTSIDE,
            "x": None,
            "y": None,
            "orient": state.placement[vid]["orient"]}
    for vid, gene in zip(state.order, chromosome):
        if gene["ship"] == OUTSIDE:
            continue
        if can_place(state, vid, gene["ship"], gene["x"], gene["y"], gene["orient"]):
            state.placement[vid] = dict(gene)
    return state


# Seleksi roulette wheel: peluang terpilih sebanding dengan fitness (value) tiap individu.
# Putar wheel: r acak di [0, total_fitness],
# lalu ambil individu pertama yang jumlah kumulatif fitness-nya sudah mencapai r.
# Kalau total fitness 0 (semua individu bernilai 0), wheel tidak bisa dipakai, jadi dipilih uniform
# Masukan: values (fitness tiap individu), rng.
# Keluaran: index individu terpilih.
def roulette_select(values, rng):
    total = sum(values)
    if total <= 0:
        return rng.randrange(len(values))
    r = rng.uniform(0, total)
    cumulative = 0
    for i, value in enumerate(values):
        cumulative += value
        if cumulative >= r:
            return i
    return len(values) - 1


# Mutasi: satu langkah neighbor random (swap/relocate/rotate) pada chromosome.
# Masukan: state (hasil repair anak), rng.
# Keluaran: state baru (belum tentu feasible).
def mutate(state, rng):
    neighbor = state.random_neighbor(rng)
    return neighbor if neighbor is not None else state


# Genetic Algorithm.
# Representasi: chromosome = state.to_chromosome(), satu gen {ship, x, y, orient} per vehicle.
# Fitness: evaluate(state) = total fee kalau feasible.
# Populasi awal: initial_state + (population_size - 1) state random feasible.
# Tiap generasi: elitism (elite individu terbaik langsung lolos, default 1),
# lalu anak dibuat dari roulette wheel -> # one-point crossover (peluang crossover_rate) ->
# mutasi (peluang mutation_rate) -> repair supaya feasible.
# Karena elitism, nilai maksimum populasi tidak pernah turun antar generasi.
# Masukan: initial_state, rng, population_size, iterations (= jumlah generasi),
# dan parameter tambahan (crossover_rate, mutation_rate, elite).
# Keluaran: dict hasil dari SearchRecorder.finish; final = individu terbaik pada generasi terakhir.
def genetic_algorithm(initial_state, rng, population_size=50, iterations=100,
                      crossover_rate=0.9, mutation_rate=0.1, elite=1):
    params = {"population_size": population_size,
              "iterations": iterations,
              "crossover_rate": crossover_rate,
              "mutation_rate": mutation_rate,
              "elite": elite}
    recorder = SearchRecorder("genetic_algorithm", initial_state, params)
    elite = min(elite, population_size)
 
    population = [initial_state.copy()]
    while len(population) < population_size:
        population.append(DockState.initial_state(initial_state.vehicles, initial_state.ships, rng))
    values = [evaluate(s) for s in population]
    recorder.record_population(population, values)
 
    for _ in range(iterations):
        ranked = sorted(range(len(population)), key=lambda i: values[i], reverse=True)
        next_population = [population[i].copy() for i in ranked[:elite]]
 
        while len(next_population) < population_size:
            parent_a = population[roulette_select(values, rng)]
            parent_b = population[roulette_select(values, rng)]
            if rng.random() < crossover_rate and len(parent_a.order) > 1:
                chromosome = one_point_crossover(parent_a.to_chromosome(), parent_b.to_chromosome(), rng)
            else:
                chromosome = parent_a.to_chromosome()
            child = repair(initial_state, chromosome)
            if rng.random() < mutation_rate:
                child = repair(initial_state, mutate(child, rng).to_chromosome())
            next_population.append(child)
 
        population = next_population
        values = [evaluate(s) for s in population]
        recorder.record_population(population, values)
 
    best = max(range(len(population)), key=lambda i: values[i])
    return recorder.finish(population[best], iterations,
                           extra={"population_size": population_size})