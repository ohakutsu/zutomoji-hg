# ZUTOMOJI_HG :cat2:

`ZUTOMOJI_HG`は、プログラミング向けフォント[白源（HackGen）](https://github.com/yuru7/HackGen)と、[ずっと真夜中でいいのに。](https://zutomayo.net/)の[オリジナル文字のフォント](https://zutomayo.net/font/) を合成したフォントです。

ずっと真夜中でいいのに。のオリジナル文字（以下、ずとまよ文字とします）を`U+100000`~`U+1000B2`に配置し、ずとまよ文字を普段遣いしやすくしています。
また、ベースとしている白源（HackGen）は、Nerd Fontsを追加合成している`HackGen NF`、`HackGen35 NF`を使用し、多くのアイコンフォントを使用できます。

## 合成方法

合成済みのフォントは配布していません。
そのため、以下の手順でフォントを合成する必要があります。

### 白源（HackGen）、ずとまよ文字フォントをダウンロードする

- [yuru7/HackGen: Hack と源柔ゴシックを合成したプログラミングフォント 白源 (はくげん／HackGen)](https://github.com/yuru7/HackGen)
  - `HackGen NF`をダウンロードします
- [FONT | ずっと真夜中でいいのに。](https://zutomayo.net/font/)

### ダウンロードしたフォントを配置する

このリポジトリをクローンし、リポジトリ直下にダウンロードしたフォントを配置します。

```console
$ exa -T
.
├── Dockerfile
├── HackGen35ConsoleNF-Bold.ttf
├── HackGen35ConsoleNF-Regular.ttf
├── HackGenConsoleNF-Bold.ttf
├── HackGenConsoleNF-Regular.ttf
├── patch.py
├── README.md
├── requirements.txt
└── ZTMY_MOJI-R.otf
```

### 合成スクリプトを実行します

Dockerを使って合成できます。

```console
$ docker build . -t zutomoji-hg
$ docker run -it --rm -v "${PWD}:/zutomoji-hg" zutomoji-hg
```

実行が完了すると、`ZUTOMOJI_HG*`のフォントファイルが生成されます。

```console
$ ls ZUTOMOJI_HG*
ZUTOMOJI_HG35C-Bold.ttf    ZUTOMOJI_HG35C-Regular.ttf ZUTOMOJI_HGC-Bold.ttf      ZUTOMOJI_HGC-Regular.ttf
```

## ずとまよ文字のコードポイント

Unicode 私用領域の`U+100000`~`U+1000B2`に配置しています。
各ずとまよ文字のコードポイントは以下の画像を参照ください。

![](/docs/zutomoji.jpg)

## Font License

ZUTOMOJI_HG 生成スクリプトにより生成されたフォントは、以下に従うものとします。

- [SIL Open Font License (OFL) Version 1.1](https://scripts.sil.org/OFL)
- [「ずっと真夜中でいいのに。」 著作物に関するガイドライン | ずっと真夜中でいいのに。](https://zutomayo.net/legal/)
- [FONT | ずっと真夜中でいいのに。](https://zutomayo.net/font/)

また、生成されたフォントの再配布は禁止とします。

## License

生成スクリプトは[MIT License](/LICENSE)に従うものとします。
