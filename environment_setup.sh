#!/bin/bash

# pyenvの自動インストール
curl -fsSL https://pyenv.run | bash

# pyenv にpathを通す(.bash_profileが存在するならそっちに書き込む)
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
echo 'eval "$(pyenv init - bash)"' >> ~/.profile

# python3.11.13で構築
pyenv install 3.11.13

# 仮想環境を作成
pyenv virtualenv 3.11.13 object_detect_cv2

# 仮想環境を有効化
pyenv activate object_detect_cv2

# ライブラリのインストール
pip install pyrealsense2
pip install numpy
pip install opencv-python
