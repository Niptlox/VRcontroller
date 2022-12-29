from typing import List

import pygame as pg
from pygame.math import Vector2

WSIZE = (720, 480)

screen = pg.display.set_mode(WSIZE)

point_r = 6


def intrpolation_logranje(points, x):
    res = 0
    for i in range(len(points)):
        mul = 1
        for k in range(len(points)):
            if k == i:
                continue
            mul *= ((x - points[k].x) / (points[i].x - points[k].x)) if points[i].x != points[k].x else 1
        res += points[i].y * mul
    return res


class Line:
    def __init__(self, points):
        self.points: List[Vector2] = points

    def draw(self, surface, color="red", colorl="white"):
        last_point = None
        i = 0
        for point in self.points:
            pg.draw.circle(surface, color, point, point_r, 2)
            if last_point:
                pg.draw.line(surface, color, point, last_point, 2,)
            last_point = point
            i += 1
            color = colorl



def main():
    fps = 600
    line_1 = Line([Vector2(50, 200), Vector2(300, 200)])
    line_2 = Line([Vector2(10, 20), Vector2(20, 20)])
    lines = [line_1, line_2]
    grabbed_point: Vector2 = None
    clock = pg.time.Clock()
    running = True
    while running:
        vec1: Vector2 =( line_1.points[1] - line_1.points[0]).normalize()
        vec2 = (line_2.points[1] - line_2.points[0]).normalize()
        pg.display.set_caption(f"{vec1.dot(vec2)}; fps: {int(clock.get_fps())}")
        clock.tick(fps)
        screen.fill("black")
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                # if event.button == pg.BUTTON_MIDDLE:
                #     spline.points.append(Vector2(event.pos))
                if event.button == pg.BUTTON_LEFT and grabbed_point is None:
                    i = 0
                    for line in lines:
                        for point in line.points:
                            if pg.Rect(point.x - point_r, point.y - point_r, point_r * 2, point_r * 2).collidepoint(
                                    event.pos):
                                if pg.key.get_pressed()[pg.K_DELETE]:
                                    del line.points[i]
                                    break
                                grabbed_point = point
                                break
                            i += 1
            elif event.type == pg.MOUSEMOTION:
                if grabbed_point:
                    grabbed_point.xy = event.pos
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == pg.BUTTON_LEFT and grabbed_point:
                    grabbed_point = None
        for line in lines:
            line.draw(surface=screen)
        pg.display.flip()


if __name__ == '__main__':
    main()
