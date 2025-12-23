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


def get_pil_text_size(text, font_size, font_name):
    font = ImageFont.truetype(font_name, font_size)
    size = font.getbbox(text)
    return size


def get_position_text(card_type, faction, text_type):
    return card_types_dictionary_positions[card_type][faction][text_type]


def get_resize_command(faction, command_type):
    if command_type in command_dictionary[faction]["Resize"]:
        return command_dictionary[faction]["Resize"][command_type]
    return None


def get_position_command(faction, command_type):
    return command_dictionary[faction][command_type]


def get_position_loyalty(faction, card_type):
    return loyalty_dictionary[card_type][faction]


def get_true_string_for_fonts(text):
    for icon in icons_dict:
        if icon in text:
            text = text.replace(icon, icons_dict[icon]["spacing"])
    for special_text in special_text_dict:
        if special_text in text:
            text = text.replace(special_text, special_text_dict[special_text]["spacing"])
    return text


def get_wrapped_text(text: str, font: ImageFont.ImageFont, line_length: int):
    lines = ['']
    actual_lines = ['']
    for word in text.split():
        before_replace = word.strip()
        replaced_word = get_true_string_for_fonts(before_replace)
        line = f'{lines[-1]} {replaced_word}'
        actual_line = f'{actual_lines[-1]} {word}'.strip()
        if font.getlength(line) <= line_length:
            lines[-1] = line
            actual_lines[-1] = actual_line
        else:
            lines.append(replaced_word)
            actual_lines.append(word)
    return '\n'.join(actual_lines)


def get_length_word(word: str, font: ImageFont.ImageFont):
    return font.getlength(word)


def get_wrapped_text_nlfix(text: str, font: ImageFont.ImageFont, line_length: int):
    return "\n".join([get_wrapped_text(line, font, line_length) for line in text.splitlines()])


def clicked():
    pass


def draw_textbox_text(input_image, text, coords, font_src=text_font, font_size=default_text_size, color=(0, 0, 0),
                      line_length=1080, font_bold=text_bold_font, font_italics=text_italics_font, default_spacing=15):
    text = text.replace("[DARK ELDAR]", "[DARK_ELDAR]")
    text = text.replace("[SPACE MARINES]", "[SPACE_MARINES]")
    text = text.replace("[ASTRA MILITARUM]", "[ASTRA_MILITARUM]")
    text = text.replace("[DEPLOY ACTION]", "[DEPLOY_ACTION]")
    text = text.replace("[COMMAND ACTION]", "[COMMAND_ACTION]")
    text = text.replace("[COMBAT ACTION]", "[COMBAT_ACTION]")
    text = text.replace("[HEADQUARTERS ACTION]", "[HEADQUARTERS_ACTION]")
    text = text.replace("[GOES FASTA]", "[GOES_FASTA]")
    text = text.replace("[HIVE MIND]", "[HIVE_MIND]")
    drawn_image = ImageDraw.Draw(input_image)
    text = text.replace("\n", " \n")
    split_text = text.split(sep=" ")
    current_coords = coords
    og_coords = coords
    font_text = ImageFont.truetype(font_src, font_size)
    word_bold_font = ImageFont.truetype(font_bold, font_size)
    word_italics_font = ImageFont.truetype(font_italics, font_size * 0.8)
    length_of_current_line = 0
    while split_text:
        no_new_lines = split_text[0].replace("\n", "")
        current_font = font_text
        len_word = 0
        spacing = default_spacing
        special_icon = False
        if no_new_lines in special_text_dict:
            if special_text_dict[no_new_lines]["type"] == "Bold":
                current_font = word_bold_font
                no_new_lines = special_text_dict[no_new_lines]["text"]
                try:
                    spacing = int(special_text_dict[no_new_lines]["spacing"])
                except:
                    pass
            elif special_text_dict[no_new_lines]["type"] == "Italics":
                current_font = word_italics_font
                no_new_lines = special_text_dict[no_new_lines]["text"]
                try:
                    spacing = int(special_text_dict[no_new_lines]["spacing"])
                except:
                    pass
        len_word = get_length_word(no_new_lines, current_font)
        if no_new_lines in icons_dict:
            required_size = icons_dict[no_new_lines]["resize"]
            len_word = required_size[0]
        if length_of_current_line + len_word > line_length or "\n" in split_text[0]:
            current_coords = (og_coords[0], current_coords[1] + font_size)
            length_of_current_line = 0
        if no_new_lines in icons_dict:
            special_icon = True
            initial_extra_offset = icons_dict[no_new_lines]["initial_extra_offset"]
            x_pos_icon = int(current_coords[0] + initial_extra_offset[0])
            y_pos_icon = int(current_coords[1] + initial_extra_offset[1])
            required_size = icons_dict[no_new_lines]["resize"]
            text_icon_img = Image.open(icons_dict[no_new_lines]["src"], 'r').convert("RGBA")
            text_icon_img = text_icon_img.resize(required_size)
            input_image.paste(text_icon_img, (x_pos_icon, y_pos_icon), text_icon_img)
            len_word = required_size[0]
        length_of_current_line = length_of_current_line + len_word + spacing
        if not special_icon:
            drawn_image.text(current_coords, no_new_lines, fill=color, font=current_font)
        current_coords = (current_coords[0] + len_word + spacing, current_coords[1])
        del split_text[0]
    return input_image


