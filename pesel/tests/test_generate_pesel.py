import pytest
import datetime
from generatepesel import GenderNotValid, GeneratePesel


# TODO: poprawić testy, sprawdzić coveragerc
class TestPeselGenerator:

    @pytest.fixture
    def dob_correct(self):
        dob = datetime.date(1992, 4, 13)
        return dob

    @pytest.fixture
    def dob_wrong_type(self):
        dob = "fdfsds"
        return dob

    @pytest.fixture
    def dob_wrong_year(self):
        dob = datetime.date(1700, 4, 4)
        return dob

    @pytest.fixture
    def gender_man(self):
        gender = "M"
        return gender

    @pytest.fixture
    def gender_woman(self):
        gender = "K"
        return gender

    @pytest.fixture
    def gender_wrong_type(self):
        gender = 3
        return gender

    @pytest.fixture
    def gender_not_gender(self):
        gender = "R"
        return gender

    def test_get_year_to_generate_correct(self, dob_correct):
        result = GeneratePesel()._get_year_to_generate_pesel(dob_correct)
        assert result == "1992"

    def test_get_year_to_generate_wrong_type(self, dob_wrong_type):
        with pytest.raises(AttributeError) as e:
            result = GeneratePesel()._get_year_to_generate_pesel(dob_wrong_type)
            assert e

    def test_get_year_to_generate_wrong_year(self, dob_wrong_year):
        with pytest.raises(ValueError) as e:
            result = GeneratePesel()._get_year_to_generate_pesel(dob_wrong_year)
            assert e

    def test_get_day_to_generate_correct(self, dob_correct):
        result = GeneratePesel()._get_day_to_generate_pesel(dob_correct)
        assert result == ["1", "3"]

    def test_get_day_to_generate_wrong_type(self):
        with pytest.raises(TypeError) as e:
            dob = datetime.time(1992, 3, "5354")
            result = GeneratePesel()._get_day_to_generate_pesel(dob)
            assert e

    def test_get_day_to_generate_wrong_attribute(self, dob_wrong_type):
        with pytest.raises(AttributeError) as e:
            result = GeneratePesel()._get_day_to_generate_pesel(dob_wrong_type)
            assert e

    def test_get_day_to_generate_wrong_day_value(self):
        with pytest.raises(ValueError) as e:
            dob = datetime.datetime(1992, 12, 32)
            result = GeneratePesel()._get_day_to_generate_pesel(dob)
            assert e

    def test_get_month_to_generate_correct(self, dob_correct):
        result = GeneratePesel()._get_month_to_generate_pesel(dob_correct)
        assert result == [0, "4"]

    def test_get_month_to_generate_wrong_attribute(self, dob_wrong_type):
        with pytest.raises(AttributeError) as e:
            result = GeneratePesel()._get_day_to_generate_pesel(dob_wrong_type)
            assert e

    def test_get_month_to_generate_wrong_type(self):
        with pytest.raises(TypeError) as e:
            dob = datetime.datetime(1992, "32", 31)
            result = GeneratePesel()._get_month_to_generate_pesel(dob)
            assert result

    def test_get_month_to_generate_wrong_value(self):
        with pytest.raises(ValueError) as e:
            dob = datetime.datetime(1992, 31, 31)
            result = GeneratePesel()._get_day_to_generate_pesel(dob)
            assert result

    def test_gender_value_woman(self, gender_woman):
        result = GeneratePesel()._get_gender_value(gender_woman)
        assert result % 2 == 0

    def test_gender_value_man(self, gender_man):
        result = GeneratePesel()._get_gender_value(gender_man)
        assert result % 2 == 1

    def test_gender_value_wrong_type(self, gender_wrong_type):
        with pytest.raises(GenderNotValid) as e:
            result = GeneratePesel()._get_gender_value(gender_wrong_type)
            assert e

    def test_gender_value_not_gender(self, gender_not_gender):
        with pytest.raises(GenderNotValid) as e:
            result = GeneratePesel()._get_gender_value(gender_not_gender)
            assert e

    def test_join_pesel_elements_correct(self, dob_correct, gender_woman):
        result = GeneratePesel()._join_pesel_elements(dob_correct, gender_woman)
        assert result

    def test_join_pesel_elements_gender_not_valid(self, dob_correct, gender_not_gender):
        with pytest.raises(GenderNotValid) as e:
            result = GeneratePesel()._join_pesel_elements(dob_correct, gender_not_gender)
            assert e

    def test_join_pesel_elements_dob_not_valid(self, gender_woman):
        with pytest.raises(ValueError) as e:
            dob = datetime.datetime(1942, 33, 5)
            result = GeneratePesel()._join_pesel_elements(dob, gender_woman)
            assert e

    def test_make_control_sum_correct(self, dob_correct, gender_woman):
        result = GeneratePesel()._make_control_sum(dob_correct, gender_woman)
        assert result

    def test_make_control_sum_dob_not_valid(self, dob_wrong_type, gender_woman):
        with pytest.raises(AttributeError) as e:
            result = GeneratePesel()._make_control_sum(dob_wrong_type, gender_woman)
            assert result

    def test_make_control_sum_gender_not_valid(self, dob_correct, gender_not_gender):
        with pytest.raises(GenderNotValid) as e:
            result = GeneratePesel()._make_control_sum(dob_correct, gender_not_gender)
            assert e

    def test_generate_correct(self, dob_correct, gender_man):
        result = GeneratePesel().generate(dob_correct, gender_man)
        assert result

    def test_generate_wrong_dob(self, dob_wrong_type, gender_woman):
        with pytest.raises(AttributeError) as e:
            result = GeneratePesel().generate(dob_wrong_type, gender_woman)
            assert e

    def test_generate_dob_empty(self, gender_woman):
        with pytest.raises(AttributeError) as e:
            dob = ""
            result = GeneratePesel().generate(dob, gender_woman)
            assert e

    def test_generate_gender_not_gender(self, dob_correct, gender_not_gender):
        with pytest.raises(GenderNotValid) as e:
            result = GeneratePesel().generate(dob_correct, gender_not_gender)
            assert e
