import pandas as pd

mos = pd.read_csv('mos.txt')
psnr = pd.read_csv('PSNR3.txt')
ssim = pd.read_csv('SSIM3.txt')

scores = pd.concat([mos, psnr, ssim], axis=1)
scores.to_csv('scores.csv', index=False)
