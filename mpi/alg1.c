#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <time.h>
#include <limits.h>

double fill_array(unsigned int *array, int size) {
    int num_threads = omp_get_max_threads();
    double start_time, end_time;
    start_time = omp_get_wtime();
    #pragma omp parallel
    {
        int thread_num = omp_get_thread_num();
        int seed = time(NULL) + thread_num;

        #pragma omp for schedule(auto)
        for (int i = 0; i < size * num_threads; i++) {
            array[i] = rand_r(&seed);
        }
    }
    end_time = omp_get_wtime();
    return end_time - start_time;
}

void sort_cube(int* cube, int cube_size) {
    for(int i = 0; i < cube_size - 1; i++) {
        for(int j = 0; j < cube_size - i - 1; j++) {
            if(cube[j] > cube[j + 1]) {
                int temp = cube[j];
                cube[j] = cube[j + 1];
                cube[j + 1] = temp;
            }
        }
    }
}

void sort_main_function(unsigned int *array, int size, int cube_num) {
    int num_threads = omp_get_max_threads();
    double start_time, end_time, start, end;
    
    #pragma omp parallel
    {
        unsigned int thread_num = omp_get_thread_num();
        int **cubes = malloc((cube_num/num_threads) * sizeof(int *));        
        int *cubes_size = (int*)malloc((cube_num/num_threads)  * sizeof(int));
        int *cubes_alloc_size = (int*)malloc((cube_num/num_threads)  * sizeof(int));

        int single_cube_size = (INT_MAX)/(cube_num);

        int start_value = single_cube_size * (cube_num/num_threads) * thread_num;
        int end_value;
        if (thread_num == num_threads - 1) {
            end_value = INT_MAX;
        } else {
            end_value = single_cube_size * (cube_num/num_threads) * (thread_num + 1);
        }
       
        int start_writing = 0;

        for(int i = 0; i < (cube_num/num_threads); i++) {
            cubes[i] = malloc(sizeof(int));
            cubes_size[i] = 0;
            cubes_alloc_size[i] = 1;
        }

        #pragma omp single
        {
            start_time = omp_get_wtime();
        }

        #pragma omp barrier
        for (int i = 0; i < size * num_threads; i++) {
            if(array[i] >= start_value && array[i] < end_value) {
                int index = (array[i] - start_value)/single_cube_size;
                if(index >= cube_num/num_threads) {
                    index = cube_num/num_threads - 1;
                }

                if(cubes_size[index] + 1 > cubes_alloc_size[index]) {
                    cubes_alloc_size[index] *= 2;
                    cubes[index] = realloc(cubes[index], cubes_alloc_size[index] * sizeof(int));
                }
                
                cubes[index][cubes_size[index]] = array[i];
                cubes_size[index] += 1;
            }
            
            if(array[i] < start_value) {
                start_writing++;
            }
        }
        #pragma omp barrier

        #pragma omp single
        {
            end_time = omp_get_wtime();
            printf("%.6f,", end_time - start_time);
        }

        #pragma omp barrier

        #pragma omp single
        {
            start_time = omp_get_wtime();
        }
        for (int i = 0; i < (cube_num/num_threads) ; i++) {
            sort_cube(cubes[i], cubes_size[i]);
        }
        
        #pragma omp barrier

        #pragma omp single
        {
            end_time = omp_get_wtime();
            printf("%.6f,", end_time - start_time);
        }

        #pragma omp barrier

        #pragma omp single
        {
            start_time = omp_get_wtime();
        }
        for (int i = 0; i < (cube_num/num_threads); i++) {
            for(int j = 0; j < cubes_size[i]; j++) {
                array[start_writing] = cubes[i][j];
                start_writing++;
            }
        }
        #pragma omp barrier 
        #pragma omp single
        {
            end_time = omp_get_wtime();
            printf("%.6f,", end_time - start_time);
        }

        for (int i = 0; i < cube_num/num_threads; i++) {
            free(cubes[i]);
        }
        free(cubes);
        free(cubes_size);
        free(cubes_alloc_size);
    }
}

int main(int argc, char *argv[]) {
    int size = atoi(argv[1]);
    int cube_num = atoi(argv[2]);

    int num_threads = omp_get_max_threads();
    int* array = (int*)malloc(size * num_threads * sizeof(int));


    double start_time = omp_get_wtime();
    printf("%d,%ld,%.6f,", num_threads, cube_num, fill_array(array, size));
    // for(int i=0;i<size*num_threads; i++) {
    //     printf("%d\n", array[i]);
    // }
    // fflush(stdout); 
    sort_main_function(array, size, cube_num);
    
    double end_time = omp_get_wtime();
    printf("%.6f\n",end_time - start_time);
    // printf("\n");
    // for(int i=0;i<size*num_threads; i++) {
    //     printf("%d\n", array[i]);
    // }
    free(array);
    
    return 0;
}