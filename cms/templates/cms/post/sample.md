[TOC]
このサイトは、管理人の日々の生活、子育て、IT関連などなど雑多に掲載する予定です。
この記事では、 MarkDown 記法を用いて記事を掲載することができます。
今回は、MarkDown 記法について記載します。

# MarkDown 記法とは
あるテキストの書き方です。この書き方に則って記載をすると、HTML の見出しや協調などに変換してくれます。
MarkDown 記法は、方言があるようですが、このサイトでは以下のように記載しています。

# 目次の付け方
目次をつけるには、文の最初に \[TOC] と書きます。
**T**able **O**f **C**ontents のです。
# 見出しの書き方
`#` を先頭に書くと見出しになります。
見出しのレベルは、 `#` を重ねた回数分上がります

\# 見出し1
この文章は大見出しです。
本文本文うんたらかんたら
\## 見出し2
この文章は中見出しです。
本文本文うんたらかんたら
\### 見出し3
この文章は小見出しです。
本文本文うんたらかんたら
# 強調
**太字**
*斜体字*
<del>取り消し線</del>

# 箇条書き
箇条書きは以下のように書きます。
先頭に + , - , * をつけてください。
<kbd>Tab</kbd> を入れると入れ子を作ることが出来ます。

- A
- B
- C
	- C-A ← タブを入れています

# 画像のはりつけ
ドラッグアンドドロップしてみると、なにやら文字が生成されます。
```![mount cook](/uploads/markdownx/4680db12-f20c-4656-a378-950e3c76e80d.jpg)```
mount cook となっている部分は画像の alt 属性です。

![mount cook](/uploads/markdownx/4680db12-f20c-4656-a378-950e3c76e80d.jpg)

# リンクの貼り付け
リンクを貼り付けるには、以下のように記載します

\[link](URL)
\[link](URL){:target="_blank"}

[ワードプレスのブログ](https://blog.world-of-f.website)
[ワードプレスのブログ_別タブ](https://blog.world-of-f.website){:target="_blank"}

[Google co jp](https://www.google.co.jp){:embed="cite"}

# 番号付きの箇条書き
\1. \2. \3. ... という感じで記載します。

1. あれやって
2. これやって
3. こうやると成功です
	4. タブを入れるとこんな感じ		

# コードを記載する
コードを記述したい場合は、\` ３つでくくります。
\```Python ←プログラミング言語名を記載する
(コードを記載)
\```
## Python の例
```python
print("Hello World")
```
## C\#  の例
```CSharp
using System;

public class Hello{
  public static void Main(){
    Console.WriteLine("hello world!");
  }
}
```

# その他の強調構文

## 重要なことを強調するとき

\!!! important "タイトル"
\    本文

のように記載します。
!!! important "タイトル！"
    この文章は Markdown 記法で記載されています。これは重要です。

## 情報を伝えたいとき

\!!! note "タイトル"
\    本文

のように記載します。

!!! note "情報。"
    この文章は Markdown 記法で記載されています。これは情報です。

## この方法でやるといいですよ的な書き方
\!!! success "タイトル"
\    本文

のように記載します。

!!! success "成功"
    この画面が表示されれば成功です。

他にもありますが、あとで書きます。

# 引用
引用は以下の書き方は、 \> をつけます。
引用元は、 \<cite></cite> で囲います

> この文章は引用です。
> <cite>引用元</cite>

# 脚注
文に脚注を設定することが出来ます。
脚注はページ最下部にその内容が展開されます。

```
脚注への参照[^1]を書くことができます。

長い脚注は[^longnote]のように書くことができます。

[^1]: 1つめの脚注への参照です。

[^longnote]: 脚注を複数ブロックで書く例です。

    後続の段落はインデントされて、前の脚注に属します。

```


脚注への参照[^1]を書くことができます。

長い脚注は[^longnote]のように書くことができます。

[^1]: 1つめの脚注への参照です。

[^longnote]: 脚注を複数ブロックで書く例です。

    後続の段落はインデントされて、前の脚注に属します。

# 数式
数式はMathJax で表示可能です。
$$\frac{1}{x}$$

長い数式は以下のように
\\[
  \sum_{n=1}^\infty \frac{1}{n^2} = \frac{\pi^2}{6}
\\]

また以下のように
\\[
  \frac{\pi}{2} =
  \left( \int_{0}^{\infty} \frac{\sin x}{\sqrt{x}} dx \right)^2 =
  \sum_{k=0}^{\infty} \frac{(2k)!}{2^{2k}(k!)^2} \frac{1}{2k+1} =
  \prod_{k=1}^{\infty} \frac{4k^2}{4k^2 - 1}
\\]

## 上付き、下付き添字の表示
上付き、下付き添字は、設定できます。
上付き添字は \<sup></sup> でくくる
下付き添字は \<sup></sup> でくくる 

H<sub>2</sub>O

2<sup>10</sup> = 1024

## id属性やclass属性などの属性を指定する
マニアックな例です。
id class 属性などなどを指定することが出来ます
\Le Site
\{ .main .shine #the-site lang=fr}

Le Site
{ .main .shine #the-site lang=fr}

... 見た目は変化ないです

# Mark
<mark>ここ</mark>をマークします
# 定義リスト
<dl>
  <!-- 複数のdd -->
  <dt>みかん</dt>
  <dd>オレンジ色。</dd>
  <dd>甘酸っぱい。</dd>
  <!-- 複数のdt -->
  <dt>りんご</dt>
  <dt>アップル</dt>
  <dd>赤くて甘い。</dd>
</dl>

# Google Map
埋め込んでみる
<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d26072.101969192616!2d139.06965655623608!3d35.23105273310026!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x6019a3a960cd05c9%3A0xe485ffffbe1c9220!2z44CSMjUwLTAzMTEg56We5aWI5bed55yM6Laz5p-E5LiL6YOh566x5qC555S65rmv5pys!5e0!3m2!1sja!2sjp!4v1614091621735!5m2!1sja!2sjp" width="100%" height="250" style="border:0;" allowfullscreen="" loading="lazy"></iframe>

# twitter
埋め込んで見る
<blockquote class="twitter-tweet"><p lang="ja" dir="ltr">家のパソコンUbuntu入れて、vscode入れたらめっちゃ快適。</p>&mdash; HLKN（はるけんのKEN　です） (@brv_HK) <a href="https://twitter.com/brv_HK/status/1198932085882273793?ref_src=twsrc%5Etfw">November 25, 2019</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>