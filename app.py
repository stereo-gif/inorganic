"""
Inorganic Chemistry Isomerism Solver — Streamlit App
Python 3.10+
"""

from collections import Counter, defaultdict
from itertools import combinations, permutations, product
import math
import re
import matplotlib.pyplot as plt
import streamlit as st

from styles import (
    ACHIRAL_BADGE_COLOR,
    CHELATE_ARC_PRIMARY,
    CHELATE_ARC_SECONDARY,
    LIGAND_COLORS,
    OPTICAL_BADGE_COLOR,
    apply_styles,
    format_type_pill,
    render_hero,
    render_legend_strip,
)

GEOMETRIES = {
    "octahedral": [
        (1.0, 0.0, 0.0),
        (-1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, -1.0, 0.0),
        (0.0, 0.0, 1.0),
        (0.0, 0.0, -1.0),
    ],
    "tetrahedral": [
        (1.0, 1.0, 1.0),
        (1.0, -1.0, -1.0),
        (-1.0, 1.0, -1.0),
        (-1.0, -1.0, 1.0),
    ],
    "square_planar": [
        (1.0, 0.0, 0.0),
        (-1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, -1.0, 0.0),
    ],
    "trigonal_bipyramidal": [
        (0.0, 0.0, 1.0),
        (0.0, 0.0, -1.0),
        (1.0, 0.0, 0.0),
        (-0.5, math.sqrt(3.0) / 2.0, 0.0),
        (-0.5, -math.sqrt(3.0) / 2.0, 0.0),
    ],
    "square_pyramidal": [
        (0.0, 0.0, 1.0),
        (1.0, 0.0, 0.0),
        (-1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, -1.0, 0.0),
    ],
}


def determinant(m):
    return (
        m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
        - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
        + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    )


def mat_vec(m, v):
    return tuple(sum(m[i][j] * v[j] for j in range(3)) for i in range(3))


def match_point_index(target, points, tol=1e-7):
    for idx, p in enumerate(points):
        if all(abs(target[k] - p[k]) <= tol for k in range(3)):
            return idx
    return None


@st.cache_data
def symmetry_permutations(geometry_name, determinant_sign):
    """All idealized symmetry operations of a site set, filtered by det +/-1."""
    points = GEOMETRIES[geometry_name]
    ops = []
    for perm in permutations(range(3)):
        for signs in product((-1.0, 1.0), repeat=3):
            matrix = tuple(
                tuple(signs[i] if perm[i] == j else 0.0 for j in range(3))
                for i in range(3)
            )
            if determinant(matrix) != determinant_sign:
                continue
            mapped = [match_point_index(mat_vec(matrix, p), points) for p in points]
            if all(x is not None for x in mapped) and len(set(mapped)) == len(points):
                ops.append(tuple(mapped))
    return list(dict.fromkeys(ops))


def parse_formula(text):
    """
    Returns chelates list [(left, right, count), ...] and mono Counter.
    """
    s = text.replace(" ", "")
    if not s.startswith("M"):
        raise ValueError("Formula must start with M, e.g. M(AB)a2b2.")
    s = s[1:]
    chelates = []
    pattern = re.compile(r"\(([A-Za-z]{2})\)(\d*)")
    for match in pattern.finditer(s):
        pair = match.group(1)
        count = int(match.group(2) or "1")
        chelates.append((pair[0], pair[1], count))
    s = pattern.sub("", s)

    mono = Counter()
    pos = 0
    while pos < len(s):
        match = re.match(r"([a-z])(\d*)", s[pos:])
        if not match:
            raise ValueError(
                f"Cannot read '{s[pos:]}'. Use lowercase letters for "
                "monodentate ligands and (AB) for bidentate ligands."
            )
        ligand = match.group(1)
        count = int(match.group(2) or "1")
        mono[ligand] += count
        pos += len(match.group(0))
    return chelates, mono


def make_groups(chelates, mono):
    """Each group is (group_name, donors_tuple, is_chelate)."""
    groups = []
    for left, right, count in chelates:
        for _ in range(count):
            groups.append((f"({left}{right})", (left, right), True))
    for ligand, count in sorted(mono.items()):
        for _ in range(count):
            groups.append((ligand, (ligand,), False))
    return groups


