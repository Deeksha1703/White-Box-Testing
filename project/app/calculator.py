from urllib.request import urlopen
import json
import holidays
from datetime import date, datetime, time
from datetime import timedelta

class Calculator():
    # you can choose to initialise variables here, if needed.
    def __init__(self, start_date, postcode, start_time, battery_capacity, initial_charge, final_charge,
                 charger_configuration):
        """
        Constructor for the Calculator class to initialise all the variables
        """
        self.postcode = int(postcode)
        # self.start_date only includes the yyyy:mm:dd
        if type(start_date) == str:
            start_date = datetime.strptime(start_date, '%d/%m/%Y').date()
        self.start_date = start_date
        # self.start_year takes the year of the starting year
        self.start_year = self.start_date.year
        # self.start_time includes the starting date and time
        if type(start_time) == str:
            start_time = datetime.strptime(start_time, '%H:%M').time()
        self.start_time = start_time
        self.full_date = datetime.combine(start_date,start_time)
        self.battery_capacity = int(battery_capacity)
        self.inital_charge = int(initial_charge)
        self.final_charge = int(final_charge)

        if charger_configuration == "1":
            self.power = 2
            self.price = 0.05
        elif charger_configuration == "2":
            self.power = 3.6
            self.price = 0.075
        elif charger_configuration == "3":
            self.power = 7.2
            self.price = 0.1
        elif charger_configuration == "4":
            self.power = 11
            self.price = 0.125
        elif charger_configuration == "5":
            self.power = 22
            self.price = 0.15
        elif charger_configuration == "6":
            self.power = 36
            self.price = 0.2
        elif charger_configuration == "7":
            self.power = 90
            self.price = 0.3
        elif charger_configuration == "8":
            self.power = 350
            self.price = 0.5
        self.time = 0
        self.time_calculation()


    # you may add more parameters if needed, you may modify the formula also.
    # Change it to meet per hour/partial hour basis
    def cost_calculation(self, current_time, current_date, energy_generated, charging_energy):
        """
         Method that calculates the cost of charging the car
        :param: current_time: The current time
        :param: current_date: The current date
        :param: energy_generated: The solar energy generated
        :param: charging_energy: The energy charged in the car
        """
        if self.is_peak(current_time):
            base_price = 100
        else:
            base_price = 50

        if self.is_holiday(current_date) or self.is_weekday(current_date):
            surcharge_factor = 1.1
        else:
            surcharge_factor = 1

        cost = round(max(charging_energy - energy_generated,0)* (base_price / 100)* surcharge_factor * self.price,2)
        return cost


    # you may add more parameters if needed, you may also modify the formula.
    # returns the time in hours
    def time_calculation(self):
        """"
        The purpose of this method is to calculate the time needed to complete charging
        """
        self.time = (((self.final_charge - self.inital_charge) / 100) * self.battery_capacity) / self.power
        return round(self.time, 3)


    # you may create some new methods at your convenience, or modify these methods, or choose not to use them.
    def is_holiday(self, start_date):
        """
        The purpose of this method is to check if the date entered is a holiday(Australian) or not
        :param: start_date: The date that charging starts
        """

        return start_date in holidays.AU()


    def is_weekday(self, start_date):
        """
        The purpose of this method is to check if the date entered is a weekday or not
        :param: start_date: The date that charging starts
        """
        chosen_day = start_date
        if chosen_day.weekday() > 4:
            return False
        else:
            return True


    def is_peak(self,start_time):
        """
        The purpose of this method is to check if the time entered lies within the peak time(Between 6am-6pm)
        :param: start_time: The time that charging starts
        """
        start_peak = datetime.strptime("06:00:00", '%H:%M:%S').time()
        off_peak = datetime.strptime("18:00:00", '%H:%M:%S').time()
        return start_time >= start_peak and \
            start_time <= off_peak

            
    def get_duration(self):
        """
        The purpose of this method is to obtain time required in format of days, H:M:S
        TOTAL DURATION OF CAR CHARGING
        """
        end_date = self.get_last_date()
        return end_date - self.full_date


    # to be acquired through API
    def get_sun_hour(self, date):
        """
        The purpose of this method is to acquire the sun_hour (sun_isolation) from the api given the date.
        :param: date: the date to check the sun_hour
        """
        response = self.search_weather(self.postcode, date)
        return response['sunHours']


    def get_last_date(self, date=""):
        """
        The purpose of this method is to acquire the last date of charging
        :param: date: the date when the car charging starts, if left empty, it takes the user inputted start_date
        """
        if date == "":
            start_date = self.full_date
        else:
            start_date = date
        last_date = start_date + timedelta(seconds=(self.time * 3600))
        return last_date



    def get_day_light_length(self, current_date):
        """
        The purpose of this method is to acquire the duration between sunrise to sunset of a given date
        :param: current_date: the date to check the duration between sunrise to sunset
        """
        response = self.search_weather(self.postcode, current_date)
        sun_rise = response['sunrise']
        sun_set = response['sunset']
        return datetime.strptime(sun_set, '%H:%M:%S') - datetime.strptime(sun_rise, '%H:%M:%S')


    
    def get_cloud_cover(self, date):
        """
        The purpose of this method is to acquire an array of cloud cover percentage based on the hour of a given date
        :param: date: the date to check the cloud cover
        """
        data = self.search_weather(self.postcode, date)
        weather_data = data['hourlyWeatherHistory']
        cloud_cover = []
        for item in weather_data:
            cloud_cover.append(item['cloudCoverPct'])
        return cloud_cover
    

    def calculate_solar_energy_req2(self):
        """
        The purpose of this method is to calculate the the cost of charging the car without taking into account of cloud cover
        """
        total_energy_needed =  (self.final_charge - self.inital_charge) / 100 * self.battery_capacity
        total_minutes_needed = self.time * 60
        energy_needed_per_minute = total_energy_needed / total_minutes_needed
        current_date = self.full_date
        last_date = self.get_last_date(current_date) # Get the last date of charging with time
        cost = 0
        sun_data = self.search_weather(self.postcode,current_date.strftime("%d/%m/%Y"))
        sunrise_time = datetime.strptime(sun_data['sunrise'],"%H:%M:%S").time() # Extracts time only
        sunrise = datetime.combine(self.start_date,sunrise_time) # Makes the time match the same date as current_date
        sunset_time = datetime.strptime(sun_data['sunset'],"%H:%M:%S").time() # Extracts time only
        sunset = datetime.combine(self.start_date,sunset_time) # Makes the time match the same date as current_date
        daylight_length = self.get_day_light_length(current_date.strftime("%d/%m/%Y"))

        while current_date < last_date: # Main loop which will go through all hours and calculate cost accordingly

            if current_date < sunrise: # If the current date is less than sunrise, calculate cost of charging until sunrise
                time_to_sunrise = (sunrise - current_date).total_seconds()
                time_to_end = ((last_date - current_date).total_seconds())
                time_gap = min(time_to_sunrise,time_to_end)
                energy_charged = (time_gap / 60) * energy_needed_per_minute
                cost += self.cost_calculation(current_date.time(), current_date.date(), 0, energy_charged)
                current_date = current_date + timedelta(seconds = time_gap)

            elif current_date >= sunset or current_date == sunset: # Current date is past sunset and still needs charging
                # Calculate the sunrise and sunset for the next day
                next_day = (current_date + timedelta(days = 1))
                sun_data = self.search_weather(self.postcode, next_day.strftime("%d/%m/%Y"))
                sunrise_time = datetime.strptime(sun_data['sunrise'],"%H:%M:%S").time()
                sunrise = datetime.combine(next_day.date(),sunrise_time)
                sunset_time = datetime.strptime(sun_data['sunset'],"%H:%M:%S").time()
                sunset = datetime.combine(next_day.date(), sunset_time)
                daylight_length = self.get_day_light_length(next_day.strftime("%d/%m/%Y"))

                # Check if the last_date is earlier than the next day's sunrise or exactly on sunrise
                if last_date < sunrise or last_date == sunrise:
                    time_gap = last_date - current_date
                    energy_charged = (time_gap.seconds / 60) * energy_needed_per_minute
                    cost += self.cost_calculation(current_date.time(), current_date.date(), 0, energy_charged)
                    current_date = last_date

                else: # Means that last date will be later than the next day's sunrise
                    time_gap = sunrise - current_date
                    energy_charged = (time_gap.seconds / 60) * energy_needed_per_minute
                    cost += self.cost_calculation(current_date.time(), current_date.date(), 0, energy_charged)
                    current_date = sunrise

            else: #The current date is within sunrise and sunset
                time_to_end = (last_date - current_date).total_seconds() / 60
                next_hour = current_date # Not sure whether doing current_date.replace() will change current_date as well
                next_hour = next_hour.replace(hour = current_date.hour + 1, minute = 0, second = 0)
                time_to_next_hour = (next_hour - current_date).total_seconds() / 60 # Increment the hour by 1 and make the seconds 0
                time_to_sunset = (sunset - current_date).total_seconds()/ 60
                charging_duration = min(time_to_end, time_to_next_hour, time_to_sunset) # Finding out which comes first
                sun_hour = self.get_sun_hour(current_date.strftime("%d/%m/%Y"))
                solar_energy = sun_hour * ((charging_duration / 60 ) / (daylight_length.seconds / 3600)) * 50 * 0.2 # Calculate energy generated
                energy_needed = charging_duration * energy_needed_per_minute # Calculate energy needed
                cost += self.cost_calculation(current_date.time(), current_date.date(), solar_energy, energy_needed)
                current_date = current_date + timedelta(seconds = charging_duration*60) # Increment the current date by the charging duration
  
        return round(cost,2)


    def calculate_solar_energy_req3_aux(self):
        """
        The purpose of this method is to find the past 3 years of the user inputted date and call calculate_solar_energy_req3() to find 
        the mean cost of charging
        """
        
        # Aux method will find reference dates and 2 previous dates and call calculate_solar_energy_req3 to calculate the cost
        # It will then add all three costs and find the mean
        today = datetime.today().date()
        first_date = None
        second_date = None
        third_date = None
        days_in_a_year = 365
        if self.start_date < today:  # Start date is before today
            if self.is_leap_year(self.start_date.year):
                days_in_a_year = 366
            else:
                days_in_a_year = 365
            first_date = self.start_date - timedelta(days_in_a_year)
        elif self.start_date == today: #Start date is exactly today
            if self.is_leap_year(self.start_date.year):
                days_in_a_year = 366
            else:
                days_in_a_year = 365
            first_date = self.start_date - timedelta(days_in_a_year)
        else: #Start date is after today
            if self.start_date.month < today.month: #If the start dates month is before today's month
                first_date = today.replace(month=self.start_date.month,day = self.start_date.day)
            elif self.start_date.month > today.month or (self.start_date.month == today.month and self.start_date.day > today.day): #If start dates month is after todays month or its the same month and days after today
                first_date = today.replace(month=self.start_date.month,day = self.start_date.day) - timedelta(days_in_a_year)
            else: #Start dates month and day are the same but year is after today
                first_date = today
        second_date = first_date.replace(year=first_date.year - 1)
        third_date = second_date.replace(year=second_date.year - 1)
        total_cost = self.calculate_solar_energy_req3(first_date) + self.calculate_solar_energy_req3(second_date) + self.calculate_solar_energy_req3(third_date)
        mean_cost = total_cost/3
        
        return round(mean_cost,2)
    

    def calculate_solar_energy_req3(self,start_date):
        """
        The purpose of this method is to calculate the cost of charging of a given date while taking into account of cloud cover
        :param: start_date: the date where charging starts
        """
        total_energy_needed =(self.final_charge - self.inital_charge) / 100 * self.battery_capacity
        total_minutes_needed =self.time * 60
        energy_needed_per_minute = total_energy_needed / total_minutes_needed
        current_date = datetime.combine(start_date,
                                        self.start_time)  # Need to use combine() because start_date is in datetime.date format and not datetime
        last_date = self.get_last_date(current_date)  # Get the last date of charging with time
        cost = 0
        data = self.search_weather(self.postcode, current_date.strftime("%d/%m/%Y"))
        sunrise_time = datetime.strptime(data['sunrise'], "%H:%M:%S").time()  # Extracts time only
        sunrise = datetime.combine(start_date, sunrise_time)  # Makes the time match the same date as current_date
        sunset_time = datetime.strptime(data['sunset'], "%H:%M:%S").time()  # Extracts time only
        sunset = datetime.combine(start_date, sunset_time)  # Makes the time match the same date as current_date
        cloud_cover = self.get_cloud_cover(current_date.strftime("%d/%m/%Y"))
        daylight_length = self.get_day_light_length(current_date.strftime("%d/%m/%Y"))

        while current_date < last_date: #Main loop which will go through all hours and calculate cost accordingly
            if current_date < sunrise: #If the current date is less than sunrise, calculate cost of charging until sunrise
                time_to_sunrise = ((sunrise - current_date).total_seconds())
                time_to_end = ((last_date - current_date).total_seconds())
                time_gap = min(time_to_sunrise,time_to_end)
                energy_charged = (time_gap/60) * energy_needed_per_minute
                cost += self.cost_calculation(current_date.time(),current_date.date(),0,energy_charged)
                current_date = current_date + timedelta(seconds = time_gap)
            elif current_date >= sunset or current_date == sunset: #Current date is past sunset and still needs charging
                #Calculate the sunrise and sunset for the next day
                next_day = (current_date + timedelta(1))
                data = self.search_weather(self.postcode, next_day.strftime("%d/%m/%Y"))
                sunrise_time = datetime.strptime(data['sunrise'],"%H:%M:%S").time()
                sunrise = datetime.combine(next_day.date(),sunrise_time)
                sunset_time = datetime.strptime(data['sunset'],"%H:%M:%S").time()
                sunset = datetime.combine(next_day.date(), sunset_time)
                cloud_cover = self.get_cloud_cover(next_day.strftime("%d/%m/%Y"))
                daylight_length = self.get_day_light_length(next_day.strftime("%d/%m/%Y"))
                #Check if the last_date is earlier than the next day's sunrise or exactly on sunrise
                if last_date < sunrise or last_date == sunrise:
                    time_gap = last_date - current_date
                    energy_charged = (time_gap.seconds/60) * energy_needed_per_minute
                    cost += self.cost_calculation(current_date.time(),current_date.date(),0,energy_charged)
                    current_date = last_date
                else: #Means that last date will be later than the next day's sunrise
                    time_gap = sunrise - current_date
                    energy_charged = (time_gap.seconds/60) * energy_needed_per_minute
                    cost += self.cost_calculation(current_date.time(),current_date.date(),0,energy_charged)
                    current_date = sunrise
            else: #The current date is within sunrise and sunset
                time_to_end = (last_date - current_date).total_seconds()/60
                next_hour = current_date #Not sure whether doing current_date.replace() will change current_date as well
                next_hour = next_hour.replace(hour = current_date.hour+1, minute = 0, second = 0)
                time_to_next_hour = (next_hour - current_date).total_seconds()/60 #Increment the hour by 1 and make the seconds 0
                time_to_sunset = (sunset - current_date).total_seconds()/60
                charging_duration = min(time_to_end,time_to_next_hour,time_to_sunset) #Finding out which comes first
                sun_hour = self.get_sun_hour(current_date.strftime("%d/%m/%Y"))
                cc = cloud_cover[current_date.hour%24] #Index of cloud_cover is from 0-23 hence need to use % to prevent index out of bound
                solar_energy = sun_hour * (charging_duration/60)/(daylight_length.seconds/3600)*(1-(cc/100)) * 50 * 0.2 #Calculate energy generated
                energy_needed = charging_duration * energy_needed_per_minute #Calculate energy needed
                cost += self.cost_calculation(current_date.time(),current_date.date(),solar_energy,energy_needed)
                current_date = current_date + timedelta(seconds = charging_duration*60) #Increment the current date by the charging duration
        return cost


    def calculate_solar_energy_req4(self):
        """
        The purpose of this method is to find the amount of solar energy generated 30 days and 365 days prior to the user inputted date
        """
        month_energy = 0
        year_energy = 0
        month_prior = (self.full_date - timedelta(days = 30)) # Although this will have a preset time, we will change it afterwards
        year_prior = (self.full_date - timedelta(days = 365)) # Although this will have a preset time, we will change it afterwards
        current_date = year_prior
        while current_date.date() < self.full_date.date():
            daily_solar_energy = 0
            data = self.search_weather(self.postcode,current_date.strftime("%d/%m/%Y"))
            sunrise_time = datetime.strptime(data['sunrise'],"%H:%M:%S").time()
            current_date = datetime.combine(current_date.date(),sunrise_time) #Set the current time as sunrise everytime we start a new day
            sunset_time = datetime.strptime(data['sunset'],"%H:%M:%S").time()
            sunset = datetime.combine(current_date.date(),sunset_time)
            cloud_cover = self.get_cloud_cover(current_date.strftime("%d/%m/%Y"))
            daylight_length = self.get_day_light_length(current_date.strftime("%d/%m/%Y"))
            sun_hour = self.get_sun_hour(current_date.strftime("%d/%m/%Y"))
            while current_date < sunset:
                next_hour = current_date
                next_hour = next_hour.replace(hour= next_hour.hour + 1, minute = 0, second = 0) #Set the next hour
                time_to_sunset = (sunset - current_date).seconds/60
                time_to_next_hour = (next_hour - current_date).seconds/60
                charging_time = min(time_to_next_hour,time_to_sunset) #Find out whether current date is closer to sunset or next hour
                cc = cloud_cover[current_date.hour%24]
                solar_energy = sun_hour * ((charging_time/60)/(daylight_length.seconds/3600))*(1-(cc/100)) * 50 * 0.2
                daily_solar_energy += solar_energy #Add hourly solar energy to daily_solar_energy
                current_date = current_date + timedelta(seconds = charging_time*60) # Increment the current date by number of seconds to next hour
            if current_date.date() >= month_prior.date():
                month_energy += daily_solar_energy
            year_energy +=daily_solar_energy #Add daily energy to total energy
            current_date = current_date + timedelta(days = 1) #Increment the day by 1
        year_energy = round(year_energy,2)
        month_energy = round(month_energy,2)
        return f"yearly energy: {year_energy}, monthly energy: {month_energy}"
    

    def is_leap_year(self, year):
        """
        Method that checks if the year entered is a leap year
        :param: year: Current year
        """
        if (year % 400 == 0 or year % 100 != 0) and year % 4 == 0:
            return True
        else:
            return False


    def search_weather(self, post_code, start_date):
        """
        The purpose of this method is to call the api with the given postcode and start date and returns a dictionary
        :param: post_code: the post code of the location
        :param: start_date: the date to check weather
        """
        current_date = datetime.strptime(start_date, "%d/%m/%Y")
        current_date = current_date.strftime("%Y-%m-%d")
        with urlopen(f"http://118.138.246.158/api/v1/location?postcode={post_code}") as response:
            source = response.read()
        data = json.loads(source)
        id = data[0]['id']
        with urlopen(f"http://118.138.246.158/api/v1/weather?location={id}&date={current_date}") as response:
            source = response.read()
        data = json.loads(source)
        return data
