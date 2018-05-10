import Gui
import os
import ftplib
import contextlib


# with contextlib.suppress(FileNotFoundError):
#     os.remove('trainer/trainer.yml')
#
# path = '/faceoff'
# filename = 'trainer.yml'
#
# ftp = ftplib.FTP("ftp.ninads.com")
# ftp.login("ninads", "ratedrko.123")
# ftp.cwd(path)
# ftp.retrbinary("RETR " + filename, open('trainer/'+filename, 'wb').write)
# ftp.quit()

st = Gui.Gui()
