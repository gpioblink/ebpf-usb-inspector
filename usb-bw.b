#include <linux/usb.h>

interval:s:1 {
  printf("--------------------------\n");
  print(@total);
  print(@sum);
  print(@buffer);
  clear(@sum);
  clear(@total);
  clear(@buffer);
}

kprobe:__usb_hcd_giveback_urb {
  $urb = (struct urb*)arg0;
  $dev = $urb->dev;
  @total = stats((uint64)$urb->actual_length);
  @sum[$dev->descriptor.idVendor,
       $dev->descriptor.idProduct,
       str($dev->product),
       str($dev->manufacturer)] = stats((uint64)$urb->actual_length);
  @buffer[$dev->descriptor.idVendor,
       $dev->descriptor.idProduct,
       $urb->transfer_buffer_length,
       str($dev->product),
       str($dev->manufacturer)] = str($urb->transfer_buffer);
}