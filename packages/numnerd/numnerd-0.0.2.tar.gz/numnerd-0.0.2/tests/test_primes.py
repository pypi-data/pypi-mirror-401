from numnerd.primes import (
    is_prime, prime_factorization, is_perfect_number,
    sieve_of_eratosthenes, lcm, is_coprime, euler_totient,
    is_sophie_germain_prime, is_twin_prime, mobius_function, goldbach_partition,
    prime_pi, is_semiprime, is_mersenne_prime, is_chen_prime, next_prime, prev_prime,
    is_fermat_prime
)

def test_is_prime():
    assert is_prime(2) is True
    assert is_prime(3) is True
    assert is_prime(4) is False
    assert is_prime(17) is True
    assert is_prime(25) is False
    assert is_prime(1) is False
    assert is_prime(-7) is False

def test_prime_factorization():
    assert prime_factorization(12) == [2, 2, 3]
    assert prime_factorization(13) == [13]
    assert prime_factorization(100) == [2, 2, 5, 5]
    assert prime_factorization(1) == []

def test_is_perfect_number():
    assert is_perfect_number(6) is True
    assert is_perfect_number(28) is True
    assert is_perfect_number(496) is True
    assert is_perfect_number(12) is False
    assert is_perfect_number(1) is False

def test_sieve_of_eratosthenes():
    assert sieve_of_eratosthenes(10) == [2, 3, 5, 7]
    assert sieve_of_eratosthenes(1) == []
    assert sieve_of_eratosthenes(20) == [2, 3, 5, 7, 11, 13, 17, 19]

def test_lcm():
    assert lcm(4, 6) == 12
    assert lcm(5, 7) == 35
    assert lcm(0, 5) == 0
    assert lcm(21, 6) == 42

def test_is_coprime():
    assert is_coprime(8, 15) is True # Factors: 2, 3, 5 (None common)
    assert is_coprime(12, 18) is False # Common: 2, 3
    assert is_coprime(17, 19) is True

def test_euler_totient():
    assert euler_totient(9) == 6 # 1, 2, 4, 5, 7, 8
    assert euler_totient(10) == 4 # 1, 3, 7, 9
    assert euler_totient(1) == 1
    assert euler_totient(13) == 12 # Prime p -> p-1

def test_is_sophie_germain_prime():
    assert is_sophie_germain_prime(2) is True # 2*2+1=5 (prime)
    assert is_sophie_germain_prime(3) is True # 2*3+1=7 (prime)
    assert is_sophie_germain_prime(5) is True # 2*5+1=11 (prime)
    assert is_sophie_germain_prime(7) is False # 2*7+1=15 (not prime)

def test_is_twin_prime():
    assert is_twin_prime(3) is True # (3,5)
    assert is_twin_prime(5) is True # (3,5) or (5,7)
    assert is_twin_prime(11) is True # (11,13)
    assert is_twin_prime(23) is False # 21 not prime, 25 not prime

def test_mobius_function():
    assert mobius_function(1) == 1
    assert mobius_function(2) == -1 # One factor (2)
    assert mobius_function(6) == 1 # Two factors (2,3) -> (-1)^2
    assert mobius_function(12) == 0 # Squared factor (2^2)
    assert mobius_function(30) == -1 # Three factors (2,3,5) -> (-1)^3

def test_goldbach_partition():
    assert sum(goldbach_partition(4)) == 4
    assert sum(goldbach_partition(10)) == 10
    assert goldbach_partition(28) is not None
    # For small numbers output is deterministic due to sieve order
    # 10 = 3 + 7 (usually finds first pair)

def test_prime_pi():
    assert prime_pi(10) == 4 # 2, 3, 5, 7
    assert prime_pi(20) == 8
    assert prime_pi(1) == 0

def test_is_semiprime():
    assert is_semiprime(4) is True # 2*2
    assert is_semiprime(6) is True # 2*3
    assert is_semiprime(9) is True # 3*3
    assert is_semiprime(12) is False # 2*2*3
    assert is_semiprime(13) is False # Prime

def test_is_mersenne_prime():
    assert is_mersenne_prime(3) is True # 2^2 - 1
    assert is_mersenne_prime(7) is True # 2^3 - 1
    assert is_mersenne_prime(31) is True # 2^5 - 1
    assert is_mersenne_prime(11) is False # Prime but not Mersenne form
    assert is_mersenne_prime(15) is False # Not prime

def test_is_chen_prime():
    assert is_chen_prime(13) is True # 13+2=15 (semiprime 3*5)
    assert is_chen_prime(3) is True # 3+2=5 (prime)
    assert is_chen_prime(14) is False # Not prime
    # 43 is prime. 43+2=45 (3*3*5 - not semiprime, 3 factors).
    assert is_chen_prime(43) is False 

def test_next_prime():
    assert next_prime(1) == 2
    assert next_prime(2) == 3
    assert next_prime(13) == 17
    assert next_prime(19) == 23

def test_prev_prime():
    assert prev_prime(3) == 2
    assert prev_prime(10) == 7
    assert prev_prime(2) is None

def test_is_fermat_prime():
    assert is_fermat_prime(3) is True # k=0
    assert is_fermat_prime(17) is True # k=2
    assert is_fermat_prime(65537) is True # k=4
    assert is_fermat_prime(7) is False # Prime but not Fermat
    assert is_fermat_prime(258) is False
