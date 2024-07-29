import numpy as np

# 角度依存性関数
def P(theta):
    return 0.5 * (1 + np.cos(theta))

# 力関数
def V(r, c):
    return np.tanh(r - c) + np.tanh(c)

# 位置と速度の更新関数
def update(positions, velocities, accelerations, dt, neighbors, a, c):
    N = len(neighbors)
    new_accelerations = np.zeros_like(accelerations)
    
    for n in range(N):
        force_sum = np.zeros(2)
        
        for m in neighbors[n]:
            rmn = np.linalg.norm(positions[n] - positions[m])
            if rmn == 0:  # avoid division by zero
                continue
            emn = (positions[n] - positions[m]) / rmn
            dot_product = np.dot(velocities[n], velocities[m])
            norms_product = np.linalg.norm(velocities[n]) * np.linalg.norm(velocities[m])
            if norms_product == 0:  # avoid division by zero
                continue
            cos_theta = np.clip(dot_product / norms_product, -1.0, 1.0)
            theta_mn = np.arccos(cos_theta)

            force_sum -= velocities[n]

    new_accelerations += a * force_sum
    new_velocities = velocities + new_accelerations * dt
    new_positions = positions + new_velocities * dt
    
    return new_positions, new_velocities, new_accelerations

# 近傍点の探索関数
def find_neighbors(positions, distance_threshold):
    N = positions.shape[0]
    neighbors = []

    for n in range(N):
        neighbor_set = []
        for m in range(N):
            if n != m:
                distance = np.linalg.norm(positions[n] - positions[m])
                if distance <= distance_threshold:
                    neighbor_set.append(m)
        neighbors.append(neighbor_set)
    
    return neighbors