def add_text_to_image(input_image, text, coords, font_src=text_font,
                      font_size=default_text_size, color=(0, 0, 0), line_length=1080,
                      font_bold=text_bold_font,
                      font_italics=text_italics_font, deepstrike=False):
    text = text.replace("[DARK ELDAR]", "[DARK_ELDAR]")
    text = text.replace("[SPACE MARINES]", "[SPACE_MARINES]")
    text = text.replace("[ASTRA MILITARUM]", "[ASTRA_MILITARUM]")
    text = text.replace("[DEPLOY ACTION]", "[DEPLOY_ACTION]")
    text = text.replace("[COMMAND ACTION]", "[COMMAND_ACTION]")
    text = text.replace("[COMBAT ACTION]", "[COMBAT_ACTION]")
    text = text.replace("[HEADQUARTERS ACTION]", "[HEADQUARTERS_ACTION]")
    text = text.replace("[GOES FASTA]", "[GOES_FASTA]")
    text = text.replace("[HIVE MIND]", "[HIVE_MIND]")
    if deepstrike:
        color = (255, 0, 0)
    drawn_image = ImageDraw.Draw(input_image)
    font_text = ImageFont.truetype(font_src, font_size)
    text = get_wrapped_text_nlfix(text, font_text, line_length)
    og_split_text = text.split(sep="\n")
    for item in special_text_dict:
        for i in range(len(og_split_text)):
            while item in og_split_text[i]:
                current_x_pos_text = og_split_text[i].find(item)
                shortened_text = og_split_text[i][:current_x_pos_text]
                x_offset = int(font_text.getlength(shortened_text))
                x_pos_icon = coords[0] + x_offset + special_text_dict[item]["initial_extra_offset"][0]
                y_pos_icon = coords[1] + special_text_dict[item]["initial_extra_offset"][1] + (font_size) * i
                if special_text_dict[item]["type"] == "Bold":
                    f_bold = ImageFont.truetype(font_bold, font_size)
                    txt_bold = Image.new('RGBA', (line_length, 330))
                    d_bold = ImageDraw.Draw(txt_bold)
                    d_bold.text((0, 0), special_text_dict[item]["text"], font=f_bold, fill="black")
                    input_image.paste(txt_bold, (x_pos_icon, y_pos_icon), txt_bold)
                else:
                    f_italics = ImageFont.truetype(font_italics, font_size * 0.75)
                    txt_italics = Image.new('RGBA', (line_length, 330))
                    d_bold = ImageDraw.Draw(txt_italics)
                    d_bold.text((0, 0), special_text_dict[item]["text"], font=f_italics, fill="black")
                    input_image.paste(txt_italics, (x_pos_icon, y_pos_icon), txt_italics)
    og_split_text = text.split(sep="\n")
    for icon in icons_dict:
        for i in range(len(og_split_text)):
            while icon in og_split_text[i]:
                current_x_pos_text = og_split_text[i].find(icon)
                shortened_text = og_split_text[i][:current_x_pos_text]
                x_offset = int(font_text.getlength(shortened_text))
                initial_extra_offset = icons_dict[icon]["initial_extra_offset"]
                extra_vertical_offset = icons_dict[icon]["extra_vertical_line_offset"]
                x_pos_icon = coords[0] + x_offset + initial_extra_offset[0]
                y_pos_icon = coords[1] + initial_extra_offset[1] + (font_size + extra_vertical_offset) * i
                required_size = icons_dict[icon]["resize"]
                text_icon_img = Image.open(icons_dict[icon]["src"], 'r').convert("RGBA")
                text_icon_img = text_icon_img.resize(required_size)
                input_image.paste(text_icon_img, (x_pos_icon, y_pos_icon), text_icon_img)
    split_text = text.split(sep="\n")
    current_coords = coords
    for i in range(len(split_text)):
        drawn_image.text(current_coords, split_text[i], fill=color, font=font_text)
        current_coords = (current_coords[0], current_coords[1] + (font_size))
    return input_image


