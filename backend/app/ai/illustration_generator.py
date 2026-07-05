"""
Turns a detected object_type + color palette into a clean, professional
SVG illustration (procedurally, not via an external image-gen API - there's
no Stable Diffusion key wired up, so this is the honest "AI redraws it"
step: templated vector art parameterized by Gemini's suggested palette).

Each function returns inner SVG markup (no outer <svg> tag) so the
animation planner can wrap it with an animated <svg viewBox=...>.
"""

Colors = list[str]


def _palette(colors: Colors, fallback=("#38bdf8", "#a855f7", "#0f172a", "#f8fafc")):
    c = (colors + list(fallback))[:4]
    return c


def human(colors: Colors) -> str:
    skin, shirt, hair, _ = _palette(colors)
    return f"""
    <g id="human">
      <ellipse cx="200" cy="360" rx="60" ry="12" fill="#000" opacity="0.15"/>
      <rect id="leg-left" x="180" y="240" width="14" height="90" rx="7" fill="{shirt}"/>
      <rect id="leg-right" x="206" y="240" width="14" height="90" rx="7" fill="{shirt}"/>
      <rect x="170" y="160" width="60" height="90" rx="18" fill="{shirt}"/>
      <g id="arm-left"><rect x="140" y="165" width="16" height="70" rx="8" fill="{skin}"/></g>
      <g id="arm-right"><rect x="244" y="165" width="16" height="70" rx="8" fill="{skin}"/></g>
      <circle cx="200" cy="120" r="38" fill="{skin}"/>
      <path d="M162 108 a38 38 0 0 1 76 0 q-38 -20 -76 0" fill="{hair}"/>
      <circle id="eye-left" cx="188" cy="118" r="4" fill="#1f2937"/>
      <circle id="eye-right" cx="212" cy="118" r="4" fill="#1f2937"/>
      <path d="M188 134 q12 10 24 0" stroke="#1f2937" stroke-width="3" fill="none" stroke-linecap="round"/>
    </g>"""


def tree(colors: Colors) -> str:
    trunk, leaf, leaf2, _ = _palette(colors, ("#7c5a3a", "#22c55e", "#16a34a", "#0f172a"))
    return f"""
    <g id="tree">
      <rect x="188" y="220" width="24" height="110" rx="6" fill="{trunk}"/>
      <g id="canopy">
        <circle cx="200" cy="170" r="70" fill="{leaf}"/>
        <circle cx="150" cy="200" r="55" fill="{leaf2}"/>
        <circle cx="250" cy="200" r="55" fill="{leaf2}"/>
      </g>
    </g>"""


def mountain(colors: Colors) -> str:
    peak, snow, sky, _ = _palette(colors, ("#64748b", "#f8fafc", "#38bdf8", "#0f172a"))
    return f"""
    <g id="mountain">
      <polygon points="60,320 200,120 340,320" fill="{peak}"/>
      <polygon points="150,320 260,180 370,320" fill="{peak}" opacity="0.85"/>
      <polygon points="170,150 200,120 230,150 200,175" fill="{snow}"/>
    </g>"""


def sun(colors: Colors) -> str:
    core, glow, _, _ = _palette(colors, ("#fbbf24", "#fde68a", "#f59e0b", "#0f172a"))
    rays = "".join(
        f'<rect id="ray-{i}" x="197" y="40" width="6" height="26" rx="3" fill="{glow}" '
        f'transform="rotate({i*30} 200 200)"/>' for i in range(12)
    )
    return f"""<g id="sun">{rays}<circle cx="200" cy="200" r="55" fill="{core}"/></g>"""


def moon(colors: Colors) -> str:
    body, shadow, _, _ = _palette(colors, ("#e2e8f0", "#94a3b8", "#0f172a", "#f8fafc"))
    return f"""
    <g id="moon">
      <circle cx="200" cy="200" r="60" fill="{body}"/>
      <circle cx="222" cy="185" r="10" fill="{shadow}" opacity="0.5"/>
      <circle cx="185" cy="215" r="7" fill="{shadow}" opacity="0.5"/>
    </g>"""


def house(colors: Colors) -> str:
    wall, roof, door, _ = _palette(colors, ("#fde68a", "#dc2626", "#7c5a3a", "#0f172a"))
    return f"""
    <g id="house">
      <rect x="140" y="200" width="120" height="100" fill="{wall}"/>
      <polygon points="130,200 200,140 270,200" fill="{roof}"/>
      <rect x="185" y="240" width="30" height="60" fill="{door}"/>
      <rect x="150" y="215" width="20" height="20" fill="#bae6fd"/>
      <rect x="230" y="215" width="20" height="20" fill="#bae6fd"/>
      <rect id="smoke-stack" x="230" y="150" width="14" height="30" fill="{roof}"/>
    </g>"""


