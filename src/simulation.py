import numpy as np
import matplotlib.pyplot as plt
import imageio
import os
from numba import jit
from model import update, find_neighbors

def run_simulation(positions, velocities, accelerations, distance_threshold, steps, dt, a, c, filename, boundary_condition):
    neighbors = find_neighbors(positions, distance_threshold)
    filenames = []

    for step in range(steps):
        positions, velocities, accelerations = update(positions, velocities, accelerations, dt, neighbors, a, c)
        
        if boundary_condition == "reflective":
            # x=0またはx=100に達したらvxを反転させる
            velocities[positions[:, 0] <= 0, 0] *= -1
            velocities[positions[:, 0] >= 100, 0] *= -1
            # y=0またはy=100に達したらvyを反転させる
            velocities[positions[:, 1] <= 0, 1] *= -1
            velocities[positions[:, 1] >= 100, 1] *= -1
            
            # x方向の境界を超えた場合の位置更新（反転）
            positions[positions[:, 0] < 0, 0] = -positions[positions[:, 0] < 0, 0]
            positions[positions[:, 0] > 100, 0] = 200 - positions[positions[:, 0] > 100, 0]
            # y方向の境界を超えた場合の位置更新（反転）
            positions[positions[:, 1] < 0, 1] = -positions[positions[:, 1] < 0, 1]
            positions[positions[:, 1] > 100, 1] = 200 - positions[positions[:, 1] > 100, 1]

        elif boundary_condition == "periodic":
            positions = positions % 100  # x方向とy方向の両方で周期境界条件を適用

        if step % 100 == 0:
            plt.figure(figsize=(6, 6))
            plt.xlim(0, 100)
            plt.ylim(0, 100)
            plt.scatter(positions[:, 0], positions[:, 1], c='blue')
            plt.title(f'Step {step}')
            temp_filename = f'{filename}_temp_{step}.png'
            plt.savefig(temp_filename)
            filenames.append(temp_filename)
            plt.close()

    with imageio.get_writer(f'{filename}.gif', mode='I', duration=0.1) as writer:
        for temp_filename in filenames:
            image = imageio.imread(temp_filename)
            writer.append_data(image)

    for temp_filename in filenames:
        os.remove(temp_filename)

    print(f"GIF作成完了！ {filename}.gif")
