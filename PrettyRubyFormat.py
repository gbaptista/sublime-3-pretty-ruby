import sublime, sublime_plugin, re, tempfile, shutil
from subprocess import Popen, PIPE, STDOUT

class PrettyRubyFormat(sublime_plugin.TextCommand):
  def run(self, edit, args=[]):
    ruby_path    = self.load_ruby_path()
    rubocop_path = self.load_rubocop_path()

    if(ruby_path == 'ruby'):
      if not self.execute_system_command('which ruby', False):
        sublime.error_message("Pretty Ruby\n\nWarning: 'ruby' command not found.\n\nRun the following command to discover your ruby path:\n\nwhich ruby\n\nMore info:\nhttps://github.com/gbaptista/sublime-3-pretty-ruby#custom-rubyrubocop-path")

    if(rubocop_path == 'rubocop'):
      if not self.execute_system_command('which rubocop', False):
        sublime.error_message("Pretty Ruby\n\nWarning: 'rubocop' command not found.\n\nRun the following command to discover your rubocop path:\n\nwhich rubocop\n\nMore info:\nhttps://github.com/gbaptista/sublime-3-pretty-ruby#custom-rubyrubocop-path")

    for region in self.view.sel():
      if not region.empty():

        original_source = self.view.substr(region)

        source = original_source

        rubocop_source = self.apply_rubocop_autocorrect(rubocop_path, source, True)
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

    prepared_source = source.replace('"', '\\"')
    prepared_source = prepared_source.replace('\\\\"', '\\\\\\"')

    ruby_pp_source = "o = [" + prepared_source + "]; raise unless o.size == 1; o = o.first; raise unless [Array, Hash].include? o.class; require 'pp'; pp(o)"
    ruby_pp_command = ruby_path + ' -e "' + ruby_pp_source + '"'

    output = self.execute_system_command(ruby_pp_command, False)

    if output:
      return output
    else:
      if(re.search('/wrappers/', ruby_path)):
        sublime.error_message("Pretty Ruby\n\nWarning: Don't use wrappers for ruby bin.\n\nWrong:\n" + ruby_path + "\n\nCorrect:\n" + ruby_path.replace('/wrappers/', '/bin/') + "\n\nMore info:\nhttps://github.com/gbaptista/sublime-3-pretty-ruby#ruby-problem-rvm-wrappersruby-not-found")
      print("\nPretty Ruby | Ruby PP Warning: \n[" + ruby_path + "]\n" + self.execute_system_command(ruby_pp_command))
      return source

  def apply_rubocop_autocorrect(self, rubocop_path, source, show_error=False):
    try:
      temp_dir = tempfile.mkdtemp()
      with open(temp_dir + '/rbcac.rb', mode='w', encoding='utf-8') as f:
        f.write(source)

      rubocop_output = self.execute_system_command(rubocop_path + ' --auto-correct ' + temp_dir + '/rbcac.rb')

      with open(temp_dir + '/rbcac.rb', encoding='utf-8') as f:
        output = f.read()

    finally:
      shutil.rmtree(temp_dir)

      if(show_error and not re.search('1 file inspected', rubocop_output)):
        if(re.search('ruby_executable_hooks', rubocop_output) and re.search('rvm', rubocop_path) and re.search('bin', rubocop_path)):
          sublime.error_message("Pretty Ruby\n\nWarning:\nRVM Problem (RuboCop): executable hooks\n\nUse wrappers instead of bin:\n\nWrong:\n" + rubocop_path + "\n\nCorrect:\n" + rubocop_path.replace('/bin/', '/wrappers/') + "\n\nMore info:\nhttps://github.com/gbaptista/sublime-3-pretty-ruby#rubocop-problem-rvm-executable-hooks")
        print("\nPretty Ruby | RuboCop Warning: \n[" + rubocop_path + "]\n" + rubocop_output)

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
