/*
Author  : Yuan-Yao Lou (Mike)
Title   : PhD student in ECE at Purdue University
Email   : yylou@purdue.edu
Website : https://yylou.github.io/
Date    : 2022/11/11

Project : Purdue ECE56300 - Project
Version : v1.0 (Data Structures and Algorithms)
*/

#include <mpi.h>
#include <string>
#include <sstream>
#include <fstream>
#include <map>
//#include <omp.h>
#include <utility.hpp>
#include <algoMpi.hpp>

//#include <queue>
//#include <vector>
// #define LOG
#define numFiles 15

std::map<int,std::vector<std::string>> filesMap;        // for reader threads to parse specified files
QueueContainer contentQueueContainer;                   // [MAPPER  QUEUE] for reader threads to put work itemsextern 
QueueContainer dataQueueContainer;                      // [REDUCER QUEUE] for mapper threads to put combined record
int threads = 0;                                        // for mapper to put work items to reducer queues by hashing
std::map<int,int> readersClockOut;                      // for mapper to stop pushing work items to reducer queues
int mappersClockOut;                                    // for reducer to stop getting work items from reducer queues
std::map<std::string,int> hashTable;                    // [FINAL ANSWER]

MPI_Datatype makeType(int rows, MPI_Datatype Particletype){
   // define the data type here
    MPI_Datatype b, block;
    MPI_Type_vector(rows, 1, 1, Particletype, &b);
    MPI_Type_commit(&b);
    MPI_Type_create_resized(b, 0, 1*sizeof(Particletype), &block);
    MPI_Type_commit(&block);
    return block;
    //return b;
}

void init2(int maxThreads){
    threads = maxThreads;
    for (int i=0 ; i<threads ; i++) {
        contentQueueContainer.emplace_back(std::queue<WorkItem>());
        dataQueueContainer.emplace_back(std::queue<WorkItem>());
    }
}


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
}

int getMapperQueueSize (int queueId) { return contentQueueContainer[queueId].size(); }
int getReducerQueueSize(int queueId) { return dataQueueContainer[queueId].size();    }

void wrapWorkItems(int queueId, std::string line) {
    #ifdef LOG
    log("[Line]", line+"\n", 0);
    #endif
    
    std::string word;    
    for (std::istringstream is(line) ; is>>word ; ) {
        if (word == " " || line.empty()) continue;
        WorkItem workItem(word, 1);

        /*  LOCK ACQUIRE  */
        contentQueueContainer[queueId].push(workItem);
        /*  LOCK RELEASE  */
    }
}

void putMapper(int queueId, MPI_Datatype &Particletype) {
    
    int global_content_size;
    for (const auto& fileName : filesMap[queueId]) {
        std::ifstream inputFile(fileName);

        if (inputFile.is_open()) {
            #ifdef LOG
            log("Parse", fileName+"\n", 0);
            #endif

            std::string line;
            while (getline(inputFile, line)) {      // line by line
                wrapWorkItems(queueId, line);       // word by word -> put work items to queue by id
            }

        } else {
            log("FILE NOT FOUND", fileName+"\n", 0);
        }

        ++readersClockOut[queueId];                  // reader clocks in when finishing
        /*  LOCK RELEASE  */
    }

     //MPI_Barrier(MPI_COMM_WORLD);
     global_content_size = getMapperQueueSize(queueId);
     //printf("global_content_size in putMapper = %d\n", global_content_size);
     MPI_Send(&contentQueueContainer[queueId], 1, makeType(global_content_size, Particletype), queueId+3, 0, MPI_COMM_WORLD);
     printf("global_content_size in putMapper = %d\n", global_content_size);
     //MPI_Send(&contentQueueContainer[queueId], global_content_size, Particletype, queueId+3, 0, MPI_COMM_WORLD);
     //MPI_Send(&global_content_size, 1, MPI_INT, queueId+3, 0, MPI_COMM_WORLD);
}

