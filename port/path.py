import math

SIMPLIFY_DELTA_MAX = 0.005
TOO_NEAR_THRESHOLD = 0.009


def delta(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)


class Path:

    def __init__(self, points=[], at=0):
        self.points = points
        self.at = at

    def simplify(self):
        self.remove_same()
        self.remove_too_near()
        self.remove_delta_too_high()

    def remove_delta_too_high(self):

        to_remove = []

        for i, _ in enumerate(self.points[1:-1]):

            A = self.points[i-1]
            B = self.points[i+1]
            M = self.points[i]

            ab = delta(A[self.at], B[self.at])
            am = delta(A[self.at], M[self.at])
            bm = delta(B[self.at], M[self.at])

            p = (ab + am + bm) / 2
            area = math.sqrt(p*(p-ab)*(p-am)*(p-bm))
            h = 2*area/ab if ab > 0 else 0

            if h > SIMPLIFY_DELTA_MAX:
                to_remove.append(i+1)

        for i in to_remove[::-1]:
            del self.points[i]

    def remove_too_near(self):
        to_remove = []

        for i, A in enumerate(self.points[:-1]):
            B = self.points[i+1]
            if delta(A[self.at], B[self.at]) < TOO_NEAR_THRESHOLD:
                to_remove.append(i+1)

        for i in to_remove[::-1]:
            del self.points[i]

    def remove_same(self):
        to_remove = []

        for i, A in enumerate(self.points[:-1]):
            A = A[self.at]
            B = self.points[i+1][self.at]
            if A.x == B.x and A.y == B.y:
                to_remove.append(i)

        for i in to_remove[::-1]:
            del self.points[i]
