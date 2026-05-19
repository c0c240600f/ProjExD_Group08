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
    """
    引数：こうかとんRectまたは爆弾Rect
    戻り数:タプル

    """
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


class Item(pg.sprite.Sprite):
    """
    得点アイテムに関するクラス
    """
    image = [pg.image.load("./fig/coin.png"), pg.image.load("./fig/ame.jpg")] # アイテムの画像をリストで管理

    def __init__ (self):
        super().__init__()
        self.image = pg.transform.scale(random.choice(__class__.image),(40, 40)) #  アイテムの画像をランダムに選択してサイズを変更
        self.rect = self.image.get_rect()
        self.rect.center = random.randint(0, WIDTH), 0
        self.vy = 5  # アイテムの落下速度

    def update(self):
        """
        アイテムを落下させる関数
        """
        self.rect.move_ip(0, self.vy)
        if self.rect.top > HEIGHT:
            self.kill()  # アイテムが画面外に出たら削除する


class Score:
    """
    スコアを管理するクラス
    """
    def __init__(self):
        self.value = 0
        self.font = pg.font.Font(None, 36)
        self.color = (0, 0, 255)
        self.value = 0
        self.image = self.font.render(f"Score: {self.value}", 0, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = 100, HEIGHT-50

    def update(self, screen: pg.Surface):
        """
        スコアを更新して画面に表示する関数
        """
        self.image = self.font.render(f"Score: {self.value}", 0, self.color)
        screen.blit(self.image, self.rect)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    items = pg.sprite.Group()  # アイテムを管理するグループ
    score = Score()  # スコア管理のインスタンスを作成

    clock = pg.time.Clock()
    tmr = 0         

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return

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

        if tmr % 300 == 0:  # 300フレームごとにアイテムを生成する
            item = Item()
            items.add(item)

        # アイテムとこうかとんの衝突判定
        for item in items:
            if kk_rct.colliderect(item.rect):
                score.value += 5  #  スコアを加算する
                item.kill()  # アイテムを削除する
        
        items.update()
        items.draw(screen)
        score.update(screen)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