def car(colors: Colors) -> str:
    body, glass, wheel, _ = _palette(colors, ("#38bdf8", "#e2e8f0", "#1f2937", "#0f172a"))
    return f"""
    <g id="car">
      <rect x="110" y="210" width="180" height="50" rx="16" fill="{body}"/>
      <path d="M140 210 q20 -40 60 -40 h20 q40 0 60 40" fill="{body}"/>
      <rect x="160" y="180" width="80" height="32" fill="{glass}" opacity="0.7"/>
      <circle id="wheel-left" cx="150" cy="262" r="20" fill="{wheel}"/>
      <circle id="wheel-right" cx="250" cy="262" r="20" fill="{wheel}"/>
    </g>"""


def airplane(colors: Colors) -> str:
    body, wing, window, _ = _palette(colors, ("#e2e8f0", "#38bdf8", "#0f172a", "#f8fafc"))
    return f"""
    <g id="airplane">
      <ellipse cx="200" cy="200" rx="90" ry="22" fill="{body}"/>
      <polygon points="160,200 100,150 130,200" fill="{wing}"/>
      <polygon points="160,200 100,250 130,200" fill="{wing}"/>
      <polygon points="285,190 320,200 285,210" fill="{wing}"/>
      <circle cx="240" cy="196" r="5" fill="{window}"/>
      <circle cx="220" cy="196" r="5" fill="{window}"/>
    </g>"""


def bird(colors: Colors) -> str:
    body, wing, beak, _ = _palette(colors, ("#38bdf8", "#0ea5e9", "#f59e0b", "#0f172a"))
    return f"""
    <g id="bird">
      <ellipse cx="200" cy="200" rx="30" ry="18" fill="{body}"/>
      <path id="wing-left" d="M190 195 q-50 -30 -70 5 q40 5 70 10 z" fill="{wing}"/>
      <path id="wing-right" d="M210 195 q50 -30 70 5 q-40 5 -70 10 z" fill="{wing}"/>
      <polygon points="228,196 245,200 228,206" fill="{beak}"/>
      <circle cx="215" cy="192" r="10" fill="{body}"/>
    </g>"""


def river(colors: Colors) -> str:
    water, bank, _, _ = _palette(colors, ("#38bdf8", "#84cc16", "#0ea5e9", "#0f172a"))
    return f"""
    <g id="river">
      <rect x="0" y="150" width="400" height="150" fill="{bank}" opacity="0.3"/>
      <path id="water" d="M0 220 Q100 190 200 220 T400 220 V300 H0 Z" fill="{water}"/>
    </g>"""


def flower(colors: Colors) -> str:
    petal, center, stem, _ = _palette(colors, ("#f472b6", "#fde68a", "#22c55e", "#0f172a"))
    petals = "".join(
        f'<ellipse cx="200" cy="160" rx="16" ry="30" fill="{petal}" '
        f'transform="rotate({i*60} 200 190)"/>' for i in range(6)
    )
    return f"""
    <g id="flower">
      <rect x="195" y="190" width="10" height="110" fill="{stem}"/>
      <g id="petals" transform-origin="200 190">{petals}</g>
      <circle cx="200" cy="190" r="14" fill="{center}"/>
    </g>"""


def cloud(colors: Colors) -> str:
    body, _, _, _ = _palette(colors, ("#f8fafc", "#e2e8f0", "#cbd5e1", "#0f172a"))
    return f"""
    <g id="cloud">
      <ellipse cx="170" cy="200" rx="50" ry="30" fill="{body}"/>
      <ellipse cx="230" cy="195" rx="60" ry="36" fill="{body}"/>
      <ellipse cx="200" cy="215" rx="70" ry="28" fill="{body}"/>
    </g>"""


def castle(colors: Colors) -> str:
    wall, roof, gate, _ = _palette(colors, ("#94a3b8", "#7c3aed", "#1f2937", "#0f172a"))
    return f"""
    <g id="castle">
      <rect x="130" y="200" width="140" height="100" fill="{wall}"/>
      <rect x="120" y="170" width="30" height="40" fill="{wall}"/>
      <rect x="250" y="170" width="30" height="40" fill="{wall}"/>
      <polygon points="120,170 135,145 150,170" fill="{roof}"/>
      <polygon points="250,170 265,145 280,170" fill="{roof}"/>
      <path d="M185 300 v-50 a15 15 0 0 1 30 0 v50" fill="{gate}"/>
    </g>"""


def robot(colors: Colors) -> str:
    body, accent, eye, _ = _palette(colors, ("#94a3b8", "#38bdf8", "#22d3ee", "#0f172a"))
    return f"""
    <g id="robot">
      <rect x="160" y="150" width="80" height="70" rx="10" fill="{body}"/>
      <circle id="eye-left" cx="182" cy="180" r="8" fill="{eye}"/>
      <circle id="eye-right" cx="218" cy="180" r="8" fill="{eye}"/>
      <rect x="150" y="230" width="100" height="80" rx="12" fill="{body}"/>
      <rect x="120" y="235" width="20" height="60" rx="8" fill="{accent}"/>
      <rect x="260" y="235" width="20" height="60" rx="8" fill="{accent}"/>
      <rect x="192" y="120" width="16" height="24" fill="{accent}"/>
      <circle cx="200" cy="115" r="8" fill="{eye}"/>
    </g>"""


