import asyncio
import time
import datetime
from utils.clock import Clock
from utils.screen import Screen
from utils.tools import get_time


async def main(loop):
    await screen.set_up()
    await asyncio.wait([read_screen()])


def test(_screen):
    while True:
        print("True")
        hour = datetime.datetime.now().strftime('%H:%M:%S')
        hourstr = '"%s"' % hour
        print(hour)
        # hourstrb = bytes(hourstr, 'utf-8')
        _screen.set_time(hourstr)
        time.sleep(2)

async def read_screen():
    screen.menu()

    while True:
        print("icit")
        test(screen)
        message = await screen.reader.read(9)
        print(message)
        # hour = datetime.datetime.now().strftime('%H:%M:%S')
        # hourstr = '"%s"' % hour
        # hourstrb = bytes(hourstr, 'utf-8')
        # screen.writer.write(b't15.txt=' + hourstrb + b'\xff\xff\xff')


if __name__ == "__main__":
    global screen, clock

    screen = Screen("/dev/ttyUSB2")
    clock = Clock()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
