import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
from dict_inits.card_types_dict_positions import card_types_dictionary_positions
from dict_inits.command_dict import command_dictionary
from dict_inits.loyalty_dict import loyalty_dictionary
from dict_inits.icons_dict import icons_dict, special_text_dict
import os
import random


card_types = ["Warlord", "Army", "Support", "Event", "Attachment", "Synapse", "Planet"]
factions = ["Space Marines", "Astra Militarum", "Orks", "Chaos", "Dark Eldar",
            "Eldar", "Tau", "Necrons", "Tyranids", "Neutral"]
loyalties = ["Common", "Loyal", "Signature"]
shields = ["0", "1", "2", "3"]
# (1440, 2052) card size


def get_pil_text_size(text, font_size, font_name):
    font = ImageFont.truetype(font_name, font_size)
    size = font.getbbox(text)
    return size


def get_position_text(card_type, faction, text_type):
    return card_types_dictionary_positions[card_type][faction][text_type]


def get_resize_command(faction, command_type):
    return command_dictionary[faction]["Resize"][command_type]


def get_position_command(faction, command_type):
    return command_dictionary[faction][command_type]


def get_position_loyalty(faction, card_type):
    return loyalty_dictionary[card_type][faction]


def get_wrapped_text(text: str, font: ImageFont.ImageFont, line_length: int):
    lines = ['']
    for word in text.split():
        line = f'{lines[-1]} {word}'.strip()
        if font.getlength(line) <= line_length:
            lines[-1] = line
        else:
            lines.append(word)
    return '\n'.join(lines)


def get_wrapped_text_nlfix(text: str, font: ImageFont.ImageFont, line_length: int):
    return "\n".join([get_wrapped_text(line, font, line_length) for line in text.splitlines()])


def clicked():
    pass


def add_text_to_image(input_image, text, coords, font_src="fonts/Markazi_Text/MarkaziText-VariableFont_wght.ttf",
                      font_size=84, color=(0, 0, 0), line_length=1080,
                      font_bold="fonts/Markazi_Text/static/MarkaziText-Bold.ttf",
                      font_italics="fonts/open_sans/OpenSans-Italic.ttf"):
    drawn_image = ImageDraw.Draw(input_image)
    text_font = ImageFont.truetype(font_src, font_size)
    text = get_wrapped_text_nlfix(text, text_font, line_length)
    og_split_text = text.split(sep="\n")
    for icon in icons_dict:
        for i in range(len(og_split_text)):
            if icon in og_split_text[i]:
                current_x_pos_text = og_split_text[i].find(icon)
                shortened_text = og_split_text[i][:current_x_pos_text]
                x_offset = int(text_font.getlength(shortened_text))
                initial_extra_offset = icons_dict[icon]["initial_extra_offset"]
                extra_vertical_offset = icons_dict[icon]["extra_vertical_line_offset"]
                x_pos_icon = coords[0] + x_offset + initial_extra_offset[0]
                y_pos_icon = coords[1] + initial_extra_offset[1] + (font_size + extra_vertical_offset) * i
                required_size = icons_dict[icon]["resize"]
                text_icon_img = Image.open(icons_dict[icon]["src"], 'r').convert("RGBA")
                text_icon_img = text_icon_img.resize(required_size)
                input_image.paste(text_icon_img, (x_pos_icon, y_pos_icon), text_icon_img)
        text = text.replace(icon, icons_dict[icon]["spacing"])
    for item in special_text_dict:
        for i in range(len(og_split_text)):
            if item in og_split_text[i]:
                current_x_pos_text = og_split_text[i].find(item)
                shortened_text = og_split_text[i][:current_x_pos_text]
                x_offset = int(text_font.getlength(shortened_text))
                x_pos_icon = coords[0] + x_offset + special_text_dict[item]["initial_extra_offset"][0]
                y_pos_icon = coords[1] + special_text_dict[item]["initial_extra_offset"][1] + (font_size - 8) * i
                f_bold = ImageFont.truetype(font_bold, font_size)
                txt_bold = Image.new('RGBA', (line_length, 330))
                d_bold = ImageDraw.Draw(txt_bold)
                d_bold.text((0, 0), special_text_dict[item]["text"], font=f_bold, fill="black")
                input_image.paste(txt_bold, (x_pos_icon, y_pos_icon), txt_bold)
        text = text.replace(item, special_text_dict[item]["spacing"])
    """
    \iUnstoppable - The first time this round this unit is assigned damage, prevent 1 of that damage and ready this unit.\i[ACTION:] ready this unit.
    """
    split_text = text.split(sep="\n")
    italics_active = False
    current_coords = coords
    f_italics = ImageFont.truetype(font_italics, int(font_size * 0.75))
    for i in range(len(split_text)):
        will_disable = False
        if split_text[i].count("\\i") % 2:
            if italics_active:
                will_disable = True
            italics_active = True
        split_text[i] = split_text[i].replace("\\i", "")
        if italics_active:
            drawn_image.text(current_coords, split_text[i], fill=color, font=f_italics)
        else:
            drawn_image.text(current_coords, split_text[i], fill=color, font=text_font)
        current_coords = (current_coords[0], current_coords[1] + (font_size - 8))
        if will_disable:
            italics_active = False
    return input_image


