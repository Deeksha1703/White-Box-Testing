import unittest
from unittest.mock import Mock
from app.calculator_form import *
from flask import Flask


class TestCalculatorForm(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.mocked_field = Mock()

        with self.app.app_context():
            self.calculator_form = Calculator_Form()


    def test_validate_BatteryPackCapacity(self):
            self.mocked_field.data = None
            with self.assertRaises(ValidationError):
                self.calculator_form.validate_BatteryPackCapacity(self.mocked_field)
            self.mocked_field.data = ""
            with self.assertRaises(ValueError):
                self.calculator_form.validate_BatteryPackCapacity(self.mocked_field)
            self.mocked_field.data = "-2"
            with self.assertRaises(ValueError):
                self.calculator_form.validate_BatteryPackCapacity(self.mocked_field)


    def test_validate_InitialCharge(self):
            self.mocked_field.data = None
            with self.assertRaises(ValidationError):
                self.calculator_form.validate_InitialCharge(self.mocked_field)
            self.mocked_field.data = "1000"
            with self.assertRaises(ValueError):
                self.calculator_form.validate_InitialCharge(self.mocked_field)
            self.mocked_field.data = "-99"
            with self.assertRaises(ValueError):
                self.calculator_form.validate_InitialCharge(self.mocked_field)


    def test_validate_FinalCharge(self):
            self.mocked_field.data = None
            with self.assertRaises(ValidationError):
                self.calculator_form.validate_FinalCharge(self.mocked_field)
            self.mocked_field.data = "1000"
            with self.assertRaises(ValueError):
                self.calculator_form.validate_FinalCharge(self.mocked_field)
            self.mocked_field.data = "-99"
            with self.assertRaises(ValueError):
                self.calculator_form.validate_FinalCharge(self.mocked_field)


    def test_validate_StartDate(self):
            self.mocked_field.data = None
            with self.assertRaises(ValidationError):
                self.calculator_form.validate_StartDate(self.mocked_field)
            self.mocked_field.data = "01/07/2007"
            with self.assertRaises(ValueError):
                self.calculator_form.validate_StartDate(self.mocked_field)
            self.mocked_field.data = "01/07/2022"
            with self.assertRaises(ValueError):
                self.calculator_form.validate_StartDate(self.mocked_field)


    def test_validate_StartTime(self):
            self.mocked_field.data = None
            with self.assertRaises(ValidationError):
                self.calculator_form.validate_StartTime(self.mocked_field)
            self.mocked_field.data = ""
            with self.assertRaises(ValidationError):
                self.calculator_form.validate_StartTime(self.mocked_field)
            self.mocked_field.data = "abc"
            with self.assertRaises(ValueError):
                self.calculator_form.validate_StartTime(self.mocked_field)


    def test_validate_ChargerConfiguration(self):
            self.mocked_field.data = None
            with self.assertRaises(ValidationError):
                self.calculator_form.validate_ChargerConfiguration(self.mocked_field)
            self.mocked_field.data = ""
            with self.assertRaises(ValidationError):
                self.calculator_form.validate_StartTime(self.mocked_field)
            self.mocked_field.data = "0"
            with self.assertRaises(ValueError):
                self.calculator_form.validate_StartTime(self.mocked_field)
            self.mocked_field.data = "10"
            with self.assertRaises(ValueError):
                self.calculator_form.validate_StartTime(self.mocked_field)


    def test_validate_PostCode(self):
            self.mocked_field.data = None
            with self.assertRaises(ValidationError):
                self.calculator_form.validate_PostCode(self.mocked_field)
            self.mocked_field.data = ""
            with self.assertRaises(ValidationError):
                self.calculator_form.validate_PostCode(self.mocked_field)
            self.mocked_field.data = "000"
            with self.assertRaises(ValueError):
                self.calculator_form.validate_PostCode(self.mocked_field)


    if __name__ == "__main__":
        pass
