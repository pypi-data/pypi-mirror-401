from numnerd.constants import (
    calculate_pi, calculate_e, calculate_golden_ratio, calculate_sqrt2,
    calculate_silver_ratio, calculate_plastic_number, calculate_catalan_constant,
    calculate_universal_parabolic_constant, calculate_aperys_constant, calculate_supergolden_ratio,
    calculate_gelfond_constant, calculate_omega_constant,
    calculate_ln2, calculate_levy_constant, calculate_reciprocal_fibonacci_constant,
    calculate_gauss_constant
)

def test_calculate_pi():
    # Pi approx: 3.1415926535
    assert calculate_pi(2) == "3.14"
    assert calculate_pi(5) == "3.14159"
    assert calculate_pi(10) == "3.1415926535"

def test_calculate_e():
    # e approx: 2.7182818284
    assert calculate_e(2) == "2.71"
    assert calculate_e(5) == "2.71828"
    assert calculate_e(10) == "2.7182818284"

def test_calculate_golden_ratio():
    # phi approx: 1.6180339887
    assert calculate_golden_ratio(2) == "1.61"
    assert calculate_golden_ratio(5) == "1.61803"
    assert calculate_golden_ratio(10) == "1.6180339887"

def test_calculate_sqrt2():
    # sqrt(2) approx: 1.4142135623
    assert calculate_sqrt2(2) == "1.41"
    assert calculate_sqrt2(5) == "1.41421"
    assert calculate_sqrt2(10) == "1.4142135623"

def test_calculate_silver_ratio():
    # delta_S approx: 2.4142135623
    assert calculate_silver_ratio(2) == "2.41"
    assert calculate_silver_ratio(5) == "2.41421"
    assert calculate_silver_ratio(10) == "2.4142135623"

def test_calculate_plastic_number():
    # rho approx: 1.3247179572
    assert calculate_plastic_number(2) == "1.32"
    assert calculate_plastic_number(5) == "1.32471"

def test_calculate_catalan_constant():
    # G approx: 0.9159655941
    assert calculate_catalan_constant(2) == "0.91"
    assert calculate_catalan_constant(4) == "0.9159"

def test_calculate_universal_parabolic_constant():
    # P approx: 2.2955871494
    assert calculate_universal_parabolic_constant(2) == "2.29"
    assert calculate_universal_parabolic_constant(5) == "2.29558"

def test_calculate_aperys_constant():
    # Zeta(3) approx: 1.2020569031
    assert calculate_aperys_constant(2) == "1.20"
    assert calculate_aperys_constant(5) == "1.20205"

def test_calculate_supergolden_ratio():
    # psi approx: 1.4655712318
    assert calculate_supergolden_ratio(2) == "1.46"
    assert calculate_supergolden_ratio(5) == "1.46557"

def test_calculate_gelfond_constant():
    # e^pi approx: 23.1406926327
    assert calculate_gelfond_constant(2) == "23.14"
    assert calculate_gelfond_constant(5) == "23.14069"

def test_calculate_omega_constant():
    # omega approx: 0.5671432904
    assert calculate_omega_constant(2) == "0.56"
    assert calculate_omega_constant(5) == "0.56714"

def test_calculate_ln2():
    # ln(2) approx: 0.6931471805
    assert calculate_ln2(2) == "0.69"
    assert calculate_ln2(5) == "0.69314"
    assert calculate_ln2(10) == "0.6931471805"

def test_calculate_levy_constant():
    # L approx: 3.2758229187
    assert calculate_levy_constant(2) == "3.27"
    assert calculate_levy_constant(5) == "3.27582"

def test_calculate_reciprocal_fibonacci_constant():
    # psi approx: 3.3598856662
    assert calculate_reciprocal_fibonacci_constant(2) == "3.35"
    assert calculate_reciprocal_fibonacci_constant(5) == "3.35988"

def test_calculate_gauss_constant():
    # G approx: 0.8346268416
    assert calculate_gauss_constant(2) == "0.83"
    assert calculate_gauss_constant(5) == "0.83462"