def add_text_to_planet_image(input_image, text, font_src="fonts/Markazi_Text/MarkaziText-VariableFont_wght.ttf",
                             font_size=84, line_length=1080,
                             font_bold="fonts/Markazi_Text/static/MarkaziText-Bold.ttf"):
    text_font = ImageFont.truetype(font_src, font_size)
    text = get_wrapped_text_nlfix(text, text_font, line_length)
    og_split_text = text.split(sep="\n")
    replacement_icons = ["[SPACE MARINES]", "[ASTRA MILITARUM]", "[ORKS]", "[CHAOS]", "[DARK ELDAR]",
                         "[ELDAR]", "[TAU]", "[TYRANIDS]", "[NECRONS]", "[RESOURCE]",
                         "[TECHNOLOGY]", "[MATERIAL]", "[STRONGPOINT]"]
    coords = (30, 400)
    for icon in replacement_icons:
        for i in range(len(og_split_text)):
            if icon in og_split_text[i]:
                current_x_pos_text = og_split_text[i].find(icon)
                shortened_text = og_split_text[i][:current_x_pos_text]
                x_offset = int(text_font.getlength(shortened_text))
                initial_extra_offset = icons_dict[icon]["initial_extra_offset"]
                extra_vertical_offset = icons_dict[icon]["extra_vertical_line_offset"]
                x_pos_icon = coords[0] + 240 + initial_extra_offset[0] - (font_size + extra_vertical_offset) * i
                y_pos_icon = coords[1] + x_offset + initial_extra_offset[1]
                required_size = icons_dict[icon]["resize"]
                text_icon_img = Image.open(icons_dict[icon]["src"], 'r').convert("RGBA")
                text_icon_img = text_icon_img.resize(required_size)
                text_icon_img = text_icon_img.rotate(270)
                input_image.paste(text_icon_img, (x_pos_icon, y_pos_icon), text_icon_img)
                "A Non-[TAU] Unit."
        text = text.replace(icon, icons_dict[icon]["spacing"])
    for item in special_text_dict:
        for i in range(len(og_split_text)):
            if item in og_split_text[i]:
                current_x_pos_text = og_split_text[i].find(item)
                shortened_text = og_split_text[i][:current_x_pos_text]
                x_offset = int(text_font.getlength(shortened_text))
                x_offset = x_offset + special_text_dict[item]["initial_extra_offset"][0] + 400
                y_offset = special_text_dict[item]["initial_extra_offset"][1] - (font_size + 0) * i + 30
                f_bold = ImageFont.truetype(font_bold, font_size)
                txt_bold = Image.new('RGBA', (line_length, 330))
                d_bold = ImageDraw.Draw(txt_bold)
                d_bold.text((0, 0), special_text_dict[item]["text"], font=f_bold, fill="black")
                w_bold = txt_bold.rotate(270, expand=1)
                input_image.paste(w_bold, (y_offset, x_offset), w_bold)
        text = text.replace(item, special_text_dict[item]["spacing"])
    f = ImageFont.truetype(font_src, font_size)
    txt = Image.new('RGBA', (line_length, 330))
    d = ImageDraw.Draw(txt)
    d.text((0, 0), text, font=f, fill="black")
    w = txt.rotate(270, expand=1)
    x_offset = 400
    input_image.paste(w, (30, x_offset), w)
    return input_image


