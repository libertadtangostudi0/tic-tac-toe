use anyhow::{anyhow, Context, Result};
use std::path::{Path, PathBuf};
use std::process::{Command, Stdio};

fn main() -> Result<()> {
    let project_root = find_project_root()?;
    println!("Project root: {}", project_root.display());

    let venv = project_root.join(".venv");

    // Check if venv exists
    if !venv.exists() {
        println!("Virtual environment not found. Creating...");
        create_venv(&project_root)?;
    }

    // Sync dependencies
    println!("Synchronizing dependencies via uv...");
    uv_sync(&project_root)?;

    // Run game
    let python = python_path(&venv);
    if !python.exists() {
        return Err(anyhow!("Python inside venv not found: {}", python.display()));
    }

    println!("Launching game...");
    run_game(&project_root, &python)?;

    Ok(())
}

/// Detect project root by locating main.py near the executable
fn find_project_root() -> Result<PathBuf> {
    let exe = std::env::current_exe().context("Unable to locate current exe path")?;
    let exe_dir = exe.parent().context("Executable has no parent directory")?;

    // Case 1: main.py is in same folder
    if exe_dir.join("main.py").exists() {
        return Ok(exe_dir.to_path_buf());
    }

    // Case 2: main.py is in parent folder
    let parent = exe_dir.parent().context("No parent directory above exe")?;
    if parent.join("main.py").exists() {
        return Ok(parent.to_path_buf());
    }

    Err(anyhow!(
        "Unable to locate project root: main.py not found"
    ))
}

/// Create virtual environment using `uv venv`
fn create_venv(project_root: &Path) -> Result<()> {
    let status = Command::new("uv")
        .arg("venv")
        .arg(".venv")
        .current_dir(project_root)
        .status()
        .context("Failed to run uv venv")?;

    if !status.success() {
        return Err(anyhow!("uv venv returned error"));
    }

    Ok(())
}

/// Sync dependencies using `uv sync`
fn uv_sync(project_root: &Path) -> Result<()> {
    let status = Command::new("uv")
        .arg("sync")
        .current_dir(project_root)
        .status()
        .context("Failed to run uv sync")?;

    if !status.success() {
        return Err(anyhow!("uv sync returned error"));
    }

    Ok(())
}

/// Return path to Python inside .venv
fn python_path(venv: &Path) -> PathBuf {
    if cfg!(windows) {
        venv.join("Scripts").join("python.exe")
    } else {
        venv.join("bin").join("python")
    }
}

/// Launch game using python main.py
fn run_game(project_root: &Path, python: &Path) -> Result<()> {
    let status = Command::new(python)
        .arg("main.py")
        .current_dir(project_root)
        .stdin(Stdio::inherit())
        .stdout(Stdio::inherit())
        .stderr(Stdio::inherit())
        .status()
        .context("Failed to launch main.py")?;

    if !status.success() {
        return Err(anyhow!("Game exited with error"));
    }

    Ok(())
}
