/*
Author  : Yuan-Yao Lou (Mike)
Title   : PhD student in ECE at Purdue University
Email   : yylou@purdue.edu
Website : https://yylou.github.io/
Date    : 2022/11/11

Project : Purdue ECE56300 - Project
Version : v1.0 (Utility functions)
*/

#include <time.h>

#include <utility.hpp>

int compareString(char* src, const char* target) {
    if (strcmp(src, target) == 0) return 1;
    else return 0;
}

void log(std::string message, std::string argu, int skip) {
    time_t time_;
    struct tm *local;
    char date[70];
    time(&time_);
    local = localtime(&time_);
    strftime(date, 20, "%Y-%m-%d %H:%M:%S", local);
    if (skip == 1) printf("\n");
    printf("[ %s ]      %s: %s", date, message.c_str(), argu.c_str());
}