void putReducer(int queueId, int size, MPI_Status &status, MPI_Datatype &Particletype) {

    int batch = size;
    int global_content_size;
    int global_data_size;

    std::hash<std::string> hash;
    std::vector<WorkItem> workItems;
    std::map<std::string,int> counter;
    QueueContainer contentQueueContainer;   // buffer                  
    

    MPI_Probe(queueId, 0, MPI_COMM_WORLD, &status);
    MPI_Get_count(&status, Particletype, &global_content_size); 
    printf("global_content_size in putReducer = %d\n", global_content_size);
    
    std::queue <WorkItem> *received_queue = NULL;
    received_queue = (std::queue <WorkItem > *) malloc (global_content_size * sizeof (std::queue <WorkItem>));
    for(int i=0; i<3; i++){
    	if(i == queueId){
		    contentQueueContainer.emplace_back(*received_queue);
	    }
	    else{
		    contentQueueContainer.emplace_back(std::queue <WorkItem>());
	    }
    }


    //MPI_Recv(&contentQueueContainer[queueId], 1, makeType(getMapperQueueSize(queueId), Particletype), queueId, 0, MPI_COMM_WORLD, &status);
    //MPI_Barrier(MPI_COMM_WORLD);
    //MPI_Recv(&contentQueueContainer[queueId], global_content_size, Particletype, queueId, 0, MPI_COMM_WORLD, &status);
    MPI_Recv(&contentQueueContainer[queueId], 1, makeType(global_content_size, Particletype), queueId, 0, MPI_COMM_WORLD, &status);
    //if (getMapperQueueSize(queueId) == 0) return;   // REMOVE for parallel version

    while (readersClockOut[queueId] < filesMap[queueId].size() ||
           getMapperQueueSize(queueId) > 0) {       // TRUE @ reader is reading OR queue is not empty
        
        /*  (1) GET work items  */
        batch = size;

        while (getMapperQueueSize(queueId) > 0 && batch-- > 0) {
            workItems.push_back(contentQueueContainer[queueId].front());
            
            /*  LOCK ACQUIRE  */
            contentQueueContainer[queueId].pop();
            /*  LOCK RELEASE  */
        }


        #ifdef LOG
        log("Combine", "\n", 0);
        #endif

        /*  (2) COMBINE records (work items)  */

        for (const auto& iter : workItems) {
            #ifdef LOG
            printf("%50s  |  %10d  |  key: %zu\n", iter.word.c_str(), iter.count, hash(iter.word));
            #endif       
            ++counter[iter.word];
        }


        #ifdef LOG
        log("Push (mapper -> reducer)", "\n", 0);
        int tmpCounter = 0;
        #endif
        
        /*  (3) PUSH to reducer queue by hash functions  */

        for (const auto& [word, count] : counter) {
            #ifdef LOG
            printf("%50s  |  %10d  |  key: %zu\n", word.c_str(), count, hash(word));
            tmpCounter += count;
            #endif
            
            WorkItem workItem_(word, count);
            int reducerQueueId = hash(word) % threads;  // hash to get recuder queue id

            /*  LOCK ACQUIRE  */
            dataQueueContainer[reducerQueueId].push(workItem_);
            /*  LOCK RELEASE  */
        }


        #ifdef LOG
        printf("%50s  |  %10d  |\n", "(total)", tmpCounter);
        #endif

        workItems.clear();
        counter.clear();
    }

    mappersClockOut++;   // mapper clocks in when finishing
    global_data_size = getReducerQueueSize(queueId);
    printf("global_data_size in putReducer = %d\n", global_data_size); 
    //MPI_Send(&dataQueueContainer[queueId], 1, makeType(getReducerQueueSize(queueId), Particletype), queueId+6, 0, MPI_COMM_WORLD);
    //MPI_Send(&global_data_size, 1, MPI_INT, queueId+6, 0, MPI_COMM_WORLD);
    MPI_Send(&dataQueueContainer[queueId], 1, makeType(global_data_size, Particletype), queueId+6, 0, MPI_COMM_WORLD);
    //MPI_Send(&dataQueueContainer[queueId], global_data_size,  Particletype, queueId+6, 0, MPI_COMM_WORLD);
}

void getReducer(int queueId, int size, MPI_Status &status, MPI_Datatype &Particletype) {
    int global_data_size;

    //MPI_Recv(&global_data_size, 1, MPI_INT, queueId+3, 0, MPI_COMM_WORLD, &status);
    //MPI_Recv(&dataQueueContainer[queueId], 1, makeType(getReducerQueueSize(queueId), Particletype), queueId+3, 0, MPI_COMM_WORLD, &status);
    //MPI_Recv(&dataQueueContainer[queueId], global_data_size[queueId%3],  Particletype, queueId-3, 0, MPI_COMM_WORLD, &status);
    int batch = size;
    std::vector<WorkItem> workItems;


    //if (getReducerQueueSize(queueId) == 0) return;  // REMOVE for parallel version
    

    MPI_Probe(queueId+6, 0, MPI_COMM_WORLD, &status);
    MPI_Get_count(&status, Particletype, &global_data_size);
    QueueContainer dataQueueContainer;   
    std::queue <WorkItem> *received_queue = NULL;
    received_queue = (std::queue <WorkItem > *) malloc (global_data_size * sizeof (std::queue <WorkItem>));
    for(int i=0; i<3; i++){
    	if(i == queueId){
		    dataQueueContainer.emplace_back(*received_queue);
	    }
	    else{
		    dataQueueContainer.emplace_back(std::queue <WorkItem>());
	    }
    }
    printf("global_data_size in getReducer = %d\n", global_data_size);
    MPI_Recv(&dataQueueContainer[queueId], 1, makeType(global_data_size, Particletype), queueId+3, 0, MPI_COMM_WORLD, &status);
    //MPI_Recv(&dataQueueContainer[queueId], 1, makeType(getReducerQueueSize(queueId), Particletype), queueId+3, 0, MPI_COMM_WORLD, &status);
    //MPI_Recv(&dataQueueContainer[queueId], global_data_size,  Particletype, queueId+3, 0, MPI_COMM_WORLD, &status);


    while (mappersClockOut < threads ||
           getReducerQueueSize(queueId) > 0) {      // TRUE @ mapper is combining OR queue is not empty
        
        batch = size;
        while (getReducerQueueSize(queueId) > 0 && batch-- > 0) {
            workItems.push_back(dataQueueContainer[queueId].front());
            
            /*  LOCK ACQUIRE  */
            dataQueueContainer[queueId].pop();
            /*  LOCK RELEASE  */
        }

        #ifdef LOG
        log("Count", "\n", 0);
        #endif

        for (const auto& iter : workItems) {
            #ifdef LOG
            printf("%50s  |  %10d\n", iter.word.c_str(), iter.count);
            #endif
            
            hashTable[iter.word]++;
        }

        workItems.clear();
    }
}

void printWordCount() {
    for (const auto& pair : hashTable) {
        printf("%50s  |  %10d\n", pair.first.c_str(), pair.second);
    }
}
