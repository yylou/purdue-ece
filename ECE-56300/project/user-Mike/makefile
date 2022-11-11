#!/bin/bash

BUILD_DIR 	:= 	./bin
INCLUDES 	:= 	-I ./include
SER_TARGET	:= 	serial.o
ROOT_DIR 	:= 	./
SRC_DIR 	:= 	./src
SOURCES 	:= 	$(wildcard $(ROOT_DIR)/*.cpp $(SRC_DIR)/*.cpp)

CXXFLAGS 	:= 	-fopenmp -O3 -Wall -std=c++0x
MKDIR		:= 	@if [ ! -d "$(BUILD_DIR)" ]; then echo "reating $(BUILD_DIR)" folder; mkdir $(BUILD_DIR) ; fi

serial:
	$(MKDIR)
	@echo "Building for serial version ..."
	@g++ $(INCLUDES) $(SOURCES) -o $(BUILD_DIR)/$(SER_TARGET)
	@rm $(SER_TARGET)
	@ln -s $(BUILD_DIR)/$(SER_TARGET) .

parallel:
	$(MKDIR)

run:
	./$(SER_TARGET) serial 1

clean:
	@rm -r $(BUILD_DIR)
