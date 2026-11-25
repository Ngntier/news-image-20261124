#!/usr/bin/env python3
"""THE WORLD IN ONE DAY - Tuesday 24 November 2026.

A dense newspaper front page summing up the world's news of
Tuesday 24 November 2026. Pure standard library only: the image is
drawn pixel by pixel with a hand-built 5x7 bitmap font and written
out as a PNG with zlib (no PIL, no network, fully deterministic).
"""
import os
import struct
import zlib

W, H = 1024, 1024
PAPER = (253, 251, 243)
INK = (18, 18, 18)
RED = (176, 32, 28)
GREY = (96, 96, 90)
RULE = (150, 148, 138)

# 5x7 bitmap font. Each glyph is 7 rows of 5 bits ('1' = ink).
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    "a": ("00000", "00000", "01110", "00001", "01111", "10001", "01111"),
    "b": ("10000", "10000", "11110", "10001", "10001", "10001", "11110"),
    "c": ("00000", "00000", "01110", "10001", "10000", "10001", "01110"),
    "d": ("00001", "00001", "01111", "10001", "10001", "10001", "01111"),
    "e": ("00000", "00000", "01110", "10001", "11111", "10000", "01110"),
    "f": ("00110", "01001", "01000", "11110", "01000", "01000", "01000"),
    "g": ("00000", "01111", "10001", "10001", "01111", "00001", "01110"),
    "h": ("10000", "10000", "11110", "10001", "10001", "10001", "10001"),
    "i": ("00100", "00000", "01100", "00100", "00100", "00100", "01110"),
    "j": ("00010", "00000", "00110", "00010", "00010", "10010", "01100"),
    "k": ("10000", "10000", "10010", "10100", "11000", "10100", "10010"),
    "l": ("01100", "00100", "00100", "00100", "00100", "00100", "01110"),
    "m": ("00000", "00000", "11010", "10101", "10101", "10101", "10101"),
    "n": ("00000", "00000", "11110", "10001", "10001", "10001", "10001"),
    "o": ("00000", "00000", "01110", "10001", "10001", "10001", "01110"),
    "p": ("00000", "00000", "11110", "10001", "11110", "10000", "10000"),
    "q": ("00000", "00000", "01111", "10001", "01111", "00001", "00001"),
    "r": ("00000", "00000", "10110", "11001", "10000", "10000", "10000"),
    "s": ("00000", "00000", "01111", "10000", "01110", "00001", "11110"),
    "t": ("01000", "01000", "11100", "01000", "01000", "01000", "00110"),
    "u": ("00000", "00000", "10001", "10001", "10001", "10011", "01101"),
    "v": ("00000", "00000", "10001", "10001", "10001", "01010", "00100"),
    "w": ("00000", "00000", "10001", "10101", "10101", "10101", "01010"),
    "x": ("00000", "00000", "10001", "01010", "00100", "01010", "10001"),
    "y": ("00000", "00000", "10001", "10001", "01111", "00001", "01110"),
    "z": ("00000", "00000", "11111", "00010", "00100", "01000", "11111"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "+": ("00000", "00100", "00100", "01110", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '"': ("01010", "01010", "01010", "00000", "00000", "00000", "00000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "#": ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    "*": ("00000", "10101", "01110", "10101", "00000", "00000", "00000"),
    "_": ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    ">": ("10000", "01000", "00100", "00010", "00100", "01000", "10000"),
    "<": ("00001", "00010", "00100", "01000", "00100", "00010", "00001"),
}


class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bytes(bg) * (w * h))

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(color)

    def rect(self, x, y, w, h, color):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, color)

    def hline(self, x, y, w, color, thick=1):
        self.rect(x, y, w, thick, color)

    def vline(self, x, y, h, color, thick=1):
        self.rect(x, y, thick, h, color)

    def text(self, x, y, s, scale, color):
        cx = x
        for ch in s:
            g = FONT.get(ch)
            if g is None:
                ch = "?"
                g = FONT["?"]
            for row in range(7):
                bits = g[row]
                for col in range(5):
                    if bits[col] == "1":
                        for dy in range(scale):
                            for dx in range(scale):
                                self.set(cx + col * scale + dx,
                                         y + row * scale + dy, color)
            cx += 6 * scale
        return cx

    def text_w(self, s, scale):
        return len(s) * 6 * scale - scale

    def text_center(self, y, s, scale, color, cx=None):
        if cx is None:
            cx = self.w // 2
        self.text(cx - self.text_w(s, scale) // 2, y, s, scale, color)


def wrap(text, scale, max_w):
    """Greedy word wrap; returns list of lines."""
    words = text.split(" ")
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if len(trial) * 6 * scale - scale <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def png_bytes(cv):
    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    raw = b"".join(
        b"\x00" + bytes(cv.px[y * cv.w * 3:(y + 1) * cv.w * 3])
        for y in range(cv.h))
    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(raw, 9))
            + chunk(b"IEND", b""))

