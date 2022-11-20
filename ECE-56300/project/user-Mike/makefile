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
OMP_TARGET  :=  openmp.o
ROOT_DIR    :=  ./
SRC_DIR     :=  ./src
SOURCES     :=  $(wildcard $(ROOT_DIR)/*.cpp $(SRC_DIR)/*.cpp)

CXXFLAGS    :=  -O3 -Wall -std=c++17
MKDIR       :=  @if [ ! -d "$(BUILD_DIR)" ]; then echo "[ `date +'%Y-%m-%d %H:%M:%S'` ]      Creating $(BUILD_DIR)" folder; mkdir $(BUILD_DIR) ; fi

serial:
	$(MKDIR)
	@echo "[ `date +'%Y-%m-%d %H:%M:%S'` ]      Compiling serial version"
	@g++ $(CXXFLAGS) $(INCLUDES) $(SOURCES) -o $(BUILD_DIR)/$(SER_TARGET)
	@rm $(SER_TARGET)
	@ln -s $(BUILD_DIR)/$(SER_TARGET) .
	
parallel:
	$(MKDIR)
	@echo "[ `date +'%Y-%m-%d %H:%M:%S'` ]      Compiling parallel version"
	@g++ $(CXXFLAGS) -fopenmp $(INCLUDES) $(SOURCES) -o $(BUILD_DIR)/$(OMP_TARGET)
	@rm $(OMP_TARGET)
	@ln -s $(BUILD_DIR)/$(OMP_TARGET) .


run_serial:
	./$(SER_TARGET) 8 serial none

run_omp:
	./$(OMP_TARGET) 6 parall omp

run_mpi:
	./$(SER_TARGET) 16 parall mpi

all: clean parallel 

clean:
	@rm -r $(BUILD_DIR)
