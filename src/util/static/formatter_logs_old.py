import re

from src.util.progressbar import print_progress_bar

PATH = "C:\\Users\\Arseniy\\PycharmProjects\\TripMaker\\results\\"
INPUT_NAME = "mow.002.log"
list_input_lines = open(PATH + INPUT_NAME, 'r').read().splitlines()

list_templates = [
        # Replace datetime object with its string representation
        [r"datetime\.datetime\(([0-9]+), ([0-9]+), ([0-9]+), [0-9]+, [0-9]+\)", r'"\1-\2-\3"'],
        # Dates with one-digit month
        [r"([0-9]{4})-([0-9]{1})(-[0-9]{2})", r"\1-0\2\3"],
        # Dates with one-digit day
        [r"([0-9]{4}-[0-9]{2})-([0-9]{1})([^0-9])", r"\1-0\2\3"],
        # Dates with both one-digit month and day
        [r"([0-9]{4})-([0-9]{1})-([0-9]{1})([^0-9])", r"\1-0\2-0\3\4"],
        # Remove "seat class"
        [r"'trip_class': <SeatClass\.economic: 'economic'>", r""],
        # Remove comma (prevented seat class) after price
        [r"('price': [0-9]+)(,)", r"\1"],
        # Change unary quotes to the double ones
        [r"\'", '"']]

list_re_compiled = [[re.compile(t[0]), t[1]] for t in list_templates]

file_out = open(PATH + INPUT_NAME + "_modif", 'w')

counter = 0
len_total = len(list_input_lines)

for line in list_input_lines:
    for re_replace in list_re_compiled:
        line = re.sub(re_replace[0], re_replace[1], line)
    file_out.write("{}\n".format(line))
    if counter % round(len_total / 100) == 0:
        print_progress_bar(counter, len_total, prefix='Processing:', decimals=0,
                           suffix='Complete', length=50)
    counter += 1
