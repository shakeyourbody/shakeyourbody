import math

SIMPLIFY_DELTA_MAX = 0.005


def delta(p1, p2, at=0):
    return math.sqrt((p1[at+0]-p2[at+0])**2 + (p1[at+1]-p2[at+1])**2)


class Path:

    def __init__(self, points=[], at=0):
        self.points = points
        self.at = at

    def reduce(self, n_at_end):
        # TODO
        pass

    def simplify(self):

        to_remove = []

        for i, _ in enumerate(self.points[1:-1]):

            A = self.points[i-1]
            B = self.points[i+1]
            M = self.points[i]

            ab = delta(A, B, at=self.at)
            am = delta(A, M, at=self.at)
            bm = delta(B, M, at=self.at)

            p = (ab + am + bm) / 2
            area = math.sqrt(p*(p-ab)*(p-am)*(p-bm))
            h = 2*area/ab

            if h > SIMPLIFY_DELTA_MAX:
                to_remove.append(i+1)

        for i in to_remove[::-1]:
            del self.points[i]
