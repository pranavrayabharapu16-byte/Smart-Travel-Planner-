import heapq
import random
from collections import defaultdict

# =============================
# SMART TRAVEL PLANNER AI PROJECT
# =============================
# Features:
# - Graph based route planning
# - A* Search Algorithm
# - BFS Search
# - DFS Search
# - UCS (Uniform Cost Search)
# - Probabilistic delay handling
# - Multiple transport methods
# - Indian cities and states
# - Cost + time estimation
# - Explainable route output
# =============================


class City:
    def __init__(self, name, state):
        self.name = name
        self.state = state

    def __str__(self):
        return f"{self.name}, {self.state}"


class Route:
    def __init__(self, destination, transport, distance, cost, delay_probability):
        self.destination = destination
        self.transport = transport
        self.distance = distance
        self.cost = cost
        self.delay_probability = delay_probability


class SmartTravelPlanner:
    def __init__(self):
        self.graph = defaultdict(list)
        self.heuristic = {}

    # =============================
    # ADD CONNECTIONS
    # =============================
    def add_route(self, source, destination, transport, distance, cost, delay_probability):
        self.graph[source].append(
            Route(destination, transport, distance, cost, delay_probability)
        )

        self.graph[destination].append(
            Route(source, transport, distance, cost, delay_probability)
        )

    # =============================
    # HEURISTIC VALUES FOR A*
    # =============================
    def set_heuristic(self, city, value):
        self.heuristic[city] = value

    # =============================
    # BFS SEARCH
    # =============================
    def bfs(self, start, goal):
        visited = set()
        queue = [(start, [start])]

        while queue:
            node, path = queue.pop(0)

            if node == goal:
                return path

            if node not in visited:
                visited.add(node)

                for route in self.graph[node]:
                    queue.append((route.destination, path + [route.destination]))

        return None

    # =============================
    # DFS SEARCH
    # =============================
    def dfs(self, start, goal):
        visited = set()
        stack = [(start, [start])]

        while stack:
            node, path = stack.pop()

            if node == goal:
                return path

            if node not in visited:
                visited.add(node)

                for route in self.graph[node]:
                    stack.append((route.destination, path + [route.destination]))

        return None

    # =============================
    # UNIFORM COST SEARCH
    # =============================
    def ucs(self, start, goal):
        pq = [(0, start, [])]
        visited = set()

        while pq:
            cost, node, path = heapq.heappop(pq)

            if node in visited:
                continue

            visited.add(node)
            path = path + [node]

            if node == goal:
                return cost, path

            for route in self.graph[node]:
                if route.destination not in visited:
                    heapq.heappush(
                        pq,
                        (cost + route.cost, route.destination, path)
                    )

        return None

    # =============================
    # A* SEARCH ALGORITHM
    # =============================
    def astar(self, start, goal):
        open_list = []
        heapq.heappush(open_list, (0, start, [], 0))

        visited = set()

        while open_list:
            f_cost, current, path, g_cost = heapq.heappop(open_list)

            if current in visited:
                continue

            visited.add(current)
            path = path + [current]

            if current == goal:
                return g_cost, path

            for route in self.graph[current]:
                if route.destination not in visited:
                    new_g = g_cost + route.cost
                    h = self.heuristic.get(route.destination, 0)
                    f = new_g + h

                    heapq.heappush(
                        open_list,
                        (f, route.destination, path, new_g)
                    )

        return None

    # =============================
    # PROBABILISTIC DELAY CHECK
    # =============================
    def simulate_delay(self, probability):
        return random.random() < probability

    # =============================
    # DISPLAY COMPLETE ROUTE DETAILS
    # =============================
    def display_route_details(self, path):
        total_distance = 0
        total_cost = 0

        print("\n========== ROUTE DETAILS ==========")

        for i in range(len(path) - 1):
            current = path[i]
            next_city = path[i + 1]

            for route in self.graph[current]:
                if route.destination == next_city:
                    print(f"\nFROM: {current}")
                    print(f"TO: {next_city}")
                    print(f"TRANSPORT: {route.transport}")
                    print(f"DISTANCE: {route.distance} KM")
                    print(f"COST: ₹{route.cost}")

                    delay = self.simulate_delay(route.delay_probability)

                    if delay:
                        print("STATUS: Delay Possible")
                    else:
                        print("STATUS: On Time")

                    total_distance += route.distance
                    total_cost += route.cost

        print("\n========== SUMMARY ==========")
        print(f"TOTAL DISTANCE: {total_distance} KM")
        print(f"TOTAL COST: ₹{total_cost}")


# =============================
# CREATE PROJECT
# =============================
planner = SmartTravelPlanner()


