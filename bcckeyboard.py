from bcc import BPF
from bcc.utils import printb
from hexdump import hexdump
import re

code = """
#include <linux/usb.h>

struct data_t {
  u64 alen;
  u64 buflen;
  u16 vendor;
  u16 product;
  unsigned int transfer_flags;
  unsigned char buf[256];
};                
BPF_PERF_OUTPUT(events);

int kprobe____usb_hcd_giveback_urb(struct pt_regs *ctx, struct urb *urb) {
  struct data_t data = {};
  struct usb_device *dev = urb->dev;
  data.vendor = dev->descriptor.idVendor;
  data.product = dev->descriptor.idProduct;
  data.alen = urb->actual_length;
  data.transfer_flags = urb->transfer_flags;
  data.buflen = urb->transfer_buffer_length;
  bpf_probe_read_kernel(data.buf, sizeof(data.buf), urb->transfer_buffer);
  events.perf_submit(ctx, &data, sizeof(data));
  return 0; 
}
"""

b = BPF(text=code)

def print_event(cpu, data, size):
    event = b["events"].event(data)
    if event.vendor == 0x05ac: # change this id to your USB device
      keycodes = []
      for c in bytes(event.buf[0:event.buflen]):
        keycodes.append(asciichar(c))
      print("%s %s (%s)" % (judge_in_out(event.transfer_flags), keycodes, re.sub(r"\s+", " ", hexdump(bytes(event.buf[0:event.buflen]), result="return"))))

def judge_in_out(transfer_flags):
  if transfer_flags & 0x0200 != 0:
    return "IN >"
  return "OUT<"

def asciichar(keynum):
    char = chr(keynum)
    if 3 < ord(char) < 40:
        char = chr(keynum + 61)
        return char

    # TODO: ここ見ながらキーコード追加！
    # https://www.win.tue.nl/~aeb/linux/kbd/scancodes-14.html
    altchars = {
        chr(0): '',
        chr(40): 'ENTER',
        chr(41): 'Esc',
        chr(42): 'BSp',
        chr(43): 'TAB',
        chr(44): "Space",
        chr(45): "- / _",
        chr(46): "= / +",
        chr(47): "[ / {",
        chr(48): "] / }",
        chr(49): "\ / |",
        chr(50): "...",
        chr(51): "; / :",
        chr(52): "'",
        chr(53): "` / ~",
        chr(54): ", / <",
        chr(55): ". / >",
        chr(56): "/ / ?",
        chr(57): "Caps Lock",
        chr(58): "F1",
        chr(59): "F2",
        chr(60): "F3",
        chr(61): "F4",
        chr(62): "F5",
        chr(63): "F6",
        chr(64): "F7",
        chr(65): "F8",
        chr(66): "F9",
        chr(67): "F10",
        chr(68): "F11",
        chr(69): "F12",
        chr(70): "PrtScr",
        chr(71): "Scroll Lock",
        chr(72): "Pause",
        chr(73): "Insert",
        chr(74): "Home",
        chr(75): "PgUp",
        chr(76): "Delete",
        chr(77): "End",
        chr(78): "PgDn",
        chr(79): "Right",
        chr(80): "Left",
        chr(81): "Down",
        chr(82): "Up",
        chr(83): "Num Lock",
        chr(84): "KP /",
        chr(85): "KP *",
        chr(86): "KP -",
        chr(87): "KP +",
        chr(88): "KP Enter",
        chr(89): "KP 1 / End",
        chr(90): "KP 2 / Down",
        chr(91): "KP 3 / PgDn",
        chr(92): "KP 4 / Left",
        chr(93): "KP 5",
        chr(94): "KP 6 / Right",
        chr(95): "KP 7 / Home",
        chr(96): "KP 8 / Up",
        chr(97): "KP 9 / PgUp",
        chr(98): "KP 0 / Ins",
        chr(99): "KP . / Del",
        chr(100): "...",
        chr(101): "Applic",
        chr(102): "Power",
        chr(103): "KP =",
        chr(104): "F13",
        chr(105): "F14",
        chr(106): "F15",
        chr(107): "F16",
        chr(108): "F17",
        chr(109): "F18",
        chr(110): "F19",
        chr(111): "F20",
        chr(112): "F21",
        chr(113): "F22",
        chr(114): "F23",
        chr(115): "F24",
        chr(116): "Execute",
        chr(117): "Help",
        chr(118): "Menu",
        chr(119): "Select",
        chr(120): "Stop",
        chr(121): "Again",
        chr(122): "Undo",
        chr(123): "Cut",
        chr(124): "Copy",
        chr(125): "Paste",
        chr(126): "Find",
        chr(127): "Mute",
        chr(128): "Volume Up",
        chr(129): "Volume Down",
        chr(130): "Locking Caps Lock",
        chr(131): "Locking Num Lock",
        chr(132): "Locking Scroll Lock",
        chr(133): "KP ,",
        chr(134): "KP =",
        chr(135): "Internat",
        chr(136): "Internat",
        chr(137): "Internat",
        chr(138): "Internat",
        chr(139): "Internat",
        chr(140): "Internat",
        chr(141): "Internat",
        chr(142): "Internat",
        chr(143): "Internat",
        chr(144): "LANG",
        chr(145): "LANG",
        chr(146): "LANG",
        chr(147): "LANG",
        chr(148): "LANG",
        chr(149): "LANG",
        chr(150): "LANG",
        chr(151): "LANG",
        chr(152): "LANG",
        chr(153): "Alt Erase",
        chr(154): "SysRq",
        chr(155): "Cancel",
        chr(156): "Clear",
        chr(157): "Prior",
        chr(158): "Return",
        chr(159): "Separ",
        chr(160): "Out",
        chr(161): "Oper",
        chr(162): "Clear / Again",
        chr(163): "CrSel / Props",
        chr(164): "ExSel",
        chr(165): "",
        chr(166): "",
        chr(167): "",
        chr(194): "ExSel",
        chr(224): "LCtrl",
        chr(225): "LShift",
        chr(226): "LAlt",
        chr(227): "LGUI",
        chr(228): "RCtrl",
        chr(229): "RShift",
        chr(230): "RAlt",
        chr(231): "RGUI"
    }
    return altchars.get(char, char)

b["events"].open_perf_buffer(print_event)
while 1:
    b.perf_buffer_poll()