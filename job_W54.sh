#!/bin/bash
#$ -pe mpi 32
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q all.q@compute-0-1

module purge
module load gnu/7.3.1
module load openmpi/4.1.4_gnu7.3.1
module load fftw/fftw-3.3.10

PWX=/home/tadeoye/q-e-qe-7.4.1/bin/pw.x

mpirun -np 32 $PWX -npool 4 -in perfect_3x3x3.in > perfect_3x3x3.out
mpirun -np 32 $PWX -npool 4 -in vacancy_3x3x3.in > vacancy_3x3x3.out

grep "^!" perfect_3x3x3.out | tail -1
grep "^!" vacancy_3x3x3.out | tail -1
grep "End of BFGS" vacancy_3x3x3.out

rm -rf ./tmp
