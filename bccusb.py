from bcc import BPF
from bcc.utils import printb
from hexdump import hexdump

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
      print("[vendor = 0x%x, product = 0x%x] transfer_flags = %d, actual_length = %d, transfer_buffer_length = %d" % (event.vendor, event.product, event.transfer_flags, event.alen, event.buflen))
      hexdump(bytes(event.buf[0:event.buflen]))
      print("")

b["events"].open_perf_buffer(print_event)
while 1:
    b.perf_buffer_poll()