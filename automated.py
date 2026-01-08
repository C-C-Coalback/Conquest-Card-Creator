from PIL import Image, ImageTk, ImageDraw, ImageFont
from dict_inits.card_types_dict_positions import card_types_dictionary_positions
from dict_inits.command_dict import command_dictionary
from dict_inits.loyalty_dict import loyalty_dictionary, resize_loyalty_dictionary
from dict_inits.icons_dict import icons_dict, special_text_dict
from process_card import process_submitted_card, process_submitted_planet_card
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


replacement_icons = [("Resources", "[RESOURCE]"), ("Resource", "[RESOURCE]"),
                     ("resources", "[RESOURCE]"), ("resource", "[RESOURCE]"),
                     ("Material", "[MATERIAL]"), ("Technology", "[TECHNOLOGY]"), ("Strongpoint", "[STRONGPOINT]"),
                     ("Faith Tokens", "[FAITH]"), ("Faith Token", "[FAITH]"),
                     ("faith tokens", "[FAITH]"), ("faith token", "[FAITH]"),
                     ("faith Tokens", "[FAITH]"), ("faith Token", "[FAITH]"),
                     ("Faith tokens", "[FAITH]"), ("Faith token", "[FAITH]"),
                     ("Faith", "[FAITH]"), ("faith", "[FAITH]"),
                     ("Necrotic", "Necrons"), ("Goes Fasta -", "Goes Fasta! — "),
                     ("Bloodthirst -", "Bloodthirst — "), ("Goes Fasta! -", "Goes Fasta! — "),
                     ("Unstoppable -", "Unstoppable — "), ("Hive Mind -", "Hive Mind — "),
                     ("(1x)", ""), ("(x1)", ""),
                     ("(2x)", ""), ("(x2)", ""),
                     ("(3x)", ""), ("(x3)", ""),
                     ("(4x)", ""), ("(x4)", ""),
                     ("(5x)", ""), ("(x5)", "")]

for faction in factions:
    replacement_icons.append((faction, ("[" + faction.upper() + "]").replace(" ", "_")))


replacement_icons.append(("Ork", "[ORKS]"))

