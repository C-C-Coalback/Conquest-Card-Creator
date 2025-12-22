import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
from dict_inits.card_types_dict_positions import card_types_dictionary_positions
from dict_inits.command_dict import command_dictionary
from dict_inits.loyalty_dict import loyalty_dictionary, resize_loyalty_dictionary
from dict_inits.icons_dict import icons_dict, special_text_dict
from process_card import process_submitted_card, process_submitted_planet_card
import os
import random


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
    if card_type != "Warlord":
        loyalty = opt_loyalty.get()
    starting_cards = "7"
    starting_resources = "7"
    if card_type == "Warlord":
        starting_cards = starting_cards_area.get("1.0", "end-1c")
        starting_resources = starting_resources_area.get("1.0", "end-1c")
    shield_value = "0"
    if card_type in ["Event", "Attachment"]:
        shield_value = opt_shields.get()
    bloodied = False
    if card_type == "Warlord":
        if opt_bloodied.get() == "Bloodied":
            bloodied = True
    if process_submitted_card(name, card_type, text, faction, traits, output_dir,
                              attack=attack, health=health, command=command, cost=cost,
                              starting_cards=starting_cards, starting_resources=starting_resources,
                              loyalty=loyalty, shield_value=shield_value, bloodied=bloodied):
        card_image = Image.open(output_dir)
        card_image = card_image.resize((240, 342))
        card_image = ImageTk.PhotoImage(card_image)
        panel = tk.Label(master, image=card_image)
        panel.place(x=650, y=150)
        return True
    return False


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
        if card_type == "Warlord":
            bloodied_label.place(x=base_x, y=current_y)
            bloodied_dropdown.place(x=base_x + 75, y=current_y)
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
bloodied_label = tk.Label(master, text="Bloodied: ", font=("Arial", 12))
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
