# Changelog

All notable changes to Task-NG will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **ATTACHED virtual tag**: Filter tasks by attachment status using `+ATTACHED` or `-ATTACHED`
- **Attachment indicator in list view**: Visual indicator (📎 or `[A:count]`) shows which tasks have attachments
- **Duplicate filename warnings**: Warns when attaching a file with the same name as an existing attachment
- **File size validation**: Configurable size limit (default 100MB) with helpful error messages
- **Improved error messages**: All attachment commands now provide clearer, more actionable error messages

### Changed
- **BREAKING: Attachment commands restructured to subcommand pattern**
  - Old: `task-ng attach <id> <file>`
  - New: `task-ng attachment add <id> <file>`

  Full migration guide:
  ```bash
  # Old syntax (REMOVED)
  task-ng attach 5 file.pdf
  task-ng attachments 5
  task-ng detach 5 1
  task-ng open 5 1
  task-ng export-attachment 5 1 dest.pdf

  # New syntax (REQUIRED)
  task-ng attachment add 5 file.pdf
  task-ng attachment list 5
  task-ng attachment remove 5 1
  task-ng attachment open 5 1
  task-ng attachment save 5 1 dest.pdf
  ```

### Configuration
New configuration options available:

```toml
[color]
attachment = "green"  # Color for attachment indicators

[ui]
attachment_indicator = "📎"  # Or "A" for ASCII-only terminals

[attachment]
max_size = 104857600  # 100MB in bytes
```

Set via CLI:
```bash
task-ng config set color.attachment "blue"
task-ng config set ui.attachment_indicator "A"
task-ng config set attachment.max_size 52428800  # 50MB
```

## [0.1.4] - Previous Release

Initial implementation of attachment feature with content-addressed storage.
