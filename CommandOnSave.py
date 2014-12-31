import sublime
import sublime_plugin
import subprocess
import os

PACKAGE_NAME = 'CommandOnSave'
SETTINGS_FILE = PACKAGE_NAME + '.sublime-settings'

class CommandOnSave(sublime_plugin.EventListener):
    def on_post_save(self, view):
        settings = sublime.load_settings(SETTINGS_FILE)
        envoy_path = settings.get("envoy_path")

        if envoy_path:

            file_name = view.file_name()
            folders = view.window().folders()

            if folders:
                folder = folders[0]

                try:
                    extensions = file_name.split('extensions/', len(file_name))[1]
                    extensions_name = extensions.split('/', len(extensions))[0]
                    extensions_sufix = extensions.split('/', len(extensions))[1]
                    extensions_name = extensions_name + '/' + extensions_sufix;

                    if isTheme(file_name, extensions_name):
                        command = 'php ' + envoy_path + ' run theme-publish --extension=' + extensions_name
                        os.chdir(folder)
                        subprocess.Popen(command, cwd=folder, shell=True)

                        print('Extension published : ' + extensions_name)
                    else:
                        print('This is not a theme file.')

                except IndexError:
                    return False
        else:
            print('Please add "envoy_path" in your preference: "Sublime Text > Preferences > Settings - User"')


def isTheme(file_name, theme_name):

    try:
        index = file_name.index(theme_name + '/themes/')
        return True
    except ValueError:
        return False
