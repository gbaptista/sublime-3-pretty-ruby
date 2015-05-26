import sublime, sublime_plugin, re, tempfile, shutil
from subprocess import Popen, PIPE, STDOUT

class PrettyRubyFormat(sublime_plugin.TextCommand):
  def run(self, edit, args=[]):
    ruby_path    = self.load_ruby_path()
    rubocop_path = self.load_rubocop_path()

    for region in self.view.sel():
      if not region.empty():

        original_source = self.view.substr(region)

        source = original_source

        rubocop_source = self.apply_rubocop_autocorrect(rubocop_path, source)
        pp_source      = self.apply_pp(ruby_path, rubocop_source)

        if(rubocop_source != pp_source):
          source = self.apply_rubocop_autocorrect(rubocop_path, pp_source)
        else:
          source = rubocop_source

        if(source != original_source):
          self.view.replace(edit, region, source)
          sublime.status_message('Pretty Ruby | Format: Done!')
        else:
          sublime.status_message('Pretty Ruby | Format: Nothing to do.')

  def apply_pp(self, ruby_path, source):
    output = ''

    ruby_pp_command = ''

    try:
      temp_dir = tempfile.mkdtemp()
      with open(temp_dir + '/pp.rb', mode='w', encoding='utf-8') as f:
        f.write(source)

      ruby_pp_source = "o = [eval(File.read('" + temp_dir + "/pp.rb'))]; o = o.first; raise unless [Array, Hash].include? o.class; require 'pp'; pp(o)"
      ruby_pp_command = ruby_path + ' -e "' + ruby_pp_source + '"'

      output = self.execute_system_command(ruby_pp_command, False)
    finally:
      shutil.rmtree(temp_dir)

      if output:
        return output
      else:
        print("Ruby PP Error: \n" + self.execute_system_command(ruby_pp_command))
        return source

  def apply_rubocop_autocorrect(self, rubocop_path, source):
    try:
      temp_dir = tempfile.mkdtemp()
      with open(temp_dir + '/rbcac.rb', mode='w', encoding='utf-8') as f:
        f.write(source)

      self.execute_system_command(rubocop_path + ' --auto-correct ' + temp_dir + '/rbcac.rb')

      with open(temp_dir + '/rbcac.rb', encoding='utf-8') as f:
        output = f.read()

    finally:
      shutil.rmtree(temp_dir)
      if output:
        return output
      else:
        return source

  def load_ruby_path(self):
    settings = sublime.load_settings('Preferences.sublime-settings')
    if settings.get('ruby_path'):
      return settings.get('ruby_path')
    else:
      settings = sublime.load_settings('PrettyRuby.sublime-settings')
      return settings.get('ruby_path')

  def load_rubocop_path(self):
    settings = sublime.load_settings('Preferences.sublime-settings')
    if settings.get('rubocop_path'):
      return settings.get('rubocop_path')
    else:
      settings = sublime.load_settings('PrettyRuby.sublime-settings')
      return settings.get('rubocop_path')

  def execute_system_command(self, command, return_error=True):
    if return_error:
      stderr = STDOUT
    else:
      stderr = None

    output = str(Popen(command, shell=True, close_fds=True, stderr=stderr, stdout=PIPE).stdout.read())

    not_result_message = ''

    if output:
      output = re.sub(r"^b('|\")|('|\")$", '', output)
      output = bytes(output, "utf-8").decode("unicode_escape")
      output = re.sub(r"\n$", '', output)
      if not output:
        output = not_result_message
    else:
      output = not_result_message

    return output
