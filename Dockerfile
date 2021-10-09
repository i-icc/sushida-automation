# --- ビルド用ステージ ---
FROM python:3.7 as builder

COPY . /src/
WORKDIR /src

RUN pip3 install -r /src/requirements.txt

# --- 実行ステージ ---
## docker run --rm -it -v $(pwd):$(pwd):cached --workdir=$(pwd) i-icc/sushida-automation
FROM python:3.7

WORKDIR /src/exe
CMD [ "python", "main.py"]