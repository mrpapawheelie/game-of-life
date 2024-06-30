import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import streamlit as st

ON = 255  # alive
OFF = 0   # dead

def update(frame_num, img, grid, N):
    new_grid = grid.copy()
    for i in range(N):
        for j in range(N):
            total = int((grid[i, (j-1)%N] + grid[i, (j+1)%N] +
                         grid[(i-1)%N, j] + grid[(i+1)%N, j] +
                         grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] +
                         grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N]) / 255)
            if grid[i, j] == ON:
                if (total < 2) or (total > 3):
                    new_grid[i, j] = OFF
            else:
                if total == 3:
                    new_grid[i, j] = ON
    img.set_data(new_grid)
    grid[:] = new_grid[:]
    return img,

def initialize_grid(N, on_prob):
    return np.random.choice([ON, OFF], N*N, p=[on_prob, 1-on_prob]).reshape(N, N)

def main():
    st.title("Conway's Game of Life")

    N = st.sidebar.slider("Grid size", min_value=10, max_value=200, value=100, step=10)
    update_interval = st.sidebar.slider("Update interval (ms)", min_value=10, max_value=1000, value=50, step=10)
    on_prob = st.sidebar.slider("Initial probability of being alive", min_value=0.0, max_value=1.0, value=0.2, step=0.05)

    grid = initialize_grid(N, on_prob)
    
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')

    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N),
                                  frames=10,
                                  interval=update_interval,
                                  save_count=50)
    
    st.pyplot(fig)

if __name__ == '__main__':
    main()