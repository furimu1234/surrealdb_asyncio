## asyncioに対応したsurrealdbのライブラリです。

なるべくsqlを書かないように設計しました。

コメント等はまだなので後で追記します。

## ビルド方法

`git clone git@github.com:furimu1234/surrealdb_asyncio.git`

`cd surrealdb_asyncio`

`poetry build -f wheel`

上記コマンド入力後、distディレクトリが作成され、`surrealdb_asyncio-0.0.1-py3-none-any.whl`ファイルが作成されます。このファイルをインストールしてください。

## インストール方法

- pip

`pip install dir/surrealdb_asyncio-0.0.1-py3-none-any.whl`
- poetry

`poetry add dir/surrealdb_asyncio-0.0.1-py3-none-any.whl`
## タスク
- [x] 最初のコミット
- [x] リファクタリング
- [ ] docstring追記
- [ ] サンプル作成
- [ ] テストケース作成