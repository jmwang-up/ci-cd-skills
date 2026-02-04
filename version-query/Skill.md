version-query Skill Implementation

This skill provides version information for projects by querying various sources.

To use this skill:
1. Navigate to any project directory
2. Run the script with desired options:
   python src/version_query.py [--source SOURCE] [--format FORMAT] [--include-metadata]

Options:
- --source: config (package.json/VERSION), git (tags/commit), or auto (tries config first, then git)
- --format: json, text, or short (version only)
- --include-metadata: Include commit hash and build timestamp

Example usage:
python src/version_query.py
python src/version_query.py --source git --format json
python src/version_query.py --include-metadata