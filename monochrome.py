#!/usr/bin/env python3
"""
Ford FG Falcon ICC HVAC Display
============================================================
Recreation of the Ford FG Falcon FDIM HVAC display.

Author: Jakka351
"""

import tkinter as tk
import math
from datetime import datetime
from dataclasses import dataclass
from enum import IntEnum


# =============================================================================

BG_COLOR = '#d0d0c8'      # LCD background - grayish cream
FG_COLOR = '#000000'      # Pure black
PANEL_BG = '#508080'      # Teal panel background (from your screenshot)


# =============================================================================
# State
# =============================================================================

@dataclass 
class HVACState:
    set_temp: float = 23.5
    outside_temp: int = -12
    fan_speed: int = 5
    ac_on: bool = False
    auto_mode: bool = True
    front_defrost: bool = True
    rear_defrost: bool = True
    hours: int = 13
    minutes: int = 28


# =============================================================================
# Main Display Panel 
# =============================================================================

class HVACDisplay(tk.Canvas):
    """the HVAC LCD display"""
    
    def __init__(self, parent, state: HVACState):
        # Match original proportions
        super().__init__(parent, width=580, height=145, bg=BG_COLOR, 
                        highlightthickness=2, highlightbackground=FG_COLOR)
        self.state = state
        self.draw()
        
    def draw(self):
        self.delete("all")
        
        # =====================================================================
        # CLOCK CIRCLE (left side)
        # =====================================================================
        clock_cx, clock_cy = 70, 68
        clock_radius = 52
        
        # Draw 60 tick marks around the circle
        for i in range(60):
            angle = math.radians(i * 6 - 90)
            
            # Every 5th tick is longer (hour marks)
            if i % 5 == 0:
                inner_r = clock_radius - 9
                outer_r = clock_radius
                width = 2
            else:
                inner_r = clock_radius - 5
                outer_r = clock_radius
                width = 1
            
            x1 = clock_cx + inner_r * math.cos(angle)
            y1 = clock_cy + inner_r * math.sin(angle)
            x2 = clock_cx + outer_r * math.cos(angle)
            y2 = clock_cy + outer_r * math.sin(angle)
            
            self.create_line(x1, y1, x2, y2, fill=FG_COLOR, width=width)
        
        # Time display
        time_str = f"{self.state.hours:02d}:{self.state.minutes:02d}"
        self.create_text(clock_cx, clock_cy - 5, text=time_str, 
                        font=("Consolas", 18, "bold"), fill=FG_COLOR)
        
        # Car icon below time
        self._draw_car(clock_cx, clock_cy + 28)
        
        # =====================================================================
        # "Auto" LABEL
        # =====================================================================
        self.create_text(138, 48, text="Auto", font=("Arial", 13, "bold"),
                        fill=FG_COLOR, anchor='w')
        
        # =====================================================================
        # FRONT DEFROST ICON (windshield with wavy lines)
        # =====================================================================
        self._draw_front_defrost(200, 55)
        
        # =====================================================================
        # AIRFLOW ARROWS AND PERSON
        # =====================================================================
        self._draw_airflow_person(295, 60)
        
        # =====================================================================
        # REAR INDICATOR (dot + "Rear" + rear defrost icon)
        # =====================================================================
        # Filled circle
        self.create_oval(370, 45, 382, 57, fill=FG_COLOR, outline=FG_COLOR)
        
        # "Rear" label
        self.create_text(408, 72, text="Rear", font=("Arial", 9), fill=FG_COLOR)
        
        # =====================================================================
        # OUTSIDE TEMPERATURE (top right area)
        # =====================================================================
        self.create_text(310, 15, text="Outside", font=("Arial", 10), 
                        fill=FG_COLOR, anchor='w')
        
        # Temperature with 7-segment style
        self._draw_small_7seg(365, 8, "-")
        self._draw_small_7seg(378, 8, "1")
        self._draw_small_7seg(394, 8, "2")
        
        self.create_text(415, 15, text="°C", font=("Arial", 10), 
                        fill=FG_COLOR, anchor='w')
        
        # =====================================================================
        # SET TEMP SECTION (right side)
        # =====================================================================
        self.create_text(480, 12, text="Set Temp", font=("Arial", 10), 
                        fill=FG_COLOR, anchor='w')
        
        # Large 7-segment temperature display
        temp_x = 455
        temp_y = 28
        temp_str = f"{self.state.set_temp:04.1f}"
        
        digit_positions = []
        x_pos = temp_x
        for char in temp_str:
            if char == '.':
                # Decimal point
                self.create_oval(x_pos, temp_y + 42, x_pos + 6, temp_y + 48,
                               fill=FG_COLOR, outline=FG_COLOR)
                x_pos += 10
            else:
                self._draw_7seg(x_pos, temp_y, char, size='large')
                x_pos += 32
        
        # Degree symbol
        self.create_text(x_pos + 5, temp_y + 5, text="°", 
                        font=("Arial", 14, "bold"), fill=FG_COLOR, anchor='w')
        
        # =====================================================================
        # SNOWFLAKE AND FAN BAR
        # =====================================================================
        # Asterisk/snowflake
        self._draw_snowflake(462, 95)
        
        # Fan speed bar (8 rectangles)
        bar_x = 482
        bar_y = 88
        for i in range(8):
            x = bar_x + i * 13
            if i < self.state.fan_speed:
                self.create_rectangle(x, bar_y, x + 10, bar_y + 14,
                                     fill=FG_COLOR, outline=FG_COLOR)
            else:
                self.create_rectangle(x, bar_y, x + 10, bar_y + 14,
                                     fill='', outline=FG_COLOR, width=1)
        
        # =====================================================================
        # HORIZONTAL DIVIDER LINE
        # =====================================================================
        self.create_line(15, 115, 565, 115, fill=FG_COLOR, width=1)
        
        # =====================================================================
        # BOTTOM LABELS
        # =====================================================================
        self.create_text(250, 130, text="Semi-Auto", font=("Arial", 11), 
                        fill=FG_COLOR, anchor='center')
        
        self.create_text(520, 130, text="A/C Off", font=("Arial", 11), 
                        fill=FG_COLOR, anchor='center')
    
    def _draw_car(self, cx, cy):
        """Draw car silhouette icon"""
        # Car body profile
        points = [
            cx - 18, cy + 5,
            cx - 14, cy - 1,
            cx - 7, cy - 6,
            cx + 5, cy - 6,
            cx + 11, cy - 1,
            cx + 16, cy + 5,
        ]
        self.create_polygon(points, fill='', outline=FG_COLOR, width=2)
        
        # Wheels
        self.create_oval(cx - 14, cy + 2, cx - 6, cy + 10, outline=FG_COLOR, width=2)
        self.create_oval(cx + 4, cy + 2, cx + 12, cy + 10, outline=FG_COLOR, width=2)
        
    def _draw_front_defrost(self, cx, cy):
        """Draw front windshield defrost icon - exact match"""
        # Windshield outline (trapezoid/arch shape)
        self.create_polygon(
            cx - 22, cy + 18,
            cx - 14, cy - 18,
            cx + 14, cy - 18,
            cx + 22, cy + 18,
            fill='', outline=FG_COLOR, width=2
        )
        
        # Three wavy/zigzag heat lines
        for offset in [-8, 0, 8]:
            # Create zigzag pattern
            points = []
            y_start = cy - 12
            for i in range(5):
                x = cx + offset + (4 if i % 2 == 0 else -4)
                y = y_start + i * 7
                points.extend([x, y])
            self.create_line(points, fill=FG_COLOR, width=2)
        
        # "Front" label
        self.create_text(cx, cy + 30, text="Front", font=("Arial", 9), fill=FG_COLOR)
        
    def _draw_airflow_person(self, cx, cy):
        """Draw person with airflow arrows - exact match to original"""
        # Arrow pointing right (toward person's face)
        self.create_line(cx - 45, cy - 20, cx - 20, cy - 20, 
                        fill=FG_COLOR, width=2, arrow=tk.LAST, arrowshape=(8, 10, 4))
        
        # Person's head (circle)
        self.create_oval(cx - 5, cy - 30, cx + 10, cy - 15, outline=FG_COLOR, width=2)
        
        # Person's body/back (seated)
        self.create_line(cx + 2, cy - 15, cx - 2, cy + 5, fill=FG_COLOR, width=2)
        
        # Seat back
        self.create_line(cx - 15, cy + 20, cx - 10, cy - 5, fill=FG_COLOR, width=2)
        
        # Arrow pointing down (to feet)
        self.create_line(cx - 45, cy + 10, cx - 20, cy + 10,
                        fill=FG_COLOR, width=2, arrow=tk.LAST, arrowshape=(8, 10, 4))
        
        # Seat bottom
        self.create_line(cx - 15, cy + 20, cx + 15, cy + 20, fill=FG_COLOR, width=2)
        
        # Legs
        self.create_line(cx - 2, cy + 5, cx + 12, cy + 20, fill=FG_COLOR, width=2)
        
    def _draw_snowflake(self, cx, cy):
        """Draw asterisk/snowflake symbol"""
        # 6-pointed asterisk
        for angle in range(0, 360, 60):
            rad = math.radians(angle)
            x = cx + 8 * math.cos(rad)
            y = cy + 8 * math.sin(rad)
            self.create_line(cx, cy, x, y, fill=FG_COLOR, width=2)
        
    def _draw_7seg(self, x, y, digit, size='large'):
        """Draw a 7-segment digit"""
        if size == 'large':
            w, h, t = 24, 44, 5
        else:
            w, h, t = 12, 20, 3
            
        # Segment patterns
        patterns = {
            '0': (1,1,1,1,1,1,0),
            '1': (0,1,1,0,0,0,0),
            '2': (1,1,0,1,1,0,1),
            '3': (1,1,1,1,0,0,1),
            '4': (0,1,1,0,0,1,1),
            '5': (1,0,1,1,0,1,1),
            '6': (1,0,1,1,1,1,1),
            '7': (1,1,1,0,0,0,0),
            '8': (1,1,1,1,1,1,1),
            '9': (1,1,1,1,0,1,1),
            '-': (0,0,0,0,0,0,1),
            ' ': (0,0,0,0,0,0,0),
        }
        
        segs = patterns.get(digit, (0,0,0,0,0,0,0))
        
        # Segment A (top)
        if segs[0]:
            self.create_polygon(
                x + t, y,
                x + w - t, y,
                x + w - t - 2, y + t,
                x + t + 2, y + t,
                fill=FG_COLOR, outline=FG_COLOR
            )
        
        # Segment B (top right)
        if segs[1]:
            self.create_polygon(
                x + w, y + t,
                x + w, y + h//2 - 2,
                x + w - t, y + h//2 - 2,
                x + w - t, y + t + 2,
                fill=FG_COLOR, outline=FG_COLOR
            )
        
        # Segment C (bottom right)
        if segs[2]:
            self.create_polygon(
                x + w, y + h//2 + 2,
                x + w, y + h - t,
                x + w - t, y + h - t - 2,
                x + w - t, y + h//2 + 2,
                fill=FG_COLOR, outline=FG_COLOR
            )
        
        # Segment D (bottom)
        if segs[3]:
            self.create_polygon(
                x + t, y + h,
                x + w - t, y + h,
                x + w - t - 2, y + h - t,
                x + t + 2, y + h - t,
                fill=FG_COLOR, outline=FG_COLOR
            )
        
        # Segment E (bottom left)
        if segs[4]:
            self.create_polygon(
                x, y + h//2 + 2,
                x, y + h - t,
                x + t, y + h - t - 2,
                x + t, y + h//2 + 2,
                fill=FG_COLOR, outline=FG_COLOR
            )
        
        # Segment F (top left)
        if segs[5]:
            self.create_polygon(
                x, y + t,
                x, y + h//2 - 2,
                x + t, y + h//2 - 2,
                x + t, y + t + 2,
                fill=FG_COLOR, outline=FG_COLOR
            )
        
        # Segment G (middle)
        if segs[6]:
            self.create_polygon(
                x + t + 1, y + h//2 - t//2,
                x + w - t - 1, y + h//2 - t//2,
                x + w - t - 1, y + h//2 + t//2,
                x + t + 1, y + h//2 + t//2,
                fill=FG_COLOR, outline=FG_COLOR
            )
            
    def _draw_small_7seg(self, x, y, digit):
        """Draw small 7-segment digit for outside temp"""
        self._draw_7seg(x, y, digit, size='small')


