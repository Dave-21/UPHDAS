**Angular Resolution (Arc Seconds per Pixel)**

**IMX519 with 120° FOV Lens**

**Sensor and Lens Parameters:**

- **Resolution:** 16 MP
- **Pixel Size:** 1.22 µm
- **Sensor Diagonal:** ≈ 7.2 mm
- **Field of View (Diagonal):** 120°

**Effective Focal Length:**  
  Formula: θ = 2 · arctan(d/(2f))

- f ≈ d / (2 · tan(θ/2))
- d = 7.2 mm and θ = 120°:  
      f ≈ 7.2 mm / (2 · tan(60°))  
        ≈ 7.2 / (2 · 1.732)  
        ≈ 7.2 / 3.464  
        ≈ 2.08 mm

**Arc Seconds per Pixel:**  
The angular resolution per pixel is given by:  
  Arcsec/pixel = (Pixel Size \[m\] / f \[m\]) × 206265  
For the IMX519:  
  Pixel Size = 1.22 × 10⁻⁶ m, f = 0.00208 m  
  Arcsec/pixel ≈ (1.22×10⁻⁶ / 0.00208) × 206265  
        ≈ 121 arcsec/pixel

This means that each pixel covers around 2 arcminutes of the sky, which causes light to spread over a large angular area, reducing the signal-to-noise ratio (SNR).

**IMX477 with 8–50 mm Varifocal C/CS Mount Lens**

**Sensor and Lens Parameters:**

- **Resolution:** 12.3 MP
- **Pixel Size:** 1.55 µm
- **Assumed Sensor Diagonal:** ≈ 7.9 mm

**Wide Setting (8 mm)**  
  f = 8 mm = 0.008 m  
  Arcsec/pixel = (1.55×10⁻⁶ / 0.008) × 206265  
        ≈ 40 arcsec/pixel

**Telephoto Setting (50 mm)**

    f = 50 mm = 0.05 m  
  Arcsec/pixel = (1.55×10⁻⁶ / 0.05) × 206265  
        ≈ 6.4 arcsec/pixel

This means each pixel covers around 40 arcseconds, which is 3 times better, boosting the SNR.

**Sensitivity and Limiting Visual Magnitude**

**Photon Collection & Signal Concentration**

- **Pixel Area Comparison:**
  - IMX519: (1.22 µm)² ≈ 1.49 × 10⁻¹² m²
  - IMX477: (1.55 µm)² ≈ 2.40 × 10⁻¹² m²  
        → **Improvement Factor in Area:** ≈ 2.40/1.49 ≈ 1.61

The IMX477 will pick up approximately 2.9 visual magnitudes lower than the IMX519.

**Estimated Limiting Magnitudes**

| **LEO Distance (km)** | **IMX519 Limiting Mag** | **IMX477 Limiting Mag** |
| --- | --- | --- |
| **400** | **7** | **10.76** |
| **600** | **6.119543705** | **9.879543705** |
| **800** | **5.494850022** | **9.254850022** |
| **1000** | **5.010299957** | **8.770299957** |
| **1200** | **4.614393726** | **8.374393726** |
| **1400** | **4.279659778** | **8.039659778** |
| **1600** | **3.989700043** | **7.749700043** |
| **1800** | **3.733937431** | **7.493937431** |
| **2000** | **3.505149978** | **7.265149978** |

This table demonstrates that the IMX519 will not capture many LEO satellites since most do not have a high visual magnitude, especially at further distances. For instance, most Starlink satellites have a visual magnitude between 5 and 8 under 1,000 km (and above 600 km), which means that the IMX519 wouldn’t typically pick up a Starlink satellite, whereas the IMX477 would. OneWeb satellites usually have a visual magnitude between 5 and 10 past 1,000 km (some are below 1,000 km, but not many, and not by much), which means the IMX519 wouldn’t be able to capture these, but, the IMX477 usually would.

**Lens Availability and Mount Considerations**

- **M12 Mount (IMX519):**

The IMX519 has an M12 mount. Unfortunately, there aren’t many lenses for this mount that work best for our situation (fast aperture for astrophotography), and if we relied on an adapter, the C/CS mounts lenses wouldn’t work as well with it, would negatively affect the light going into the sensor (decrease resolution), and cause some distortion.

- **C/CS Mount (IMX477):**

The IMX477 uses a CS mount by default and works well with most C/CS lens. The thing is, there are more C/CS mount lenses that work well for our project (made for fast aperture astrophotography), so going with a C/CS mount camera is our best option.

**Conclusion**

- **IMX519 Drawbacks:**

The IMX519, with its smaller sensor and less flexible lens availability, makes it difficult to get the optimal angular coverage, and won’t capture as faint of objects. It looks like it wouldn’t even detect a lot of Starlink satellites past 500 km (magnitude of 5 to 7).

- **IMX477 Advantages:**

The IMX477 has a larger sensor and a more adaptable lens configuration, which helps increase the light sensitivity for faint (and distant) objects.