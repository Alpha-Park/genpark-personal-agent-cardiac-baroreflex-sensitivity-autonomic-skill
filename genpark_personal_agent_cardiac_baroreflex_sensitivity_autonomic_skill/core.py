# -*- coding: utf-8 -*-
"""Cardiac Baroreflex Sensitivity Sentinel for GenPark Personal Agent."""
import json
from typing import Dict, Any

class CardiacBaroreflexSensitivitySentinel:
    @staticmethod
    def compute_baroreflex_sensitivity_index(rr_interval_delta_ms: float, systolic_pressure_delta_mmhg: float, baseline_hrv_rmssd: float = 45.0) -> Dict[str, Any]:
        # BRS = delta_RR / delta_SBP (ms/mmHg)
        brs_slope = round(rr_interval_delta_ms / max(0.5, abs(systolic_pressure_delta_mmhg)), 2)
        if brs_slope < 5.0:
            tier = "DEPRESSED_AUTONOMIC_RESTORATION (High Mortality Risk)"
            vagal_status = "Severely blunted parasympathetic buffering; arterial stiffness and sympathetic hyperactivity."
        elif brs_slope < 10.0:
            tier = "MODERATE_CARDIOVASCULAR_STIFFNESS"
            vagal_status = "Sub-optimal autonomic elasticity; elevated exertional blood pressure surge."
        elif brs_slope <= 25.0:
            tier = "HEALTHY_VAGAL_ELASTICITY"
            vagal_status = "Optimal cardiac parasympathetic modulation and rapid hemodynamic stabilization."
        else:
            tier = "ATHLETIC_SUPRA_PHYSIOLOGICAL"
            vagal_status = "Elite aerobic endurance autonomic adaptation."

        return {
            "brs_slope_ms_per_mmhg": brs_slope,
            "baseline_rmssd_ms": baseline_hrv_rmssd,
            "autonomic_buffering_tier": tier,
            "vagal_function_assessment": vagal_status
        }

    @staticmethod
    def synthesize_vagal_nerve_stimulation_protocol(brs_score: float) -> Dict[str, Any]:
        return {
            "current_brs": brs_score,
            "target_brs_ms_per_mmhg": 15.0,
            "neuro_interventions": [
                "Resonance Frequency Breathing: Inhale 4.0s, Exhale 6.0s (0.1 Hz) for 20 minutes daily using haptic pacer",
                "Auricular Vagus Nerve Stimulation (tVNS) at tragus/concha: 25 Hz, 200 µs pulse width, 15 min",
                "Cold splash face immersion (mammalian dive reflex) 30s to stimulate vagal bradycardia"
            ],
            "expected_outcome": "Restores blood pressure buffering and boosts RMSSD HRV by 18-35% in 4 weeks."
        }
