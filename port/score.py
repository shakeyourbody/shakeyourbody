from enum import Enum


ranges = dict(
    HIT=(1, lambda c: c + 0.1),
    NEARLY=(0.5, lambda c: c),
    MISS=(0, lambda c: 1)
)


class Score:

    def __init__(self):
        self.score = 0
        self.combo_multi = 1

    def step(self, dist):
        score_adder, multi = self.range(dist)
        self.combo_multi = multi(self.combo_multi)
        self.score += score_adder * self.combo_multi

    def range(self, dist):
        if dist < 40:
            return ranges['HIT']
        elif dist < 80:
            return ranges['NEARLY']
        else:
            return ranges['MISS']
