# -*- coding: utf-8 -*-
"""Critical Power & W-Prime Anaerobic Work Capacity Battery Model for GenPark Personal Agent."""
import json
import math
from typing import Dict, Any

class CriticalPowerWPrimeAnaerobicBatteryModel:
    """Hyperbolic 2-parameter Critical Power (CP) and anaerobic capacity (W') engine."""

    @staticmethod
    def compute_critical_power_and_wprime(p1_watts: float, t1_seconds: int, p2_watts: float, t2_seconds: int) -> Dict[str, Any]:
        """Linear work-time model: Work = CP * t + W' -> CP = (W2 - W1)/(t2 - t1)."""
        w1_joules = p1_watts * t1_seconds
        w2_joules = p2_watts * t2_seconds

        delta_t = t2_seconds - t1_seconds
        if delta_t <= 0:
            raise ValueError("t2 must be greater than t1")

        cp = (w2_joules - w1_joules) / delta_t
        wprime = w1_joules - (cp * t1_seconds)

        return {
            "critical_power_watts": round(cp, 1),
            "wprime_kilojoules": round(wprime / 1000.0, 2),
            "wprime_joules": round(wprime, 1),
            "anaerobic_energy_contribution": f"Above {round(cp, 1)}W, energy is finite and depletes W' ({round(wprime/1000.0, 1)} kJ).",
            "sustainable_aerobic_floor": f"Sub-{round(cp, 1)}W efforts allow dynamic W' reconstitution."
        }

    @staticmethod
    def simulate_wprime_depletion_and_recovery(critical_power_watts: float, wprime_joules: float, surge_power_watts: float, surge_duration_seconds: int, recovery_power_watts: float = 0.0, recovery_duration_seconds: int = 0) -> Dict[str, Any]:
        """Simulate dynamic W' depletion rate during attack and exponential recovery."""
        excess_power = max(0.0, surge_power_watts - critical_power_watts)
        joules_drained = excess_power * surge_duration_seconds
        wprime_remaining = max(0.0, wprime_joules - joules_drained)
        depletion_pct = round((joules_drained / wprime_joules) * 100.0, 1)

        # Skiba exponential recovery model: tau = 546 * e^(-0.01 * D_CP) + 316
        if recovery_duration_seconds > 0 and recovery_power_watts < critical_power_watts:
            sub_cp_deficit = critical_power_watts - recovery_power_watts
            tau = 546.0 * math.exp(-0.01 * sub_cp_deficit) + 316.0
            reconstituted_joules = (wprime_joules - wprime_remaining) * (1.0 - math.exp(-recovery_duration_seconds / tau))
            final_wprime = min(wprime_joules, wprime_remaining + reconstituted_joules)
        else:
            final_wprime = wprime_remaining

        return {
            "surge_power_watts": surge_power_watts,
            "surge_duration_sec": surge_duration_seconds,
            "wprime_drained_joules": round(joules_drained, 1),
            "battery_depletion_pct": min(100.0, depletion_pct),
            "wprime_post_surge_pct": round((wprime_remaining / wprime_joules) * 100.0, 1),
            "post_recovery_battery_pct": round((final_wprime / wprime_joules) * 100.0, 1),
            "tactical_pacing_advisory": "CRITICAL_BLOWUP_RISK: Surge exceeds total anaerobic capacity." if joules_drained > wprime_joules else "SAFE_SURGE: Battery remains resilient."
        }