# =============================
# ADD ROUTES
# =============================

# Telangana
planner.add_route("Hyderabad", "Warangal", "Bus", 150, 400, 0.1)
planner.add_route("Hyderabad", "Nizamabad", "Train", 175, 350, 0.2)
planner.add_route("Hyderabad", "Karimnagar", "Car", 165, 1200, 0.15)

# Andhra Pradesh
planner.add_route("Hyderabad", "Vijayawada", "Train", 275, 600, 0.2)
planner.add_route("Vijayawada", "Visakhapatnam", "Flight", 350, 3500, 0.05)
planner.add_route("Tirupati", "Vijayawada", "Bus", 430, 800, 0.25)

# Karnataka
planner.add_route("Hyderabad", "Bengaluru", "Flight", 570, 4500, 0.1)
planner.add_route("Bengaluru", "Mysuru", "Bus", 145, 350, 0.15)
planner.add_route("Bengaluru", "Mangaluru", "Train", 350, 900, 0.2)

# Tamil Nadu
planner.add_route("Bengaluru", "Chennai", "Train", 345, 700, 0.2)
planner.add_route("Chennai", "Coimbatore", "Flight", 500, 4000, 0.1)
planner.add_route("Chennai", "Madurai", "Bus", 460, 900, 0.3)

# Kerala
planner.add_route("Coimbatore", "Kochi", "Car", 190, 2500, 0.15)
planner.add_route("Kochi", "Thiruvananthapuram", "Train", 200, 650, 0.2)

# Maharashtra
planner.add_route("Hyderabad", "Mumbai", "Flight", 710, 5500, 0.08)
planner.add_route("Mumbai", "Pune", "Bus", 150, 450, 0.1)
planner.add_route("Pune", "Nagpur", "Train", 720, 1200, 0.25)

# Delhi
planner.add_route("Mumbai", "Delhi", "Flight", 1400, 6500, 0.12)
planner.add_route("Hyderabad", "Delhi", "Flight", 1250, 6200, 0.1)

# Rajasthan
planner.add_route("Delhi", "Jaipur", "Bus", 280, 600, 0.18)
planner.add_route("Jaipur", "Udaipur", "Car", 395, 3500, 0.2)

# Gujarat
planner.add_route("Mumbai", "Ahmedabad", "Train", 530, 900, 0.15)
planner.add_route("Ahmedabad", "Surat", "Bus", 265, 500, 0.12)

# West Bengal
planner.add_route("Delhi", "Kolkata", "Flight", 1500, 7000, 0.1)
planner.add_route("Kolkata", "Darjeeling", "Car", 620, 4500, 0.3)

# Odisha
planner.add_route("Kolkata", "Bhubaneswar", "Train", 440, 800, 0.2)

# Goa
planner.add_route("Mumbai", "Goa", "Train", 590, 1100, 0.2)

# Punjab
planner.add_route("Delhi", "Amritsar", "Train", 450, 850, 0.18)

# Uttar Pradesh
planner.add_route("Delhi", "Lucknow", "Bus", 550, 900, 0.22)
planner.add_route("Lucknow", "Varanasi", "Train", 320, 600, 0.2)

# Assam
planner.add_route("Kolkata", "Guwahati", "Flight", 1000, 5500, 0.15)


# =============================
# HEURISTIC VALUES
# =============================
planner.set_heuristic("Warangal", 120)
planner.set_heuristic("Nizamabad", 140)
planner.set_heuristic("Karimnagar", 130)
planner.set_heuristic("Vijayawada", 250)
planner.set_heuristic("Visakhapatnam", 300)
planner.set_heuristic("Bengaluru", 450)
planner.set_heuristic("Chennai", 500)
planner.set_heuristic("Mumbai", 700)
planner.set_heuristic("Delhi", 1000)
planner.set_heuristic("Kolkata", 1300)
planner.set_heuristic("Goa", 600)
planner.set_heuristic("Jaipur", 1050)
planner.set_heuristic("Lucknow", 1150)
planner.set_heuristic("Guwahati", 1600)


# =============================
# MAIN PROGRAM
# =============================
print("\n========== SMART TRAVEL PLANNER ==========")

print("\nAvailable Cities:")
for city in planner.graph.keys():
    print(city)

start = input("\nEnter Source City: ")
goal = input("Enter Destination City: ")

# =============================
# AUTOMATICALLY RUN A* SEARCH
# =============================
result = planner.astar(start, goal)

if result:
    cost, path = result

    print("\nBEST ROUTE FOUND USING A* SEARCH")
    print(" -> ".join(path))
    print(f"ESTIMATED COST: ₹{cost}")

    planner.display_route_details(path)

else:
    print("No path found")