def add_name_to_card(card_type, name, resulting_img):
    if card_type == "Support":
        f = ImageFont.truetype("fonts/billboard-college-cufonfonts/Billboard-College.ttf", 84)
        txt = Image.new('RGBA', (900, 100))
        d = ImageDraw.Draw(txt)
        d.text((0, 0), name, font=f, fill="black")
        w = txt.rotate(90, expand=1)
        x_offset = int((0.5 * get_pil_text_size(name, 84,
                                                "fonts/billboard-college-cufonfonts/Billboard-College.ttf")[2]) - 100)
        resulting_img.paste(w, (110, x_offset), w)
    elif card_type == "Planet":
        f = ImageFont.truetype("fonts/billboard-college-cufonfonts/Billboard-College.ttf", 84)
        txt = Image.new('RGBA', (900, 100))
        d = ImageDraw.Draw(txt)
        d.text((0, 0), name, font=f, fill="black")
        w = txt.rotate(270, expand=1)
        x_offset = int((-1 * get_pil_text_size(name, 84, "fonts/billboard-college-cufonfonts/Billboard-College.ttf")[2]))
        x_offset = x_offset + 1900
        resulting_img.paste(w, (1210, x_offset), w)
    elif card_type == "Attachment":
        x_offset = int(690 - (0.5 * get_pil_text_size(name, 84,
                                                      "fonts/billboard-college-cufonfonts/Billboard-College.ttf")[2]))
        add_text_to_image(
            resulting_img, name, (x_offset, 1220), font_src="fonts/billboard-college-cufonfonts/Billboard-College.ttf"
        )
    elif card_type == "Warlord":
        x_offset = int(750 - (0.5 * get_pil_text_size(name, 84,
                                                      "fonts/billboard-college-cufonfonts/Billboard-College.ttf")[2]))
        add_text_to_image(
            resulting_img, name, (x_offset, 94), font_src="fonts/billboard-college-cufonfonts/Billboard-College.ttf"
        )
    elif card_type == "Event":
        x_offset = int(810 - (0.5 * get_pil_text_size(name, 84,
                                                      "fonts/billboard-college-cufonfonts/Billboard-College.ttf")[2]))
        add_text_to_image(
            resulting_img, name, (x_offset, 78), font_src="fonts/billboard-college-cufonfonts/Billboard-College.ttf"
        )
    else:
        x_offset = int(810 - (0.5 * get_pil_text_size(name, 84,
                                                      "fonts/billboard-college-cufonfonts/Billboard-College.ttf")[2]))
        add_text_to_image(
            resulting_img, name, (x_offset, 108), font_src="fonts/billboard-college-cufonfonts/Billboard-College.ttf"
        )
    return resulting_img


def add_traits_to_card(card_type, traits, resulting_img):
    x_offset = int(840 - (0.5 * get_pil_text_size(traits, 84, "fonts/Markazi_Text/static/MarkaziText-Bold.ttf")[2]))
    y_offset = 1320
    if card_type == "Army":
        x_offset = x_offset - 50
    if card_type == "Support":
        x_offset = x_offset - 100
        y_offset = 1370
    if card_type == "Warlord":
        x_offset = x_offset - 80
        y_offset = 230
    if card_type == "Attachment":
        x_offset = x_offset - 140
        y_offset = 1370
    if card_type == "Event":
        x_offset = x_offset - 100
        y_offset = 1390
    add_text_to_image(
        resulting_img, traits, (x_offset, y_offset), font_src="fonts/Markazi_Text/static/MarkaziText-Bold.ttf"
    )
    return resulting_img


def add_command_icons(command, first_command_src, extra_command_src, command_end_src, resulting_img, faction):
    command = int(command)
    if command > 0:
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


