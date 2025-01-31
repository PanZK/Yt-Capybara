# -*- encoding: utf-8 -*-
'''
@Time    :   2025/01/13 17:52:43
@File    :   cmdOperate.py
@Software:   VSCode
@Author  :   PPPPAN 
@Version :   0.1.0
@Contact :   for_freedom_x64@live.com
'''
import subprocess, os, platform


class CmdOperate():
    haveYt_dlp, haveFfmpeg = False, False
    yt_dlpVersion, ffmpegVersion = None, None
    yt_dlpExe, ffmpegExe = 'yt-dlp', 'ffmpeg'

    def __init__(self):
        if platform.system() == 'Darwin':
            pass
            # Check if has installed yt-dlp.
            # self.testpythonPathsList = self.getPythonPaths()
            pythonPathsList = self.getPythonPaths()
            # pythonPathsList = ['/System/Library/Frameworks/Python.framework/Versions/3.10/bin', '/usr/local/Cellar/python@3.10/3.10.2/bin', '/Library/Frameworks/Python.framework/Versions/3.10/bin']
            exe = self.findExecutable('yt-dlp', pythonPathsList)
            # exe = self.findExecutable('yt-dlp')
            if exe != None:
                self.haveYt_dlp = True
                self.yt_dlpExe = exe
                yt_dlpCmd = exe + ' --version'
                self.yt_dlpVersion = self.runCommand(yt_dlpCmd).strip()

            # Check if has installed ffmpeg.
            exe = self.findExecutable('ffmpeg')
            if exe != None:
                self.haveFfmpeg = True
                self.ffmpegExe = exe
                ffmpegCmd = exe + ' -version'
                self.ffmpegVersion = self.runCommand(ffmpegCmd).split()[2]
        elif platform.system() == 'Linux':
            # Check if has installed yt-dlp.
            yt_dlpCmd = 'yt-dlp --version'
            result = self.runCommand(yt_dlpCmd)
            if result != '':
                self.haveYt_dlp = True
                self.yt_dlpVersion = result.strip()

            ffmpegCmd = 'ffmpeg -version'
            result = self.runCommand(ffmpegCmd)
            if result != '':
                self.haveFfmpeg = True
                self.ffmpegVersion = result.split()[2]
        elif platform.system() == 'Windows':
            pass

    def findExecutable(self, executableName:str, givenPaths:list=None):
        """
        动态查找可执行文件路径
        :param executable_name: 可执行文件名，例如 'yt-dlp' 或 'ffmpeg'
        :param commonPaths: 常见的可能路径列表
        :return: 可执行文件路径，或 None 如果未找到
        """
        # 尝试从系统 PATH 中查找
        # execPath = shutil.which(executableName)
        # if execPath:
        #     return execPath

        # 在 PATH 和常见路径检查
        currentPaths = [
                "/usr/local/bin",
                "/opt/homebrew/bin",
                os.path.expanduser("~/.local/bin")
                # "/Library/Frameworks/Python.framework/Versions/3.10/bin",
            ]
        if givenPaths is None:
            givenPaths = currentPaths
        else:
            givenPaths = givenPaths + currentPaths
        # if executableName == 'yt-dlp':
        #     self.testpythonPathsList = givenPaths
        #     print(givenPaths)

        for path in givenPaths:
            execPath = os.path.join(path, executableName)
            if os.path.isfile(execPath) and os.access(execPath, os.X_OK):  # 检查是否存在且可执行
                # if executableName == 'yt-dlp':
                #     self.testpythonPathsList = [path]
                #     print(path)
                return execPath
        # 如果找不到，则返回 None
        return None

    def getPythonPaths(self) -> list:
        cmdList = ['/usr/local/bin/python3 --version', 'python3 --version']
        for cmd in cmdList:
            result = self.runCommand(cmd)
            if result == '':
                cmd = 'python --version'
                result = self.runCommand(cmd)
                if result == '':
                    return None
                else:
                    break
            else:
                break
        fullVersion = result.strip().split(' ')[1]
        version = fullVersion.split('.')
        version = version[0] + '.' + version[1]
        sysPython = f'/System/Library/Frameworks/Python.framework/Versions/{version}/bin'
        brewPath = f'/usr/local/Cellar/python@{version}/{fullVersion}/bin'
        userPath = f'/Library/Frameworks/Python.framework/Versions/{version}/bin'
        # print(fullVersion)
        # print(version)
        # print([sysPython, brewPath, userPath])
        return [sysPython, brewPath, userPath]

    def runCommand(self, cmd:str) -> str:
        terminalProcess = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return terminalProcess.stdout.readline().decode('utf-8')

    def getYt_dlpVersion(self):
        return self.yt_dlpVersion

    def getFfmpegVersion(self):
        return self.ffmpegVersion


if __name__ == '__main__':
    cmdOperate = CmdOperate()
    print(cmdOperate.haveYt_dlp)
    print(cmdOperate.haveFfmpeg)
    print(cmdOperate.getYt_dlpVersion())
    print(cmdOperate.getFfmpegVersion())