# fastapi-sandbox

http://localhost:8000/docs#/


## Description

- [Tool Versions](#tool-versions)
- [Supported Version](#supported-version)
- [Getting Started](#getting-started)
- [Command](#command)

---

## Tool Versions
基本的に大きくバージョンが離れておらず、下記のバージョン以上であればOKです。

### MacOS

```zsh
$ sw_vers
ProductName:		macOS
ProductVersion:		14.6.1
BuildVersion:		23G93
```

### Python ( in Docker Container )

```zsh
$ python -V
Python 3.12.6
```

※コンテナ生成のタイミングによって、パッチバージョンは異なる可能性があります。

### Docker Compose
```zsh
$ docker compose version
Docker Compose version v2.29.1-desktop.1
```

### other

[pyproject.toml](./pyproject.toml)を参照。

---

## Getting Started

[こちら](./readme/01_GETTING_STARTED.md)

---

## Command

主要なコマンドは以下の通りです。
それ以外のコマンドの[詳細はこちら](./readme/02_COMMAND.md)。

### コンテナのビルド

```zsh
$ make build
```

### コンテナの起動

```zsh
$ make up
```

### コンテナの起動（バックグラウンド）

```zsh
$ make upd
```

### コンテナの停止

```zsh
$ make stop
```

### コンテナの削除

```zsh
$ make down

```

### コードチェック

```zsh
$ make py/check
```

### コード修正

```zsh
$ make py/fix
```

### テスト

```zsh
$ make py/test
```

---
