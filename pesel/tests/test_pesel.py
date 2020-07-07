import pytest

from pesel.pesel import Pesel, PeselNotValid


class TestClass:

    @pytest.fixture
    def test_fixture(self):
        assert 0

    def test_short_pesel_not_valid(self):
        with pytest.raises(PeselNotValid):
            result = Pesel(peselkwarg="2423").validate()
            assert result

    def test_pesel_string(self):
        result = Pesel(peselkwarg="12345678901")
        assert result

    def test_pesel_int(self):
        assert Pesel(peselkwarg=12345678901)

    def test_pesel_lenght(self):
        result = len(Pesel(peselkwarg="12345").pesel) != 11
        assert result

    def test_pesel_char(self):
        with pytest.raises(ValueError):
            assert Pesel(peselkwarg="qwertyuiop")

    def test_gender_woman(self):

        gender_woman = Pesel(peselkwarg="97082035264").gender_check()
        assert gender_woman == "Kobieta"

    def test_gender_man(self):

        gender_man = Pesel(peselkwarg="97081032157").gender_check()
        assert gender_man == "Mężczyzna"

    def test_birthdate_correct(self):

        birthdate_correct = Pesel(peselkwarg="97121100156").date_of_birth()
        assert birthdate_correct == "1997-Dec-11"

    def test_birthdate_failure(self):
        with pytest.raises(ValueError) as e:
            birthdate_failure = Pesel(peselkwarg="97341100156").date_of_birth()
            assert e.value == 'month must be in 1..12'

    def test_control_sum_correct(self):
        control_sum = Pesel(peselkwarg="97341100156")._calculate_control_sum()
        assert  control_sum

    def test_control_sum_failure(self):
        with pytest.raises(ValueError) as e:
            control_sum = Pesel(peselkwarg="qweetrywer1")._calculate_control_sum()
            assert control_sum

    def test_validate_correct(self):
        result = Pesel(peselkwarg="97081800157").validate()
        assert result

    def test_validate_failure(self):
        with pytest.raises(PeselNotValid):
            result = Pesel(peselkwarg="97081800167").validate()
            assert result

    #testy dla generowania numeru PESEL

