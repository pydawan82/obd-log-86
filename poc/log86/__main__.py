import sys
import time
import argparse as ap
import collections.abc as cabc
import itertools as itt

import obd
import obd.commands as obdc

class Args(ap.Namespace):
    port: str | None
    repeat: int | None
    command: cabc.Callable[['Args'], None]

def get_parser() -> ap.ArgumentParser:
    parser = ap.ArgumentParser(prog='log86')
    subparsers = parser.add_subparsers(required=True)
    parser.add_argument('-p', '--port')

    parser_show = subparsers.add_parser('show')
    parser_show.set_defaults(command=show)
    parser_show.add_argument('-n', type=int, dest='repeat')    
    
    parser_bandwidth = subparsers.add_parser('bandwidth')
    parser_bandwidth.set_defaults(command=bandwidth)
    parser_bandwidth.add_argument('-c', type=int, dest='count', default=100)

    return parser

def parse_args() -> Args:
    parser = get_parser()
    result = parser.parse_args(sys.argv[1:], namespace=Args())

    return result

def get_port(args: Args) -> str:
    port = args.port
    
    if not port:
        ports = obd.scan_serial()
        if not ports:
            raise ValueError('could not find any candidate serial port')
        port = ports[0]

    return port

def get_obd(args: Args) -> obd.OBD:
    my_obd = obd.OBD(get_port(args))

    if not my_obd.is_connected():
        raise Exception(f'connection failed: {my_obd.status()}')

    return my_obd

def repeat(count: int | None= None) -> cabc.Iterable[int]:
    if count == None:
        return itt.count()
    else:
        return range(count)

def format_cols(names: cabc.Iterable[str], widths: cabc.Iterable[int]) -> str:
    return '  '.join(f'{name:{col_width}s}' for (name, col_width) in zip(names, widths))

def show(args: Args):
    my_obd = get_obd(args)

    obd_commands = [
        ('RPM', obdc.RPM),
        ('SPEED', obdc.SPEED),
        ('THROTTLE', obdc.THROTTLE_POS),
        ('COOLANT TEMPERATURE', obdc.COOLANT_TEMP),
        ('OIL TEMPERATURE', obdc.OIL_TEMP),
        ('FUEL RATE', obdc.FUEL_RATE)
    ]

    col_widths = [max(8, len(name)) for (name, _) in obd_commands]
    title = format_cols((x[0] for x in obd_commands), col_widths)
    print(title)

    try:
        for _ in repeat(args.repeat):
            now = time.perf_counter()
            values = [
                    my_obd.query(command)
                    for _, command in obd_commands
            ]
            row = '  '.join(f'{value.value.magnitude:{width}d}' for (value, width) in zip(values, col_widths))
            print(row)
            then = time.perf_counter()
            time.sleep(max(0., 1. + (now - then)))
    except KeyboardInterrupt:
        pass

def bandwidth(args: Args):
    my_obd = get_obd(args)
    
    start = time.perf_counter_ns()

    for _ in range(args.count):
        my_obd.query(obdc.RPM)

    end = time.perf_counter_ns()

    duration = end - start
    duration_s = duration / 1e9
    query_bandwidth =  args.count / duration_s

    print(f'Performed {args.count} query in {duration/1e6:d}ms; Average {query_bandwidth} query/s')

def main():
    args = parse_args()

    try:
        args.command(args)
    except Exception as e:
        print(e, file=sys.stderr)

if __name__ == '__main__':
    main()
