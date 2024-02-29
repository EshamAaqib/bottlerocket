use std::process::{exit, Command};

fn main() -> Result<(), std::io::Error> {
    std::env::set_var("BUILD_ID", "01");
    let ret = Command::new("buildsys").arg("build-package").status()?;
    if !ret.success() {
        exit(1);
    }
    Ok(())
}
