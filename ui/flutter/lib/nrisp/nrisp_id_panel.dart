// ---------------------------------------------------------------------------
// ستون کنار برنامه — موسسه تحقیقات سیاست علمی کشور
// چیدمان و رنگ‌بندی بر پایهٔ نرم‌افزار درسان‌دسک: زمینهٔ تیره، رنگ نارنجی،
// کارت «دسکتاپ شما» با شناسه و رمز عبور و فهرست تنظیمات.
// ---------------------------------------------------------------------------

import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_hbb/common.dart';
import 'package:flutter_hbb/desktop/pages/desktop_tab_page.dart';
import 'package:flutter_hbb/models/platform_model.dart';
import 'package:flutter_hbb/models/state_model.dart';
import 'package:url_launcher/url_launcher.dart';

/// نام نمایشی برنامه (فارسی)
const String nrispAppNameFa = 'دسترسی راه دور موسسه';

/// نام سازمان
const String nrispCompanyFa = 'موسسه تحقیقات سیاست علمی کشور';

/// نشانی سایت سازمان
const String nrispDomain = 'nrisp.ac.ir';

/// رنگ‌های سازمانی — بر پایهٔ پوستهٔ تیرهٔ درسان‌دسک
class NrispBrand {
  static const Color orange = Color(0xFFFB4201); // نارنجی اصلی
  static const Color orangeSoft = Color(0xFFFF7A3D);
  static const Color orangeFaint = Color(0x1AFB4201);
  static const Color bg = Color(0xFF181B21); // زمینهٔ پنجره
  static const Color sidebar = Color(0xFF1B1F26); // زمینهٔ ستون کنار
  static const Color card = Color(0xFF1F232A); // کارت‌ها
  static const Color row = Color(0xFF24282F); // ردیف‌های داخلی
  static const Color line = Color(0xFF2A2F37);
  static const Color text = Color(0xFFF2F4F7);
  static const Color muted = Color(0xFF98A2B0);
  static const Color green = Color(0xFF2ECC71);
  static const Color red = Color(0xFFE5484D);
}

class NrispIdPanel extends StatefulWidget {
  const NrispIdPanel({Key? key}) : super(key: key);

  @override
  State<NrispIdPanel> createState() => _NrispIdPanelState();
}

class _NrispIdPanelState extends State<NrispIdPanel> {
  String _id = '';
  String _password = '';
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    _load();
    _timer = Timer.periodic(const Duration(seconds: 2), (_) => _load());
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  Future<void> _load() async {
    try {
      final id = await bind.mainGetMyId();
      final pw = await bind.mainGetTemporaryPassword();
      if (!mounted) return;
      if (id != _id || pw != _password) {
        setState(() {
          _id = id;
          _password = pw;
        });
      }
    } catch (_) {
      // سرویس هنوز آماده نیست
    }
  }

  void _copy(String text) {
    if (text.trim().isEmpty) return;
    Clipboard.setData(ClipboardData(text: text));
    showToast(translate('Copied'));
  }

