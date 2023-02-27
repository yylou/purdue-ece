The implementation of your selected optimization goes here.
---

[Date]      2021.10.21  
[Update]  
    - [config3.ini]     Change log path (config3.ini)  
    - [config3.ini]     Fix 'window_size' = 3  
    - [sender.py]       Intialization (infrastructure define)  
    - [sender.py]       Fix 'timeout' = max( 0.4, min( 0.65, 1.65 * PACKET_SIZE / BW + 2 * PROP_DELAY ) )  
    - [receiver.py]     Intialization (infrastructure define)  