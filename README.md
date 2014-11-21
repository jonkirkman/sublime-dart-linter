sublime-dart-linter
===================

**DEPRECATED** - Use the excellent [dart-sublime-bundle](https://github.com/guillermooo/dart-sublime-bundle)

An attempt to leverage Dart's analyzer for linting and other nice magic in Sublime Text 3.

## Status

This package ~~doesn't really do anything yet~~ only covers the basics but feel free to jump in and help make it better. 

The items below should really be completed before calling it alpha.

### TODO

- [x] Find dartanalyzer (check settings for path to Dart SDK)
- ~~[ ] Find the project root & packages directory~~
- [x] Spawn subprocess/thread for dartanalyzer
- [x] Parse the ouput from dartanalyzer (--machine flag might help)
- [x] Filter issues to those in current file
- [x] Create a text region for each issue
- [x] Decorate the regions with gutter-mark or outline
- [x] Display the corresponding warning/error in statusbar while the cursor is in region
- [ ] Add a license
