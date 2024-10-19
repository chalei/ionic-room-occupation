import ujson
import machine
import time
import ubinascii

# Initialize UART with the specified TX and RX pins
uart1 = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rx=machine.Pin(1))  # Replace with actual pins

while True:
    if uart1.any():  # Check if there is data available
        data = uart1.read()  # Read the binary data from Serial
        try:
            # Extract the text part (e.g., Intruder alert)
            if b'Intruder alert' in data:
                alert_msg = "Intruder alert"

            # Extract the binary part (assuming image data is encoded after the alert)
            binary_start = data.find(b'/9j/')
            if binary_start != -1:
                image_data = data[binary_start:]  # Extract image binary data (JPEG format)
                encoded_image = ubinascii.b2a_base64(image_data).decode('utf-8')  # Base64 encode the binary

                # Build the JSON object
                json_obj = {
                    "alert": alert_msg,
                    "image": encoded_image
                }

                # Convert to JSON string
                json_string = ujson.dumps(json_obj)
                print(json_string)  # Print the resulting JSON

        except Exception as e:
            print("Error processing data:", e)
