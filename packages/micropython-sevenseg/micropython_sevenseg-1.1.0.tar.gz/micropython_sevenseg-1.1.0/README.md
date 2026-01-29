# 🔢 SevenSeg – MicroPython Library for 1-Digit 7-Segment Display

A lightweight, easy-to-use **MicroPython library** to control **single-digit 7-segment displays** (common cathode or common anode) on boards like **ESP32**, **ESP8266**, and **Raspberry Pi Pico 2 W**.

<p align="center">
  <a href="https://micropython.org/"><img src="https://img.shields.io/badge/MicroPython-✓-green?logo=micropython&logoColor=white" alt="MicroPython"></a>
  <a href="https://www.espressif.com/en/products/socs/esp32"><img src="https://img.shields.io/badge/ESP32-Supported-orange?logo=espressif&logoColor=white" alt="ESP32"></a>
  <a href="https://www.espressif.com/en/products/socs/esp8266"><img src="https://img.shields.io/badge/ESP8266-Supported-red?logo=espressif&logoColor=white" alt="ESP8266"></a>
  <a href="https://www.raspberrypi.com/products/raspberry-pi-pico/"><img src="https://img.shields.io/badge/Raspberry%20Pi%20Pico%20 2 W-Compatible-darkgreen?logo=raspberrypi&logoColor=white" alt="Pico 2 W"></a>
  <a href="https://github.com/kritishmohapatra/sevenseg-micropython/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?logo=open-source-initiative&logoColor=white" alt="License"></a>
  
</p>


---

## 🚀 Features
- Supports **both Common Cathode & Common Anode** types  
- Optional **decimal point (dp)** control  
- Simple API: `show()`, `clear()`, `dot()`  
- Works on multiple MicroPython boards  
- Clean, modular design for beginners & embedded developers  

---

## ⚙️ Installation

Copy the `sevenseg.py` file to your device using **Thonny**, **ampy**, or **rshell**.

Or clone this repo:
```bash
git clone https://github.com/kritishmohapatra/SevenSeg.git
# Copy to the root directory of your MicroPython board
sevenseg.py → /
```

## 🧠 Pin Diagram (Typical)
     ---a---
    |       |
    f       b
    |       |
     ---g---
    |       |
    e       c
    |       |
     ---d---   ● dp

## 🧪 Board Examples

| Board | File | Description |
|--------|------|-------------|
| ESP32 | `examples/esp32_basic_counter_example.py` | Demo on ESP32 with GPIO 23–17 |
| ESP8266 | `examples/esp8266_basic_counter_example.py` | Demo on NodeMCU (D1–D8 pins) |
| Raspberry Pi Pico 2 W | `examples/rpi_pico_2_w_counter_example.py` | Demo using GP0–GP7 |

## 🧩 Library API

| Function | Description |
|-----------|--------------|
| `show(num)` | Display a number (0–9) |
| `clear()` | Turn off all segments |
| `dot(on=True)` | Turn the decimal point on/off |
| `common_anode` | Set `True` for common-anode displays |
## 📦 Folder Structure
    SevenSeg/
        ├── sevenseg.py
        ├── __init__.py
    examples/
        ├── sevenseg_esp32_demo.py
        ├── sevenseg_esp8266_demo.py
        └── sevenseg_pico2w_demo.py
    setup.py
    LICENSE
    README.md

## 📜 License

This project is licensed under the **MIT License**.  
© 2025 Kritish Mohapatra – Open Source for MicroPython Community 💡

## 🔄 What's New in v1.1.0

- Optimized segment control logic using XOR operation
- Correct decimal point (DP) behavior for common anode and cathode displays
- Cleaner and faster pin value handling
- Community-reviewed improvements


## ❤️ Contribute

Pull requests are welcome!  
If you find a bug or want to suggest an improvement, feel free to open an issue.

## 🌐 Author

**Kritish Mohapatra**  
🔗 [GitHub](https://github.com/kritishmohapatra)  
📧 kritishmohapatra06norisk@gmail.com  

✨ *Made with passion for Embedded Systems and MicroPython learners.*