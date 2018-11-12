#include <stdio.h>
#include <string.h>

int calc(char *IMEI) {
    int i = 0;
    int length = strlen(IMEI);
    int i2 = 0;
    while (i2 < length) {
        if (i2 < 5 || i2 >= length - 5) {
            int codePointAt = IMEI[i2] & 255;
            i = (i + (((((49635 * codePointAt) & 65535) >> 1) - codePointAt) & 65535)) & 65535;
        }
        i2 += 1;
    }
    return i;
}

int calc2(char *IMEI, size_t length) {
    int i0 = (((49635 * IMEI[0]) & 65535) >> 1) - IMEI[0];
	int i1 = (((49635 * IMEI[1]) & 65535) >> 1) - IMEI[1];
	int i2 = (((49635 * IMEI[2]) & 65535) >> 1) - IMEI[2];
	int i3 = (((49635 * IMEI[3]) & 65535) >> 1) - IMEI[3];
	int i4 = (((49635 * IMEI[4]) & 65535) >> 1) - IMEI[4];
	int i5 = (((49635 * IMEI[length - 5]) & 65535) >> 1) - IMEI[length - 5];
	int i6 = (((49635 * IMEI[length - 4]) & 65535) >> 1) - IMEI[length - 4];
	int i7 = (((49635 * IMEI[length - 3]) & 65535) >> 1) - IMEI[length - 3];
	int i8 = (((49635 * IMEI[length - 2]) & 65535) >> 1) - IMEI[length - 2];
	int i9 = (((49635 * IMEI[length - 1]) & 65535) >> 1) - IMEI[length - 1];
    return (i0+i1+i2+i3+i4+i5+i6+i7+i8+i9) & 65535;
}

int main(int argc, char *argv[]) {
	int regCode = 0;
	if (argc != 2) {
		printf("Usage:\r\n");
		printf("%s <YOUR_IMEI>", argv[0]);
		return -1;
	}
	if (strlen(argv[1]) < 10) {
		printf("Registration code: %05d\r\n", calc(argv[1]));
	}
	else {
		printf("Registration code: %05d\r\n", calc2(argv[1], strlen(argv[1])));
	}
	return 0;
}
