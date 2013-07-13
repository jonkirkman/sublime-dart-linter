import os
import sublime
import sublime_plugin
import subprocess
import threading


class DartLintCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        name = self.view.file_name()
        self.view.insert(edit, 0, "Hello, World!\n")

        working_directory = os.path.dirname(name)
        print('--DARTLINT--> Working dir: %s' % working_directory)

        # for now let's just use the working dir
        project_root = working_directory
        print('--DARTLINT--> Project root: %s' % project_root)

        print('--DARTLINT--> File to analyze: %s' % os.path.basename(name))

        settings = self.view.settings()
        dartsdk_path = settings.get('dartsdk_path')

        if not dartsdk_path:
            print('--DARTLINT--> ERROR: Cannot find Dart SDK')
            dartsdk_path = '/Users/jonkirkman/Development/dart/dart-sdk'

        analyzer_path = os.path.join(dartsdk_path, 'bin', 'dartanalyzer')
        result = subprocess.check_output([analyzer_path, "-h"], universal_newlines=True)
        print('--DARTLINT--> CMD: %s' % result)

    def findProjectRoot():
        print('--DARTLINT--> Find the project root')


class AnalyzerThread(threading.Thread):

    def run(self):
        print('DARTLINT-> ...')
