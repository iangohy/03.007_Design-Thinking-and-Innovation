# 03.007 Design Thinking and Innovation
## Recyclace
A smart recycling bin with moveable compartments and a barcode scanning feature, enhancing the ease of recycling and recycling efficiency.

## Testing mode
For testing without barcode scanner, set `$recyclace=testing`

## Hardware Wiring
### Raspberrypi Pinout
![Rpi GPIO Pinout](https://www.raspberrypi-spy.co.uk/wp-content/uploads/2012/06/Raspberry-Pi-GPIO-Header-with-Photo.png)
### Pololu VL53L0X TOF sensor
| Raspberry Pi | Sensor |
| ------------ | ------ |
| 3.3V | VIN |
| GND | GND |
| SCL | SCL |
| SDA | SDA |

### Stepper Motor Driver TB6600
| Raspberry Pi                | TB6600 |
| --------------------------- | ------ |
| GPIO 17                     | ENA-   |
| 3.3V                        | ENA+   |
| GPIO 27                     | DIR-   |
| 3.3V                        | DIR+   |
| GPIO 22                     | PUL-   |
| 3.3V                        | PUL+   |
| - (Connect to motor yellow) | B-     |
| - (Connect to motor red)    | B+     |
| - (Connect to motor green)  | A-     |
| - (Connect to motor blue)   | A+     |
| 12V Power Supply            | VCC    |
| GND                         | GND    |

###  LED Strips
| Raspberry Pi                | LED |
| --------------------------- | ------ |
| GPIO 16                     | RED- (via 10k resistor) |
| GPIO 26                     | BLUE- (via 10k resistor) |
| GPIO 19                     | YELLOW- (via 10k resistor) |
| GPIO 20                     | GREEN- (via 10k resistor) |

### Keylock Switch
| Raspberry Pi                | Switch |
| --------------------------- | ------ |
| GPIO 14                     | Terminal A |
| 3.3V                        | Terminal B |

### VL53L0X Sensor
| Raspberry Pi                | VL53L0X |
| --------------------------- | ------ |
| 3.3V                        | VIN |
| GND                         | GND |
| SDA                         | SDA |
| SCL                         | SCL |

## Files

data.csv - Barcode database of items

## VL53L0X Sensor Testing
`/VL53L0X_1.0.2` - API library downloaded from ST Electronics
`/VL53L0X_rasp` - API port for Raspberry Pi (Initialise using `git submodule init` and `git submodule update`)

## Additional Info
To find food product barcodes: https://world.openfoodfacts.org/
