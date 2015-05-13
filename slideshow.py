#!/usr/bin/python
# many dependencies are all brought in with this import...
from libslideshow import *
from random import randrange, shuffle
from string import split,join
import os
import urllib2

#=============================================================================
# ==================================  MAIN  ==================================
#=============================================================================

# indicate what display we are using (i.e., uncomment it)...
#disptype = 'LVDS'  # FSL LVDS display 
#disptype = 'EEEpc' # EEE PC netbook 
#disptype = 'mx28'  # i.MX28 LCD display
disptype = 'fullhd' #hdmi TV

# define the image type so we can maximize it on the display without distorting
#imgtype = 'D90' # D90 camera image
imgtype = 'disp' # horizontal 4-up composite image

# set up display and image sizes for screen
if disptype == 'LVDS':
   size = (1024, 768) 				# LVDS display screen size
   if imgtype == 'D90': imagesz = (1152, 768)  	# D90 aspect ratio
   if imgtype == 'disp': imagesz = (1024, 698) 	# composite aspect ratio
if disptype == 'EEEpc':
   size = (1024, 600) 				# EEE pc screen size
   if imgtype == 'D90': imagesz = (900, 600) 	# D90 aspect ratio
   if imgtype == 'disp': imagesz = (880, 600) 	# composite aspect ratio
if disptype == 'mx28':
   size = (800, 480) 				# i.MX28 LCD screen size
   if imgtype == 'D90': imagesz = (720, 480)  	# D90 aspect ratio
   if imgtype == 'disp': imagesz = (704, 480) 	# composite aspect ratio
if disptype == 'fullhd':
   size = (1920, 1080)
   if imgtype == 'D90': imagesz  = (1620, 1080)
   if imgtype == 'disp': imagesz = (1584, 1080)

# determine the offset to centered the image on the display in use...
imageloc = center_loc(size, imagesz) 

# initiate pygame and hide mouse...
pygame.init()
screen = pygame.display.set_mode(size)
pygame.mouse.set_visible(False)

# define the base url to the photo booth web server
baseurl = 'http://10.81.56.160/'

lastone = '' 	# holds the newest image number from the web server: DSCxxxx 
		# there is no extension to make things easier... 
count = 0    	# index variable used to stepping 'files'
files = []   	# holds list of images to display

# play slideshow forever
while(1):

	# check to see if a new image is ready...
	check = urllib2.urlopen(baseurl+'lastone.txt').read()

	# if there has been a change, grab the directory index...
	if check <> lastone:

		lastone = check # the latest is the new 'lastone'...
		print "New one!", check

		# grab the directory listing from the web server...
		indx = urllib2.urlopen(baseurl+'for-display/').read()

		# extract the first half image names from the html
		# (no need for a pretty html parser...)
		indx = split(indx, 'href="')[2:]

		# iterate over the list of file names
		for i in indx:

			# finish splitting the name
			filename = split(i, '">')[0]
			print 'filename:', filename
			# add to files if it's not already in there...
			if filename not in files and 'DSC' in filename: files.append(filename)

			# if 'i' is actually the latest, then display it right now...
			# holding it a little longer so people can see it when they come out
			if lastone in filename:
				# if it's not already local, grab the image...
				if filename not in os.listdir(os.curdir):
					print 'Grabbing file...', filename
					open(filename, 'wb').write(urllib2.urlopen(baseurl+'for-display/'+filename).read())
				print 'displaying lastone ... ', filename 
				displayimage (screen, filename, imagesz, imageloc )
				time.sleep(10)

	# increment the counter used for stepping through 'files'
	count += 1
	# check for the end of the list; and if it is, shuffle the file list as well
	if count == len(files): 
		count = 0
		print 'Shuffling file list...'
		shuffle(files) # so we don't always play the same order

	# Finally, display the next image in the file list...
        if count < len(files): 
		# if it's not already local, grab the image...
		if files[count] not in os.listdir(os.curdir):
			print 'Grabbing file...', filename
			open(files[count], 'wb').write(urllib2.urlopen(baseurl+'for-display/'+files[count]).read())
		displayimage (screen, files[count], imagesz, imageloc )
		print count, files[count]

	# check for a signal to quit...
        for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
		if event.type == pygame.KEYDOWN: 
			if event.key == K_q or event.key == ESCAPE: 
				sys.exit()

	# This is a place holder for other administrative functions 
	# like shutting down or rebooting via a flag file from the web server.
	# We still need to add in the extra images ("go to the photo booth", etc), too...

	# delay time for displaying the image...
	time.sleep(3)


