#!/usr/bin/env python3
"""
ddscatcli - CLI utility to edit and run a ddscat.par file for DDSCAT.

Copyright (C) 2025  Clément Argentin
License: GPL-3.0 (see LICENSE)
"""
# flake8: noqa E501
import sys
import argparse
import shutil
import subprocess
import re
import os
from pathlib import Path
from datetime import datetime


class StoreOnceAction(argparse.Action):
    """
    Argparse action that forbids passing the same scalar option multiple times.
    This prevents silent overrides ("last wins") for scalar options.
    """

    def __call__(self, parser, namespace, values, option_string=None):
        current = getattr(namespace, self.dest, None)
        if current is not None:
            parser.error(
                f"Option {option_string} cannot be used multiple times."
            )
        setattr(namespace, self.dest, values)


# ---------- Applied if the corresponding -KEY is passed ----------
REPLACEMENTS = {
    "CSHAPE": (
        "= CSHAPE*9",
        "'ANIRCTNGL' = CSHAPE*9 shape directive\n",
    ),
    "CMDTRQ": (
        ("= CMDTRQ*6", "= CMTORQ*6"),
        "'NOTORQ' = CMDTRQ*6 (DOTORQ, NOTORQ) -- either do or skip torque calculations\n",
    ),
    "CMDSOL": (
        "= CMDSOL*6",
        "'PBCGS2' = CMDSOL*6 (PBCGS2, PBCGST, GPBICG, QMRCCG, PETRKP) -- CCG method\n",
    ),
    "CMDFFT": (
        ("= CMDFFT*6", "= CMETHD*6"),
        "'GPFAFT' = CMDFFT*6 (GPFAFT, FFTMKL) -- FFT method\n",
    ),
    "CALPHA": (
        "= CALPHA*6",
        "'GKDLDR' = CALPHA*6 (GKDLDR, LATTDR, FLTRCD) -- DDA method\n",
    ),
    "CBINFLAG": (
        "= CBINFLAG",
        "'NOTBIN' = CBINFLAG (NOTBIN, ORIGIN, ALLBIN)\n",
    ),
    "MEM_ALLOW": (
        "dimensioning allowance for target generation",
        "100 100 100 = dimensioning allowance for target generation\n",
    ),
    "WAVELENGTHS": (
        "= wavelengths (",
        "0.5 0.5 1 'INV' = wavelengths (1st,last,howmany,how=LIN,INV,LOG,TAB)\n",
    ),
    "NAMBIENT": ("= NAMBIENT", "1.0000 = NAMBIENT\n"),
    "AEFF": (
        ("a_eff", "aeff", "eff. radii"),
        "0.39789 0.39789 1 'LIN' = a_eff (1st,last,howmany,how=LIN,INV,LOG,TAB)\n",
    ),
    "NRFLD": (
        "= NRFLD (",
        "0 = NRFLD (=0 to skip nearfield calc., =1 to calculate nearfield E)\n",
    ),
    "NRFLD_EXTENTS": (
        "(fract. extens. of calc. vol.",
        "0.0 0.0 0.0 0.0 0.0 0.0 (fract. extens. of calc. vol. in -x,+x,-y,+y,-z,+z)\n",
    ),
    "TOL": (
        "= TOL = MAX ALLOWED",
        "1.00e-5 = TOL = MAX ALLOWED (NORM OF |G>=AC|E>-ACA|X>)/(NORM OF AC|E>)\n",
    ),
    "MXITER": ("= MXITER", "200      = MXITER\n"),
    "GAMMA": (
        "= GAMMA (",
        "0.00125 = GAMMA (1e-2 is normal, 3e-3 for greater accuracy)\n",
    ),
    "ETASCA": (
        "= ETASCA (",
        "0.5\t= ETASCA (number of angles is proportional to [(3+x)/ETASCA]^2 )\n",
    ),
    "POL_E01": (
        "Polarization state e01",
        "(0,0) (1.,0.) (0.,0.) = Polarization state e01 (k along x axis)\n",
    ),
    "IORTH": (
        "= IORTH",
        "2 = IORTH  (=1 to do only pol. state e01; =2 to also do orth. pol. state)\n",
    ),
    "IWRKSC": (
        "= IWRKSC",
        '1 = IWRKSC (=0 to suppress, =1 to write ".sca" file for each target orient.\n',
    ),
    "ROT_BETA": (
        "BETAMI, BETAMX, NBETA",
        "0.    0.   1  = BETAMI, BETAMX, NBETA  (beta=rotation around a1)\n",
    ),
    "ROT_THETA": (
        "THETMI, THETMX, NTHETA",
        "60.  60.   1  = THETMI, THETMX, NTHETA (theta=angle between a1 and k)\n",
    ),
    "ROT_PHI": (
        "PHIMIN, PHIMAX, NPHI",
        "0.    0.   1  = PHIMIN, PHIMAX, NPHI (phi=rotation angle of a1 around k)\n",
    ),
    "START_IWAV": (
        "first IWAV, first IRAD, first IORI",
        "0   0   0    = first IWAV, first IRAD, first IORI (0 0 0 to begin fresh)\n",
    ),
    "NSMELTS": (
        "= NSMELTS",
        "6\t= NSMELTS = number of elements of S_ij to print (not more than 9)\n",
    ),
    "SMELTS_LIST": (
        "= indices ij of elements to print",
        "11 12 21 22 31 41\t= indices ij of elements to print\n",
    ),
    "CMDFRM": (
        "= CMDFRM",
        "'TFRAME' = CMDFRM (LFRAME, TFRAME for Lab Frame or Target Frame)\n",
    ),
}

