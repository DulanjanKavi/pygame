import pygame
import random
import math
from queue import PriorityQueue
pygame.init()

win = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Advanced Enemy AI Example")

clock = pygame.time.Clock()
s=[]

class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.health = 100

    def draw(self, win):
        pygame.draw.rect(win, (0, 0, 255), (self.x, self.y, self.width, self.height))

    def move(self, keys, obstacles):
        if keys[pygame.K_LEFT]:
            self.x -= self.vel
            if self.collide(obstacles):
                self.x += self.vel
        if keys[pygame.K_RIGHT]:
            self.x += self.vel
            if self.collide(obstacles):
                self.x -= self.vel
        if keys[pygame.K_UP]:
            self.y -= self.vel
            if self.collide(obstacles):
                self.y += self.vel
        if keys[pygame.K_DOWN]:
            self.y += self.vel
            if self.collide(obstacles):
                self.y -= self.vel

    def collide(self, obstacles):
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        for obstacle in obstacles:
            if player_rect.colliderect(obstacle):
                return True
        return False

class Enemy:
    def __init__(self, x, y, width, height, waypoints):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 3
        self.waypoints = waypoints
        self.current_waypoint = 0
        self.state = "patrolling"
        self.path = []
        self.attack_range = 50
        self.attack_cooldown = 0
        self.vision_front = 200  # Vision range in front
        self.vision_back =   50# Vision range in the back
        self.vision_side = 100   # Vision range on the sides
        self.vision_angle = 360   # Vision angle in degrees]
        self.color=(0,0,0)

    def move_towards_player(self, player, obstacles):
        if self.path:
            next_pos = self.path[0]
            if self.x < next_pos[0]:
                self.x += self.vel
                if self.collide(obstacles):
                    self.x -= self.vel
            elif self.x > next_pos[0]:
                self.x -= self.vel
                if self.collide(obstacles):
                    self.x += self.vel
            if self.y < next_pos[1]:
                self.y += self.vel
                if self.collide(obstacles):
                    self.y -= self.vel
            elif self.y > next_pos[1]:
                self.y -= self.vel
                if self.collide(obstacles):
                    self.y += self.vel

            if math.hypot(self.x - next_pos[0], self.y - next_pos[1]) < 5:
                self.path.pop(0)

    def patrol(self, obstacles):
        waypoint = self.waypoints[self.current_waypoint]
        if self.x < waypoint[0]:
            self.x += self.vel
            if self.collide(obstacles):
                self.x -= self.vel
        elif self.x > waypoint[0]:
            self.x -= self.vel
            if self.collide(obstacles):
                self.x += self.vel
        if self.y < waypoint[1]:
            self.y += self.vel
            if self.collide(obstacles):
                self.y -= self.vel
        elif self.y > waypoint[1]:
            self.y -= self.vel
            if self.collide(obstacles):
                self.y += self.vel

        if math.hypot(self.x - waypoint[0], self.y - waypoint[1]) < 5:
            self.current_waypoint = (self.current_waypoint + 1) % len(self.waypoints)

    def attack(self, player):
        if self.attack_cooldown == 0:
            player.health -= 10
            self.attack_cooldown = 30 # Cooldown period before the next attack
            if "attack mode" not in s:
                s.append("attack mode")
                self.color=(255,0,0)

    def draw(self, win):
        #pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.width, self.height))
        # Draw vision cone
        self.draw_vision_cone(win)
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    def draw_vision_cone(self, win):
    # Calculate the center of the enemy
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2

        # Define the vision ranges
        vision_front = self.vision_front
        vision_back = self.vision_back
        vision_side = self.vision_side

        # Calculate the points of the oval-shaped vision cone
        points = []
        for angle in range(0,360,10):
            radians = math.radians(angle)
            if -45 <= angle <= 45:
                vision_range = vision_front
            elif 135 <= angle <= 225 or -225 <= angle <= -135:
                vision_range = vision_back
            else:
                vision_range = vision_side
            y = vision_side * math.cos(radians)
            x = vision_front * math.sin(radians)
            rotated_x = x * math.cos(math.radians(0)) - y * math.sin(math.radians(0))+30
            rotated_y = x * math.sin(math.radians(0)) + y * math.cos(math.radians(0))

            end_x, end_y = self.check_obstacles((center_x, center_y), (center_x + rotated_x, center_y + rotated_y)) 
            points.append((end_x, end_y))

            

            

        
        for point in points:
            pygame.draw.line(win, (255, 255, 0), (center_x, center_y), point, 1)


    def check_obstacles(self, start, end):
        for obstacle in obstacles:
            if self.line_intersects_rect(start, end, obstacle):
                return self.get_intersection_point(start, end, obstacle)
        return end

    def get_intersection_point(self, start, end, rect):
        # Calculate the intersection point of a line with a rectangle
        rect_lines = [
            ((rect.left, rect.top), (rect.right, rect.top)),
            ((rect.left, rect.top), (rect.left, rect.bottom)),
            ((rect.right, rect.top), (rect.right, rect.bottom)),
            ((rect.left, rect.bottom), (rect.right, rect.bottom))
        ]
        for line in rect_lines:
            intersection = self.line_intersection(start, end, line[0], line[1])
            if intersection:
                return intersection
        return end

    def line_intersection(self, p1, p2, p3, p4):
        # Calculate the intersection point of two lines
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        x4, y4 = p4

        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denom == 0:
            return None

        px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
        py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom

        if (min(x1, x2) <= px <= max(x1, x2) and min(y1, y2) <= py <= max(y1, y2) and
                min(x3, x4) <= px <= max(x3, x4) and min(y3, y4) <= py <= max(y3, y4)):
            return px, py
        return None

    def collide(self, obstacles):
        enemy_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        for obstacle in obstacles:
            if enemy_rect.colliderect(obstacle):
                return True
        return False
    
    def cal_attack_Range(self):
    # Calculate the center of the enemy
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2

        # Define the vision ranges
        vision_front = self.vision_front
        vision_back = self.vision_back
        vision_side = self.vision_side

        # Calculate the points of the oval-shaped vision cone
        points = []
        for angle in range(0,360,10):
            radians = math.radians(angle)
            if -45 <= angle <= 45:
                vision_range = vision_front
            elif 135 <= angle <= 225 or -225 <= angle <= -135:
                vision_range = vision_back
            else:
                vision_range = vision_side
            y = vision_side * math.cos(radians)
            x = vision_front * math.sin(radians)
            rotated_x = x * math.cos(math.radians(0)) - y * math.sin(math.radians(0))+30
            rotated_y = x * math.sin(math.radians(0)) + y * math.cos(math.radians(0))
            points.append((center_x + rotated_x, center_y + rotated_y))

    def update(self, player, obstacles):
        if self.state == "chasing":
            self.path = self.a_star((self.x, self.y), (player.x, player.y), obstacles)
            self.move_towards_player(player, obstacles)
            if math.hypot(self.x - player.x, self.y - player.y) < self.attack_range:
                self.attack(player)
        elif self.state == "patrolling":
            self.patrol(obstacles)
        elif self.state == "searching":
            self.search(player)
        elif self.state == "fleeing":
            self.flee(player)

        # Check if the enemy should start chasing the player
        if self.can_see_player(player, obstacles):
            self.state = "chasing"
            if "chasing" not in s:
                s.append("chasing")
                self.color=(255,0,255)
        else:
            self.state = "patrolling"
            if "patrolling" not in s:
                s.append("patrolling")
                self.color=(255,255,0)

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            if "cooldown" not in s:
                s.append("cooldown")
                self.color=(0,0,255)

    def can_see_player(self, player, obstacles):
        # Check if the player is within the vision cone
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.hypot(dx, dy)
        if distance > self.vision_front:
            return False

        angle = math.degrees(math.atan2(dy, dx))
        if angle < 0:
            angle += 360

        start_angle =0# (self.vision_angle / 2) % 360
        end_angle =360 #(360 - self.vision_angle / 2) % 360

        if start_angle < end_angle:
            if not (start_angle <= angle <= end_angle):
                return False
        else:
            if not (angle >= start_angle or angle <= end_angle):
                return False

        # Check if there are obstacles blocking the view
        for obstacle in obstacles:
            if self.line_intersects_rect((self.x + self.width // 2, self.y + self.height // 2), (player.x, player.y), obstacle):
                return False

        return True

    def line_intersects_rect(self, start, end, rect):
        # Check if a line intersects a rectangle
        rect_lines = [
            ((rect.left, rect.top), (rect.right, rect.top)),
            ((rect.left, rect.top), (rect.left, rect.bottom)),
            ((rect.right, rect.top), (rect.right, rect.bottom)),
            ((rect.left, rect.bottom), (rect.right, rect.bottom))
        ]
        for line in rect_lines:
            if self.lines_intersect(start, end, line[0], line[1]):
                return True
        return False

    def lines_intersect(self, p1, p2, p3, p4):
        # Check if two lines intersect
        def ccw(A, B, C):
            return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
        return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)

    def search(self, player):
        # Implement search behavior
        if "search mode" not in s:
            s.append("search mode")
        pass

    def flee(self, player):
        # Implement flee behavior
        if "flee mode" not in s:
            s.append("flee mode")
        pass

    def a_star(self, start, goal, obstacles):
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        open_set = PriorityQueue()
        open_set.put((0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, goal)}

        while not open_set.empty():
            current = open_set.get()[1]

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (current[0] + dx, current[1] + dy)
                if 0 <= neighbor[0] < 1000 and 0 <= neighbor[1] < 800 and neighbor not in obstacles:
                    tentative_g_score = g_score[current] + 1
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                        open_set.put((f_score[neighbor], neighbor))

        return []

def redraw_game_window():
    win.fill((0, 0, 0))
    player.draw(win)
    enemy.draw(win)
    for obstacle in obstacles:
        pygame.draw.rect(win, (0, 255, 0), obstacle)
    pygame.display.update()

# Main loop
player = Player(400, 300, 50, 50)
waypoints = [(0, 0), (1000, 0), (0, 800), (1000, 800)]
enemy = Enemy(random.randint(0, 750), random.randint(0, 550), 50, 50, waypoints)
obstacles =[pygame.Rect(300, 200, 200, 50), pygame.Rect(500, 400, 50, 200)]

run = True
while run:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    player.move(keys, obstacles)

    enemy.update(player, obstacles)
    redraw_game_window()

pygame.quit()
print(s)
