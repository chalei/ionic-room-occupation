from microdot_asyncio import Microdot, Response, send_file
from microdot_utemplate import render_template
from led_module import LEDModule
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
Response.default_content_type = 'text/html'

# Our LED Module
led_module = LEDModule(19)


@app.route('/')
async def index(request):
    return render_template('index.html', led_value=led_module.get_value())


@app.route('/toggle')
async def toggle_led(request):
    print("Receive Toggle Request!")
    led_module.toggle()
    return "OK"


@app.route('/shutdown')
async def shutdown(request):
    request.app.shutdown()
    return 'The server is shutting down...'


@app.route('/static/<path:path>')
def static(request, path):
    if '..' in path:
        # directory traversal is not allowed
        return 'Not found', 404
    return send_file('static/' + path)

app.run()
