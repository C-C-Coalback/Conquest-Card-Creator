from PIL import Image, ImageTk, ImageDraw, ImageFont
from dict_inits.card_types_dict_positions import card_types_dictionary_positions
from dict_inits.command_dict import command_dictionary
from dict_inits.loyalty_dict import loyalty_dictionary, resize_loyalty_dictionary
from dict_inits.icons_dict import icons_dict, special_text_dict
import os
import random
import pandas as pd

card_types = ["Warlord", "Army", "Support", "Event", "Attachment", "Synapse", "Planet"]
factions = ["Space Marines", "Astra Militarum", "Orks", "Chaos", "Dark Eldar",
            "Eldar", "Tau", "Necrons", "Tyranids", "Neutral"]
loyalties = ["Common", "Loyal", "Signature"]
shields = ["0", "1", "2", "3"]
# (1440, 2052) card size
name_font = "fonts/Names/Conquestnames-Regular.ttf"
trait_font = "fonts/Ascender Serif/AscenderSerifW01-BdIt-Regular.otf"
text_font = "fonts/Ascender Serif/Ascender-Serif-W01-Regular.ttf"
text_bold_font = "fonts/Ascender Serif/Ascender-Serif-W01-Bold.ttf"
text_italics_font = "fonts/open_sans/OpenSans-Italic.ttf"
numbers_font = "fonts/numbers/Conquestnumbers-Regular.ttf"
name_size = 90
trait_size = 70
default_text_size = 62
numbers_size = 105


csv_space_marines = pd.read_csv("csv_blackstone/Blackstone Project Custom Cards - Space Marines.csv")



