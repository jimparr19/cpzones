import numpy as np

race_weight = 70
race_distance = 5000
race_time = 1200

air_density = 1.225

fatigue_factor = np.array([1.05, 1.08])  # Amount a runner's velocity decreases as race distance increases.
c = np.array([0.88, 1.08])  # specific energy cost of running (related to running economy)
cda = np.array([0.2, 0.24])  # coefficient of drag times ares

distance_at_ftp = (3600 / race_time) ** (1 / fatigue_factor) * race_distance
velocity_at_ftp = distance_at_ftp / 3600

power_ftp_upper = min(6.4 * race_weight, (max(c) * max(velocity_at_ftp) * race_weight) + (
        0.5 * air_density * max(cda) * max(velocity_at_ftp) ** 3))  # 6.4 watts/kg is limits of human power
power_ftp_lower = (min(c) * min(velocity_at_ftp) * race_weight) + (
        0.5 * air_density * min(cda) * min(velocity_at_ftp) ** 3)

print(f'lower ftp {np.round(power_ftp_lower)} upper ftp {np.round(power_ftp_upper)}')
print(f'range ftp {power_ftp_upper - power_ftp_lower}')
