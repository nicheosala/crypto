'''
Nicolò Sala, 4th July 2021

https://jeremykun.com/2014/02/24/elliptic-curves-as-python-objects/
'''

from random import choice, randint
from accessories import *
from functools import cache


class EllipticCurve:
    '''
    Elliptic curve over a finite filed Fp, with p prime number greater than 3.
    '''

    def __init__(self, p: int, a: int, b: int) -> None:

        assert prime(p), 'p must be a prime number.'
        assert p > 3, 'p must be greater than 3.'
        assert 4 * a ** 3 + 27 * b ** 2 != 0, 'The curve is not smooth.'

        self.p = p
        self.a = a
        self.b = b

    @cache
    def __f(self, y):
        return pow(y, 2, self.p)

    @cache
    def __g(self, x):
        return (pow(x, 3, self.p) + self.a * x + self.b) % self.p

    def __repr__(self) -> str:
        return f"y^2 = x^3 + {self.a}x + {self.b} (mod {self.p})"

    def is_ec_point(self, p: 'Point') -> bool:

        if isinstance(p, Ideal):
            return p.curve == self

        return self.__f(p.y) == self.__g(p.x)

    def order(self) -> int:
        return len(tuple(self.points()))

    def _is_generator(self, p: 'Point') -> bool:
        return all(p * e != Ideal(self) for e in proper_natural_divisors(self.p - 1))

    def generators(self) -> Iterator['Point']:
        return filter(self._is_generator, self.points())

    def points(self) -> Iterator['Point']:
        '''
        Return an iterator over the points of the elliptic curve.
        TODO may be implemented more efficiently?
        '''
        return filter(self.is_ec_point, [Ideal(self)] + [Point(self, x, y) for x in range(self.p) for y in range(self.p)])

    def group_table(self) -> tuple[tuple['Point', 'Point', 'Point']]:
        return ((p1, p2, p1 + p2) for p1 in self.points() for p2 in self.points())


class Point:

    def __init__(self, curve: EllipticCurve, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.curve = curve

        # if not curve.is_ec_point(self):
        #    raise Exception(f'The point is not on the given elliptic curve!')

    def __neg__(self):
        return Point(self.curve, self.x, -self.y % self.curve.p)

    def __add__(self, Q: 'Point') -> 'Point':

        assert self.curve == Q.curve, 'You cannot sum up points on different curves.'

        if isinstance(Q, Ideal):
            return self

        if isinstance(self, Ideal):
            return Q

        p1, p2, p = self, Q, self.curve.p
        if p1 != p2:
            i = inverse(p1.x - p2.x, p)
            if i == 0:
                return Ideal(self.curve)
            else:
                l = ((p1.y - p2.y) * i) % p
                x = (l ** 2 - p1.x - p2.x) % p
                y = (l * (p1.x - x) - p1.y) % p
        else:
            i = inverse(2 * p1.y, p)
            if i == 0:
                return Ideal(self.curve)
            else:
                l = ((3 * p1.x ** 2 + self.curve.a) * i) % p
                x = (l ** 2 - 2 * p1.x) % p
                y = (- p1.y + l * (p1.x - x)) % p

        return Point(self.curve, x, y)

    def __sub__(self, Q: 'Point') -> 'Point':
        return self + -Q

    def __eq__(self, o: object) -> bool:
        return (self.__class__ == o.__class__ and
                self.x == o.x and self.y == o.y and
                self.curve == o.curve)

    def __mul__(self, n: int) -> 'Point':
        if not isinstance(n, int):
            raise Exception(
                "Can't scale a point by something which isn't an int!")
        else:
            if n < 0:
                return -self * -n
            if n == 0:
                return Ideal(self.curve)
            else:
                # Q = Ideal(self.curve)
                # for R in [self] * n:
                #     Q = Q + R
                # return Q
                Q = self
                R = self if n & 1 == 1 else Ideal(self.curve)

                i = 2
                while i <= n:
                    Q = Q + Q

                    if n & i == i:
                        R = Q + R

                    i = i << 1
            return R

    def __rmul__(self, n):
        return self * n

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"


class Ideal(Point):
    def __init__(self, curve: EllipticCurve) -> None:
        self.curve = curve

    def __neg__(self) -> Point:
        return self

    def __add__(self, Q: Point) -> Point:
        return Q

    def __eq__(self, o: object) -> bool:
        return (self.__class__ == o.__class__ and
                self.curve == o.curve)

    def __repr__(self) -> str:
        return "Ideal"


def ECDH_keygen(n: int, P: Point) -> tuple[int, Point]:
    from random import randint
    priv = randint(2, n - 1)

    return priv, priv * P


def ECDH_key_exchange():
    '''Elliptic Curve Diffie-Hellman key exchange (ECDH)'''
    n, P = ec.order(), next(ec.generators())

    k_priv_a, k_pub_a = ECDH_keygen(n, P)
    k_priv_b, k_pub_b = ECDH_keygen(n, P)

    k_ab = k_priv_a * k_pub_b
    k_ba = k_priv_b * k_pub_a

    assert k_ab == k_ba


def ECEG_encrypt(m: Point, n: int, P: Point, s_P: Point) -> tuple[Point, Point]:
    l = randint(1, n - 1)
    return l * P, m + l * s_P


def ECEG_decrypt(gamma: Point, delta: Point, n: int, s: int) -> Point:
    return delta - s * gamma


def ECEG_cryptoscheme():
    '''Elliptic Curve ElGamal cryptoscheme.'''
    n, P = ec.order(), next(ec.generators())
    s: int = randint(1, n - 1)

    # Just for testing, I take a random point of the EC as plaintext.
    m: Point = choice(tuple(ec.points()))
    assert m in ec.points()

    gamma, delta = ECEG_encrypt(m, n, P, s * P)
    cleartext = ECEG_decrypt(gamma, delta, n, s)

    # print(f'm: {m}, gamma: {gamma}, delta: {delta}, cleartext: {cleartext}')
    assert m == cleartext


if __name__ == '__main__':
    ec = EllipticCurve(11, 1, 6)
    print(ec)
    print(tuple(ec.points()))
    # print(Point(ec, 2, 7) * 2)
    # print(tuple(ec.group_table()))
    # print(tuple(ec.generators()))
    # ECDH_key_exchange()
    # ECEG_cryptoscheme()
