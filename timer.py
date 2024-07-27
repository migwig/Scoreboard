import time

class CountdownTimer:
    def __init__(self, countdown_minutes=10):
        self.set_countdown_minutes(countdown_minutes)
        #self.total_seconds = countdown_minutes * 60
        #self.remaining_seconds = self.total_seconds
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
"""
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
        self.paused = True

    def stop(self):
        if not self.running:
            return None
        if self.paused:
            self.total_paused_duration += time.time() - self.pause_time
            self.paused = False
        elapsed_time = self.total_seconds - (time.time() - self.start_time - self.total_paused_duration)
        self.running = False
        self.start_time = None
        self.total_paused_duration = 0
        return max(elapsed_time, 0)  # Return 0 if time is up

    def get_remaining_time(self):
        if self.running:
            return max(self.total_seconds - (time.time() - self.start_time - self.total_paused_duration), 0)
        return self.remaining_seconds
"""