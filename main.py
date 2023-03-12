import threading
import time
import keyboard
import pygame


class CoolDownChecker:
    def __init__(self, gt_hotkey, alert_cd, default_wait_time=1, sound_path="gt_sound.mp3"):
        self.hotkey = gt_hotkey
        self.alert_cd = alert_cd
        self.default_wait_time = default_wait_time

        self.t_last_gt = -self.alert_cd

        pygame.init()
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound(sound_path)
        self.sound.set_volume(1)  # Now plays at 90% of full volume.

    def run(self):
        thread = threading.Thread(target=self.check_gt_cd)
        thread.start()

        keyboard.hook(self.on_gt)
        keyboard.wait()

    def on_gt(self, e):
        if e.name == self.hotkey and e.event_type == "down":
            self.t_last_gt = time.time()

    def check_gt_cd(self):
        while True:
            t_now = time.time()

            wait_time = self.default_wait_time
            if t_now - self.t_last_gt >= self.alert_cd:
                self.sound.play()
            else:
                wait_time = self.alert_cd - (t_now - self.t_last_gt)

            time.sleep(wait_time)


if __name__ == "__main__":
    CoolDownChecker(gt_hotkey='5', alert_cd=75).run()
