from .constraints import total_penalty


def total_fee(state):
    # ret sum fee dari state.placed_vehicles()
    raise NotImplementedError


def evaluate(state):
    # ret total_fee(state) - total_penalty(state)
    raise NotImplementedError
