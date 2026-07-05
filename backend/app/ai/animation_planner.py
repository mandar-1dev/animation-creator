"""
Takes the illustration SVG + Gemini's suggested_animations list and
injects real CSS @keyframes animations targeting the element ids defined
in illustration_generator.py. This is the "Animation Engine" from the
spec, scoped to CSS/SVG (no Manim/physics-engine render farm needed to
get real, visible motion in the browser).
"""

# Each entry: element id (as defined in illustration_generator templates) -> keyframes + animation rule
ANIMATION_LIBRARY = {
    "walk": {
        "target": "#leg-left, #leg-right",
        "keyframes": "@keyframes walk { 0%,100% { transform: rotate(-8deg); } 50% { transform: rotate(8deg); } }",
        "rule": "animation: walk 0.6s ease-in-out infinite; transform-origin: center top;",
    },
    "wave": {
        "target": "#arm-right",
        "keyframes": "@keyframes wave { 0%,100% { transform: rotate(0deg); } 50% { transform: rotate(-35deg); } }",
        "rule": "animation: wave 0.8s ease-in-out infinite; transform-origin: top center;",
    },
    "blink": {
        "target": "#eye-left, #eye-right",
        "keyframes": "@keyframes blink { 0%,92%,100% { opacity: 1; } 96% { opacity: 0.05; } }",
        "rule": "animation: blink 3.5s ease-in-out infinite;",
    },
    "leaves_sway": {
        "target": "#canopy",
        "keyframes": "@keyframes sway { 0%,100% { transform: rotate(-3deg); } 50% { transform: rotate(3deg); } }",
        "rule": "animation: sway 2.4s ease-in-out infinite; transform-origin: bottom center;",
    },
    "wind": {
        "target": "#canopy",
        "keyframes": "@keyframes sway { 0%,100% { transform: rotate(-3deg); } 50% { transform: rotate(3deg); } }",
        "rule": "animation: sway 2.4s ease-in-out infinite; transform-origin: bottom center;",
    },
    "glow": {
        "target": "#sun, #moon",
        "keyframes": "@keyframes glow { 0%,100% { opacity: 1; } 50% { opacity: 0.75; } }",
        "rule": "animation: glow 2s ease-in-out infinite;",
    },
    "rotate": {
        "target": "#sun",
        "keyframes": "@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }",
        "rule": "animation: spin 12s linear infinite; transform-origin: 200px 200px;",
    },
    "smoke_chimney": {
        "target": "#smoke-stack",
        "keyframes": "@keyframes puff { 0%,100% { opacity: 0.6; } 50% { opacity: 1; } }",
        "rule": "animation: puff 1.6s ease-in-out infinite;",
    },
    "window_glow": {
        "target": "#house rect[fill='#bae6fd']",
        "keyframes": "@keyframes wglow { 0%,100% { opacity: 0.6; } 50% { opacity: 1; } }",
        "rule": "animation: wglow 2.5s ease-in-out infinite;",
    },
    "drive": {
        "target": "#car",
        "keyframes": "@keyframes bob { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-3px); } }",
        "rule": "animation: bob 0.4s ease-in-out infinite;",
    },
    "wheel_rotation": {
        "target": "#wheel-left, #wheel-right",
        "keyframes": "@keyframes rot { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }",
        "rule": "animation: rot 0.7s linear infinite; transform-origin: center;",
    },
    "flying": {
        "target": "#bird",
        "keyframes": "@keyframes fly { 0% { transform: translate(0,0); } 50% { transform: translate(40px,-20px); } 100% { transform: translate(80px,0); } }",
        "rule": "animation: fly 3s ease-in-out infinite alternate;",
    },
    "wing_flapping": {
        "target": "#wing-left, #wing-right",
        "keyframes": "@keyframes flap { 0%,100% { transform: rotate(0deg); } 50% { transform: rotate(-20deg); } }",
        "rule": "animation: flap 0.35s ease-in-out infinite; transform-origin: center right;",
    },
    "flow": {
        "target": "#water",
        "keyframes": "@keyframes flow { 0% { transform: translateX(0); } 100% { transform: translateX(-40px); } }",
        "rule": "animation: flow 2.5s linear infinite;",
    },
    "ripple": {
        "target": "#water",
        "keyframes": "@keyframes ripple { 0%,100% { opacity: 1; } 50% { opacity: 0.85; } }",
        "rule": "animation: ripple 2s ease-in-out infinite;",
    },
    "launch": {
        "target": "#rocket",
        "keyframes": "@keyframes launch { 0% { transform: translateY(0); } 100% { transform: translateY(-260px); opacity: 0.2; } }",
        "rule": "animation: launch 2.2s ease-in forwards;",
    },
    "fire": {
        "target": "#flame",
        "keyframes": "@keyframes flame { 0%,100% { transform: scaleY(1); } 50% { transform: scaleY(1.3); } }",
        "rule": "animation: flame 0.25s ease-in-out infinite; transform-origin: top center;",
    },
    "move_slowly": {
        "target": "#cloud",
        "keyframes": "@keyframes drift { 0% { transform: translateX(-20px); } 100% { transform: translateX(20px); } }",
        "rule": "animation: drift 6s ease-in-out infinite alternate;",
    },
    "petals": {
        "target": "#petals",
        "keyframes": "@keyframes petalsway { 0%,100% { transform: rotate(-4deg); } 50% { transform: rotate(4deg); } }",
        "rule": "animation: petalsway 2.5s ease-in-out infinite;",
    },
    "float": {
        "target": "g",
        "keyframes": "@keyframes floaty { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }",
        "rule": "animation: floaty 3s ease-in-out infinite;",
    },
}

# Map a few Gemini-phrased animation names to library keys
ALIASES = {
    "hand movement": "wave", "hair movement": "wind", "smiling": "blink",
    "shadow": "float", "camera zoom": "float", "walking": "walk",
    "dance": "walk", "wing flapping": "wing_flapping", "flying": "flying",
    "smoke": "smoke_chimney", "door open": "window_glow", "rain": "move_slowly",
}


def build_animated_svg(illustration_svg: str, animations: list[str]) -> str:
    style_rules = []
    css_rules = []
    seen_targets = set()

    for anim in animations:
        key = anim.strip().lower().replace(" ", "_")
        key = ALIASES.get(anim.strip().lower(), key)
        spec = ANIMATION_LIBRARY.get(key)
        if not spec or spec["target"] in seen_targets:
            continue
        seen_targets.add(spec["target"])
        style_rules.append(spec["keyframes"])
        css_rules.append(f'{spec["target"]} {{ {spec["rule"]} }}')

    if not css_rules:
        # default gentle idle animation so nothing is ever fully static
        spec = ANIMATION_LIBRARY["float"]
        style_rules.append(spec["keyframes"])
        css_rules.append(f'g {{ {spec["rule"]} }}')

    style_block = "<style>" + "\n".join(style_rules) + "\n" + "\n".join(css_rules) + "</style>"

    if "</svg>" in illustration_svg:
        return illustration_svg.replace("</svg>", style_block + "</svg>")
    return illustration_svg + style_block
