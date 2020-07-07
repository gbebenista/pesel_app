import json
import click
from pesel.pesel import Pesel, PeselNotValid


@click.group()
def commands():
    pass


@commands.group()
def pesel():
    pass


@pesel.command()
@click.argument('pesel_number')
@click.option('--fmt', type=int, default=1)
def decryption(pesel_number, fmt):
    try:
        p = Pesel(peselkwarg=pesel_number)
        validation_value = p.validate()
        if validation_value is not True:
            click.echo(validation_value)
            return
        click.echo(validation_value)
        click.echo(p.date_of_birth(fmt))
        click.echo(p.gender_check())
    except Exception as e:
        print(e)


@pesel.command()
@click.argument('pesel_list', type=list, nargs=-1)
@click.option('--file', type=click.Path())
@click.option('--fmt', type=int, default=1)
def dob(pesel_list, file, fmt):
    if file:
        with open(file, "r") as f:
            lines = f.readlines()

        pesel_list = [json.loads(p)["pesel"] for p in lines]

    for pesel in pesel_list:
        try:
            p = Pesel(peselkwarg=pesel)
            click.echo(p.validate())
            click.echo(p.date_of_birth(fmt))
            click.echo(p.gender_check())
        except PeselNotValid as e:
            print(e)


@pesel.command()
@click.option('--dob', type=click.DateTime(), required=True)
@click.option('--gender', required=True)
def generate(dob, gender):
    p = Pesel()
    print(p.generate(dob, gender))


# if __name__ == '__main__':
commands()