def adjacent_pairs(points, tol=1e-6):
    """Coordination bonds are represented by shortest non-zero site distances."""
    distances = {}
    for i, p in enumerate(points):
        for j in range(i + 1, len(points)):
            q = points[j]
            d = math.sqrt(sum((p[k] - q[k]) ** 2 for k in range(3)))
            distances[(i, j)] = d
    shortest = min(distances.values())
    return {(i, j) for (i, j), d in distances.items() if abs(d - shortest) <= tol}


def combinations_sorted(items):
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            yield items[i], items[j]


def enumerate_arrangements(points, groups):
    n = len(points)
    total_donors = sum(len(g[1]) for g in groups)
    if total_donors != n:
        raise ValueError(
            f"Donor count is {total_donors}, but this "
            f"geometry has {n} coordination sites."
        )
    edges = adjacent_pairs(points)
    states = set()

    def recurse(group_index, remaining, site_labels, bridges):
        if group_index == len(groups):
            states.add((tuple(site_labels), tuple(sorted(bridges))))
            return
        _, donors, is_chelate = groups[group_index]
        if not is_chelate:
            for site in remaining:
                new_labels = list(site_labels)
                new_labels[site] = donors[0]
                recurse(
                    group_index + 1,
                    tuple(x for x in remaining if x != site),
                    new_labels,
                    bridges,
                )
        else:
            for i, j in combinations_sorted(remaining):
                if (min(i, j), max(i, j)) not in edges:
                    continue
                orientations = [(donors[0], donors[1])]
                if donors[0] != donors[1]:
                    orientations.append((donors[1], donors[0]))
                for first, second in orientations:
                    new_labels = list(site_labels)
                    new_labels[i], new_labels[j] = first, second
                    new_bridges = list(bridges) + [(min(i, j), max(i, j))]
                    recurse(
                        group_index + 1,
                        tuple(x for x in remaining if x not in (i, j)),
                        new_labels,
                        new_bridges,
                    )

    recurse(0, tuple(range(n)), [None] * n, [])
    return states


def transform_state(state, permutation):
    labels, bridges = state
    result_labels = [None] * len(labels)
    for old_site, new_site in enumerate(permutation):
        result_labels[new_site] = labels[old_site]
    mapped_bridges = tuple(
        sorted(
            (min(permutation[i], permutation[j]), max(permutation[i], permutation[j]))
            for i, j in bridges
        )
    )
    return (tuple(result_labels), mapped_bridges)


def transform_arrangement(arrangement, permutation):
    result = [None] * len(arrangement)
    for old_site, new_site in enumerate(permutation):
        result[new_site] = arrangement[old_site]
    return tuple(result)


def canonical_state(state, ops):
    return min(transform_state(state, op) for op in ops)


def canonical_arrangement(arrangement, ops):
    return min(transform_arrangement(arrangement, op) for op in ops)


def angle_deg(v1, v2):
    n1 = math.sqrt(sum(x * x for x in v1))
    n2 = math.sqrt(sum(x * x for x in v2))
    if n1 == 0 or n2 == 0:
        return 0.0
    cos_theta = max(-1.0, min(1.0, sum(a * b for a, b in zip(v1, v2)) / (n1 * n2)))
    return math.degrees(math.acos(cos_theta))


