import os
import ftplib
import contextlib


class Ymloperations:

    def download(self):
        with contextlib.suppress(FileNotFoundError):
            os.remove('trainer/trainer.yml')
            path = '/faceoff'
            filename = 'trainer.yml'

            ftp = ftplib.FTP("ftp.ninads.com")
            ftp.login("ninads", "ratedrko.123")
            ftp.cwd(path)
            ftp.retrbinary("RETR " + filename, open('trainer/' + filename, 'wb').write)
            ftp.quit()

    def upload(self):
        IP = "ftp.ninads.com"
        path_file1 = "trainer/trainer.yml"
        UID = "ninads"
        PSW = "ratedrko.123"
        ftp = ftplib.FTP(IP)
        ftp.login(UID, PSW)
        ftp.cwd("/faceoff")
        with open(path_file1, 'rb') as myfile:
            ftp.storlines('STOR ' + 'trainer.yml', myfile)


