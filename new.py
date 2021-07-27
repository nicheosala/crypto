'''
This file focuses on cyclic multiplicative groups.

Questions:
TODO how do I understand if a given multiplicative group is cyclic?
'''

from accessories import *


class FiniteField:
    '''
    Finite field with prime order.

    TODO extend this class so to consider finite fields of any order p ** m.
    '''

    def __init__(self, p: int) -> None:

        assert prime(p)
        self.p = p
        self.order = p
        self.characteristic = p
        self.mul = CyclicMultiplicativeGroup(p)

    def primitive_element(self, candidate: int) -> bool:
        return self.mul.generator(candidate)

    def primitive_elements(self) -> Iterator[int]:
        return self.mul.generators()


class CyclicMultiplicativeGroup:

    def __cyclic_condition(self, n: int) -> None:
        '''
        The group (Z_p*, ·) is cyclic if and only if n=1, 2, 4, n=p^k , n=2p^k
        where k≥1 and p≥3 is a prime integer.
        '''
        prime_factors_n = tuple(prime_factors(n))
        assert (n in (1, 2, 4) or
                len(prime_factors_n) == 2 and 2 in prime_factors_n and n % 4 != 0 or
                len(prime_factors_n) == 1), 'Z_p* is not a cyclic multiplicative group.'

    def __init__(self, p: int) -> None:
        self.__cyclic_condition(p)
        self.p = p
        self.order = totient(p)

    def element(self, candidate: int) -> bool:
        '''
        Return True if and only if :candidate is an element of Z_p*.

        :candidate is an element of Z_p* if and only if it is coprime with n.
        '''
        return coprime(candidate, self.p)

    def elements(self) -> Iterator[int]:
        '''
        Return all the elements of the cyclic multiplicative group Z_p*.
        TODO Is the cyclic condition required?
        '''
        return filter(self.element, range(1, self.p))

    def number_of_elements(self) -> int:
        '''
        The number of elements of a group is its order.

        You may drop this method and always use self.order.
        '''
        return self.order

    def number_of_generators(self) -> int:
        '''
        The number of generators is the number of elements coprime with
        the order of the group. i.e. the totient of the order of the group.
        '''
        return totient(self.order)

    def generator(self, candidate: int) -> bool:
        '''
        Return True if and only if the :candidate integer is a generator
        of the cyclic multiplicative group Z_p*.

        :candidate is a generator of Z_p* if and only if it is an element of Z_p* and
        pow(candidate, f, order(n)) != 1 mod n, for each proper divisor f of the order of the group.

        For example, given n = 54, order(n) == 18, candidate = 5 is a generator
        of Z_54, because 5 ** f mod n != 1 for each proper factor of 18: {2, 3, 6, 9}
        '''
        return self.element(candidate) and all(pow(candidate, f, self.p) != 1 for f in proper_natural_divisors(self.order))

    def generators(self) -> Iterator[int]:
        '''
        Return all the generators of Z_p*.
        '''
        return filter(self.generator, self.elements())

    def generators_from(self, gen: int) -> Iterator[int]:
        '''
        Return all the generators of Z_p*, knowing the generator :gen.

        Given any generator :gen of Z_p*, it is possible to compute all the
        other generators with pow(:gen, num, n), where num is a number coprime with the group order.

        For example, if n == 54 and so order == 18, the numbers coprime with 18 are: {1, 5, 7, 11, 13, 17},
        so the generators would be: pow(:gen, 1, 54), pow(:gen, 5, 54), ..., pow(:gen, 17, 54)
        '''
        assert self.generator(gen)

        return (pow(gen, num, self.p) for num in coprimes(self.order))

    def logarithm_existence(self, g: int, b: int) -> bool:
        '''
        Return True if and only if the discrete logarithm x = log(g, b) mod n exists.
        '''
        if not self.element(b):
            return False

        if not self.element(g):
            return False

        if not self.generator(g):
            return False

        return True

    def subgroups_orders(self) -> Iterator[int]:
        '''
        Return the order for each of the subgroups of Z_p*.

        For each factor of the order of Z_p*, there is a subgroup.
        This is true only because we are considering an abelian group.

        For example, if n == 54, then self.order == 18.
        The factors of 18 are: {1, 2, 3, 6, 9, 18}.
        So, we will have 6 subgroups.

        We can get the generator of the subgroup with x elements as: pow(g, n // x, n).
        Where g is a generator of Z_p*, x is any factor of self.order.
        '''
        return natural_divisors(self.order)

    def number_of_subgroups(self) -> int:
        return len(tuple(natural_divisors(self.order)))

    def subgroups(self) -> Iterator[tuple[int, set[int]]]:
        g: int = next(self.generators())    # Pick any generator of Z_p*
        return (self.__subgroup(d, g) for d in natural_divisors(self.order))

    def __subgroup(self, d: int, g: int):
        gen = pow(g, n // d, n)
        elements = set(pow(gen, i, n) for i in range(d))
        return d, elements

    def __repr__(self) -> str:
        return f'''
        p: {self.p}
        number of elements (order): {self.order}
        elements: {set(self.elements())}
        number of generators: {self.number_of_generators()}
        generators: {set(self.generators())}
        number of subgroups: {self.number_of_subgroups()}
        orders of the subgroups: {set(self.subgroups_orders())}
        '''


if __name__ == '__main__':
    n = 9
    group = CyclicMultiplicativeGroup(n)
    print(group)
