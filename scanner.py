import time

def scan_i2c(i2c) -> None:
    while not i2c.try_lock():
        pass

    try:
        print(
            "I2C addresses found:",
            [hex(device_address) for device_address in i2c.scan()],
        )
        time.sleep(0.2)

    finally: 
        i2c.unlock()
        return
