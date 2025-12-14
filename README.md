# FG-HVAC-Display
Display the HVAC Data from CANbus messages on a custom screen or headunit video input.

There is a re-creation of the Monochrome FDIM HVAC display done in python, and there is a recreation of the Colour FDIM Display done in HTML/Javascript - meant to be used with a device running socketCAN, looking for a CAN network on can0 to read ID 0x353 for HVAC DATA, and button pushes are sent out on 0x307 to control the HVAC systemm. The HTML display is meant to be displayed on a Touchcreen of some kind, thus the touchscreen buttons....

<img width="899" height="572" alt="image" src="https://github.com/user-attachments/assets/00c7d778-3408-417a-affb-574f30a90dd3" />

### Ford FG Falcon ICC HVAC Display System
A complete recreation of the Ford FG Falcon Interior Command Centre (ICC) climate control display
#### Monochrome LCD Display (Python/Tkinter)
Circular clock with 60 tick marks and car silhouette
7-segment temperature displays
Front/rear defrost icons, airflow person, fan speed bar
Full button panel with LED indicators
Temperature slider controls with seat icons

#### Color Display (HTML/JavaScript/React)  
Modern interpretation with blue glow effects and scanlines
Dual-zone climate display (Passenger/Driver temperatures)
Animated icons for heated seats, recirculation, and airflow
Real-time clock with date
Interactive fan speed bar and all HVAC controls
