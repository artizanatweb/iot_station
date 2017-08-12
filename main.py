import sys
import micropython
from Board import Board as EspBoard

micropython.alloc_emergency_exception_buf(100)


if __name__ == '__main__':
    board = EspBoard()
    try:
        board.setup()
        board.loop()
    except:
        print("Can't run board loop!")
        sys.exit(1)

