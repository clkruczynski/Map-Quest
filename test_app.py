import unittest
from mapquest_parse_json_8 import register, login, validate_location, get_weather

class TestApp(unittest.TestCase):

    def test_duplicate_register(self):
        result = register("test_user", "password123")
        self.assertEqual(result, 'Registration successful!')

        result = register("test_user", "password456")
        self.assertEqual(result, 'Username already exists. Please choose another one.')

    def test_invalid_location(self):
        result = validate_location('')
        self.assertEqual(result, False)

        result = validate_location('New York')
        self.assertEqual(result, True)

    def test_login_failure(self):
        register("test_user", "password123")
        result = login("test_user", "wrongpassword")
        self.assertEqual(result, 'Invalid username or password.')

        result = login("test_user", "password123")
        self.assertEqual(result, 'Login successful! Welcome, test_user!')

    def test_route_and_weather(self):
        result = get_weather('London')
        self.assertIn('Weather at London', result)

        result = get_weather('InvalidLocation')
        self.assertIn('Unable to fetch weather', result)

    def test_weather_check(self):
        result = get_weather('Boston')
        self.assertIn('Weather at Boston', result)

        result = get_weather('InvalidLocation')
        self.assertIn('Unable to fetch weather', result)

if __name__ == '__main__':
    unittest.main()
