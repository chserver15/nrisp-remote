// ---------------------------------------------------------------------------
// NRISP: تا وقتی اولین تصویر از کامپیوتر نرسیده باشد، علت روی صفحه نوشته
// می‌شود (کدک، تعداد نمایشگر و وضوح گزارش‌شده از طرف کامپیوتر).
// هدف: پیدا کردن دقیق جای خرابی به‌جای حدس زدن.
// ---------------------------------------------------------------------------

import 'package:flutter/material.dart';
import 'package:flutter_hbb/common.dart';
import 'package:flutter_hbb/models/model.dart';
import 'package:get/get.dart';

class NrispWaitingInfo extends StatelessWidget {
  const NrispWaitingInfo({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Positioned(
      left: 8,
      top: 8,
      child: Obx(() {
        if (!gFFI.ffiModel.waitForFirstImage.value) {
          return const SizedBox.shrink();
        }
        String codec = '—';
        try {
          codec = gFFI.qualityMonitorModel.data.codecFormat ?? '—';
        } catch (_) {}
        int dispCount = 0;
        String res = '—';
        String host = '—';
        try {
          final PeerInfo pi = gFFI.ffiModel.pi;
          dispCount = pi.displays.length;
          if (pi.platform.isNotEmpty) {
            host = pi.platform;
            if (pi.version.isNotEmpty) {
              host = '$host ${pi.version}';
            }
          }
          final Display? d = pi.tryGetDisplay();
          if (d != null && d.isOriginalResolutionSet) {
            res = '${d.originalWidth}×${d.originalHeight}';
          }
        } catch (_) {}
        return Container(
          constraints: const BoxConstraints(maxWidth: 320),
          padding: const EdgeInsets.symmetric(horizontal: 9, vertical: 6),
          decoration: BoxDecoration(
            color: Colors.black.withOpacity(0.66),
            borderRadius: BorderRadius.circular(8),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              const Text(
                'در انتظار تصویر از کامپیوتر…',
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 11.5,
                  fontWeight: FontWeight.w700,
                ),
              ),
              const SizedBox(height: 3),
              Text(
                'کدک: $codec   |   نمایشگر: $dispCount   |   وضوح: $res',
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
                style: const TextStyle(color: Colors.white70, fontSize: 10.5),
              ),
              const SizedBox(height: 1),
              Text(
                'طرف مقابل: $host',
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
                style: const TextStyle(color: Colors.white54, fontSize: 10),
              ),
            ],
          ),
        );
      }),
    );
  }
}
