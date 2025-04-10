from typing import Optional
import socket
import threading
from time import sleep, time
from random import random

class ControlCenter:
    """Class for managing digital flagpoles."""

    def __init__(self, ips: list[str], time: Optional[float] = 5):

        self.ips = ips

        self.flagpoles = {}
        self.ip_threads = {}

        for ip in self.ips:
            
            flagpole = DigitalFlagpole(ip)
            self.flagpoles[ip] = flagpole

            thread = threading.Thread(target=flagpole.start)
            self.ip_threads[ip] = thread
            thread.start()

        self.max_time = time


    def start(self):
        """Start the timer and listen to flagpole changes."""
        try:

            self.starting_time = time()

            while (time() - self.starting_time) < self.max_time:
                sleep(1) # 100 ms
                print(f"Time Elapsed: {time() - self.starting_time:.1f} seconds")

        except KeyboardInterrupt:
            pass

        total_red_time: float = 0
        total_blue_time: float = 0

        for ip, flagpole in self.flagpoles.items():
            flagpole.stop()
            total_red_time += flagpole.red_time
            total_blue_time += flagpole.blue_time

        for ip, thread in self.ip_threads.items():
            thread.join()

        print(f"Total red time: {total_red_time:.2f} seconds")
        print(f"Total blue time: {total_blue_time:.2f} seconds")
        
        if total_red_time > total_blue_time:
            print("Red team won!")
        else:
            print("Blue team won!")


class DigitalFlagpole:
    """Class for communicating with flagpoles."""

    def __init__(self, ip: str):
        self.ip = ip
        self.event = threading.Event()
        self.red_time = 0
        self.blue_time = 0
        self.last_button_press = 0

    def start(self):
        """Start listening to flagpole messages."""
        self.event.set()
        last_time = time()

        while self.event.is_set():
            sleep(1)
            current_time = time()

            # Add time for whichever team held the flagpole
            if self.last_button_press == 0:
                self.red_time += current_time - last_time
            else:
                self.blue_time += current_time - last_time

            # Assign current team holder of the flagpole
            if random() < 0.25:
                self.last_button_press = 1 - self.last_button_press
            
            last_time = current_time

    def stop(self):
        """Stop receiving messages from flagpole."""
        self.event.clear()


if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(
        prog = 'Command & Control',
        description = 'Manages digital flagpoles'
    )
    
    parser.add_argument('ipfile', type = str, help='The file containing newline-separated ip addresses of flagpoles.')
    parser.add_argument('--time', default = 5, type = float, help='Session time in minutes.')
    
    args = parser.parse_args()

    ips = []
    with open(args.ipfile, 'r') as f:
        for line in f.readlines():
            ips.append(line.strip())

    controller = ControlCenter(time=60 * args.time, ips=ips)
    controller.start()