# ---------------------------------------------------------------- stories
# Every story below happened, or was first reported, on
# Tuesday 24 November 2026. Sources are the outlets that reported it.

LEADS = [
    ("CLIMATE", "COP31 COLLAPSES WITHOUT A DEAL",
     "Climate talks in Antalya end in failure after running almost 50 "
     "hours into overtime: more than 90 nations reject a final text "
     "that never says 'fossil fuels'. Grist calls it climate "
     "diplomacy's 'darkest moment'.",
     "Grist / The Daily Edition"),
    ("TECH", "HUANG IS BACK AT NVIDIA",
     "Jensen Huang is reinstated as chief executive less than two "
     "weeks after resigning, after a White House push by President "
     "Trump. Shares jumped about 30% on Monday; the rally faded "
     "on Tuesday.",
     "AP / Dow Jones"),
]

# (kicker, headline, body, source)
COLUMNS = [
    [  # WAR & DIPLOMACY
        ("IRAN WAR",
         "VANCE AND RUBIO MEET QATAR PM AT WHITE HOUSE",
         "The vice president and the secretary of state hold separate "
         "talks with Qatar's prime minister as Iran vows to use all "
         "its tools against the US naval blockade.",
         "AP / Just Security"),
        ("GAZA",
         "ISRAELI STRIKES KILL HAMAS SECURITY CHIEF",
         "Airstrikes kill Naeem Abu Nahel, director of Hamas' internal "
         "security, and six others, including two police officers, "
         "medics and police say.",
         "Reuters"),
        ("UKRAINE",
         "RUSSIAN STRIKE ON ZAPORIZHZHIA KILLS TWO",
         "An overnight attack hits an apartment block, killing two "
         "people and wounding 40, including four children, the "
         "regional governor says.",
         "Kyiv Independent"),
        ("LIBYA",
         "UKRAINE CLAIMS IT SANK A RUSSIAN WARSHIP",
         "Kyiv says seven naval drones sank the corvette Merkury at "
         "the Benghazi naval base, carrying the Black Sea fight into "
         "the Mediterranean.",
         "Middle East Eye"),
        ("NATO",
         "RUTTE WARNS ALLIANCE WILL DEFEND SPACE",
         "The NATO chief says the alliance will answer any threat in "
         "space, after reports that Russia may orbit a nuclear-armed "
         "satellite before the year ends.",
         "Reuters / NDR"),
        ("NATO",
         "ZELENSKY PRESSES CASE TO JOIN NATO",
         "Ukraine's president calls for NATO membership at the "
         "alliance's parliamentary assembly in Berlin, as Russia "
         "tests the Article 5 promise.",
         "Kyiv Independent"),
        ("KOREA",
         "RUSSIAN JETS ENTER KOREA AIR ZONE",
         "Several Russian aircraft fly inside South Korea's air "
         "defence identification zone, over waters between the "
         "Korean peninsula and Japan.",
         "South Korean Joint Chiefs"),
    ],
    [  # BUSINESS & TECH
        ("MARKETS",
         "US STOCKS MIXED AS HUANG RALLY FADES",
         "The Nasdaq and S&P 500 give back some of Monday's rally, "
         "the best day for US stocks since April 2025, as traders "
         "digest the Nvidia drama.",
         "Dow Jones"),
        ("ECONOMY",
         "US CONSUMER CONFIDENCE ROARS BACK",
         "The Conference Board index jumps to 103.3 in November "
         "from 91.9 in October, a much stronger reading than "
         "economists expected.",
         "Dow Jones"),
        ("TRADE",
         "US READIES HIGHER TARIFFS ON CHINA",
         "Higher levies targeting excess industrial capacity "
         "overseas are expected this week, Dow Jones reports.",
         "Dow Jones"),
        ("TRADE",
         "CHINA EASES CURBS ON CRITICAL MATERIALS",
         "Beijing extends its suspension of some export controls "
         "to the US until January, days after the Trump-Xi summit "
         "in Shenzhen.",
         "Dow Jones"),
        ("TECH",
         "STATES SUE SPACEX OVER GROK IMAGES",
         "Oregon and Virginia sue SpaceX, alleging its Grok chatbot "
         "generated child abuse images.",
         "IQMIA"),
        ("AI",
         "SEOUL PAYS TO CATCH AI EXAM CHEATS",
         "South Korea offers rewards of up to $375,000 to catch "
         "students using AI to cheat in the College Scholastic "
         "Ability Test.",
         "Just Security"),
        ("CHIPS",
         "ARM EXTENDS ITS CHIEF TO 2033",
         "Arm extends chief executive Rene Haas' tenure to 2033, "
         "amid speculation over Nvidia's leadership.",
         "IQMIA"),
    ],
    [  # SCIENCE, SPORT & LIFE
        ("SPACE",
         "FALCON 9 LOFTS SECRET SPACE FORCE LOAD",
         "SpaceX launches the classified USSF-266 mission from "
         "Vandenberg, California; the booster lands on a drone "
         "ship in the Pacific.",
         "USA Today Network"),
        ("SPACE",
         "ARIANE 6 LAUNCHES 36 AMAZON SATELLITES",
         "Europe's Ariane 6 puts 36 Amazon Leo broadband satellites "
         "in orbit, after a Vulcan failure lost 40 of them earlier "
         "in November.",
         "Ars Technica"),
        ("MARS",
         "HALF OF NASA'S MARS FLEET GOES DARK",
         "Two of NASA's four Mars missions suspend science after "
         "separate faults: the Perseverance rover and the Odyssey "
         "orbiter.",
         "Ars Technica"),
        ("HEALTH",
         "SPACE MEDICINE PASSES A ROCKET TEST",
         "An Adelaide team shows a coating made from crustacean "
         "shells keeps medicine droplets stable through launch "
         "and seven minutes of weightlessness.",
         "Adelaide University"),
        ("SPORT",
         "REAL MADRID HIT FIVE; ARSENAL HELD",
         "Champions League, matchday 5: Real Madrid 5-1 PSV, "
         "Arsenal 1-1 Dortmund, Man City 2-2 Napoli, Galatasaray "
         "1-0 Aston Villa.",
         "UEFA"),
        ("CULTURE",
         "SUPER BOWL LXI HEADS TO IMAX",
         "ESPN and the NFL will show the Super Bowl in IMAX "
         "cinemas for the first time.",
         "ESPN / NFL"),
        ("BRITAIN",
         "POPE'S PRIVATE DIARY IS PUBLISHED",
         "The late Pope Francis' diary, released today, details a "
         "profound spiritual crisis and visions of the devil.",
         "CWEB"),
    ],
]

