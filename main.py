import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os


card_types = ["Warlord", "Army", "Support", "Event", "Attachment", "Synapse", "Planet"]
factions = ["Space Marines", "Astra Militarum", "Orks", "Chaos", "Dark Eldar",
            "Eldar", "Tau", "Necrons", "Tyranids", "Neutral"]
loyalties = ["Common", "Loyal", "Signature"]
shields = ["0", "1", "2", "3"]
card_types_dictionary_positions = {
    "Army": {
        "Text Box": (0, 0),
        "Art": (0, 0),
        "Text": (264, 1416),
        "Cost": (110, 60),
        "Attack": (95, 1415),
        "Health": (95, 1685),
        "Loyalty": (1313, 950)
    },
    "Support": {
        "Text Box": (0, 0),
        "Art": (0, 0),
        "Text": (64, 1466),
        "Cost": (130, 60),
        "Loyalty": (1313, 950)
    },
    "Attachment": {
        "Text Box": (0, 0),
        "Art": (0, 0),
        "Text": (64, 1466),
        "Cost": (140, 94),
        "Loyalty": (1313, 825),
        "Shield": (0, 350)
    },
    "Event": {
        "Text Box": (0, 0),
        "Art": (0, 0),
        "Text": (64, 1466),
        "Cost": (114, 56),
        "Loyalty": (1313, 950),
        "Shield": (0, 350)
    },
    "Warlord": {
        "Text Box": (0, 0),
        "Art": (0, 0),
        "Text": (164, 400),
        "Attack": (105, 1515),
        "Health": (105, 1785),
        "Cards": (600, 1825),
        "Resources": (780, 1825)
    }
}
# (1440, 2052) card size
command_dictionary = {
    "Space Marines": {
        "First": (0, 1180),
        "Extra": (129, 1190),
        "End": (129, 1184),
        "Spacing": 134,
        "Resize": {
            "First": (200, 169),
            "Extra": (134, 146),
            "End": (190, 159)
        }
    },
    "Astra Militarum": {
        "First": (0, 1181),
        "Extra": (130, 1181),
        "End": (130, 1181),
        "Spacing": 145,
        "Resize": {
            "First": (200, 171),
            "Extra": (145, 171),
            "End": (235, 171)
        }
    },
    "Eldar": {
        "First": (0, 1181),
        "Extra": (126, 1181),
        "End": (126, 1181),
        "Spacing": 133,
        "Resize": {
            "First": (126, 171),
            "Extra": (133, 171),
            "End": (112, 171)
        }
    },
    "Chaos": {
        "First": (0, 1181),
        "Extra": (106, 1180),
        "End": (106, 1180),
        "Spacing": 133,
        "Resize": {
            "First": (166, 171),
            "Extra": (133, 171),
            "End": (144, 171)
        }
    },
    "Dark Eldar": {
        "First": (0, 1181),
        "Extra": (136, 1180),
        "End": (136, 1180),
        "Spacing": 133,
        "Resize": {
            "First": (136, 171),
            "Extra": (133, 171),
            "End": (200, 171)
        }
    },
    "Orks": {
        "First": (0, 1181),
        "Extra": (106, 1180),
        "End": (106, 1180),
        "Spacing": 133,
        "Resize": {
            "First": (166, 171),
            "Extra": (133, 171),
            "End": (144, 171)
        }
    },
    "Tau": {
        "First": (0, 1181),
        "Extra": (106, 1180),
        "End": (106, 1180),
        "Spacing": 133,
        "Resize": {
            "First": (166, 171),
            "Extra": (133, 171),
            "End": (144, 171)
        }
    },
    "Tyranids": {
        "First": (0, 1181),
        "Extra": (106, 1180),
        "End": (106, 1180),
        "Spacing": 133,
        "Resize": {
            "First": (166, 171),
            "Extra": (133, 171),
            "End": (144, 171)
        }
    },
    "Necrons": {
        "First": (0, 1181),
        "Extra": (144, 1180),
        "End": (60, 1180),
        "Spacing": 168,
        "Resize": {
            "First": (144, 171),
            "Extra": (168, 171),
            "End": (221, 171)
        }
    },
    "Neutral": {
        "First": (0, 1181),
        "Extra": (106, 1180),
        "End": (106, 1180),
        "Spacing": 133,
        "Resize": {
            "First": (166, 171),
            "Extra": (133, 171),
            "End": (144, 171)
        }
    }
}


def get_pil_text_size(text, font_size, font_name):
    font = ImageFont.truetype(font_name, font_size)
    size = font.getbbox(text)
    return size


