# Copyright (c) 2012 Krystalic.com - Mathieu Claudel - Tout droits reserves

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sublime
import sublime_plugin

import os


class StExplorerCommand(sublime_plugin.WindowCommand):
    language = None
    text_language = {}
    delimiter = os.sep
    default_root = ''
    options = []
    dir = []

    # def __init__(self, *args, **kwargs):
        # super(StExplorerCommand, self).__init__(*args, **kwargs)

    def run(self):
        # print '------------------------------------------------------------------------------------------------'
        # print '------------------------------------------------------------------------------------------------'

        self.language = self.load_options('StE_language')
        # key = 'StE_text_to_close_' + self.language
        self.text_language['text_to_close'] = self.load_options('StE_text_to_close_' + self.language)
        self.reset()
        self.build_root()
        self.prepare_dir()

        self.view_list()

    def load_options(self, key):
        settings = None
        view = self.window.active_view()

        if view:
            settings = self.window.active_view().settings()

        if settings and settings.has('StExplorer') and key in settings.get('StExplorer'):
            # Get proj1ect-specific setting
            results = settings.get('StExplorer')[key]
        else:
            # Get user-specific or default setting
            settings = sublime.load_settings('StExplorer.sublime-settings')
            results = settings.get(key)
        return results

    def reset(self):
        self.options = []
        self.dir = []
        self.window.run_command("hide_overlay")

    def view_list(self):
        self.window.run_command("hide_overlay")
        self.window.show_quick_panel(self.options, self.callback)

    def callback(self, index):
        # print '> indexSelected = ' + str(index)
        # print '> indexSelected = ' + str(self.dir[index])

        if index < 0:
            self.reset()
            return False

        if index == 0:
            self.reset()
            return False
        else:
            if self.dir[index][1] == 0:
                self.list_dir(self.root + self.delimiter + self.dir[index][0])
            elif self.dir[index][1] == 1:
                self.open_files(self.root + self.delimiter + self.dir[index][0])

    def build_root(self):
        self.default_root = self.window.folders()[0]

    def prepare_dir(self, root=None):
        if not root:
            self.root = self.default_root
        else:
            self.root = root

        # print 'root = ' + self.root

        ListDir = []
        ListDir = os.listdir(self.root)
        ListDir.insert(0, '..')
        ListDir.insert(0, self.text_language['text_to_close'])
        # self.options.append(self.entry_browser)

        self.dir = []
        for dir in ListDir:
            type = 1
            if os.path.isdir(self.root + self.delimiter + dir) == True:
                dir += self.delimiter
                type = 0

            self.options.append(dir)
            self.dir.append([dir, type])

        # self.options = self.dir
        # print str(self.options)

    def list_dir(self, path=None):
        if not path:
            sublime.error_message('Error (line 64) : No Path Found')

        # print '> list_dir(' + path + ')'

        self.window.run_command("hide_overlay")
        self.reset()
        self.prepare_dir(path)
        self.view_list()

    def open_files(self, path=None):
        if not path:
            sublime.error_message('Error (line 69) : No Path Found')

        # print '> open_files(' + path + ')'

        # self.window.open_file(path)
