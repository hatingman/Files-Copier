# Files Copier
# # # # # # # #
# autor https://github.com/hatingman


import os, shutil, ctypes

rhost = ''
user = os.getlogin()
dir = 'C:\\USERS\\{}\\DESKTOP\\'.format(user)
storage = '\\\\{}\\Users\\{}\\'.format(rhost, user)

# making shortcut
def mkshortcut(link):
    import winshell
    from win32com.client import Dispatch

    desktop = winshell.desktop()
    path = os.path.join(desktop, "Share.lnk")
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = link
    shortcut.save()

# sending email if it needed
def email(username):
    import smtplib
    user = 'username'
    subj = 'User request.'
    to = 'mail-to'
    text = 'Hello, sir!\nNeed to creat a user \'{}\' for access to DiskStation.\n\nThank you!'.format(username)
    body = '\r\n'.join((
        'From: %s' % user,
        'To: %s' % to,
        'Subject: %s' % subj,
        '',
        text
    ))
    send = smtplib.SMTP('smtp.server', 25)
    send.login(user, 'password')
    send.sendmail(user, [to], body)
    send.quit()

# making log file
def wlog(obj, storage, text):
    from datetime import datetime
    with open(storage + 'copier.log', 'a') as file:
        file.write('\n-------\n{}: file \'{}\' was {} {}'.format(str(datetime.now()), obj, text, storage))
        file.close()

# doing main job
def filesync(obj, user, storage):

    filetypes = ['.doc', '.docx', '.xls', '.xlsx', '.jpg', '.jpeg', '.pdf',
        '.png', '.bmp', '.psd', '.tiff', '.ai', '.ait', '.cdr', '.draw',
        '.PNG', '.BMP', '.PSD', '.TIFF', '.AI', '.AIT', '.CDR', '.DRAW',
        '.DOC', '.DOCX', '.XLS', '.XLSX', '.JPG', '.JPEG', '.PDF']

    for ft in filetypes:
        if obj.endswith(ft):
            try:
                head, tail = os.path.split(obj)
                directory = storage + head.split(os.sep)[-1]
                if not os.path.exists(directory):
                    os.makedirs(directory)
                rmfile = storage + '\\' + tail
                if os.path.isfile(rmfile):
                    if os.path.getmtime(obj) > os.path.getmtime(rmfile):
                        shutil.copy(obj, rmfile)
                        wlog(obj, storage, 'replaced in {}\\'.format(directory))
                    else:
                        pass
                else:
                    shutil.copy(obj, rmfile)
                    wlog(obj, storage, 'copied to {}\\'.format(directory))
            except FileNotFoundError or PermissionError:
                pass

# checking folders, call functions
def main(dir, user, storage):
    try:
        rootdir = os.listdir(dir)
    except FileNotFoundError:
        pass

    for obj in rootdir:
        if os.path.isdir(dir + obj):
            main(dir + obj + '\\', user, storage)
        elif os.path.isfile(dir + obj):
            filesync(dir + obj, user, storage)
        else:
            pass


if __name__ == '__main__':
    title = 'Files Copier'
    try:
        if os.path.isdir(storage):
            main(dir, user, storage)
            mkshortcut(storage)
            ctypes.windll.user32.MessageBoxW(0,
            'Done!\nThe files from the desktop are synchronized with the network folder.\nThe \"Share\" shortcut was created(updated) on the desktop for quick access to the archive!',
            title, 64)
        else:
            email(user)
            ctypes.windll.user32.MessageBoxW(0,
            'Aww!\nThere is no network folder for the user \'{}\' in the storage!\nTo the system administrator was sent a request letter to add.\nThanks!'.format(user),
            title, 64)
    except PermissionError:
        ctypes.windll.user32.MessageBoxW(0,
        'Oops!\nThere is no access to the user\'s network folder!\nContact your System Administrator for help!\nThanks!'.format(user),
        title, 16)
