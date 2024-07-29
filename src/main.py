import numpy as np
from simulation import run_simulation

# 定数
L = 100  # 正方形の一辺の長さ
N = 10   # 粒子の数
position_noise_strength = 0.1  # ノイズの強さ
velocity_noise_strength = 0.1  # ノイズの強さ
steps = 1000
dt = 0.005
distance_threshold = 2.0
a = 1.0
c = 1.0

def generate_initial_positions_around_perimeter(N, L):
    positions = np.zeros((N, 2))
    side_points = N // 4
    points_per_side = np.linspace(0, L, side_points, endpoint=False)
    
    # 下辺
    positions[:side_points, 0] = points_per_side
    positions[:side_points, 1] = 0
    
    # 右辺
    positions[side_points:2*side_points, 0] = L
    positions[side_points:2*side_points, 1] = points_per_side
    
    # 上辺
    positions[2*side_points:3*side_points, 0] = points_per_side[::-1]
    positions[2*side_points:3*side_points, 1] = L
    
    # 左辺
    positions[3*side_points:, 0] = 0
    positions[3*side_points:, 1] = points_per_side[::-1]
    
    return positions

# 初期位置の生成関数
def generate_initial_positions_reflection(N,  L, noise_strength):
    positions = np.zeros((N * N, 2))
    sqrt3 = np.sqrt(3)
    
    for i in range(N):
        for j in range(N):
            x_position = i * sqrt3
            y_position = j * 2 + (1 if i % 2 != 0 else 0)
            positions[i * N + j] = [x_position, y_position]
    
    # Add noise if necessary
    if noise_strength > 0:
        positions += np.random.normal(0, noise_strength, positions.shape)
    
    return positions

# 初期速度の設定関数
def generate_initial_velocities(N, direction='right'):
    velocities = np.zeros((N, 2))
    if direction == 'right':
        velocities[:, 0] = 5.0  # すべての粒子が右方向に移動
        velocities += np.random.normal(0, velocity_noise_strength, velocities.shape)
    # elif direction == 'center':
    #     center = np.array([L/2, L/2])
    #     for i in range(N):
    #         direction_vector = center - positions[i]
    #         direction_vector /= np.linalg.norm(direction_vector)
    #         velocities[i] = direction_vector * 5  # 基本速度を設定
    #     velocities += np.random.normal(0, velocity_noise_strength, velocities.shape)
    # elif direction == 'random':
    #     velocities = np.random.randn(N, 2)
    #     velocities += np.random.normal(0, velocity_noise_strength, velocities.shape)
    return velocities



def main():
    # シミュレーションの設定
    simulations = [
        {"name": "reflective", "boundary_condition": "periodic", "direction": "right"},
        # {"name": "towards_center", "boundary_condition": "reflective", "direction": "center"},
        # {"name": "periodic_random", "boundary_condition": "periodic", "direction": "random"}
    ]

    np.random.seed(0)

    # 複数のシミュレーションを実行
    for i, sim in enumerate(simulations):
        if sim["name"] == "reflective":
            positions = generate_initial_positions_reflection(N, L, position_noise_strength)
        elif sim["name"] == "towards_center":
            positions = generate_initial_positions_around_perimeter(N, L)
        velocities = generate_initial_velocities(len(positions), sim["direction"])
        accelerations = np.zeros((len(positions), 2))
        filename = f'simulation_{sim["name"]}_{i}'
        run_simulation(positions, velocities, accelerations, distance_threshold, steps, dt, a, c, filename, sim["boundary_condition"])

if __name__ == '__main__':
    main()