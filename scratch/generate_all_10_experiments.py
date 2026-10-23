# scratch/generate_all_10_experiments.py
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
os.chdir(project_root)

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from experiments_common import (
    set_cell_background, set_cell_margins, add_image_placeholder,
    add_code_block, add_table_data, add_styled_heading, add_body_paragraph
)

from exp_data_part1 import EXP_1

print("Imported base modules successfully.")