# =============================================================================
# Button Panel - Exact Recreation
# =============================================================================

class HVACButtons(tk.Canvas):
    """Button panel - exact recreation"""
    
    def __init__(self, parent, callbacks):
        super().__init__(parent, width=580, height=45, bg=BG_COLOR,
                        highlightthickness=2, highlightbackground=FG_COLOR)
        self.callbacks = callbacks
        self.draw()
        self.bind('<Button-1>', self._on_click)
        
    def draw(self):
        self.delete("all")
        
        # Button sections with dividers
        dividers = [72, 144, 216, 288, 360, 432, 504]
        for x in dividers:
            self.create_line(x, 5, x, 40, fill=FG_COLOR, width=1)
        
        # OFF
        self.create_text(36, 15, text="OFF", font=("Arial", 10, "bold"), fill=FG_COLOR)
        self._draw_3_leds(36, 32)
        
        # Recirc icon
        self._draw_recirc(108, 15)
        self._draw_3_leds(108, 32)
        
        # A/C
        self.create_text(180, 15, text="A/C", font=("Arial", 10, "bold"), fill=FG_COLOR)
        self._draw_3_leds(180, 32)
        
        # AUTO
        self.create_text(252, 15, text="AUTO", font=("Arial", 10, "bold"), fill=FG_COLOR)
        self._draw_3_leds(252, 32)
        
        # Hazard triangle
        self._draw_hazard(324, 22)
        
        # Front defrost
        self._draw_front_def_btn(396, 20)
        
        # Air direction with LED
        self._draw_air_dir_btn(468, 20)
        self.create_oval(495, 18, 503, 26, outline=FG_COLOR, width=1)
        
        # Rear defrost
        self._draw_rear_def_btn(540, 20)
        
    def _draw_3_leds(self, cx, cy):
        """Draw three LED indicators"""
        for offset in [-15, 0, 15]:
            self.create_oval(cx + offset - 4, cy - 4, cx + offset + 4, cy + 4,
                           outline=FG_COLOR, width=1)
            
    def _draw_recirc(self, cx, cy):
        """Recirculation icon - car with curved arrow"""
        # Simple car shape
        self.create_polygon(
            cx - 12, cy + 6,
            cx - 8, cy,
            cx - 2, cy - 4,
            cx + 6, cy - 4,
            cx + 10, cy,
            cx + 12, cy + 6,
            fill='', outline=FG_COLOR, width=1
        )
        # Curved arrow
        self.create_arc(cx - 18, cy - 12, cx - 2, cy + 4, start=120, extent=200,
                       style='arc', outline=FG_COLOR, width=1)
        self.create_polygon(cx - 18, cy - 2, cx - 13, cy - 6, cx - 13, cy + 2,
                          fill=FG_COLOR)
        
    def _draw_hazard(self, cx, cy):
        """Hazard triangle"""
        self.create_polygon(
            cx, cy - 14,
            cx - 16, cy + 10,
            cx + 16, cy + 10,
            fill='', outline=FG_COLOR, width=2
        )
        
    def _draw_front_def_btn(self, cx, cy):
        """Front defrost button icon"""
        # Windshield
        self.create_polygon(
            cx - 14, cy + 10,
            cx - 8, cy - 10,
            cx + 8, cy - 10,
            cx + 14, cy + 10,
            fill='', outline=FG_COLOR, width=1
        )
        # Lines
        for offset in [-5, 0, 5]:
            self.create_line(cx + offset, cy + 6, cx + offset, cy - 6, fill=FG_COLOR, width=1)
            
    def _draw_air_dir_btn(self, cx, cy):
        """Air direction button"""
        # Lines representing airflow
        self.create_line(cx - 15, cy - 5, cx - 5, cy - 5, fill=FG_COLOR, width=1)
        self.create_line(cx - 15, cy, cx - 5, cy, fill=FG_COLOR, width=1)
        self.create_line(cx - 15, cy + 5, cx - 5, cy + 5, fill=FG_COLOR, width=1)
        
        # Person icon
        self.create_oval(cx + 2, cy - 10, cx + 10, cy - 2, outline=FG_COLOR, width=1)
        self.create_line(cx + 6, cy - 2, cx + 6, cy + 10, fill=FG_COLOR, width=1)
        
    def _draw_rear_def_btn(self, cx, cy):
        """Rear defrost button"""
        self.create_rectangle(cx - 12, cy - 8, cx + 12, cy + 8, outline=FG_COLOR, width=1)
        for y_off in [-4, 0, 4]:
            self.create_line(cx - 9, cy + y_off, cx + 9, cy + y_off, fill=FG_COLOR, width=1)
            
    def _on_click(self, event):
        x = event.x
        if x < 72:
            self.callbacks.get('off', lambda: None)()
        elif x < 144:
            self.callbacks.get('recirc', lambda: None)()
        elif x < 216:
            self.callbacks.get('ac', lambda: None)()
        elif x < 288:
            self.callbacks.get('auto', lambda: None)()
        elif x < 360:
            self.callbacks.get('hazard', lambda: None)()
        elif x < 432:
            self.callbacks.get('front_def', lambda: None)()
        elif x < 504:
            self.callbacks.get('air_dir', lambda: None)()
        else:
            self.callbacks.get('rear_def', lambda: None)()