def get_parameters_then_process():
    global card_image
    global panel
    name = name_area.get("1.0", "end-1c")
    card_type = card_type_label.cget("text")
    card_type = card_type.replace("Card Type: ", "")
    text = text_box_area.get("1.0", "end-1c")
    output_dir = "current_card_info/resulting_image.png"
    if card_type == "Planet":
        cards_value = planet_cards_area.get("1.0", "end-1c")
        resources_value = planet_resources_area.get("1.0", "end-1c")
        icons_grouped = planet_icons_area.get("1.0", "end-1c")
        if process_submitted_planet_card(name, card_type, text, cards_value, resources_value, icons_grouped,
                                         output_dir):
            card_image = Image.open(output_dir)
            card_image = card_image.resize((240, 342))
            card_image = ImageTk.PhotoImage(card_image)
            panel = tk.Label(master, image=card_image)
            panel.place(x=650, y=150)
            return True
        return False
    faction = faction_label.cget("text")
    traits = traits_area.get("1.0", "end-1c")
    faction = faction.replace("Faction: ", "")
    cost = "0"
    if card_type in ["Army", "Support", "Event", "Attachment"]:
        cost = cost_area.get("1.0", "end-1c")
    attack = "0"
    health = "0"
    if card_type in ["Army", "Warlord", "Synapse"]:
        attack = attack_area.get("1.0", "end-1c")
        health = health_area.get("1.0", "end-1c")
    command = "0"
    if card_type in ["Army", "Synapse"] and faction != "Neutral":
        command = command_area.get("1.0", "end-1c")
    loyalty = "Common"
    if card_type == "Warlord":
        loyalty = opt_loyalty.get()
    starting_cards = "7"
    starting_resources = "7"
    if card_type == "Warlord":
        starting_cards = starting_cards_area.get("1.0", "end-1c")
        starting_resources = starting_resources_area.get("1.0", "end-1c")
    shield_value = "0"
    if card_type in ["Event", "Attachment"]:
        shield_value = opt_shields.get()
    if process_submitted_card(name, card_type, text, faction, traits, output_dir,
                              attack=attack, health=health, command=command, cost=cost,
                              starting_cards=starting_cards, starting_resources=starting_resources,
                              loyalty=loyalty, shield_value=shield_value):
        card_image = Image.open(output_dir)
        card_image = card_image.resize((240, 342))
        card_image = ImageTk.PhotoImage(card_image)
        panel = tk.Label(master, image=card_image)
        panel.place(x=650, y=150)
        return True
    return False


def process_submitted_planet_card(name, card_type, text, cards_value, resources_value, icons_grouped, output_dir):
    resources_src = "card_srcs/Planet/Values/resource_" + resources_value + ".jpg"
    cards_src = "card_srcs/Planet/Values/card_" + cards_value + ".jpg"
    text_src = "card_srcs/" + card_type + "/Text/Text.png"
    if not os.path.exists(text_src):
        return False
    card_art_src = "current_card_info/src_img/img.png"
    expansion_icon_src = "current_card_info/expansion_icon/expansion_icon.png"
    resulting_img = Image.new("RGBA", (1440, 2052))
    card_art_img = Image.open(card_art_src, 'r').convert("RGBA")
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
        text, 84, "fonts/billboard-college-cufonfonts/Billboard-College.ttf"
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


def process_submitted_card(name, card_type, text, faction, traits, output_dir,
                           attack="0", health="0", command="0", cost="0",
                           starting_cards="7", starting_resources="7",
                           loyalty="Common", shield_value="0"):
    global card_image
    global panel
    text_src = "card_srcs/" + faction + "/" + card_type + "/Text.png"
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
    text_resize_amount = (1440, 2052)
    required_line_length = 1240
    if card_type == "Army":
        required_line_length = 1080
    if card_type == "Warlord":
        required_line_length = 720
    text_img = Image.open(text_src, 'r').convert("RGBA")
    text_img = text_img.resize(text_resize_amount)
    resulting_img.paste(text_img, get_position_text(card_type, faction, "Text Box"), text_img)
    expansion_icon_img = Image.open(expansion_icon_src, 'r').convert("RGBA").resize((55, 55))
    resulting_img.paste(expansion_icon_img, get_position_text(card_type, faction, "Expansion Icon"), expansion_icon_img)
    add_name_to_card(card_type, name, resulting_img)
    add_traits_to_card(card_type, traits, resulting_img)
    add_text_to_image(resulting_img, text, get_position_text(card_type, faction, "Text"),
                      line_length=required_line_length)
    if card_type in ["Army", "Support", "Event", "Attachment"]:
        add_text_to_image(
            resulting_img, cost, get_position_text(card_type, faction, "Cost"), font_size=168, color=(0, 0, 0)
        )
    if card_type in ["Army", "Warlord", "Synapse"]:
        add_text_to_image(
            resulting_img, attack, get_position_text(card_type, faction, "Attack"), font_size=168, color=(255, 255, 255)
        )
        add_text_to_image(
            resulting_img, health, get_position_text(card_type, faction, "Health"), font_size=168, color=(0, 0, 0)
        )
    if card_type in ["Army"] and faction != "Neutral":
        try:
            add_command_icons(command, first_command_src, extra_command_src, command_end_src, resulting_img, faction)
        except ValueError:
            pass
    if card_type == "Warlord":
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
            resize_loyalty = (127, 84)
            if faction == "Tau":
                resize_loyalty = (147, 184)
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


