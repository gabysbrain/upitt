#include "stdio.h"

#define NUMS 100

int partition(int *array, int min, int max, int pivot)
{
    int pivotVal;
    int tmp, len, i;

    len = max;
    pivotVal = array[pivot];
    array[pivot] = array[max-1];
    array[max-1] = pivotVal;

    max--;
    for(i=min; i<len-1; i++) {
        if(array[i] <= pivotVal) {
            tmp = array[i];
            array[i] = array[min];
            array[min] = tmp;
            min++;
        }
    }

    array[len-1] = array[min];
    array[min] = pivotVal;

    return min;
}

void quicksort(int *array, int min, int max)
{
    int pivoti;
    //if(max > min+1) {
    if(max > min+1) {
        pivoti = (min+max) / 2;
        pivoti = partition(array, min, max, pivoti);
        quicksort(array, min, pivoti);
        quicksort(array, pivoti, max);
    }
}

int main()
{
    int i;
    int *nums;
    int val;
    nums = (int*) malloc(sizeof(int) * NUMS);
    val = NUMS-1;
    for(i=0, val=NUMS-1; i<NUMS; i++, val--)
        nums[i] = val;

    quicksort(nums, 0, NUMS);
    for(i=0; i<NUMS; i++)
        printf("%d ", nums[i]);
    printf("\n");
}

