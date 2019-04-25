for x in range(1, 26):
	for y in range(1, 25):
		for z in range(1, 6):
			print('./vmafossexec.exe yuv444p 512 384 reference_images/i%02d.bmp.yuv distorted_images/i%02d_%02d_%d.bmp.yuv model/vmaf_v0.6.1.pkl | grep "score =" | sed "s/VMAF\ score\ =\ //" >> vmaf.txt' % (x, x, y, z))
