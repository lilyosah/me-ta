import math
from csv import DictWriter

FILE_NAME = "proj2/metadata.txt"
WRITE_TO = "proj2/processed.txt"
ALLOWED_BOXES_IN_ROW = 100  # Play with this #
START_COL = 1
POSSIBLE_SPAN = ALLOWED_BOXES_IN_ROW
ROUND_WORDS = 10
# CSS PROPERTY MAPPING
COLOR_MAP = {
    'Email': "#ffadad",
    'Text': "#ffd6a5",
    'Reddit': "#fdffb6",
    'Slack': "#caffbf",
    'GroupMe': "#9bf6ff",
    'Discord': "#a0c4ff",
    'Zoom': "#bdb2ff",
    'WhatsApp': "#ffc6ff"
}

BORDER_RADIUS_MAP = {
    "Incoming": "0",
    "Outgoing": "20px",
    "Variable": ""
}


def process_metadata():
    f = open(FILE_NAME, "r")
    all_lines = f.readlines()
    axis = all_lines[0][:-1].split(",")[1:]
    data = []
    num_boxes_in_row = START_COL
    row = []
    platforms = []
    for line in all_lines[1:]:
        line = line[line.find(",")+1:]
        split = line[:-1].split(",")
        new_dict = {}
        for i in range(len(split)):
            new_dict[axis[i]] = split[i]
        print(new_dict["Content"])
        # Every 10 words is box
        num_boxes_needed = math.ceil(int(new_dict["Words"])/ROUND_WORDS)
        if num_boxes_needed == 0:
            num_boxes_needed += 1
        elif (num_boxes_needed > POSSIBLE_SPAN):
            num_boxes_needed = POSSIBLE_SPAN

        if (num_boxes_needed + num_boxes_in_row > POSSIBLE_SPAN):
            data.append(row)
            row = []
            num_boxes_in_row = START_COL

        if new_dict["Platform"] not in platforms:
            platforms.append(new_dict["Platform"])

        new_dict = add_css(new_dict, num_boxes_in_row,
                           num_boxes_needed, data)
        row.append(new_dict)
        num_boxes_in_row += num_boxes_needed

    f.close()
    data.append(row)
    return data


def add_css(new_dict, num_boxes_in_row, num_boxes_needed, data):
    css_dict = {}
    # Add col position
    css_dict["grid_col"] = "{} / span {}".format(
        num_boxes_in_row, num_boxes_needed)
    css_dict["grid_row"] = len(data)+1
    # Add border radius
    css_dict["border_radius"] = BORDER_RADIUS_MAP[new_dict["Incoming/Outgoing"]]
    # BG color
    css_dict["bg_color"] = COLOR_MAP[new_dict["Platform"]]
    css_dict["content"] = new_dict["Content"]

    return css_dict


data = process_metadata()

f = open(WRITE_TO, "a")

f.write("[")
for line in data:
    f.write(str(line)+",\n")
f.write("];")
f.close()
