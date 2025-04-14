#!/bin/bash
#SBATCH --partition=plgrid
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=10
#SBATCH --mem-per-cpu=10GB
#SBATCH --time=12:00:00
#SBATCH -N 1

# Output CSV
output="results.csv"
echo "scaling,threads,buckets,fill_time,partition_time,sort_time,merge_time,total_time" > $output

gcc -o algo1 algo1.c -fopenmp
problem_size=100000000

for buckets in 1000000 10000000; do
  for threads in {1..10}; do
    export OMP_NUM_THREADS=$threads
    buckets_weak=$((buckets * threads) / 10)
    result=$(./algo1 $problem_size $buckets_weak)
    echo "weak,$result" >> $output
  done
done

for buckets in 1000000 10000000; do
  for threads in {1..10}; do
    export OMP_NUM_THREADS=$threads
    problem_size_strong=$((problem_size / threads))
    result=$(./algo1 $problem_size_strong $buckets)
    echo "strong,$result" >> $output
  done
done