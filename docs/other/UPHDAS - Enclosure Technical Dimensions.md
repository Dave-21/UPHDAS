**Raspberry Pi 5 Dimensions:**

- Length: 85 mm
- Width: 56 mm
- Height (approx.): 18 mm (considering tallest component, including ports)
- Mounting Hole Diameters: 2.7 mm and 3 mm

STEP file and CAD files for Raspberry Pi 5:

- STEP file (official, reliable dimensions):
  - <https://datasheets.raspberrypi.com/rpi5/RaspberryPi5-step.zip>
- Additional CAD references (I can’t confirm the accuracy of these dimensions):
  - <https://grabcad.com/library/raspberry-pi-5-2>
  - <https://makerworld.com/en/models/218275-raspberry-5-cad-model>

**ArduCam IMX477 HQ Camera Module Dimensions:**

- PCB Width and Length: 38 mm x 38 mm
- Height: Approximately 29 mm
- Width at Cable Connection: 34 mm

Camera Link:

- <https://www.arducam.com/product/12-3mp-imx477-hq-camera-module-b024001/>

**ArduCam 8-50mm Varifocal C-Mount Lens Dimensions:**

- Diameter: 40 mm
- Length: 68.3 mm
- Weight: 148g
- C-Mount thread depth: 5 mm

Lens Link:

- <https://www.arducam.com/product/arducam-8-50mm-varifocal-c-mount-lens-for-raspberry-pi-hq-camera-with-c-cs-adapter-ln057/>

**Ribbon Cable Dimensions:**

- Length: 300 mm
- Width: 11.5 mm

**General Requirements for Case Design:**

- Include ventilation ports (intake and exhaust), positioned on the sides or bottom, to dissipate heat from electronics.
- Enclosure is not airtight, so we need ingress protection from debris, moisture, and snow.
- Allow internal component access for maintenance (Raspberry Pi, Camera, Lens adjustments).
- Provide at least a 5-10° angled surface to allow runoff on optical viewing port.
- Material recommendations for the optical viewing port:
  - UV-resistant, high optical transparency (visible wavelengths)
  - Mechanically robust (resistant to scratching and breaking)
  - Cost-effective (eyeglass-quality polycarbonate or automotive-grade glass)

**Heater Management:**

- Consider putting the heater near viewing port for more effective snow/condensation removal.

**Power Management:**

- AC input through modular 16-gauge extension cable if needed.
- Bottom-mounted ports for cable entry, sealed with rubber gaskets or grommets.

**Additional Notes:**

- Allow slight dimensional tolerance for easy internal assembly.
- We might consider checking the Pi’s power cable slack and discuss possible solutions for cable management (anchor point for cable clips or zip-ties)

**Mechanical Drawings and Labeled Dimensions**

- Here’s a Google Drive link that has a couple of mechanical drawings and some labeled images with dimensions:
  - <https://drive.google.com/drive/folders/1LJb7Fg8mN19LTgqKchFTqy_Jr4UYCspg?usp=sharing>