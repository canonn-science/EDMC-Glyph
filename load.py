import sys
import tkinter as tk
from ttkHyperlinkLabel import HyperlinkLabel
import webbrowser
import requests
import json
from l10n import Locale
from theme import theme
import itertools
import plug

import logging
import os

from config import appname

this = sys.modules[__name__]

# This could also be returned from plugin_start3()
plugin_name = os.path.basename(os.path.dirname(__file__))

# A Logger is used per 'found' plugin to make it easy to include the plugin's
# folder name in the logging output format.
# NB: plugin_name here *must* be the plugin's folder name as per the preceding
#     code, else the logger won't be properly set up.
logger = logging.getLogger(f'{appname}.{plugin_name}')

# If the Logger has handlers then it was already set up by the core code, else
# it needs setting up here.
if not logger.hasHandlers():
    level = logging.INFO  # So logger.info(...) is equivalent to print()

    logger.setLevel(level)
    logger_channel = logging.StreamHandler()
    logger_formatter = logging.Formatter(
        f'%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d:%(funcName)s: %(message)s')
    logger_formatter.default_time_format = '%Y-%m-%d %H:%M:%S'
    logger_formatter.default_msec_format = '%s.%03d'
    logger_channel.setFormatter(logger_formatter)
    logger.addHandler(logger_channel)


def plugin_start3(plugin_dir):
    plugin_start(plugin_dir)


def plugin_start(plugin_dir):
    """
    Load this plugin into EDMC
    """
    this.plugin_dir = plugin_dir
    logger.info("I am loaded! My plugin folder is {}".format(plugin_dir))
    return "Test"


def plugin_app(parent):
    """
    Create a pair of TK widgets for the EDMC main window
    """
    this.frame = tk.Frame(parent)
    # By default widgets inherit the current theme's colors

    this.title = tk.Label(this.frame, text="Glyph:")
    this.status = tk.Label(
        this.frame,
        text="Waiting for scan",
        foreground="green"
    )

    this.title.grid(row=0, column=0, sticky="NSEW")
    this.status.grid(row=0, column=1, sticky="NSEW")
    this.title.grid_remove()
    this.status.grid_remove()

    this.glyph = tk.Label(this.frame, text="Glyph:")
    this.ship = tk.Label(this.frame, text="Ship:")

    this.ship_label = tk.Label(this.frame, text="Ship:")
    # Override theme's foreground color
    #this.glyph_id = tk.Label(this.frame, text="Ready", foreground="green")
    this.glyph_id = tk.Label(this.frame, text="Ready")
    this.systemName = "systemName"
    this.system = tk.Label(this.frame, text="SystemName")
    this.submit = tk.Button(this.frame, text="Submit", foreground="green")
    this.dismiss = tk.Button(this.frame, text="Dismiss", foreground="red")

    this.frame.columnconfigure(3, weight=1)

    this.system.grid(row=2, columnspan=2, column=0, sticky="NSEW")

    this.glyph.grid(row=0, column=0, sticky="NSEW")
    this.ship.grid(row=0, column=1, sticky="NSEW")

    this.glyph_id.grid(row=1, column=0, sticky="NSEW")
    this.ship_label.grid(row=1, column=1, sticky="NSEW")

    this.submit.grid(row=3, column=0, sticky="NSEW")
    this.dismiss.grid(row=3, column=1, sticky="NSEW")

    this.glyph.bind('<Button-1>', leftclick)
    this.ship.bind('<Button-1>', shipclick)
    this.glyph.bind('<Button-3>', rightclick)
    this.ship.bind('<Button-3>', shipclick)
    this.ship_label.bind('<Button-1>', toggle_hostility)
    this.dismiss.bind('<Button-1>', hide)
    this.submit.bind('<Button-1>', glyph_submit)
    #this.title.bind('<Button-1>', test_show)

    # one through 11 inclusive
    # should replace this by parsing the images
    this.inners = itertools.cycle(list(range(1, 12)))
    this.outers = itertools.cycle([
        "1A", "1B", "1C", "1D",
        "2A", "2B", "2C", "2D", "2E",
        "3A", "3B",
        "4A", "4B", "4C", "4D", "4E", "4F",
        "5A",
        "7A"
    ])
    this.interceptors = itertools.cycle([
        "Cyclops",
        "Basilisk",
        "Medusa",
        "Hydra",
        "Orthrus"
    ])
    this.interceptor = next(this.interceptors)
    this.inner_value = next(this.inners)
    this.outer_value = next(this.outers)

    this.hostile = False

    display()
    hide()
    return this.frame


def toggle_hostility(event=None):
    if this.hostile:
        this.hostile = False
    else:
        this.hostile = True
    display()


