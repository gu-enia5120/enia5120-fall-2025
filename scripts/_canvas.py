from canvasapi import Canvas
import os
import re

pattern1 = r'GU_CANVAS'
pattern2 = r"(?<=\").*?(?=\")"
key = []
with open(os.path.expanduser('~/.creds'), 'r') as f:
   for line in f:
    if re.search(pattern1, line) is not None:
        match_2 = re.findall(pattern2, line)
        key.extend(match_2)

API_URL = "https://georgetown.instructure.com"
canvas_key = key[0]
canvas = Canvas(API_URL, canvas_key)

course = canvas.get_course(214224)
