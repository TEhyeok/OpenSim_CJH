"""Real OpenSim simulation demo for the Korean user manual.

Loads Arm26 (downloaded from opensim-org/opensim-models), runs a short
forward dynamics simulation under hand-crafted muscle excitations, then
also drives the arm with a prescribed elbow flexion motion and runs
inverse dynamics to recover the elbow moment.

Outputs all results under demo_runs/ and renders three figures into
docs/images/real-*.png.

Run from repo root:
    python3 scripts/run_real_demo.py
"""
from __future__ import annotations

import os
import shutil
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import opensim as osim

REPO = Path(__file__).resolve().parent.parent
MODEL_SRC = Path("/tmp/opensim_demo/Models/arm26.osim")
RUNS = REPO / "demo_runs"
IMAGES = REPO / "docs" / "images"
RUNS.mkdir(exist_ok=True)
IMAGES.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({"font.family": "DejaVu Sans", "savefig.dpi": 160,
                     "savefig.bbox": "tight"})


def banner(msg: str) -> None:
    bar = "─" * 60
    print(f"\n{bar}\n{msg}\n{bar}")


def load_model() -> osim.Model:
    banner("1. Loading Arm26 model")
    target = RUNS / "arm26.osim"
    shutil.copy(MODEL_SRC, target)
    model = osim.Model(str(target))
    # No visualizer (headless), but build the system for simulation.
    model.setUseVisualizer(False)
    state = model.initSystem()
    print(f"  Name        : {model.getName()}")
    print(f"  # Bodies    : {model.getBodySet().getSize()}")
    print(f"  # Joints    : {model.getJointSet().getSize()}")
    print(f"  # Muscles   : {model.getMuscles().getSize()}")
    print(f"  # DOF       : {model.getNumCoordinates()}")
    coords = [model.getCoordinateSet().get(i).getName()
              for i in range(model.getNumCoordinates())]
    print(f"  Coordinates : {coords}")
    muscles = [model.getMuscles().get(i).getName()
               for i in range(model.getMuscles().getSize())]
    print(f"  Muscles     : {muscles}")
    return model


# -------------------------------------------------------------------
# Forward dynamics demo: bicep co-contraction → elbow flexes
# -------------------------------------------------------------------
def forward_demo(model: osim.Model) -> None:
    banner("2. Forward dynamics — biceps activation flexes the elbow")
    state = model.initSystem()

    # Set initial pose: shoulder neutral, elbow extended at 0 rad
    coords = model.getCoordinateSet()
    coords.get("r_shoulder_elev").setValue(state, 0.0)
    coords.get("r_elbow_flex").setValue(state, 0.1)

    # Prescribed controller: biceps high, triceps low
    muscles = model.getMuscles()
    excitations = {
        "BIClong": 0.8, "BICshort": 0.8, "BRA": 0.3,
        "TRIlong": 0.02, "TRIlat": 0.02, "TRImed": 0.02,
    }
    controller = osim.PrescribedController()
    controller.setName("excitations")
    for i in range(muscles.getSize()):
        m = muscles.get(i)
        controller.addActuator(m)
        controller.prescribeControlForActuator(
            m.getName(), osim.Constant(excitations[m.getName()]))
    model.addController(controller)
    state = model.initSystem()

    # Reporter to collect coordinate values and muscle activations
    coord_rep = osim.TableReporter()
    coord_rep.set_report_time_interval(0.02)
    for i in range(model.getNumCoordinates()):
        c = model.getCoordinateSet().get(i)
        coord_rep.addToReport(c.getOutput("value"), c.getName())
    model.addComponent(coord_rep)

    mus_rep = osim.TableReporter()
    mus_rep.set_report_time_interval(0.02)
    for i in range(muscles.getSize()):
        m = muscles.get(i)
        mus_rep.addToReport(m.getOutput("activation"), m.getName())
    model.addComponent(mus_rep)

    state = model.initSystem()
    # Re-apply initial coordinate values after re-init
    coords = model.getCoordinateSet()
    coords.get("r_shoulder_elev").setValue(state, 0.0)
    coords.get("r_elbow_flex").setValue(state, 0.1)
    model.equilibrateMuscles(state)

    manager = osim.Manager(model)
    manager.setIntegratorAccuracy(1e-4)
    state.setTime(0.0)
    manager.initialize(state)
    print("  Integrating 0 → 1.0 s ...")
    t0 = time.time()
    manager.integrate(1.0)
    print(f"  Done in {time.time() - t0:.2f} s")

    coord_table = coord_rep.getTable()
    mus_table = mus_rep.getTable()
    osim.STOFileAdapter.write(coord_table, str(RUNS / "fd_coordinates.sto"))
    osim.STOFileAdapter.write(mus_table, str(RUNS / "fd_activations.sto"))

    # Plot
    t = np.array(coord_table.getIndependentColumn())
    elbow = np.rad2deg(np.array(coord_table.getDependentColumn(
        "r_elbow_flex").to_numpy()))
    shoulder = np.rad2deg(np.array(coord_table.getDependentColumn(
        "r_shoulder_elev").to_numpy()))

    fig, ax = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
    ax[0].plot(t, elbow, label="Elbow flexion", lw=2, color="#C13B3B")
    ax[0].plot(t, shoulder, label="Shoulder elevation",
               lw=2, color="#3B7DE2", linestyle="--")
    ax[0].axhline(0, color="#aaa", lw=0.6)
    ax[0].set_ylabel("Joint angle (deg)")
    ax[0].set_title(
        "Arm26 Forward Dynamics — Real OpenSim 4.6 simulation\n"
        "(biceps excitation 0.8 → elbow flexes)",
        fontsize=11)
    ax[0].grid(alpha=0.3); ax[0].legend(loc="lower right")

    mt = np.array(mus_table.getIndependentColumn())
    for name, color in [("BIClong", "#C13B3B"), ("BICshort", "#E25555"),
                        ("BRA", "#A33333"),
                        ("TRIlong", "#3B7DE2"), ("TRIlat", "#5B97E2"),
                        ("TRImed", "#7BB3F2")]:
        a = np.array(mus_table.getDependentColumn(name).to_numpy())
        ax[1].plot(mt, a, label=name, lw=1.6, color=color)
    ax[1].set_xlabel("Time (s)")
    ax[1].set_ylabel("Activation [0, 1]")
    ax[1].set_ylim(0, 1)
    ax[1].grid(alpha=0.3); ax[1].legend(loc="upper right", ncol=2)

    fig.tight_layout()
    fig.savefig(IMAGES / "real-fd-arm26.png")
    plt.close(fig)
    print(f"  Saved {IMAGES / 'real-fd-arm26.png'}")
    return elbow[-1], shoulder[-1]


