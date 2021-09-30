import pygame, random

WIDTH = 800
HEIGHT = 600


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BULLE HELL")
clock = pygame.time.Clock()

def show_go_screen():
  inicio = pygame.image.load("backgroud_inicio.png")
  screen.blit(inicio, [0, 0])
  draw_text(screen,"BULLET HELL",65, WIDTH // 2, HEIGHT / 4)
  draw_text(screen, "(Instrucción)", 27, WIDTH // 2, HEIGHT // 2)
  draw_text(screen, "Presiona una tecla", 17, WIDTH // 2, HEIGHT * 3/4)
  pygame.display.flip()
  waiting = True
  while waiting:
    clock.tick(60)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
      if event.type == pygame.KEYUP:
        waiting = False

def gameOver_screen():
  player.shield = 150
  game_over = pygame.image.load("game_over.png")
  screen.blit(game_over, [0, 0])
  draw_text(screen, str(player.score), 25, WIDTH // 2, 10)
  pygame.display.flip()
  waiting = True
  while waiting:
    clock.tick(60)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
      if event.type == pygame.KEYUP:
        waiting = False

def draw_text(surface, text, size, x, y):
  font = pygame.font.SysFont("serif", size)
  text_surface = font.render(text, True, (255, 255, 255))
  text_rect = text_surface.get_rect()
  text_rect.midtop = (x, y)
  surface.blit(text_surface, text_rect)


def draw_shield_bar(surface, x, y, percentage):
	BAR_LENGHT = 150
	BAR_HEIGHT = 10
	fill = (percentage / 150) * BAR_LENGHT
	border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
	fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
	pygame.draw.rect(surface, GREEN, fill)
	pygame.draw.rect(surface, WHITE, border, 2)

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("ship.png")
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH // 2
		self.rect.bottom = HEIGHT - 10
		self.speed_x = 0
		self.shield = 150
		self.game_over = False
		self.score = 0

	def update(self):
		self.speed_x = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speed_x = -5
		if keystate[pygame.K_RIGHT]:
			self.speed_x = 5
		self.rect.x += self.speed_x
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0

	def shoot(self):
		bullet = Bullet(self.rect.centerx, self.rect.top)
		all_sprites.add(bullet)
		bullets.add(bullet)

		#Agregamos sonido
		laser_sound.play()
    

class Meteor(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = random.choice(meteor_images)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-100, -40)
		self.speedy = random.randrange(1, 10)
		self.speedx = random.randrange(-5, 5)

	def update(self):
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 22 :
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-100, -40)
			self.speedy = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load("shot.png")
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.centerx = x
		self.speedy = -25

	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0:
			self.kill()

class Explosion(pygame.sprite.Sprite):
	def __init__(self, center):
		super().__init__()
		self.image = explosion_anim[0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 50 # how long to wait for the next frame VELOCITY OF THE EXPLOSION

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.frame += 1
			if self.frame == len(explosion_anim):
				self.kill() # if we get to the end of the animation we don't keep going.
			else:
				center = self.rect.center
				self.image = explosion_anim[self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center

meteor_images = []
meteor_list =["A1.png","A2.png","A3.png"]


for img in meteor_list:
  meteor_images.append(pygame.image.load(img))

#---- EXPLOSION 
explosion_anim = []
for i in range(8):
	file = "E{}.png".format(i)
	img = pygame.image.load(file)
	img_scale = pygame.transform.scale(img, (70, 70))
	explosion_anim.append(img_scale)

# Cargar fondo.
background = pygame.image.load("backgroud.png")

#sonido
laser_sound = pygame.mixer.Sound("scifi002_1.ogg")
explosion_sound = pygame.mixer.Sound("scifi002_1.ogg")
sound = pygame.mixer.Sound("mi_explosion_03_hpx.ogg")

# Game Loop
player = Player()
player.game_over = False
running = True
while running:
	if player.game_over == False:
		show_go_screen()
		player.game_over = True
		all_sprites = pygame.sprite.Group()
		meteor_list = pygame.sprite.Group()
		bullets = pygame.sprite.Group()  


		
		all_sprites.add(player)

		for i in range(8):
			meteor = Meteor()
			all_sprites.add(meteor)
			meteor_list.add(meteor)

		player.score = 0

	clock.tick(60)
	# Process input (events)
	for event in pygame.event.get():
		# check for closing window
		if event.type == pygame.QUIT:
			running = False
		
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player.shoot()

	# Update
	all_sprites.update()
	# Colisiones meteoro - laser
	hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)
	for hit in hits:
		player.score += 1
		#explosion_sound.play()
		explosion = Explosion(hit.rect.center)
		all_sprites.add(explosion)

		meteor = Meteor()
		all_sprites.add(meteor)
		meteor_list.add(meteor)
		
	# Colisiones jugador - meteoro
	hits = pygame.sprite.spritecollide(player, meteor_list, False)
	for hit in hits:
		player.shield -= 1
		meteor = Meteor()
		if player.shield <= 0:
			gameOver_screen()
			player.game_over = False
	#Draw / Render
	screen.blit(background, [0, 0])
	all_sprites.draw(screen)
  #Marcador

	draw_text(screen, str(player.score), 25, WIDTH // 2, 10)

	pygame.display.flip()		

	# Update
	all_sprites.update()

	#Draw / Render

	screen.blit(background, [0, 0])
	all_sprites.draw(screen)
	draw_shield_bar(screen, 5, 5, player.shield)
	# *after* drawing everything, flip the display.
	pygame.display.flip()

pygame.quit()
