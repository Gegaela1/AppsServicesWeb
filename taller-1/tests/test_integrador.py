from integrador import (
    fahrenheit_a_celsius,
    ms_a_kmh
)


def test_fahrenheit_a_celsius():

    resultado = fahrenheit_a_celsius(32)

    assert resultado == 0


def test_ms_a_kmh():

    resultado = ms_a_kmh(1)

    assert resultado == 3.6


def test_temperatura_212_f():

    resultado = fahrenheit_a_celsius(212)

    assert resultado == 100


def test_viento_10_ms():

    resultado = ms_a_kmh(10)

    assert resultado == 36


def test_viento_0_ms():

    resultado = ms_a_kmh(0)

    assert resultado == 0