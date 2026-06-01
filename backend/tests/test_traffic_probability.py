"""
TDD Tests: Traffic Probability Service
Scenarios: TP-01 through TP-08
"""
import pytest
from app.services.traffic_probability import junction_probability, probabilistic_traffic


class TestJunctionProbability:
    """Unit tests for junction_probability function"""

    def test_tp01_junction_type_B_returns_0_5(self):
        """TP-01: Junction type 'B' (belokan) → probabilitas 0.5"""
        assert junction_probability("B") == 0.5

    def test_tp02_junction_type_P_returns_one_third(self):
        """TP-02: Junction type 'P' (T-junction) → probabilitas 1/3"""
        result = junction_probability("P")
        assert abs(result - 1/3) < 1e-10

    def test_tp03_junction_type_JK_returns_0_4(self):
        """TP-03: Junction type 'JK' (jalan kecil) → probabilitas 0.4"""
        assert junction_probability("JK") == 0.4

    def test_tp04_junction_type_unknown_returns_0_8(self):
        """TP-04: Junction type unknown → default probabilitas 0.8"""
        assert junction_probability("X") == 0.8
        assert junction_probability("UNKNOWN") == 0.8
        assert junction_probability("") == 0.8


class TestProbabilisticTraffic:
    """Unit tests for probabilistic_traffic function"""

    def test_tp05_multiple_junctions(self):
        """TP-05: Probabilistic traffic dengan multiple junctions [B, P, B]"""
        result = probabilistic_traffic(1000, ["B", "P", "B"])
        expected = 1000 * 0.5 * (1/3) * 0.5  # ≈ 83.33
        assert abs(result - expected) < 0.01

    def test_tp06_empty_junctions_returns_same_traffic(self):
        """TP-06: Traffic dengan junction list kosong → traffic tidak berubah"""
        assert probabilistic_traffic(1000, []) == 1000.0

    def test_tp07_single_junction_B(self):
        """TP-07: Traffic dengan single junction 'B'"""
        assert probabilistic_traffic(500, ["B"]) == 250.0

    def test_tp08_zero_initial_traffic(self):
        """TP-08: Traffic awal 0 → tetap 0 berapapun junction"""
        assert probabilistic_traffic(0, ["B", "P"]) == 0.0
        assert probabilistic_traffic(0, ["B", "P", "JK", "B"]) == 0.0
