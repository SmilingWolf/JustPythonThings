import sys

# Your IMEI here
IMEI = '111111111111111'
IMEI = sys.argv[1]

i = 0;
length = len(IMEI);
i2 = 0;
while (i2 < length):
	if (i2 < 5 or i2 >= length - 5):
		codePointAt = ord(IMEI[i2]) & 255
		i = (i + (((((49635 * codePointAt) & 65535) >> 1) - codePointAt) & 65535)) & 65535
	i2 += 1
print("Registration code: %05d" % i);