# ---------- utils ----------
_HDR_COUNT_RX = re.compile(r"^\s*(\d+)\s*=")
_NCOMP_RX = re.compile(r"^\s*\d+\s*=\s*NCOMP\b", re.IGNORECASE)
_DIEL_PATH_RX = re.compile(r"'([^']+)'")


def _resolve_env_path(varname: str) -> Path | None:
    """
    Resolve an environment path.
    Absolute paths are used as-is.
    Relative paths are interpreted relative to the current working directory.
    """
    v = os.getenv(varname)
    if not v:
        return None
    p = Path(v).expanduser()
    if not p.is_absolute():
        p = (Path.cwd() / p).resolve()
    return p


def _resolve_file_env_or_local(
    env_var: str, local_name: str, what: str
) -> Path:
    """
    Resolve a file path with the pattern:
      1) $ENV_VAR (absolute recommended; if relative -> relative to cwd)
      2) ./local_name (current directory where ddscatcli is launched)
    """
    envp = _resolve_env_path(env_var)
    if envp:
        return envp

    local = Path.cwd() / local_name
    if local.exists():
        return local

    print(
        f"[ERROR] {what} not found. Set it via:\n"
        f"  export {env_var}=/path/to/{local_name}\n"
        f"or place {local_name} in the current directory.",
        file=sys.stderr,
    )
    sys.exit(2)


def _resolve_exe_env_or_local_or_path(
    env_var: str, local_name: str, what: str
) -> Path:
    """
    Resolve an executable path with the pattern:
      1) $ENV_VAR (absolute recommended; if relative -> relative to cwd)
      2) ./local_name (current directory where ddscatcli is launched)
      3) local_name found on PATH
    """
    envp = _resolve_env_path(env_var)
    if envp:
        return envp

    local = Path.cwd() / local_name
    if local.exists():
        return local.resolve()

    which = shutil.which(local_name)
    if which:
        return Path(which).resolve()

    print(
        f"[ERROR] {what} executable not found.\n"
        f"Set it via:\n"
        f"  export {env_var}=/path/to/{local_name}\n"
        f"or place an executable named '{local_name}' in the current directory,\n"
        f"or ensure '{local_name}' is on your PATH.",
        file=sys.stderr,
    )
    sys.exit(4)


def _resolve_par() -> Path:
    return _resolve_file_env_or_local("DDSCAT_PAR", "ddscat.par", "ddscat.par")


def _resolve_post_par() -> Path:
    return _resolve_file_env_or_local(
        "DDPOST_PAR", "ddpostprocess.par", "ddpostprocess.par"
    )


def _resolve_exe() -> Path:
    return _resolve_exe_env_or_local_or_path("DDSCAT_EXE", "ddscat", "ddscat")


