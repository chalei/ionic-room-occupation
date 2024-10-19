from machine import Pin, UART
import time

# Set up the UART port (adjust the TX/RX pins as per your board)
uart = UART(0, baudrate=115200, tx=0, rx=1, timeout=1000)  # Change TX/RX pins accordingly

class LEDModule:
    """This will represent our LED"""
    
    def __init__(self, pinNumber):
        self.pinNumber = pinNumber
        self.led_pin = Pin(self.pinNumber, Pin.OUT)
        
    def get_value(self):
        while True:            
            if uart.any():
                print("something's detected")
                self.led_pin.value(1)
            time.sleep(0.5)
            return self.led_pin.value()
    
    def toggle(self):
        self.led_pin.value(not self.get_value())
    
    