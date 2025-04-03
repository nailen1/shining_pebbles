# Shining Pebbles

## Description

A collection of utility functions that enable treating a file system of multiple files as a pseudo-database, facilitating maintenance and operations across the large-scale file system.

## Installation

```bash
pip install shining_pebbles
```

## Use Cases

- RPA projects @ LIFE Asset Management

## Contact

- **June Young Park**, AI Management Dev Team Lead at LIFE Asset Management
- Email: [juneyoungpaak@gmail.com](mailto:juneyoungpaak@gmail.com)
- **Life Asset Management**, A hedge fund and private equity management firm headquartered in the International Finance Center, Yeouido, South Korea, dedicated to enhancing corporate value and shareholder value.

## Version History

### v0.5.1
- Restructured project layout for better organization
  - Moved file management utilities to `pseudo_database` package
  - Added new `load_utils.py` for DataFrame loading operations
  - Split file utilities into specialized modules

### v0.5.0
- Added new module `delete_utils.py` for file deletion operations
  - `delete_file`: Delete a single file
  - `delete_old_files`: Delete old files while keeping N newest files
  - `delete_old_files_in_file_folder_by_regex`: Delete old files in a folder matching regex pattern