def infer_descriptors(points, arrangement, geometry):
    indices_by_label = defaultdict(list)
    for idx, lbl in enumerate(arrangement):
        indices_by_label[lbl].append(idx)

    descriptors = []

    for lbl, idxs in sorted(indices_by_label.items()):
        if len(idxs) == 3 and geometry in ("octahedral", "trigonal_bipyramidal"):
            pair_angles = [
                angle_deg(points[i], points[j]) for i, j in combinations(idxs, 2)
            ]
            has_180 = any(abs(ang - 180.0) <= 5.0 for ang in pair_angles)
            if geometry == "octahedral":
                tag = "mer" if has_180 else "fac"
                descriptors.append(f"{tag}-{lbl}3")

    for lbl, idxs in sorted(indices_by_label.items()):
        if len(idxs) >= 2:
            for i, j in combinations(idxs, 2):
                ang = angle_deg(points[i], points[j])
                if abs(ang - 180.0) <= 5.0:
                    descriptors.append(f"trans-{lbl}")
                elif (
                    geometry in ("octahedral", "square_planar", "square_pyramidal")
                    and abs(ang - 90.0) <= 5.0
                ):
                    descriptors.append(f"cis-{lbl}")

    return list(dict.fromkeys(descriptors))


def solve(formula, geometry):
    geometry = geometry.lower().replace(" ", "_")
    if geometry not in GEOMETRIES:
        raise ValueError("Unknown geometry. Choose: " + ", ".join(GEOMETRIES))
    chelates, mono = parse_formula(formula)
    groups = make_groups(chelates, mono)
    points = GEOMETRIES[geometry]
    states = enumerate_arrangements(points, groups)

    proper = symmetry_permutations(geometry, +1)
    improper = symmetry_permutations(geometry, -1)
    full_ops = proper + improper
    if not improper:
        raise RuntimeError(
            "Could not construct improper symmetry operations for this geometry."
        )

    stereo_reps = {}
    for st_item in states:
        key = canonical_state(st_item, proper)
        stereo_reps[key] = key

    stereoisomer_states = sorted(stereo_reps)
    stereoisomers = [item[0] for item in stereoisomer_states]
    bridges_by_arr = {item[0]: item[1] for item in stereoisomer_states}

    geom_reps = {}
    for st_item in states:
        gkey = canonical_state(st_item, full_ops)
        geom_reps[gkey] = gkey

    geometric_states = sorted(geom_reps)
    geometric_isomers = [item[0] for item in geometric_states]
    geom_bridges_by_arr = {item[0]: item[1] for item in geometric_states}

    chiral = []
    achiral = []
    mirror_pairs = []
    seen_pairs = set()
    enantiomer_label_map = {}

    for arr in stereoisomers:
        mirror_images = {
            canonical_arrangement(transform_arrangement(arr, op), proper)
            for op in improper
        }
        if arr in mirror_images:
            achiral.append(arr)
        else:
            chiral.append(arr)
            mirror_key = min(mirror_images)
            pair = tuple(sorted((arr, mirror_key)))
            if pair not in seen_pairs:
                seen_pairs.add(pair)
                mirror_pairs.append(pair)

    for pair_idx, (first_arr, second_arr) in enumerate(mirror_pairs, 1):
        enantiomer_label_map[first_arr] = f"Enantiomer Pair {pair_idx} (Form A)"
        enantiomer_label_map[second_arr] = f"Enantiomer Pair {pair_idx} (Form B)"

    geom_is_optical = {}
    geom_pair_index = {}
    pair_lookup = {}
    for pair_idx, (first_arr, second_arr) in enumerate(mirror_pairs, 1):
        pair_lookup[first_arr] = pair_idx
        pair_lookup[second_arr] = pair_idx

    for g_state in geometric_states:
        g_arr = g_state[0]
        matching_pair_idx = None
        for s_arr in stereoisomers:
            if canonical_arrangement(s_arr, full_ops) == canonical_arrangement(
                g_arr, full_ops
            ):
                if s_arr in pair_lookup:
                    matching_pair_idx = pair_lookup[s_arr]
                    break
        geom_is_optical[g_arr] = matching_pair_idx is not None
        geom_pair_index[g_arr] = matching_pair_idx

    descriptors_map = {
        arr: infer_descriptors(points, arr, geometry) for arr in stereoisomers
    }
    geom_descriptors_map = {
        arr: infer_descriptors(points, arr, geometry) for arr in geometric_isomers
    }

    return {
        "geometry": geometry,
        "site_count": len(points),
        "raw_arrangements": len(states),
        "stereoisomers": stereoisomers,
        "bridges_by_arr": bridges_by_arr,
        "geometric_isomers": geometric_isomers,
        "geom_bridges_by_arr": geom_bridges_by_arr,
        "geom_is_optical": geom_is_optical,
        "geom_pair_index": geom_pair_index,
        "achiral": achiral,
        "chiral": chiral,
        "enantiomer_pairs": mirror_pairs,
        "enantiomer_label_map": enantiomer_label_map,
        "descriptors_map": descriptors_map,
        "geom_descriptors_map": geom_descriptors_map,
        "points": points,
    }


