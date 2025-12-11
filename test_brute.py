import unittest
import pytest
from brute import Brute

class TestBruteOnce(unittest.TestCase):
    def test_it_guesses_correctly(self):
        b = Brute("CorrectGuess")
        self.assertTrue(b.bruteOnce("CorrectGuess"))
    def test_it_guesses_incorrectly(self):
        b = Brute("CaseSensitiveCheck")
        self.assertFalse(b.bruteOnce("casesensitivecheck"))
        self.assertFalse(b.bruteOnce("CaseSensitivecheck"))
        self.assertFalse(b.bruteOnce("IncorrectGuess"))
        self.assertFalse(b.bruteOnce(""))
    def test_it_errors_on_non_strings(self):
        b = Brute("0")
        self.assertRaises(TypeError, lambda: b.bruteOnce(None))
        self.assertRaises(TypeError, lambda: b.bruteOnce(0))
        self.assertRaises(TypeError, lambda: b.bruteOnce(0.0))
        self.assertRaises(TypeError, lambda: b.bruteOnce(b"This is a string, right? There's quotes!"))
        self.assertRaises(TypeError, lambda: b.bruteOnce(0b00110011))
        self.assertRaises(TypeError, lambda: b.bruteOnce(True))
    def test_it_guesses_long_strings_correctly(self):
        b = Brute("VERY LONG GUESS"*500)
        self.assertTrue(b.bruteOnce("VERY LONG GUESS"*500))
    def test_it_guesses_long_strings_incorrectly(self):
        b = Brute("GUESS"*500)
        self.assertFalse(b.bruteOnce("GUESS"*499))
        self.assertFalse(b.bruteOnce("GUESS"*501))
        self.assertFalse(b.bruteOnce("guess"*500))
        self.assertFalse(b.bruteOnce("GUESs"*500))

@pytest.fixture
def hash_static(mocker):
    return mocker.patch.object(Brute, 'hash', return_value="Hash will always return this")

@pytest.fixture
def random_guess_correct(mocker):
    return mocker.patch.object(Brute, 'randomGuess', return_value="CorrectGuess")

@pytest.fixture
def random_guess_incorrect(mocker):
    return mocker.patch.object(Brute, 'randomGuess', return_value="IncorrectGuess")

@pytest.fixture
def guess(mocker) -> Brute:
    return Brute("CorrectGuess")

@pytest.fixture
def brute_once_incorrect(mocker):
    return mocker.patch.object(Brute, 'bruteOnce', return_value=False)

def describe_BruteMany():
    def it_guesses_correctly(guess: Brute, random_guess_correct):
        assert guess.bruteMany() >= 0
        random_guess_correct.assert_called()
    def it_guesses_incorrectly(guess: Brute, random_guess_incorrect, brute_once_incorrect):
        assert guess.bruteMany(limit=1000) == -1
        brute_once_incorrect.assert_called_with("IncorrectGuess")
        random_guess_incorrect.assert_called()
    def it_obeys_the_limit_at_one(guess: Brute, random_guess_incorrect):
        assert guess.bruteMany(limit=1) == -1
        random_guess_incorrect.assert_called_once()
    def it_obeys_the_limit_at_zero(guess: Brute, random_guess_correct):
        assert guess.bruteMany(limit=0) == -1 # It should still return -1 despite the guess being correct
        random_guess_correct.assert_not_called()
