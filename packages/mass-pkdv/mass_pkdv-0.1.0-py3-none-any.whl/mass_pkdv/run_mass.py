import subprocess
from pathlib import Path

def run_mass(
    input_file,
    output_file,
    dim=2,
    method=3,
    n_x=300,
    k_type_x=1,
    b_x_ratio=1.0,
    n_y=300,
    k_type_y=1,
    b_y_ratio=1.0
):
    pkg_dir = Path(__file__).parent
    exe_path = pkg_dir / "bin" / "mass_pkdv.exe"

    if not exe_path.exists():
        raise FileNotFoundError(f"Executable not found: {exe_path}")

    cmd = [
        str(exe_path),
        str(input_file),
        str(output_file),
        str(dim),
        str(method),
        str(n_x),
        str(k_type_x),
        str(b_x_ratio),
        str(n_y),
        str(k_type_y),
        str(b_y_ratio),
    ]

    subprocess.run(cmd, check=True)
