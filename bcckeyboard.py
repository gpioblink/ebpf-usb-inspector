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

    # TODO: ここ見ながらキーコード追加！
    # https://www.win.tue.nl/~aeb/linux/kbd/scancodes-14.html
    altchars = {
        chr(0): '',
        chr(40): 'ENTER',
        chr(43): 'TAB'
    }
    return altchars.get(char, char)

b["events"].open_perf_buffer(print_event)
while 1:
    b.perf_buffer_poll()