def _resolve_post_exe() -> Path:
    return _resolve_exe_env_or_local_or_path(
        "DDPOST_EXE", "ddpostprocess", "ddpostprocess"
    )


def _run_ddpostprocess():
    post_par = _resolve_post_par()
    post_exe = _resolve_post_exe()

    workdir = post_par.parent
    print(f"[POST] {post_exe} (cwd: {workdir})")

    subprocess.run([str(post_exe)], cwd=str(workdir), check=True)


def normalize_line(s: str) -> str:
    return s if s.endswith("\n") else (s + "\n")


def smart_patch(default_line: str, user_value: str) -> str:
    """
    If the user passes a full line (contains '=' or starts with a quote),
    keep it verbatim (ensuring a trailing newline).
    Otherwise, replace the LHS token(s) before '=' of the default_line with user_value.
    If default_line starts with a quoted token, replace only that token.
    """
    v = user_value.strip()
    if ("=" in v) or v.startswith("'"):
        return v + ("\n" if not v.endswith("\n") else "")
    dl = default_line.rstrip("\n")
    if dl.startswith("'"):
        try:
            q_end = dl.index("'", 1)
            return f"'{v}'{dl[q_end+1:]}\n"
        except ValueError:
            pass
    eq = dl.find("=")
    if eq != -1:
        rhs = dl[eq:]
        return f"{v} {rhs}\n"
    return v + "\n"


def read_lines(path: Path):
    try:
        return path.read_text().splitlines(keepends=True)
    except Exception as e:
        print(f"ERROR: cannot read {path}: {e}", file=sys.stderr)
        sys.exit(2)


def write_with_backup(path: Path, lines):
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    bak = path.with_suffix(path.suffix + f".bak.{ts}")
    shutil.copy2(path, bak)
    path.write_text("".join(lines))
    return bak


def find_index_contains(lines, substr, start_at=0):
    for i in range(start_at, len(lines)):
        if substr.lower() in lines[i].lower():
            return i
    return None


def _line_contains_any_needle(line: str, needle_or_list) -> bool:
    if isinstance(needle_or_list, (tuple, list)):
        L = line.lower()
        return any(n.lower() in L for n in needle_or_list)
    else:
        return needle_or_list.lower() in line.lower()


def _parse_header_count(header_line: str) -> int:
    m = _HDR_COUNT_RX.match(header_line)
    if not m:
        raise RuntimeError(
            f"Cannot parse count from scattering header: {header_line.strip()}"
        )
    return int(m.group(1))


def patch_shpar_only(lines, override_values):
    """
    Replace the next len(override_values) lines immediately after the CSHAPE line,
    using the current file’s lines as the base for smart_patch.
    """
    out = list(lines)
    idx_cshape = find_index_contains(out, "= CSHAPE*9")
    if idx_cshape is None:
        raise RuntimeError("CSHAPE line not found (looking for '= CSHAPE*9').")

    bases = []
    cursor = idx_cshape + 1
    for _ in range(len(override_values)):
        if cursor >= len(out):
            raise RuntimeError(
                "File too short while reading existing SHPAR lines."
            )
        bases.append(out[cursor])
        cursor += 1

    patched = [
        smart_patch(bases[i], override_values[i])
        for i in range(len(override_values))
    ]
    for i, new_line in enumerate(patched):
        pos = idx_cshape + 1 + i
        out[pos] = new_line
    return out


def apply_generic_replacements(
    lines, replacements, cli_overrides, keys_to_process=None
):
    """
    Apply replacements only for keys with CLI values (or the provided keys_to_process).
    """
    if keys_to_process is None:
        keys_to_process = [
            k for k, v in cli_overrides.items() if v is not None
        ]
    successes, errors, changed = [], [], False
    out = list(lines)
    for key in keys_to_process:
        needle, default_line = replacements[key]
        user_val = cli_overrides.get(key)
        replacement = smart_patch(default_line, user_val)
        found = False
        for i, line in enumerate(out):
            if _line_contains_any_needle(line, needle):
                found = True
                if line != replacement:
                    out[i] = replacement
                    changed = True
                    successes.append(f"{key}: replaced.")
                else:
                    successes.append(f"{key}: already correct.")
                break
        if not found:
            nstr = (
                " | ".join(needle)
                if isinstance(needle, (tuple, list))
                else str(needle)
            )
            errors.append(f"{key}: pattern not found (needle: {nstr})")
    return out, changed, successes, errors


