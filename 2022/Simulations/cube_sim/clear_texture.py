#probably not needed
import pygame

def main(all_points, dis):
    #lines per cube: [0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]
    for i in range(len(all_points)):
        for j in range(len(all_points) - 1):
            if j >= i:
                j += 1
            if all_points[i][0] == all_points[j][2]:
                print(all_points[i][1], all_points[j][3])
            if all_points[i][0] == all_points[j][2] and all_points[i][1] == all_points[i][3]:
                print(True)
                pygame.draw.line(dis, 'white', all_points[i][0], all_points[i][1])
            if all_points[i][1] == all_points[j][3] and all_points[i][2] == all_points[i][0]:
                print(True)
                pygame.draw.line(dis, 'white', all_points[i][1], all_points[i][2])
            if all_points[i][2] == all_points[j][0] and all_points[i][3] == all_points[i][1]:
                print(True)
                pygame.draw.line(dis, 'white', all_points[i][0], all_points[i][1])
            if all_points[i][3] == all_points[j][1] and all_points[i][0] == all_points[i][2]:
                print(True)
                pygame.draw.line(dis, 'white', all_points[i][1], all_points[i][2])
    