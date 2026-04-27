import unittest

# Функции для теста (имитация логики валидации)
def validate_year(year):
    return year.isdigit()

def validate_rating(rating):
    try:
        r = float(rating)
        return 0 <= r <= 10
    except ValueError:
        return False

class TestMovieApp(unittest.TestCase):
    def test_year_is_digit(self):
        # Позитивный тест: год — число
        self.assertTrue(validate_year("2024"))
        # Негативный тест: год — буквы
        self.assertFalse(validate_year("две тысячи"))

    def test_rating_range(self):
        # Позитивный тест: рейтинг в границах
        self.assertTrue(validate_rating("8.5"))
        self.assertTrue(validate_rating("0"))
        self.assertTrue(validate_rating("10"))
        # Граничный/негативный случай: выше 10 или ниже 0
        self.assertFalse(validate_rating("11"))
        self.assertFalse(validate_rating("-1"))

if __name__ == '__main__':
    unittest.main()