# (UTC time, event) for the timeline strip
TIMELINE = [
    ("02:00", "COP31 collapses in Antalya"),
    ("10:17", "Soyuz launches Progress MS-36 to the ISS"),
    ("12:15", "German business sentiment rises again"),
    ("16:08", "SpaceX Falcon 9 lifts off, USSF-266"),
    ("16:50", "NASA: half its Mars fleet offline"),
    ("18:15", "US consumer confidence jumps to 103.3"),
    ("21:45", "Champions League: Madrid 5-1 PSV"),
    ("22:15", "US stocks mixed as Huang rally fades"),
]

# ---------------------------------------------------------------- layout

def draw_story(cv, x, y, w, kicker, headline, body, source):
    """One column story block. Returns the y below it."""
    cv.text(x, y, kicker, 1, RED)
    y += 12
    for line in wrap(headline, 2, w)[:2]:
        cv.text(x, y, line, 2, INK)
        y += 16
    for line in wrap(body, 1, w)[:3]:
        cv.text(x, y, line, 1, INK)
        y += 9
    cv.text(x, y, "Source: " + source, 1, GREY)
    y += 11
    return y


def render():
    cv = Canvas(W, H, PAPER)
    mx = 22                      # side margin
    cw = W - 2 * mx              # content width

    # --- masthead -------------------------------------------------
    cv.text_center(14, "THE WORLD IN ONE DAY", 6, INK)
    cv.hline(mx, 62, cw, INK, 3)
    cv.text_center(70, "TUESDAY 24 NOVEMBER 2026", 4, RED)
    cv.text_center(98,
                   "The day's news from every time zone - all of it "
                   "reported on 24 November 2026", 1, GREY)
    cv.hline(mx, 114, cw, INK, 2)

    # --- lead stories ---------------------------------------------
    y0 = 126
    lw = (cw - 16) // 2
    for i, (kicker, head, body, source) in enumerate(LEADS):
        x = mx + i * (lw + 16)
        cv.rect(x, y0, lw, 118, (255, 255, 255))
        cv.rect(x, y0, lw, 3, RED)
        cv.text(x + 8, y0 + 9, kicker + "  -  TOP STORY", 1, RED)
        yy = y0 + 24
        for line in wrap(head, 3, lw - 16):
            cv.text(x + 8, yy, line, 3, INK)
            yy += 24
        for line in wrap(body, 1, lw - 16)[:3]:
            cv.text(x + 8, yy, line, 1, INK)
            yy += 10
        cv.text(x + 8, yy + 3, "Source: " + source, 1, GREY)

    # --- UTC timeline ---------------------------------------------
    ty = 258
    cv.text(mx, ty, "THE DAY IN UTC", 1, RED)
    cv.hline(mx, ty + 12, cw, RULE, 1)
    tl_y = ty + 20
    # evenly spaced ticks; labels alternate above/below to avoid overlap
    n = len(TIMELINE)
    step = cw / n
    for i, (t, ev) in enumerate(TIMELINE):
        cx = int(mx + step * i + step / 2)
        cv.vline(cx, tl_y, 8, RED, 2)
        cv.text_center(tl_y + 11, t, 1, RED, cx)
        lab = wrap(ev, 1, int(step) - 6)
        ly = tl_y + 23
        for line in lab[:2]:
            cv.text_center(ly, line, 1, INK, cx)
            ly += 9
    cv.hline(mx, ty + 62, cw, INK, 2)

    # --- three columns of stories ---------------------------------
    col_w = (cw - 32) // 3
    top = 336
    for ci, stories in enumerate(COLUMNS):
        x = mx + ci * (col_w + 16)
        if ci:
            cv.vline(x - 9, top, 628, RULE, 1)
        y = top
        for kicker, head, body, source in stories:
            y = draw_story(cv, x, y, col_w, kicker, head, body, source)
            y += 5
            cv.hline(x, y - 4, col_w, RULE, 1)

    # --- footer: date check ----------------------------------------
    fy = 972
    cv.hline(mx, fy, cw, INK, 2)
    cv.text_center(fy + 8,
                   "DATE CHECK: every story on this page happened, or was "
                   "first reported, on Tuesday 24 November 2026.", 1, RED)
    cv.text_center(fy + 22,
                   "Sources: AP, Reuters, Dow Jones, UEFA, NASA, Ars "
                   "Technica, Grist, Just Security, Kyiv Independent, "
                   "Middle East Eye, USA Today.", 1, GREY)
    cv.text_center(fy + 35,
                   "THE WORLD IN ONE DAY  -  24 NOVEMBER 2026", 1, INK)
    return cv


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    data = png_bytes(render())
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)
    print("wrote %s (%d bytes)" % (path, len(data)))


if __name__ == "__main__":
    main()
