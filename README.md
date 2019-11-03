# linkers-task 実行説明資料

リンカーズ株式会社様の二次面接課題の回答です。

## 動作環境

実行ファイルはmacOS Mojave 10.12.6で動作確認済みです。

## 開発環境

python 3.8.0で動作確認済みです。

実行ファイルを生成するためにpyinstallerを使用しています。
2019/11/03現在、python 3.8.0に対応したpyinstallerは未リリースのため、
開発用のものを直接インストールする必要があります。

```
pip install https://github.com/pyinstaller/pyinstaller/archive/develop.tar.gz
```

## TODO

- 技術説明資料の作成

## 実行

### インデックスの作成 

コマンドでも作成できますが、初回検索時にindexがなかった場合は自動で作成されます。

#### 直接実行

```
python3 linkerstask.py index
```

#### バイナリで実行

```
./linkerstask index
```

### 検索例

#### 直接実行

```
python3 linkerstask.py search 渋谷
python3 linkerstask.py search 東京都

# 8行に渡ってcsvの住所が書かれている例
python3 linkerstask.py search 天神

# 同一の郵便番号に複数の町域がある例
python3 linkerstask.py search 久美
```

なお、`-p`もしくは`--perfect`をつけると完全一致で検索することができます。
ただし、この場合は例２にあったように「東京都」で検索した時に東京と京都が含まれている住所は出てきません。
（「京都」で検索をかけると、「東京都」と「京都」が出てきます。）

```
python3 linkerstask.py search -p 京都
```

#### バイナリで実行

```
./linkerstask search 渋谷
```

## 単体テスト実行

```
python3 -m unittest
```

## バイナリファイルのビルド

```
pyinstaller linkerstask.py --onefile --clean
```
