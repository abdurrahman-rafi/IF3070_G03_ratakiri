import argparse
import json
import random

from .model.instance import load_instance
from .model.state import DockState
from .model.objective import evaluate
from .model.constraints import total_penalty


def main():
    # parse args: --instance, --seed (default 945), --algo (nanti)
    # vehicles, ships = load_instance(args.instance)
    # rng = random.Random(args.seed)
    # state = DockState.initial_state(vehicles, ships, rng)
    # print state.to_dict(), evaluate(state), total_penalty(state)
    raise NotImplementedError


if __name__ == "__main__":
    main()
