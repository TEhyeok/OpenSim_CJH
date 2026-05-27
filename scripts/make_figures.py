"""Generate figures for the OpenSim Korean user manual.

All figures use English/symbolic labels inside the image; Korean
captions live in the surrounding Markdown. Run from repo root:

    python3 scripts/make_figures.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = Path(__file__).resolve().parent.parent / "docs" / "images"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.titlesize": 12,
    "axes.labelsize": 10,
    "savefig.dpi": 160,
    "savefig.bbox": "tight",
})


# -----------------------------------------------------------------
# 1. Analysis workflow
# -----------------------------------------------------------------
def workflow():
    fig, ax = plt.subplots(figsize=(10, 4.2))
    ax.set_xlim(0, 10); ax.set_ylim(0, 4.5); ax.axis("off")

    stages = [
        ("Experimental\nData\n(.trc, .mot)", "#FFF1B6", 0.5),
        ("Scale", "#B6E2D3", 2.3),
        ("Inverse\nKinematics", "#B6CFE2", 4.1),
        ("Inverse\nDynamics", "#C9B6E2", 5.9),
        ("Static Opt. /\nCMC", "#E2B6C7", 7.7),
        ("Results &\nAnalysis", "#F5C6A0", 9.5),
    ]
    y0 = 2.2; w = 1.5; h = 1.4
    centers = []
    for text, color, x in stages:
        box = FancyBboxPatch((x - w/2, y0 - h/2), w, h,
                             boxstyle="round,pad=0.05",
                             linewidth=1.2, edgecolor="#444",
                             facecolor=color)
        ax.add_patch(box)
        ax.text(x, y0, text, ha="center", va="center", fontsize=10)
        centers.append(x)

    for i in range(len(centers) - 1):
        arr = FancyArrowPatch((centers[i] + w/2 + 0.02, y0),
                              (centers[i+1] - w/2 - 0.02, y0),
                              arrowstyle="->", mutation_scale=18,
                              linewidth=1.8, color="#333")
        ax.add_patch(arr)

    annotations = [
        (2.3, ("Scaled\nModel\n.osim",)),
        (4.1, ("Joint\nAngles\n.mot",)),
        (5.9, ("Joint\nMoments\n.sto",)),
        (7.7, ("Muscle\nForce/Act.\n.sto",)),
    ]
    for x, (txt,) in annotations:
        ax.annotate(txt, (x, y0 - h/2 - 0.05), (x, 0.55),
                    ha="center", va="center", fontsize=8.5,
                    color="#555",
                    arrowprops=dict(arrowstyle="->",
                                    color="#888", lw=0.8))
    ax.text(5, 4.05, "OpenSim Standard Analysis Workflow",
            ha="center", fontsize=13, fontweight="bold")
    fig.savefig(OUT / "workflow.png")
    plt.close(fig)


# -----------------------------------------------------------------
# 2. Model hierarchy
# -----------------------------------------------------------------
def model_hierarchy():
    fig, ax = plt.subplots(figsize=(11, 5.2))
    ax.set_xlim(0, 12); ax.set_ylim(0, 6); ax.axis("off")

    root = FancyBboxPatch((5.1, 5.0), 1.8, 0.7,
                          boxstyle="round,pad=0.05",
                          facecolor="#FFF1B6", edgecolor="#444",
                          linewidth=1.4)
    ax.add_patch(root)
    ax.text(6.0, 5.35, "Model (.osim)",
            ha="center", va="center", fontsize=11, fontweight="bold")

    children = [
        ("Bodies", "humerus, ulna,\nfemur, ...", 1.1, "#B6E2D3"),
        ("Joints", "PinJoint, BallJoint,\nCustomJoint, ...", 3.05, "#B6CFE2"),
        ("Forces", "Muscle,\nExternalForce, ...", 5.0, "#C9B6E2"),
        ("Markers", "RASI, LASI,\nRKNE, ...", 6.95, "#E2B6C7"),
        ("Controllers", "PrescribedController,\nCMC, ...", 8.9, "#F5C6A0"),
        ("Contacts &\nConstraints", "ContactSphere,\nContactHalfSpace", 10.85, "#D8D8D8"),
    ]
    y_top = 3.8; y_bot = 2.0
    for name, detail, x, color in children:
        b = FancyBboxPatch((x - 0.85, y_top - 0.3), 1.7, 0.65,
                           boxstyle="round,pad=0.04",
                           facecolor=color, edgecolor="#444",
                           linewidth=1.1)
        ax.add_patch(b)
        ax.text(x, y_top, name, ha="center", va="center",
                fontsize=10, fontweight="bold")
        ax.text(x, y_bot, detail, ha="center", va="center",
                fontsize=8.5, color="#333")
        ax.plot([6.0, x], [5.0, y_top + 0.35],
                color="#888", lw=0.9)
        ax.plot([x, x], [y_top - 0.3, y_bot + 0.35],
                color="#aaa", lw=0.9, linestyle=":")

    ax.text(6, 0.6,
            "Each Component owns Properties (mass, length, force, ...) "
            "and Sockets (parent_body, ...)",
            ha="center", fontsize=8.5, color="#555", style="italic")
    fig.savefig(OUT / "model-hierarchy.png")
    plt.close(fig)


# -----------------------------------------------------------------
# 3. GUI layout
# -----------------------------------------------------------------
def gui_layout():
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")

    ax.add_patch(Rectangle((0, 0), 10, 6, facecolor="#F4F4F4",
                           edgecolor="#333", linewidth=1.5))
    ax.add_patch(Rectangle((0, 5.6), 10, 0.4, facecolor="#3B5998",
                           edgecolor="#222"))
    ax.text(0.15, 5.8,
            "File   Edit   View   Tools   Window   Help",
            color="white", fontsize=10, va="center")

    ax.add_patch(Rectangle((0, 5.15), 10, 0.45,
                           facecolor="#D8E4F2", edgecolor="#888"))
    btns = ["▶", "◼", "⟲", "◀◀", "▶▶",
            "Scale", "IK", "ID", "SO", "CMC", "FD",
            "Plot", "Cam"]
    x = 0.15
    for b in btns:
        w = 0.55 if len(b) <= 2 else 0.7
        ax.add_patch(Rectangle((x, 5.22), w, 0.31,
                               facecolor="white", edgecolor="#888"))
        ax.text(x + w/2, 5.38, b, ha="center", va="center",
                fontsize=8.5)
        x += w + 0.05

    ax.add_patch(Rectangle((0.1, 1.1), 2.4, 4.0,
                           facecolor="#E8F2DE", edgecolor="#666"))
    ax.text(1.3, 4.9, "Navigator",
            ha="center", fontsize=10, fontweight="bold")
    tree = ["arm26.osim", "  Bodies", "    humerus", "    ulna_radius",
            "  Joints", "    r_shoulder", "    r_elbow",
            "  Forces", "    BIClong", "    BICshort",
            "  Markers"]
    for i, t in enumerate(tree):
        ax.text(0.2, 4.55 - i * 0.32, t, fontsize=8.5,
                family="monospace")

    ax.add_patch(Rectangle((2.6, 1.1), 5.0, 4.0,
                           facecolor="#FFFFFF", edgecolor="#666"))
    ax.text(5.1, 4.9, "3D Visualizer",
            ha="center", fontsize=10, fontweight="bold")
    ax.plot([5.1, 5.1], [2.0, 3.8], lw=4, color="#A87753",
            solid_capstyle="round")
    ax.plot([5.1, 6.0], [2.0, 1.3], lw=3.5, color="#A87753",
            solid_capstyle="round")
    ax.scatter([5.1, 5.1, 5.1, 5.4, 5.6, 5.9],
               [3.8, 2.9, 2.0, 1.7, 1.5, 1.3],
               c="#C13B3B", s=22, zorder=5)
    ax.plot([5.07, 5.13], [3.0, 2.1], lw=1.5, color="#E25555")
    ax.plot([5.13, 5.18], [3.5, 2.6], lw=1.5, color="#3B7DE2")
    ax.text(5.1, 1.45, "shoulder / elbow + muscles",
            ha="center", fontsize=8, color="#666", style="italic")

    ax.add_patch(Rectangle((7.7, 1.1), 2.2, 4.0,
                           facecolor="#FFF5E0", edgecolor="#666"))
    ax.text(8.8, 4.9, "Coordinates",
            ha="center", fontsize=10, fontweight="bold")
    coords = ["r_shoulder_elev", "shoulder_elv_angle",
              "elv_angle", "shoulder_rot", "elbow_flexion",
              "pro_sup"]
    for i, c in enumerate(coords):
        y = 4.45 - i * 0.55
        ax.text(7.85, y, c, fontsize=8)
        ax.add_patch(Rectangle((7.85, y - 0.18), 1.95, 0.08,
                               facecolor="#DDD", edgecolor="#999"))
        ax.add_patch(Rectangle((7.85 + 0.3 + i*0.15, y - 0.21), 0.12, 0.14,
                               facecolor="#3B5998", edgecolor="#222"))

    ax.add_patch(Rectangle((0.1, 0.1), 9.8, 0.9,
                           facecolor="#222", edgecolor="#000"))
    ax.text(0.2, 0.85, "Messages",
            color="white", fontsize=9.5, fontweight="bold")
    log = ["[INFO]  OpenSim 4.5.2 loaded",
           "[INFO]  Model arm26.osim opened ( 6 muscles, 2 DOF )",
           "[INFO]  Inverse Kinematics : RMS marker error = 0.0123 m"]
    for i, l in enumerate(log):
        ax.text(0.25, 0.65 - i*0.18, l,
                color="#7FEF7F", fontsize=8, family="monospace")

    fig.savefig(OUT / "gui-layout.png")
    plt.close(fig)


# -----------------------------------------------------------------
# 4. Joint angles example (IK output)
# -----------------------------------------------------------------
def joint_angles():
    t = np.linspace(0, 100, 200)
    hip = 28 * np.sin(np.radians(t * 3.6 - 30)) - 5
    knee = 35 + 28 * np.sin(np.radians(t * 3.6 * 2 - 60))
    knee = np.clip(knee, 0, None)
    ankle = 10 * np.sin(np.radians(t * 3.6 - 110))

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(t, hip, label="Hip Flexion", lw=2)
    ax.plot(t, knee, label="Knee Flexion", lw=2)
    ax.plot(t, ankle, label="Ankle Dorsiflexion", lw=2)
    ax.axhline(0, color="#aaa", lw=0.7)
    ax.axvspan(0, 60, color="#FFEAA0", alpha=0.3,
               label="Stance phase")
    ax.set_xlabel("Gait cycle (%)")
    ax.set_ylabel("Angle (degrees)")
    ax.set_title("Joint Angles (Inverse Kinematics output)")
    ax.set_xlim(0, 100); ax.set_ylim(-30, 80)
    ax.grid(alpha=0.3)
    ax.legend(loc="upper right", framealpha=0.95)
    fig.savefig(OUT / "joint-angles-example.png")
    plt.close(fig)


# -----------------------------------------------------------------
# 5. Joint moments example (ID output)
# -----------------------------------------------------------------
def joint_moments():
    t = np.linspace(0, 100, 200)
    hip_m = -0.8 * np.cos(np.radians(t * 3.6)) + 0.2
    knee_m = -0.5 * np.sin(np.radians(t * 3.6 - 30))
    ank_m = -1.2 * np.exp(-((t - 50)/15)**2) + 0.1

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(t, hip_m, label="Hip Extension Moment", lw=2)
    ax.plot(t, knee_m, label="Knee Extension Moment", lw=2)
    ax.plot(t, ank_m, label="Ankle Plantarflexion Moment", lw=2)
    ax.axhline(0, color="#aaa", lw=0.7)
    ax.axvspan(0, 60, color="#FFEAA0", alpha=0.3,
               label="Stance phase")
    ax.set_xlabel("Gait cycle (%)")
    ax.set_ylabel("Moment (N·m / kg)")
    ax.set_title("Joint Moments (Inverse Dynamics output)")
    ax.set_xlim(0, 100)
    ax.grid(alpha=0.3)
    ax.legend(loc="upper right", framealpha=0.95)
    fig.savefig(OUT / "joint-moments-example.png")
    plt.close(fig)


# -----------------------------------------------------------------
# 6. Muscle activation example (SO/CMC output)
# -----------------------------------------------------------------
def muscle_activation():
    t = np.linspace(0, 100, 200)
    soleus = np.clip(0.85 * np.exp(-((t - 45)/14)**2) + 0.02, 0, 1)
    gas = np.clip(0.7 * np.exp(-((t - 48)/12)**2) + 0.02, 0, 1)
    tib_ant = np.clip(0.5 * np.exp(-((t - 90)/12)**2)
                      + 0.4 * np.exp(-((t - 5)/8)**2) + 0.02, 0, 1)
    glut_max = np.clip(0.6 * np.exp(-((t - 15)/12)**2) + 0.05, 0, 1)
    rect_fem = np.clip(0.45 * np.exp(-((t - 60)/15)**2) + 0.05, 0, 1)

    fig, ax = plt.subplots(figsize=(8, 4))
    for label, y in [("Soleus", soleus), ("Gastrocnemius", gas),
                     ("Tibialis Ant.", tib_ant),
                     ("Gluteus Max.", glut_max),
                     ("Rectus Fem.", rect_fem)]:
        ax.plot(t, y, label=label, lw=2)
    ax.axvspan(0, 60, color="#FFEAA0", alpha=0.3,
               label="Stance phase")
    ax.set_xlabel("Gait cycle (%)")
    ax.set_ylabel("Activation [0, 1]")
    ax.set_title("Muscle Activations (Static Optimization output)")
    ax.set_xlim(0, 100); ax.set_ylim(0, 1.05)
    ax.grid(alpha=0.3)
    ax.legend(loc="upper right", framealpha=0.95, ncol=2)
    fig.savefig(OUT / "muscle-activation-example.png")
    plt.close(fig)


# -----------------------------------------------------------------
# 7. OpenSim coordinate convention
# -----------------------------------------------------------------
def coord_system():
    fig, ax = plt.subplots(figsize=(5.5, 5))
    ax.set_xlim(-2.2, 2.2); ax.set_ylim(-2.2, 2.6); ax.axis("off")
    ax.set_aspect("equal")
    # Y points visually up, Z points visually right, X comes out
    # toward lower-left to imply "forward" (toward viewer).
    arrows = [
        ((0, 0), (-1.0, -0.7),  "r", "+X (forward)"),
        ((0, 0), (0, 1.6),      "g", "+Y (up)"),
        ((0, 0), (1.7, 0),      "b", "+Z (right)"),
    ]
    for (x0, y0), (dx, dy), c, label in arrows:
        ax.add_patch(FancyArrowPatch((x0, y0), (x0 + dx, y0 + dy),
                                     arrowstyle="-|>", mutation_scale=22,
                                     lw=3.0, color=c))
    ax.text(-1.15, -0.95, "+X (forward,\ntoward viewer)", color="r",
            ha="center", va="top", fontsize=10)
    ax.text(0.08, 1.75, "+Y (up)", color="g",
            ha="left", va="bottom", fontsize=10)
    ax.text(1.78, -0.05, "+Z (right)", color="b",
            ha="left", va="top", fontsize=10)

    # Floor / sagittal plane hints
    ax.plot([-1.2, 1.2, 1.8, -0.6, -1.2],
            [-0.84, -0.84, -0.45, -0.45, -0.84],
            color="#bbb", lw=0.8, linestyle="--")
    ax.text(0, -1.05, "(ground plane)", ha="center",
            fontsize=8, color="#888", style="italic")

    ax.set_title("OpenSim Coordinate Convention\n(right-handed, Y-up)",
                 fontsize=12, fontweight="bold")
    fig.savefig(OUT / "coordinate-system.png")
    plt.close(fig)


# -----------------------------------------------------------------
# 8. Tools input/output
# -----------------------------------------------------------------
def tools_io():
    fig, ax = plt.subplots(figsize=(10, 6.4))
    ax.set_xlim(0, 12); ax.set_ylim(0, 8); ax.axis("off")
    tools = [
        ("Scale",      "generic.osim\nstatic.trc\nmeasure.xml",
                       "scaled.osim\nscaled markers"),
        ("IK",         "scaled.osim\nmotion.trc",
                       "joint_angles.mot"),
        ("ID",         "scaled.osim\njoint_angles.mot\ngrf.xml",
                       "joint_moments.sto"),
        ("SO",         "scaled.osim\njoint_angles.mot\ngrf.xml",
                       "activations.sto\nmuscle_forces.sto"),
        ("CMC",        "scaled.osim\ntracking_tasks.xml\nactuators.xml",
                       "controls.sto\nstates.sto"),
        ("Forward Dyn.","scaled.osim\ncontrols.sto\ninit_states.sto",
                        "states.sto\nkinematics.sto"),
    ]
    for i, (name, inp, out) in enumerate(tools):
        y = 7 - i * 1.15
        ax.add_patch(FancyBboxPatch((0.2, y - 0.45), 3.2, 0.9,
                                    boxstyle="round,pad=0.05",
                                    facecolor="#FFF1B6",
                                    edgecolor="#444", linewidth=1.0))
        ax.text(1.8, y, inp, ha="center", va="center",
                fontsize=8.5, family="monospace")
        ax.add_patch(FancyBboxPatch((4.6, y - 0.45), 2.4, 0.9,
                                    boxstyle="round,pad=0.05",
                                    facecolor="#B6E2D3",
                                    edgecolor="#444", linewidth=1.2))
        ax.text(5.8, y, name, ha="center", va="center",
                fontsize=12, fontweight="bold")
        ax.add_patch(FancyArrowPatch((3.45, y), (4.55, y),
                                     arrowstyle="->", mutation_scale=14,
                                     lw=1.5, color="#333"))
        ax.add_patch(FancyArrowPatch((7.05, y), (8.15, y),
                                     arrowstyle="->", mutation_scale=14,
                                     lw=1.5, color="#333"))
        ax.add_patch(FancyBboxPatch((8.2, y - 0.45), 3.6, 0.9,
                                    boxstyle="round,pad=0.05",
                                    facecolor="#B6CFE2",
                                    edgecolor="#444", linewidth=1.0))
        ax.text(10.0, y, out, ha="center", va="center",
                fontsize=8.5, family="monospace")

    ax.text(1.8, 7.85, "Inputs", ha="center", fontsize=11,
            fontweight="bold", color="#666")
    ax.text(5.8, 7.85, "Tool", ha="center", fontsize=11,
            fontweight="bold", color="#666")
    ax.text(10.0, 7.85, "Outputs", ha="center", fontsize=11,
            fontweight="bold", color="#666")
    fig.savefig(OUT / "tools-io.png")
    plt.close(fig)


# -----------------------------------------------------------------
# 9. Hill-type muscle model
# -----------------------------------------------------------------
def hill_muscle():
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    lm = np.linspace(0.3, 1.7, 200)
    fl_active = np.exp(-((lm - 1.0) / 0.45) ** 2 / 0.5)
    fl_passive = np.where(lm > 1.0,
                          np.exp(5.0 * (lm - 1.0)) - 1, 0)
    fl_passive = fl_passive / fl_passive.max() * 0.7
    ax[0].plot(lm, fl_active, label="Active", lw=2, color="#C13B3B")
    ax[0].plot(lm, fl_passive, label="Passive", lw=2, color="#3B7DE2")
    ax[0].plot(lm, fl_active + fl_passive, label="Total",
               lw=2, color="#333", linestyle="--")
    ax[0].set_xlabel("Normalized fiber length  l̃m  = lm / lopt")
    ax[0].set_ylabel("Normalized force  f̃  = F / Fmax")
    ax[0].set_title("Force-Length Relation")
    ax[0].grid(alpha=0.3); ax[0].legend()
    ax[0].axvline(1.0, color="#999", lw=0.7, linestyle=":")

    vm = np.linspace(-1, 1, 200)
    fv = np.where(vm < 0,
                  (1 + vm) / (1 - vm / 0.25),
                  1.5 - 0.5 * (1 - vm) / (1 + vm * 6))
    ax[1].plot(vm, fv, lw=2, color="#2C8C3A")
    ax[1].axvline(0, color="#999", lw=0.7, linestyle=":")
    ax[1].axhline(1, color="#999", lw=0.7, linestyle=":")
    ax[1].set_xlabel("Normalized velocity  ṽm  (− = shortening)")
    ax[1].set_ylabel("Normalized force  f̃")
    ax[1].set_title("Force-Velocity Relation")
    ax[1].grid(alpha=0.3)
    fig.suptitle("Hill-type Muscle Model Characteristics",
                 fontsize=12, fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT / "hill-muscle.png")
    plt.close(fig)


# -----------------------------------------------------------------
if __name__ == "__main__":
    workflow()
    model_hierarchy()
    gui_layout()
    joint_angles()
    joint_moments()
    muscle_activation()
    coord_system()
    tools_io()
    hill_muscle()
    print("All figures generated to", OUT)
