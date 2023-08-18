from pygame import*
from random import randint
init()

W = 500
H = 700

window = display.set_mode((W, H))
display.set_caption("Shooter")
display.set_icon(image.load("rocket.png"))

back = transform.scale(image.load('Skyy.jpg'), (W, H))
# clock = time.Clock()
# Зміни для підрахунку пропущених, вбитих,
lost = 0
killed = 0
life = 5
"""  ЗВУКИ  """
mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.3) 
fire = mixer.Sound('fire.ogg')
mixer.music.play()

"""  ШРИФТИ  """
font.init()
font1 = font.SysFont("Arial", 20)
font2 = font.SysFont("Arial", 60, bold=True)


"""  КЛАСИ  """
# клас-батько для інших спрайтів
class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # викликаємо конструктор класу (Sprite):
        super().__init__()
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        # кожен спрайт повинен зберігати власти
# кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    # метод, що малює героя у вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):

    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < W - 80:
    
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("dult.png", self.rect.centerx, self.rect.top, 15, 20, 10)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > H:
            self.rect.y = 0
            self.rect.x = randint(0, W - 80 )
            lost +=1


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
class Asteroid(Enemy):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > H:
            self.rect.y = 0
            self.rect.x = randint(0, W - 80 )

player = Player("rocket.png", W/2, H-100, 80, 100, 10) # гравець
monsters = sprite.Group() # створення групи спрайтів
bullets = sprite.Group()
asteroids = sprite.Group()

for i in range(5):# створюємо ворогів та добавити в групу
    monster = Enemy("Shahed_136.png", randint(0, W-80),-50, 80, 50, randint(1, 3))
    monsters.add(monster)

for i in range(3):
    asteroid = Asteroid("asteroid.png", randint(0, W-80), randint(-50, 0), 80, 50, randint(1, 3))
    asteroids.add(asteroid)

game = True
finish = False
while game:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
                fire.play() 
    if not finish:  
        window.blit(back, (0, 0))
        player.reset()
        player.update()

        monsters.draw(window)# малюємо групу ворогів
        monsters.update()# запускаємо рух ворогів
        bullets.draw(window)# 
        bullets .update()# 
        asteroids.draw(window)# 
        asteroids.update()#  

        lost_txt = font1.render("Пропущено: " + str(lost), 1, (255,255, 255)) # текст пропущено
        window.blit(lost_txt, (10, 10)) # відображення тексту
        killed_txt = font1.render("Збито: " + str(killed), 1, (255,255, 255)) 
        window.blit(killed_txt, (10, 45))
        life_txt = font1.render(str(life), 1, (255,255, 255)) 
        window.blit(life_txt, (450, 5))

        if sprite.spritecollide(player, monsters, True):
            life -=1
            monster = Enemy("Shahed_136.png", randint(0, W - 80), -50, 80, 50, randint(1, 3))
            monsters.add(monster)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for col in collides:
            monster = Enemy("Shahed_136.png", randint(0, W - 80), -50, 80, 50, randint(1, 3))
            monsters.add(monster)
            killed += 1
        if killed >= 10:
            win = font2.render("Ти виграв!!!", True, (0, 225, 0 ))
            window.blit(win, (W/2-150, H/2))
            finish = True
        if life == 0 or lost >= 5:
            lose = font2.render("Ти програв!!!", True, (0, 225, 0 ))
            window.blit(lose, (W/2-150, H/2))
            finish = True
        if sprite.spritecollide(player, asteroids, True):
            life -=1
            asteroid = Asteroid("asteroid.png", randint(0, W - 80), randint(-50, 0), 80, 50, randint(1, 3))
            asteroids.add(asteroid)
    else:
        keys_pressed = key.get_pressed()
        if keys_pressed[K_r]:
            life = 5
            killed = 0
            lost = 0
            for m in monsters:
                m.kill()
            for b in bullets:
                b.kill()
            for i in range(5):# створюємо ворогів та добавити в групу
                monster = Enemy("Shahed_136.png", randint(0, W-80),-50, 80, 50, randint(1, 3))
                monsters.add(monster)
            finish = False
    display.update()