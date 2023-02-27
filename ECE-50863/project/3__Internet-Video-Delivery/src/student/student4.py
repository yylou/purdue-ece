from typing import List

# Adapted from code by Zach Peats

# ======================================================================================================================
# Do not touch the client message class!
# ======================================================================================================================


class ClientMessage:
    """
    This class will be filled out and passed to student_entrypoint for your algorithm.
    """
    total_seconds_elapsed:      float   # The number of simulated seconds elapsed in this test
    previous_throughput:        float   # The measured throughput for the previous chunk in kB/s

    buffer_current_fill:        float   # The number of kB currently in the client buffer
    buffer_seconds_per_chunk:   float   # Number of seconds that it takes the client to watch a chunk. Every
                                        # buffer_seconds_per_chunk, a chunk is consumed from the client buffer.
    buffer_seconds_until_empty: float   # The number of seconds of video left in the client buffer. A chunk must
                                        # be finished downloading before this time to avoid a rebuffer event.
    buffer_max_size:            float   # The maximum size of the client buffer. If the client buffer is filled beyond
                                        # maximum, then download will be throttled until the buffer is no longer full

    # The quality bitrates are formatted as follows:
    #
    #   quality_levels is an integer reflecting the # of quality levels you may choose from.
    #
    #   quality_bitrates is a list of floats specifying the number of kilobytes the upcoming chunk is at each quality
    #   level. Quality level 2 always costs twice as much as quality level 1, quality level 3 is twice as big as 2, and
    #   so on.
    #       quality_bitrates[0] = kB cost for quality level 1
    #       quality_bitrates[1] = kB cost for quality level 2
    #       ...
    #
    #   upcoming_quality_bitrates is a list of quality_bitrates for future chunks. Each entry is a list of
    #   quality_bitrates that will be used for an upcoming chunk. Use this for algorithms that look forward multiple
    #   chunks in the future. Will shrink and eventually become empty as streaming approaches the end of the video.
    #       upcoming_quality_bitrates[0]: Will be used for quality_bitrates in the next student_entrypoint call
    #       upcoming_quality_bitrates[1]: Will be used for quality_bitrates in the student_entrypoint call after that
    #       ...
    #
    quality_levels:             int
    quality_bitrates:           List[float]
    upcoming_quality_bitrates:  List[List[float]]

    # You may use these to tune your algorithm to each user case! Remember, you can and should change these in the
    # config files to simulate different clients!
    #
    #   User Quality of Experience =    (Average chunk quality) * (Quality Coefficient) +
    #                                   -(Number of changes in chunk quality) * (Variation Coefficient)
    #                                   -(Amount of time spent rebuffering) * (Rebuffering Coefficient)
    #
    #   *QoE is then divided by total number of chunks
    #
    quality_coefficient:        float
    variation_coefficient:      float
    rebuffering_coefficient:    float


# ======================================================================================================================


# Your helper functions, variables, classes here. You may also write initialization routines to be called
# when this script is first imported and anything else you wish.
STARTUP_STAGE = True
prev_decision, prev_buffer = None, 0

def rate_to_quality(chunk_size: dict, rate: float) -> int:
    for i in range(2, -1, -1):
        if rate >= chunk_size[i]: return i
    
    return 0

def threshold(chunk_size: dict, prev_R: float) -> tuple:
    chunk_size = list(chunk_size.items())
    chunk_size.sort(key=lambda tup: tup[1] , reverse=True)

    candidate = [i[1] for i in chunk_size if i[1] > prev_R]
    if not candidate: R_plus = prev_R
    else: R_plus = min(candidate)
    
    candidate = [i[1] for i in chunk_size if i[1] < prev_R]
    if not candidate: R_minus = prev_R
    else: R_minus = max(candidate)

    return R_minus, R_plus

def chunk_map(chunk_size: dict, cur_buffer: float, R_minus: float, R_plus: float, prev_R: float) -> float:
    chunk_size = list(chunk_size.items())
    chunk_size.sort(key=lambda tup: tup[1] , reverse=True)

    # x - C_min : C_max - C_min = cur_buffer : B_max
    cur_buffer = ((chunk_size[0][1] - chunk_size[-1][1]) * cur_buffer) / 30.0 + chunk_size[-1][1]

    selected_rate = None
    if   cur_buffer >= R_plus:
        candidate = [i[1] for i in chunk_size if i[1] < cur_buffer]
        if not candidate: selected_rate = prev_R
        else: selected_rate = max(candidate)

    elif cur_buffer <= R_minus:
        candidate = [i[1] for i in chunk_size if i[1] > cur_buffer]
        if not candidate: selected_rate = prev_R
        else: selected_rate = min(candidate)

    else: selected_rate = prev_R

    return selected_rate

