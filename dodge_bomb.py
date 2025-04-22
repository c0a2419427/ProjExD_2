import os
import random
import sys
import pygame as pg
import time

WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def gameover(screen: pg.Surface, img1: pg.Surface) -> None:
    black_surf = pg.Surface((WIDTH, HEIGHT))
    black_surf.set_alpha(128)  # 半透明（0=透明, 255=不透明）
    black_surf.fill((0, 0, 0))  # 黒で塗る
    screen.blit(black_surf, (0, 0))
    screen.blit(img1, (250, 300))  # img1を表示
    screen.blit(img1, (800, 300))
    font = pg.font.Font(None, 80)
    txt = font.render("Game Over", True, (255, 255, 255))
    screen.blit(txt, (400, 300))
    pg.display.update()
    time.sleep(5)

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()

    # 初期化
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect(center=(300, 200))

    # 爆弾
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect(center=(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
    vx, vy = +5, +5

    # ゲームオーバー画像
    img1 = pg.image.load("fig/4.png")

    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(bg_img, (0, 0))

        # 衝突判定
        if kk_rct.colliderect(bb_rct):
            gameover(screen, img1)
            return

        # こうかとん移動
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        # 爆弾移動
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