def get_position_text(card_type, text_type):
    return card_types_dictionary_positions[card_type][text_type]


def get_resize_command(faction, command_type):
    return command_dictionary[faction]["Resize"][command_type]


def get_position_command(faction, command_type):
    return command_dictionary[faction][command_type]


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
                      font_size=84, color=(0, 0, 0), line_length=1080):
    drawn_image = ImageDraw.Draw(input_image)
    text_font = ImageFont.truetype(font_src, font_size)
    text = get_wrapped_text_nlfix(text, text_font, line_length)
    drawn_image.text(coords, text, fill=color, font=text_font)
    return input_image


def add_name_to_card(card_type, name, resulting_img):
    if card_type == "Support":
        f = ImageFont.truetype("fonts/billboard-college-cufonfonts/Billboard-College.ttf", 84)
        txt = Image.new('RGBA', (900, 100))
        d = ImageDraw.Draw(txt)
        d.text((0, 0), name, font=f, fill="black")
        w = txt.rotate(90, expand=1)
        x_offset = int((0.5 * get_pil_text_size(name, 84, "fonts/billboard-college-cufonfonts/Billboard-College.ttf")[2]) - 100)
        resulting_img.paste(w, (110, x_offset), w)
    elif card_type == "Attachment":
        x_offset = int(690 - (0.5 * get_pil_text_size(name, 84, "fonts/billboard-college-cufonfonts/Billboard-College.ttf")[2]))
        add_text_to_image(
            resulting_img, name, (x_offset, 1220), font_src="fonts/billboard-college-cufonfonts/Billboard-College.ttf"
        )
    elif card_type == "Warlord":
        x_offset = int(750 - (0.5 * get_pil_text_size(name, 84, "fonts/billboard-college-cufonfonts/Billboard-College.ttf")[2]))
        add_text_to_image(
            resulting_img, name, (x_offset, 94), font_src="fonts/billboard-college-cufonfonts/Billboard-College.ttf"
        )
    elif card_type == "Event":
        x_offset = int(810 - (0.5 * get_pil_text_size(name, 84, "fonts/billboard-college-cufonfonts/Billboard-College.ttf")[2]))
        add_text_to_image(
            resulting_img, name, (x_offset, 78), font_src="fonts/billboard-college-cufonfonts/Billboard-College.ttf"
        )
    else:
        x_offset = int(810 - (0.5 * get_pil_text_size(name, 84, "fonts/billboard-college-cufonfonts/Billboard-College.ttf")[2]))
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


