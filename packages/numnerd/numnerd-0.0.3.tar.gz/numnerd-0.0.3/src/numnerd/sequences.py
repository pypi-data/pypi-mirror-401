import math
import decimal
from typing import List, Tuple

def fibonacci(n: int) -> int:
    """
    Returns the n-th Fibonacci number using an iterative approach.

    Args:
        n (int): The index of the Fibonacci sequence (non-negative).

    Returns:
        int: The n-th Fibonacci number.

    Example:
        >>> fibonacci(10)
        55
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 0
    if n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def lucas_number(n: int) -> int:
    """
    Returns the n-th Lucas number.
    Lucas sequence starts with L(0)=2, L(1)=1 and follows L(n) = L(n-1) + L(n-2).

    Args:
        n (int): The index of the sequence (non-negative).

    Returns:
        int: The n-th Lucas number.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 2
    if n == 1:
        return 1
    a, b = 2, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def catalan_number(n: int) -> int:
    """
    Returns the n-th Catalan number using the factorial formula.

    Args:
        n (int): The index of the sequence (non-negative).

    Returns:
        int: The n-th Catalan number.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    return math.factorial(2 * n) // (math.factorial(n + 1) * math.factorial(n))

def triangular_number(n: int) -> int:
    """
    Returns the n-th Triangular number (sum of integers from 1 to n).

    Args:
        n (int): The index of the sequence (non-negative).

    Returns:
        int: The n-th triangular number.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    return n * (n + 1) // 2

def look_and_say(n: int) -> str:
    """
    Returns the n-th term of the Look-and-Say sequence as a string.
    Term 1 is "1", Term 2 is "11", etc.

    Args:
        n (int): The term index (positive).

    Returns:
        str: The n-th term string.
    """
    if n <= 0:
        raise ValueError("n must be a positive integer")
    if n == 1:
        return "1"
    
    current = "1"
    for _ in range(n - 1):
        next_val = []
        i = 0
        while i < len(current):
            count = 1
            while i + 1 < len(current) and current[i] == current[i+1]:
                i += 1
                count += 1
            next_val.append(str(count))
            next_val.append(current[i])
            i += 1
        current = "".join(next_val)
    return current

def lazy_caterer(n: int) -> int:
    """
    Returns the maximum number of pieces a circle can be cut into with n straight cuts.

    Args:
        n (int): Number of cuts (non-negative).

    Returns:
        int: Max pieces count.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    return (n**2 + n + 2) // 2

def pell_number(n: int) -> int:
    """
    Returns the n-th Pell number.
    Recurrence: P(n) = 2*P(n-1) + P(n-2), starting with 0, 1.

    Args:
        n (int): Index (non-negative).

    Returns:
        int: The n-th Pell number.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 0
    if n == 1:
        return 1
    p0, p1 = 0, 1
    for _ in range(2, n + 1):
        p0, p1 = p1, 2 * p1 + p0
    return p1

def thue_morse_iteration(n: int) -> str:
    """
    Returns the sequence after n iterations of the Thue-Morse pattern construction.

    Args:
        n (int): Iteration count (non-negative).

    Returns:
        str: The generated binary string.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    s = "0"
    for _ in range(n):
        inverse = "".join("1" if c == "0" else "0" for c in s)
        s += inverse
    return s

def recaman_sequence(n: int) -> List[int]:
    """
    Generates the first n terms of Recaman's sequence.

    Args:
        n (int): Number of terms (positive).

    Returns:
        List[int]: List containing the sequence terms.
    """
    if n <= 0:
        raise ValueError("n must be a positive integer")
    
    sequence = [0]
    seen = {0}
    current = 0
    
    for i in range(1, n):
        back = current - i
        if back > 0 and back not in seen:
            current = back
        else:
            current = current + i
        sequence.append(current)
        seen.add(current)
        
    return sequence

def padovan_sequence(n: int) -> int:
    """
    Returns the n-th Padovan number.
    Recurrence: P(n) = P(n-2) + P(n-3), starting 1, 1, 1.

    Args:
        n (int): Index (non-negative).

    Returns:
        int: The n-th Padovan number.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 2:
        return 1
    
    p0, p1, p2 = 1, 1, 1
    for _ in range(3, n + 1):
        p_next = p0 + p1
        p0, p1, p2 = p1, p2, p_next
    return p2

def sylvester_sequence(n: int) -> int:
    """
    Returns the n-th term of Sylvester's sequence.

    Args:
        n (int): Index (non-negative).

    Returns:
        int: The n-th term.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 2
    
    current = 2
    for _ in range(n):
        current = current * current - current + 1
    return current

def bell_number(n: int) -> int:
    """
    Returns the n-th Bell number (number of ways to partition a set of n items).

    Args:
        n (int): Set size (non-negative).

    Returns:
        int: n-th Bell number.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 1
    
    triangle = [[1]]
    for i in range(1, n + 1):
        prev_row = triangle[-1]
        new_row = [prev_row[-1]]
        for j in range(i):
            new_row.append(new_row[-1] + prev_row[j])
        triangle.append(new_row)
        
    return triangle[n][0]

