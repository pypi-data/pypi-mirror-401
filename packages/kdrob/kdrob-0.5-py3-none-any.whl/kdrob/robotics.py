def battery_time(capacity_mAh, current_mA):
    return capacity_mAh / current_mA

def stop_distance(speed, deceleration):
    return (speed ** 2) / (2 * deceleration)

def encoder_to_distance(pulses, wheel_radius, pulses_per_rev):
    circumference = 2 * 3.14159 * wheel_radius
    revolutions = pulses / pulses_per_rev
    return revolutions * circumference

def motor_health(temperature, vibration, current):
    score = 100

    if temperature > 60:
        score -= 30
    if vibration > 5:
        score -= 30
    if current > 10:
        score -= 20

    return max(score, 0)
