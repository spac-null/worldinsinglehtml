import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import time
import math

# Initialize Pygame and OpenGL
pygame.init()
WIDTH, HEIGHT = 1200, 600
pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL | OPENGLBLIT)
glViewport(0, 0, WIDTH, HEIGHT)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# Shaders
vertex_shader = """
#version 330
in vec3 position;
in vec3 normal;
in vec2 texCoord;
uniform mat4 mvp;
out vec2 fragTexCoord;
out vec3 fragNormal;
out vec3 fragPos;
void main() {
    gl_Position = mvp * vec4(position, 1.0);
    fragTexCoord = texCoord;
    fragNormal = normal;
    fragPos = position;
}
"""

fragment_shader = """
#version 330
in vec2 fragTexCoord;
in vec3 fragNormal;
in vec3 fragPos;
out vec4 fragColor;
uniform float time;
uniform vec2 resolution;

float perlin(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    vec2 u = f * f * (3.0 - 2.0 * f);
    float a = dot(vec2(127.1, 311.7), i);
    float b = dot(vec2(269.5, 183.3), i + vec2(1.0, 0.0));
    float c = dot(vec2(419.2, 371.9), i + vec2(0.0, 1.0));
    float d = dot(vec2(742.3, 547.7), i + vec2(1.0, 1.0));
    return mix(mix(fract(sin(a) * 43758.5453), fract(sin(b) * 43758.5453), u.x),
               mix(fract(sin(c) * 43758.5453), fract(sin(d) * 43758.5453), u.x), u.y);
}

void main() {
    vec2 uv = fragTexCoord;
    float theta = uv.x * 6.2832;  // Full circle
    float r = length(fragPos.xz);
    float n = perlin(vec2(theta * 5.0 + time * 0.2, uv.y * 10.0));
    float wave = sin(theta * 10.0 + time) * cos(fragPos.y * 5.0 + time * 0.5);
    vec3 baseColor = vec3(
        0.5 + 0.5 * sin(wave + n),
        0.5 + 0.5 * cos(wave + n + 2.0),
        0.5 + 0.5 * sin(wave + n + 4.0)
    );
    vec3 lightDir = normalize(vec3(1.0, 1.0, -1.0));
    float diff = max(dot(normalize(fragNormal), lightDir), 0.0);
    fragColor = vec4(baseColor * (0.5 + 0.5 * diff) * (1.0 - r * 0.5), 1.0);
}
"""

# Compile shaders
shader = compileProgram(
    compileShader(vertex_shader, GL_VERTEX_SHADER),
    compileShader(fragment_shader, GL_FRAGMENT_SHADER)
)

# Generate cylinder geometry
def create_cylinder(radius=1.0, height=2.0, segments=64):
    vertices = []
    indices = []
    for i in range(segments):
        theta = 2.0 * math.pi * i / segments
        theta_next = 2.0 * math.pi * (i + 1) / segments
        x, z = math.cos(theta) * radius, math.sin(theta) * radius
        x_next, z_next = math.cos(theta_next) * radius, math.sin(theta_next) * radius
        # Bottom
        vertices.extend([x, -height/2, z, x, 0, z, i/segments, 0.0])
        vertices.extend([x_next, -height/2, z_next, x_next, 0, z_next, (i+1)/segments, 0.0])
        # Top
        vertices.extend([x, height/2, z, x, 0, z, i/segments, 1.0])
        vertices.extend([x_next, height/2, z_next, x_next, 0, z_next, (i+1)/segments, 1.0])
        # Indices for two triangles per segment
        base = i * 4
        indices.extend([base, base + 1, base + 2, base + 1, base + 3, base + 2])
    return np.array(vertices, dtype=np.float32), np.array(indices, dtype=np.uint32)

vertices, indices = create_cylinder(1.0, 2.0, 64)

# VBO and IBO
vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

ibo = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

# Vertex attributes
position_loc = glGetAttribLocation(shader, "position")
normal_loc = glGetAttribLocation(shader, "normal")
texcoord_loc = glGetAttribLocation(shader, "texCoord")
glEnableVertexAttribArray(position_loc)
glEnableVertexAttribArray(normal_loc)
glEnableVertexAttribArray(texcoord_loc)
glVertexAttribPointer(position_loc, 3, GL_FLOAT, GL_FALSE, 32, None)
glVertexAttribPointer(normal_loc, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
glVertexAttribPointer(texcoord_loc, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(24))

# Uniforms
mvp_loc = glGetUniformLocation(shader, "mvp")
time_loc = glGetUniformLocation(shader, "time")
resolution_loc = glGetUniformLocation(shader, "resolution")

# Camera and projection (frustum)
def get_mvp():
    projection = np.array([
        [1.0 / (WIDTH/HEIGHT), 0, 0, 0],
        [0, 1.0, 0, 0],
        [0, 0, -1.0 / (5.0 - 1.0), -5.0 / (5.0 - 1.0)],
        [0, 0, -1.0, 0]
    ], dtype=np.float32)
    view = np.eye(4, dtype=np.float32)
    view[2, 3] = -3.0  # Move camera back
    model = np.eye(4, dtype=np.float32)
    return projection @ view @ model

# Particle system (simplified for brevity)
class Particle:
    def __init__(self):
        self.pos = np.array([random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)], dtype=np.float32)
        self.vel = np.array([random.uniform(-0.01, 0.01), random.uniform(-0.01, 0.01), random.uniform(-0.01, 0.01)], dtype=np.float32)
        self.life = 100

particles = [Particle() for _ in range(1000)]

# Main loop
glUseProgram(shader)
glUniform2f(resolution_loc, WIDTH, HEIGHT)
running = True
start_time = time.time()
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    current_time = time.time() - start_time
    glUniform1f(time_loc, current_time)

    # Update particles
    for p in particles[:]:
        p.pos += p.vel
        p.life -= 1
        if p.life <= 0:
            particles.remove(p)
            particles.append(Particle())

    # Draw cylinder
    mvp = get_mvp()
    glUniformMatrix4fv(mvp_loc, 1, GL_FALSE, mvp)
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

    # Draw particles
    glPointSize(3)
    glBegin(GL_POINTS)
    for p in particles:
        glColor4f(1.0, 1.0 - p.life/100, 0.5, p.life/100)
        glVertex3fv(p.pos)
    glEnd()

    pygame.display.flip()
    clock.tick(60)

# Cleanup
glDeleteBuffers(1, [vbo])
glDeleteBuffers(1, [ibo])
glDeleteProgram(shader)
pygame.quit()