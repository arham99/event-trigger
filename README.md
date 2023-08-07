## event-trigger

This code is used to recognize all coincidance events captured by multiple stations.

To run this code you NEED to install `ObsPy` library and import the `trigger` module.

The raw waveform file is in `.mseed` format.

**The output:**

1. One file consist of all coincidance events, timestamps, and the stations list.

2. The `.pick` file of all coincidance events compatible to be input of program `SeisGram2K70.jar`
