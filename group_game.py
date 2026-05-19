import os
import sys
import pygame as pg
import random
import time

WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP:(0,-5),
         pg.K_DOWN:(0,+5),
         pg.K_LEFT:(-5,0),
         pg.K_RIGHT:(+5,0),
         }
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct:pg.Rect) -> tuple[bool,bool]:

    yoko, tate = True,True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko,tate

def game_over(screen: pg.Surface) -> None: # 演習1
    black_screen = pg.Surface((WIDTH,HEIGHT))
    pg.draw.rect(black_screen,(0,0,0),(0,0,WIDTH,HEIGHT))
    black_screen.set_alpha(150)
    font = pg.font.Font(None,80)
    txt = font.render("Game Over",True,(255,255,255))
    screen.blit(black_screen, [0,0])
    screen.blit(txt,[WIDTH//2 - 140, HEIGHT//2 - 50])
    kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"),0,1.5)
    screen.blit(kk_img, [WIDTH//2 - 240, HEIGHT//2 - 80])
    screen.blit(kk_img, [WIDTH//2 + 220, HEIGHT//2 - 80])
    pg.display.update()
    time.sleep(5)


def draw_stopwatch(screen: pg.Surface, elapsed_sec: int) -> None:
    font = pg.font.Font(None, 50)
    txt = font.render(f"Time: {elapsed_sec}", True, (255, 255, 255))
    txt_rct = txt.get_rect()
    txt_rct.topright = (WIDTH - 10, 10)

    bg = pg.Surface((txt_rct.width + 10, txt_rct.height + 6))
    bg.set_alpha(120)
    bg.fill((0, 0, 0))
    screen.blit(bg, (txt_rct.left - 5, txt_rct.top - 3))
    screen.blit(txt, txt_rct)

def main():
    pg.display.set_caption("GROUP_08 落ち物キャッチゲーム")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    

    clock = pg.time.Clock()
    tmr = 0        

    start_time = pg.time.get_ticks()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        elapsed_ms = pg.time.get_ticks() - start_time
        elapsed_sec = elapsed_ms // 1000

        screen.blit(bg_img, [0, 0])


        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])

        screen.blit(kk_img, kk_rct)

        draw_stopwatch(screen, elapsed_sec)

        
        pg.display.update()
        tmr += 1
        clock.tick(50)



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