def _find_scatter_header_index(lines, mode):
    probes = []
    if mode == "planes":
        probes = ["number of scattering planes", " nplanes "]
    elif mode == "orders":
        probes = ["number of scattering orders", " norders "]
    elif mode == "cones":
        probes = ["number of scattering cones", " cones"]
    else:
        return None
    for i, ln in enumerate(lines):
        L = ln.lower()
        if any(p in L for p in probes):
            return i
    return None


def patch_scatter_only(
    lines, nplanes=None, norders=None, ncones=None, payload_lines=None
):
    out = list(lines)

    mode = None
    count = None
    if nplanes is not None:
        mode, count = "planes", int(nplanes)
    if norders is not None:
        mode, count = "orders", int(norders)
    if ncones is not None:
        mode, count = "cones", int(ncones)

    if mode is None and payload_lines:
        mode = "planes"  # default guess

    if mode is None:
        return out

    idx_head = _find_scatter_header_index(out, mode)
    if idx_head is None:
        raise RuntimeError(
            "Scattering header not found (planes/orders/cones)."
        )

    old_n = _parse_header_count(out[idx_head])

    if count is None and payload_lines is not None:
        count = len(payload_lines)
    if count is None:
        return out

    base = out[idx_head].rstrip("\n")
    header_new = re.sub(r"^\s*\d+", str(count), base) + "\n"

    end_old = idx_head + 1 + old_n
    if end_old > len(out):
        raise RuntimeError(
            f"File too short: header says {old_n} lines but only {len(out) - (idx_head+1)} available."
        )

    if payload_lines is not None:
        new_payload = [
            ln if ln.endswith("\n") else (ln + "\n") for ln in payload_lines
        ]
        if len(new_payload) != count:
            raise RuntimeError(
                f"Provided {len(new_payload)} payload lines but header count is {count}."
            )
    else:
        if count > old_n:
            raise RuntimeError(
                f"Increasing count from {old_n} to {count} requires providing lines "
                f"(-PLANE/-ORDER/-CONE)."
            )
        new_payload = out[idx_head + 1 : idx_head + 1 + count]

    out[idx_head] = header_new
    del out[idx_head + 1 : end_old]
    for j, ln in enumerate(new_payload):
        out.insert(idx_head + 1 + j, ln)

    return out


# === NCOMP + dielectric files ===
def _find_ncomp_header_index(lines):
    for i, ln in enumerate(lines):
        if _NCOMP_RX.search(ln):
            return i
    return None


def _extract_diel_path(line):
    m = _DIEL_PATH_RX.search(line)
    return m.group(1) if m else None


def _format_diel_line(idx_one_based, user_str, base_existing=None):
    s = user_str.strip()
    # user provided a full line
    if ("=" in s) or s.startswith("'"):
        return normalize_line(s)
    # user provided only a path
    return f"'{s}' = file with refractive index {idx_one_based}\n"


