import pygame
import moderngl
import struct
import time
import os
import urllib.request

# --- CONFIGURATION ---
WIDTH, HEIGHT = 1280, 720
BH_RADIUS = 1.0
IMG_URL = "https://www.krqe.com/wp-content/uploads/sites/12/2022/12/AdobeStock_81556974.jpeg?w=2560&h=1440&crop=1"
IMG_FILENAME = "galaxy.jpg"

# --- HELPER: AUTO-DOWNLOAD TEXTURE ---
def ensure_texture_exists():
    if not os.path.exists(IMG_FILENAME):
        print(f"Downloading galaxy texture from {IMG_URL}...")
        try:
            # Fake a user agent so the server doesn't block the script
            req = urllib.request.Request(
                IMG_URL, 
                data=None, 
                headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
            )
            with urllib.request.urlopen(req) as response, open(IMG_FILENAME, 'wb') as out_file:
                out_file.write(response.read())
            print("Download complete.")
        except Exception as e:
            print(f"Failed to download image: {e}")
            print("Will generate noise fallback.")

# --- SHADERS (GLSL) ---
vertex_shader = '''
#version 330
in vec2 in_vert;
void main() {
    gl_Position = vec4(in_vert, 0.0, 1.0);
}
'''

fragment_shader = '''
#version 330
uniform vec2 u_resolution;
// uniform float u_time; // REMOVED: Unused variable caused KeyError
uniform vec2 u_mouse;
uniform float u_zoom;
uniform sampler2D u_skybox;

out vec4 f_color;

#define MAX_STEPS 80 
#define BH_RADIUS 1.0
#define PI 3.14159265359

vec3 getSkybox(vec3 dir) {
    float u = 0.5 + atan(dir.z, dir.x) / (2.0 * PI);
    float v = 0.5 - asin(dir.y) / PI;
    return texture(u_skybox, vec2(u, v)).rgb;
}

void main() {
    vec2 uv = (gl_FragCoord.xy - 0.5 * u_resolution.xy) / u_resolution.y;

    float camDist = 12.0 / u_zoom;
    
    // Mouse Interaction
    float angleX = (u_mouse.x / u_resolution.x) * 6.28;
    float angleY = ((u_mouse.y / u_resolution.y) - 0.5) * 3.0;
    angleY = clamp(angleY, -1.5, 1.5);

    vec3 ro = vec3(camDist * sin(angleX) * cos(angleY), 
                   camDist * sin(angleY), 
                   camDist * cos(angleX) * cos(angleY));
    
    vec3 target = vec3(0.0, 0.0, 0.0);
    
    vec3 ww = normalize(target - ro);
    vec3 uu = normalize(cross(ww, vec3(0.0, 1.0, 0.0)));
    vec3 vv = normalize(cross(uu, ww));
    
    vec3 rd = normalize(uv.x * uu + uv.y * vv + 1.2 * ww);

    // Physics Loop
    vec3 pos = ro;
    vec3 dir = rd;
    bool escaped = true;

    for(int i = 0; i < MAX_STEPS; i++) {
        float r = length(pos);
        if(r < BH_RADIUS) {
            escaped = false;
            break;
        }

        // Gravity
        float h = max(0.05, r * 0.1); 
        vec3 force = -normalize(pos) * (3.0 / (r * r)); 
        
        dir += force * h;
        dir = normalize(dir);
        pos += dir * h;
        
        if(r > 1000.0) break;
    }

    vec3 col = vec3(0.0);
    if(escaped) {
        col = getSkybox(dir);
    } 
    
    f_color = vec4(col, 1.0);
}
'''

# --- SETUP ---
ensure_texture_exists() # Download image if needed

pygame.init()
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)
ctx = moderngl.create_context()

# Quad for full screen rendering
vertices = [
    -1.0, -1.0,
    1.0, -1.0,
    -1.0, 1.0,
    1.0, 1.0,
]
vbo = ctx.buffer(struct.pack('8f', *vertices))
prog = ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
vao = ctx.vertex_array(prog, [(vbo, '2f', 'in_vert')])

# --- TEXTURE LOADING ---
def load_texture(ctx, path):
    if not os.path.exists(path):
        # Generate noise texture if file missing
        print("Image not found (download failed?), generating noise...")
        return ctx.texture((512, 512), 3, os.urandom(512*512*3))
    
    try:
        img = pygame.image.load(path)
    except pygame.error:
        print("File exists but Pygame couldn't read it. Corrupt? Generating noise.")
        return ctx.texture((512, 512), 3, os.urandom(512*512*3))

    img = pygame.transform.flip(img, False, True) # OpenGL flips Y
    texture_data = pygame.image.tostring(img, "RGB")
    texture = ctx.texture(img.get_size(), 3, texture_data)
    texture.build_mipmaps()
    texture.filter = (moderngl.LINEAR_MIPMAP_LINEAR, moderngl.LINEAR)
    return texture

# Load 'galaxy.jpg' or fallback
texture = load_texture(ctx, IMG_FILENAME)
texture.use(location=0)

# --- UNIFORMS ---
u_resolution = prog['u_resolution']
# u_time = prog['u_time'] # REMOVED
u_mouse = prog['u_mouse']
u_zoom = prog['u_zoom']
u_skybox = prog['u_skybox']

u_skybox.value = 0 # Texture unit 0
u_resolution.value = (WIDTH, HEIGHT)
u_zoom.value = 1.0

# --- MAIN LOOP ---
running = True
clock = pygame.time.Clock()
zoom = 1.0
mouse_x, mouse_y = WIDTH/2, HEIGHT/2
dragging = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            ctx.viewport = (0, 0, WIDTH, HEIGHT)
            u_resolution.value = (WIDTH, HEIGHT)
        
        # Mouse Interaction
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: dragging = True
            if event.button == 4: zoom = min(zoom + 0.5, 10.0)
            if event.button == 5: zoom = max(zoom - 0.5, 0.1)
            u_zoom.value = zoom
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_x += event.rel[0]
                mouse_y += event.rel[1]
                # OpenGL coordinates are bottom-left, pygame is top-left
                u_mouse.value = (mouse_x, HEIGHT - mouse_y)

    # Render
    # u_time.value = time.time() - start_time # REMOVED
    
    ctx.clear(0.0, 0.0, 0.0)
    vao.render(moderngl.TRIANGLE_STRIP)
    
    pygame.display.flip()
    clock.tick(60)
    pygame.display.set_caption(f"GPU Black Hole - FPS: {clock.get_fps():.2f}")

pygame.quit()
