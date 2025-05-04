import pytest
from software.simulation.simulate_gas import ambient_pressure_at_altitude

def test_pressure_sea_level():
    assert pytest.approx(ambient_pressure_at_altitude(0), rel=1e-3) == 1.0

def test_pressure_decreases_with_altitude():
    p1, p2 = ambient_pressure_at_altitude(0), ambient_pressure_at_altitude(7000)
    assert p2 < p1
