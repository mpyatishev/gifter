import datetime
import math
import random


class Gift:
    def __init__(self, name='', quantity=None,
                 drawing_start=None, drawing_end=None):
        self.name = name
        self.quantity = quantity
        self.winners = 0
        self.drawing_start = drawing_start
        self.drawing_end = drawing_end

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


def select_gift(gifts):
    today = datetime.date.today()
    infinite_gifts = [g for g in gifts if g.quantity is None]
    finite_gifts = [
        g for g in gifts
        if g.quantity is not None and g.quantity > 0 and
        g.drawing_start <= today < g.drawing_end
    ]

    if not finite_gifts:
        return random.choice(infinite_gifts)

    probabilities = {
        g: get_probability_puasson(g) for g in finite_gifts
    }
    sum_probabilities = sum(p for p in probabilities.values())

    random_value = random.random()

    if random_value < sum_probabilities:
        return random.choice(infinite_gifts)

    gift = sorted(probabilities, key=lambda g: probabilities[g])[0]
    return gift


def get_probability(gift):
    today = datetime.date.today()
    time_pass = (today - gift.drawing_start).seconds
    time_left = (gift.drawing_end - today).seconds
    hit_rate = float(gift.winners) / (time_pass or 0.5)
    p = abs(gift.quantity + gift.winners - time_left * hit_rate)

    return ((gift.drawing_end - gift.drawing_start).seconds) / p


def get_probability_puasson(gift):
    # Puasson
    gift_count = gift.quantity + gift.winners
    lam = gift_count / (gift.drawing_end - gift.drawing_start).total_seconds()
    k = gift.quantity
    p = math.pow(lam, k) * math.exp(-k) / math.factorial(k)

    return p