# =============================================================================
# Slider Panel - Exact Recreation  
# =============================================================================

class HVACSliders(tk.Canvas):
    """Slider control panel - exact recreation"""
    
    def __init__(self, parent, callbacks):
        super().__init__(parent, width=580, height=40, bg=BG_COLOR,
                        highlightthickness=2, highlightbackground=FG_COLOR)
        self.callbacks = callbacks
        self.draw()
        self.bind('<Button-1>', self._on_click)
        
    def draw(self):
        self.delete("all")
        
        # Inner border
        self.create_rectangle(4, 4, 576, 36, outline=FG_COLOR, width=1)
        
        # Vertical dividers (3 sections)
        self.create_line(193, 6, 193, 34, fill=FG_COLOR, width=1)
        self.create_line(387, 6, 387, 34, fill=FG_COLOR, width=1)
        
        # LEFT SECTION (Passenger temp)
        self._draw_temp_control(97, 20)
        
        # CENTER SECTION (Fan)
        self._draw_fan_control(290, 20)
        
        # RIGHT SECTION (Driver temp)
        self._draw_temp_control(483, 20)
        
    def _draw_temp_control(self, cx, cy):
        """Temperature slider control"""
        # LED left
        self.create_oval(cx - 85, cy - 4, cx - 77, cy + 4, outline=FG_COLOR, width=1)
        
        # Left arrow (triangle)
        self.create_polygon(
            cx - 70, cy,
            cx - 60, cy - 6,
            cx - 60, cy + 6,
            fill=FG_COLOR, outline=FG_COLOR
        )
        
        # Tick marks
        for i in range(12):
            tick_x = cx - 50 + i * 7
            if i == 5 or i == 6:
                # Taller center ticks
                self.create_line(tick_x, cy - 8, tick_x, cy + 8, fill=FG_COLOR, width=1)
            else:
                self.create_line(tick_x, cy - 5, tick_x, cy + 5, fill=FG_COLOR, width=1)
        
        # Seat icon in center (small)
        self._draw_small_seat(cx, cy + 2)
        
        # Right arrow
        self.create_polygon(
            cx + 70, cy,
            cx + 60, cy - 6,
            cx + 60, cy + 6,
            fill=FG_COLOR, outline=FG_COLOR
        )
        
        # LED right
        self.create_oval(cx + 77, cy - 4, cx + 85, cy + 4, outline=FG_COLOR, width=1)
        
    def _draw_small_seat(self, cx, cy):
        """Tiny seat icon"""
        # Back
        self.create_line(cx - 4, cy + 4, cx - 2, cy - 4, fill=FG_COLOR, width=1)
        self.create_line(cx - 2, cy - 4, cx + 3, cy - 4, fill=FG_COLOR, width=1)
        self.create_line(cx + 3, cy - 4, cx + 5, cy + 4, fill=FG_COLOR, width=1)
        # Bottom
        self.create_line(cx - 4, cy + 4, cx + 8, cy + 4, fill=FG_COLOR, width=1)
        
    def _draw_fan_control(self, cx, cy):
        """Fan slider control"""
        # LED left
        self.create_oval(cx - 85, cy - 4, cx - 77, cy + 4, outline=FG_COLOR, width=1)
        
        # Minus
        self.create_line(cx - 70, cy, cx - 55, cy, fill=FG_COLOR, width=2)
        
        # Tick marks
        for i in range(12):
            tick_x = cx - 45 + i * 6
            if i == 5 or i == 6:
                self.create_line(tick_x, cy - 8, tick_x, cy + 8, fill=FG_COLOR, width=1)
            else:
                self.create_line(tick_x, cy - 5, tick_x, cy + 5, fill=FG_COLOR, width=1)
        
        # Fan icon
        self._draw_small_fan(cx + 5, cy)
        
        # Plus
        self.create_line(cx + 55, cy, cx + 70, cy, fill=FG_COLOR, width=2)
        self.create_line(cx + 62, cy - 7, cx + 62, cy + 7, fill=FG_COLOR, width=2)
        
        # LED right
        self.create_oval(cx + 77, cy - 4, cx + 85, cy + 4, outline=FG_COLOR, width=1)
        
    def _draw_small_fan(self, cx, cy):
        """Tiny fan icon"""
        for angle in range(0, 360, 90):
            rad = math.radians(angle + 30)
            x = cx + 5 * math.cos(rad)
            y = cy + 5 * math.sin(rad)
            self.create_line(cx, cy, x, y, fill=FG_COLOR, width=1)
        self.create_oval(cx - 2, cy - 2, cx + 2, cy + 2, fill=FG_COLOR)
        
    def _on_click(self, event):
        x = event.x
        if x < 193:
            # Left section
            if x < 50:
                self.callbacks.get('pass_temp_down', lambda: None)()
            elif x > 140:
                self.callbacks.get('pass_temp_up', lambda: None)()
        elif x < 387:
            # Center section
            if x < 240:
                self.callbacks.get('fan_down', lambda: None)()
            elif x > 340:
                self.callbacks.get('fan_up', lambda: None)()
        else:
            # Right section
            if x < 430:
                self.callbacks.get('drv_temp_down', lambda: None)()
            elif x > 530:
                self.callbacks.get('drv_temp_up', lambda: None)()