def rocket(colors: Colors) -> str:
    body, window, flame, _ = _palette(colors, ("#e2e8f0", "#38bdf8", "#f97316", "#0f172a"))
    return f"""
    <g id="rocket">
      <path d="M200 100 q40 60 40 140 h-80 q0 -80 40 -140 z" fill="{body}"/>
      <circle cx="200" cy="190" r="16" fill="{window}"/>
      <polygon points="160,240 130,270 160,270" fill="{body}"/>
      <polygon points="240,240 270,270 240,270" fill="{body}"/>
      <polygon id="flame" points="185,240 200,290 215,240" fill="{flame}"/>
    </g>"""


def dragon(colors: Colors) -> str:
    body, wing, fire, _ = _palette(colors, ("#16a34a", "#22c55e", "#f97316", "#0f172a"))
    return f"""
    <g id="dragon">
      <path d="M120 220 Q200 140 280 200 Q250 210 230 200 Q210 240 170 240 Q140 240 120 220 Z" fill="{body}"/>
      <path id="wing" d="M190 180 Q220 120 270 150 Q240 170 220 190 Z" fill="{wing}"/>
      <circle cx="255" cy="195" r="6" fill="#1f2937"/>
      <path id="fire" d="M282 200 q30 -6 46 4 q-24 10 -46 6 z" fill="{fire}"/>
    </g>"""


def cat(colors: Colors) -> str:
    body, ear, _, _ = _palette(colors, ("#f59e0b", "#78350f", "#1f2937", "#0f172a"))
    return f"""
    <g id="cat">
      <ellipse cx="200" cy="230" rx="55" ry="40" fill="{body}"/>
      <circle cx="200" cy="170" r="35" fill="{body}"/>
      <polygon points="175,145 185,110 195,145" fill="{ear}"/>
      <polygon points="205,145 215,110 225,145" fill="{ear}"/>
      <path id="tail" d="M250 240 q40 10 30 -30" stroke="{body}" stroke-width="14" fill="none" stroke-linecap="round"/>
    </g>"""


def dog(colors: Colors) -> str:
    body, ear, _, _ = _palette(colors, ("#b45309", "#78350f", "#1f2937", "#0f172a"))
    return f"""
    <g id="dog">
      <ellipse cx="200" cy="235" rx="60" ry="42" fill="{body}"/>
      <circle cx="200" cy="170" r="38" fill="{body}"/>
      <ellipse cx="172" cy="165" rx="10" ry="22" fill="{ear}"/>
      <ellipse cx="228" cy="165" rx="10" ry="22" fill="{ear}"/>
      <path id="tail" d="M255 250 q30 -20 20 -45" stroke="{body}" stroke-width="12" fill="none" stroke-linecap="round"/>
    </g>"""


def road(colors: Colors) -> str:
    asphalt, line, _, _ = _palette(colors, ("#334155", "#f8fafc", "#94a3b8", "#0f172a"))
    return f"""
    <g id="road">
      <rect x="0" y="230" width="400" height="70" fill="{asphalt}"/>
      <rect id="lane-marking" x="20" y="262" width="40" height="6" fill="{line}"/>
      <rect id="lane-marking-2" x="120" y="262" width="40" height="6" fill="{line}"/>
      <rect id="lane-marking-3" x="220" y="262" width="40" height="6" fill="{line}"/>
      <rect id="lane-marking-4" x="320" y="262" width="40" height="6" fill="{line}"/>
    </g>"""


TEMPLATES = {
    "human": human, "tree": tree, "mountain": mountain, "sun": sun, "moon": moon,
    "house": house, "car": car, "airplane": airplane, "bird": bird, "river": river,
    "flower": flower, "cloud": cloud, "castle": castle, "robot": robot,
    "rocket": rocket, "dragon": dragon, "cat": cat, "dog": dog, "road": road,
}


def generate_illustration_svg(object_type: str, colors: Colors) -> str:
    fn = TEMPLATES.get(object_type)
    if fn is None:
        # Generic fallback: soft blob with a label, so unknown objects
        # still render something instead of erroring out.
        c = _palette(colors)
        return f"""
        <g id="generic">
          <circle cx="200" cy="200" r="80" fill="{c[0]}" opacity="0.8"/>
          <text x="200" y="205" font-size="18" text-anchor="middle" fill="{c[2]}">{object_type}</text>
        </g>"""
    inner = fn(colors)
    return f'<svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">{inner}</svg>'
