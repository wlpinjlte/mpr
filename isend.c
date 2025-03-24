#include<stdio.h>
#include<stdlib.h>
#include<mpi.h>

#define N 1000

int main(int argc, char **argv) {
    MPI_Init(&argc, &argv);
    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);
    int rankNeighbor = world_rank==0 ? 1 : 0;
    MPI_Request request;
    for (double size = 1; size <= (1 << 25); size *= 2) {
            char *buffer = (char *)malloc(size);

            MPI_Barrier(MPI_COMM_WORLD);
            double time = MPI_Wtime();
            MPI_Barrier(MPI_COMM_WORLD);

            for (int i=world_rank;i<=N+world_rank; i++) {
                if (i % 2 == 0) {
                    MPI_Isend(buffer, size, MPI_CHAR, rankNeighbor, 0, MPI_COMM_WORLD, &request);
                    MPI_Wait(&request, MPI_STATUS_IGNORE);
                    //printf("ping\n");
                } else {
                    MPI_Irecv(buffer, size, MPI_CHAR, rankNeighbor, 0, MPI_COMM_WORLD, &request);
                    MPI_Wait(&request, MPI_STATUS_IGNORE);
                    //printf("pong\n");
                }
            }
            MPI_Barrier(MPI_COMM_WORLD);

            if(world_rank == 0){
                    double endTime = MPI_Wtime()-time;
                    double w = (size * 8 * N)/(endTime* 1024 * 1024);
                    // printf("Size: %lf, Przepustowość: %lf Mbit/s, time is %lf\n",size, w, endTime);
                    printf("%lf,%lf,\n", size, w);
                    if(size == 1) {
                        double latency_ms = (endTime * 1000.0) / N;
                        printf("Size,Bandwidth,Delay\n");
                        printf("%lf,%lf,%lf\n", size, w, latency_ms);
                    }
            }
            free(buffer);
    }
    MPI_Finalize();
    return 0;
}