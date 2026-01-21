import config

class GameClock:
    def __init__(self):
        # Time state
        self.time = 6.0
        self.day = 1
        self.month = 1
        self.year = 1
        self.phase = self.get_phases()

        # Control
        self.paused = False
        self.time_scale = 1.0
        self.skipping_night = False

        # Callbacks
        self.on_phase_change = []
        self.on_new_day = []

        # Timekeeping for hour transition
        self.seconds_accumulated = 0
        self.seconds_per_hour = config.seconds_per_hour

        # Cached values
        self.gamedt = 0

    def update(self, dt):
        "Updates game clock and returns scaled dt for fast-forwarding"
        if self.paused:
            self.gamedt = 0.0
            return 0.0
        
        # Scale time
        scaled_dt = dt * self.time_scale
        self.gamedt = scaled_dt

        # Acumulate time
        self.seconds_accumulated += scaled_dt

        while self.seconds_accumulated >= self.seconds_per_hour:
            self.seconds_accumulated -= self.seconds_per_hour
            self.increment_hour()

        return scaled_dt
    
    def increment_hour(self):
        old_phase = self.phase
        self.time += 1.0

        # Day rollover
        if self.time >= 24.0:
            self.time = 0.0
            self.increment_day()

        self.phase = self.get_phases()
        if self.phase != old_phase:
            self._notify_phase_change(old_phase, self.phase)

            if self.skipping_night and self.phase == "dawn":
                self.stop_skip_night()

        # for callback in self.on_hour_change:
        #     callback(self.time)

    def increment_day(self):
        self.day += 1
        
        if self.day > 30:
            self.day = 1
            self.increment_month()
        
        for callback in self.on_new_day:
            callback(self.day, self.month, self.year)

    def increment_month(self):
        self.month += 1

        if self.month > 12:
            self.month = 1
            self.increment_year()

    def increment_year(self):
        self.year += 1

    def get_phases(self):
        hour = self.time
        if 5.0 <= hour < 7.0:
            return "dawn"
        elif 7.0 <= hour < 18.0:
            return "day"
        elif 18.0 <= hour < 20:
            return "dusk"
        else:
            return "night"
        
    def register_phase_listener(self, callback):
        "To be called when day phase changes. Parameters: (old_phase, new_phase)"
        self.on_phase_change.append(callback)

    def _notify_phase_change(self, old_phase, new_phase):
        for callback in self.on_phase_change:
            callback(old_phase, new_phase)

# --- Public control methods ---

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    def toggle_pause(self):
        self.paused= not self.paused
    
    def start_skip_night(self):
        self.skipping_night = True
        self.time_scale = 50.0

    def stop_skip_night(self):
        self.skipping_night = False
        self.time_scale = 1.0

# --- Public getters ---
    def get_dt(self):
        return self.gamedt
    
    def get_phase(self):
        return self.phase
    
    def get_formatted_time(self):
        "Return in format hh:00 AM/PM"
        hour = int(self.time)
        display_hour = hour % 12
        if display_hour == 0:
            display_hour = 12

        period = "AM" if hour < 12 else "PM"

        return f"{display_hour}:00 {period}"
    
    def get_formatted_date(self):
        return f"Day {self.day}, Month{self.month}, Year{self.year}"