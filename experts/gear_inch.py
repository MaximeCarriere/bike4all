# experts/gear_inch.py
import math

def compute_speed(chainring_teeth: int,
                  sprocket_teeth: int,
                  cadence_rpm: float,
                  wheel_diameter: float) -> dict:
    """
    Gear‐Inch model:
      1) Convert diameter (m → inches)
      2) GearInches = (chainring ÷ sprocket) × diameter_in
      3) dist_per_rev_m = (GearInches × π) / 12
      4) speed_m_s = dist_per_rev_m × (cadence_rpm/60)
      5) speed_kmh = speed_m_s × 3.6
    """
    diameter_in = wheel_diameter * 39.3701
    gear_inches = (chainring_teeth / sprocket_teeth) * diameter_in

    dist_per_rev_m = (gear_inches * math.pi) / 12.0
    cadence_rps    = cadence_rpm / 60.0
    speed_m_s      = dist_per_rev_m * cadence_rps
    speed_kmh      = speed_m_s * 3.6

    return {
        'speed_kmh':    round(speed_kmh, 1),
        'gear_inches':  round(gear_inches, 1),
        'dist_per_rev': round(dist_per_rev_m, 2),
        'cadence_rps':  round(cadence_rps, 2),
        'cadence_rpm':  cadence_rpm
    }
