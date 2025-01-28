#!/bin/bash
echo "......将 Yt-Capybara 安装于 /opt/Yt-Capybara 目录下...."
echo "请用管理员权限运行脚本"

sudo chmod 4755 -R Yt-Capybara
sudo cp -r Yt-Capybara /opt
sudo cp Yt-Capybara.desktop /usr/local/share/applications

echo "......finishe Yt-Capybara as /opt/Yt-Capybara...."