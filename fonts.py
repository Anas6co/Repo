"""100 Unicode text styles. Each style is (name, function(str) -> str)."""
import string

UP, LO, DG = string.ascii_uppercase, string.ascii_lowercase, string.digits


def _table(upper=None, lower=None, digits=None, extra=None):
    t = {}
    if upper:
        t.update(zip(UP, upper))
    if lower:
        t.update(zip(LO, lower))
    if digits:
        t.update(zip(DG, digits))
    for k, v in (extra or {}).items():
        t[k] = v
    for seq in (upper, lower):
        assert seq is None or len(seq) == 26, seq
    assert digits is None or len(digits) == 10, digits
    return str.maketrans(t)


def _block(up, lo=None, dg=None, exc=None):
    upper = [chr(up + i) for i in range(26)]
    lower = [chr(lo + i) for i in range(26)] if lo is not None else upper
    digits = [chr(dg + i) for i in range(10)] if dg is not None else None
    return _table(upper, lower, digits, exc)


def _tr(table, pre=None):
    def f(s):
        return (pre(s) if pre else s).translate(table)
    return f


def _combine(mark):
    return lambda s: "".join(c if c.isspace() else c + mark for c in s)


def _wrap(template, base):
    return lambda s: template.format(base(s))


def _sep(sep, base):
    return lambda s: " ".join(sep.join(w) for w in base(s).split())


def _both(base, deco):
    return lambda s: deco(base(s))


# ---- Math alphanumeric blocks (the classic "fancy fonts") ----
_SCRIPT_EXC = {"B": "ℬ", "E": "ℰ", "F": "ℱ", "H": "ℋ", "I": "ℐ",
               "L": "ℒ", "M": "ℳ", "R": "ℛ", "e": "ℯ", "g": "ℊ", "o": "ℴ"}
_FRAK_EXC = {"C": "ℭ", "H": "ℌ", "I": "ℑ", "R": "ℜ", "Z": "ℨ"}
_DS_EXC = {"C": "ℂ", "H": "ℍ", "N": "ℕ", "P": "ℙ", "Q": "ℚ",
           "R": "ℝ", "Z": "ℤ"}

_FIX = lambda t, e: {**t, **{ord(k): v for k, v in e.items()}}  # noqa: E731

_MATH = {
    "Bold": _block(0x1D400, 0x1D41A, 0x1D7CE),
    "Italic": _block(0x1D434, 0x1D44E, None, {"h": "ℎ"}),
    "Bold Italic": _block(0x1D468, 0x1D482),
    "Script": _block(0x1D49C, 0x1D4B6, None, _SCRIPT_EXC),
    "Bold Script": _block(0x1D4D0, 0x1D4EA),
    "Fraktur": _block(0x1D504, 0x1D51E, None, _FRAK_EXC),
    "Bold Fraktur": _block(0x1D56C, 0x1D586),
    "Double-struck": _block(0x1D538, 0x1D552, 0x1D7D8, _DS_EXC),
    "Sans": _block(0x1D5A0, 0x1D5BA, 0x1D7E2),
    "Sans Bold": _block(0x1D5D4, 0x1D5EE, 0x1D7EC),
    "Sans Italic": _block(0x1D608, 0x1D622),
    "Sans Bold Italic": _block(0x1D63C, 0x1D656),
    "Monospace": _block(0x1D670, 0x1D68A, 0x1D7F6),
}
# exceptions in _block are keyed by character, so convert them to ordinals
for _name, _exc in (("Italic", {"h": "ℎ"}), ("Script", _SCRIPT_EXC),
                    ("Fraktur", _FRAK_EXC), ("Double-struck", _DS_EXC)):
    _MATH[_name] = _FIX(_MATH[_name], _exc)

_full = {c: chr(c + 0xFEE0) for c in range(0x21, 0x7F)}
_full[0x20] = "　"

_BASE = {n: _tr(t) for n, t in _MATH.items()}
_BASE.update({
    "Full Width": _tr(_full),
    "Circled": _tr(_table([chr(0x24B6 + i) for i in range(26)], [chr(0x24D0 + i) for i in range(26)],
                          "⓪①②③④⑤⑥⑦⑧⑨")),
    "Black Circled": _tr(_table([chr(0x1F150 + i) for i in range(26)], [chr(0x1F150 + i) for i in range(26)],
                                "⓿❶❷❸❹❺❻❼❽❾")),
    "Squared": _tr(_table([chr(0x1F130 + i) for i in range(26)], [chr(0x1F130 + i) for i in range(26)])),
    "Black Squared": _tr(_table([chr(0x1F170 + i) for i in range(26)], [chr(0x1F170 + i) for i in range(26)])),
    "Parenthesized": _tr(_table([chr(0x1F110 + i) for i in range(26)], [chr(0x249C + i) for i in range(26)])),
    "Small Caps": _tr(_table(None, "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ"), str.lower),
    "Superscript": _tr(_table(None, "ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖqʳˢᵗᵘᵛʷˣʸᶻ", "⁰¹²³⁴⁵⁶⁷⁸⁹"), str.lower),
    "Subscript": _tr(str.maketrans({**{k: v for k, v in zip("aehijklmnoprstuvx", "ₐₑₕᵢⱼₖₗₘₙₒₚᵣₛₜᵤᵥₓ")},
                                    **dict(zip(DG, "₀₁₂₃₄₅₆₇₈₉"))}), str.lower),
    "Canadian": _tr(_table("ᗩᗷᑕᗪEᖴGᕼIᒍKᒪᗰᑎOᑭᑫᖇᔕTᑌᐯᗯ᙭Yᘔ", "ᗩᗷᑕᗪEᖴGᕼIᒍKᒪᗰᑎOᑭᑫᖇᔕTᑌᐯᗯ᙭Yᘔ")),
    "Cute Greek": _tr(_table(None, "αႦƈԃҽϝɠԋιʝƙʅɱɳσρϙɾʂƚυʋɯxყȥ"), str.lower),
    "Hybrid": _tr(_table(None, "ǟɮƈɖɛʄɢɦɨʝӄʟʍռօքզʀֆtʊʋաӼʏʐ"), str.lower),
    "Thai": _tr(_table(None, "ค๒ς๔єŦﻮђเןкɭ๓ภ๏קợГรՇยשฬאฯճ"), str.lower),
    "Lambda": _tr(_table("ΛβϾDΞFGΉIJKᄂMПӨPQЯƧƬЦVЩXYZ", None), str.upper),
})

