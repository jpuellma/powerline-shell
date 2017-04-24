"""
This has been heavily modified by jpuellma
"""
import os

ELLIPSIS = u'\u2026'


def replace_home_dir(cwd):
    home = os.getenv('HOME')
    if cwd.startswith(home):
        return '~' + cwd[len(home):]
    return cwd


def split_path_into_names(cwd):
    names = cwd.split(os.sep)

    if names[0] == '':
        names = names[1:]

    if not names[0]:
        return ['/']

    return names


def requires_special_home_display(name):
    """Returns true if the given directory name matches the home indicator and
    the chosen theme should use a special home indicator display."""
    return (name == '~' and Color.HOME_SPECIAL_DISPLAY)


def maybe_shorten_name(powerline, name):
    """If the user has asked for each directory name to be shortened, will
    return the name up to their specified length. Otherwise returns the full
    name."""
    if powerline.args.cwd_max_dir_size:
        return name[:powerline.args.cwd_max_dir_size]
    return name


def get_fg_bg(name):
    """Returns the foreground and background color to use for the given name.
    """
    if requires_special_home_display(name):
        return (Color.HOME_FG, Color.HOME_BG,)
    return (Color.PATH_FG, Color.PATH_BG,)


def add_cwd2_segment(powerline):
    pwd = os.getenv('PWD')
    homedir = os.getenv('HOME')
    if pwd == homedir:
        powerline.append(u"\U0001F3E0 ", 255, 16)
    else:
        pwd = replace_home_dir(pwd)
        dirs = split_path_into_names(pwd)
        last_two_dirs = dirs[-2:]
        prompt_string = ELLIPSIS
        for i in last_two_dirs:
            prompt_string = prompt_string + '/' + i
        powerline.append('%s/' % (prompt_string,), 255, 16)