def patch_ncomp_and_dielectrics(lines, ncomp=None, diel_list=None):
    """
    Edit the NCOMP header and the subsequent dielectric lines.
    Rules:
      - If diel_list is provided and ncomp is None -> ncomp = len(diel_list)
      - If increasing ncomp without providing enough diel lines -> error
      - If decreasing ncomp without diel_list -> truncate existing lines
      - When reusing existing lines, renumber indices 1..ncomp
    """
    out = list(lines)
    idx_head = _find_ncomp_header_index(out)
    if idx_head is None:
        raise RuntimeError("NCOMP header not found.")

    old_n = _parse_header_count(out[idx_head])

    # Decide target count (strict when ncomp is explicitly provided)
    if ncomp is not None:
        new_n = int(ncomp)
        if diel_list is not None and len(diel_list) != new_n:
            raise RuntimeError(
                f"NCOMP={new_n} but received {len(diel_list)} dielectric entries. "
                "Provide exactly NCOMP dielectric files/lines."
            )
    elif diel_list:
        new_n = len(diel_list)
    else:
        # Nothing to do
        return out, False, []

    # Build payload
    start = idx_head + 1
    end_old = start + old_n
    if end_old > len(out):
        raise RuntimeError(
            f"File too short after NCOMP: header says {old_n} dielectric lines but fewer are present."
        )

    existing = out[start:end_old]

    payload = []
    info_msgs = []

    if diel_list:
        # Use user-provided list (validated above if NCOMP was explicitly set)
        for i in range(new_n):
            payload.append(_format_diel_line(i + 1, diel_list[i]))
    else:
        # No new lines provided
        if new_n > old_n:
            raise RuntimeError(
                f"Increasing NCOMP from {old_n} to {new_n} requires providing dielectric lines via -DIEL."
            )
        # Reuse/truncate existing, but renumber indices 1..new_n
        for i in range(new_n):
            line = existing[i]
            path = _extract_diel_path(line) or ""
            payload.append(f"'{path}' = file with refractive index {i+1}\n")

    # Rewrite header (preserve RHS)
    base = out[idx_head].rstrip("\n")
    header_new = re.sub(r"^\s*\d+", str(new_n), base) + "\n"

    changed = False
    if out[idx_head] != header_new:
        out[idx_head] = header_new
        changed = True

    # Replace dielectric block
    del out[start:end_old]
    for j, ln in enumerate(payload):
        out.insert(start + j, ln)
    changed = True

    return out, changed, info_msgs


KNOWN_CSHAPES = [
    "ANIRCTNGL",
    "CYLNDRPBC",
    "DSKRCTPBC",
    "ELLIPSOID",
    "FROM_FILE",
    "FRMFILPBC",
    "LYRSLBPBC",
    "ONIONSHEL",
    "RCTGL_PBC",
    "RCTGLPRSM",
    "SPH_ANI_N",
    "SPHERES_N",
    "SPHRN_PBC",
]


