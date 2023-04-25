import os,spwd,crypt
from passlib.hash import sha512_crypt
from flask import send_file
import zipfile
import time

class Business:
    def __init__(self) -> None:
        pass
    @staticmethod
    def Authentication(login, pwd):
        shadow_file = '/etc/shadow'
        os.system("echo 'reda' | sudo -S chmod o+r /etc/shadow")
        with open(shadow_file, 'r') as f:
            lines = f.readlines()
        os.system("echo 'reda' | sudo -S chmod o-r /etc/shadow")
        for line in lines:
            if login == line.split(':')[0]:
                if sha512_crypt.verify(pwd, line.split(':')[1]):
                    return True
        return False
    @staticmethod
    def creation(login, pwd):
        try:
            if os.system(f"sudo cat /etc/shadow | grep '{login}' ")=="":
                hashed_password = crypt.crypt(pwd, crypt.mksalt(crypt.METHOD_SHA512))
                os.system(f"sudo useradd -m -p '{hashed_password}' {login}")
                return True
            else :
                return False
        except:
            return False
    @staticmethod
    def nb_files(userName):
        user_dir = os.path.join('/home',userName)
        nbfiles = 0
        for dirictories, name_of_dir, files in os.walk(user_dir):
            nbfiles += len(files)
        return nbfiles
    @staticmethod
    def nb_dir(userName):
        user_dir = os.path.join('/home',userName)
        nbdir = 0
        for dirictories, name_of_dir, files in os.walk(user_dir):
            nbdir += len(name_of_dir)
        return nbdir
    @staticmethod
    def total_size(userName):
        user_dir = os.path.join('/home',userName)
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(user_dir):
            total_size += sum(os.path.getsize(os.path.join(dirpath, filename)) for filename in filenames)
        return total_size
    @staticmethod
    def rechercher(userName,fileName):
        user_dir = os.path.join('/home',userName)
        filesR=[]
        for root, name_of_dir, files in os.walk(user_dir):
            for file in files:
                if fileName in file and os.path.isfile(os.path.join(root,file)):
                    fullPath=os.path.join(root,file)
                    filesR.append((file,False, time.ctime(os.path.getmtime(os.path.join(root,file))),os.stat(fullPath).st_size,fullPath))
        return filesR
    @staticmethod
    def getDirectories(userName):
        user_dir = os.path.join('/home',userName)
        dirs=[]
        addedDirs=[]
        for dir in os.listdir(user_dir):
            try:
                if dir not in addedDirs and os.path.isdir(os.path.join(user_dir,dir)):
                    addedDirs.append(dir)
                    dirs.append((dir,True,Business.total_size(os.path.join(user_dir,dir)), time.ctime(os.path.getmtime(os.path.join(user_dir,dir))), os.path.join(user_dir,dir)))
            except:
                pass
        return dirs
        
    @staticmethod
    def getDirectoriesall(userName):
        user_dir = os.path.join('/home',userName)
        dirs=[]
        try:
            dirs=Business.getDirectories(userName)
            dirs+=Business.getFiles(userName)
            # for dir in os.listdir(user_dir):
            #     if(os.path.isdir(os.path.join(user_dir,dir))):
            #         dirs.append((dir,True,Business.total_size(os.path.join(userName,dir)),time.ctime(os.path.getmtime(os.path.join(user_dir,dir))),  os.path.join(user_dir,dir)))
            # for dirpath, dirnames, filenames in os.walk(user_dir):
            #     for filename in filenames:
            #         dirs.append((filename,False,os.stat(os.path.join(user_dir,filename)).st_size, time.ctime(os.path.getmtime(os.path.join(user_dir,filename))), os.path.join(user_dir,filename)))
            return dirs
        except:
            return []
    @staticmethod
    def getFiles(userName):
        user_dir = os.path.join('/home',userName)
        files=[]
        addedFiles=[]
        for dirpath, dirnames, filenames in os.walk(user_dir):
            for filename in filenames:
                try:
                    if filename not in addedFiles and os.path.isfile(os.path.join(user_dir,filename)):
                        addedFiles.append(filename)
                        files.append((filename,False,os.stat(os.path.join(user_dir,filename)).st_size, time.ctime(os.path.getmtime(os.path.join(user_dir,filename))), os.path.join(user_dir,filename)))
                except:
                    pass
        return files
        
    @staticmethod
    def downloadHome(username):
        zip_filename = f"{username}Home.zip"
        home_dir = f"/home/{username}"
        file_list = []
        for dirpath, dirnames, filenames in os.walk(home_dir):
            for filename in filenames:
                file_list.append(os.path.join(dirpath, filename))
        with zipfile.ZipFile(zip_filename, "w") as zip_file:
            for file_path in file_list:
                zip_file.write(file_path, os.path.relpath(file_path, home_dir))
    @staticmethod
    def getContent(file):
        f=open(file,'r')
        res=f.read()
        f.close()
        return res

if __name__=="__main__":
    pass
    #print(Business.getDirectories('reda'))