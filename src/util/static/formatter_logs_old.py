import re

PATH = "C:\\Users\\Arseniy\\PycharmProjects\\TripMaker\\results\\"
INPUT_NAME = "mow_10.log"
list_input_lines = open(PATH + INPUT_NAME, 'r').read().splitlines()

list_templates = [[r"datetime\.datetime\(([0-9]+), ([0-9]+), ([0-9]+), [0-9]+, [0-9]+\)", r'"\1-\2-\3"'],
                  [r"([0-9]{4})-([0-9]{1})(-[0-9]{2})", r"\1-0\2\3"],
                  [r"([0-9]{4}-[0-9]{2})-([0-9]{1})([^0-9])", r"\1-0\2\3"],
                  [r"([0-9]{4})-([0-9]{1})-([0-9]{1})([^0-9])", r"\1-0\2-0\3\4"],
                  [r"'trip_class': <SeatClass\.economic: 'economic'>", r""],
                  [r"('price': [0-9]+)(,)", r"\1"],
                  [r"\'", '"']]

list_re_compiled = [[re.compile(t[0]), t[1]] for t in list_templates]

file_out = open(PATH + INPUT_NAME + "_modif", 'w')

for line in list_input_lines:
    for re_replace in list_re_compiled:
        line = re.sub(re_replace[0], re_replace[1], line)
    file_out.write("{}\n".format(line))
