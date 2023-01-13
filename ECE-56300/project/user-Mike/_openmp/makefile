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
PAR_TARGET  :=  parallel.o
MPI_TARGET  :=	mpi.o
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
	@echo "[ `date +'%Y-%m-%d %H:%M:%S'` ]      Compiling OpenMP version"
	@mpiicpc -qopenmp $(CXXFLAGS) $(INCLUDES) $(SOURCES) -o $(BUILD_DIR)/$(PAR_TARGET)
	@rm -f $(PAR_TARGET)
	@ln -s $(BUILD_DIR)/$(PAR_TARGET) .

mpi:
	$(MKDIR)
	@echo "[ `date +'%Y-%m-%d %H:%M:%S'` ]      Compiling MPI version"
	@mpiicpc -qopenmp $(CXXFLAGS) $(INCLUDES) $(SOURCES) -o $(BUILD_DIR)/$(MPI_TARGET)
	@rm -f $(MPI_TARGET)
	@ln -s $(BUILD_DIR)/$(MPI_TARGET) .

compile: clean serial parallel mpi

submit:
	@echo "Submit OpenMP version"
	@sbatch submit_openmp_4.cfg

run: compile submit

clean:
	@rm -f slurm*
