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

/// Detect project root by locating main.py or game/main.py near the executable
fn find_project_root() -> Result<PathBuf> {
    use std::path::PathBuf;

    let exe = std::env::current_exe().context("Unable to locate current exe path")?;
    let mut dir: PathBuf = exe
        .parent()
        .context("Executable has no parent directory")?
        .to_path_buf();

    // Walk up several levels: target/release -> target -> launcher -> project root -> ...
    for _ in 0..8 {
        let main_py = dir.join("main.py");
        let game_main_py = dir.join("game").join("main.py");

        if main_py.exists() || game_main_py.exists() {
            // dir is project root (contains main.py or game/main.py)
            return Ok(dir);
        }

        // Go one level up; stop if there is nowhere to go
        if !dir.pop() {
            break;
        }
    }

    Err(anyhow!(
        "Unable to locate project root: main.py or game/main.py not found"
    ))
}    

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
        .arg("game/main.py")
        .current_dir(project_root)
        .stdin(Stdio::inherit())
        .stdout(Stdio::inherit())
        .stderr(Stdio::inherit())
        .status()
        .context("Failed to launch game/main.py")?;

    if !status.success() {
        return Err(anyhow!("Game exited with error"));
    }
    Ok(())
}
