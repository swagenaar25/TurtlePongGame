import time


class Throttle:
    def __init__(self, fps: int):
        self.prev_time = 0
        self.fps = fps
        self.frame_times = []
        self.iters = 0

    def limit(self):
        self.iters += 1
        seconds_per_frame = 1/self.fps
        now = time.time()
        diff_time = abs(now-self.prev_time)
        sleep_time = max(seconds_per_frame-diff_time, 0)
        if sleep_time > 0:
            time.sleep(sleep_time)
        """if self.prev_time != 0 and self.iters > 100:
            self.frame_times.append(max(diff_time, sleep_time))
        if len(self.frame_times) % 100 == 99:
            print(f"Fps: {len(self.frame_times)/sum(self.frame_times)}")
            self.frame_times.clear()"""
        self.prev_time = time.time()
