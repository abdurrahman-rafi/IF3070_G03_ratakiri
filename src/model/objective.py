from .constraints import is_feasible


# Keluaran: jumlah fee dari semua vehicle placed (di ship mana pun).
def total_fee(state):
    return sum(state.vehicles[vid]["fee"] for vid in state.placed_vehicles())


# Objective function yang dimaksimalkan semua algoritma.
# Keluaran: 0 kalau ada constraint yang dilanggar, selain itu total_fee(state).
# Menggantikan draft fitnessScore = value - penalty: neighbor tidak disaring,
# yang melanggar constraint tetap dibangkitkan dan hanya bernilai 0.
def evaluate(state):
    if not is_feasible(state):
        return 0
    return total_fee(state)
