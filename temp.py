def speed_with_ramp(self, **kwargs) -> float:
    """
    Calculate the speed control for the next cycle considering ramp-up and ramp-down.

    Args:
        v_now: Current speed input.
        v_cmd: Speed command.
        dt: Time of speed input.
        pid_offset: PID offset (predict point - reference point, (-) hb at front (+) hb at back).
        ramp_up_time: Drive up ramp.
        ramp_down_time: Drive down ramp.
        max_spd_per: Percentage 0.0 - 1.0.

    Returns:
        Speed percentage control for the next cycle.
    """
    v_now = kwargs.get('v_now', 0.0)
    v_cmd = kwargs.get('v_cmd', 0.0)
    ramp_up_time = kwargs.get('ramp_up_time', 6.0)
    ramp_down_time = kwargs.get('ramp_down_time', 6.0)
    max_spd_per = kwargs.get('max_spd_per', 0.9)
    pid_offset = kwargs.get('pid_offset', 0)
    dt = kwargs.get('dt', 0) * 2

    ramp_up = 100 * max_spd_per / ramp_up_time
    ramp_down = -100 * max_spd_per / ramp_down_time

    if v_cmd >= 0:
        ramp = ramp_up if v_cmd > self.speed_interior else ramp_down
    else:
        ramp = ramp_down if v_cmd < self.speed_interior else ramp_up

    if v_cmd != self.speed_interior or (v_cmd == 0 and self.speed_interior == 0):
        self.speed_interior += ramp * dt

    if int(self.speed_interior) == 0:
        self.set_spd = [0]
        self.smooth_spd = [0]

    if dt == 0:
        speed_out = self.speed_interior
        self.set_spd = [0]
    else:
        speed_offset = (pid_offset / dt) / (180 / 60)
        self.set_spd.append(self.speed_interior + speed_offset)
        self.smooth_spd = self.moving_average(self.set_spd, 10)
        max_spd_offset = self.speed_interior + (100 / ramp_up_time * dt)
        min_spd_offset = self.speed_interior - (100 / ramp_down_time * dt)
        speed_out = max(min_spd_offset, min(max_spd_offset, self.smooth_spd[-1]))

    if v_cmd > 0:
        cntr_spd = max(0, speed_out)
    elif v_cmd < 0:
        cntr_spd = min(0, speed_out)
    else:
        cntr_spd = speed_out

    return cntr_spd