def glyph_submit(event):
    this.ship_label["fg"] = "green"
    hostility = "Friendly"
    if this.hostile:
        hostility = "Hostile"
        this.ship_label["fg"] = "red"

    url = "https://docs.google.com/forms/d/e/1FAIpQLSfv6uhfJtGuS9IizUaNO3VnX-t_AZX1DDnsRDT4Cxrj29n7Fw/formResponse?usp=pp_url"
    params = f"&entry.1933517733={this.cmdr}&entry.896344291={this.systemName}&entry.1250600565={this.interceptor}&entry.302977208={this.id64}&entry.1507205151={this.x}&entry.554889217={this.y}&entry.743397442={this.z}&entry.245136015={this.glyph_identity}&&entry.1226132342={hostility}"

    r = requests.get(url+params)

    hide(event)


def hide(event=None):
    this.glyph.grid_remove()
    this.ship.grid_remove()
    this.glyph_id.grid_remove()
    this.ship_label.grid_remove()
    this.submit.grid_remove()
    this.system.grid_remove()
    this.dismiss.grid_remove()
    # show the status
    this.title.grid()
    this.status.grid()


def test_show(event=None):
    edsm = get_edsm("Merope")
    this.x, this.y, this.z = edsm.get("coords").values()
    this.id64 = edsm.get("id64")
    show("systemName")


def show(system):
    this.system["text"] = system
    this.glyph.grid()
    this.ship.grid()
    this.glyph_id.grid()
    this.ship_label.grid()
    this.submit.grid()
    this.system.grid()
    this.dismiss.grid()
    # show the status
    this.title.grid_remove()
    this.status.grid_remove()


def display():

    this.glyph_identity = f"{this.outer_value}-{this.inner_value}"
    gif = f"{this.glyph_identity}.gif"
    this.glyph_image = tk.PhotoImage(
        file=os.path.join(this.plugin_dir, "images", gif))

    this.ship_label["fg"] = "green"
    if this.hostile:
        this.ship_label["fg"] = "red"

    this.ship_image = tk.PhotoImage(file=os.path.join(
        this.plugin_dir, "images", f"{this.interceptor}.gif"))
    this.glyph["image"] = this.glyph_image
    this.ship["image"] = this.ship_image

    this.glyph_id["text"] = this.glyph_identity
    this.ship_label["text"] = this.interceptor
    this.system["text"] = this.systemName


def set_ship(type):
    while this.interceptor != type:
        this.interceptor = next(this.interceptors)


def leftclick(event):

    this.inner_value = next(this.inners)
    if this.inner_value in [1, 2, 3]:
        set_ship("Cyclops")
    if this.inner_value in [4, 5, 6]:
        set_ship("Medusa")
    if this.inner_value in [7, 8, 9]:
        set_ship("Basilisk")
    if this.inner_value in [10]:
        set_ship("Basilisk")
    if this.inner_value in [11]:
        set_ship("Orthrus")
    display()


def rightclick(event):
    this.outer_value = next(this.outers)
    display()


def shipclick(event):
    this.interceptor = next(this.interceptors)
    display()

# this should really be done with a thread


def get_edsm(system):
    url = f"https://www.edsm.net/api-v1/system?systemName={system}&showCoordinates=1&showId=1"
    r = requests.get(url)
    return r.json()


def journal_entry(cmdr, is_beta, system, station, entry, state):
    # this is what happens when you scan a goid
    tgnames = {
        "$Codex_Ent_Basilisk_Name;": "Basilisk",
        "$Codex_Ent_Orthrus_Name;": "Orthrus",
        "$Codex_Ent_Cyclops_Name;": "Cyclops",
        "$Codex_Ent_Hydra_Name;": "Hydra",
        "$Codex_Ent_Medusa_Name;": "Medusa"
    }

    if entry.get("event") == "Music":
        if entry.get("MusicTrack") in ("Combat_Unknown"):
            this.hostile = True
        else:
            this.hostile = False

    tgscanned = (entry.get("event") == "MaterialCollected" and entry.get(
        "Name") in ("tg_shipflightdata", "unknownshipsignature"))
    tgtest = (entry.get("event") == "SendText" and entry.get(
        "Message") and entry.get("Message") == "test glyph scanner")
    tgcomp = (entry.get("event") ==
              "CodexEntry" and tgnames.get(entry.get("Name")))

    if tgscanned or tgtest or tgcomp:
        this.cmdr = cmdr
        this.systemName = system
        if tgcomp:
            set_ship(tgnames.get(entry.get("Name")))

        edsm = get_edsm(system)
        this.x, this.y, this.z = edsm.get("coords").values()
        this.id64 = edsm.get("id64")
        show(system)
