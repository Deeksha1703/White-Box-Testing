from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField
from wtforms.validators import DataRequired, ValidationError, Optional
from datetime import date, datetime, time, timedelta

# validation for form inputs
class Calculator_Form(FlaskForm):
    # this variable name needs to match with the input attribute name in the html file
    # you are NOT ALLOWED to change the field type, however, you can add more built-in validators and custom messages
    BatteryPackCapacity = StringField("Battery Pack Capacity", [DataRequired()])
    InitialCharge = StringField("Initial Charge", [DataRequired()])
    FinalCharge = StringField("Final Charge", [DataRequired()])
    StartDate = DateField("Start Date", [DataRequired("Data is missing or format is incorrect")], format='%d/%m/%Y')
    StartTime = TimeField("Start Time", [DataRequired("Data is missing or format is incorrect")], format='%H:%M')
    ChargerConfiguration = StringField("Charger Configuration", [DataRequired()])
    PostCode = StringField("Post Code", [DataRequired()])

    # use validate_ + field_name to activate the flask-wtforms built-in validator
    # this is an example for you
    def validate_BatteryPackCapacity(self, field):
        """
        Method that checks if the battery pack capacity is valid
        """
        if field.data is None:
            raise ValidationError('Field data is none')
        elif field.data == '':
            raise ValueError("cannot fetch data")
        elif int(field.data) <=0:
            raise ValueError("Cannot be less than or equal to 0")


    # validate initial charge here
    def validate_InitialCharge(self, field):
        """
        Method that checks if the initial charge is valid
        """
        # another example of how to compare initial charge with final charge
        # you may modify this part of the code
        if field.data is None:
            raise ValidationError('Field data is none')
        if int(field.data) > 100 or int(field.data) < 0:
            raise ValueError("Initial charge data error")


    # validate final charge here
    def validate_FinalCharge(self, field):
        """
        Method that checks if the final charge is valid
        """
        if field.data is None:
            raise ValidationError('Field data is none')
        if int(field.data) > 100 or int(field.data) < 0:
            raise ValueError("Final charge data error")


    # validate start date here
    def validate_StartDate(self, field):
        """
        Method that checks if the start date is valid
        """
        if field.data is None:
            raise ValidationError('Field data is none')
        early_date = datetime.strptime("01/07/2008", "%d/%m/%Y").date()
        late_date = datetime.strptime("27/09/2021", "%d/%m/%Y").date()
        if type(field.data) == str:
            start_date = datetime.strptime(field.data, "%d/%m/%Y").date()
        else:
            start_date = field.data
        if start_date < early_date or start_date > late_date:
            raise ValueError("Final charge data error")
        pass


    # validate start time here
    def validate_StartTime(self, field):
        """
        Method that checks if the start time is valid
        """
        if field.data is None or field.data == "":
            raise ValidationError("data cannot be empty")
        if (type(field.data)==str):
            try:
                datetime.strptime(field.data, "%H:%M")
            except:
                raise ValueError("Start time is not in HH:MM format")


    # validate charger configuration here
    def validate_ChargerConfiguration(self, field):
        """
        Method that checks if the charger configuration is valid
        """
        if field.data is None or field.data == "":
            raise ValidationError('Field data is none')
        if int(field.data) < 1 or int(field.data) > 8:
            raise ValueError('Charger configuration data error')
        pass


    # validate postcode here
    def validate_PostCode(self, field):
        """
        Method that checks if the post code is valid
        """
        if field.data is None or field.data == "":
            raise ValidationError('Field data is none')
        if len(field.data) < 4:
            raise ValueError('PostCode data error')
        pass
