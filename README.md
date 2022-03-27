# gimp-python-fu-testing

Windows 版 GIMP 2.10.x 向けに自作した Python-fu スクリプトを単体テストする方法を説明する。

# TL;DR

[test_shrink.bat#L29-L30](test_shrink.bat#L29-L30)

```bat
"%gimp%" -i -d -f --batch-interpreter python-fu-eval ^
	-b - -b "pdb.gimp_quit(1)" < test_shrink.py
```

[test_shrink.py#L140-L142](test_shrink.py#L140-L142)

```python
    with tempfile.TemporaryFile() as out:
        runner = unittest.TextTestRunner(stream=out)
        unittest.main(argv=[__file__], testRunner=runner, exit=False)
```

1. GIMP のコマンドラインで `--batch-interpreter python-fu-eval` を指定してバッチ実行機能により Python の単体テストを実行する。
2. GIMP のコマンドラインで `-b - -b "pdb.gimp_quit(1) < test_foobar.py"` のように指定して単体テストを Python ファイルからリダイレクトして読み込む。
3. `unittest.main()` の呼出し時に `argv` `testRunner` `exit` を適切に指定してクラッシュやエラーが起きないようにする。

# うまくいく例

次のファイルを用いて説明する。

- **shrink.py** -- 画像のタテとヨコのサイズをそれぞれ半分にする Python-fu スクリプト
  - `def shrink(image, drawable)` -- GIMP に登録される関数
  - `def half(length)` -- shrink 関数から呼び出される関数
- **test_shrink.py** -- shrink.py の単体テスト
  - `class TestShrink(unittest.TestCase)` -- shrink 関数をテストするクラス
  - `class TestHalf(unittest.TestCase)` -- half 関数をテストするクラス
- **test_shrink.bat** -- shrink.py を実行するためのバッチファイル
- **test_shrink-output.txt** -- バッチファイルを実行した際の出力例

## 要点1：GIMP のバッチ実行機能による単体テストの実行

[test_shrink.bat#L29-L30](test_shrink.bat#L29-L30)

```bat
"%gimp%" -i -d -f --batch-interpreter python-fu-eval ^
	-b - -b "pdb.gimp_quit(1)" < test_shrink.py
```

GIMP にはバッチ実行機能が備わっており、GUI を起動することなくスクリプトの実行が可能である。一般的には画像の一括処理のために用いるこの機能を、ここでは単体テストの実行のために用いる。

デフォルトのスクリプトは Script-Fu (Scheme 言語で書くスクリプト) のため、`--batch-interpreter python-fu-eval` オプションを指定して Python-fu に切り替える。

> --batch-interpreter=proc
>
> Specify the procedure to use to process batch commands. **The default procedure is Script-Fu.**
>
> https://docs.gimp.org/2.10/en/gimp-fire-up.html#gimp-concepts-running-command-line

python-fu-eval の実体は plug-ins/python-eval.py のようだ。

- https://github.com/GNOME/gimp/blob/GIMP_2_10_30/plug-ins/pygimp/plug-ins/python-eval.py

なお `-i -d -f` オプションの意味は次のとおり。

> -i, --no-interface
>
> Run without a user interface.
>
> -d, --no-data
>
> Do not load patterns, gradients, palettes, or brushes. Often useful in non-interactive situations where start-up time is to be minimized.
>
> -f, --no-fonts
>
> Do not load any fonts. This is useful to load GIMP faster for scripts that do not use fonts, or to find problems related to malformed fonts that hang GIMP.
>
> https://docs.gimp.org/2.10/en/gimp-fire-up.html#gimp-concepts-running-command-line

`^` はひとつのコマンドを複数行にまたいで書くために用いている。

`-b` オプションについては次のセクションで説明する。

## 要点2：リダイレクトによる単体テストの読込み

[test_shrink.bat#L29-L30](test_shrink.bat#L29-L30) (再掲)

```bat
"%gimp%" -i -d -f --batch-interpreter python-fu-eval ^
	-b - -b "pdb.gimp_quit(1)" < test_shrink.py
```

python-fu-eval は `-b` オプションで指定された Python コードを実行する。`-b` オプションは複数回指定可能であり、実行順序は左から右である。

ここで `-b -` と指定すると、python-fu-eval は標準入力からコードを読み込んで実行する。単体テストのコードをあらかじめファイル (ここでは test_shrink.py) に書いておき、リダイレクト `< test_shrink.py` で渡すことにより、コードの見通しを良くしている。

> -b, --batch=commands
>
> Execute the set of commands non-interactively. The set of commands is typically in the form of a script that can be executed by one of the GIMP scripting extensions. **When the command is -, commands are read from standard input.**
>
> https://docs.gimp.org/2.10/en/gimp-fire-up.html#gimp-concepts-running-command-line

`-b "pdb.gimp_quit(1)"` はバッチ実行機能の終了時の作法である。`-b` オプションで渡す代わりに単体テストのファイルの最後に書いてもいい。

## 要点3：unittest.main() の呼出し方法

[test_shrink.py#L139-L145](test_shrink.py#L139-L145)

```python
    content = None
    with tempfile.TemporaryFile() as out:
        runner = unittest.TextTestRunner(stream=out)
        unittest.main(argv=[__file__], testRunner=runner, exit=False)
        out.seek(0)
        content = out.read()
    gimp.message(content)
```

`unittest.main()` の呼出し時には `argv` `testRunner` `exit` を適切に指定する必要がある。さもなくばバッチ実行でクラッシュまたはエラーが起きる。それぞれを適切に指定しなかった場合の例は「うまくいかない例」セクションを参照。

ここでは単体テストの実行結果を一時ファイル `out` に出力する。このファイルの内容を読み込んで `gimp.message()` に渡すことによってコンソールに実行結果を表示する。

# うまくいかない例

## unittest.main() 呼出し時に argv=[\_\_file\_\_] を指定しない

実行時にクラッシュする。詳しくは [1_argv](1_argv) を参照。

原因はおそらく、単体テスト実行時の `sys.argv` に `unittest.main()` が対応していない引数が含まれていることにあると思われる。バッチ実行される Python-fu スクリプト (ここでは単体テスト) は GIMP プラグイン python-eval.py によって実行される。この実行時には `-gimp 9 7 -run 0` といったコマンドライン引数が渡されて `sys.argv` となっている。デフォルトの `unittest.main()` は `sys.argv` を使うため、これらの引数を使ってしまう。

> unittest.main([module[, defaultTest[, **argv**[, testRunner[, testLoader[, exit[, verbosity[, failfast[, catchbreak[, buffer]]]]]]]]]])
>
> [..]
>
> The **argv** argument can be a list of options passed to the program, with the first element being the program name. **If not specified** or None, the values of **sys.argv** are used.
>
> https://docs.python.org/2.7/library/unittest.html#unittest.main

各コマンドライン引数の意味は次のコードを読むとなんとなく想像できるかもしれない。

- https://github.com/GNOME/gimp/blob/GIMP_2_10_30/libgimp/gimp.c#L278-L288

## unittest.main() 呼出し時に testRunner を適切に指定しない

実行時にエラーになる。詳しくは [2_testRunner](2_testRunner) を参照。

原因はおそらく、標準エラー出力を使用していることにあると思われる。デフォルトの `unittest.main()` はテストランナーにデフォルトの `unittest.TextTestRunner` を使用しており、これは `stream=sys.stderr` となっていて標準エラー出力を使用している。「うまくいく例」では `stream` を指定した `unittest.TextTestRunner` を `unittest.main()` の `testRunner` に指定することでうまくいっている。

> class unittest.TextTestRunner(**stream=sys.stderr**, descriptions=True, verbosity=1, failfast=False, buffer=False, resultclass=None)
>
> https://docs.python.org/2.7/library/unittest.html#unittest.TextTestRunner

デフォルトの `unittest.main()` がテストランナーにデフォルトの `unittest.TextTestRunner` を使用していることについては次のコードを参照。

- https://github.com/python/cpython/blob/v2.7.18/Lib/unittest/main.py#L91
- https://github.com/python/cpython/blob/v2.7.18/Lib/unittest/main.py#L219-L220

## unittest.main() 呼出し時に exit=False を指定しない

実行時にクラッシュする。詳しくは [3_exit](3_exit) を参照。

原因はおそらく、デフォルトの `unittest.main()` が `pdb.gimp_quit(1)` でなく `sys.exit()` で終了してしまうことにあると思われる。

> By default main calls **sys.exit()** with an exit code indicating success or failure of the tests run.
>
> https://docs.python.org/ja/2.7/library/unittest.html#unittest.main

## バンドルされている Python で直接単体テストを実行する

環境変数 PYTHONPATH を設定しなかった場合はもちろん、適切に設定した場合もエラーになる。詳しくは [4_ImportError](4_ImportError) および [5_LibGimpBase-ERROR](5_LibGimpBase-ERROR) を参照。

エラーメッセージ `gimp_wire_write_msg: the wire protocol has not been initialized` はコードで言えばこの箇所のようだ。

- https://github.com/GNOME/gimp/blob/GIMP_2_10_30/libgimpbase/gimpwire.c#L251

これ以上のことは GIMP の内部に踏み込むことになりそうなので調べられていない。

-----

Author: Takashi Menjo &lt;takashi DOT menjo PLUS github AT gmail DOT com&gt;
