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


class Item:
    """
    落下アイテムを管理するクラス。

    画面上部のランダムな位置に生成され，一定速度で落下する。
    キャラクターに触れるとスコア加算，画面下端を超えるとライフ減少のトリガーとなる。

    Attributes:
        img (pg.Surface): アイテムの画像
        rct (pg.Rect): アイテムの矩形領域（位置と大きさ）
        speed (int): 落下速度（ピクセル／フレーム）
    """

    _imgs: list[pg.Surface] = []  # 画像はクラス変数として共有（初回のみ読み込み）

    def __init__(self) -> None:
        """
        アイテムをランダムな位置・速度で初期化する。
        画像リストが空の場合のみ fig/0.png～9.png を読み込む。
        """
        if not Item._imgs:
            for i in range(10):
                img = pg.transform.rotozoom(
                    pg.image.load(f"fig/{i}.png"), 0, 0.5
                )
                Item._imgs.append(img)

        self.img: pg.Surface = random.choice(Item._imgs)
        self.rct: pg.Rect = self.img.get_rect()
        # 画面横幅内のランダムなX座標に配置
        self.rct.x = random.randint(0, WIDTH - self.rct.width)
        # 画面上端より少し上からスタート
        self.rct.y = -self.rct.height
        self.speed: int = random.randint(3, 7)

    def update(self) -> bool:
        """
        アイテムを1フレーム分落下させる。

        Returns:
            bool: 画面下端を超えた（取り逃した）場合は True，それ以外は False
        """
        self.rct.y += self.speed
        return self.rct.top > HEIGHT

    def draw(self, screen: pg.Surface) -> None:
        """
        アイテムを画面に描画する。

        Args:
            screen (pg.Surface): 描画対象のサーフェス
        """
        screen.blit(self.img, self.rct)


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

    clock = pg.time.Clock()
    tmr = 0

    # ライフオブジェクトの生成（初期ライフ数：3）
    life = Life(initial_lives=3)

    items: list[Item] = []
    ITEM_SPAWN_INTERVAL = 60  # アイテムを生成するフレーム間隔


    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

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

        # ── アイテム生成 ──────────────────────────────
        if tmr % ITEM_SPAWN_INTERVAL == 0:
            items.append(Item())

        # ── アイテム更新・当たり判定・ライフ管理 ─────────
        active_items: list[Item] = []
        for item in items:
            missed = item.update()  # 落下処理。画面外に出たら True
            if missed:
                # 画面下端を超えたアイテムは消去（ダメージなし）
                pass
            elif kk_rct.colliderect(item.rct):
                # アイテムに当たった → ライフ減少（ダメージ）
                life.decrease()
            else:
                # 画面内にある通常のアイテムは描画して保持
                active_items.append(item)
                item.draw(screen)
        items = active_items  # 当たり・画面外アイテムを除いた新リストに更新

        # ── キャラクター描画 ──────────────────────────
        screen.blit(kk_img, kk_rct)

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
