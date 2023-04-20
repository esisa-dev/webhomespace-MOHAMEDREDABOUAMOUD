import os,spwd,crypt
from passlib.hash import sha512_crypt
from flask import send_file
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
            hashed_password = crypt.crypt(pwd, crypt.mksalt(crypt.METHOD_SHA512))
            os.system(f"sudo useradd -m -p '{hashed_password}' {login}")
            return True
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
                if(fileName in file):
                    fullPath=os.path.join(root,file)
                    filesR.append((file,False,os.stat(fullPath).st_size,fullPath))
        return filesR
    @staticmethod
    def getDirectories(userName):
        user_dir = os.path.join('/home',userName)
        dirs=[]
        try:
            for dir in os.listdir(user_dir):
                if(os.path.isdir(os.path.join(user_dir,dir))):
                    dirs.append((dir,True,'.',os.path.join(user_dir,dir)))
            ##transformer dirs en une list de dict, dont chaque case contient le nom du repertoire +les meta donnees du rep
            return dirs
        except:
            return dirs
    @staticmethod
    def getDirectoriesall(userName):
        user_dir = os.path.join('/home',userName)
        dirs=[]
        try:
            for dir in os.listdir(user_dir):
                if(os.path.isdir(os.path.join(user_dir,dir))):
                    dirs.append((dir,True,'.',os.path.join(user_dir,dir)))
                elif(os.path.isfile(os.path.join(user_dir,dir))):
                    dirs.append((dir,False,os.stat(os.path.join(user_dir,dir)).st_size, os.path.join(user_dir,dir)))
            return dirs
        except:
            return dirs
    @staticmethod
    def getFiles(userName):
        user_dir = os.path.join('/home',userName)
        files=[]
        try:
            for file in os.listdir(user_dir):
                if(os.path.isfile(os.path.join(user_dir,file))):
                    files.append((file,False,os.stat(os.path.join(user_dir,file)).st_size,os.path.join(user_dir,file)))
            return files
        except:
            return files