def add_text_to_planet_image(input_image, text, font_src=text_font,
                             font_size=84, line_length=1080,
                             font_bold=text_bold_font, font_italics=text_italics_font):
    text = text.replace("[DARK ELDAR]", "[DARK_ELDAR]")
    text = text.replace("[SPACE MARINES]", "[SPACE_MARINES]")
    text = text.replace("[ASTRA MILITARUM]", "[ASTRA_MILITARUM]")
    text = text.replace("[DEPLOY ACTION]", "[DEPLOY_ACTION]")
    text = text.replace("[COMMAND ACTION]", "[COMMAND_ACTION]")
    text = text.replace("[COMBAT ACTION]", "[COMBAT_ACTION]")
    text = text.replace("[HEADQUARTERS ACTION]", "[HEADQUARTERS_ACTION]")
    text = text.replace("[GOES FASTA]", "[GOES_FASTA]")
    text = text.replace("[HIVE MIND]", "[HIVE_MIND]")
    drawn_image = ImageDraw.Draw(input_image)
    text = text.replace("\n", " \n")
    split_text = text.split(sep=" ")
    coords = (30, 400)
    default_spacing = 15
    current_coords = coords
    color = (0, 0, 0)
    og_coords = coords
    font_text = ImageFont.truetype(font_src, font_size)
    word_bold_font = ImageFont.truetype(font_bold, font_size)
    word_italics_font = ImageFont.truetype(font_italics, font_size * 0.8)
    length_of_current_line = 0
    while split_text:
        no_new_lines = split_text[0].replace("\n", "")
        current_font = font_text
        len_word = 0
        spacing = default_spacing
        special_icon = False
        if no_new_lines in special_text_dict:
            if special_text_dict[no_new_lines]["type"] == "Bold":
                current_font = word_bold_font
                no_new_lines = special_text_dict[no_new_lines]["text"]
                try:
                    spacing = int(special_text_dict[no_new_lines]["spacing"])
                except:
                    pass
            elif special_text_dict[no_new_lines]["type"] == "Italics":
                current_font = word_italics_font
                no_new_lines = special_text_dict[no_new_lines]["text"]
                try:
                    spacing = int(special_text_dict[no_new_lines]["spacing"])
                except:
                    pass
        len_word = get_length_word(no_new_lines, current_font)
        if no_new_lines in icons_dict:
            required_size = icons_dict[no_new_lines]["resize"]
            len_word = required_size[0]
        if length_of_current_line + len_word > line_length or "\n" in split_text[0]:
            current_coords = (og_coords[0], current_coords[1] + font_size)
            length_of_current_line = 0
        if no_new_lines in icons_dict:
            special_icon = True
            initial_extra_offset = icons_dict[no_new_lines]["initial_extra_offset"]
            x_pos_icon = int(current_coords[0] + initial_extra_offset[0])
            y_pos_icon = int(current_coords[1] + initial_extra_offset[1])
            required_size = icons_dict[no_new_lines]["resize"]
            text_icon_img = Image.open(icons_dict[no_new_lines]["src"], 'r').convert("RGBA")
            text_icon_img = text_icon_img.resize(required_size)
            input_image.paste(text_icon_img, (x_pos_icon, y_pos_icon), text_icon_img)
            len_word = required_size[0]
        length_of_current_line = length_of_current_line + len_word + spacing
        if not special_icon:
            drawn_image.text(current_coords, no_new_lines, fill=color, font=current_font)
        current_coords = (current_coords[0] + len_word + spacing, current_coords[1])
        del split_text[0]
    return input_image


