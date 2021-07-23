# python -m cProfile -s tottime runner.py > profile.txt

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
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())