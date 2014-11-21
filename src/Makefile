run:
	time python simulation.py -s348 -t600 -n673 -c15 1500
test:
	time python simulation.py -s348 -t600 -n673 -c15 1
profile:
	time python -m cProfile -o profile simulation.py -s348 -t600 -n6735 -c30 1
review:
	python -c 'import pstats; pstats.Stats("profile").strip_dirs().sort_stats("cumulative").print_stats(30)'
dot:
	dot network.dot -Tpng -o network.png
	dot ledger.dot  -Tpng -o ledger.png
open:
	open -g network.png
	open -g ledger.png
refresh:
	osascript refresh.scpt
clean:
	rm -f *.{dot,png,pyc} profile
