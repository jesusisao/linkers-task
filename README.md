# linkers-task

リンカーズ株式会社様の二次面接課題の回答です。

## 環境

python 3.8.0で動作確認済みです。

## 実行

### インデックスの作成 

コマンドでも作成できますが、初回検索時にindexがなかった場合は自動で作成されます。

```
python3 main.py index
```

### 検索例

```
python3 main.py search 渋谷
python3 main.py search 東京都

# 8行に渡ってcsvの住所が書かれている例
python3 main.py search 天神

# 同一の郵便番号に複数の町域がある例
python3 main.py search 久美
```

## 単体テスト実行

```
python3 -m unittest
```
