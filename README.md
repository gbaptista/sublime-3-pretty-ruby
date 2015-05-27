# Pretty Ruby

Use [Ruby PP](http://ruby-doc.org/stdlib-2.0/libdoc/pp/rdoc/PP.html) and [RuboCop Autocorrect](https://github.com/bbatsov/rubocop#autocorrect) to prettify your Ruby code.

## Demos
Source:
```ruby
['Lorem', 'Ipsum', 'Dolor', 'Sit', 'Amet']

{ :lorem => "Ipsum", :dolor => 'Sit' }
```
Result:
```ruby
%w(Lorem Ipsum Dolor Sit Amet)

{ lorem: 'Ipsum', dolor: 'Sit' }
```
Source:
```ruby
[{ :lorem => "Ipsum", :dolor => 'Sit' }, { :lorem => "Ipsum", :dolor => 'Sit' }, { :lorem => "Ipsum", :dolor => 'Sit' }, { :lorem => "Ipsum", :dolor => 'Sit' }, { :lorem => "Ipsum", :dolor => 'Sit' }, { :lorem => "Ipsum", :dolor => 'Sit' }, { :lorem => "Ipsum", :dolor => 'Sit' }]
```
Result:
```ruby
[{ lorem: 'Ipsum', dolor: 'Sit' },
 { lorem: 'Ipsum', dolor: 'Sit' },
 { lorem: 'Ipsum', dolor: 'Sit' },
 { lorem: 'Ipsum', dolor: 'Sit' },
 { lorem: 'Ipsum', dolor: 'Sit' },
 { lorem: 'Ipsum', dolor: 'Sit' },
 { lorem: 'Ipsum', dolor: 'Sit' }]
```

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

#### RVM Problem (RuboCop): executable hooks
`/usr/bin/env: ruby_executable_hooks: No such file or directory`


Use `wrappers` instead of `bin`:

`User/Preferences.sublime-settings`:
```python
//  which rubocop
// "rubocop_path": "/home/user/.rvm/gems/ruby-2.2.2/bin/rubocop"
"rubocop_path": "/home/user/.rvm/gems/ruby-2.2.2/wrappers/rubocop"
```
