from microdot import Microdot
from machine import Pin,WIZNET_PIO_SPI
import network
import time

#W5x00 chip init
def w5x00_init():
    spi = WIZNET_PIO_SPI(baudrate=31_250_000, mosi=Pin(23),miso=Pin(22),sck=Pin(21)) #W55RP20 PIO_SPI
    nic = network.WIZNET5K(spi,Pin(20),Pin(25)) #spi,cs,reset pin
    nic.active(True)
    
#None DHCP
    nic.ifconfig(('192.168.0.180','255.255.255.0','192.168.0.1','8.8.8.8'))
    
#DHCP
    #nic.ifconfig('dhcp')
    print('IP address :', nic.ifconfig())
    
    while not nic.isconnected():
        time.sleep(1)
        print(nic.regs())

w5x00_init()
app = Microdot()

html = '''<!DOCTYPE html>
<html>
    <head>
        <title>Microdot Example Page</title>
        <meta charset="UTF-8">
    </head>
    <body>
        <div>
            <h1>Microdot Example Page</h1>
            <p>Hello from Microdot!</p>
            <p><a href="/shutdown">Click to shutdown the server</a></p>
        </div>
    </body>
</html>
'''


@app.route('/')
async def hello(request):
    return html, 200, {'Content-Type': 'text/html'}


@app.route('/shutdown')
async def shutdown(request):
    request.app.shutdown()
    return 'The server is shutting down...'


app.run(debug=True)