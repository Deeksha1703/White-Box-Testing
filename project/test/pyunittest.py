from app.calculator import *
import unittest
from unittest.mock import MagicMock
from datetime import date, datetime, time
from datetime import timedelta


class TestCalculator(unittest.TestCase):
    def test_cost(self):
        """ Testing Strategy:
            100 % Branch(Decision) coverage
            100 % Condition coverage
            100 % Line(Statement) coverage
        """
        # test case 1
        self.calculator = Calculator(
            "20/03/2020", "3800", "8:00", 82, 20, 80, "8")
        self.assertEqual(self.calculator.cost_calculation(
            self.calculator.start_time, self.calculator.start_date, 50, 100), 27.50)

        # test case 2
        self.calculator = Calculator(
            "12/06/2020", "3800", "19:00", 82, 20, 80, "7")
        self.assertEqual(self.calculator.cost_calculation(
            self.calculator.start_time, self.calculator.start_date, 50, 100), 8.25)

        # test case 3
        self.calculator = Calculator(
            "01/01/2020", "3800", "19:00", 82, 20, 80, "7")
        self.assertEqual(self.calculator.cost_calculation(
            self.calculator.start_time, self.calculator.start_date, 50, 100), 8.25)


    def test_time_calculation(self):
        """ Testing Strategy:
            100 % Line(Statement) coverage
            100 % Branch(Decision) coverage
            100 % Condition coverage
            Since the method doesn't have any conditions or loops, Branch(Decision) coverage
            and Condition coverage would automatically 100 %
        """
        # test case 1
        self.calculator = Calculator(
            "20/03/2020", "3800", "8:00", 82, 20, 80, "7")
        self.assertEqual(self.calculator.time_calculation(), 0.547)


    def test_get_duration(self):
        """ Testing Strategy:
            100 % Line(Statement) coverage
            100 % Branch(Decision) coverage
            100 % Condition coverage
            Since the method doesn't have any conditions or loops, Branch(Decision) coverage
            and Condition coverage would automatically 100 %
        """
        # test case 1
        self.calculator = Calculator(
            "20/03/2020", "3800", "8:00", 82, 20, 80, "7")
        self.assertEqual(self.calculator.get_duration(),
                         timedelta(seconds=1968))


    def test_is_holiday(self):
        """ Testing Strategy:
            100 % Branch coverage
            100 % Statement(Line) coverage
            100 % Condition coverage
        """
        # test case 1
        self.calculator = Calculator(
            "01/01/2020", "3800", "7:00", 82, 20, 80, "7")
        self.assertEqual(self.calculator.is_holiday(
            self.calculator.start_date), True)

        # test case 2
        self.calculator = Calculator(
            "28/02/2020", "3800", "7:00", 82, 20, 80, "7")
        self.assertEqual(self.calculator.is_holiday(
            self.calculator.start_date), False)


    def test_is_leap_year(self):
        """ Testing Strategy:
            100 % Branch coverage
            100 % Statement(Line) coverage
            100 % Condition coverage
        """
        # test case 1
        self.calculator = Calculator(
            "28/02/2012", "3800", "7:00", 82, 20, 80, "7")
        self.assertEqual(self.calculator.is_leap_year(
            self.calculator.start_year), True)

        # test case 2
        self.calculator = Calculator(
            "28/02/2021", "3800", "7:00", 82, 20, 80, "7")
        self.assertEqual(self.calculator.is_leap_year(
            self.calculator.start_year), False)


    def test_is_peak(self):
        """ Testing Strategy:
            100 % Branch coverage
            100 % Statement(Line) coverage
            100 % Condition coverage
        """
        # test case 1
        self.calculator = Calculator(
            "28/02/2020", "3800", "7:00", 82, 20, 80, "7")
        self.assertEqual(self.calculator.is_peak(
            self.calculator.start_time), True)

        # test case 2
        self.calculator = Calculator(
            "28/02/2020", "3800", "19:00", 82, 20, 80, "7")
        self.assertEqual(self.calculator.is_peak(
            self.calculator.start_time), False)


    def test_is_weekday(self):
        """ Testing Strategy:
            100 % Branch coverage
            100 % Statement(Line) coverage
            100 % Condition coverage
        """
        # test case 1
        self.calculator = Calculator(
            "30/07/2020", "3800", "7:00", 82, 20, 80, "7")
        self.assertEqual(self.calculator.is_weekday(
            self.calculator.start_date), True)

        # test case 2
        self.calculator = Calculator(
            "02/01/2021", "3800", "7:00", 82, 20, 80, "7")
        self.assertEqual(self.calculator.is_weekday(
            self.calculator.start_date), False)

    # Dummy data for testing requirement 2, 3, 4
    DATA = {
        "sunrise": "06:00:00",
        "sunset": "19:00:00",
        "sunHours": 8.6,
        "hourlyWeatherHistory": [
            {
                "cloudCoverPct": 50
            },
            {
                "cloudCoverPct": 50
            },
            {
                "cloudCoverPct": 50
            },
            {
                "cloudCoverPct": 50
            },
            {
                "cloudCoverPct": 50
            },
            {
                "cloudCoverPct": 50
            },
            {
                "cloudCoverPct": 50
            },
            {
                "cloudCoverPct": 50
            },
            {
                "cloudCoverPct": 50
            },
            {
                "cloudCoverPct": 50
            },
            {
                "cloudCoverPct": 50
            },
            {
                "cloudCoverPct": 50
            },
            {
                "cloudCoverPct": 50
            },
            {
                "cloudCoverPct": 50
            },
            {
                "cloudCoverPct": 50
            },
            {
                "cloudCoverPct": 50
            },
            {
                "cloudCoverPct": 50
            },
            {
                "cloudCoverPct": 50
            },
            {
                "cloudCoverPct": 50
            },
            {
                "cloudCoverPct": 50
            },
            {
                "cloudCoverPct": 50
            },
            {
                "cloudCoverPct": 50
            },
            {
                "cloudCoverPct": 50
            },
            {
                "cloudCoverPct": 50
            }
        ]
    }


    def test_req2(self):
        """ Testing Strategy:
            100 % Branch coverage
            100 % Statement(Line) coverage
            100 % Condition coverage
        """
        # test case 1 
        self.calculator = Calculator("20/03/2020", "3800", "8:00", 82, 20, 80, "8")
        self.calculator.search_weather = MagicMock(return_value=self.DATA)
        self.assertEqual(self.calculator.calculate_solar_energy_req2(), 26.55)

        # test case 2
        self.calculator = Calculator("20/03/2020", "3800", "8:00", 82, 20, 80, "2")
        self.assertEqual(self.calculator.calculate_solar_energy_req2(), 1.1)

        # test case 3
        self.calculator = Calculator("20/03/2020", "3800", "4:00", 82, 20, 80, "2")
        self.assertEqual(self.calculator.calculate_solar_energy_req2(), 1.03)

        # test case 4
        self.calculator = Calculator("20/03/2020", "3800", "20:00", 82, 20, 80, "3")
        self.assertEqual(self.calculator.calculate_solar_energy_req2(), 2.71)

        # test case 5
        self.calculator = Calculator("20/03/2020", "3800", "20:00", 82, 20, 80, "2")
        self.assertEqual(self.calculator.calculate_solar_energy_req2(), 1.8)

   
    def test_req3(self):
        """ Testing Strategy:
            100 % Branch coverage
            100 % Statement(Line) coverage
            100 % Condition coverage
        """
        # test case 1 
        self.calculator = Calculator("20/03/2020", "3800", "8:00", 82, 70, 80, "8")
        self.calculator.search_weather = MagicMock(return_value=self.DATA)
        self.assertEqual(self.calculator.calculate_solar_energy_req3_aux(), 4.47)
        
        # test case 2
        self.calculator = Calculator("20/03/2020", "3800", "5:30", 100, 20, 100, "7")
        self.assertEqual(self.calculator.calculate_solar_energy_req3_aux(), 13.61)
        
        # test case 3
        self.calculator = Calculator("20/03/2020", "3800", "21:00", 80, 20, 100, "7")
        self.assertEqual(self.calculator.calculate_solar_energy_req3_aux(), 10.56)
        
        # test case 4
        self.calculator = Calculator("1/10/2021", "3800", "21:00", 80, 20, 100, "7")
        self.assertEqual(self.calculator.calculate_solar_energy_req3_aux(), 10.56)
        
        # test case 5
        self.calculator = Calculator("20/3/2022", "3800", "21:00", 80, 20, 100, "7")
        self.assertEqual(self.calculator.calculate_solar_energy_req3_aux(), 10.24)
        
    def test_req4(self):
        """ Testing Strategy:
            100 % Branch coverage
            100 % Statement(Line) coverage
            100 % Condition coverage
        """
        # test case 1
        self.calculator = Calculator("20/03/2020", "3800", "8:00", 82, 20, 80, "8")
        self.calculator.search_weather = MagicMock(return_value=self.DATA)
        self.assertEqual(self.calculator.calculate_solar_energy_req4(), 'yearly energy: 15695.0, monthly energy: 1290.0')
        
    if __name__ == "__main__":
        pass
