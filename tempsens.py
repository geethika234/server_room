import time
import pickle

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008


# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
# The read_adc function will get the value of the channel 0
value = mcp.read_adc(0)
temp=(value*28)/100
print(temp)
f= open("/path/to/folder/server.txt","wb")
pickle.dump(temp, f)
f.close()
time.sleep(0.5)
