// ---------------------------------------------------------------------------
// ستون کنار برنامه — موسسه تحقیقات سیاست علمی کشور
// چیدمان، پویا و ضد بیرون‌زدگی؛ پشتیبان هر دو پوستهٔ روشن و تیره.
// ---------------------------------------------------------------------------

import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_hbb/common.dart';
import 'package:flutter_hbb/desktop/pages/desktop_setting_page.dart';
import 'package:flutter_hbb/desktop/pages/desktop_tab_page.dart';
import 'package:flutter_hbb/models/platform_model.dart';
import 'package:flutter_hbb/models/state_model.dart';

/// نام نمایشی برنامه (فارسی)
const String nrispAppNameFa = 'دسترسی راه دور موسسه';

/// نام سازمان
const String nrispCompanyFa = 'موسسه تحقیقات سیاست علمی کشور';

/// نشانی سایت سازمان
const String nrispDomain = 'nrisp.ac.ir';

/// رنگ سازمانی روی هر دو پوسته
const Color nrispOrange = Color(0xFFFB4201);
const Color nrispOrangeSoft = Color(0xFFFF7A3D);

class NrispIdPanel extends StatefulWidget {
  const NrispIdPanel({Key? key}) : super(key: key);

  @override
  State<NrispIdPanel> createState() => _NrispIdPanelState();
}

class _NrispIdPanelState extends State<NrispIdPanel> {
  String _id = '';
  String _password = '';
  String _version = '';
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    _load();
    _timer = Timer.periodic(const Duration(seconds: 2), (_) => _load());
    bind.mainGetVersion().then((v) {
      if (mounted) setState(() => _version = v);
    }).catchError((_) {});
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

  // ------------------------------------------------------------------ رنگ‌ها

  bool get _dark => Theme.of(context).brightness == Brightness.dark;
  Color get _bg => _dark ? const Color(0xFF191C22) : const Color(0xFFF4F6F9);
  Color get _card => _dark ? const Color(0xFF20242B) : Colors.white;
  Color get _rowBg => _dark ? const Color(0xFF262B33) : const Color(0xFFF5F6F8);
  Color get _line => _dark ? const Color(0xFF2C323B) : const Color(0xFFE3E7EE);
  Color get _text => _dark ? const Color(0xFFF2F4F7) : const Color(0xFF16222E);
  Color get _muted => _dark ? const Color(0xFF98A2B0) : const Color(0xFF77808C);
  Color get _faint =>
      _dark ? const Color(0x1AFB4201) : const Color(0x14FB4201);

