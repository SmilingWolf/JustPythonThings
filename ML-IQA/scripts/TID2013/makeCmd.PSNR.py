for x in range(1, 26):
	for y in range(1, 25):
		for z in range(1, 6):
			print('./dump_psnr.exe -s reference_images/i%02d.png.y4m distorted_images/i%02d_%02d_%d.png.y4m | grep Total >> PSNR3.txt' % (x, x, y, z))