def run(argv=None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    if "-CSHAPE" in argv:
        i = argv.index("-CSHAPE")
        if i + 1 < len(argv) and argv[i + 1] in ("-h", "--help"):
            print("Available CSHAPE values:")
            for s in KNOWN_CSHAPES:
                print("  -", s)
            return 0

    ap = argparse.ArgumentParser(description="Use a single ddscat.par")
    ap.add_argument(
        "-dry-run",
        action="store_true",
        help="Preview changes without writing.",
    )
    ap.add_argument(
        "-run", action="store_true", help="Run DDSCAT after successful edits."
    )
    ap.add_argument(
        "-post",
        action="store_true",
        help="Run ddpostprocess (independent or after DDSCAT if -run is also used).",
    )

    ap.add_argument(
        "-mpi",
        nargs="?",
        const="mpirun",
        action=StoreOnceAction,
        help="MPI launcher to use (e.g., 'mpirun', 'mpiexec', 'srun'). "
        "If provided without a value, defaults to 'mpirun'.",
    )
    ap.add_argument(
        "-np",
        type=int,
        action=StoreOnceAction,
        help="Number of MPI ranks (with -mpi).",
    )
    ap.add_argument(
        "-omp-threads",
        type=int,
        action=StoreOnceAction,
        help="Set OMP_NUM_THREADS for OpenMP threading.",
    )

    # SHPAR and scattering overrides
    ap.add_argument(
        "-SHPAR",
        action="append",
        help="Override SHPAR line(s). Repeat per line if the shape uses "
        "multiple SHPAR lines.",
    )
    ap.add_argument(
        "-NPLANES",
        type=int,
        action=StoreOnceAction,
        help="Override number of scattering planes.",
    )
    ap.add_argument("-PLANE", action="append", help="Override a plane line.")
    ap.add_argument(
        "-NORDERS",
        type=int,
        action=StoreOnceAction,
        help="Override number of diffraction orders.",
    )
    ap.add_argument("-ORDER", action="append", help="Override an order line.")
    ap.add_argument(
        "-NCONES",
        type=int,
        action=StoreOnceAction,
        help="Override number of scattering cones.",
    )
    ap.add_argument("-CONE", action="append", help="Override a cone line.")

    # NCOMP + dielectric files
    ap.add_argument(
        "-NCOMP",
        type=int,
        action=StoreOnceAction,
        help="Set number of dielectric materials.",
    )

    diel_group = ap.add_mutually_exclusive_group()
    diel_group.add_argument(
        "-DIEL",
        action="append",
        help="Dielectric file line or path. Repeat once per material. "
        "If a plain path is given, the line will be formatted as "
        "'<path>' = file with refractive index i",
    )
    diel_group.add_argument(
        "--diels",
        nargs="+",
        action=StoreOnceAction,
        help="Dielectric file paths/lines in a single flag. Example: "
        "--diels file1 file2 file3",
    )

    # Generic replacements (scalar: forbid duplicates)
    for key in REPLACEMENTS.keys():
        ap.add_argument(
            f"-{key}",
            dest=key,
            action=StoreOnceAction,
            help=f"Override {key} line. Pass a full line or a short value.",
        )

    args = ap.parse_args(argv)

    if args.post and not args.run:
        _run_ddpostprocess()
        return 0

    DDSCAT_PAR = _resolve_par()
    lines = read_lines(DDSCAT_PAR)

    # 1) Apply generic replacements first (includes -CSHAPE, ETASCA, etc.)
    cli_overrides = {k: getattr(args, k) for k in REPLACEMENTS.keys()}
    lines_after, _, ok_msgs, err_msgs = apply_generic_replacements(
        lines, REPLACEMENTS, cli_overrides, keys_to_process=None
    )
    for m in ok_msgs:
        print("  -", m)
    for err_msg in err_msgs:
        print("  !", err_msg)

    # 2) SHPAR edits (immediately after the current CSHAPE line)
    if args.SHPAR:
        try:
            lines_after = patch_shpar_only(lines_after, args.SHPAR)
        except RuntimeError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 3

    # 3) Scattering-only edits
    if (
        (args.NPLANES is not None)
        or (args.NORDERS is not None)
        or (args.NCONES is not None)
        or args.PLANE
        or args.ORDER
        or args.CONE
    ):
        try:
            payload = args.PLANE or args.ORDER or args.CONE
            lines_after = patch_scatter_only(
                lines_after,
                nplanes=args.NPLANES,
                norders=args.NORDERS,
                ncones=args.NCONES,
                payload_lines=payload,
            )
        except RuntimeError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 3

    # 4) NCOMP + dielectric handling
    diel_list = args.diels if args.diels else args.DIEL
    if (args.NCOMP is not None) or diel_list:
        try:
            lines_after, _, info_msgs = patch_ncomp_and_dielectrics(
                lines_after, ncomp=args.NCOMP, diel_list=diel_list
            )
            for m in info_msgs:
                print("  -", m)
        except RuntimeError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 3

    # 5) Write or preview
    if args.dry_run:
        diff_ct = sum(1 for a, b in zip(lines, lines_after) if a != b) + abs(
            len(lines_after) - len(lines)
        )
        print(f"[DRY-RUN] Would change {diff_ct} line(s).")
        return 0

    if lines_after != lines:
        bak = write_with_backup(DDSCAT_PAR, lines_after)
        print(f"[OK] Updated ddscat.par (backup: {bak})")
    else:
        print("[--] No changes (already matched).")

    # Exit non-zero only if user asked us to change a key we couldn't find
    if err_msgs:
        return 3

    if args.run:
        exe_path = _resolve_exe()

        cmd = []
        if args.mpi:
            launcher = args.mpi  # 'mpirun', 'mpiexec', or 'srun'
            cmd.append(launcher)
            if args.np is not None:
                if launcher.startswith("mpirun") or launcher.startswith(
                    "mpiexec"
                ):
                    cmd += ["-np", str(args.np)]
                else:
                    cmd += ["-n", str(args.np)]
        cmd.append(str(exe_path))

        env = os.environ.copy()
        if args.omp_threads is not None:
            env["OMP_NUM_THREADS"] = str(args.omp_threads)

        print(f"[RUN] {' '.join(cmd)} (cwd: {DDSCAT_PAR.parent})")
        subprocess.run(cmd, cwd=str(DDSCAT_PAR.parent), env=env, check=True)

    if args.post:
        _run_ddpostprocess()

    return 0


def main():
    raise SystemExit(run())


if __name__ == "__main__":
    main()
