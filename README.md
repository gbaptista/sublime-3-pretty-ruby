# Pretty Ruby

Use [Ruby PP](http://ruby-doc.org/stdlib-2.0/libdoc/pp/rdoc/PP.html) and [RuboCop Autocorrect](https://github.com/bbatsov/rubocop#autocorrect) to indent, format and prettify your Ruby code.

![Demo: Pretty Ruby](https://raw.githubusercontent.com/gbaptista/sublime-3-pretty-ruby/master/demo.gif)

### Dependencies:

* [Ruby](https://www.ruby-lang.org/)
* [RuboCop](https://github.com/bbatsov/rubocop)

`gem install rubocop`

### Command Palette

Pretty Ruby: Format `pretty_ruby_format`

### Default Shortcuts

* Linux: _ctrl + shift + r + p_ `["ctrl+shift+r", "ctrl+shift+p"]`
* Mac: _shift + super + r + p_ `["shift+super+r", "shift+super+p"]`
* Windows: _ctrl + shift + r + p_ `["ctrl+shift+r", "ctrl+shift+p"]`

### Custom Shortcuts
`User/Default (Linux).sublime-keymap`:
```python
{ "keys": ["ctrl+shift+h"], "command": "pretty_ruby_format" }
```

### Custom Ruby/RuboCop path:
`User/Preferences.sublime-settings`:
```python
//  which ruby
"ruby_path": "/home/user/.rvm/rubies/ruby-2.2.2/bin/ruby",

//  which rubocop
"rubocop_path": "/home/user/.rvm/gems/ruby-2.2.2/bin/rubocop"
```

#### RuboCop Problem (RVM): executable hooks
`/usr/bin/env: ruby_executable_hooks: No such file or directory`

Use `wrappers` instead of `bin`:

`User/Preferences.sublime-settings`:
```python
//  which rubocop
// "rubocop_path": "/home/user/.rvm/gems/ruby-2.2.2/bin/rubocop" // wrong
"rubocop_path": "/home/user/.rvm/gems/ruby-2.2.2/wrappers/rubocop" // correct
```

#### Ruby Problem (RVM): /wrappers/ruby: not found
`/bin/sh: 1: /home/user/.rvm/rubies/ruby-2.2.2/wrappers/ruby: not found`

Don't use `wrappers` for ruby bin.

`User/Preferences.sublime-settings`:
```python
//  which rubocop
// "ruby_path": "/home/user/.rvm/rubies/ruby-2.2.2/wrappers/ruby" // wrong
"ruby_path": "/home/user/.rvm/rubies/ruby-2.2.2/bin/ruby" // correct
```
