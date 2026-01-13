from numnerd.sequences import (
    fibonacci, collatz_path, lucas_number, catalan_number, triangular_number,
    look_and_say, lazy_caterer, pell_number, thue_morse_iteration,
    recaman_sequence, padovan_sequence, sylvester_sequence,
    bell_number, motzkin_number, juggler_sequence, golomb_sequence, perrin_number,
    narayana_cows, hofstadter_q, wythoff_sequences, van_eck_sequence
)

def test_fibonacci():
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(2) == 1
    assert fibonacci(3) == 2
    assert fibonacci(10) == 55

def test_lucas_number():
    assert lucas_number(0) == 2
    assert lucas_number(1) == 1
    assert lucas_number(2) == 3
    assert lucas_number(3) == 4
    assert lucas_number(5) == 11

def test_catalan_number():
    assert catalan_number(0) == 1
    assert catalan_number(1) == 1
    assert catalan_number(2) == 2
    assert catalan_number(3) == 5
    assert catalan_number(5) == 42

def test_triangular_number():
    assert triangular_number(1) == 1
    assert triangular_number(3) == 6
    assert triangular_number(4) == 10
    assert triangular_number(5) == 15
    assert triangular_number(0) == 0

def test_look_and_say():
    assert look_and_say(1) == "1"
    assert look_and_say(2) == "11"
    assert look_and_say(3) == "21"
    assert look_and_say(4) == "1211"
    assert look_and_say(5) == "111221"

def test_lazy_caterer():
    assert lazy_caterer(0) == 1
    assert lazy_caterer(1) == 2
    assert lazy_caterer(2) == 4
    assert lazy_caterer(3) == 7
    assert lazy_caterer(4) == 11

def test_pell_number():
    assert pell_number(0) == 0
    assert pell_number(1) == 1
    assert pell_number(2) == 2
    assert pell_number(3) == 5
    assert pell_number(4) == 12

def test_thue_morse_iteration():
    assert thue_morse_iteration(0) == "0"
    assert thue_morse_iteration(1) == "01"
    assert thue_morse_iteration(2) == "0110"
    assert thue_morse_iteration(3) == "01101001"

def test_recaman_sequence():
    assert recaman_sequence(1) == [0]
    assert recaman_sequence(5) == [0, 1, 3, 6, 2]
    assert recaman_sequence(10) == [0, 1, 3, 6, 2, 7, 13, 20, 12, 21]

def test_padovan_sequence():
    assert padovan_sequence(0) == 1
    assert padovan_sequence(1) == 1
    assert padovan_sequence(2) == 1
    assert padovan_sequence(3) == 2
    assert padovan_sequence(4) == 2
    assert padovan_sequence(5) == 3
    assert padovan_sequence(6) == 4
    assert padovan_sequence(7) == 5

def test_sylvester_sequence():
    assert sylvester_sequence(0) == 2
    assert sylvester_sequence(1) == 3
    assert sylvester_sequence(2) == 7
    assert sylvester_sequence(3) == 43
    assert sylvester_sequence(4) == 1807

def test_bell_number():
    assert bell_number(0) == 1
    assert bell_number(1) == 1
    assert bell_number(2) == 2
    assert bell_number(3) == 5
    assert bell_number(4) == 15
    assert bell_number(5) == 52

def test_motzkin_number():
    assert motzkin_number(0) == 1
    assert motzkin_number(1) == 1
    assert motzkin_number(2) == 2
    assert motzkin_number(3) == 4
    assert motzkin_number(4) == 9
    assert motzkin_number(5) == 21

def test_juggler_sequence():
    assert juggler_sequence(3) == [3, 5, 11, 36, 6, 2, 1]
    assert juggler_sequence(2) == [2, 1]
    assert juggler_sequence(9) == [9, 27, 140, 11, 36, 6, 2, 1]

def test_golomb_sequence():
    assert golomb_sequence(1) == [1]
    assert golomb_sequence(5) == [1, 2, 2, 3, 3]
    assert golomb_sequence(10) == [1, 2, 2, 3, 3, 4, 4, 4, 5, 5]

def test_perrin_number():
    assert perrin_number(0) == 3
    assert perrin_number(1) == 0
    assert perrin_number(2) == 2
    assert perrin_number(3) == 3
    assert perrin_number(4) == 2
    assert perrin_number(5) == 5
    assert perrin_number(6) == 5
    assert perrin_number(7) == 7

def test_narayana_cows():
    assert narayana_cows(0) == 1
    assert narayana_cows(1) == 1
    assert narayana_cows(2) == 1
    assert narayana_cows(3) == 2
    assert narayana_cows(4) == 3
    assert narayana_cows(5) == 4
    assert narayana_cows(6) == 6

def test_hofstadter_q():
    assert hofstadter_q(5) == [1, 1, 2, 3, 3]
    assert hofstadter_q(10) == [1, 1, 2, 3, 3, 4, 5, 5, 6, 6]

def test_wythoff_sequences():
    assert wythoff_sequences(1) == (1, 2)
    assert wythoff_sequences(2) == (3, 5)
    assert wythoff_sequences(3) == (4, 7)

def test_van_eck_sequence():
    assert van_eck_sequence(5) == [0, 0, 1, 0, 2]
    assert van_eck_sequence(10) == [0, 0, 1, 0, 2, 0, 2, 2, 1, 6]

def test_collatz_path():
    assert collatz_path(1) == [1]
    assert collatz_path(6) == [6, 3, 10, 5, 16, 8, 4, 2, 1]
    assert collatz_path(13) == [13, 40, 20, 10, 5, 16, 8, 4, 2, 1]
