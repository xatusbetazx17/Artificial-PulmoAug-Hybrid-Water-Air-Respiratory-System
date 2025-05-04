import pytest
from software.simulation.simulate_flux import (
    dissolved_o2_mg_per_l,
    required_water_flow
)

def test_dissolved_o2_positive():
    assert dissolved_o2_mg_per_l(20.0) > 0

def test_required_water_flow():
    # known values: VO₂=1.2 L/min, conc≈40 mg/L, eff=0.3
    flow = required_water_flow(1.2, 40.0, 0.3)
    expected = (1.2 * 1000 * 1.429) / (40.0 * 0.3)
    assert pytest.approx(flow, rel=1e-2) == expected
