#!/bin/bash
# Author  : Yuan-Yao Lou (Mike)
# Title   : PhD student in ECE at Purdue University
# Email   : yylou@purdue.edu
# Website : https://yylou.github.io/
# Date    : 2022/11/11
# 
# Project : Purdue ECE56300 - Project
# Version : v1.0 (makefile)

BUILD_DIR   :=  ./bin
INCLUDES    :=  -I ./include
SER_TARGET  :=  serial.o
<<<<<<< HEAD
OMP_TARGET  :=  openmp.o
MPI_TARGET  :=  mpi.o
=======
PAR_TARGET  :=  parallel.o
MPI_TARGET  :=	mpi.o
>>>>>>> 9b61a44 (ECE-563 (Jan 13, 2023))
ROOT_DIR    :=  ./
SRC_DIR     :=  ./src
SOURCES     :=  $(wildcard $(ROOT_DIR)/*.cpp $(SRC_DIR)/*.cpp)

CXXFLAGS    :=  -O3 -Wall -std=c++17
MKDIR       :=  @if [ ! -d "$(BUILD_DIR)" ]; then echo "[ `date +'%Y-%m-%d %H:%M:%S'` ]      Creating $(BUILD_DIR)" folder; mkdir $(BUILD_DIR) ; fi

serial:
	$(MKDIR)
	@echo "[ `date +'%Y-%m-%d %H:%M:%S'` ]      Compiling serial version"
	@mpiicpc -qopenmp $(CXXFLAGS) $(INCLUDES) $(SOURCES) -o $(BUILD_DIR)/$(SER_TARGET)
	@rm -f $(SER_TARGET)
	@ln -s $(BUILD_DIR)/$(SER_TARGET) .
	
parallel:
	$(MKDIR)
<<<<<<< HEAD
	@echo "[ `date +'%Y-%m-%d %H:%M:%S'` ]      Compiling parallel version"
	@g++ $(CXXFLAGS) -fopenmp $(INCLUDES) $(SOURCES) -o $(BUILD_DIR)/$(OMP_TARGET)
	@rm $(OMP_TARGET)
	@ln -s $(BUILD_DIR)/$(OMP_TARGET) .

mpi:
	$(MKDIR)
	@echo "[ `date +'%Y-%m-%d %H:%M:%S'` ]      Compiling MPI version"
	@mpiCC $(CXXFLAGS) $(INCLUDES) $(SOURCES) -o $(BUILD_DIR)/$(MPI_TARGET)
	@rm $(MPI_TARGET)
	@ln -s $(BUILD_DIR)/$(MPI_TARGET) .
=======
	@echo "[ `date +'%Y-%m-%d %H:%M:%S'` ]      Compiling OpenMP version"
	@mpiicpc -qopenmp $(CXXFLAGS) $(INCLUDES) $(SOURCES) -o $(BUILD_DIR)/$(PAR_TARGET)
	@rm -f $(PAR_TARGET)
	@ln -s $(BUILD_DIR)/$(PAR_TARGET) .
>>>>>>> 9b61a44 (ECE-563 (Jan 13, 2023))

mpi:
	$(MKDIR)
	@echo "[ `date +'%Y-%m-%d %H:%M:%S'` ]      Compiling MPI version"
	@mpiicpc -qopenmp $(CXXFLAGS) $(INCLUDES) $(SOURCES) -o $(BUILD_DIR)/$(MPI_TARGET)
	@rm -f $(MPI_TARGET)
	@ln -s $(BUILD_DIR)/$(MPI_TARGET) .

<<<<<<< HEAD
run_omp:
	./$(OMP_TARGET) 6 parall omp

run_mpi:
	./$(MPI_TARGET) 3 parall mpi

all: parallel 
=======
compile: clean serial parallel mpi

submit:
	@sbatch submit_serial.cfg
	@sbatch submit_openmp_1.cfg
	@sbatch submit_openmp_2.cfg
	@sbatch submit_openmp_4.cfg
	@sbatch submit_openmp_8.cfg
	@sbatch submit_openmp_16.cfg

run: compile submit
>>>>>>> 9b61a44 (ECE-563 (Jan 13, 2023))

clean:
	@rm -f slurm*