# -------------------------------------------------------------------
# Inverse dynamics demo: prescribe elbow flexion → recover moment
# -------------------------------------------------------------------
def inverse_dynamics_demo() -> None:
    banner("3. Inverse Dynamics — prescribed elbow motion → joint moment")
    # Fresh model load (no controller/reporters from FD demo).
    model = osim.Model(str(MODEL_SRC))
    state = model.initSystem()

    # Build a coordinates .mot: shoulder fixed, elbow 0 → 90° in 1s
    duration = 1.0
    n = 101
    t = np.linspace(0, duration, n)
    elbow_deg = 90 * (0.5 - 0.5 * np.cos(np.pi * t / duration))
    shoulder_deg = np.zeros_like(t)

    # Build TimeSeriesTable
    labels = osim.StdVectorString()
    coords = model.getCoordinateSet()
    for i in range(model.getNumCoordinates()):
        labels.append(coords.get(i).getName())
    table = osim.TimeSeriesTable()
    table.setColumnLabels(labels)
    for k in range(n):
        row = osim.RowVector(model.getNumCoordinates(), 0.0)
        for i in range(model.getNumCoordinates()):
            name = coords.get(i).getName()
            if name == "r_elbow_flex":
                row[i] = float(np.deg2rad(elbow_deg[k]))
            elif name == "r_shoulder_elev":
                row[i] = float(np.deg2rad(shoulder_deg[k]))
            else:
                row[i] = 0.0
        table.appendRow(float(t[k]), row)
    # Tell OpenSim the angles are in radians
    table.addTableMetaDataString("inDegrees", "no")
    mot_path = RUNS / "prescribed_elbow.mot"
    osim.STOFileAdapter.write(table, str(mot_path))
    print(f"  Wrote prescribed motion → {mot_path.name}")

    # Configure InverseDynamicsTool
    id_tool = osim.InverseDynamicsTool()
    id_tool.setModel(model)
    id_tool.setStartTime(0.0)
    id_tool.setEndTime(duration)
    id_tool.setLowpassCutoffFrequency(-1.0)  # no filter for our clean signal
    id_tool.setCoordinatesFileName(str(mot_path))
    id_tool.setResultsDir(str(RUNS))
    id_tool.setOutputGenForceFileName("id_moments.sto")
    print("  Running InverseDynamicsTool ...")
    t0 = time.time()
    id_tool.run()
    print(f"  Done in {time.time() - t0:.2f} s")

    # Load and plot
    id_table = osim.TimeSeriesTable(str(RUNS / "id_moments.sto"))
    cols = list(id_table.getColumnLabels())
    print(f"  ID output columns: {cols}")
    id_t = np.array(id_table.getIndependentColumn())
    elbow_moment = np.array(id_table.getDependentColumn(
        "r_elbow_flex_moment").to_numpy())

    fig, ax = plt.subplots(2, 1, figsize=(8, 5.6), sharex=True)
    ax[0].plot(t, elbow_deg, lw=2, color="#3B7DE2")
    ax[0].set_ylabel("Prescribed elbow\nangle (deg)")
    ax[0].set_title("Arm26 Inverse Dynamics — Real OpenSim 4.6 run",
                    fontsize=11)
    ax[0].grid(alpha=0.3)

    ax[1].plot(id_t, elbow_moment, lw=2, color="#C13B3B")
    ax[1].axhline(0, color="#aaa", lw=0.6)
    ax[1].set_xlabel("Time (s)")
    ax[1].set_ylabel("Elbow joint\nmoment (N·m)")
    ax[1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(IMAGES / "real-id-arm26.png")
    plt.close(fig)
    print(f"  Saved {IMAGES / 'real-id-arm26.png'}")

    return id_t, elbow_moment


# -------------------------------------------------------------------
# Muscle force-length curve sampled from the actual model
# -------------------------------------------------------------------
def sample_muscle_curves() -> None:
    banner("4. Sampling BIClong active force-length curve from the model")
    model = osim.Model(str(MODEL_SRC))
    state = model.initSystem()
    muscles = model.getMuscles()
    bic = osim.Millard2012EquilibriumMuscle.safeDownCast(
        muscles.get("BIClong"))
    if bic is None:
        bic = osim.Thelen2003Muscle.safeDownCast(muscles.get("BIClong"))
    if bic is None:
        # Generic Muscle interface still works for length-tension queries
        bic = muscles.get("BIClong")
    print(f"  Muscle type: {type(bic).__name__}")

    # Sweep the elbow angle and compute the BIClong fiber length /
    # active force. This exercises the real OpenSim path geometry +
    # wrapping calculations.
    coords = model.getCoordinateSet()
    elbow = coords.get("r_elbow_flex")
    angles_deg = np.linspace(0, 130, 60)
    fiber_lengths = []
    active_forces = []
    for a_deg in angles_deg:
        elbow.setValue(state, float(np.deg2rad(a_deg)))
        model.realizeVelocity(state)
        model.equilibrateMuscles(state)
        model.realizeDynamics(state)
        fiber_lengths.append(bic.getFiberLength(state))
        active_forces.append(bic.getActiveFiberForce(state))

    fiber_lengths = np.array(fiber_lengths)
    active_forces = np.array(active_forces)
    print(f"  Fiber length range: {fiber_lengths.min():.4f} ~ "
          f"{fiber_lengths.max():.4f} m")
    print(f"  Active force range: {active_forces.min():.1f} ~ "
          f"{active_forces.max():.1f} N (at activation=1.0)")

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    ax[0].plot(angles_deg, fiber_lengths * 1000, lw=2, color="#2C8C3A")
    ax[0].set_xlabel("Elbow flexion (deg)")
    ax[0].set_ylabel("BIClong fiber length (mm)")
    ax[0].set_title("Fiber length vs. elbow angle")
    ax[0].grid(alpha=0.3)

    ax[1].plot(angles_deg, active_forces, lw=2, color="#C13B3B")
    ax[1].set_xlabel("Elbow flexion (deg)")
    ax[1].set_ylabel("Active force at a=1.0 (N)")
    ax[1].set_title("BIClong active force vs. elbow angle")
    ax[1].grid(alpha=0.3)

    fig.suptitle(
        "Arm26 BIClong characteristics — sampled from real OpenSim 4.6 model",
        fontsize=11, fontweight="bold")
    fig.tight_layout()
    fig.savefig(IMAGES / "real-biclong-curves.png")
    plt.close(fig)
    print(f"  Saved {IMAGES / 'real-biclong-curves.png'}")


def main() -> None:
    print(f"OpenSim version: {osim.__version__}")
    model = load_model()
    final_elbow, final_shoulder = forward_demo(model)
    inverse_dynamics_demo()
    sample_muscle_curves()
    banner("Summary")
    print(f"  FD final elbow flexion : {final_elbow:.2f}°")
    print(f"  FD final shoulder elev : {final_shoulder:.2f}°")
    print(f"  Outputs in : {RUNS}")
    print(f"  Figures in : {IMAGES}")


if __name__ == "__main__":
    main()
