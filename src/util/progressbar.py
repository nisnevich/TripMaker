CHAR_PROGRESS_FILLED ='✈'
CHAR_PROGRESS_EMPTY = '-'


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100,
                       fill=CHAR_PROGRESS_FILLED, empty = CHAR_PROGRESS_EMPTY):
    """
    Call in a loop to create terminal progress bar
    @params:
        :param iteration:   - Required  : current iteration (Int)
        :param total:       - Required  : total iterations (Int)
        :param prefix:      - Optional  : prefix string (Str)
        :param suffix:      - Optional  : suffix string (Str)
        :param decimals:    - Optional  : positive number of decimals in percent complete (Int)
        :param length:      - Optional  : character length of bar (Int)
        :param fill:        - Optional  : bar fill character (Str)
        :param empty:       - Optional  : bar empty character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + empty * (length - filled_length)
    print('\r{} |{}| {}% {}'.format(prefix, bar, percent, suffix), end="")
    if iteration == total:
        print()
