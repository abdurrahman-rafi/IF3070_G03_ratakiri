import argparse
import json
import random

from .model.instance import load_instance
from .model.state import DockState
from .model.objective import evaluate
from .model.constraints import is_feasible


# Preview: membaca instance, membuat satu initial state random, lalu mencetak
# placement, value, dan feasible atau tidaknya.
# Argumen: --instance (path json), --seed (default 945).
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--instance", required=True)
    parser.add_argument("--seed", type=int, default=945)
    args = parser.parse_args()

    vehicles, ships = load_instance(args.instance)
    rng = random.Random(args.seed)
    state = DockState.initial_state(vehicles, ships, rng)
    print(json.dumps(state.to_dict(), indent=2))
    print("value:", evaluate(state))
    print("feasible:", is_feasible(state))


if __name__ == "__main__":
    main()
