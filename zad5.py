import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

viewer = [0.0, 0.0, 10.0]

theta = 0.0
phi = 0.0
pix2angle = 1.0
scale = 1.0

left_mouse_button_pressed = 0
right_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0

R = 25.0

upY = 1.0
n = 20
vertices = np.zeros((n + 1, n + 1, 3))
matrixColor = np.zeros((n + 1, n + 1, 3))

# Metoda rysujaca lancuch torusow
def drawChain():
    drawTorus(1.0, 1.0, 1.0, -12.0)
    drawTorus(1.0, 0.0, 0.0, -8.0)
    drawTorus(0.0, 1.0, 0.0, -4.0)
    drawTorus(0.0, 0.0, 1.0, 0.0)
    drawTorus(1.0, 1.0, 0.0, 4.0)
    drawTorus(1.0, 0.0, 1.0, 8.0)
    drawTorus(0.0, 1.0, 1.0, 12.0)

# Metoda wypelniajaca tablice vertices wspolrzednymi wierzcholkow torusa
def torusVertices():
    for i in range(0, n + 1):
        for j in range(0, n + 1):
            u = i / n
            v = j / n
            R = 3
            r = 1
            vertices[i][j][0] = (R + r * np.cos(2 * np.pi * v)) * np.cos(2 * np.pi * u)
            vertices[i][j][1] = (R + r * np.cos(2 * np.pi * v)) * np.sin(2 * np.pi * u)
            vertices[i][j][2] = r * np.sin(2 * np.pi * v)

# Metoda do wyrysowania pojedynczego torusa
def drawTorus(r, g, b, c):
    spin(90)
    glColor3f(r, g, b)
    for i in range(n):
        for j in range(n):
            glBegin(GL_LINES)
            glVertex3f(vertices[i][j][0], vertices[i][j][1] + c, vertices[i][j][2])
            glVertex3f(vertices[i + 1][j][0], vertices[i + 1][j][1] + c, vertices[i + 1][j][2])
            glVertex3f(vertices[i][j][0], vertices[i][j][1] + c, vertices[i][j][2])
            glVertex3f(vertices[i][j + 1][0], vertices[i][j + 1][1] + c, vertices[i][j + 1][2])
            glEnd()


def render(time):
    global theta
    global phi
    global R
    global upY

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        theta = theta % 360
        phi += delta_y * pix2angle
        phi = phi % 360

    if right_mouse_button_pressed:
        R += delta_x * 0.01
        R = max(5.0, min(R, 25.0))

    x_eye = R * np.cos(theta * np.pi / 180) * np.cos(phi * np.pi / 180)
    y_eye = R * np.sin(phi * np.pi / 180)
    z_eye = R * np.sin(theta * np.pi / 180) * np.cos(phi * np.pi / 180)

    # Ograniczenie zakresu phi do (-180; 180]
    if phi > 180:
        phi -= 360
    elif phi <= -180:
        phi += 360

    # Wartosc parametru upY w zaleznosci od wartosci phi
    if phi < -90 or phi > 90:
        upY = -1.0
    else:
        upY = 1.0

    gluLookAt(x_eye, y_eye, z_eye, 0.0, 0.0, 0.0, 0.0, upY, 0.0)

    axes()
    drawChain()
    glFlush()


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed
    global right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0

    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = 1
    else:
        right_mouse_button_pressed = 0


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old
    global delta_y
    global mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global e_button_state

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)
    torusVertices()
    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


def axes():
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-7.5, 0.0, 0.0)
    glVertex3f(7.5, 0.0, 0.0)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -7.5, 0.0)
    glVertex3f(0.0, 7.5, 0.0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -7.5)
    glVertex3f(0.0, 0.0, 7.5)
    glEnd()


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


if __name__ == '__main__':
    main()