def curved_bridge_points(p1, p2, bulge=0.28, steps=28):
    """Generates a smooth outward arc connecting two bidentate donor sites."""
    mx = (p1[0] + p2[0]) / 2.0
    my = (p1[1] + p2[1]) / 2.0
    mz = (p1[2] + p2[2]) / 2.0
    norm = math.sqrt(mx * mx + my * my + mz * mz)
    if norm > 1e-6:
        ux, uy, uz = mx / norm, my / norm, mz / norm
    else:
        ux, uy, uz = 0.0, 0.0, 1.0

    ctrl_x = mx + bulge * ux
    ctrl_y = my + bulge * uy
    ctrl_z = mz + bulge * uz

    xs, ys, zs = [], [], []
    for k in range(steps + 1):
        t = k / steps
        inv = 1.0 - t
        x = inv * inv * p1[0] + 2.0 * inv * t * ctrl_x + t * t * p2[0]
        y = inv * inv * p1[1] + 2.0 * inv * t * ctrl_y + t * t * p2[1]
        z = inv * inv * p1[2] + 2.0 * inv * t * ctrl_z + t * t * p2[2]
        xs.append(x)
        ys.append(y)
        zs.append(z)
    return xs, ys, zs


def draw_isomer_3d(
    points, arrangement, bridges, title, badge_text, badge_color, dark_mode=False
):
    unique_labels = sorted(set(arrangement))
    color_lookup = {
        lbl: LIGAND_COLORS[i % len(LIGAND_COLORS)]
        for i, lbl in enumerate(unique_labels)
    }
    bridge_set = {tuple(sorted(pair)) for pair in bridges}

    canvas_bg = "#111827" if dark_mode else "#FFFFFF"
    label_color = "#F8FAFC" if dark_mode else "#0F172A"
    edge_color = "#334155" if dark_mode else "#CBD5E1"

    fig = plt.figure(figsize=(4.2, 4.0), facecolor=canvas_bg)
    ax = fig.add_subplot(111, projection="3d", facecolor=canvas_bg)

    ax.scatter(
        [0.0],
        [0.0],
        [0.0],
        s=250,
        color="#1E293B",
        edgecolors="white",
        linewidth=1.3,
        zorder=5,
    )
    ax.text(
        0.0,
        0.0,
        0.0,
        "M",
        color="white",
        fontsize=9,
        fontweight="bold",
        ha="center",
        va="center",
        zorder=6,
    )

    for pt, lbl in zip(points, arrangement):
        x, y, z = pt
        c = color_lookup[lbl]
        ax.plot(
            [0.0, x],
            [0.0, y],
            [0.0, z],
            color="#94A3B8",
            linestyle="-",
            linewidth=1.6,
            alpha=0.85,
        )
        ax.scatter(
            [x],
            [y],
            [z],
            s=215,
            color=c,
            edgecolors="#1E293B",
            linewidth=1.0,
            zorder=6,
        )
        ax.text(
            x * 1.24,
            y * 1.24,
            z * 1.24,
            lbl,
            color=label_color,
            fontsize=10,
            fontweight="bold",
            ha="center",
            va="center",
            zorder=7,
        )

    edges = adjacent_pairs(points)
    for i, j in edges:
        pair = (min(i, j), max(i, j))
        if pair in bridge_set:
            continue
        p1, p2 = points[i], points[j]
        ax.plot(
            [p1[0], p2[0]],
            [p1[1], p2[1]],
            [p1[2], p2[2]],
            color=edge_color,
            linestyle=":",
            linewidth=0.9,
            alpha=0.7,
        )

    for idx_b, (i, j) in enumerate(sorted(bridge_set)):
        p1, p2 = points[i], points[j]
        arc_color = CHELATE_ARC_PRIMARY if idx_b % 2 == 0 else CHELATE_ARC_SECONDARY
        xs, ys, zs = curved_bridge_points(p1, p2, bulge=0.28, steps=28)
        ax.plot(
            xs,
            ys,
            zs,
            color=arc_color,
            linestyle="-",
            linewidth=2.5,
            alpha=0.95,
            zorder=8,
        )

    lim = 1.48
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(-lim, lim)
    ax.set_box_aspect([1, 1, 1])
    ax.set_axis_off()
    ax.set_title(
        f"{title} · [{badge_text}]",
        fontsize=9.5,
        fontweight="bold",
        color=badge_color,
        pad=6,
    )
    plt.tight_layout()
    return fig


