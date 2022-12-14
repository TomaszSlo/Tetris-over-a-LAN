import pygame
from network import Network
from tetris import Tetris, colors

width = 400
height = 460
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

clientNumber = 0

def main():
    run = True
    done = False
    fps = 25
    counter = 0

    n = Network()
    game = n.getP()
    clock = pygame.time.Clock()

    pressing_down = False
    pygame.init()
    while not done:
        p2 = n.send(game)

        if not p2.connected():
            screen.fill((30, 30, 30))
            font = pygame.font.SysFont("Calibri", 40)
            text = font.render("Wait for a player!", 1, (255,0,0))
            screen.blit(text, (50, 200))
            pygame.display.update()
            continue

        if game.figure is None:
            game.new_figure()
        counter += 1
        if counter > 100000:
            counter = 0

        if counter % (fps // game.level // 2) == 0 or pressing_down:
            if game.state == "start":
                game.go_down()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.rotate()
                if event.key == pygame.K_DOWN:
                    pressing_down = True
                if event.key == pygame.K_LEFT:
                    game.go_side(-1)
                if event.key == pygame.K_RIGHT:
                    game.go_side(1)
                if event.key == pygame.K_SPACE:
                    game.go_space()
                if event.key == pygame.K_ESCAPE:
                    game.__init__(20, 10)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    pressing_down = False

        screen.fill((30, 30, 30))

        for i in range(game.height):
            for j in range(game.width):
                pygame.draw.rect(screen, (51, 51, 51),
                                 [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
                if game.field[i][j] > 0:
                    pygame.draw.rect(screen, colors[game.field[i][j]],
                                     [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2,
                                      game.zoom - 1])

        if game.figure is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in game.figure.image():
                        pygame.draw.rect(screen, colors[game.figure.color],
                                         [game.x + game.zoom * (j + game.figure.x) + 1,
                                          game.y + game.zoom * (i + game.figure.y) + 1,
                                          game.zoom - 2, game.zoom - 2])
        font = pygame.font.SysFont('Calibri', 23, True, False)
        font1 = pygame.font.SysFont('Calibri', 60, True, False)

        tetris_text = font1.render("TETRIS", True, (255, 125, 0))
        score1_text = font.render("Your Score: ", True, (128, 255, 128))
        score2_text = font.render("Opponent Score: ", True, (255, 77, 77))
        score1 = font.render(str(game.score), True, (128, 255, 128))
        score2 = font.render(str(p2.score), True, (255, 77, 77))

        text_game_over = font1.render("Game Over", True, (255, 125, 0))
        text_game_over1 = font.render("Press ESC", True, (255, 0, 0))
        text_game_over2 = font.render("Wait for a opponent!", True, (255, 0, 0))
        text_win = font1.render("You WIN!", True, (128, 255, 128))
        text_lose = font1.render("You LOSE!", True, (255, 0, 0))
        text_draw = font1.render("Draw!", True, (255, 125, 0))

        screen.blit(tetris_text, [25, 0])
        screen.blit(score1_text, [220, 350])
        screen.blit(score2_text, [220, 400])
        screen.blit(score1, [220, 372])
        screen.blit(score2, [220, 422])

        if game.state == "gameover":
            if p2.state != "gameover":
                screen.fill((30, 30, 30))
                screen.blit(text_game_over, (60, 200))
                screen.blit(text_game_over2, (100, 250))

                screen.blit(score1_text, [220, 350])
                screen.blit(score2_text, [220, 400])
                screen.blit(score1, [220, 372])
                screen.blit(score2, [220, 422])
                pygame.display.update()

            if p2.state == "gameover":
                if game.get_score() > p2.get_score():
                    screen.fill((30, 30, 30))
                    screen.blit(text_win, (80, 180))
                    screen.blit(text_game_over1, (150, 230))

                    screen.blit(score1_text, [220, 350])
                    screen.blit(score2_text, [220, 400])
                    screen.blit(score1, [220, 372])
                    screen.blit(score2, [220, 422])
                    pygame.display.update()
                elif game.get_score() < p2.get_score():
                    screen.fill((30, 30, 30))
                    screen.blit(text_lose, (70, 180))
                    screen.blit(text_game_over1, (150, 230))

                    screen.blit(score1_text, [220, 350])
                    screen.blit(score2_text, [220, 400])
                    screen.blit(score1, [220, 372])
                    screen.blit(score2, [220, 422])
                    pygame.display.update()
                else:
                    screen.fill((30, 30, 30))
                    screen.blit(text_draw, (120, 180))
                    screen.blit(text_game_over1, (150, 230))

                    screen.blit(score1_text, [220, 350])
                    screen.blit(score2_text, [220, 400])
                    screen.blit(score1, [220, 372])
                    screen.blit(score2, [220, 422])
                    pygame.display.update()

        pygame.display.flip()
        clock.tick(fps)
        #pygame.quit()



def menu_screen():
    run = True
    clock = pygame.time.Clock()
    pygame.init()
    while run:
        clock.tick(60)
        screen.fill((30, 30, 30))
        font = pygame.font.SysFont("Calibri", 60)
        text = font.render("Click to Play!", 1, (255,0,0))
        screen.blit(text, (50,200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()


while True:
    menu_screen()
    break