# =============================================================================
# Main Application
# =============================================================================

class FordFGHVACApp(tk.Tk):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        self.title("Ford FG Falcon ICC - HVAC Display")
        self.configure(bg=PANEL_BG)
        self.resizable(False, False)
        
        self.state = HVACState()
        
        # Callbacks
        self.callbacks = {
            'off': self._on_off,
            'recirc': self._on_recirc,
            'ac': self._on_ac,
            'auto': self._on_auto,
            'hazard': lambda: print("[CAN] Hazard"),
            'front_def': self._on_front_def,
            'air_dir': lambda: print("[CAN] Air direction"),
            'rear_def': self._on_rear_def,
            'fan_up': self._on_fan_up,
            'fan_down': self._on_fan_down,
            'pass_temp_up': self._on_temp_up,
            'pass_temp_down': self._on_temp_down,
            'drv_temp_up': self._on_temp_up,
            'drv_temp_down': self._on_temp_down,
        }
        
        # Main container with padding
        container = tk.Frame(self, bg=PANEL_BG, padx=15, pady=10)
        container.pack()
        
        # Display panel
        self.display = HVACDisplay(container, self.state)
        self.display.pack(pady=(0, 8))
        
        # Button panel
        self.buttons = HVACButtons(container, self.callbacks)
        self.buttons.pack(pady=(0, 8))
        
        # Slider panel
        self.sliders = HVACSliders(container, self.callbacks)
        self.sliders.pack()
        
        # Start clock update
        self._update_clock()
        
    def _refresh(self):
        self.display.draw()
        
    def _on_off(self):
        print("[CAN TX] OFF pressed")
        
    def _on_recirc(self):
        print("[CAN TX] Recirc pressed")
        
    def _on_ac(self):
        self.state.ac_on = not self.state.ac_on
        print(f"[CAN TX] A/C: {'On' if self.state.ac_on else 'Off'}")
        self._refresh()
        
    def _on_auto(self):
        self.state.auto_mode = not self.state.auto_mode
        print(f"[CAN TX] Auto: {'On' if self.state.auto_mode else 'Off'}")
        self._refresh()
        
    def _on_front_def(self):
        self.state.front_defrost = not self.state.front_defrost
        print(f"[CAN TX] Front Defrost: {'On' if self.state.front_defrost else 'Off'}")
        self._refresh()
        
    def _on_rear_def(self):
        self.state.rear_defrost = not self.state.rear_defrost
        print(f"[CAN TX] Rear Defrost: {'On' if self.state.rear_defrost else 'Off'}")
        self._refresh()
        
    def _on_fan_up(self):
        if self.state.fan_speed < 8:
            self.state.fan_speed += 1
            print(f"[CAN TX] Fan: {self.state.fan_speed}")
            self._refresh()
            
    def _on_fan_down(self):
        if self.state.fan_speed > 0:
            self.state.fan_speed -= 1
            print(f"[CAN TX] Fan: {self.state.fan_speed}")
            self._refresh()
            
    def _on_temp_up(self):
        if self.state.set_temp < 32:
            self.state.set_temp += 0.5
            print(f"[CAN TX] Temp: {self.state.set_temp}°C")
            self._refresh()
            
    def _on_temp_down(self):
        if self.state.set_temp > 16:
            self.state.set_temp -= 0.5
            print(f"[CAN TX] Temp: {self.state.set_temp}°C")
            self._refresh()
            
    def _update_clock(self):
        now = datetime.now()
        self.state.hours = now.hour
        self.state.minutes = now.minute
        self._refresh()
        self.after(1000, self._update_clock)


# =============================================================================
# Entry Point
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Ford FG Falcon ICC HVAC Display")
    print("Pixel-Perfect Exact Recreation")
    print("Jakka351")
    print("=" * 60)
    
    app = FordFGHVACApp()
    app.mainloop()
