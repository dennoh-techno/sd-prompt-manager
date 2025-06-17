# sd-prompt-manager

主にAIで作成したStable Diffusion Forge用のプロンプト管理・挿入拡張機能です。  
毎回、お決まりの複数プロンプトの塊を入力するのは面倒なので、複数プロンプトをラベルにまとめて、  
ラベル選択で一括挿入出来るような拡張機能を作りました。  
カテゴリ・ラベルごとにプロンプトを整理し、ワンクリックでプロンプト欄やネガティブプロンプト欄へ挿入できます。  

![image](https://github.com/user-attachments/assets/c0ca12f8-3130-44af-88fd-31b1f55fc6d1)

以下のように入力して、よく使用するプロンプトの塊を管理します。  

![image](https://github.com/user-attachments/assets/36599cca-e9c3-482e-874b-272686ec43f3)
  
Insert Promptsタブにて、上記フォームで作成したカテゴリを選択すると、ラベル（ボタン）が表示されます。
- ポジティブ・プロンプトに挿入したい場合、ボタンを左クリック
- ネガティブ・プロンプトに挿入したい場合、ボタンを右クリック
でプロンプト入力欄に挿入できます。

![image](https://github.com/user-attachments/assets/ce068a67-d12c-44cb-9194-f92d92b7a4de)

---

## 主な機能

- カテゴリ・ラベルごとにプロンプトを管理
- txt2img・img2imgタブ両対応
- ボタンを左クリックでプロンプト欄へ、右クリックでネガティブプロンプト欄へ挿入
- カーソル位置への挿入に対応

---

## インストール方法

Stable Diffusion WebUIを使用の場合は、  
拡張機能(Extensions)タブから、拡張機能のリポジトリのURL（URL for extension's git repository）  に  
    ```
    https://github.com/dennoh-techno/sd-prompt-manager.git
    ```  
を入力してインストールして下さい。

gitのcloneコマンドでインストールしたい場合は、以下の通りです。  
1. このリポジトリを`extensions`フォルダにクローンまたはコピーします。

    ```
    git clone https://github.com/dennoh-techno/sd-prompt-manager.git
    ```

2. Stable Diffusion WebUIを再起動します。

---

## 使い方

1. WebUIの「拡張機能」タブから「sd-prompt-manager」を開きます。
2. カテゴリを選択し、表示されたラベルボタンをクリックするとプロンプト欄に挿入されます。
    - **左クリック**：プロンプト欄に挿入
    - **右クリック**：ネガティブプロンプト欄に挿入
3. カーソル位置にプロンプトが挿入されます。

---

## カスタマイズ

- `scripts/prompt_data.yaml`を編集することで、カテゴリやラベル、プロンプト内容を自由に追加・編集できます。

---

## 注意事項

- 本拡張機能はStable Diffusion WebUI Forge/Automatic1111系で動作確認済みです。
- 追加の依存パッケージはありません。

---

## ライセンス

MIT License
