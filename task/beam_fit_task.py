import time

from task.task import Task


class BeamFitTask(Task):
    """
        change IL focus and stigmatism to create a maximally round and condensed beam shape
    """

    def __init__(self, control_worker):
        super().__init__(control_worker, "BeamFit")
        self.duration_s = 30
        self.estimated_duration_s = self.duration_s + 0.1

    def run(self):
        # for x in range(0x8400,0x8700,20):
        #    for y in range(0x8400,0x8700,20):
        #        time.sleep(0.2)
        #        print(x,y, self.control.stream_receiver.fit)
        _, il1_guess1 = self.sweep_il1_linear(21500, 22100, 5)
        self.tem_command("lens", "SetILFocus", [il1_guess1])

        _, il1_guess2 = self.sweep_il1_linear(il1_guess1 - 20, il1_guess1 + 20, 1)
        self.tem_command("lens", "SetILFocus", [il1_guess2])

    def move_to_stigm(self, stigm_x, stigm_y):
        self.tem_command("defl", "SetILs", [stigm_x, stigm_y])

    def sweep_il1_linear(self, lower, upper, step, wait_time_s=0.2):
        max_amplitude = 0
        max_il1value = None
        for il1_value in range(lower, upper, step):
            self.tem_command("lens", "SetILFocus", [il1_value])
            time.sleep(wait_time_s)
            amplitude = self.control.stream_receiver.fit[0]
            if max_amplitude < amplitude:
                max_amplitude = amplitude
                max_il1value = il1_value
        return max_amplitude, max_il1value
