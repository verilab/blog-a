import os


def apply_theme(theme):
    theme_dir = os.path.join('themes', theme)
    if not os.path.isdir(theme_dir):
        print('There seems no "themes" directory existing.')
        return

    template_dir = os.path.join(theme_dir, 'templates')
    if not os.path.isdir(template_dir):
        print('The theme "'
              + theme + '" is invalid, because there is no "templates" subdirectory in this theme.')
        return

    applied_template_dir = 'templates'
    applied_static_dir = 'static'

    # make symlinks for template files
    print('Applying template files...', end='')
    if not os.path.exists(applied_template_dir):
        os.mkdir(applied_template_dir)
    file_list = os.listdir(template_dir)
    for file in file_list:
        rel_path = os.path.join('..', template_dir, file)
        symlink_path = os.path.join(applied_template_dir, file)
        if os.path.lexists(symlink_path):
            os.remove(symlink_path)
        os.symlink(rel_path, symlink_path, os.path.isdir(rel_path))
    print('OK')

    # make symlinks for static files
    print('Applying static files...', end='')
    static_dir = os.path.join(theme_dir, 'static')
    if os.path.isdir(static_dir):
        if not os.path.exists(applied_static_dir):
            os.mkdir(applied_static_dir)
        file_list = os.listdir(static_dir)
        for file in file_list:
            rel_path = os.path.join('..', static_dir, file)
            symlink_path = os.path.join(applied_static_dir, file)
            if os.path.lexists(symlink_path):
                os.remove(symlink_path)
            os.symlink(rel_path, symlink_path, os.path.isdir(rel_path))
    print('OK')

    print('Successfully applied theme "' + theme + '"')