def add_name_to_card(card_type, name, resulting_img):
    if card_type == "Support":
        f = ImageFont.truetype(name_font, name_size)
        txt = Image.new('RGBA', (900, 100))
        d = ImageDraw.Draw(txt)
        d.text((0, 0), name, font=f, fill="black")
        w = txt.rotate(90, expand=1)
        x_offset = int((0.5 * get_pil_text_size(name, name_size,
                                                name_font)[2]) - 100)
        resulting_img.paste(w, (100, x_offset), w)
    elif card_type == "Planet":
        f = ImageFont.truetype(name_font, name_size)
        txt = Image.new('RGBA', (900, 100))
        d = ImageDraw.Draw(txt)
        d.text((0, 0), name, font=f, fill="black")
        w = txt.rotate(270, expand=1)
        x_offset = int((-1 * get_pil_text_size(name, name_size, name_font)[2]))
        x_offset = x_offset + 1900
        resulting_img.paste(w, (1210, x_offset), w)
    elif card_type == "Attachment":
        x_offset = int(690 - (0.5 * get_pil_text_size(name, name_size, name_font)[2]))
        add_text_to_image(
            resulting_img, name, (x_offset, 1210), font_src=name_font, font_size=name_size
        )
    elif card_type == "Warlord":
        x_offset = int(750 - (0.5 * get_pil_text_size(name, name_size, name_font)[2]))
        add_text_to_image(
            resulting_img, name, (x_offset, 84), font_src=name_font, font_size=name_size
        )
    elif card_type == "Event":
        x_offset = int(810 - (0.5 * get_pil_text_size(name, name_size, name_font)[2]))
        add_text_to_image(
            resulting_img, name, (x_offset, 68), font_src=name_font, font_size=name_size
        )
    else:
        x_offset = int(810 - (0.5 * get_pil_text_size(name, name_size, name_font)[2]))
        add_text_to_image(
            resulting_img, name, (x_offset, 98), font_src=name_font, font_size=name_size
        )
    return resulting_img


def add_traits_to_card(card_type, traits, resulting_img, faction=""):
    x_offset = int(840 - (0.5 * get_pil_text_size(traits, trait_size, trait_font)[2]))
    y_offset = 1360
    if card_type == "Army":
        x_offset = x_offset - 50
        if faction == "Tau":
            y_offset = y_offset + 20
    if card_type == "Support":
        x_offset = x_offset - 100
        y_offset = 1370
    if card_type == "Warlord":
        x_offset = x_offset - 80
        y_offset = 240
    if card_type == "Attachment":
        x_offset = x_offset - 140
        y_offset = 1390
    if card_type == "Event":
        x_offset = x_offset - 100
        y_offset = 1390
    add_text_to_image(
        resulting_img, traits, (x_offset, y_offset), font_src=trait_font,
        font_size=trait_size
    )
    return resulting_img