def process_submitted_type_and_faction():
    card_type = opt_card_type.get()
    faction = opt_faction.get()
    if card_type == "Synapse":
        faction = "Tyranids"
    elif card_type == "Planet":
        faction = "Neutral"
    if card_type == "Warlord" and faction == "Neutral":
        feedback_submit.config(text="Warlords can not be neutral")
    else:
        welcome_label.pack_forget()
        welcome_label.config(text="Select card attributes")
        current_y = 0
        increment_y = 30
        base_x = 200
        welcome_label.place(x=450, y=current_y)
        current_y += increment_y
        name_label.place(x=base_x, y=current_y)
        current_y += increment_y
        name_area.place(x=base_x, y=current_y)
        current_y += increment_y
        card_type_label.config(text=("Card Type: " + card_type))
        card_type_label.place(x=base_x, y=current_y)
        current_y += increment_y
        if card_type != "Planet":
            faction_label.config(text=("Faction: " + faction))
            faction_label.place(x=base_x, y=current_y)
            current_y += increment_y
        if card_type != "Planet" and card_type != "Warlord":
            loyalty_label.place(x=base_x, y=current_y)
            loyalty_dropdown.place(x=base_x + 80, y=current_y)
            current_y += increment_y
        if card_type not in ["Warlord", "Synapse", "Planet"]:
            cost_label.place(x=base_x, y=current_y)
            cost_area.place(x=base_x + 50, y=current_y)
            current_y += increment_y
        text_box_label.place(x=base_x, y=current_y)
        current_y += increment_y
        text_box_area.place(x=base_x, y=current_y)
        current_y += increment_y + 150
        if card_type != "Planet":
            traits_label.place(x=base_x, y=current_y)
            current_y += increment_y
            traits_area.place(x=base_x, y=current_y)
            current_y += increment_y
        else:
            planet_resources_label.place(x=base_x, y=current_y)
            planet_resources_area.place(x=base_x + 82, y=current_y)
            current_y += increment_y
            planet_cards_label.place(x=base_x, y=current_y)
            planet_cards_area.place(x=base_x + 82, y=current_y)
            current_y += increment_y
            planet_icons_label.place(x=base_x, y=current_y)
            planet_icons_area.place(x=base_x + 82, y=current_y)
            current_y += increment_y
        if card_type in ["Army", "Warlord", "Synapse"]:
            attack_label.place(x=base_x, y=current_y)
            attack_area.place(x=base_x + 60, y=current_y)
            current_y += increment_y
            health_label.place(x=base_x, y=current_y)
            health_area.place(x=base_x + 60, y=current_y)
            current_y += increment_y
            if card_type != "Warlord":
                command_label.place(x=base_x, y=current_y)
                command_area.place(x=base_x + 90, y=current_y)
                current_y += increment_y
            else:
                starting_amounts_label.place(x=base_x, y=current_y)
                starting_cards_area.place(x=base_x + 270, y=current_y)
                starting_resources_area.place(x=base_x + 290, y=current_y)
                current_y += increment_y
        if card_type in ["Attachment", "Event"]:
            shield_label.place(x=base_x, y=current_y)
            shield_dropdown.place(x=base_x + 60, y=current_y)
            current_y += increment_y
        submit_card.place(x=base_x, y=current_y)
        current_y += increment_y
        card_types_dropdown.pack_forget()
        factions_dropdown.pack_forget()
        submit_type_faction_button.pack_forget()
        feedback_submit.pack_forget()


