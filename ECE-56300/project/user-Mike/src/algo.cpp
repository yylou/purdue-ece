/*
Author  : Yuan-Yao Lou (Mike)
Title   : PhD student in ECE at Purdue University
Email   : yylou@purdue.edu
Website : https://yylou.github.io/
Date    : 2022/11/11

Project : Purdue ECE56300 - Project
Version : v1.0 (Data Structures and Algorithms)
*/

<<<<<<< HEAD
//#include <mpi.h>

=======
#include <omp.h>
>>>>>>> 9b61a44 (ECE-563 (Jan 13, 2023))
#include <string>
#include <sstream>
#include <fstream>
#include <map>
#include <omp.h>
#include <utility.hpp>
#include <algo.hpp>

// #define LOG
#define numFiles 15

std::map<int,std::vector<std::string>> filesMap;        // for reader threads to parse specified files
QueueContainer contentQueueContainer;                   // [MAPPER  QUEUE] for reader threads to put work items
QueueContainer dataQueueContainer;                      // [REDUCER QUEUE] for mapper threads to put combined record
int threads = 0;                                        // for mapper to put work items to reducer queues by hashing
std::map<int,int> readersClockOut;                      // for mapper to stop pushing work items to reducer queues
int mappersClockOut = 0;                                // for reducer to stop getting work items from reducer queues
std::map<std::string,int> hashTable;                    // [FINAL ANSWER]

<<<<<<< HEAD

=======
omp_lock_t queueContentLocks[numFiles];
omp_lock_t queueDataLocks[numFiles];
omp_lock_t readerLock, mapperLock, counterLock;
>>>>>>> 9b61a44 (ECE-563 (Jan 13, 2023))

void init(int maxThreads) {
    threads = maxThreads;
    
    int filesPerThread = numFiles / threads;            // ──┐ divmod 
    int remain = numFiles - filesPerThread * threads;   // ──┘ 

    /*  (1) Queue Container: each element is a queue for a specific thread  */
    int prev = 1;
    for (int tid=0 ; tid<threads ; ++tid) {
        contentQueueContainer.emplace_back(std::queue<WorkItem>());
        dataQueueContainer.emplace_back(std::queue<WorkItem>());

        /*  (2) Files Map: each thread is assigned with 0+ files  */
        int fid;
        for (fid=prev ; fid<(prev + filesPerThread + (tid < remain)) ; ++fid) {
            filesMap[tid].push_back("./data/" + std::to_string((int) fid) + ".txt");
        }
        prev = fid;
    }
<<<<<<< HEAD
=======

    /*  (3) Lock initialization  */
    for(int i=0 ; i<numFiles ; i++) {
        omp_init_lock(&queueContentLocks[i]);
        omp_init_lock(&queueDataLocks[i]);
    }
    omp_init_lock(&readerLock);
    omp_init_lock(&mapperLock);
    omp_init_lock(&counterLock);
>>>>>>> 9b61a44 (ECE-563 (Jan 13, 2023))
}

int getFilesMapSize    (int queueId) { return filesMap[queueId].size(); }
int getMapperQueueSize (int queueId) { return contentQueueContainer[queueId].size(); }
int getReducerQueueSize(int queueId) { return dataQueueContainer[queueId].size();    }

void wrapWorkItems(int queueId, std::string line) {
    std::string word;
 
    for (std::istringstream is(line) ; is>>word ; ) {
        if (word == " " || line.empty()) continue;
        WorkItem workItem(word, 1);

<<<<<<< HEAD
        /*  LOCK ACQUIRE  */
        omp_lock_t lck;
        omp_init_lock (&lck); 
        omp_set_lock(&lck);
        contentQueueContainer[queueId].push(workItem);
        /*  LOCK RELEASE  */
        omp_unset_lock(&lck);
        omp_destroy_lock(&lck);
=======
        omp_set_lock(&queueContentLocks[queueId]);
        contentQueueContainer[queueId].push(workItem);
        omp_unset_lock(&queueContentLocks[queueId]);
>>>>>>> 9b61a44 (ECE-563 (Jan 13, 2023))
    }
}

void putMapper(int queueId) {
    if (filesMap[queueId].size() == 0) return;

    for (const auto& fileName : filesMap[queueId]) {
        std::ifstream inputFile(fileName);

        if (inputFile.is_open()) {
            // #ifdef LOG
            log("Parse", fileName+"\n", 0);
            // #endif

            std::string line;
            while (getline(inputFile, line)) {      // line by line
                wrapWorkItems(queueId, line);       // word by word -> put work items to queue by id
            }
            line.clear();

        } else {
            log("FILE NOT FOUND", fileName+"\n", 0);
        }

<<<<<<< HEAD
        /*  LOCK ACQUIRE  */
        omp_lock_t lck;
        omp_init_lock (&lck); 
        omp_set_lock(&lck);
        ++readersClockOut[queueId];                  // reader clocks in when finishing
        /*  LOCK RELEASE  */
        omp_unset_lock(&lck);
        omp_destroy_lock(&lck);
    }
}

void putReducer1(int queueId, int size) {
 
    int batch = size;
=======
        omp_set_lock(&readerLock);
        ++readersClockOut[queueId];                  // reader clocks in when finishing
        inputFile.close();
        omp_unset_lock(&readerLock);
    }
}

