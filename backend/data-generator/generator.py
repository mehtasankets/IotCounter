#!/bin/python
import random

limit = [15, 20, 75, 75]
days = ["20160825", "20160824", "20160823", "20160822", "20160821", "20160820", "20160819", "20160818", "20160817", "20160816", "20160815", "20160814", "20160813", "20160812", "20160811", "20160810", "20160809", "20160808", "20160807", "20160806", "20160805", "20160804", "20160803", "20160802", "20160801"]
days.reverse()
i=0
f = open('data.txt', 'w')
f.write('{\n')
tables = ['phoenixBadmintonCounter', 'phoenixGymCounter', 'phoenixParkingCounter', 'rahejaParkingCounter']
for t in tables:
    f.write('  "' + t + '" : {\n')
    for d in days:
        f.write('    "' + d + '" : {' + '\n')
        total = 0
        for hour in range (0, 24):
            n = random.randint(1, limit[i])
            f.write(('      "%02d":' % hour) + str(n) + ',\n')
            total += n
        if(i > 1):
            f.write('      "total":' + str(int(total / 10)) + '\n')
        else:
            f.write('      "total":' + str(int(total * 3 / 4)) + '\n')
        if(d == days[-1]):
            f.write('    } \n')
        else:
            f.write('    }, \n')
    if(t == tables[-1]):
        f.write('  } \n')
    else:
        f.write('  }, \n')
    i += 1

f.write('}\n')
f.close()

print 'done!'

