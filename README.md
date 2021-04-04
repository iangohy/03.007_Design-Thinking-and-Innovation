# 03.007 Design Thinking and Innovation
## Recyclace
A smart recycling bin with moveable compartments and a barcode scanning feature, enhancing the ease of recycling and recycling efficiency.

## Hardware Wiring
### Pololu VL53L0X TOF sensor
| Raspberry Pi | Sensor |
| ------------ | ------ |
| 3.3V | VIN |
| GND | GND |
| SCL | SCL |
| SDA | SDA |


## Files
data.csv - Barcode database of items

## VL53L0X Sensor Testing
`/VL53L0X_1.0.2` - API library downloaded from ST Electronics
`/VL53L0X_rasp` - API port for Raspberry Pi (Initialise using `git submodule init` and `git submodule update`)

## Additional Info
To find food product barcodes: https://world.openfoodfacts.org/
