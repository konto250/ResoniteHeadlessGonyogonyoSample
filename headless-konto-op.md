# Resoniteヘッドレスサーバ　設定のまとめ(N=1)

> 記事中のConfig例は筆者の運用実績(N=1)に基づくものです。[公式ドキュメント](https://wiki.resonite.com/Headless_server_software)も必ず参照してください。

---

## セッションIDの固定（`customSessionId`）

```json
"customSessionId": "S-U-1NVSRdevcJs:RadioExercise1"
```

`customSessionId` を固定しておくと、セッションへの案内URLが不変になります。

```
https://go.resonite.com/session/S-U-1NVSRdevcJs:RadioExercise1
```

セッションURLをDiscordやイベント告知に貼っておくだけで、参加者が直接JOINできるため、ホスト側の招待コスト削減になります。

---

## アセット転送数の調整（`maxConcurrentAssetTransfers`）

```json
"maxConcurrentAssetTransfers": 100
```

アセット数が多いワールドでは増やすと転送が速くなる場合があります。ただし、**ヘッドレスPC側の回線速度に依存**するため、上げすぎると逆効果になることがあります。実際の帯域と相談しながら調整してください。

---

## タグの設定（`tags`）

```json
"tags": ["jp"]
```

ヘッドレスのセッションはワールド検索で見つかりにくい傾向があります。適切なタグを設定しておくと、セッションブラウザからの発見性が上がります。

---

## アイドル時のワールドリセット（`idleRestartInterval`）

```json
"idleRestartInterval": -1.0
```

**ワールドの保存が主目的のイベント**では、`-1.0`（無効）にしておくほうが無難です。意図しないリセットでデータが失われるリスクを避けられます。

---

## AFK自動キック（`awayKickMinutes`）

```json
"awayKickMinutes": 5.0
```

Resoniteは複数セッションへの同時参加ができるため、AFK状態で席を占有し `maxUsers` の上限に達してしまうケースがあります。集会型イベントでは設定を推奨します。

---

## クラッシュ時の自動復旧（`autoRecover`）

```json
"autoRecover": true
```

ヘッドレスがクラッシュした際に自動で再起動します。運が良ければ落ちる直前のワールド状態で復帰します。

---

## 自動保存（`autosaveInterval`）と保存先の選択（`saveAsOwner`）

```json
"autosaveInterval": 600.0
```

デフォルトでは自動保存は行われません。`autosaveInterval` を設定する場合、**`saveAsOwner` の値が動作に大きく影響します**。

### `saveAsOwner` の選択肢と挙動

| 値 | 保存先 | 備考 |
|---|---|---|
| `"LocalMachine"` | ヘッドレスPC（ローカル） | 最も安定。クラウドへの反映は別途必要 |
| `"CloudUser"` | ヘッドレスアカウントのクラウド | 新規保存扱いになり、シンクが詰まりやすく、最悪コンフリクトが発生 |
| `null`（デフォルト） | 読み込み元レコードに上書き | ローカルにも保存されている場合あり(挙動不明) |


---

## データ・キャッシュ・ログの保存先指定

```json
"dataFolder": "C:/Datas/CJ/db",
"cacheFolder": "C:/Datas/CJ",
"logsFolder": "C:/Datas/CJ/logs"
```

デフォルトのパスではなく、わかりやすい場所に明示的に指定しておくと管理が楽になります。また `dataFolder` にはクラッシュ直前のワールド状態が保存されていることがあり、**復旧の手がかり**になります。

---

## ワールドが爆散したときの復旧手順

自動保存を有効にしている場合、`dataFolder` 内に `.lz4bson` 拡張子のファイルが一定間隔で保存されています。

**復旧手順：**

1. `dataFolder` 内の `.lz4bson` ファイルを探す
2. そのファイルを **ヘッドあり（通常）クライアントのウィンドウにドラッグ＆ドロップ**する
3. ワールドが開く

---

## 有用な外部Mod

> Modの使用は自己責任で。導入前にResoniteのModサポートポリシーを確認してください。

- **[ResoniteIPv6Mod](https://github.com/bontebok/ResoniteIPv6Mod)**  
  IPv6環境での接続問題を改善する可能性があります。

- **[StresslessHeadless](https://codeberg.org/Raidriar/StresslessHeadless)**  
  ヘッドレスに不要な計算をさせないことで、リソース効率を上げます。

- **[HeadlessTweaks](https://github.com/New-Project-Final-Final-WIP/HeadlessTweaks)**  
  Discordへのステータス通知、Resonite内DM経由でのセッション起動・シャットダウン・保存などが可能になります。

---

*最終更新：2026年4月*
