import sublime
import sublime_plugin

from ..core import oa_syntax, oa_setting, decorate_pkg_name, log
from ..core import ReportGenerationThread
from ...lib.packages import PackageList

###----------------------------------------------------------------------------


class OverrideReportThread(ReportGenerationThread):
    """
    Generate a report on all packages which have overrides and what they are,
    if any. The report always includes expired packages and overrides, but the
    optional parameter filters to only show expired results.
    """
    def _process(self):
        pkg_list = PackageList()

        ignored = oa_setting("ignore_overrides_in")

        only_expired = self.args["only_expired"]
        ignore_empty = self.args["ignore_empty"]

        if only_expired:
            title = "OverrideAudit: Expired Override Report"
            report_type = ":overrides_expired"
        else:
            title = "OverrideAudit: Override Report"
            report_type = ":overrides"

        expired_pkgs = []
        result = []
        if only_expired:
            result.append("WARNING: Showing only expired overrides!\n"
                          "WARNING: Non-expired overrides may exist!\n")
        result.append(self._generation_time())

        displayed = 0
        for pkg_name, pkg_info in pkg_list:
            if pkg_name not in ignored:
                if self._output_package(result, pkg_info, only_expired,
                                        expired_pkgs):
                    displayed += 1

        if displayed == 0:
            if ignore_empty:
                return sublime.set_timeout(self._notify_empty(), 10)

            result.append(self._empty_msg())

        self._set_content(title, result, report_type,
                          oa_syntax("OA-OverrideReport"),
                          {"override_audit_expired_pkgs": expired_pkgs})

    def _output_package(self, result, pkg_info, only_expired, expired_pkgs):
        shipped_override = pkg_info.has_possible_overrides(simple=False)
        normal_overrides = pkg_info.override_files(simple=True)

        expired_overrides = pkg_info.expired_override_files(simple=True)
        expired_pkg = bool(pkg_info.expired_override_files(simple=False))

        # No need to do anything if there are no overrides at all
        if not normal_overrides and not shipped_override:
            return False

        if only_expired and not expired_overrides and not expired_pkg:
            return False

        if expired_overrides:
            expired_pkgs.append(pkg_info.name)

        result.append(decorate_pkg_name(pkg_info))

        self._output_overrides(result, normal_overrides,
                               expired_overrides, only_expired)
        result.append("")

        return True

    def _output_overrides(self, result, overrides, expired, only_expired):
        if not overrides:
            return result.append("    <No simple overrides found>")

        # Must be overrides, if none are expired use a different message.
        if only_expired and not expired:
            return result.append("    <No expired simple overrides found>")

        for item in (expired if only_expired else overrides):
            fmt = "  `- {}" if item not in expired else "  `- [X] {}"
            result.append(fmt.format(item))

    def _empty_msg(self):
        return "No packages with %soverrides found" % (
                "expired " if self.args["only_expired"] else "")

    def _notify_empty(self):
        log(self._empty_msg(), status=True)


###----------------------------------------------------------------------------


class OverrideAuditOverrideReportCommand(sublime_plugin.WindowCommand):
    """
    Generate a report on all packages which have overrides and what they are,
    if any. The report always includes expired packages and overrides, but the
    optional parameter filters this to only show expired results if desired.
    """
    def run(self, force_reuse=False, only_expired=False, ignore_empty=False):
        OverrideReportThread(self.window, "Generating Override Report",
                             self.window.active_view(),
                             force_reuse=force_reuse,
                             only_expired=only_expired,
                             ignore_empty=ignore_empty).start()


###----------------------------------------------------------------------------
#