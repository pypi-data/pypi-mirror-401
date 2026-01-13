from numnerd.recreational import (
    is_armstrong_number, is_happy_number, kaprekar_routine, digital_root,
    is_vampire_number, is_munchausen_number, is_spy_number, is_neon_number,
    is_harshad_number, is_automorphic_number, is_pronic_number, is_smith_number,
    is_disarium_number, is_keith_number, is_abundant_number, is_deficient_number,
    is_kaprekar_number, is_polydivisible_number
)

def test_is_armstrong_number():
    assert is_armstrong_number(153) is True
    assert is_armstrong_number(370) is True
    assert is_armstrong_number(9474) is True
    assert is_armstrong_number(9) is True
    assert is_armstrong_number(10) is False

def test_is_happy_number():
    assert is_happy_number(19) is True
    assert is_happy_number(7) is True
    assert is_happy_number(2) is False
    assert is_happy_number(4) is False

def test_kaprekar_routine():
    assert kaprekar_routine(6174) == 0
    # 3524 -> 5432 - 2345 = 3087 -> 8730 - 0378 = 8352 -> 8532 - 2358 = 6174 (3 steps)
    assert kaprekar_routine(3524) == 3 
    assert kaprekar_routine(1111) == -1

def test_digital_root():
    assert digital_root(16) == 7 # 1+6
    assert digital_root(942) == 6 # 9+4+2=15 -> 1+5=6
    assert digital_root(0) == 0
    assert digital_root(9) == 9

def test_is_disarium_number():
    assert is_disarium_number(89) is True # 8^1 + 9^2 = 8 + 81 = 89
    assert is_disarium_number(135) is True # 1^1 + 3^2 + 5^3 = 1 + 9 + 125 = 135
    assert is_disarium_number(175) is True
    assert is_disarium_number(80) is False

def test_is_keith_number():
    assert is_keith_number(14) is True # 1, 4 -> 5, 9, 14
    assert is_keith_number(19) is True # 1, 9 -> 10, 19
    assert is_keith_number(197) is True # As explained
    assert is_keith_number(10) is False # 1, 0 -> 1, 1, 2, ...
    assert is_keith_number(5) is False

def test_is_abundant_number():
    assert is_abundant_number(12) is True # 1+2+3+4+6=16 > 12
    assert is_abundant_number(18) is True
    assert is_abundant_number(6) is False # Perfect (==)
    assert is_abundant_number(10) is False # Deficient (<)

def test_is_deficient_number():
    assert is_deficient_number(10) is True # 1+2+5=8 < 10
    assert is_deficient_number(13) is True # Prime -> 1 < 13
    assert is_deficient_number(6) is False # Perfect
    assert is_deficient_number(12) is False # Abundant

def test_is_kaprekar_number():
    assert is_kaprekar_number(9) is True # 81 -> 8+1=9
    assert is_kaprekar_number(45) is True # 2025 -> 20+25=45
    assert is_kaprekar_number(297) is True # 88209 -> 88+209=297
    assert is_kaprekar_number(10) is False

def test_is_polydivisible_number():
    assert is_polydivisible_number(381654729) is True
    assert is_polydivisible_number(102) is True # 1/1, 10/2, 102/3
    assert is_polydivisible_number(103) is False

def test_is_harshad_number():
    assert is_harshad_number(18) is True # 1+8=9, 18%9==0
    assert is_harshad_number(19) is False # 1+9=10, 19%10!=0
    assert is_harshad_number(21) is True # 2+1=3, 21%3==0

def test_is_automorphic_number():
    assert is_automorphic_number(5) is True # 25
    assert is_automorphic_number(6) is True # 36
    assert is_automorphic_number(25) is True # 625
    assert is_automorphic_number(76) is True # 5776
    assert is_automorphic_number(7) is False # 49

def test_is_pronic_number():
    assert is_pronic_number(12) is True # 3*4
    assert is_pronic_number(42) is True # 6*7
    assert is_pronic_number(20) is True # 4*5
    assert is_pronic_number(13) is False
    assert is_pronic_number(0) is True # 0*1

def test_is_smith_number():
    assert is_smith_number(22) is True # 2+2=4. Factors 2,11 -> 2+1+1=4.
    assert is_smith_number(4) is True # 4. Factors 2,2 -> 2+2=4.
    assert is_smith_number(378) is True 
    # 378 = 2 * 3^3 * 7 = 2,3,3,3,7
    # Digits: 3+7+8 = 18
    # Factors: 2 + 3+3+3 + 7 = 18
    assert is_smith_number(13) is False # Prime
    assert is_smith_number(21) is False # 2+1=3. Factors 3,7 -> 3+7=10.

def test_is_vampire_number():
    assert is_vampire_number(1260) is True  # 21 * 60
    assert is_vampire_number(1395) is True  # 15 * 93
    assert is_vampire_number(1261) is False
    assert is_vampire_number(100) is False  # Odd digits (len 3)
    # 12600 = 210 * 60? No, both end in 0. But 12600 = 120 * 105?
    # Actually 12600 is a vampire number because 12600 = 600 * 21 (Wait, no trailing zeros allowed on BOTH).
    # 12600 = 120 * 105 (Contains 1,2,0,1,0,5 -> 001125 vs 12600. No.)
    # Let's stick to the classic examples.

def test_is_munchausen_number():
    assert is_munchausen_number(1) is True # 1^1 = 1
    assert is_munchausen_number(3435) is True # 3^3 + 4^4 + 3^3 + 5^5 = 3435
    assert is_munchausen_number(10) is False

def test_is_spy_number():
    assert is_spy_number(1124) is True # 1+1+2+4=8, 1*1*2*4=8
    assert is_spy_number(22) is True   # 2+2=4, 2*2=4
    assert is_spy_number(123) is True  # 1+2+3=6, 1*2*3=6
    assert is_spy_number(10) is False

def test_is_neon_number():
    assert is_neon_number(9) is True   # 9^2=81 -> 8+1=9
    assert is_neon_number(1) is True   # 1^1=1 -> 1
    assert is_neon_number(0) is True   # 0
    assert is_neon_number(12) is False # 144 -> 9 != 12
