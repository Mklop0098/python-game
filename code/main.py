import pygame, sys
from settings import * 
from level import Level
from overworld import Overworld
from ui import UI
from menu import Menu
from button import Button

class Game:
	def __init__(self):

		# game attributes
		self.max_level = 2
		self.max_health = 100
		self.cur_health = 100
		self.coins = 0
		self.pause = False
		
		# audio 
		self.level_bg_music = pygame.mixer.Sound('./audio/level_music.wav')
		self.overworld_bg_music = pygame.mixer.Sound('./audio/overworld_music.wav')
		self.menu_bg_music = pygame.mixer.Sound('./audio/overworld_music.wav')

		# user interface 
		self.ui = UI(screen)

		self.overworld = Overworld(0,self.max_level,screen,self.create_level)
		self.menu = Menu(screen, self.create_overworld)
		self.level = Level(0,screen,self.create_overworld,self.change_coins,self.change_health, self.create_menu)
		# menu creation
		self.status = 'overworld'
		self.menu_bg_music.play(loops=-1) 

	def create_level(self,current_level):
		self.level = Level(current_level,screen,self.create_overworld,self.change_coins,self.change_health, self.create_menu)
		self.status = 'level'
		self.overworld_bg_music.stop()
		self.menu_bg_music.stop()
		self.level_bg_music.play(loops = -1)

	def create_overworld(self,current_level,new_max_level):
		if new_max_level > self.max_level:
			self.max_level = new_max_level
		self.overworld = Overworld(current_level,self.max_level,screen,self.create_level)
		self.status = 'overworld'
		self.overworld_bg_music.play(loops = -1)
		self.level_bg_music.stop()
		self.menu_bg_music.stop()

	def create_menu(self):
		self.overworld = Menu(screen,self.create_overworld)
		self.status = 'menu'
		self.menu_bg_music.play(loops = -1)
		self.level_bg_music.stop()
		self.overworld_bg_music.stop()


	def change_coins(self,amount):
		self.coins += amount

	def change_health(self,amount):
		self.cur_health += amount

	def check_game_over(self):
		if self.cur_health <= 0:
			self.cur_health = 100
			self.coins = 0
			self.max_level = 0
			self.overworld = Overworld(0,self.max_level,screen,self.create_level)
			self.status = 'overworld'
			self.level_bg_music.stop()
			self.overworld_bg_music.play(loops = -1)

	def run(self):
		if self.status == 'menu':
			self.menu.run()	
		elif self.status == 'overworld':
			self.overworld.run()
		else:
			self.level.run()
			self.ui.show_health(self.cur_health,self.max_health)
			self.ui.show_coins(self.coins)
			self.check_game_over()

	def pick_map(self):
		self.status = 'overworld'
		self.overworld_bg_music.stop()
		self.level_bg_music.stop()
		self.overworld_bg_music.play(loops = -1)
	
	def restart(self):
		self.create_level(self.level.current_level)
		self.level_bg_music.stop()
		self.level_bg_music.play(loops=-1)


def main_menu():
    while True:
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="MAP", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

# main_menu()

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)



screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
game = Game()

pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")

def get_font(size): 
    return pygame.font.Font("assets/font.ttf", size)

# Biến trạng thái cho tùy chọn và trò chơi
menu_open = True
game_open = False
option_open = False
map_select = False
restart = False

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE and not menu_open:
				if not option_open:
					option_open = True
					game_open = False
					map_select = False
				else:
					option_open = False
					map_select = False
					game_open = True
	

	if game_open:
		game.run()
		pygame.display.update()
		clock.tick(60)
	
	if map_select:
		game.pick_map()
		map_select = False
		game_open = True
		
	if restart:
		game.restart()
		restart = False
		game_open = True


	if option_open:
		screen.blit(BG, (0, 0))

		MENU_MOUSE_POS = pygame.mouse.get_pos()

		MENU_TEXT = get_font(100).render("PAUSE", True, "#b68f40")
		MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

		CONTINUE_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
							text_input="CONTINUE", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
		RE_PLAY_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
							text_input="PLAY AGAIN", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
		MAP_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
							text_input="MAP", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

		screen.blit(MENU_TEXT, MENU_RECT)

		for button in [CONTINUE_BUTTON, RE_PLAY_BUTTON, MAP_BUTTON]:
			button.changeColor(MENU_MOUSE_POS)
			button.update(screen)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if CONTINUE_BUTTON.checkForInput(MENU_MOUSE_POS):
					game_open = True
					menu_open = False
					option_open = False
				if MAP_BUTTON.checkForInput(MENU_MOUSE_POS) and not map_select:
					map_select = True
					option_open = False
					game_open = False
				if RE_PLAY_BUTTON.checkForInput(MENU_MOUSE_POS) and not map_select:
					restart = True
					game_open = False
					option_open = False
					
	pygame.display.flip()

	if menu_open:
		screen.blit(BG, (0, 0))

		MENU_MOUSE_POS = pygame.mouse.get_pos()

		MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
		MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

		PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
							text_input="MAP", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
		OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
							text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
		QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
							text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

		screen.blit(MENU_TEXT, MENU_RECT)

		for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
			button.changeColor(MENU_MOUSE_POS)
			button.update(screen)
		
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
					game_open = True
					menu_open = False
				if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
					pygame.quit()
					sys.exit()

	pygame.display.flip()

pygame.quit()
sys.exit()


# # # Pygame setup
# # pygame.init()

# # while True:
# # 	for event in pygame.event.get():
# # 		if event.type == pygame.QUIT:
# # 			pygame.quit()
# # 			sys.exit()
# # 	screen.fill('grey')
# # 	game.run()

# # 	pygame.display.update()
# # 	clock.tick(60)


# pygame.init()


# def play():
#     while True:
#         PLAY_MOUSE_POS = pygame.mouse.get_pos()

#         screen.fill("black")

#         PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
#         PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
#         screen.blit(PLAY_TEXT, PLAY_RECT)

#         PLAY_BACK = Button(image=None, pos=(640, 460), 
#                             text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

#         PLAY_BACK.changeColor(PLAY_MOUSE_POS)
#         PLAY_BACK.update(screen)

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
#                     main_menu()
#         pygame.display.update()
    
# def options():
#     while True:
#         OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

#         screen.fill("white")

#         OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
#         OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
#         screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

#         OPTIONS_BACK = Button(image=None, pos=(640, 460), 
#                             text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

#         OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
#         OPTIONS_BACK.update(screen)

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
#                     game.run()

#         pygame.display.update()
