import sublime
import sublime_plugin

from ..core import ContextHelper


###----------------------------------------------------------------------------


class OverrideAuditDiffPackageCommand(ContextHelper,sublime_plugin.TextCommand):
    """
    Bulk diff either a single package or all packages. This can be invoked via
    a context menu to set a package, invoked with a "package" argument to set
    the package, or with no arguments to diff all packages.
    """
    def run(self, edit, **kwargs):
        ctx = self.view_context(None, False, **kwargs)

        self.view.window().run_command("override_audit_diff_report",
                                       {"package": ctx.package})

    def description(self, **kwargs):
        stub = "OverrideAudit: Bulk Diff Package"
        ctx = self.view_context(None, False, **kwargs)
        if ctx.package_only():
            return "%s '%s'" % (stub, ctx.package)
        else:
            return stub

    def is_visible(self, **kwargs):
        if self.always_visible(**kwargs):
            return True

        return self.view_context(None, False, **kwargs).package_only()

    def is_enabled(self, **kwargs):
        ctx = self.view_context(None, False, **kwargs)
        report_type = self._report_type(**kwargs)

        return report_type != ctx.package and self.package_exists(ctx)


###----------------------------------------------------------------------------
