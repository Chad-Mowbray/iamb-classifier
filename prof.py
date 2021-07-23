# python -m cProfile -s tottime runner.py > profile.txt
# https://github.com/jrfonseca/gprof2dot

import cProfile, pstats, io
from pstats import SortKey
pr = cProfile.Profile(builtins=False)
pr.enable()

from runner import Runner
contents = "disceased earthshattering fireflies lamp-lit gentle haunts to pass address expeditiously\n"
r = Runner(contents)
r.initial_process_contents()

pr.disable()
s = io.StringIO()
# sortby = SortKey.CUMULATIVE
sortby = SortKey.TIME
stats = pstats.Stats(pr, stream=s)

ps = stats.sort_stats(sortby)
ps.print_stats()

stats.print_callers()
print(s.getvalue())