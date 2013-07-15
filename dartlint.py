import os
import sublime
import sublime_plugin
import subprocess
import threading


class DartLintCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        print('DARTLINT: run')
        name = self.view.file_name()

        working_directory = os.path.dirname(name)
        print('  |-> Working dir: %s' % working_directory)

        # for now let's just use the working dir
        project_root = working_directory
        print('  |-> Project root: %s' % project_root)

        print('  |-> File to analyze: %s' % os.path.basename(name))

        settings = self.view.settings()
        dartsdk_path = settings.get('dartsdk_path')

        if not dartsdk_path:
            print('  |-> ERROR: Cannot find Dart SDK')
            dartsdk_path = '/Users/jonkirkman/Development/dart/dart-sdk'

        # analyzer_path = os.path.join(dartsdk_path, 'bin', 'dartanalyzer')
        args = [
            os.path.join(dartsdk_path, 'bin', 'dartanalyzer'),
            '--machine',
            '--package-root',
            os.path.join(project_root, 'packages'),
            name
        ]
        try:
            subprocess.check_output(args, universal_newlines=True)
        except subprocess.CalledProcessError as e:
            print('returncode: %s' % e.returncode)
            print('cmd: %s' % e.cmd)
            print('output: %s' % e.output)

    def findProjectRoot():
        print('DARTLINT: findProjectRoot')


class AnalyzerThread(threading.Thread):

    def run(self):
        print('...')

    def parseResults():
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
        print('...')
