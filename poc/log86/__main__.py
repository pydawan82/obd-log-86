import sys, os

import obd
import obd.commands as obdc
import time

def main():
    ports = obd.scan_serial()

    try:
        # port = ports[0]
        port = '/dev/rfcomm0' 
        print('selected port:', port)
        myobd = obd.OBD(port, fast=False)
        print('connected to obd:', port)
        print('connection status: ', myobd.status())
    except Exception as e:
        myobd = None
        print('failed to connect to obd:', e, file=sys.stderr)
        raise

    print('testing some simple commands')

    commands = [
        'RPM',
        'SPEED',
        'ACCELERATOR_POS_D',
    ]

    try:
        while True:
            for command_name in commands:
                print('testing', command_name)
                command = getattr(obdc, command_name)
                result = myobd.query(command)
                print(result.value)
            time.sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
