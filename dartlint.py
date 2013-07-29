import os
import sublime
import sublime_plugin
import subprocess


class DartLintIssue:
    """ An issue from dartanalyzer """

    def __init__(self, file, severity, code, message, region):
        self.file = file
        self.severity = severity
        self.code = code
        self.message = message
        self.region = region
        

class DartLintPlugin(sublime_plugin.EventListener):
    """ This plugin uses Dart analyzer to highlight issues in your files """

    errors = []
    warnings = []
    suggestions = []

    def __init__(self, *args, **kwargs):
        sublime_plugin.EventListener.__init__(self, *args, **kwargs)

    def on_load_async(self, view):
        if view.file_name().endswith('.dart'):
            self.lint_it(view)

    def on_post_save_async(self, view):
        if view.file_name().endswith('.dart'):
            self.lint_it(view)

    def on_selection_modified(self, view):
        # TODO: Make this more efficient
        # TODO: Show multiple issues occuring on the same line
        for sel in view.sel():
            for i in (self.errors + self.warnings + self.suggestions):
                if i.region.contains(sel):
                    view.set_status('dart_lint', i.message)
                    return
                else:
                    view.erase_status('dart_lint')

    def lint_it(self, view):
        name = view.file_name()

        # we need to find the dartanalyzer executable
        # TODO: Why doesn't this work?
        dartsdk_path = view.settings().get('dartsdk_path')

        if not dartsdk_path:
            print('Oh snap! Cannot find Dart SDK')
            dartsdk_path = '/Users/jonkirkman/Development/dart/dart-sdk'

        # working_directory = os.path.dirname(name)
        # for now let's just use the working dir
        # project_root = working_directory

        args = [
            os.path.join(dartsdk_path, 'bin', 'dartanalyzer'),
            '--machine',
            # '--package-root',
            # os.path.join(project_root, 'packages'),
            name
        ]

        self.clear_issues(view)

        try:
            subprocess.check_output(args, universal_newlines=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as analyzer:
            self.parse_results(view, analyzer.output)

        self.draw_issues(view)

    def parse_results(self, view, analyzed):
        """ Parse the output of dartanalyzer to a list of DartLintIssue objects.
        Using the --machine flag skips the summary and yields a single issue per line
        Each line should contain the following fields, delimited by `|`
        [0] severity
            ERROR, WARNING, SUGGESTION
        [1] error.errorCode.type
            HINT, COMPILE_TIME_ERROR, PUB_SUGGESTION, STATIC_WARNING,
            STATIC_TYPE_WARNING, SYNTACTIC_ERROR
        [2] error.errorCode
        [3] source.fullName
        [4] location.lineNumber
        [5] location.columnNumber
        [6] length
        [7] error.message """

        for line in analyzed.splitlines():
            part = line.split('|')
            # let's only worry about the current view for now
            if part[3] != view.file_name():
                continue

            r = view.line( view.text_point( int(part[4])-1, int(part[5]) ) )
            issue = DartLintIssue(file=part[3], severity=part[0], code=part[2], message=part[7], region=r)

            if part[0] == 'ERROR':
                self.errors.append(issue)
            elif part[0] == 'WARNING':
                self.warnings.append(issue)
            elif part[0] == 'SUGGESTION':
                self.suggestions.append(issue)

    def draw_issues(self, view):
        all = list(map(lambda x: x.region, self.errors + self.warnings + self.suggestions))
        view.add_regions('dart_lint', all, 'support', 'dot', sublime.DRAW_OUTLINED)

    def clear_issues(self, view):
        self.errors = []
        self.warnings = []
        self.suggestions = []
        view.erase_regions('dart_lint')

