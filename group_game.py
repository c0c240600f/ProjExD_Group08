import os
import sys
import pygame as pg
import random
import time

WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    矩形が画面内に収まっているか確認する。

    Args:
        rct (pg.Rect): 確認対象の矩形

    Returns:
        tuple[bool, bool]: (横方向に収まっているか, 縦方向に収まっているか)
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def game_over(screen: pg.Surface) -> None:
    """
    ゲームオーバー画面を表示する。
    半透明の黒画面とテキストを重ねて表示し、5秒後に終了する。

    Args:
        screen (pg.Surface): 描画対象のサーフェス
    """
    black_screen = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(black_screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    black_screen.set_alpha(150)
    font = pg.font.Font(None, 80)
    txt = font.render("Game Over", True, (255, 255, 255))
    screen.blit(black_screen, [0, 0])
    screen.blit(txt, [WIDTH // 2 - 140, HEIGHT // 2 - 50])
    kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 1.5)
    screen.blit(kk_img, [WIDTH // 2 - 240, HEIGHT // 2 - 80])
    screen.blit(kk_img, [WIDTH // 2 + 220, HEIGHT // 2 - 80])
    pg.display.update()
    time.sleep(5)


class Life:
    """
    プレイヤーのライフ（残機）を管理するクラス。

    ライフ数をこうかとんのアイコンとして画面左上に表示する。
    アイテムを取り逃すごとにライフが1減少し，0になるとゲームオーバーとなる。

    Attributes:
        lives (int): 現在のライフ数
        max_lives (int): 最大ライフ数
        heart_img (pg.Surface): ライフアイコン用の画像
        font (pg.font.Font): 「LIFE:」ラベル描画用フォント
    """

    def __init__(self, initial_lives: int = 3) -> None:
        """
        ライフオブジェクトを初期化する。

        Args:
            initial_lives (int): 初期ライフ数。デフォルトは 3。
        """
        self.lives: int = initial_lives
        self.max_lives: int = initial_lives
        # こうかとんの画像をライフアイコンとして流用
        self.heart_img: pg.Surface = pg.transform.rotozoom(
            pg.image.load("fig/3.png"), 0, 0.4
        )
        self.font: pg.font.Font = pg.font.SysFont(None, 45)

    def decrease(self) -> None:
        """ライフを1つ減らす。0以下にはならない。"""
        if self.lives > 0:
            self.lives -= 1

    def is_alive(self) -> bool:
        """
        ライフが残っているか確認する。

        Returns:
            bool: ライフが1以上あれば True，0なら False
        """
        return self.lives > 0

    def get_lives(self) -> int:
        """
        現在のライフ数を返す。

        Returns:
            int: 現在のライフ数
        """
        return self.lives

    def draw(self, screen: pg.Surface) -> None:
        """
        ライフ数をアイコンで画面左上に描画する。
        「LIFE:」ラベルの右に，残ライフ数だけアイコンを横並びで表示する。

        Args:
            screen (pg.Surface): 描画対象のサーフェス
        """
        # 「LIFE:」ラベルを赤文字で表示
        label = self.font.render("LIFE:", True, (255, 50, 50))
        screen.blit(label, (10, 10))
        # 残ライフ数のぶんだけアイコンを横に並べる
        for i in range(self.lives):
            screen.blit(self.heart_img, (100 + i * 55, 5))


def main() -> None:
    """ゲームのメインループ。初期化・更新・描画を毎フレーム処理する。"""
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

    # ライフオブジェクトの生成（初期ライフ数：3）
    life = Life(initial_lives=3)

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

        # ライフが0になったらゲームオーバー処理を呼び出して終了
        if not life.is_alive():
            game_over(screen)
            return

        screen.blit(bg_img, [0, 0])

        # ── キャラクター移動 ──────────────────────────
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        # 画面外に出た場合は元の位置に戻す
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        # ── UI 描画（ライフ・スコア）────────────────────
        life.draw(screen)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