_flip = _table(None, "ɐqɔpǝɟƃɥᴉɾʞlɯuodbɹsʇnʌʍxʎz", "0ƖᄅƐㄣϛ9ㄥ86",
               {"?": "¿", "!": "¡", ".": "˙", ",": "'", "(": ")", ")": "(", "&": "⅋", "_": "‾"})
_BASE["Upside Down"] = lambda s: s.lower().translate(_flip)[::-1]
_BASE["Plain"] = lambda s: s

_BASE_ORDER = [
    "Bold", "Italic", "Bold Italic", "Script", "Bold Script", "Fraktur", "Bold Fraktur",
    "Double-struck", "Sans", "Sans Bold", "Sans Italic", "Sans Bold Italic", "Monospace",
    "Full Width", "Circled", "Black Circled", "Squared", "Black Squared", "Parenthesized",
    "Small Caps", "Superscript", "Subscript", "Upside Down",
    "Canadian", "Cute Greek", "Hybrid", "Thai", "Lambda",
]

STYLES = [(n, _BASE[n]) for n in _BASE_ORDER]

# ---- Combining-mark decorations on plain text ----
_MARKS = [
    ("Strikethrough", "̶"), ("Short Strike", "̵"), ("Slash", "̸"),
    ("Underline", "̲"), ("Double Underline", "̳"), ("Overline", "̅"),
    ("Double Overline", "̿"), ("Wavy Underline", "̰"), ("Dotted Underline", "̤"),
    ("Dot Below", "̣"), ("Dot Above", "̇"), ("X Above", "̽"),
    ("X Below", "͓"), ("Bridge Below", "̪"), ("Caret Above", "̂"),
    ("Equals Below", "͇"),
]
STYLES += [(n, _combine(m)) for n, m in _MARKS]

# ---- Style + decoration combos ----
_COMBOS = [
    ("Bold", "̲"), ("Italic", "̶"), ("Script", "̅"), ("Fraktur", "̤"),
    ("Double-struck", "̰"), ("Sans Bold", "̳"), ("Monospace", "̶"),
    ("Bold Italic", "̸"), ("Small Caps", "̲"), ("Full Width", "̶"),
    ("Bold Script", "̣"), ("Sans Italic", "̲"),
]
STYLES += [(f"{b} + {dict((m, n) for n, m in _MARKS)[mk]}", _both(_BASE[b], _combine(mk)))
           for b, mk in _COMBOS]

# ---- Letter spacing ----
_SEPS = [("Spaced", " "), ("Dotted", "•"), ("Dashed", "-"), ("Slashed", "/"),
         ("Starred", "*"), ("Wavy", "~"), ("Pipe", "|"), ("Heart", "♥")]
_SEP_BASES = ["Plain", "Bold", "Sans Bold", "Monospace", "Script", "Fraktur", "Double-struck", "Small Caps"]
STYLES += [(f"{n} ({b})", _sep(s, _BASE[b])) for (n, s), b in zip(_SEPS, _SEP_BASES)]

# ---- Decorative wrappers ----
_WRAPS = [
    "★{}★", "✦{}✦", "꧁{}꧂", "【{}】", "『{}』", "「{}」", "《{}》", "♛{}♛", "☆{}☆", "♥{}♥",
    "✿{}✿", "❀{}❀", "⚡{}⚡", "🔥{}🔥", "💫{}💫", "▀▄▀▄ {} ▄▀▄▀", "•°•{}•°•", "░▒▓ {} ▓▒░",
    "⋆˚✿ {} ✿˚⋆", "┌─ {} ─┐", "☾ {} ☽", "༺ {} ༻", "〖{}〗", "｡･:*:･ﾟ★ {} ★ﾟ･:*:･｡",
    "»»— {} —««", "▁▂▃ {} ▃▂▁", "·.·´¯`·.·★ {} ★·.·´¯`·.·", "✧･ﾟ: *✧･ﾟ:* {} *:･ﾟ✧*:･ﾟ✧",
    "🌸 {} 🌸", "🦋 {} 🦋", "👑 {} 👑", "💎 {} 💎", "🌙 {} 🌙", "⚜️ {} ⚜️", "♪ {} ♪", "✨ {} ✨",
]
_WRAP_BASES = ["Bold", "Italic", "Script", "Bold Script", "Fraktur", "Double-struck",
               "Sans Bold", "Monospace", "Bold Italic", "Small Caps"]
STYLES += [(w.replace("{}", "…"), _wrap(w, _BASE[_WRAP_BASES[i % len(_WRAP_BASES)]]))
           for i, w in enumerate(_WRAPS)]