def add_command_icons(command, first_command_src, extra_command_src, command_end_src,
                      resulting_img, faction, card_type):
    command = int(command)
    if command > 0:
        str_command = str(command)
        default_command_src = "card_srcs/" + faction + "/" + card_type + "/" + str(command) + "_Command.png"
        if get_resize_command(faction, str_command) is not None and os.path.exists(default_command_src):
            first_command_img = Image.open(default_command_src, 'r').convert("RGBA")
            first_command_img = first_command_img.resize(get_resize_command(faction, str_command))
            resulting_img.paste(first_command_img, get_position_command(faction, "First"), first_command_img)
        elif faction != "Tyranids" or (0 < command < 4 and card_type == "Army") \
                or (0 < command < 3 and card_type == "Synapse"):
            current_x_pos_end_command, y_end_command = get_position_command(faction, "End")
            first_command_img = Image.open(first_command_src, 'r').convert("RGBA")
            first_command_img = first_command_img.resize(get_resize_command(faction, "First"))
            resulting_img.paste(first_command_img, get_position_command(faction, "First"), first_command_img)
            extra_command_img = Image.open(extra_command_src, 'r').convert("RGBA")
            extra_command_img = extra_command_img.resize(get_resize_command(faction, "Extra"))
            current_position_command, y_extra_command = get_position_command(faction, "Extra")
            spacing = get_position_command(faction, "Spacing")
            for i in range(command - 1):
                resulting_img.paste(extra_command_img, (current_position_command, y_extra_command), extra_command_img)
                current_position_command += spacing
                current_x_pos_end_command += spacing
            command_end_img = Image.open(command_end_src, 'r').convert("RGBA")
            command_end_img = command_end_img.resize(get_resize_command(faction, "End"))
            resulting_img.paste(command_end_img, (current_x_pos_end_command, y_end_command), command_end_img)


