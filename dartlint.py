import os
import sublime
import sublime_plugin
import subprocess


class DartLintPlugin(sublime_plugin.EventListener):
    issues = []

    def __init__(self, *args, **kwargs):
        sublime_plugin.EventListener.__init__(self, *args, **kwargs)

    def on_load_async(self, view):
        print('DARTLINT: async load')

    def on_post_save_async(self, view):
        print('DARTLINT: post save')
        if view.file_name().endswith('.dart'):
            self.lint_it(view)
    
    def on_modified_async(self, view):
        print('DARTLINT: modified')

    def on_selection_modified(self, view):
        print('DARTLINT: selection modified')
        for sel in view.sel():
            for i in self.issues:
                if i.contains(sel):
                    view.set_status('issues', 'blah!')
                    return
                else:
                    view.erase_status('issues')

    def lint_it(self, view):
        print('DARTLINT: lint it')
        name = view.file_name()

        # working_directory = os.path.dirname(name)

        # for now let's just use the working dir
        # project_root = working_directory

        # we need to find the dartanalyzer executable
        settings = view.settings()
        dartsdk_path = settings.get('dartsdk_path')

        if not dartsdk_path:
            print('Oh snap! Cannot find Dart SDK')
            dartsdk_path = '/Users/jonkirkman/Development/dart/dart-sdk'

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
        except subprocess.CalledProcessError as e:
            for issue in e.output.splitlines():
                part = issue.split('|')
                if part[3] == name:
                    pt = view.text_point(int(part[4])-1, int(part[5]))
                    self.issues.append(view.line(pt))

        self.draw_issues(view)

    def find_project_root():
        print('DARTLINT: findProjectRoot')

    def parse_results(self, report):
        # Using the --machine flag skips the summary and yields a single issue per line
        # Each line should contain the following fields, delimited by `|`
        # [0] severity
        #     ERROR, WARNING, SUGGESTION
        # [1] error.errorCode.type
        #     HINT, COMPILE_TIME_ERROR, PUB_SUGGESTION, STATIC_WARNING,
        #     STATIC_TYPE_WARNING, SYNTACTIC_ERROR
        # [2] error.errorCode
        # [3] source.fullName
        # [4] location.lineNumber
        # [5] location.columnNumber
        # [6] length
        # [7] error.message
        print('parseResults...')

        # region_set = []

        # for issue in report.splitlines():
        #     part = issue.split('|')
        #     pt = self.view.text_point(part[4], part[5])
        #     region_set.append(self.view.line(pt))

        # print(len(region_set))
        # self.view.add_regions('issues', region_set, 'string', 'circle')

    def draw_issues(self, view):
        print('drawing %d issues'% len(self.issues))
        view.add_regions('issues', self.issues, 'support', 'dot', sublime.DRAW_OUTLINED)

    def clear_issues(self, view):
        print('clearing %d issues'% len(self.issues))
        self.issues = []
        view.erase_regions('dartanalyzer')

