for x in range(1, 26):
	for y in range(1, 25):
		for z in range(1, 6):
			print('./dssim.exe reference_images/i%02d.png distorted_images/i%02d_%02d_%d.png >> DSSIM.txt' % (x, x, y, z))
