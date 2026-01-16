# SCALIGER

**A multi-target boilerplate generator for strictly-typed datasets.**

SCALIGER is a utility for converting Python dictionaries and lists into type-safe code structures (Enums, Structs, and Implementation blocks) across multiple programming languages.

## Technical Scope

* **Code Generation:** Automates the creation of Enums with complex `impl` blocks in Rust and class-based Enums in Python.
* **Metadata Support:** Handles automatic generation of Rust `derives`, `macros`, and required `imports`.
* **Standardisation:** Ensures that data defined in one place (like an archaeological database) remains consistent across an Actix-web server (Rust) and data-processing scripts (Python).

## Status

**SCALIGER is currently in a private Alpha stage.** Version 0.0.1 is a placeholder release to secure the namespace. The core generator logic is currently maintained in a private repository to protect ongoing research and intellectual property.

## License

This project is licensed under the MIT Licence.