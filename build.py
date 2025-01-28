# -*- encoding: utf-8 -*-
'''
@Time    :   2025/01/13 18:21:43
@File    :   Yt_Capybara.py
@Software:   VSCode
@Author  :   PPPPAN 
@Version :   0.1.0
@Contact :   for_freedom_x64@live.com
'''

import os, platform, shutil

if __name__ == '__main__':
    if platform.system() == 'Darwin':
        print('当前系统为: MacOS')
        flag = input('输入1: 使用 Nuitka 编译程序为app包，并压缩为dmg发布。\n输入2: 使用 PyInstaller 打包程序app包，并压缩为dmg发布。\n')
        if flag == '1':
            print('......使用 Nuitka 编译程序为app包，并压缩为dmg......')
            shutil.rmtree('dist/Yt-Capybara.MacOS.Nuitka', True)
            cmd = 'python -m nuitka \
                --macos-create-app-bundle \
                --nofollow-import-to=numpy,scipy,PIL,PySide6.QtPrintSupport,cryptography,lib-dynload,libcrypto,libcrypto.1.1,PySide6.QtDBus,PySide6.QtPdf,PySide6.QtPdfWidgets,libncursesw,libncursesw.5,libssl,libssl.1.1,PySide6.QtNetwork,PySide6.QtNetworkAuth,PySide6.qt-plugins,QtNetwork,QtPdf,QtPdfWidgets,QtDBus \
                --lto=yes \
                --enable-plugin=pyside6 \
                --include-data-dir=icons=icons \
                --macos-app-ico=icons/capybara.icns \
                --output-dir=dist/Yt-Capybara.MacOS.Nuitka \
                Yt-Capybara.py'
            os.system(cmd)
            shutil.copytree('icons', 'dist/Yt-Capybara.MacOS.Nuitka/Yt-Capybara.app/Contents/Resources/icons')
            shutil.copy('bale/Info.plist', 'dist/Yt-Capybara.MacOS.Nuitka/Yt-Capybara.app/Contents/Info.plist')
            # os.system('SetFile -a C dist/Yt-Capybara.MacOS.Nuitka/Yt-Capybara.app')
            shutil.copytree('dist/Yt-Capybara.MacOS.Nuitka/Yt-Capybara.app', 'dist/Yt-Capybara.MacOS.Nuitka/Yt-Capybara/Yt-Capybara.app')
            shutil.rmtree('dist/Yt-Capybara.MacOS.Nuitka/Yt-Capybara.build', True)
            shutil.rmtree('dist/Yt-Capybara.MacOS.Nuitka/Yt-Capybara.dist', True)
            os.chdir("dist/Yt-Capybara.MacOS.Nuitka")
            cmd = 'create-dmg \
                --volname "Yt-Capybara" \
                --background "../../bale/dmg-background-144dpi.png" \
                --volicon "../../icons/capybara.icns" \
                --window-pos 200 120 \
                --window-size 650 400 \
                --icon-size 140 \
                --icon "Yt-Capybara.app" 175 160 \
                --hide-extension "Yt-Capybara.app" \
                --app-drop-link 475 160 \
                "Yt-Capybara.dmg" \
                "Yt-Capybara.app"'
            os.system(cmd)
            shutil.rmtree('Yt-Capybara', True)
            print('......使用 Nuitka 编译程序为app包，并压缩为dmg......完成')

        elif flag == '2':
            print('......使用 PyInstaller 打包程序app包，并压缩为dmg......')
            shutil.rmtree('build', True)
            shutil.rmtree('dist/Yt-Capybara.MacOS.PyInstaller', True)
            # Original cmd = 'pyinstaller -F -w -i icons/capybara.ico Yt-Capybara.py'
            cmd = 'pyinstaller bale/Yt-Capybara.MacOS.spec'
            os.system(cmd)
            shutil.copytree('dist/Yt-Capybara.app', 'dist/Yt-Capybara.MacOS.PyInstaller/Yt-Capybara/Yt-Capybara.app')
            shutil.move('dist/Yt-Capybara.app','dist/Yt-Capybara.MacOS.PyInstaller/Yt-Capybara.app' )
            os.remove('dist/Yt-Capybara')
            os.chdir("dist/Yt-Capybara.MacOS.PyInstaller")
            cmd = 'create-dmg \
                --volname "Yt-Capybara" \
                --background "../../bale/dmg-background-144dpi.png" \
                --volicon "../../icons/capybara.icns" \
                --window-pos 200 120 \
                --window-size 650 400 \
                --icon-size 140 \
                --icon "Yt-Capybara.app" 175 160 \
                --hide-extension "Yt-Capybara.app" \
                --app-drop-link 475 160 \
                "Yt-Capybara.dmg" \
                "Yt-Capybara.app"'
            os.system(cmd)
            shutil.rmtree('Yt-Capybara', True)
            print('......使用 PyInstaller 打包程序app包，并压缩为dmg......完成')

        else:
            print('error')
    elif platform.system() == 'Linux':
        print('当前系统为:Linux')
        flag = input('输入1: 使用 Nuitka 编译程序为 单文件和文件夹。\n输入2: 使用 PyInstaller 仅打包为 单文件程序。\n输入3: 使用 PyInstaller 打包为 文件夹。\n')
        if flag == '1':
            print('......使用 Nuitka 编译程序为单文件和文件夹......')
            shutil.rmtree('dist/Yt-Capybara.Linux.Nuitka.folder', True)
            shutil.rmtree('dist/Yt-Capybara.Linux.Nuitka.onefile', True)
            cmd = 'python -m nuitka --onefile --nofollow-import-to=numpy,scipy,PIL,PySide6.QtPrintSupport,cryptography,lib-dynload,libcrypto,libcrypto.1.1,PySide6.QtDBus,PySide6.QtPdf,PySide6.QtPdfWidgets,libncursesw,libncursesw.5,libssl,libssl.1.1,PySide6.QtNetwork,PySide6.QtNetworkAuth,PySide6.qt-plugins --lto=yes --linux-icon=icons/capybara.png --enable-plugin=pyside6 --include-data-dir=icons=icons --output-dir=dist Yt-Capybara.py'
            os.system(cmd)
            os.mkdir("dist/Yt-Capybara.Linux.Nuitka.folder")
            shutil.move('dist/Yt-Capybara.dist', 'dist/Yt-Capybara.Linux.Nuitka.folder/Yt-Capybara')
            shutil.copy('bale/make.Yt-Capybara.Linux.sh', 'dist/Yt-Capybara.Linux.Nuitka.folder/make.sh')
            shutil.copy('bale/Yt-Capybara.Nuitka.desktop', 'dist/Yt-Capybara.Linux.Nuitka.folder/Yt-Capybara.desktop')
            shutil.copytree('icons', 'dist/Yt-Capybara.Linux.Nuitka.onefile/Yt-Capybara/icons')
            shutil.move('dist/Yt-Capybara.bin', 'dist/Yt-Capybara.Linux.Nuitka.onefile/Yt-Capybara/Yt-Capybara.bin')
            shutil.copy('bale/make.Yt-Capybara.Linux.sh', 'dist/Yt-Capybara.Linux.Nuitka.onefile/make.sh')
            shutil.copy('bale/Yt-Capybara.Nuitka.desktop', 'dist/Yt-Capybara.Linux.Nuitka.onefile/Yt-Capybara.desktop')
            shutil.rmtree('dist/Yt-Capybara.onefile-build', True)
            shutil.rmtree('dist/Yt-Capybara.build', True)
            print('......使用 Nuitka 编译程序为单文件和文件夹......完成')

        elif flag == '2':
            print('......使用 PyInstaller 仅打包为 单文件 程序......')
            shutil.rmtree('build', True)
            shutil.rmtree('dist/Yt-Capybara.Linux.PyInstaller.onefile', True)
            cmd = 'pyinstaller bale/Yt-Capybara.Linux.onefile.spec'
            # Original cmd = 'pyinstaller -F -w Yt-Capybara.py'
            os.system(cmd)
            shutil.copytree('icons', 'dist/Yt-Capybara.Linux.PyInstaller.onefile/Yt-Capybara/icons')
            shutil.move('dist/Yt-Capybara', 'dist/Yt-Capybara.Linux.PyInstaller.onefile/Yt-Capybara')
            shutil.copy('bale/make.Yt-Capybara.Linux.sh', 'dist/Yt-Capybara.Linux.PyInstaller.onefile/make.sh')
            shutil.copy('bale/Yt-Capybara.PyInstaller.desktop', 'dist/Yt-Capybara.Linux.PyInstaller.onefile/Yt-Capybara.desktop')
            print('......使用 PyInstaller 仅打包为 单文件 程序......完成')

        elif flag == '3':
            print('......使用 PyInstaller 打包为 文件夹......')
            shutil.rmtree('build', True)
            shutil.rmtree('dist/Yt-Capybara.Linux.PyInstaller.folder', True)
            # Original cmd = 'pyinstaller --onedir --noconsole --contents-directory . Yt-Capybara.py'
            cmd = 'pyinstaller bale/Yt-Capybara.Linux.folder.spec'
            os.system(cmd)
            os.mkdir("dist/Yt-Capybara.Linux.PyInstaller.folder")
            shutil.move('dist/Yt-Capybara', 'dist/Yt-Capybara.Linux.PyInstaller.folder/Yt-Capybara')
            shutil.copy('bale/make.Yt-Capybara.Linux.sh', 'dist/Yt-Capybara.Linux.PyInstaller.folder/make.sh')
            shutil.copy('bale/Yt-Capybara.PyInstaller.desktop', 'dist/Yt-Capybara.Linux.PyInstaller.folder/Yt-Capybara.desktop')
            print('......使用 PyInstaller 打包为 文件夹......完成')
        else:
            print('error')
    elif platform.system() == 'Windows':
        print('当前系统为:Windows')
        flag = input('make为单文件和文件夹 输入1 ,仅make为文件夹 输入2 :\n')
        if flag == '1':
            print('......开始make为 单文件 程序......')
            print('......开始make为 单文件 程序......完成')
        elif flag == '2':
            print('......开始make为 文件夹 程序......')
            print('......开始make为 文件夹 程序......完成')
        else:
            print('error')