# ebpf-usb-inspector

eBPFを使って、USBのManInTheMiddleをするためのツールです。

## 使用方法

`$sudo python3 bccusb.py`を実行するだけ。

中身開いて、`# change this id to your USB device`の部分のvendorIdを取得したいUSBデバイスのものに変えてお使いください。

## 使用方法(キーボード用)

キーボード用に、押したキーの値が表示されたりするツールも作りました。
`$sudo python3 bcckeyboard.py`を実行してください。

## 使用方法(旧: こちらは正しく動作しません)

`$ sudo bpftrace usb-bw.b`するだけ

参考: https://blog.habets.se/2020/08/Measuring-USB-with-bpftrace.html
