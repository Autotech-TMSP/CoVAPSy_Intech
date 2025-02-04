import smbus #type: ignore #ignore the module could not be resolved error because it is a linux only module
import time

# Create an SMBus instance
bus = smbus.SMBus(1)  # 1 indicates /dev/i2c-1

# I2C address of the slave
SLAVE_ADDRESS = 0x08

def write_data(data):
    # Convert string to list of ASCII values
    data_list = [ord(char) for char in data]
    bus.write_i2c_block_data(SLAVE_ADDRESS, 0, data_list)

def read_data(length):
    # Read a block of data from the slave
    data = bus.read_i2c_block_data(SLAVE_ADDRESS, 0, length)
    # Convert list of ASCII values to string
    return ''.join(chr(byte) for byte in data)

if __name__ == "__main__":
    try:
        # Send data to the slave
        write_data("Hello Slave!")
        time.sleep(1)  # Wait for the slave to process the data

        # Request data from the slave
        received = read_data(13)  # Adjust length as needed
        print("Received from slave:", received)

    except Exception as e:
        print("Error:", e)