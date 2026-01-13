import math
from typing import List, Optional, Tuple

def is_prime(n: int) -> bool:
    """
    Checks if a number is prime using a optimized trial division method.

    Args:
        n (int): The integer to check for primality.

    Returns:
        bool: True if n is prime, False otherwise.
        
    Example:
        >>> is_prime(17)
        True
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def prime_factorization(n: int) -> List[int]:
    """
    Computes the prime factors of an integer.

    Args:
        n (int): The integer to factorize.

    Returns:
        List[int]: A list of prime factors in ascending order.
        
    Example:
        >>> prime_factorization(12)
        [2, 2, 3]
    """
    factors = []
    if n < 1:
        return []
    temp_n = n
    # Handle 2s
    while temp_n % 2 == 0:
        factors.append(2)
        temp_n //= 2
    # Handle odd factors
    for i in range(3, int(math.sqrt(temp_n)) + 1, 2):
        while temp_n % i == 0:
            factors.append(i)
            temp_n //= i
    if temp_n > 2:
        factors.append(temp_n)
    return factors

def is_perfect_number(n: int) -> bool:
    """
    Checks if a number is a perfect number (sum of proper divisors equals n).

    Args:
        n (int): The integer to check.

    Returns:
        bool: True if n is a perfect number, False otherwise.
        
    Example:
        >>> is_perfect_number(28)
        True
    """
    if n <= 1:
        return False
    sum_divisors = 1
    # Check divisors up to sqrt(n)
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            sum_divisors += i
            if i * i != n:
                sum_divisors += n // i
    return sum_divisors == n

def sieve_of_eratosthenes(limit: int) -> List[int]:
    """
    Generates all prime numbers up to a specified limit.

    Args:
        limit (int): The upper bound (inclusive) for the prime search.

    Returns:
        List[int]: A list of all prime numbers found.
    """
    if limit < 2:
        return []
    
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    
    for start in range(2, int(math.sqrt(limit)) + 1):
        if sieve[start]:
            for i in range(start * start, limit + 1, start):
                sieve[i] = False
                
    return [num for num, is_p in enumerate(sieve) if is_p]

def lcm(a: int, b: int) -> int:
    """
    Calculates the Least Common Multiple of two integers.

    Args:
        a (int): First integer.
        b (int): Second integer.

    Returns:
        int: The LCM of a and b.
    """
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)

def is_coprime(a: int, b: int) -> bool:
    """
    Checks if two numbers are coprime (their GCD is 1).

    Args:
        a (int): First integer.
        b (int): Second integer.

    Returns:
        bool: True if a and b are coprime, False otherwise.
    """
    return math.gcd(a, b) == 1

def euler_totient(n: int) -> int:
    """
    Calculates Euler's Totient function Phi(n).
    
    Args:
        n (int): A positive integer.

    Returns:
        int: The count of numbers <= n that are coprime to n.
        
    Raises:
        ValueError: If n is not a positive integer.
    """
    if n <= 0:
         raise ValueError("n must be a positive integer")
    result = n
    p = 2
    temp_n = n
    while p * p <= temp_n:
        if temp_n % p == 0:
            while temp_n % p == 0:
                temp_n //= p
            result -= result // p
        p += 1
    if temp_n > 1:
        result -= result // temp_n
    return result

def is_sophie_germain_prime(n: int) -> bool:
    """
    Checks if n is a Sophie Germain prime.
    A prime p is Sophie Germain if 2p + 1 is also prime.

    Args:
        n (int): The integer to check.

    Returns:
        bool: True if n is a Sophie Germain prime.
    """
    return is_prime(n) and is_prime(2 * n + 1)

def is_twin_prime(n: int) -> bool:
    """
    Checks if n is part of a twin prime pair.

    Args:
        n (int): The integer to check.

    Returns:
        bool: True if n is prime and either n-2 or n+2 is also prime.
    """
    if not is_prime(n):
        return False
    return is_prime(n - 2) or is_prime(n + 2)

def mobius_function(n: int) -> int:
    """
    Calculates the Mobius function mu(n).

    Args:
        n (int): A positive integer.

    Returns:
        int: 1 if n is square-free with an even number of prime factors.
             -1 if n is square-free with an odd number of prime factors.
             0 if n has a squared prime factor.
    """
    if n == 1:
        return 1
    
    temp_n = n
    prime_factors_count = 0
    
    # Check 2
    if temp_n % 2 == 0:
        temp_n //= 2
        prime_factors_count += 1
        if temp_n % 2 == 0:
            return 0
            
    # Check odd numbers
    i = 3
    while i * i <= temp_n:
        if temp_n % i == 0:
            temp_n //= i
            prime_factors_count += 1
            if temp_n % i == 0:
                return 0
        i += 2
        
    if temp_n > 1:
        prime_factors_count += 1
        
    return -1 if prime_factors_count % 2 == 1 else 1

def goldbach_partition(n: int) -> Optional[Tuple[int, int]]:
    """
    Finds a Goldbach partition for an even integer n > 2.

    Args:
        n (int): An even integer greater than 2.

    Returns:
        Optional[Tuple[int, int]]: A tuple of two primes that sum to n, 
                                   or None if no such partition is found.
                                   
    Raises:
        ValueError: If n is not an even integer greater than 2.
    """
    if n <= 2 or n % 2 != 0:
         raise ValueError("n must be an even integer greater than 2")
    
    primes = sieve_of_eratosthenes(n)
    prime_set = set(primes)
    
    for p in primes:
        if (n - p) in prime_set:
            return (p, n - p)
    return None

def prime_pi(n: int) -> int:
    """
    Calculates the prime-counting function pi(n).

    Args:
        n (int): The upper bound.

    Returns:
        int: The number of prime numbers less than or equal to n.
    """
    if n < 2:
        return 0
    return len(sieve_of_eratosthenes(n))

def is_semiprime(n: int) -> bool:
    """
    Checks if n is a semiprime (product of exactly two prime numbers).

    Args:
        n (int): The integer to check.

    Returns:
        bool: True if n is a semiprime.
    """
    if n <= 3:
        return False
        
    factors = prime_factorization(n)
    return len(factors) == 2

def is_mersenne_prime(n: int) -> bool:
    """
    Checks if n is a Mersenne prime (a prime of the form 2^p - 1).

    Args:
        n (int): The integer to check.

    Returns:
        bool: True if n is a Mersenne prime.
    """
    if not is_prime(n):
        return False
    
    x = n + 1
    return (x > 0) and ((x & (x - 1)) == 0)

def is_chen_prime(n: int) -> bool:
    """
    Checks if n is a Chen prime (p is prime and p+2 is prime or semiprime).

    Args:
        n (int): The integer to check.

    Returns:
        bool: True if n is a Chen prime.
    """
    if not is_prime(n):
        return False
    
    target = n + 2
    if is_prime(target):
        return True
    return is_semiprime(target)

def next_prime(n: int) -> int:
    """
    Finds the smallest prime number strictly greater than n.

    Args:
        n (int): The starting integer.

    Returns:
        int: The next prime number.
    """
    if n < 2:
        return 2
    
    candidate = n + 1
    if candidate > 2 and candidate % 2 == 0:
        candidate += 1
        
    while True:
        if is_prime(candidate):
            return candidate
        candidate += 2

def prev_prime(n: int) -> Optional[int]:
    """
    Finds the largest prime number strictly less than n.

    Args:
        n (int): The starting integer.

    Returns:
        Optional[int]: The previous prime number, or None if n <= 2.
    """
    if n <= 2:
        return None
        
    candidate = n - 1
    if candidate > 2 and candidate % 2 == 0:
        candidate -= 1
        
    while candidate >= 2:
        if is_prime(candidate):
            return candidate
        candidate -= 2
    return None

def is_fermat_prime(n: int) -> bool:
    """
    Checks if n is a Fermat prime (prime of the form 2^(2^k) + 1).

    Args:
        n (int): The integer to check.

    Returns:
        bool: True if n is a Fermat prime.
    """
    if not is_prime(n):
        return False
    
    x = n - 1
    if x <= 0 or (x & (x - 1)) != 0:
        return False
    
    m = x.bit_length() - 1
    if m == 0: return True # n=3, k=0
    return (m & (m - 1)) == 0