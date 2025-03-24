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
    
    for (double size = 1; size <= (1 << 25); size *= 2) {
            char *buffer =(char *) malloc(size + MPI_BSEND_OVERHEAD);
            char *msg = (char *) malloc(size + MPI_BSEND_OVERHEAD);
            MPI_Buffer_attach(buffer, size + MPI_BSEND_OVERHEAD);

            MPI_Barrier(MPI_COMM_WORLD);
            double time = MPI_Wtime();
            MPI_Barrier(MPI_COMM_WORLD);
            

            for (int i=world_rank;i <= N + world_rank; i++) {
                if (i % 2 == 0) {
                    MPI_Bsend(msg, size, MPI_CHAR, rankNeighbor, 0, MPI_COMM_WORLD);
                    //printf("ping\n");
                } else {
                    MPI_Recv(msg, size, MPI_CHAR, rankNeighbor, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
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

            void *old_buff;
            int detached_size;
            MPI_Buffer_detach(&old_buff, &detached_size);
            free(buffer);
            free(msg);
        }
    MPI_Finalize();
    return 0;
}