void putReducer(int queueId, int size) {
>>>>>>> 9b61a44 (ECE-563 (Jan 13, 2023))
    std::hash<std::string> hash;
    std::vector<WorkItem> workItems;
    std::map<std::string,int> counter;
    
    while (readersClockOut[queueId] < filesMap[queueId].size() ||
           getMapperQueueSize(queueId) > 0) {       // TRUE @ reader is reading OR queue is not empty
<<<<<<< HEAD
        
        /*  (1) GET work items  */
        batch = size;

        while (getMapperQueueSize(queueId) > 0 && batch-- > 0) {
            workItems.push_back(contentQueueContainer[queueId].front());
            
            /*  LOCK ACQUIRE  */
            omp_lock_t lck;
            omp_init_lock(&lck); 
            omp_set_lock(&lck);
            contentQueueContainer[queueId].pop();
            /*  LOCK RELEASE  */
            omp_unset_lock(&lck);
            omp_destroy_lock(&lck);
        }
=======
>>>>>>> 9b61a44 (ECE-563 (Jan 13, 2023))


        #ifdef LOG
        log("Retrieve", std::to_string(queueId)+"\n", 0);
        #endif

        /*  (1) GET work items  */
        omp_set_lock(&queueContentLocks[queueId]);
        while (getMapperQueueSize(queueId) > 0 && workItems.size() < size) {
            workItems.push_back(contentQueueContainer[queueId].front());
            contentQueueContainer[queueId].pop();
        }
        omp_unset_lock(&queueContentLocks[queueId]);

        #ifdef LOG
        log("Combine", std::to_string(queueId)+"\n", 0);
        #endif
        /*  (2) COMBINE records (work items)  */

        for (const auto& iter : workItems) {
<<<<<<< HEAD
            #ifdef LOG
            printf("%50s  |  %10d  |  key: %zu\n", iter.word.c_str(), iter.count, hash(iter.word));
            #endif
            omp_lock_t lck2;
            omp_init_lock(&lck2); 
            omp_set_lock(&lck2);            
=======
>>>>>>> 9b61a44 (ECE-563 (Jan 13, 2023))
            ++counter[iter.word];
            omp_unset_lock(&lck2);
            omp_destroy_lock(&lck2);
        }


        #ifdef LOG
        log("Push (mapper -> reducer)", std::to_string(queueId)+"\n", 0);
        #endif
        
        /*  (3) PUSH to reducer queue by hash functions  */

        for (const auto& [word, count] : counter) {
            #ifdef LOG
            printf("%50s  |  %10d  |  key: %zu\n", word.c_str(), count, hash(word));
            tmpCounter += count;
            #endif
            
            WorkItem workItem(word, count);
            int reducerQueueId = hash(word) % threads;  // hash to get recuder queue id
<<<<<<< HEAD

            /*  LOCK ACQUIRE  */
            omp_lock_t lck1;
            omp_init_lock (&lck1); 
            omp_set_lock(&lck1);
            dataQueueContainer[reducerQueueId].push(workItem_);
            /*  LOCK RELEASE  */
            omp_unset_lock(&lck1);
            omp_destroy_lock(&lck1);
        }


        #ifdef LOG
        printf("%50s  |  %10d  |\n", "(total)", tmpCounter);
        #endif
        omp_lock_t lck3;
        omp_init_lock (&lck3); 
        omp_set_lock(&lck3);
=======
            
            omp_set_lock(&queueDataLocks[reducerQueueId]);
            dataQueueContainer[reducerQueueId].push(workItem);
            omp_unset_lock(&queueDataLocks[reducerQueueId]);
        }

>>>>>>> 9b61a44 (ECE-563 (Jan 13, 2023))
        workItems.clear();
        omp_unset_lock(&lck3);
        omp_destroy_lock(&lck3);

<<<<<<< HEAD
        omp_lock_t lck4;
        omp_init_lock (&lck4); 
        omp_set_lock(&lck4);
        counter.clear();
        omp_unset_lock(&lck4);
        omp_destroy_lock(&lck4);
    }
    /*  LOCK ACQUIRE  */
    omp_lock_t lck5;
    omp_init_lock (&lck5); 
    omp_set_lock(&lck5);
    mappersClockOut++;   // mapper clocks in when finishing
    omp_unset_lock(&lck5);
    omp_destroy_lock(&lck5);
=======
    // omp_set_lock(&mapperLock);
    mappersClockOut++;   // mapper clocks in when finishing
    // omp_unset_lock(&mapperLock);
>>>>>>> 9b61a44 (ECE-563 (Jan 13, 2023))
}

void getReducer(int queueId, int size) {
    std::vector<WorkItem> workItems;

    while (mappersClockOut != 1 ||
           getReducerQueueSize(queueId) > 0) {      // TRUE @ mapper is combining OR queue is not empty
        
        omp_set_lock(&queueDataLocks[queueId]);
        while (getReducerQueueSize(queueId) > 0 && workItems.size() < size) {
            workItems.push_back(dataQueueContainer[queueId].front());
<<<<<<< HEAD
            
            /*  LOCK ACQUIRE  */
            omp_lock_t lck;
            omp_init_lock (&lck); 
            omp_set_lock(&lck);
            dataQueueContainer[queueId].pop();
            /*  LOCK RELEASE  */
            omp_unset_lock(&lck);
            omp_destroy_lock(&lck);
=======
            dataQueueContainer[queueId].pop();
>>>>>>> 9b61a44 (ECE-563 (Jan 13, 2023))
        }
        omp_unset_lock(&queueDataLocks[queueId]);

        #ifdef LOG
        log("Count", "\n", 0);
        #endif

        omp_set_lock(&counterLock);
        for (const auto& iter : workItems) { hashTable[iter.word] += iter.count; }
        omp_unset_lock(&counterLock);

        workItems.clear();
    }
}

void printWordCount() {
    long total = 0;
    for (const auto& pair : hashTable) {
        // printf("%50s  |  %10d\n", pair.first.c_str(), pair.second);
        total += pair.second;
    }
    printf("%50s  |  %10lu\n", "(total @ Final)", total);
}