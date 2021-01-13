from helps import *
import os

html = get_one_page(os.getenv('URL'))
parse_one_page(html)