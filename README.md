# ebpf-usb-inspector

This is a tool for USB ManInTheMiddle using eBPF.

eBPFを使って、USBのManInTheMiddleをするためのツールです。

## How to Use 使用方法

Please execute `$sudo python3 bccusb.py`.

Before your execusion, please open the source code and change vendorId to your kerboard.
(Edit the line `# change this id to your USB device`.)


`$sudo python3 bccusb.py`を実行するだけ。

中身開いて、`# change this id to your USB device`の部分のvendorIdを取得したいUSBデバイスのものに変えてお使いください。

## How to Use (For Keyboard HID) 使用方法(キーボード用)

For the keyboard, we also created a tool that displays the value of keys pressed.

Please run `$sudo python3 bcckeyboard.py`.

キーボード用に、押したキーの値が表示されたりするツールも作りました。
`$sudo python3 bcckeyboard.py`を実行してください。

## 使用方法(旧: こちらは正しく動作しません This section is outdated.)

`$ sudo bpftrace usb-bw.b`するだけ

参考: https://blog.habets.se/2020/08/Measuring-USB-with-bpftrace.html