def motzkin_number(n: int) -> int:
    """
    Returns the n-th Motzkin number.

    Args:
        n (int): Index (non-negative).

    Returns:
        int: n-th Motzkin number.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return 1
    
    m = [1, 1]
    for i in range(2, n + 1):
        val = ((2 * i + 1) * m[i - 1] + (3 * i - 3) * m[i - 2]) // (i + 2)
        m.append(val)
    return m[n]

def juggler_sequence(n: int) -> List[int]:
    """
    Returns the Juggler sequence starting with n.

    Args:
        n (int): Starting positive integer.

    Returns:
        List[int]: The Juggler sequence terms until 1.
    """
    if n <= 0:
        raise ValueError("n must be a positive integer")
    
    seq = [n]
    while n != 1:
        if n % 2 == 0:
            n = int(math.floor(math.sqrt(n)))
        else:
            n = int(math.floor(n * math.sqrt(n)))
        seq.append(n)
    return seq

def golomb_sequence(n: int) -> List[int]:
    """
    Returns the first n terms of Golomb's self-describing sequence.

    Args:
        n (int): Number of terms (positive).

    Returns:
        List[int]: First n terms.
    """
    if n <= 0:
        raise ValueError("n must be a positive integer")
    if n == 1:
        return [1]
    
    g = [0, 1]
    for i in range(2, n + 1):
        val = 1 + g[i - g[g[i-1]]]
        g.append(val)
        
    return g[1:]

def perrin_number(n: int) -> int:
    """
    Returns the n-th Perrin number.
    Recurrence: P(n) = P(n-2) + P(n-3), starting with 3, 0, 2.

    Args:
        n (int): Index (non-negative).

    Returns:
        int: n-th Perrin number.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0: return 3
    if n == 1: return 0
    if n == 2: return 2
    
    p0, p1, p2 = 3, 0, 2
    for _ in range(3, n + 1):
        p_next = p0 + p1
        p0, p1, p2 = p1, p2, p_next
    return p2

def narayana_cows(n: int) -> int:
    """
    Returns the n-th term of Narayana's cows sequence.
    Recurrence: C(n) = C(n-1) + C(n-3), starting 1, 1, 1.

    Args:
        n (int): Index (non-negative).

    Returns:
        int: n-th term.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 2:
        return 1
    
    c0, c1, c2 = 1, 1, 1
    for _ in range(3, n + 1):
        c_next = c2 + c0
        c0, c1, c2 = c1, c2, c_next
    return c2

def hofstadter_q(n: int) -> List[int]:
    """
    Returns the first n terms of the Hofstadter Q-sequence.

    Args:
        n (int): Term count (positive).

    Returns:
        List[int]: First n terms.
    """
    if n <= 0:
        raise ValueError("n must be a positive integer")
    if n == 1:
        return [1]
    
    q = [0, 1, 1]
    for i in range(3, n + 1):
        val = q[i - q[i-1]] + q[i - q[i-2]]
        q.append(val)
        
    return q[1:]

def wythoff_sequences(n: int) -> Tuple[int, int]:
    """
    Returns the n-th terms of both the Lower and Upper Wythoff sequences.

    Args:
        n (int): Index (non-negative).

    Returns:
        Tuple[int, int]: (Lower term, Upper term).
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    
    decimal.getcontext().prec = 50
    phi = (decimal.Decimal(1) + decimal.Decimal(5).sqrt()) / decimal.Decimal(2)
    
    lower = int(math.floor(decimal.Decimal(n) * phi))
    upper = int(math.floor(decimal.Decimal(n) * phi**2))
    
    return (lower, upper)

def van_eck_sequence(n: int) -> List[int]:
    """
    Generates the first n terms of the Van Eck sequence.

    Args:
        n (int): Number of terms (non-negative).

    Returns:
        List[int]: Sequence list.
    """
    if n <= 0:
        return []
    
    sequence = [0]
    last_seen = {}
    
    for i in range(n - 1):
        current = sequence[i]
        if current in last_seen:
            sequence.append(i - last_seen[current])
        else:
            sequence.append(0)
        last_seen[current] = i
        
    return sequence

def collatz_path(n: int) -> List[int]:
    """
    Generates the Collatz sequence path for a positive integer n.

    Args:
        n (int): Starting positive integer.

    Returns:
        List[int]: Full Collatz path until 1.
    """
    if n <= 0:
        raise ValueError("n must be a positive integer")
    path = [n]
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        path.append(n)
    return path