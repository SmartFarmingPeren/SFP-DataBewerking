#include <math.h>
#include <stdio.h>


extern int CloserTo(float ax, float ay, float az, float (*Bar)[3], int sizeOfArray);

__declspec(dllexport) int __cdecl CloserTo(float ax, float ay, float az, float (*Bar)[3], int sizeOfArray) {
	float Ax = ax;
	float Ay = ay;
	float Az = az;
	float distance = 100000000000000000;
	int returnVal = 0;

	float val = 0;
	for (int i = 0; i < sizeOfArray-1; i++) {
		val = pow((Ax - Bar[i][0]), 2) + pow((Ay - Bar[i][1]), 2) + pow((Az - Bar[i][2]), 2);
		if (val < distance) {
			distance = val;
			returnVal = i;
		}
	}

	return returnVal;
}

int main(){
}