def process_submitted_card(name, card_type, text, faction, traits, output_dir,
                           attack="0", health="0", command="0", cost="0",
                           starting_cards="7", starting_resources="7",
                           loyalty="Common", shield_value="0", bloodied=False, automated=False, auto_card_art_src=""):
    text_src = "card_srcs/" + faction + "/" + card_type + "/Text.png"
    if bloodied and card_type == "Warlord":
        text_src = "card_srcs/" + faction + "/Warlord_Bloodied/Text.png"
    if not os.path.exists(text_src):
        return False
    card_art_src = "current_card_info/src_img/"
    expansion_icon_dirs = "current_card_info/expansion_icon/"
    dirs_expansion = os.listdir(expansion_icon_dirs)
    if not dirs_expansion:
        return False
    random.shuffle(dirs_expansion)
    expansion_icon_src = "current_card_info/expansion_icon/" + dirs_expansion[0]
    first_command_src = "card_srcs/" + faction + "/" + card_type + "/First_Command.png"
    command_end_src = "card_srcs/" + faction + "/" + card_type + "/Command_End.png"
    extra_command_src = "card_srcs/" + faction + "/" + card_type + "/Extra_Command_Icon.png"
    resulting_img = Image.new("RGBA", (1440, 2052))
    if not automated:
        dirs_art = os.listdir(card_art_src)
        if not dirs_art:
            return False
        random.shuffle(dirs_art)
        card_art_img = Image.open(card_art_src + dirs_art[0], 'r').convert("RGBA")
        if card_type == "Warlord":
            card_art_img = card_art_img.resize((1440, 2052))
        else:
            card_art_img = card_art_img.resize((1440, 1500))
        resulting_img.paste(card_art_img, get_position_text(card_type, faction, "Art"))
    else:
        if os.path.exists(auto_card_art_src):
            card_art_img = Image.open(auto_card_art_src, 'r').convert("RGBA")
            if card_type == "Warlord":
                card_art_img = card_art_img.resize((1440, 2052))
            else:
                card_art_img = card_art_img.resize((1440, 1500))
            resulting_img.paste(card_art_img, get_position_text(card_type, faction, "Art"))
    if card_type == "Warlord" and bloodied:
        bloodied_img = Image.open("card_srcs/blood/blood.png", 'r').convert("RGBA")
        bloodied_img = bloodied_img.resize((1440, 2052))
        resulting_img.paste(bloodied_img, get_position_text(card_type, faction, "Art"), bloodied_img)
    text_resize_amount = (1440, 2052)
    required_line_length = 1240
    if card_type != "Planet":
        required_line_length = card_types_dictionary_positions[card_type][faction]["Text Length"]
    text_img = Image.open(text_src, 'r').convert("RGBA")
    text_img = text_img.resize(text_resize_amount)
    resulting_img.paste(text_img, get_position_text(card_type, faction, "Text Box"), text_img)
    expansion_icon_img = Image.open(expansion_icon_src, 'r').convert("RGBA").resize((55, 55))
    resulting_img.paste(expansion_icon_img, get_position_text(card_type, faction, "Expansion Icon"), expansion_icon_img)
    add_name_to_card(card_type, name, resulting_img)
    add_traits_to_card(card_type, traits, resulting_img, faction=faction)
    draw_textbox_text(resulting_img, text, get_position_text(card_type, faction, "Text"),
                      line_length=required_line_length)
    deepstrike = False
    if "Deep Strike (" in text:
        deepstrike = True
    if card_type in ["Army", "Support", "Event", "Attachment"]:
        x_offset = int((0.5 * get_pil_text_size(cost, numbers_size, numbers_font)[2]))
        x_pos, y_pos = get_position_text(card_type, faction, "Cost")
        x_pos = x_pos - x_offset
        add_text_to_image(
            resulting_img, cost, (x_pos, y_pos),
            font_src=numbers_font, font_size=numbers_size, color=(0, 0, 0),
            deepstrike=deepstrike
        )
    if card_type in ["Army", "Warlord", "Synapse"]:
        x_offset = int((0.5 * get_pil_text_size(attack, numbers_size, numbers_font)[2]))
        x_pos, y_pos = get_position_text(card_type, faction, "Attack")
        x_pos = x_pos - x_offset
        add_text_to_image(
            resulting_img, attack, (x_pos, y_pos),
            font_src=numbers_font, font_size=numbers_size, color=(255, 255, 255)
        )
        x_offset = int((0.5 * get_pil_text_size(health, numbers_size, numbers_font)[2]))
        x_pos, y_pos = get_position_text(card_type, faction, "Health")
        x_pos = x_pos - x_offset
        add_text_to_image(
            resulting_img, health, (x_pos, y_pos),
            font_src=numbers_font, font_size=numbers_size, color=(0, 0, 0)
        )
    if card_type in ["Army", "Synapse"] and faction != "Neutral":
        try:
            add_command_icons(command, first_command_src, extra_command_src,
                              command_end_src, resulting_img, faction, card_type)
        except ValueError:
            pass
    if card_type == "Warlord" and not bloodied:
        add_text_to_image(
            resulting_img, starting_cards, get_position_text(card_type, faction, "Cards"),
            font_size=168, color=(0, 0, 0)
        )
        add_text_to_image(
            resulting_img, starting_resources, get_position_text(card_type, faction, "Resources"),
            font_size=168, color=(243, 139, 18)
        )
    if card_type in ["Army", "Support", "Event", "Attachment"]:
        if (loyalty == "Loyal" or loyalty == "Signature") and faction != "Neutral":
            loyalty_src = "card_srcs/" + faction + "/Loyalty/" + loyalty + ".png"
            loyalty_img = Image.open(loyalty_src, 'r').convert("RGBA")
            resize_loyalty = resize_loyalty_dictionary[faction]
            loyalty_img = loyalty_img.resize(resize_loyalty)
            resulting_img.paste(loyalty_img, get_position_loyalty(faction, card_type), loyalty_img)
    if card_type in ["Event", "Attachment"]:
        shield_value = int(shield_value)
        if shield_value > 0:
            shield_src = "card_srcs/" + faction + "/Shield/Shield_Icon.png"
            shield_icon_img = Image.open(shield_src, 'r').convert("RGBA")
            shield_icon_img = shield_icon_img.resize((221, 101))
            starting_position_shield = get_position_text(card_type, faction, "Shield")
            for i in range(shield_value):
                resulting_img.paste(shield_icon_img, starting_position_shield, shield_icon_img)
                starting_position_shield = (starting_position_shield[0], starting_position_shield[1] + 100)
    resulting_img.save(output_dir, "PNG")
    return True