def create_card_init():
    create_card_init_button.pack_forget()
    welcome_label.pack_forget()
    welcome_label.config(text="Select card type and faction")
    welcome_label.pack()
    card_types_dropdown.pack()
    factions_dropdown.pack()
    submit_type_faction_button.pack()
    feedback_submit.pack()


def quit_program():
    master.destroy()


master = tk.Tk()


master.geometry('1080x800')

master.title("Conquest Card Builder")

opt_card_type = tk.StringVar(value="Warlord")

card_types_dropdown = tk.OptionMenu(master, opt_card_type, *card_types)

opt_faction = tk.StringVar(value="Space Marines")

factions_dropdown = tk.OptionMenu(master, opt_faction, *factions)

submit_type_faction_button = tk.Button(master, text="Confirm choices", command=process_submitted_type_and_faction)

feedback_submit = tk.Label(master, text="Feedback will appear here.")

welcome_label = tk.Label(master, text="Welcome", font=("Arial", 18))
welcome_label.pack(pady=20)

create_card_init_button = tk.Button(master, text="Create Card", command=create_card_init, font=("Arial", 12))
quit_button = tk.Button(master, text="Quit Program", command=quit_program, font=("Arial", 12), background="red")

card_type_label = tk.Label(master, text="Card Type: ", font=("Arial", 12))
faction_label = tk.Label(master, text="Faction: ", font=("Arial", 12))
opt_loyalty = tk.StringVar(value="Common")
loyalty_dropdown = tk.OptionMenu(master, opt_loyalty, *loyalties)
loyalty_label = tk.Label(master, text="Loyalty: ", font=("Arial", 12))
opt_shields = tk.StringVar(value="0")
shield_dropdown = tk.OptionMenu(master, opt_shields, *shields)
shield_label = tk.Label(master, text="Shields: ", font=("Arial", 12))
opt_bloodied = tk.StringVar(value="Hale")
bloodied_dropdown = tk.OptionMenu(master, opt_bloodied, *["Hale", "Bloodied"])
name_label = tk.Label(master, text="Name:", font=("Arial", 12))
name_area = tk.Text(master, height=1, width=52)
cost_label = tk.Label(master, text="Cost:", font=("Arial", 12))
cost_area = tk.Text(master, height=1, width=2)
text_box_label = tk.Label(master, text="Text:", font=("Arial", 12))
text_box_area = tk.Text(master, height=10, width=52)
traits_label = tk.Label(master, text="Traits:", font=("Arial", 12))
traits_area = tk.Text(master, height=1, width=52)
attack_label = tk.Label(master, text="Attack:", font=("Arial", 12))
attack_area = tk.Text(master, height=1, width=2)
health_label = tk.Label(master, text="Health:", font=("Arial", 12))
health_area = tk.Text(master, height=1, width=2)
command_label = tk.Label(master, text="Command:", font=("Arial", 12))
command_area = tk.Text(master, height=1, width=2)
starting_amounts_label = tk.Label(master, text="Starting amounts (Cards/Resources):", font=("Arial", 12))
starting_cards_area = tk.Text(master, height=1, width=2)
starting_resources_area = tk.Text(master, height=1, width=2)
submit_card = tk.Button(master, text="Submit Card", command=get_parameters_then_process, font=("Arial", 12),
                        background="green")

planet_resources_label = tk.Label(master, text="Resources:", font=("Arial", 12))
planet_resources_area = tk.Text(master, height=1, width=2)
planet_cards_label = tk.Label(master, text="Cards:", font=("Arial", 12))
planet_cards_area = tk.Text(master, height=1, width=2)
planet_icons_label = tk.Label(master, text="Icons:", font=("Arial", 12))
planet_icons_area = tk.Text(master, height=1, width=4)


card_image = ImageTk.PhotoImage(Image.open("card_srcs/Space Marines/Army/Text.png").resize((240, 342)))
panel = tk.Label(master, image=card_image)


create_card_init_button.pack(pady=20)
quit_button.pack(pady=20, side=tk.BOTTOM)

tk.mainloop()