def MPC(client_message: ClientMessage, prev_Q: int):
    import itertools

    # QoE Initialization
    look_ahead_size = 9
    permutation = [_ for _ in itertools.product([q for q in range(1, client_message.quality_levels + 1)], repeat=look_ahead_size)]

    QoE = dict()
    for _ in permutation: QoE[_] = []

    # Quality + Quality Variation
    for key in QoE:
        QoE_score = sum(key)

        variation = 0
        for i in range(0, len(key)):
            if i == 0: 
                if prev_Q != 0: variation += abs(key[i] - prev_Q)
                else: variation += 0
            else: variation += abs(key[i] - key[i-1])
        
        QoE[key].append(4  * QoE_score)
        QoE[key].append(client_message.variation_coefficient * variation * -1)

    cur_buffer = client_message.buffer_seconds_until_empty
    throughput = client_message.previous_throughput if client_message.previous_throughput != 0 else 2.0
    look_ahead = [client_message.quality_bitrates] + client_message.upcoming_quality_bitrates[:look_ahead_size - 1] if len(client_message.upcoming_quality_bitrates) > look_ahead_size - 1 else [client_message.quality_bitrates] + client_message.upcoming_quality_bitrates[:]
    time       = []

    # Download time
    for wnd in look_ahead:
        tmp = []
        for size in wnd: tmp.append(size / throughput)
        time.append(tmp)

    # Rebuffer Time
    for key in QoE:
        tmp_buffer    = cur_buffer
        rebuffer_time = 0
        for i in range(len(time)):
            rebuffer_time += max(time[i][key[i]-1] - tmp_buffer, 0)
            tmp_buffer     = max(tmp_buffer - time[i][key[i]-1], 0)
        
        QoE[key].append(client_message.rebuffering_coefficient * rebuffer_time * -1)
        QoE[key].append(4 * tmp_buffer)

    Q = max(QoE, key= lambda x: sum(QoE[x]))[0] - 1
    return Q

def BBA2_mod(client_message: ClientMessage):
    global STARTUP_STAGE, prev_decision, prev_buffer

    max_buffer      = client_message.buffer_max_size
    cur_buffer      = client_message.buffer_seconds_until_empty
    chunk_size      = dict(enumerate(client_message.quality_bitrates))  # (Quality: Chunk Size, e.g., {0: 1.2, 1: 2.4, 2: 4.8})
    reservoir       = chunk_size[0]

    R_min, R_max    = chunk_size[0], chunk_size[2]                      # (e.g., chunk_size[0] = 1.2, chunk_size[2] = 4.8)
    pre_throughput  = client_message.previous_throughput if client_message.previous_throughput != 0 else 2.0
    prev_Q, prev_R  = prev_decision[0] if prev_decision is not None else 0, prev_decision[1] if prev_decision is not None else R_min
    R_minus, R_plus = threshold(chunk_size, prev_R)

    selected_quality = None

    if STARTUP_STAGE:
        suggested_rate = chunk_map(chunk_size, cur_buffer, R_minus, R_plus, prev_R)
        suggested_q = rate_to_quality(chunk_size, suggested_rate)
        delta_B = 1 - client_message.quality_bitrates[suggested_q] / pre_throughput
        selected_quality = min(2, prev_Q+1) if delta_B > 0.45 else prev_Q

        if cur_buffer < prev_buffer or suggested_rate > prev_R: STARTUP_STAGE = False

    else:
        if   cur_buffer <= reservoir:        selected_quality = rate_to_quality(chunk_size, R_min)
        elif cur_buffer >= max_buffer * 0.4: selected_quality = rate_to_quality(chunk_size, R_max)
        else: selected_quality = MPC(client_message, prev_Q)

    prev_buffer, prev_decision = cur_buffer, (selected_quality, chunk_size[selected_quality])
    return selected_quality

def student_entrypoint(client_message: ClientMessage):
    """
    Your mission, if you choose to accept it, is to build an algorithm for chunk bitrate selection that provides
    the best possible experience for users streaming from your service.

    Construct an algorithm below that selects a quality for a new chunk given the parameters in ClientMessage. Feel
    free to create any helper function, variables, or classes as you wish.

    Simulation does ~NOT~ run in real time. The code you write can be as slow and complicated as you wish without
    penalizing your results. Focus on picking good qualities!

    Also remember the config files are built for one particular client. You can (and should!) adjust the QoE metrics to
    see how it impacts the final user score. How do algorithms work with a client that really hates rebuffering? What
    about when the client doesn't care about variation? For what QoE coefficients does your algorithm work best, and
    for what coefficients does it fail?

    Args:
        client_message : ClientMessage holding the parameters for this chunk and current client state.

    :return: float Your quality choice. Must be one in the range [0 ... quality_levels - 1] inclusive.
    """

    return BBA2_mod(client_message)