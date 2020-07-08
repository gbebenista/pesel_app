from random import choice
from faker import Faker
import time


def timer(func):
    def wrapper_timer(*args, **kwargs):
        start_time = time.time()
        do_things = func(*args, **kwargs)
        stop_time = time.time()
        elapsed_time = stop_time - start_time
        print("Executing time is: ", elapsed_time)
        return do_things
    return wrapper_timer


class GenderNotValid(Exception):
    pass


class GeneratePesel:

    def __call__(self, *args):
        return self.generate(*args)

    def _get_year_to_generate_pesel(self, dob):
        if not isinstance(dob.year, int):
            raise AttributeError("Year must be a string")
        if 1800 <= dob.year <= 2299:
            year = str(dob.year)
            return year
        raise ValueError("Year must be between 1800 and 2299")

    def _get_day_to_generate_pesel(self, dob):
        if not isinstance(dob.day, int):
            raise AttributeError
        day = str(dob.day)
        if len(day) == 1:
            day_list = ["0", day[0]]
        else:
            day_list = [day[0], day[1]]
        return day_list

    def _month_dictionary(self, dob):
        year = [self._get_year_to_generate_pesel(dob)[0], self._get_year_to_generate_pesel(dob)[1]]
        year_joined = int(''.join(map(str, year)))

        month_dict = {
            18: 8,
            19: 0,
            20: 2,
            21: 4,
            22: 6
        }

        right_month = month_dict.get(year_joined)
        return right_month

    def _get_month_to_generate_pesel(self, dob):
        if not isinstance(dob.month, int):
            raise AttributeError
        month = str(dob.month)
        if len(month) == 2 and month[0] == "1":
            month_list = [self._month_dictionary(dob) + 1, month[1]]
        else:
            month_list = [self._month_dictionary(dob), month[0]]
        return month_list

    def _is_gender_value_valid(self, gender):
        if isinstance(gender, str) and gender in ["M", "K"]:
            return True
        return False

    def _get_gender_value(self, gender):
        if not self._is_gender_value_valid(gender):
            raise GenderNotValid
        if gender == "K":
            gender_value = choice(range(0, 8, 2))
            return gender_value
        gender_value = choice(range(1, 9, 2))
        return gender_value

    @staticmethod
    def _get_random_number():
        random_to_pesel = str(choice(range(0, 9, 1)))

        return random_to_pesel

    def _join_pesel_elements(self, dob, gender):
        pesel_elements = [self._get_year_to_generate_pesel(dob)[2], self._get_year_to_generate_pesel(dob)[3],
                          self._get_month_to_generate_pesel(dob)[0], self._get_month_to_generate_pesel(dob)[1],
                          self._get_day_to_generate_pesel(dob)[0], self._get_day_to_generate_pesel(dob)[1],
                          self._get_random_number(),
                          self._get_random_number(), self._get_random_number(), self._get_gender_value(gender)]

        return pesel_elements

    def _make_control_sum(self, dob, gender):
        control_sum_formula = [9, 7, 3, 1, 9, 7, 3, 1, 9, 7]
        control_sum = 0

        i = 0
        while i < 10:
            control_sum += int(self._join_pesel_elements(dob, gender)[i]) * control_sum_formula[i]
            i += 1

        return control_sum

    def _get_control_digit(self, dob, gender):
        control_digit = self._make_control_sum(dob, gender) % 10
        return control_digit

    def _join_control_digit_to_pesel(self, dob, gender):
        pesel_with_joined_control_digit = self._join_pesel_elements(dob, gender)
        pesel_with_joined_control_digit.append(self._get_control_digit(dob, gender))
        return pesel_with_joined_control_digit

    @timer
    def generate(self, dob, gender):
        generated_pesel_joined = ''.join(map(str, self._join_control_digit_to_pesel(dob, gender)))
        return generated_pesel_joined

    def fake_pesel(self, dob, gender):
        fake = Faker("pl_PL")
        return fake.pesel(dob, gender)