def render_isomer_grid(cards, cols_per_row=2, dark_mode=False):
    for start in range(0, len(cards), cols_per_row):
        row_cols = st.columns(cols_per_row)
        chunk = cards[start : start + cols_per_row]
        for offset, item in enumerate(chunk):
            with row_cols[offset]:
                with st.container(border=True):
                    st.markdown(item["pill_html"], unsafe_allow_html=True)
                    st.markdown(f"**{item['title']}**")
                    fig = draw_isomer_3d(
                        item["points"],
                        item["arr"],
                        item["bridges"],
                        item["short_title"],
                        item["badge_text"],
                        item["badge_color"],
                        dark_mode=dark_mode,
                    )
                    st.pyplot(fig, use_container_width=True)
                    plt.close(fig)
                    desc_text = (
                        ", ".join(item["descs"])
                        if item["descs"]
                        else "No cis/trans or fac/mer label"
                    )
                    st.markdown(f"**Descriptors:** `{desc_text}`")


def render_app():
    st.set_page_config(
        page_title="Inorganic Chemistry Isomerism Solver",
        page_icon="🧪",
        layout="wide",
    )

    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False
    if "formula" not in st.session_state:
        st.session_state.formula = "M(AB)a2b2"
    if "geometry" not in st.session_state:
        st.session_state.geometry = "octahedral"

    dark_mode = st.toggle("Dark Mode", key="dark_mode")
    apply_styles(dark_mode=dark_mode)
    render_hero()
    render_legend_strip()

    with st.expander("Notation & Model Limitations", expanded=False):
        st.markdown(
            """
            - **M**: Central metal
            - **a2, b2...**: Monodentate ligands
            - **(AB)**: Bidentate ligand with two distinct donor atoms **A** and **B**
            - **(AA)**: Symmetrical bidentate ligand with identical donor ends

            *Note: This model relies on idealized coordination geometries without modeling conformational flexibility, linkage isomerism, or oxidation states.*
            """
        )

    col_input, col_geom = st.columns([2, 1])

    with col_input:
        formula = st.text_input(
            "Symbolic Formula",
            key="formula",
            help="Examples: M(AB)a2b2, Ma4, Ma3b2, M(AA)2a2",
        )

    with col_geom:
        geometry = st.selectbox(
            "Coordination Geometry",
            options=list(GEOMETRIES.keys()),
            key="geometry",
            format_func=lambda g: g.replace("_", " ").title(),
        )

    if not formula.strip():
        st.warning("Please enter a valid coordination formula.")
        return

    try:
        result = solve(formula.strip(), geometry)
    except Exception as exc:
        st.error(f"Input Error: {exc}")
        return

    st.divider()

    st.subheader("Isomer Counts")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Geometric Classes", len(result["geometric_isomers"]))
    m2.metric("Total Stereoisomers", len(result["stereoisomers"]))
    m3.metric("Achiral", len(result["achiral"]))
    m4.metric("Optical (Chiral)", len(result["chiral"]))
    m5.metric("Enantiomer Pairs", len(result["enantiomer_pairs"]))

    view_mode = st.radio(
        "Display Mode:",
        options=[
            "Geometric Isomers (Matches Geometric Classes count)",
   
