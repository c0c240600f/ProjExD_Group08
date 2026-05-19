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


class Poison(pg.sprite.Sprite):
    def __init__(self, surface: pg.Surface, x: int, y: int, speed: int = 2):
        """毒アイテムを初期化する関数

        Args:
            surface (pg.Surface): 画面のSurface
            x (int): 毒アイテムのX座標
            y (int): 毒アイテムのY座標
            speed (int, optional): 落下スピード、デフォルト値2
        """
        super().__init__()
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = +5
        self.scale = random.uniform(0.3, 0.5)
        self.speed = speed
        # 毒アイテムの画像を複数にしてみる
        self.image_list = ["./fig/poison.png", "./fig/poison1.png"]
        self.image = pg.transform.rotozoom(pg.image.load(self.image_list[random.randint(0, len(self.image_list) - 1)]), 0, self.scale)
        self.screen = surface
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x
        self.rect.centery = self.y
        
    def update(self):
        """毒アイテムの更新関数
        """
        self.rect.move_ip(self.speed*self.vx, self.speed*self.vy)
        self.x = self.rect.centerx
        self.y = self.rect.centery

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

    # 毒アイテムのリスト
    poisons = pg.sprite.Group()
    # 毒アイテムの速度(倍率)
    poison_speed = 1
    # 毒アイテムの出現頻度(フレーム)
    poison_spwan_rate = 150

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

        if tmr % 150 == 0:
            # 毒アイテムの速度を徐々に上げる
            poison_speed += 0.25
            print(poison_speed)
            # 毒アイテムの出現頻度を徐々に上げる(下限あり)
            if poison_spwan_rate > 25:
                poison_spwan_rate -= 10
            else:
                pass
            print(poison_spwan_rate)


        if tmr % poison_spwan_rate  == 0:
            poisons.add(Poison(screen, random.randint(0, WIDTH), -100, poison_speed))

        screen.blit(kk_img, kk_rct)

        draw_stopwatch(screen, elapsed_sec)

        
        poisons.draw(screen)
        poisons.update()

        #毒アイテムにあたってしまった時の処理
        for poison in poisons:
            if kk_rct.colliderect(poison.rect):
                # ここにライフ減算処理いれたい
                poisons.remove(poison)
            
            #画面外に行ったら消去
            if poison.y - poison.image.height * poison.scale  > HEIGHT:
                poisons.remove(poison)

        pg.display.update()
        tmr += 1
        clock.tick(50)



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