def process_submitted_card():
    global card_image
    global panel
    name = name_area.get("1.0", "end-1c")
    card_type = card_type_label.cget("text")
    faction = faction_label.cget("text")
    text = text_box_area.get("1.0", "end-1c")
    traits = traits_area.get("1.0", "end-1c")
    card_type = card_type.replace("Card Type: ", "")
    faction = faction.replace("Faction: ", "")
    text_src = "card_srcs/" + faction + "/" + card_type + "/Text.png"
    if not os.path.exists(text_src):
        return False
    card_art_src = "current_card_info/src_img/img.png"
    output_dir = "current_card_info/resulting_image.png"
    first_command_src = "card_srcs/" + faction + "/" + card_type + "/First_Command.png"
    command_end_src = "card_srcs/" + faction + "/" + card_type + "/Command_End.png"
    extra_command_src = "card_srcs/" + faction + "/" + card_type + "/Extra_Command_Icon.png"
    resulting_img = Image.new("RGBA", (1440, 2052))
    card_art_img = Image.open(card_art_src, 'r').convert("RGBA")
    if card_type == "Warlord":
        card_art_img = card_art_img.resize((1440, 2052))
    else:
        card_art_img = card_art_img.resize((1440, 1500))
    resulting_img.paste(card_art_img, get_position_text(card_type, "Art"))
    text_resize_amount = (1440, 2052)
    required_line_length = 1240
    if card_type == "Army":
        required_line_length = 1080
    if card_type == "Warlord":
        required_line_length = 720
    text_img = Image.open(text_src, 'r').convert("RGBA")
    text_img = text_img.resize(text_resize_amount)
    resulting_img.paste(text_img, get_position_text(card_type, "Text Box"), text_img)
    add_name_to_card(card_type, name, resulting_img)
    add_traits_to_card(card_type, traits, resulting_img)
    add_text_to_image(resulting_img, text, get_position_text(card_type, "Text"), line_length=required_line_length)
    if card_type in ["Army", "Support", "Event", "Attachment"]:
        cost = cost_area.get("1.0", "end-1c")
        add_text_to_image(
            resulting_img, cost, get_position_text(card_type, "Cost"), font_size=168, color=(0, 0, 0)
        )
    if card_type in ["Army", "Warlord"]:
        attack = attack_area.get("1.0", "end-1c")
        health = health_area.get("1.0", "end-1c")
        add_text_to_image(
            resulting_img, attack, get_position_text(card_type, "Attack"), font_size=168, color=(255, 255, 255)
        )
        add_text_to_image(
            resulting_img, health, get_position_text(card_type, "Health"), font_size=168, color=(0, 0, 0)
        )
    if card_type == "Army" and faction != "Neutral":
        command = command_area.get("1.0", "end-1c")
        try:
            add_command_icons(command, first_command_src, extra_command_src, command_end_src, resulting_img, faction)
        except ValueError:
            pass
    if card_type == "Warlord":
        starting_cards = starting_cards_area.get("1.0", "end-1c")
        starting_resources = starting_resources_area.get("1.0", "end-1c")
        add_text_to_image(
            resulting_img, starting_cards, get_position_text(card_type, "Cards"), font_size=168, color=(0, 0, 0)
        )
        add_text_to_image(
            resulting_img, starting_resources, get_position_text(card_type, "Resources"), font_size=168, color=(243, 139, 18)
        )
    if card_type in ["Army", "Support", "Event", "Attachment"]:
        loyalty = opt_loyalty.get()
        if (loyalty == "Loyal" or loyalty == "Signature") and faction != "Neutral":
            loyalty_src = "card_srcs/" + faction + "/Loyalty/" + loyalty + ".png"
            loyalty_img = Image.open(loyalty_src, 'r').convert("RGBA")
            loyalty_img = loyalty_img.resize((127, 84))
            resulting_img.paste(loyalty_img, get_position_text(card_type, "Loyalty"), loyalty_img)
    if card_type in ["Event", "Attachment"]:
        shield_value = opt_shields.get()
        shield_value = int(shield_value)
        if shield_value > 0:
            shield_src = "card_srcs/" + faction + "/Shield/Shield_Icon.png"
            shield_icon_img = Image.open(shield_src, 'r').convert("RGBA")
            shield_icon_img = shield_icon_img.resize((221, 101))
            starting_position_shield = get_position_text(card_type, "Shield")
            for i in range(shield_value):
                resulting_img.paste(shield_icon_img, starting_position_shield, shield_icon_img)
                starting_position_shield = (starting_position_shield[0], starting_position_shield[1] + 100)
    resulting_img.save(output_dir, "PNG")
    card_image = Image.open(output_dir)
    card_image = card_image.resize((240, 342))
    card_image = ImageTk.PhotoImage(card_image)
    panel = tk.Label(master, image=card_image)
    panel.place(x=800, y=150)


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
        welcome_label.pack()
        name_label.pack()
        name_area.pack()
        card_type_label.config(text=("Card Type: " + card_type))
        faction_label.config(text=("Faction: " + faction))
        card_type_label.pack()
        faction_label.pack()
        if faction != "Planet":
            loyalty_dropdown.pack()
        if card_type not in ["Warlord", "Synapse", "Planet"]:
            cost_label.pack()
            cost_area.pack()
        text_box_label.pack()
        text_box_area.pack()
        if card_type != "Planet":
            traits_label.pack()
            traits_area.pack()
        if card_type in ["Army", "Warlord", "Synapse"]:
            attack_label.pack()
            attack_area.pack()
            health_label.pack()
            health_area.pack()
            if card_type != "Warlord":
                command_label.pack()
                command_area.pack()
            else:
                starting_amounts_label.pack()
                starting_cards_area.pack()
                starting_resources_area.pack()
        if card_type in ["Attachment", "Event"]:
            shield_dropdown.pack()
        submit_card.pack()
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
opt_shields = tk.StringVar(value="0")
shield_dropdown = tk.OptionMenu(master, opt_shields, *shields)
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
submit_card = tk.Button(master, text="Submit Card", command=process_submitted_card, font=("Arial", 12), background="green")


card_image = ImageTk.PhotoImage(Image.open("card_srcs/Space Marines/Army/Text.png").resize((240, 342)))
panel = tk.Label(master, image=card_image)


create_card_init_button.pack(pady=20)
quit_button.pack(pady=20, side=tk.BOTTOM)

tk.mainloop()
