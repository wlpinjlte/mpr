#include<stdio.h>
#include<stdlib.h>
#include<mpi.h>

int main(int argc, char **argv) {
    MPI_Init(&argc, &argv);
    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    unsigned long n = (unsigned long) strtod(argv[1], NULL);
    srand(world_rank);

    MPI_Barrier(MPI_COMM_WORLD);
    double time = MPI_Wtime();
    MPI_Barrier(MPI_COMM_WORLD);

    unsigned long local_sum = 0;
    for (int i = 0; i < n; i++) {
        double x = (double) rand() / RAND_MAX;
        double y = (double) rand() / RAND_MAX;
        // printf("x=%f, y=%f\n", x, y);
        if (x*x + y*y <= 1) {
            local_sum ++;
        }
    }

    unsigned long  global_sum;
    //printf("local_sum = %lu\n", local_sum);
    MPI_Reduce(&local_sum, &global_sum, 1, MPI_UNSIGNED_LONG, MPI_SUM, 0,
               MPI_COMM_WORLD);

    // Print the result
    if (world_rank == 0) {
        //printf("global_sum = %lu\n", global_sum);
        const double pi = (global_sum/ ((double) (world_size * n)))*4;
        double endTime = MPI_Wtime() - time;
        //printf("Pi: %lf\n", pi);
        printf("%lf", endTime);
    }
    MPI_Finalize();
    return 0;
}
