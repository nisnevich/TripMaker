from time import sleep

from src.util.progressbar import print_progress_bar

counter = 0
list_test = range(0, 100)
print_progress_bar(counter, len(list_test), prefix='Processing:', suffix='Complete', length=50)
for i in list_test:
    sleep(0.1)
    counter += 1
    print("\n" + str(counter))
    print_progress_bar(counter, len(list_test), prefix='Processing:', suffix='Complete', length=50)
