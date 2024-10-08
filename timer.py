import threading
import time
from settings import *

class CountdownTimer:
    def __init__(self, countdown_minutes=10):
        self.set_countdown_minutes(countdown_minutes)
        self.start_time = None
        self.pause_time = None
        self.total_paused_duration = 0
        self.running = False
        self.paused = False
		
    def start(self):
        if self.running:
            return
        if self.paused:
            self.total_paused_duration += time.time() - self.pause_time
            self.paused = False
        else:
            self.start_time = time.time()
        self.running = True

    def pause(self):
        if not self.running or self.paused:
            return
        self.pause_time = time.time()
        self.remaining_seconds -= (self.pause_time - self.start_time - self.total_paused_duration)
        self.paused = True
        self.running = False

    def stop(self):
        if not self.running:
            return None
        if self.paused:
            self.total_paused_duration += time.time() - self.pause_time
            self.paused = False
        elapsed_time = self.total_seconds - (time.time() - self.start_time - self.total_paused_duration)
        self.running = False
        self.start_time = None
        self.pause_time = None
        self.total_paused_duration = 0
        return max(elapsed_time, 0)  # Return 0 if time is up

    def get_remaining_time(self):
        if self.running:
            return max(self.total_seconds - (time.time() - self.start_time - self.total_paused_duration), 0)
        return self.remaining_seconds
	
    def set_countdown_minutes(self, countdown_minutes):
        self.total_seconds = countdown_minutes * 60
        self.remaining_seconds = self.total_seconds
        self.start_time = None
        self.pause_time = None
        self.total_paused_duration = 0
        self.running = False
        self.paused = False

button_press_event = threading.Event()		

def run_timers_with_interval(num_iterations, countdown_minutes, interval_seconds, start_button_press_callback):
	for i in range(num_iterations):
		# Wait for button before starting timer
		print(f"Waiting for button press to start Timer {i+1}")
		button_press_event.wait()
		button_press_event.clear()
		
		# Start the countdown timer
		timer = CountdownTimer(countdown_minutes)
		timer.start()
		print(f"Timer {i+1} initialised")
		
		# Run the timer until it stops
		while timer.get_remaining_time() > 0:
			remaining_time = timer.get_remaining_time()
			minutes, seconds = divmod(int(remaining_time), 60)
			time.sleep(1)
			print(remaining_time)
			state.display_time = remaining_time
		
		# Stop the timer
		timer.stop()
		state.display_time = 0
		print(f"Timer {i+1} completed")
		
		# If there are more iterations left then run the break timer
		if i < num_iterations - 1:
			for remaining_interval in range(interval_seconds, 0, -1):
				state.display_time = remaining_interval
				minutes, seconds = divmod(remaining_interval, 60)
				time.sleep(1)