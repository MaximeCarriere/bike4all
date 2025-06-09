# experts/pure_kinematic.py

import math

def compute_speed(chainring_teeth: int,
                  sprocket_teeth: int,
                  cadence_rpm: float,
                  wheel_diameter: float) -> dict:
    """
    Pure kinematic model:
      speed_m_s = (π × diameter) × (cadence_rpm/60) × (chainring/sprocket)
      speed_kmh = speed_m_s × 3.6

    Returns a dict with speed_kmh and intermediate values.
    """
    circumference = math.pi * wheel_diameter
    gear_ratio    = chainring_teeth / sprocket_teeth
    cadence_rps   = cadence_rpm / 60.0

    speed_m_s = circumference * cadence_rps * gear_ratio
    speed_kmh = speed_m_s * 3.6

    return {
        'speed_kmh':     round(speed_kmh, 1),
        'gear_ratio':    round(gear_ratio, 2),
        'circumference': round(circumference, 2),
        'cadence_rps':   round(cadence_rps, 2),
        'cadence_rpm':   cadence_rpm
    }

