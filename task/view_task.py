from task.task import Task

"""
    Short cut for viewing w/o recording files:
    - disarm singla (to ensure consistent state)
    - disable filewriter 
    - set nimages to very high number
    - arm
    - trigger
"""


class ViewTask(Task):
    def __init__(self, control_worker):
        super().__init__(control_worker, "View")

    def run(self):
        # Disable writing and setup for viewing
        self.control.detector.send_command("disarm")
        self.control.detector.set_config("mode", "disabled", "filewriter")
        frame_time = self.control.detector.get_config("frame_time", "detector")
        self.control.detector.set_config("nimages", int(86400.0 / frame_time), "detector")
        self.control.arm()
        self.control.detector.send_command("trigger")
