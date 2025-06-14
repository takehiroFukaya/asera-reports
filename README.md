# アセラ日報自動化
## Python コーディング規約

### 基本構文とスタイル

- PEP8 に準拠
  - PEP8の公式ドキュメントは以下より確認できます。
    - [日本語版](https://pep8-ja.readthedocs.io/ja/latest/)
    - [English](https://peps.python.org/pep-0008/)
- インデントは **スペース4つ**
- 1ファイル = 1責任単位（UI / ロジック / 設定 など）
- ファイルの先頭に不要なコメントやエンコーディング宣言は不要

これらのスタイルを自動的に守れるようにするため、PyCharmのFile Watcherで以下のリンター・フォーマッターを有効にしてください。
- `flake8`
- `black`
- `isort`
- `mypy`

追加の仕方は[【PyCharm】ファイル保存時にlinterとformatterが自動実行されるように設定する](https://zenn.dev/horitaka/articles/4fc4a5c19bee22)を参照してください。

### 命名規則

| 種別   | 形式            | 例                          |
|------|---------------|----------------------------|
| 変数名  | `snake_case`  | `user_name`, `data_df`     |
| 関数名  | `snake_case`  | `load_data()`, `run_app()` |
| クラス名 | `PascalCase`  | `DataLoader`, `MainView`   |
| 定数   | `UPPER_SNAKE` | `MAX_ROWS`, `API_TIMEOUT`  |


### Streamlit 特有の設計

- UI要素（`st.button`, `st.text_input` など）は**セクションごとに整理**
- 状態管理は **`st.session_state` を活用**
- データ処理や重い関数にはキャッシュを使う：

  ```python
  @st.cache_data
  def load_data(path):
      return pd.read_csv(path)
  ````

### 関数・モジュール設計

* 関数は **単一の責務** を守る
* **UIとロジック(機能)は分離**する：

  ```python
  # UI関数
  def render_sidebar():
      st.sidebar.selectbox("選択", ["A", "B"])

  # ロジック関数
  def load_config(path):
      with open(path) as f:
          return yaml.safe_load(f)
  ```


### ファイル構成
※ファイル名の一部は要件定義書のものをそのまま使っています。実際の開発のときに修正してください。
```
project/
├── app.py
├── pages/
│   ├── __init__.py
│   ├── top.py
│   ├── 勤怠入力.py
│   ├── 作業登録.py
│   ├── 請求一覧.py
│   ├── 出勤簿.py
│   └── 日報一覧.py
├── utils/
│   ├── __init__.py
│   ├── 出勤時間登録.py
│   └── 退勤時間登録.py # 以下省略
├── config.py
├── __init__.py
├── requirements.txt
├── pyproject.toml # Linter/Formatterの設定用
└── setup.cfg #flake8の設定用
```


### コメントとドキュメント

* 関数やクラスには簡潔な docstring を記述：

  ```python
  def load_data(path: str) -> pd.DataFrame:
      """指定されたパスからCSVを読み込む"""
      ...
  ```
* コメントは日本語または英語で書いてください。

### バージョン管理・依存管理

* `requirements.txt` を使用

* `.gitignore` に以下を含める：

  * `__pycache__/`
  * `.env`
  * `.venv/`



### セキュリティ・環境変数管理

* APIキーや秘密情報は `.env`で管理
* 読み込み例（Streamlit）：

  ```python
  api_key = st.secrets["openai"]["api_key"]
  ```