def process_submitted_planet_card(name, card_type, text, cards_value, resources_value, icons_grouped, output_dir):
    resources_src = "card_srcs/Planet/Values/resource_" + resources_value + ".jpg"
    cards_src = "card_srcs/Planet/Values/card_" + cards_value + ".jpg"
    text_src = "card_srcs/" + card_type + "/Text/Text.png"
    if not os.path.exists(text_src):
        return False
    card_art_src = "current_card_info/src_img/"
    expansion_icon_src = "expansion_icon.png"
    resulting_img = Image.new("RGBA", (1440, 2052))
    dirs_art = os.listdir(card_art_src)
    if not dirs_art:
        return False
    random.shuffle(dirs_art)
    card_art_img = Image.open(card_art_src + dirs_art[0], 'r').convert("RGBA")
    card_art_img = card_art_img.resize((1440, 2052))
    resulting_img.paste(card_art_img, get_position_text(card_type, "Planet", "Art"))
    text_resize_amount = (1440, 2052)
    text_img = Image.open(text_src, 'r').convert("RGBA")
    text_img = text_img.resize(text_resize_amount)
    resulting_img.paste(text_img, get_position_text(card_type, "Planet", "Text Box"), text_img)
    if os.path.exists(cards_src):
        cards_value_img = Image.open(cards_src, 'r').convert("RGBA")
        cards_value_img = cards_value_img.resize((256, 176))
        resulting_img.paste(cards_value_img, get_position_text(card_type, "Planet", "Card"), cards_value_img)
    if os.path.exists(resources_src):
        resources_value_img = Image.open(resources_src, 'r').convert("RGBA")
        resources_value_img = resources_value_img.resize((202, 142))
        resulting_img.paste(resources_value_img, get_position_text(card_type, "Planet", "Resource"),
                            resources_value_img)
    expansion_icon_img = Image.open(expansion_icon_src, 'r').convert("RGBA").resize((40, 40))
    resulting_img.paste(expansion_icon_img, get_position_text(card_type, "Planet", "Expansion Icon"),
                        expansion_icon_img)
    add_name_to_card(card_type, name, resulting_img)
    x_offset = int(690 - (0.5 * get_pil_text_size(
        text, 84, "fonts/norwester/norwester.otf"
    )[2]))
    add_text_to_planet_image(
        resulting_img, text
    )
    num_icons = 0
    for c in icons_grouped:
        if c == "R":
            material_src = "card_srcs/Planet/Icons/Material.png"
            material_img = Image.open(material_src, 'r').convert("RGBA").resize((197, 278))
            icon_coords = get_position_text(card_type, "Planet", "First Icon")
            icon_coords = (icon_coords[0],
                           icon_coords[1] + num_icons * get_position_text(card_type, "Planet", "Icon Spacing"))
            resulting_img.paste(material_img, icon_coords, material_img)
            num_icons += 1
        if c == "B":
            technology_src = "card_srcs/Planet/Icons/Technology.png"
            technology_img = Image.open(technology_src, 'r').convert("RGBA").resize((197, 278))
            icon_coords = get_position_text(card_type, "Planet", "First Icon")
            icon_coords = (icon_coords[0],
                           icon_coords[1] + num_icons * get_position_text(card_type, "Planet", "Icon Spacing"))
            resulting_img.paste(technology_img, icon_coords, technology_img)
            num_icons += 1
        if c == "G":
            strongpoint_src = "card_srcs/Planet/Icons/Strongpoint.png"
            strongpoint_img = Image.open(strongpoint_src, 'r').convert("RGBA").resize((197, 278))
            icon_coords = get_position_text(card_type, "Planet", "First Icon")
            icon_coords = (icon_coords[0],
                           icon_coords[1] + num_icons * get_position_text(card_type, "Planet", "Icon Spacing"))
            resulting_img.paste(strongpoint_img, icon_coords, strongpoint_img)
            num_icons += 1
        if c in ["R", "G", "B"] and num_icons > 1:
            connector_src = "card_srcs/Planet/Icons/Icon_Join.jpg"
            connector_img = Image.open(connector_src, 'r').convert("RGBA").resize((74, 45))
            icon_coords = get_position_text(card_type, "Planet", "First Join")
            print(icon_coords)
            icon_coords = (icon_coords[0], icon_coords[1] + (num_icons - 1)
                           * get_position_text(card_type, "Planet", "Join Spacing"))
            print(icon_coords)
            resulting_img.paste(connector_img, icon_coords, connector_img)
    resulting_img.save(output_dir, "PNG")
    return True
