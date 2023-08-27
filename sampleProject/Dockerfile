# 建立python環境
FROM python:3.7

# 設置python環境變量
ENV PYTHONUNBUFFERED 1

# 建立虛擬環境
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
# PATH: PATH is a list of directories which are searched for commands to run. activate
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# 建立文件資料夾
RUN mkdir /my_django

# 設定主要工作目錄 
WORKDIR /my_django

# 複製需求文件至文件資料夾中　
COPY . /my_django

# 下載需求的資料檔案
RUN . "$VIRTUAL_ENV/bin/activate"
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

# 設置環境變數
ENV SPIDER=/my_django