  @override
  Widget build(BuildContext context) {
    return Directionality(
      textDirection: TextDirection.rtl,
      child: Container(
        width: 300,
        decoration: const BoxDecoration(
          color: NrispBrand.sidebar,
          border: Border(left: BorderSide(color: NrispBrand.line, width: 1)),
        ),
        child: SingleChildScrollView(
          padding: const EdgeInsets.fromLTRB(14, 16, 14, 18),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              _brand(),
              const SizedBox(height: 16),
              _desktopCard(),
              const SizedBox(height: 14),
              _menu(),
              const SizedBox(height: 20),
              _footer(),
            ],
          ),
        ),
      ),
    );
  }

  // ------------------------------------------------------------- سرصفحه

  Widget _brand() {
    return Row(
      children: [
        Container(
          width: 40,
          height: 40,
          padding: const EdgeInsets.all(5),
          decoration: BoxDecoration(
            color: NrispBrand.card,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: NrispBrand.line),
          ),
          child: loadIcon(30),
        ),
        const SizedBox(width: 10),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: const [
              Text(
                nrispAppNameFa,
                style: TextStyle(
                  fontSize: 13.5,
                  fontWeight: FontWeight.w800,
                  color: NrispBrand.orange,
                  height: 1.35,
                ),
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
              ),
              SizedBox(height: 2),
              Text(
                nrispCompanyFa,
                style: TextStyle(
                  fontSize: 10,
                  color: NrispBrand.muted,
                  height: 1.3,
                ),
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
            ],
          ),
        ),
      ],
    );
  }

  // -------------------------------------------------- کارت «دسکتاپ شما»

  Widget _desktopCard() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Row(
          children: const [
            Icon(Icons.desktop_windows_outlined,
                size: 15, color: NrispBrand.orange),
            SizedBox(width: 6),
            Text(
              'دسکتاپ شما',
              style: TextStyle(
                fontSize: 13,
                fontWeight: FontWeight.w700,
                color: NrispBrand.text,
              ),
            ),
          ],
        ),
        const SizedBox(height: 9),
        _valueRow(
          label: 'شناسه',
          value: _id.isEmpty ? '...' : _id,
          onCopy: () => _copy(_id),
        ),
        const SizedBox(height: 8),
        _valueRow(
          label: 'رمز عبور',
          value: _password.isEmpty ? '------' : _password,
          onCopy: () => _copy(_password),
          trailing: IconButton(
            padding: EdgeInsets.zero,
            constraints: const BoxConstraints(minWidth: 28, minHeight: 28),
            icon: const Icon(Icons.refresh_rounded,
                size: 16, color: NrispBrand.muted),
            tooltip: 'رمز تازه',
            onPressed: _load,
          ),
        ),
        const SizedBox(height: 8),
        SizedBox(
          height: 36,
          child: ElevatedButton(
            onPressed: () => _copy(
                _password.isEmpty ? _id : '$_id  $_password'),
            style: ElevatedButton.styleFrom(
              backgroundColor: NrispBrand.orange,
              foregroundColor: Colors.white,
              elevation: 0,
              padding: const EdgeInsets.symmetric(horizontal: 12),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(10),
              ),
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: const [
                Icon(Icons.send_rounded, size: 15, color: Colors.white),
                SizedBox(width: 7),
                Text(
                  'ارسال شناسه و رمز',
                  style: TextStyle(fontSize: 12, fontWeight: FontWeight.w700),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _valueRow({
    required String label,
    required String value,
    required VoidCallback onCopy,
    Widget? trailing,
  }) {
    return Container(
      padding: const EdgeInsets.fromLTRB(6, 6, 11, 6),
      decoration: BoxDecoration(
        color: NrispBrand.row,
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: NrispBrand.line),
      ),
      child: Row(
        children: [
          if (trailing != null) trailing,
          Expanded(
            child: FittedBox(
              fit: BoxFit.scaleDown,
              alignment: Alignment.centerRight,
              child: Text(
                value,
                style: const TextStyle(
                  fontSize: 15,
                  fontWeight: FontWeight.w700,
                  color: NrispBrand.text,
                  letterSpacing: 1.2,
                ),
              ),
            ),
          ),
          const SizedBox(width: 8),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 9, vertical: 4),
            decoration: BoxDecoration(
              color: NrispBrand.orangeFaint,
              borderRadius: BorderRadius.circular(20),
            ),
            child: Text(
              label,
              style: const TextStyle(
                fontSize: 10.5,
                fontWeight: FontWeight.w700,
                color: NrispBrand.orangeSoft,
              ),
            ),
          ),
          IconButton(
            padding: EdgeInsets.zero,
            constraints: const BoxConstraints(minWidth: 28, minHeight: 28),
            icon: const Icon(Icons.copy_rounded,
                size: 15, color: NrispBrand.muted),
            tooltip: 'کپی',
            onPressed: onCopy,
          ),
        ],
      ),
    );
  }

  // ------------------------------------------------------------ فهرست

  Widget _menu() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        _menuRow(
            icon: Icons.monitor_outlined,
            title: 'نمایش دادن',
            onTap: DesktopTabPage.onAddSetting),
        _menuRow(
            icon: Icons.person_outline_rounded,
            title: 'پروفایل',
            onTap: DesktopTabPage.onAddSetting),
        _menuRow(
            icon: Icons.info_outline_rounded,
            title: 'دربارهٔ برنامه',
            onTap: DesktopTabPage.onAddSetting),
        _menuRow(
            icon: Icons.language_rounded,
            title: 'وب‌سایت موسسه',
            onTap: () => launchUrlString('https://$nrispDomain')),
        const SizedBox(height: 6),
        _serverRow(),
      ],
    );
  }

  Widget _menuRow({
    required IconData icon,
    required String title,
    required VoidCallback onTap,
  }) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Material(
        color: NrispBrand.card,
        borderRadius: BorderRadius.circular(11),
        child: InkWell(
          borderRadius: BorderRadius.circular(11),
          onTap: onTap,
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 11),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(11),
              border: Border.all(color: NrispBrand.line),
            ),
            child: Row(
              children: [
                Icon(icon, size: 16, color: NrispBrand.orange),
                const SizedBox(width: 9),
                Expanded(
                  child: Text(
                    title,
                    style: const TextStyle(
                      fontSize: 12.5,
                      color: NrispBrand.text,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
                const Icon(Icons.chevron_left_rounded,
                    size: 16, color: NrispBrand.muted),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _serverRow() {
    final status = stateGlobal.svcStatus.value;
    final Color dot;
    final String label;
    if (status == SvcStatus.ready) {
      dot = NrispBrand.green;
      label = 'سرورهای عمومی';
    } else if (status == SvcStatus.connecting) {
      dot = NrispBrand.orangeSoft;
      label = 'در حال آماده‌سازی';
    } else {
      dot = NrispBrand.red;
      label = 'سرویس فعال نیست';
    }
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
      decoration: BoxDecoration(
        color: NrispBrand.card,
        borderRadius: BorderRadius.circular(11),
        border: Border.all(color: NrispBrand.line),
      ),
      child: Row(
        children: [
          Container(
            width: 9,
            height: 9,
            decoration: BoxDecoration(color: dot, shape: BoxShape.circle),
          ),
          const SizedBox(width: 9),
          Expanded(
            child: Text(
              label,
              style: const TextStyle(fontSize: 12, color: NrispBrand.text),
            ),
          ),
          Text(
            'آماده',
            style: TextStyle(
              fontSize: 11,
              fontWeight: FontWeight.w700,
              color: dot,
            ),
          ),
        ],
      ),
    );
  }

  // ------------------------------------------------------------- پابرگ

  Widget _footer() {
    return Column(
      children: const [
        Text(
          nrispCompanyFa,
          textAlign: TextAlign.center,
          style: TextStyle(fontSize: 10, color: NrispBrand.muted, height: 1.5),
        ),
        SizedBox(height: 3),
        Text(
          nrispDomain,
          style: TextStyle(
            fontSize: 10.5,
            color: NrispBrand.orange,
            fontWeight: FontWeight.w700,
            letterSpacing: 0.4,
          ),
        ),
      ],
    );
  }
}