  // ------------------------------------------------------------------ بدنه

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(builder: (context, c) {
      final win = MediaQuery.of(context).size.width;
      double width = win >= 1360
          ? 340
          : win >= 1120
              ? 310
              : 280;
      if (c.maxWidth.isFinite && c.maxWidth < width) {
        width = c.maxWidth;
      }
      return Container(
        width: width,
        decoration: BoxDecoration(
          color: _bg,
          border: Border(
            left: BorderSide(color: _line),
          ),
        ),
        child: SingleChildScrollView(
          padding: const EdgeInsets.fromLTRB(12, 14, 12, 16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              _brand(),
              const SizedBox(height: 16),
              _sectionTitle('دسکتاپ شما'),
              const SizedBox(height: 8),
              _desktopCard(),
              const SizedBox(height: 14),
              _serviceRow(),
              const SizedBox(height: 16),
              _sectionTitle('تنظیمات'),
              const SizedBox(height: 8),
              _settingsList(),
              const SizedBox(height: 16),
              _sectionTitle('پوسته'),
              const SizedBox(height: 8),
              _themeRow(),
              const SizedBox(height: 18),
              _footer(),
            ],
          ),
        ),
      );
    });
  }

  // ---------------------------------------------------------------- سرصفحه

  Widget _brand() {
    return Row(
      children: [
        Container(
          width: 38,
          height: 38,
          padding: const EdgeInsets.all(5),
          decoration: BoxDecoration(
            color: _card,
            borderRadius: BorderRadius.circular(11),
            border: Border.all(color: _line),
          ),
          child: loadIcon(28),
        ),
        const SizedBox(width: 9),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                nrispAppNameFa,
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
                style: const TextStyle(
                  fontSize: 13,
                  fontWeight: FontWeight.w800,
                  color: nrispOrange,
                  height: 1.4,
                ),
              ),
              const SizedBox(height: 1),
              Text(
                nrispCompanyFa,
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
                style: TextStyle(fontSize: 9.5, color: _muted, height: 1.4),
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _sectionTitle(String t) {
    return Row(
      children: [
        Expanded(
          child: Text(
            t,
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
            style: TextStyle(
              fontSize: 11.5,
              fontWeight: FontWeight.w700,
              color: _muted,
            ),
          ),
        ),
      ],
    );
  }

  // -------------------------------------------------- کارت «دسکتاپ شما»

  Widget _desktopCard() {
    return Container(
      padding: const EdgeInsets.fromLTRB(10, 10, 10, 10),
      decoration: BoxDecoration(
        color: _card,
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: _line),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          _valueRow(
            label: 'شناسه',
            value: _id.isEmpty ? '···' : _id,
            big: true,
            onCopy: () => _copy(_id),
          ),
          const SizedBox(height: 8),
          _valueRow(
            label: 'رمز عبور',
            value: _password.isEmpty ? '······' : _password,
            onCopy: () => _copy(_password),
            trailing: IconButton(
              padding: EdgeInsets.zero,
              splashRadius: 16,
              constraints: const BoxConstraints(minWidth: 26, minHeight: 26),
              icon: Icon(Icons.refresh_rounded, size: 15, color: _muted),
              tooltip: 'رمز تازه',
              onPressed: _load,
            ),
          ),
          const SizedBox(height: 10),
          _orangeButton(
            icon: Icons.send_rounded,
            text: 'ارسال شناسه و رمز',
            onTap: () => _copy(_password.isEmpty ? _id : '$_id  $_password'),
          ),
        ],
      ),
    );
  }

  Widget _valueRow({
    required String label,
    required String value,
    required VoidCallback onCopy,
    Widget? trailing,
    bool big = false,
  }) {
    return Container(
      padding: const EdgeInsets.fromLTRB(8, 5, 8, 5),
      decoration: BoxDecoration(
        color: _rowBg,
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: _line),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
            decoration: BoxDecoration(
              color: _faint,
              borderRadius: BorderRadius.circular(20),
            ),
            child: Text(
              label,
              maxLines: 1,
              style: const TextStyle(
                fontSize: 10,
                fontWeight: FontWeight.w700,
                color: nrispOrange,
              ),
            ),
          ),
          const SizedBox(width: 8),
          Expanded(
            child: FittedBox(
              fit: BoxFit.scaleDown,
              alignment: Alignment.centerLeft,
              child: Text(
                value,
                maxLines: 1,
                style: TextStyle(
                  fontSize: big ? 17 : 14,
                  fontWeight: FontWeight.w800,
                  letterSpacing: 1.4,
                  color: _text,
                ),
              ),
            ),
          ),
          if (trailing != null) trailing,
          IconButton(
            padding: EdgeInsets.zero,
            splashRadius: 16,
            constraints: const BoxConstraints(minWidth: 26, minHeight: 26),
            icon: Icon(Icons.copy_rounded, size: 15, color: _muted),
            tooltip: 'کپی',
            onPressed: onCopy,
          ),
        ],
      ),
    );
  }

  Widget _orangeButton({
    required IconData icon,
    required String text,
    required VoidCallback onTap,
  }) {
    return SizedBox(
      height: 40,
      child: ElevatedButton(
        onPressed: onTap,
        style: ElevatedButton.styleFrom(
          backgroundColor: nrispOrange,
          foregroundColor: Colors.white,
          elevation: 0,
          padding: const EdgeInsets.symmetric(horizontal: 10),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(11),
          ),
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 15, color: Colors.white),
            const SizedBox(width: 7),
            Flexible(
              child: Text(
                text,
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
                style: const TextStyle(
                  fontSize: 12,
                  fontWeight: FontWeight.w700,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  // ------------------------------------------------------------ ردیف سرویس

  Widget _serviceRow() {
    final status = stateGlobal.svcStatus.value;
    final Color dot;
    final String label;
    if (status == SvcStatus.ready) {
      dot = const Color(0xFF2ECC71);
      label = 'سرویس فعال است';
    } else if (status == SvcStatus.connecting) {
      dot = nrispOrangeSoft;
      label = 'در حال آماده‌سازی';
    } else {
      dot = const Color(0xFFE5484D);
      label = 'سرویس فعال نیست';
    }
    return Container(
      padding: const EdgeInsets.fromLTRB(10, 7, 6, 7),
      decoration: BoxDecoration(
        color: _card,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: _line),
      ),
      child: Row(
        children: [
          Container(
            width: 9,
            height: 9,
            decoration: BoxDecoration(color: dot, shape: BoxShape.circle),
          ),
          const SizedBox(width: 8),
          Expanded(
            child: Text(
              label,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
              style: TextStyle(fontSize: 11.5, color: _text),
            ),
          ),
          TextButton(
            onPressed: () => start_service(status != SvcStatus.ready),
            style: TextButton.styleFrom(
              minimumSize: const Size(0, 26),
              padding: const EdgeInsets.symmetric(horizontal: 10),
              foregroundColor: nrispOrange,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(8),
              ),
            ),
            child: Text(
              status == SvcStatus.ready ? 'راه‌اندازی دوباره' : 'اجرای سرویس',
              maxLines: 1,
              style: const TextStyle(
                fontSize: 11,
                fontWeight: FontWeight.w700,
              ),
            ),
          ),
        ],
      ),
    );
  }

  // ---------------------------------------------------------- فهرست تنظیمات

  Widget _settingsList() {
    final rows = <List<Object>>[
      [Icons.settings_outlined, 'عمومی', SettingsTabKey.general],
      [Icons.lock_outline_rounded, 'امنیت', SettingsTabKey.safety],
      [Icons.lan_outlined, 'شبکه', SettingsTabKey.network],
      [Icons.monitor_outlined, 'نمایش دادن', SettingsTabKey.display],
      [Icons.print_outlined, 'چاپگر', SettingsTabKey.printer],
      [Icons.info_outline_rounded, 'دربارهٔ برنامه', SettingsTabKey.about],
    ];
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        for (final r in rows)
          _menuRow(
            icon: r[0] as IconData,
            title: r[1] as String,
            onTap: () =>
                DesktopTabPage.onAddSetting(initialPage: r[2] as SettingsTabKey),
          ),
      ],
    );
  }

  Widget _menuRow({
    required IconData icon,
    required String title,
    required VoidCallback onTap,
  }) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 7),
      child: Material(
        color: _card,
        borderRadius: BorderRadius.circular(11),
        child: InkWell(
          borderRadius: BorderRadius.circular(11),
          onTap: onTap,
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 9),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(11),
              border: Border.all(color: _line),
            ),
            child: Row(
              children: [
                Icon(icon, size: 16, color: nrispOrange),
                const SizedBox(width: 9),
                Expanded(
                  child: Text(
                    title,
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: TextStyle(
                      fontSize: 12,
                      color: _text,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
                Icon(Icons.chevron_left_rounded, size: 16, color: _muted),
              ],
            ),
          ),
        ),
      ),
    );
  }

  // ------------------------------------------------------------- پوسته

  Widget _themeRow() {
    Widget chip(String title, IconData icon, bool active, VoidCallback onTap) {
      return Expanded(
        child: Material(
          color: active ? _faint : _card,
          borderRadius: BorderRadius.circular(10),
          child: InkWell(
            borderRadius: BorderRadius.circular(10),
            onTap: onTap,
            child: Container(
              padding: const EdgeInsets.symmetric(vertical: 9),
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(10),
                border: Border.all(
                    color: active ? nrispOrange : _line,
                    width: active ? 1.4 : 1),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(icon,
                      size: 14, color: active ? nrispOrange : _muted),
                  const SizedBox(width: 6),
                  Text(
                    title,
                    maxLines: 1,
                    style: TextStyle(
                      fontSize: 11.5,
                      fontWeight: FontWeight.w700,
                      color: active ? nrispOrange : _muted,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      );
    }

    return Row(
      children: [
        chip('روشن', Icons.light_mode_outlined, !_dark,
            () => MyTheme.changeDarkMode(ThemeMode.light)),
        const SizedBox(width: 8),
        chip('تیره', Icons.dark_mode_outlined, _dark,
            () => MyTheme.changeDarkMode(ThemeMode.dark)),
      ],
    );
  }

  // ------------------------------------------------------------- پابرگ

  Widget _footer() {
    return Column(
      children: [
        Text(
          nrispCompanyFa,
          textAlign: TextAlign.center,
          style: TextStyle(fontSize: 9.5, color: _muted, height: 1.6),
        ),
        const SizedBox(height: 2),
        Text(
          nrispDomain,
          style: const TextStyle(
            fontSize: 10,
            color: nrispOrange,
            fontWeight: FontWeight.w700,
            letterSpacing: 0.4,
          ),
        ),
        if (_version.isNotEmpty) ...[
          const SizedBox(height: 4),
          Text(
            'نسخه: $_version',
            style: TextStyle(fontSize: 9.5, color: _muted),
          ),
        ],
      ],
    );
  }
}
