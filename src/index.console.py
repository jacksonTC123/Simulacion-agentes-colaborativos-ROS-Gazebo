import pygame
from infrastructure.Simulacion_2D.sim2d import make_demo

if __name__ == "__main__":
    pygame.init()
    sim = make_demo(n=3)
    sim.run()
