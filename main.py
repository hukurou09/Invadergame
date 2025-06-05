import pygame
import random
import sys
import os

# ゲームの初期化
pygame.init()

# 画面サイズの設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("インベーダーゲーム")

# 色の定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# プレイヤークラス
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([50, 30])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2 - 25
        self.rect.y = SCREEN_HEIGHT - 50
        self.speed = 5
        self.bullets = pygame.sprite.Group()
        self.shoot_delay = 500  # ミリ秒
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        
        # 弾の更新
        self.bullets.update()
        
        # 画面外の弾を削除
        for bullet in self.bullets:
            if bullet.rect.bottom < 0:
                bullet.kill()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            self.bullets.add(bullet)

# 弾クラス
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([4, 10])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed

# 敵クラス
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([40, 40])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1
        self.speed = 2

    def update(self):
        self.rect.x += self.speed * self.direction

# ゲームクラス
class Game:
    def __init__(self):
        self.player = Player()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.enemies = pygame.sprite.Group()
        self.create_enemies()
        self.score = 0
        self.game_over = False
        self.font = pygame.font.SysFont(None, 36)
        self.clock = pygame.time.Clock()

    def create_enemies(self):
        # 敵を5行8列で配置
        for row in range(5):
            for column in range(8):
                enemy = Enemy(column * 80 + 50, row * 60 + 50)
                self.enemies.add(enemy)
                self.all_sprites.add(enemy)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.shoot()
                elif event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_r and self.game_over:
                    self.__init__()  # ゲームをリセット
        return True

    def run_logic(self):
        if not self.game_over:
            # プレイヤーの更新
            self.player.update()
            
            # 敵の更新
            self.enemies.update()
            
            # 敵の移動方向を変更（画面端に到達したら）
            for enemy in self.enemies:
                if enemy.rect.right >= SCREEN_WIDTH or enemy.rect.left <= 0:
                    for e in self.enemies:
                        e.direction *= -1
                        e.rect.y += 10
                    break
            
            # 弾と敵の衝突判定
            hits = pygame.sprite.groupcollide(self.enemies, self.player.bullets, True, True)
            for hit in hits:
                self.score += 100
            
            # 敵がプレイヤーに到達したらゲームオーバー
            for enemy in self.enemies:
                if enemy.rect.bottom >= SCREEN_HEIGHT - 50:
                    self.game_over = True
            
            # 敵をすべて倒したら新しい敵を作成
            if len(self.enemies) == 0:
                self.create_enemies()

    def display_frame(self):
        screen.fill(BLACK)
        
        if not self.game_over:
            self.all_sprites.draw(screen)
            self.player.bullets.draw(screen)
            
            # スコア表示
            score_text = self.font.render(f"スコア: {self.score}", True, WHITE)
            screen.blit(score_text, (10, 10))
        else:
            # ゲームオーバー画面
            game_over_text = self.font.render("ゲームオーバー", True, WHITE)
            restart_text = self.font.render("Rキーでリスタート", True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 30))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20))
        
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.process_events()
            self.run_logic()
            self.display_frame()
            self.clock.tick(60)  # 60FPS

# メイン関数
def main():
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
