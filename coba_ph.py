import spidev
import time

# SPI setup
spi = spidev.SpiDev()
spi.open(0, 0)  # Open bus 0, device 0 (CE0)
spi.max_speed_hz = 1350000  # Speed for MCP3008

# Function to read from MCP3008
def read_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

# Function to convert MCP3008 data to voltage
def convert_to_voltage(data, vref=3.3):
    return (data * vref) / 1023.0

# Main loop
try:
    while True:
        ph_channel = 0  # Using CH0 for pH sensor
        ph_value = read_channel(ph_channel)
        ph_voltage = convert_to_voltage(ph_value)
        print(f"Raw pH Value: {ph_value}, Voltage: {ph_voltage:.2f}V")
        
        # Convert voltage to pH (depending on the calibration equation)
        # Example: Assuming 3V corresponds to pH 7 (neutral), adjust as per your calibration
        ph = 7 + (ph_voltage - 2.5) * 3.5  # Adjust based on sensor specifics
        print(f"pH Value: {ph:.2f}")
        
        time.sleep(1)

except KeyboardInterrupt:
    spi.close()
    print("Program stopped.")
