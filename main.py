import pygame
import sys
import random
from water import Water

def main():

	#Initialisation
	pygame.init()
	width = (800, 800)
	screen = pygame.display.set_mode(width)
	fps_clock = pygame.time.Clock()
	delay = 10

	block_img = pygame.image.load("block.png")
	sand_img = pygame.image.load("sand.png")
	water_img = pygame.image.load("water.png")
	my_font = pygame.font.SysFont("OCR A Std", 14)

	white = (255, 255, 255)
	orange = (205, 133, 63)
	grey = (105, 105, 105)
	blue = (0, 125, 255)
	black = (0, 0, 0)

	water_blocks = []
	sand_blocks = []
	blocks = []
	water_rects = []
	paused = True
	placing = "sand"

	while 1:

		#Events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

		if pygame.mouse.get_pressed()[0]:
			if placing == "sand":
				sand_blocks = place_item(pygame.mouse.get_pos(), sand_blocks, blocks, water_rects, sand_img)
				sand_blocks = sorted(sand_blocks, key=lambda sand: sand.y)
				sand_blocks.reverse()
			else:
				water_blocks = place_water(pygame.mouse.get_pos(), water_blocks, water_rects, blocks, sand_blocks, water_img)
				water_blocks = sorted(water_blocks, key=lambda water: water.rect.y)
				water_blocks.reverse()
		elif pygame.mouse.get_pressed()[2]:
			blocks = place_item(pygame.mouse.get_pos(), blocks, sand_blocks, water_rects, block_img)

		key_states = pygame.key.get_pressed()
		if key_states[pygame.K_p]:
			if delay == 10:
				delay = 0
				if paused:
					paused = False
				else:
					paused = True
		if key_states[pygame.K_s]:
			if delay == 10:
				delay = 0
				if placing == "water":
					placing = "sand"
				else:
					placing = "water"
		if key_states[pygame.K_r]:
			sand_blocks = []
			water_blocks = []
			blocks = []

		#Logic
		if not paused:
			new_sand_blocks = []
			for sand in sand_blocks:
				sand = sand.move(0, 15)
				if sand.collidelist(sand_blocks) < 0 and sand.collidelist(blocks) < 0:
					new_sand_blocks.append(sand)
				else:
					if random.randint(0, 1):
						sand = sand.move(15, 0)
						if sand.collidelist(sand_blocks) < 0 and sand.collidelist(blocks) < 0:
							new_sand_blocks.append(sand)
						else:
							sand = sand.move(-30, 0)
							if sand.collidelist(sand_blocks) < 0 and sand.collidelist(blocks) < 0:
								new_sand_blocks.append(sand)
							else:
								sand = sand.move(15, -15)
								new_sand_blocks.append(sand)
					else:
						sand = sand.move(-15, 0)
						if sand.collidelist(sand_blocks) < 0 and sand.collidelist(blocks) < 0:
							new_sand_blocks.append(sand)
						else:
							sand = sand.move(30, 0)
							if sand.collidelist(sand_blocks) < 0 and sand.collidelist(blocks) < 0:
								new_sand_blocks.append(sand)
							else:
								sand = sand.move(-15, -15)
								new_sand_blocks.append(sand)
			sand_blocks = new_sand_blocks

			new_water_blocks = []
			for water in water_blocks:
				if not water.rect.collidelist(sand_blocks) < 0:
					water.rect = water.rect.move(0, -15)
					new_water_blocks.append(water)
				else:
					water.rect = water.rect.move(0, 15)
					if water.rect.collidelist(sand_blocks) < 0 and water.rect.collidelist(blocks) < 0 and water.rect.collidelist(water_rects) < 0:
						new_water_blocks.append(water)
					else:
						water.rect = water.rect.move(0, -15)
						if water.direction == 1:
							water.rect = water.rect.move(15, 0)
							if water.rect.collidelist(sand_blocks) < 0 and water.rect.collidelist(blocks) < 0 and water.rect.collidelist(water_rects) < 0:
								new_water_blocks.append(water)
							else:
								water.direction = 0
								water.rect = water.rect.move(-15, 0)
								new_water_blocks.append(water)
						else:
							water.rect = water.rect.move(-15, 0)
							if water.rect.collidelist(sand_blocks) < 0 and water.rect.collidelist(blocks) < 0 and water.rect.collidelist(water_rects) < 0:
								new_water_blocks.append(water)
							else:
								water.direction = 1
								water.rect = water.rect.move(15, 0)
								new_water_blocks.append(water)
			water_blocks = new_water_blocks

		if delay < 10:
			delay += 1

		new_sand_blocks = []
		for sand in sand_blocks:
			if sand.y < 815:
				new_sand_blocks.append(sand)
		sand_blocks = new_sand_blocks

		new_water_blocks = []
		new_water_rects = []
		for water in water_blocks:
			if water.rect.y < 815:
				new_water_blocks.append(water)
				new_water_rects.append(water.rect)
		water_blocks = new_water_blocks
		water_rects = new_water_rects

		#Render
		screen.fill(white)

		for sand in sand_blocks:
			screen.blit(sand_img, sand)
		for block in blocks:
			screen.blit(block_img, block)
		for water in water_blocks:
			screen.blit(water_img, water.rect)

		sand_label = my_font.render("Number of sand blocks: " + str(len(sand_blocks)), 1, orange)
		block_label = my_font.render("Number of solid blocks: " + str(len(blocks)), 1, grey)
		water_label = my_font.render("Number of water blocks: " + str(len(water_blocks)), 1, blue)
		placing_label = my_font.render("Placing: " + placing, 1, black)
		controls1 = my_font.render("R: resets blocks", 1, black)
		controls2 = my_font.render("P: pauses", 1, black)
		controls3 = my_font.render("LMB: place water or sand", 1, black)
		controls4 = my_font.render("RMB: place solid block", 1, black)
		controls5 = my_font.render("S: switch water/sand", 1, black)
		screen.blit(controls1, (550, 12))
		screen.blit(controls2, (550, 25))
		screen.blit(controls3, (550, 38))
		screen.blit(controls4, (550, 51))
		screen.blit(controls5, (550, 64))
		screen.blit(block_label, (20, 12))
		screen.blit(sand_label, (20, 25))
		screen.blit(water_label, (20, 38))
		screen.blit(placing_label, (20, 51))

		pygame.display.flip()
		fps_clock.tick(30)

def place_item(pos, similar_blocks, other_blocks1, other_blocks2, image):
	block = image.get_rect()
	block.center = pos
	while not block.right % 15 == 0:
		block = block.move(-1, 0)
	while not block.bottom % 15 == 0:
		block = block.move(0, -1)
	if block.collidelist(similar_blocks) < 0 and  block.collidelist(other_blocks1) < 0 and  block.collidelist(other_blocks2) < 0:
		similar_blocks.append(block)
	return similar_blocks

def place_water(pos, water_blocks, water_rects, other_blocks1, other_blocks2, image):
	water = Water(image)
	water.rect.center = pos
	while not water.rect.right % 15 == 0:
		water.rect = water.rect.move(-1, 0)
	while not water.rect.bottom % 15 == 0:
		water.rect = water.rect.move(0, -1)
	if water.rect.collidelist(water_rects) < 0 and  water.rect.collidelist(other_blocks1) < 0 and  water.rect.collidelist(other_blocks2) < 0:
		water_blocks.append(water)
	return water_blocks

if __name__ == "__main__":
	main()