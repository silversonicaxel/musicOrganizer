'''
class about operations on files
'''

import os
import shutil
import mimetypes
import getpass
import platform

class CFileSystemOperations(object):
    _N_POS_ORIGINAL_FILE = 0
    _N_POS_ARTIST = 1
    _N_POS_YEAR = 2
    _N_POS_ALBUM = 3
    _N_POS_NUMDISC = 4
    _N_POS_NUMTRACK = 5
    _N_POS_TITLE = 6
    _N_POS_EXTENSION = 7
    
    bCheckSourceDirectoryOnlySongs = True
    
    def __init__(self, sMusicLibrary):
        self.sMusicLibrary = sMusicLibrary
        
    def checkSourceDirectoryOnlySongs(self):
        return self.bCheckSourceDirectoryOnlySongs
    
    def readMp3Info(self, sMp3File):
        '''
        function to get informations about an mp3 file
        http://nullege.com/codes/search/mutagen.mp3
        http://nullege.com/codes/search/eyeD3
        '''
        from mutagen.mp3 import MP3, error as MP3Error, delete, MPEGInfo, EasyMP3
        from mutagen.easyid3 import EasyID3
        
        hMp3File = MP3(sMp3File, ID3=EasyID3)
        sMp3Artist = hMp3File['artist'][0]
        nMp3Year = hMp3File['date'][0]
        sMp3Album = hMp3File['album'][0]
        aMp3Track = hMp3File['tracknumber'][0].split("/")
        nMp3Track = str(aMp3Track[0]).rjust(2, '0')
        try:
            aMp3Disc = hMp3File['discnumber'][0].split("/")
            nMp3Disc = str(aMp3Disc[0])
        except:
            nMp3Disc = '1'
        sMp3Title = hMp3File['title'][0]
        aMp3DataSong = sMp3File, sMp3Artist, nMp3Year, sMp3Album, nMp3Disc, nMp3Track, sMp3Title, 'mp3'
        return aMp3DataSong
    
    
    def readM4aInfo(self, sM4aFile):
        '''
        function to get informations about an m4a file
        http://nullege.com/codes/search/mutagen.m4a
        '''
        from mutagen.m4a import M4A, Atom, Atoms, M4ATags, M4AInfo, delete, M4ACover, M4AMetadataError

        hM4aFile = M4A(sM4aFile)
        sM4aArtist = hM4aFile.tags['\xa9ART']
        nM4aYear = hM4aFile.tags['\xa9day']
        sM4aAlbum = hM4aFile.tags['\xa9alb']
        aM4aTrack = hM4aFile.tags['trkn']
        nM4aTrack = str(aM4aTrack[0]).rjust(2, '0')
        try:
            aM4aDisc = hM4aFile.tags['disk']
            nM4aDisc = str(aM4aDisc[0])
        except:
            nM4aDisc = '1'
        sM4aTitle = hM4aFile.tags['\xa9nam']
        aM4aDataSong = sM4aFile, sM4aArtist, nM4aYear, sM4aAlbum, nM4aDisc, nM4aTrack, sM4aTitle, 'm4a'
        return aM4aDataSong
    
    
    def readDirectorySongs(self, sDirectory):
        '''
        read directory
        '''
        try:
            aListFiles = os.listdir(sDirectory)
            aListSongs = []
            for sFile in aListFiles:
                if sFile != '.DS_Store':
                    aListSongs.append(sDirectory + sFile)
        except:
            raise Exception()     
        return aListSongs
    
    
    def getDataSongs(self, aSongFiles):
        '''
        get directory artist and album if consistent data
        same artist, same album, same year
        '''
        dDataSongs = []

        for sSongFile in aSongFiles:
            if os.path.isfile(sSongFile):
                #understanding file extension
                hGuessType = mimetypes.guess_type(sSongFile)
                sExtension = mimetypes.guess_extension(hGuessType[0], False)
                sExtension = sExtension.replace(".", "")
                
                if sExtension.lower() == 'mp3':
                    aDataSong = self.readMp3Info(sSongFile)
                    dDataSongs.append(aDataSong)
                elif sExtension.lower() == 'm4a':
                    aDataSong = self.readM4aInfo(sSongFile)
                    dDataSongs.append(aDataSong)
        return dDataSongs
        

    def manageDirectorySongs(self, sDirectorySongs, aDataSongs):
        '''
        rename the songs and delete eventually the dir if empty
        '''
        self.bCheckSourceDirectoryOnlySongs = True
        #for each song check...
        for aSong in aDataSongs:
            sBaseDirSong = self.sMusicLibrary + aSong[self._N_POS_ARTIST] + "/" + aSong[self._N_POS_YEAR] + " - " + aSong[self._N_POS_ALBUM] + "/"
            sBaseFileSong = aSong[self._N_POS_NUMDISC] + "." + aSong[self._N_POS_NUMTRACK] + " " + aSong[self._N_POS_TITLE] + "." + aSong[self._N_POS_EXTENSION]
            
            #check destination directory
            if not os.path.exists(sBaseDirSong):
                os.makedirs(sBaseDirSong)
                    
            #renames
            os.renames(aSong[self._N_POS_ORIGINAL_FILE], sBaseDirSong + sBaseFileSong)
            
            #check source directory
            if os.path.samefile(sDirectorySongs, sBaseDirSong):
                self.bCheckSourceDirectoryOnlySongs = False

        #remove direcotory if empty
        if self.bCheckSourceDirectoryOnlySongs:
            shutil.rmtree(sDirectorySongs)
        return True
    
    def getRepositoryDirectory():
        '''
        static function to get the possible music repository directory
        '''
        sUsername = getpass.getuser()
        sIdOs = platform.platform().lower()
        sRepositoryDirectory = ""
        if 'darwin' in sIdOs or 'os' in sIdOs:
            sRepositoryDirectory = "/Users/" + sUsername + "/Music/iTunes/iTunes Music/"
        elif 'win' in sIdOs:
            sRepositoryDirectory = "C:/Users/" + sUsername + "/Music/"
        elif 'linux' in sIdOs:
            sRepositoryDirectory = "/home/" + sUsername + "/music/"
            
        return sRepositoryDirectory            
    getRepositoryDirectory = staticmethod(getRepositoryDirectory)