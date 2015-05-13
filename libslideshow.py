#!/usr/bin/python
import threading
import time
import os, sys
import shutil
import pygame
from string import split,join
from pygame.locals import *


# execute a shell command, printing it to the console for debugging purposes...
def shellcmd(command):
	print ' =>', command
	os.system(command)

def fillscreen(screen, color):
	screen.fill(color)
	pygame.display.flip()


def center_loc(size, imagesize):
	# screen size should always be >= imagesize, no checks here...
	w, h = size
	iw, ih = imagesize
	dx = int( (w-iw)/2. )
	dy = int( (h-ih)/2. )
	return ( (dx, dy) )

def displayimage(screen, filename, size, location=(0,0)):
		f = open(filename, 'rb')
		print filename
		image = pygame.image.load(f, filename)
		imagerect = image.get_rect()
		image = pygame.transform.scale(image, size)
		screen.blit(image, location)
		pygame.display.flip()

def flashtext(duration, rate, screen, text, size, location=None):
	bgwhite = pygame.Surface(screen.get_size())
	bgblack = pygame.Surface(screen.get_size())
	bgwhite = bgwhite.convert()
	bgblack = bgblack.convert()
	bgwhite.fill(white)
	bgblack.fill(black)
	
	fontname = pygame.font.match_font('freeserif')
	font = pygame.font.Font(fontname, 128)
	textw = font.render(text, 1, white)
	textb = font.render(text, 1, black)
	textwpos = textw.get_rect()
	textbpos = textb.get_rect()
	if location==None:
		textwpos.centerx = textbpos.centerx = bgwhite.get_rect().centerx	
		textwpos.centery = textbpos.centery = bgwhite.get_rect().centery
	else:
		w,h = location
		textwpos.centerx = textbpos.centerx = w
		textwpos.centery = textbpos.centery = h
	bgwhite.blit(textb, textbpos)
	bgblack.blit(textw, textbpos)

	start = time.time()
	while (time.time()-start < duration):
		screen.blit(bgblack, (0,0))
		pygame.display.flip()
		time.sleep(rate/2.)
		screen.blit(bgwhite, (0,0))
		pygame.display.flip()
		time.sleep(rate/2.)


def showtext(screen, text, size, location=None):
	bgwhite = pygame.Surface(screen.get_size())
	bgwhite = bgwhite.convert()
	bgwhite.fill(black)#white)
	
	fontname = pygame.font.match_font('freeserif')
	font = pygame.font.Font(fontname, size)
	textb = font.render(text, 1, white)#black)

	textbpos = textb.get_rect()
	if location==None:
		textbpos.centerx = bgwhite.get_rect().centerx	
		textbpos.centery = bgwhite.get_rect().centery
	else:
		w,h = location
		textbpos.centerx = w	
		textbpos.centery = h
	bgwhite.blit(textb, textbpos)

	screen.blit(bgwhite, (0,0))
	pygame.display.flip()




