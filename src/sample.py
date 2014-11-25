#!/usr/bin/env python
import sys
import os

if len(sys.argv) != 2:
    print 'Usage: %s SAMPLE_ID' % (sys.argv[0])
    sys.exit(1)

for size_mb in [0.5, 1, 2, 5, 10]:
    for time_s in [5, 10, 30, 60, 150, 300, 600, 1000, 1500]:

        size  = 1024 * size_mb
        time  = time_s
        nodes = 600
        conn  = 15
        hours = 2 * time
        fname = 's%d_t%d_%s.json' % (size, time, sys.argv[1])

        print 'Computing %s for %d hours' % (fname, hours)

        os.system('time ./simulation.py -s%d -t%d -n%d -c%d -o%s %d' % (
            size, time, nodes, conn, fname, hours
        ))