csv_dir = "csv_blackstone"
card_number = 1
last_warlord_num = 55
current_sig_num = 1
current_warlord_num = last_warlord_num + 1
for filename in os.listdir(csv_dir):
    df = pd.read_csv(os.path.join(csv_dir, filename), header=None)
    df.columns = ["Faction", "Card Type", "Name", "Traits", "Text", "COST", "CMD", "ATK", "HP", "SHLD", "Loyal",
                  "Unique", "Notes", "State of Image", "Iridial Status"]
    df.drop("Notes", axis=1, inplace=True)
    df.drop("State of Image", axis=1, inplace=True)
    df.drop("Iridial Status", axis=1, inplace=True)
    df.dropna(subset=['Card Type'], inplace=True)
    df.drop(index=df.index[0], inplace=True)
    for current_pos in range(df.shape[0]):
        current_name = df['Name'].values[current_pos]
        current_faction = df['Faction'].values[current_pos]
        current_card_type = df['Card Type'].values[current_pos]
        current_traits = df['Traits'].values[current_pos]
        current_text = df['Text'].values[current_pos]
        current_cost = str(df['COST'].values[current_pos])
        current_cmd = str(df['CMD'].values[current_pos])
        current_atk = str(df['ATK'].values[current_pos])
        current_hp = str(df['HP'].values[current_pos])
        current_shld = str(df['SHLD'].values[current_pos])
        current_loyal = df['Loyal'].values[current_pos]
        current_unique = df['Unique'].values[current_pos]
        current_num = str(card_number)
        while len(current_num) < 3:
            current_num = "0" + current_num
        if current_card_type == "Warlord":
            current_warlord_num = last_warlord_num + 1
            current_sig_num = 2
            last_warlord_num = current_warlord_num
        if current_card_type != "Warlord" and current_name != "Rat Colony":
            if current_unique == "TRUE":
                current_unique = True
            else:
                current_unique = False
            new_text = current_text
            num_copies = 1
            if "(1x)" in new_text or "(x1)" in new_text:
                num_copies = 1
            elif "(2x)" in new_text or "(x2)" in new_text:
                num_copies = 2
            elif "(3x)" in new_text or "(x3)" in new_text:
                num_copies = 3
            elif "(4x)" in new_text or "(x4)" in new_text:
                num_copies = 4
            elif "(5x)" in new_text or "(x5)" in new_text:
                num_copies = 5
            for icon in replacement_icons:
                new_text = new_text.replace(icon[0], icon[1])
            for special_text in special_text_dict:
                extra_space = ""
                if special_text in ["[BATTLE:]", "[DEPLOY_ACTION:]", "[COMMAND_ACTION:]", "[COMBAT_ACTION:]",
                                    "[HEADQUARTERS_ACTION:]", "[REACTION:]", "[FORCED_REACTION:]", "[ACTION:]",
                                    "[INTERRUPT:]", "[FORCED_INTERRUPT:]"]:
                    extra_space = " "
                if special_text == "[CULTIST]":
                    new_text = new_text.replace(special_text_dict[special_text]["text"], special_text + extra_space)
                    new_text = new_text.replace("[CULTIST] token", "Cultist token")
                elif special_text == "[RED]":
                    if " Red " in new_text:
                        new_text = new_text.replace(special_text_dict[special_text]["text"], special_text + extra_space)
                elif special_text == "[ARMOR]":
                    if " Armor " in new_text:
                        new_text = new_text.replace(special_text_dict[special_text]["text"], special_text + extra_space)
                else:
                    new_text = new_text.replace(special_text_dict[special_text]["text"], special_text + extra_space)
            print(current_name)

            output_dir = os.getcwd()
            output_dir = os.path.join(output_dir, "created_cards_blackstone")
            output_dir = os.path.join(output_dir, current_faction)
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)
            stored_output_dir = output_dir
            output_dir = os.path.join(output_dir, current_name.replace(" ", "_") + ".png")
            auto_card_art_src = "images for conquest cards\\" + current_name.replace(" ", "_")
            if os.path.exists(auto_card_art_src + ".png"):
                auto_card_art_src = auto_card_art_src + ".png"
            elif os.path.exists(auto_card_art_src + ".jpg"):
                auto_card_art_src = auto_card_art_src + ".jpg"
            elif os.path.exists(auto_card_art_src + ".jpeg"):
                auto_card_art_src = auto_card_art_src + ".jpeg"
            elif os.path.exists(auto_card_art_src + ".webp"):
                auto_card_art_src = auto_card_art_src + ".webp"
            elif os.path.exists(auto_card_art_src + ".gif"):
                auto_card_art_src = auto_card_art_src + ".gif"
            if current_loyal == "Signature":
                for i in range(num_copies):
                    warlord_num_text = str(current_warlord_num)
                    while len(warlord_num_text) < 3:
                        warlord_num_text = "0" + warlord_num_text
                    sig_squad_text_number = "0" + str(current_sig_num) + "/09"
                    sig_squad_text = warlord_num_text + "    " + sig_squad_text_number
                    current_sig_num += 1
                    output_dir = os.path.join(stored_output_dir, current_name.replace(" ", "_") + "_"
                                              + str(i + 1) + ".png")
                    process_submitted_card(current_name, current_card_type, new_text, current_faction, current_traits,
                                           output_dir,
                                           attack=current_atk, health=current_hp, command=current_cmd,
                                           cost=current_cost,
                                           starting_cards="7", starting_resources="7",
                                           loyalty=current_loyal, shield_value=current_shld, bloodied=False,
                                           automated=True,
                                           auto_card_art_src=auto_card_art_src, unique=current_unique,
                                           card_number=current_num, sig_squad_text=sig_squad_text)
            else:
                process_submitted_card(current_name, current_card_type, new_text, current_faction, current_traits,
                                       output_dir,
                                       attack=current_atk, health=current_hp, command=current_cmd, cost=current_cost,
                                       starting_cards="7", starting_resources="7",
                                       loyalty=current_loyal, shield_value=current_shld, bloodied=False, automated=True,
                                       auto_card_art_src=auto_card_art_src, unique=current_unique,
                                       card_number=current_num)
        if current_name != "Rat Colony":
            card_number += 1

