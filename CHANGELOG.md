OverrideAudit ChangeLog
=======================

Next Version (????-??-??)
-------------------------
  * Fix a bug in save_on_diff handling whereby the buffer might
    visually appear unsaved in some circumstances even though
    the file was actually saved.

  * Fix a bug introduced in 1.1.0 while fixing #24 which caused
    text in reports telling you that there are no overrides to
    be treated as an override.

  * Improve detection of packages that are dependency packages
    that are still under development so that they appear as
    appropriate in package reports (#25).

  * Massive internal refactoring has been done to make it easier
    to add in new commands and functionality. The primary target
    of the refactor was in taking a few commands which were
    overloaded and took an "action" parameter to select how they
    worked and splitting them out into distinct commands.

    This change will make it easier to add in new functionality
    but it does mean that many commands have been renamed to
    more descriptive names.

    The full list of changes is:

      override_audit_diff_override
        -> override_audit_diff_single

      override_audit_diff_package
        -> override_audit_diff_report

      override_audit_context_override
        -> override_audit_toggle_override
        -> override_audit_diff_override
        -> override_audit_edit_override
        -> override_audit_delete_override
        -> override_audit_freshen_override

      override_audit_context_package
        -> override_audit_diff_package
        -> override_audit_freshen_package

      override_audit_context_report
        -> override_audit_refresh_report

  * Enhanced all of the commands available via the context menu:

      - Commands are now always visible unless you provide an argument telling
        them to hide themselves when they do not apply; this allows you to add
        these commands to other menus and control visibily.

      - Commands will be visible but disabled when the underlying package or
        override they are supposed to work with does not exist. For an override
        this means a file does not exist, while for a package it means that the
        unpacked folder is missing.

      - The default captions for disabled commands is slightly different when
        the appropriate context information is not available to tell you what
        exactly they will do (e.g. "Diff Override" instead of telling you what
        override will be diffed)


Version 1.1.1 (2017-05-01)
--------------------------
  * Remove a debug print statement that slipped through during some
    last minute code testing prior to the last release.


Version 1.1.0 (2017-04-28)
--------------------------

  * Implement the ability to "freshen" a single expired override or
    all within a package (#15) via a context menu option
  * Implement the ability to show the diff header even if a diff is
    empty (#18) controlled via `diff_empty_hdr` option
  * Fix a problem with overrides starting with a period not being
    correctly recognized as an override (#24).
  * Fix a file case issue on Windows/MacOS where opening an override
    from a package folder with an incorrect case would not enable
    the commands to edit or diff the override.
  * Performance enhancements for some package operations for users
    with a large number of installed packages.


Version 1.0.1 (2017-04-10)
--------------------------

  * Fix mixed path separators in diff output, delete confirmations and
    diff tab headers so they are always forward slashes (unix-style)
    to visually conform with how Sublime represents package path
    fragments internally (#14).

  * The Package Report, Override Report and and Bulk Diff Reports now
    have word wrap turned off by default.

  * Enhanced the checks performed at file load and save so to more
    correctly determine if a file is actually an override or not when
    enabling integration with OverrideAudit Edit/Diff functionality.

  * Rename the "Swap Diff/Override View" command to "Swap Diff/Edit
    View" in the command palette and change the associated text used
    in Diff tab titles.

  * Add a configuration option `save_on_diff` (defaults to false) to
    control if the contents of an edited override should be persisted
    to disk before performing a diff on it.


Version 1.0.0 (2017-04-03)
--------------------------

  * Initial release