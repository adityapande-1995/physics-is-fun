import pygame
import math
import random

# --- Configuration ---
WIDTH, HEIGHT = 800, 800
HALF_HEIGHT = HEIGHT // 2
FPS = 60

# Physics Constants
G = 1.0
C = 1.0
DT = 0.5
TRAIL_LENGTH = 100
SPAWN_RATE = 5  # Frames between spawns

# Colors
BLACK = (5, 5, 5)
WHITE = (255, 255, 255)
SCHWARZ_COLOR = (0, 255, 170)  # Teal/Green
KERR_COLOR = (0, 255, 255)     # Cyan
HORIZON_COLOR = (0, 0, 0)
PHOTON_SPHERE_COLOR = (255, 255, 255) # Low alpha handled in draw
TEXT_COLOR = (200, 200, 200)

class SimulationState:
    def __init__(self):
        self.mass = 30.0
        self.spin = 0.9  # Kerr spin parameter a (0 to 1)
        self.show_horizon = True
        self.particles_schwarz = []
        self.particles_kerr = []
        self.frame_count = 0

state = SimulationState()

class Photon:
    def __init__(self, y, screen_width, is_kerr=False, hole_spin=0):
        self.pos = [0, y] # Start at x=0 (relative to canvas, will be offset)
        # We spawn them at x = -width/2 relative to center, so coordinate conversion happens later
        self.x_raw = -screen_width / 2
        self.y_raw = y
        
        self.vel = [4.0, 0.0] # vx, vy
        self.history = []
        self.active = True
        self.is_kerr = is_kerr
        self.hole_spin = hole_spin
        self.dead = False

    def update(self, mass, center_x, center_y):
        if not self.active:
            return

        # Store history for drawing trails
        self.history.append((self.x_raw + center_x, self.y_raw + center_y))
        if len(self.history) > TRAIL_LENGTH:
            self.history.pop(0)

        # Distance to center (0,0 is the black hole in physics coords)
        dx = self.x_raw
        dy = self.y_raw
        r2 = dx*dx + dy*dy
        r = math.sqrt(r2)

        # Event Horizon (Schwarzschild Radius)
        Rs = 2 * mass

        # Collision check
        if r < Rs:
            self.active = False
            return

        # --- PHYSICS ENGINE ---
        rx = dx / r
        ry = dy / r

        # Angular momentum Lz = x*vy - y*vx
        Lz = dx * self.vel[1] - dy * self.vel[0]
        h2 = Lz * Lz

        # 1. Newtonian Gravity: -GM/r^2
        f_mag = -(G * mass) / r2

        # 2. General Relativity Correction: -3GM*h^2 / c^2*r^4
        # This creates the photon sphere instability
        gr_correction = -(3 * G * mass * h2) / (r**4)
        f_mag += gr_correction

        ax = f_mag * rx
        ay = f_mag * ry

        # --- KERR SPIN APPROXIMATION ---
        if self.is_kerr and self.hole_spin != 0:
            # Alignment: 1 if corotating, -1 if counter-rotating
            # We use sign of Lz vs sign of Spin
            alignment = 0
            if Lz != 0:
                alignment = (Lz / abs(Lz)) * (self.hole_spin / abs(self.hole_spin) if self.hole_spin != 0 else 0)
            
            # Frame dragging (Lense-Thirring) qualitative force
            # Tangential push: F ~ J/r^3
            drag_mag = (2 * self.hole_spin * mass) / (r**3)
            
            # Apply tangential force (-ry, rx)
            ax += -ry * drag_mag * 0.5
            ay += rx * drag_mag * 0.5

            # Modify effective potential based on alignment
            # Prograde (aligned) can get closer; Retrograde is pushed away effectively
            spin_factor = 1.0 - (alignment * 0.3 * abs(self.hole_spin))
            
            # Adjust the GR correction strength based on spin direction
            gr_diff = gr_correction * (spin_factor - 1.0)
            ax += gr_diff * rx
            ay += gr_diff * ry

        # Integration (Euler)
        self.vel[0] += ax * DT
        self.vel[1] += ay * DT
        
        self.x_raw += self.vel[0] * DT
        self.y_raw += self.vel[1] * DT

        # Kill if too far
        if math.sqrt(self.x_raw**2 + self.y_raw**2) > WIDTH:
            self.dead = True

    def draw(self, surface, color):
        if len(self.history) < 2:
            return
        
        # Draw trail
        pygame.draw.lines(surface, color, False, self.history, 2)
        
        # Draw head
        if self.active:
            head_x = int(self.x_raw + surface.get_width()//2)
            head_y = int(self.y_raw + surface.get_height()//2)
            pygame.draw.circle(surface, WHITE, (head_x, head_y), 2)


def draw_black_hole(surface, width, height, is_kerr):
    cx, cy = width // 2, height // 2
    Rs = 2 * state.mass
    
    # 1. Event Horizon
    pygame.draw.circle(surface, HORIZON_COLOR, (cx, cy), int(Rs))
    pygame.draw.circle(surface, (150, 0, 200) if is_kerr else WHITE, (cx, cy), int(Rs), 2)

    # 2. Photon Sphere (1.5 Rs)
    if state.show_horizon:
        ps_radius = int(Rs * 1.5)
        # Pygame doesn't support dashed lines natively easily, so we draw a thin alpha circle
        s = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.circle(s, (255, 255, 255, 50), (cx, cy), ps_radius, 1)
        surface.blit(s, (0, 0))

    # 3. Label
    font = pygame.font.SysFont("monospace", 16)
    label = f"KERR (SPIN a={state.spin})" if is_kerr else "SCHWARZSCHILD (STATIC)"
    text = font.render(label, True, WHITE)
    surface.blit(text, (20, 20))

    # 4. Spin Arrow for Kerr
    if is_kerr:
        arrow_radius = Rs + 20
        start_angle = math.pi 
        end_angle = -math.pi / 2
        # Pygame arc takes a rect and angles in radians
        rect = pygame.Rect(cx - arrow_radius, cy - arrow_radius, arrow_radius*2, arrow_radius*2)
        pygame.draw.arc(surface, (200, 0, 255), rect, 0, math.pi*1.5, 3)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Black Hole Geodesic Simulation")
    clock = pygame.time.Clock()

    # Create sub-surfaces for split screen
    rect_top = pygame.Rect(0, 0, WIDTH, HALF_HEIGHT)
    rect_bot = pygame.Rect(0, HALF_HEIGHT, WIDTH, HALF_HEIGHT)
    
    # Fonts
    font_ui = pygame.font.SysFont("Arial", 14)

    running = True
    while running:
        # --- Input Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: # Reset
                    state.particles_schwarz = []
                    state.particles_kerr = []
                if event.key == pygame.K_h: # Toggle Horizon
                    state.show_horizon = not state.show_horizon
                if event.key == pygame.K_UP:
                    state.mass = min(state.mass + 5, 100)
                if event.key == pygame.K_DOWN:
                    state.mass = max(state.mass - 5, 10)
                if event.key == pygame.K_RIGHT:
                    state.spin = min(state.spin + 0.1, 1.0)
                if event.key == pygame.K_LEFT:
                    state.spin = max(state.spin - 0.1, -1.0)

        # --- Spawning ---
        state.frame_count += 1
        if state.frame_count % SPAWN_RATE == 0:
            # Spawn columns
            for y_off in range(-100, 101, 10):
                # Top (Schwarzschild)
                p_s = Photon(y_off, WIDTH, is_kerr=False)
                state.particles_schwarz.append(p_s)
                
                # Bottom (Kerr)
                p_k = Photon(y_off, WIDTH, is_kerr=True, hole_spin=state.spin)
                state.particles_kerr.append(p_k)

        # --- Updates ---
        # Top
        for p in state.particles_schwarz:
            p.update(state.mass, 0, 0) # Center is 0,0 relative to particle logic
        state.particles_schwarz = [p for p in state.particles_schwarz if not p.dead]

        # Bottom
        for p in state.particles_kerr:
            p.hole_spin = state.spin # Update spin in real-time
            p.update(state.mass, 0, 0)
        state.particles_kerr = [p for p in state.particles_kerr if not p.dead]

        # --- Drawing ---
        screen.fill(BLACK)

        # Top Surface
        surf_top = screen.subsurface(rect_top)
        surf_top.fill(BLACK)
        draw_black_hole(surf_top, WIDTH, HALF_HEIGHT, False)
        for p in state.particles_schwarz:
            p.draw(surf_top, SCHWARZ_COLOR)
        
        # Divider Line
        pygame.draw.line(screen, (50, 50, 50), (0, HALF_HEIGHT), (WIDTH, HALF_HEIGHT), 2)

        # Bottom Surface
        surf_bot = screen.subsurface(rect_bot)
        surf_bot.fill(BLACK)
        draw_black_hole(surf_bot, WIDTH, HALF_HEIGHT, True)
        for p in state.particles_kerr:
            p.draw(surf_bot, KERR_COLOR)

        # --- UI Overlay ---
        controls_text = [
            f"Mass (UP/DWN): {state.mass}",
            f"Spin (LFT/RGT): {state.spin:.1f}",
            "Reset Rays: 'R'",
            "Toggle Horizon: 'H'"
        ]
        
        for i, line in enumerate(controls_text):
            txt_surf = font_ui.render(line, True, TEXT_COLOR)
            screen.blit(txt_surf, (WIDTH - 160, 20 + i * 20))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
