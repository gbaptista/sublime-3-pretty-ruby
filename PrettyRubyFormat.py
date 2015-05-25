import sublime, sublime_plugin, subprocess, re, tempfile, shutil
from subprocess import Popen, PIPE

class PrettyRubyFormat(sublime_plugin.TextCommand):
  def run(self, edit, args=[]):

    settings = sublime.load_settings('PrettyRuby.sublime-settings')
    if settings.get('ruby_path'):
      ruby_path = settings.get('ruby_path')
    if settings.get('rubocop_path'):
      rubocop_path = settings.get('rubocop_path')

    settings = sublime.load_settings('Preferences.sublime-settings')
    if settings.get('ruby_path'):
      ruby_path = settings.get('ruby_path')
    if settings.get('rubocop_path'):
      rubocop_path = settings.get('rubocop_path')

    for region in self.view.sel():
      if not region.empty():
        s = self.view.substr(region)

        # Start PP ---------------------------------
        output = str(Popen([ruby_path, '-e', "o = [" + s + "]; o = o.first; raise unless [Array, Hash].include? o.class; require 'pp'; pp(o)"], stdout=PIPE).stdout.read())

        if output:
          output = re.sub(r"^b'|'$", '', output)
          output = bytes(output, "utf-8").decode("unicode_escape")
          output = re.sub(r"\n$", '', output)
          if output:
            s = output
        # End PP ---------------------------------

        # Start Rubocop --------------------------
        try:
          temp_dir = tempfile.mkdtemp()
          with open(temp_dir + '/c.rb', mode='w', encoding='utf-8') as f:
            f.write(s)

          subprocess.call([rubocop_path, '--auto-correct', temp_dir + '/c.rb'])

          with open(temp_dir + '/c.rb', encoding='utf-8') as f:
            output = f.read()

        finally:
          if output:
              s = re.sub(r"\n$", '', output)

          shutil.rmtree(temp_dir)
        # End Rubocop --------------------------

        self.view.replace(edit, region, s)

        sublime.status_message('Pretty Ruby | Format: Done!')
