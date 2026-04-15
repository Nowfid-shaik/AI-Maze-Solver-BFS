import tkinter as tk
import random
from collections import deque

# Grid size
ROWS = 10
COLS = 10
CELL_SIZE = 40

# Colors
COLORS = {
    "empty": "#d0e1f9",
    "wall": "#2c3e50",
    "start": "#27ae60",
    "goal": "#e74c3c",
    "visited": "#5dade2",
    "path": "#f4d03f"
}

start = (0, 0)
goal = (ROWS - 1, COLS - 1)

maze = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# GUI setup
window = tk.Tk()
window.title("✨ AI Maze Solver (BFS)")
window.configure(bg="#1e1e2f")

canvas = tk.Canvas(
    window,
    width=COLS * CELL_SIZE,
    height=ROWS * CELL_SIZE,
    bg="#1e1e2f",
    highlightthickness=0
)
canvas.pack(pady=10)

info_label = tk.Label(
    window,
    text="Ready",
    fg="white",
    bg="#1e1e2f",
    font=("Arial", 12)
)
info_label.pack()

speed_var = tk.IntVar(value=50)

speed_slider = tk.Scale(
    window,
    from_=10,
    to=200,
    orient="horizontal",
    label="Animation Speed",
    variable=speed_var,
    bg="#1e1e2f",
    fg="white"
)
speed_slider.pack(pady=5)


# Draw grid
def draw_grid():
    canvas.delete("all")

    for r in range(ROWS):
        for c in range(COLS):

            x1 = c * CELL_SIZE
            y1 = r * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE

            if (r, c) == start:
                color = COLORS["start"]

            elif (r, c) == goal:
                color = COLORS["goal"]

            elif maze[r][c] == 1:
                color = COLORS["wall"]

            else:
                color = COLORS["empty"]

            canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=color,
                outline="#1e1e2f"
            )


# Toggle wall by clicking
def toggle_wall(event):

    col = event.x // CELL_SIZE
    row = event.y // CELL_SIZE

    if (row, col) == start:
        return

    if (row, col) == goal:
        return

    maze[row][col] = 1 - maze[row][col]

    draw_grid()


canvas.bind("<Button-1>", toggle_wall)


# Generate random maze
def random_maze():

    for r in range(ROWS):
        for c in range(COLS):

            if (r, c) != start and (r, c) != goal:

                maze[r][c] = random.choice([0, 0, 0, 1])

    draw_grid()


# Reset maze
def reset_maze():

    for r in range(ROWS):
        for c in range(COLS):

            maze[r][c] = 0

    draw_grid()

    info_label.config(text="Maze Reset")


# BFS algorithm
def bfs():

    queue = deque([(start, [start])])
    visited = set()

    nodes = 0

    def step():

        nonlocal nodes

        if not queue:

            info_label.config(text="No Path Found")
            return

        (r, c), path = queue.popleft()

        if (r, c) in visited:
            window.after(speed_var.get(), step)
            return

        visited.add((r, c))

        nodes += 1

        if (r, c) != start and (r, c) != goal:

            x1 = c * CELL_SIZE
            y1 = r * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE

            canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=COLORS["visited"],
                outline="#1e1e2f"
            )

        if (r, c) == goal:

            for pr, pc in path:

                if (pr, pc) != start and (pr, pc) != goal:

                    x1 = pc * CELL_SIZE
                    y1 = pr * CELL_SIZE
                    x2 = x1 + CELL_SIZE
                    y2 = y1 + CELL_SIZE

                    canvas.create_rectangle(
                        x1,
                        y1,
                        x2,
                        y2,
                        fill=COLORS["path"],
                        outline="#1e1e2f"
                    )

            info_label.config(
                text=f"✔ Path: {len(path)} steps | Nodes: {nodes}"
            )

            return

        directions = [(-1,0),(1,0),(0,-1),(0,1)]

        for dr, dc in directions:

            nr = r + dr
            nc = c + dc

            if (
                0 <= nr < ROWS
                and 0 <= nc < COLS
                and maze[nr][nc] == 0
            ):

                queue.append(
                    ((nr, nc), path + [(nr, nc)])
                )

        window.after(speed_var.get(), step)

    step()


# Buttons
button_frame = tk.Frame(window, bg="#1e1e2f")
button_frame.pack(pady=10)

run_btn = tk.Button(
    button_frame,
    text="▶ Run BFS",
    command=bfs,
    width=12,
    bg="#3498db",
    fg="white"
)
run_btn.grid(row=0, column=0, padx=5)

reset_btn = tk.Button(
    button_frame,
    text="↺ Reset",
    command=reset_maze,
    width=12,
    bg="#e67e22",
    fg="white"
)
reset_btn.grid(row=0, column=1, padx=5)

random_btn = tk.Button(
    button_frame,
    text="🎲 Random Maze",
    command=random_maze,
    width=14,
    bg="#9b59b6",
    fg="white"
)
random_btn.grid(row=0, column=2, padx=5)

draw_grid()

window.mainloop()