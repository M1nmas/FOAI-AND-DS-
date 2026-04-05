from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

import streamlit as st

try:
	import pandas as pd
except Exception:
	pd = None


BASE_DIR = Path(__file__).resolve().parent


def get_workspace_files() -> list[Path]:
	"""Return all files in the workspace root, sorted by name."""
	return sorted([p for p in BASE_DIR.iterdir() if p.is_file()], key=lambda p: p.name.lower())


def preview_text_file(file_path: Path, max_chars: int = 10000) -> str:
	"""Read a text file safely for preview."""
	try:
		return file_path.read_text(encoding="utf-8", errors="replace")[:max_chars]
	except Exception as exc:
		return f"Unable to read file: {exc}"


def preview_csv_file(file_path: Path) -> None:
	"""Preview CSV data using pandas when available, otherwise fallback to csv module."""
	st.subheader("CSV Preview")

	if pd is not None:
		try:
			data = pd.read_csv(file_path)
			st.dataframe(data, use_container_width=True)
			st.caption(f"Rows: {len(data)} | Columns: {len(data.columns)}")
			return
		except Exception as exc:
			st.warning(f"Pandas could not parse CSV. Falling back to basic preview. Reason: {exc}")

	try:
		with file_path.open("r", encoding="utf-8", errors="replace", newline="") as f:
			reader = csv.reader(f)
			rows = []
			for i, row in enumerate(reader):
				rows.append(row)
				if i >= 30:
					break
		if rows:
			st.table(rows)
		else:
			st.info("CSV file is empty.")
	except Exception as exc:
		st.error(f"Unable to preview CSV: {exc}")


def run_python_file(file_path: Path) -> tuple[int, str, str]:
	"""Run a Python file and return exit code, stdout, stderr."""
	completed = subprocess.run(
		[sys.executable, str(file_path)],
		cwd=str(BASE_DIR),
		capture_output=True,
		text=True,
		timeout=60,
	)
	return completed.returncode, completed.stdout, completed.stderr


def render_file_actions(file_path: Path) -> None:
	st.markdown(f"### {file_path.name}")

	with st.container(border=True):
		col1, col2, col3 = st.columns(3)

		with col1:
			if st.button("Preview", key=f"preview_{file_path.name}"):
				if file_path.suffix.lower() == ".csv":
					preview_csv_file(file_path)
				else:
					content = preview_text_file(file_path)
					st.code(content, language="python" if file_path.suffix.lower() == ".py" else "text")

		with col2:
			if st.button("Download", key=f"download_{file_path.name}"):
				try:
					file_bytes = file_path.read_bytes()
					st.download_button(
						label=f"Click to download {file_path.name}",
						data=file_bytes,
						file_name=file_path.name,
						mime="application/octet-stream",
						key=f"download_btn_{file_path.name}",
					)
				except Exception as exc:
					st.error(f"Unable to prepare download: {exc}")

		with col3:
			is_python = file_path.suffix.lower() == ".py" and file_path.name != Path(__file__).name
			if is_python and st.button("Run Python", key=f"run_{file_path.name}"):
				with st.spinner(f"Running {file_path.name}..."):
					try:
						return_code, stdout_text, stderr_text = run_python_file(file_path)
						st.write(f"Exit code: {return_code}")
						if stdout_text.strip():
							st.text_area("stdout", stdout_text, height=180)
						else:
							st.info("No stdout output.")

						if stderr_text.strip():
							st.text_area("stderr", stderr_text, height=180)
					except subprocess.TimeoutExpired:
						st.error("Execution timed out after 60 seconds.")
					except Exception as exc:
						st.error(f"Could not execute Python file: {exc}")


def main() -> None:
	st.set_page_config(page_title="File Link Hub", layout="wide")
	st.title("Workspace File Link Hub")
	st.caption("Use the buttons below to preview, download, or run files from this workspace.")

	files = get_workspace_files()

	if not files:
		st.warning("No files found in the workspace root.")
		return

	st.info(f"Detected {len(files)} files in: {BASE_DIR}")

	for file_path in files:
		render_file_actions(file_path)


if __name__ == "__main__":
	main()
