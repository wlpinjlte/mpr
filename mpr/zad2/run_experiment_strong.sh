#!/bin/bash -l
#SBATCH --nodes 1
#SBATCH --ntasks 12
#SBATCH --time=01:00:00
#SBATCH --partition=plgrid
#SBATCH --account=plgmpr25-cpu

# Experiment parameters
THREADS=(1 2 3 4 5 6 7 8 9 10 11 12)  # Number of threads
SIZES=(100000 10000000 1000000000)  # Problem sizes
REPEATS=10  # Number of repeats
output_file="results.csv"  # Output file

# Write CSV headers (in English)
echo "threads,problem_size,scaling,repeat,time" > "$output_file"

# Function to run experiment
run_experiment() {
    local threads=$1
    local size=$2
    local scaling=$3
    local repeat=$4
    local size_per_thread=$((size / threads))

    # Run the program and capture the result
    result=$(mpiexec -np $threads ./pi $size_per_thread)  # The program 'pi' returns the time result

    # Write the result to CSV file
    echo "$threads,$size,$scaling,$repeat,$result" >> "$output_file"
}

# Main experiment loop
for size in "${SIZES[@]}"  # For each problem size
do
    for repeat in $(seq 1 $REPEATS)  # For each repeat
    do
        for threads in "${THREADS[@]}"  # For each number of threads
        do
            scaling_type="strong"  # You can change this based on the scaling type
            run_experiment $threads $size $scaling_type $repeat  # Run the experiment
        done
    done
done

echo "Experiments completed. Results saved to $output_file."