# experts/tire_pressure.py
import math

def compute_pressure(weight_kg: float,
                     tire_width_mm: float,
                     wheel_diameter_mm: float,
                     desired_patch_ratio: float = 1.0) -> dict:
    """
    Estimate optimal tire pressure:
      1) Approximate tire internal volume V ≈ π·(wheel_diameter/2)^2 × tire_width
         (a simplification treating tire as a thin torus)
      2) Contact patch area A ≈ V / (π·wheel_circumference) * desired_patch_ratio
      3) Pressure P = (weight * g) / A  [in Pa], convert to bar
    """
    g = 9.81
    r = wheel_diameter_mm / 2 / 1000  # m
    w = tire_width_mm / 1000          # m

    # rough volume (m³)
    V = 2 * math.pi * r * (math.pi * r**2 * w)
    circumference = 2 * math.pi * r

    A = (V / circumference) * desired_patch_ratio
    P_pa = (weight_kg * g) / A
    P_bar = P_pa / 1e5

    return {
        'pressure_bar': round(P_bar, 2),
        'contact_area_cm2': round(A * 1e4, 1),
        'tire_volume_l': round(V * 1e3, 2)
    }

