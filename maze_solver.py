import heapq
import os

# --- Maze Grid ---
maze = [
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0],
    [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
]

start = (0, 0)
goal  = (8, 10)

# --- Heuristic ---
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# --- Reconstruct Path ---
def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append(current)
    path.reverse()
    return path

# --- A* Algorithm ---
def astar(maze, start, goal):
    rows = len(maze)
    cols = len(maze[0])
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}

    while open_list:
        _, current = heapq.heappop(open_list)
        if current == goal:
            return reconstruct_path(came_from, current)
        row, col = current
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = row+dr, col+dc
            if nr < 0 or nr >= rows: continue
            if nc < 0 or nc >= cols: continue
            if maze[nr][nc] == 1:    continue
            new_g = g_score[current] + 1
            neighbor = (nr, nc)
            if neighbor not in g_score or new_g < g_score[neighbor]:
                g_score[neighbor] = new_g
                f = new_g + heuristic(neighbor, goal)
                heapq.heappush(open_list, (f, neighbor))
                came_from[neighbor] = current
    return None

# --- Display Maze ---
def display(maze, player, path_cells, start, goal, steps, show_path):
    os.system('cls' if os.name == 'nt' else 'clear')

    print("=" * 40)
    print("      MAZE SOLVER — A* GAME")
    print("=" * 40)
    print(f"  Steps taken : {steps}")
    opt = len(path_cells) - 1 if path_cells else '?'
    print(f"  Optimal path: {opt} steps")
    print("=" * 40)
    print()

    path_set = set(path_cells) if show_path else set()

    for r, row in enumerate(maze):
        line = "  "
        for c, cell in enumerate(row):
            pos = (r, c)
            if pos == player:
                line += " P "
            elif pos == goal:
                line += " G "
            elif pos == start:
                line += " S "
            elif cell == 1:
                line += "███"
            elif pos in path_set:
                line += " · "
            else:
                line += " . "
        print(line)

    print()
    print("  Legend: P=You  S=Start  G=Goal  ███=Wall  ·=Path")
    print()
    print("  Controls:")
    print("  W = Up   S = Down   A = Left   D = Right")
    print("  H = Show/Hide A* path   R = Restart   Q = Quit")
    print()

# --- Main Game ---
def main():
    player = list(start)
    steps = 0
    show_path = False
    visited = set()
    visited.add(tuple(player))

    # Pre-calculate optimal path
    path = astar(maze, start, goal)
    path_cells = path if path else []

    rows = len(maze)
    cols = len(maze[0])

    display(maze, tuple(player), path_cells, start, goal, steps, show_path)

    while True:
        move = input("  Your move: ").strip().lower()

        if move == 'q':
            print("\n  Thanks for playing! Goodbye.")
            break

        elif move == 'r':
            player = list(start)
            steps = 0
            show_path = False
            visited = set()
            visited.add(tuple(player))
            display(maze, tuple(player), path_cells, start, goal, steps, show_path)
            continue

        elif move == 'h':
            show_path = not show_path
            display(maze, tuple(player), path_cells, start, goal, steps, show_path)
            continue

        # Movement
        dr, dc = 0, 0
        if   move == 'w': dr = -1
        elif move == 's': dr =  1
        elif move == 'a': dc = -1
        elif move == 'd': dc =  1
        else:
            display(maze, tuple(player), path_cells, start, goal, steps, show_path)
            print("  Invalid key! Use W A S D to move.")
            continue

        nr = player[0] + dr
        nc = player[1] + dc

        # Check bounds and walls
        if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
            display(maze, tuple(player), path_cells, start, goal, steps, show_path)
            print("  Out of bounds! Try another direction.")
            continue

        if maze[nr][nc] == 1:
            display(maze, tuple(player), path_cells, start, goal, steps, show_path)
            print("  Wall! You can't go there.")
            continue

        # Valid move
        player = [nr, nc]
        steps += 1
        visited.add(tuple(player))

        # Check win
        if tuple(player) == goal:
            display(maze, tuple(player), path_cells, start, goal, steps, show_path)
            print("=" * 40)
            print("  YOU REACHED THE GOAL!")
            opt = len(path_cells) - 1 if path_cells else '?'
            if steps == opt:
                print(f"  PERFECT! Optimal path in {steps} steps!")
            else:
                print(f"  Completed in {steps} steps!")
                print(f"  Optimal was {opt} steps.")
            print("=" * 40)
            again = input("\n  Play again? (Y/N): ").strip().lower()
            if again == 'y':
                main()
            break

        display(maze, tuple(player), path_cells, start, goal, steps, show_path)

if __name__ == "__main__":
    main()