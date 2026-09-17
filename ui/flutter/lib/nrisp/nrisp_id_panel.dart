// ---------------------------------------------------------------------------
// پنل شناسهٔ دستگاه — نسخهٔ اختصاصی موسسه تحقیقات سیاست علمی کشور
// این فایل جای لوگو، شناسه، رمز و وضعیت سرویس را در صفحهٔ اصلی می‌گیرد.
// ---------------------------------------------------------------------------

import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_hbb/common.dart';
import 'package:flutter_hbb/desktop/pages/desktop_tab_page.dart';
import 'package:flutter_hbb/models/platform_model.dart';
import 'package:flutter_hbb/models/state_model.dart';

/// رنگ‌های سازمانی موسسه
class NrispBrand {
  static const Color blue = Color(0xFF0E3091);
  static const Color orange = Color(0xFFE89B25);
  static const Color ink = Color(0xFF16222E);
  static const Color muted = Color(0xFF7A8A98);
  static const Color line = Color(0xFFE4EBF1);
  static const Color cardDark = Color(0xFF1B2430);
  static const Color softBlue = Color(0xFFEEF3FB);
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
    // شناسه و رمز یک‌بارمصرف ممکن است از سمت سرویس تغییر کنند
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
      // سرویس ممکن است هنوز آماده نباشد
    }
  }

  bool get _isDark => Theme.of(context).brightness == Brightness.dark;
  Color get _card => _isDark ? NrispBrand.cardDark : Colors.white;
  Color get _title => _isDark ? Colors.white : NrispBrand.ink;
  Color get _sub => _isDark ? const Color(0xFF9BAAB8) : NrispBrand.muted;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(14, 18, 14, 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          _buildHeader(),
          const SizedBox(height: 16),
          _buildIdCard(),
          const SizedBox(height: 10),
          _buildPasswordRow(),
          const SizedBox(height: 16),
          _buildStatusRow(),
          const SizedBox(height: 16),
          _buildSettingsButton(),
          const SizedBox(height: 20),
          _buildFooter(),
        ],
      ),
    );
  }

  // --------------------------------------------------------------- سرصفحه

  Widget _buildHeader() {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        loadIcon(26),
        const SizedBox(width: 9),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                appName,
                style: TextStyle(
                    fontSize: 12.5,
                    fontWeight: FontWeight.w700,
                    color: _title,
                    height: 1.3),
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
              Text(
                'موسسه تحقیقات سیاست علمی کشور',
                style: TextStyle(fontSize: 9.5, color: _sub, height: 1.3),
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
            ],
          ),
        ),
      ],
    );
  }

  // ----------------------------------------------------------- کارت شناسه

  Widget _buildIdCard() {
    return Container(
      padding: const EdgeInsets.fromLTRB(14, 13, 14, 11),
      decoration: BoxDecoration(
        color: _card,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: _isDark ? Colors.white12 : NrispBrand.line),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(_isDark ? 0.30 : 0.06),
            blurRadius: 16,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Text(
            'شناسهٔ این دستگاه',
            style: TextStyle(fontSize: 11, color: _sub),
          ),
          const SizedBox(height: 6),
          FittedBox(
            fit: BoxFit.scaleDown,
            child: Text(
              _id.isEmpty ? '...' : _id,
              style: const TextStyle(
                fontSize: 25,
                fontWeight: FontWeight.w800,
                color: NrispBrand.blue,
                letterSpacing: 1.6,
                height: 1.2,
              ),
            ),
          ),
          const SizedBox(height: 8),
          _buildCopyChip(),
        ],
      ),
    );
  }

  Widget _buildCopyChip() {
    return Material(
      color: Colors.transparent,
      child: InkWell(
        borderRadius: BorderRadius.circular(20),
        onTap: () {
          if (_id.isEmpty) return;
          Clipboard.setData(ClipboardData(text: _id));
          showToast(translate('Copied'));
        },
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
          decoration: BoxDecoration(
            color: NrispBrand.softBlue,
            borderRadius: BorderRadius.circular(20),
          ),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(Icons.copy_rounded,
                  size: 13, color: NrispBrand.blue),
              const SizedBox(width: 6),
              Text('کپی شناسه',
                  style: const TextStyle(
                      fontSize: 11,
                      color: NrispBrand.blue,
                      fontWeight: FontWeight.w600)),
            ],
          ),
        ),
      ),
    );
  }

  // ------------------------------------------------------------- رمز ورود

  Widget _buildPasswordRow() {
    return Container(
      padding: const EdgeInsets.fromLTRB(12, 10, 8, 10),
      decoration: BoxDecoration(
        color: _isDark ? Colors.white10 : NrispBrand.softBlue.withOpacity(0.65),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('رمز یک‌بارمصرف',
                    style: TextStyle(fontSize: 9.5, color: _sub)),
                const SizedBox(height: 2),
                FittedBox(
                  fit: BoxFit.scaleDown,
                  child: Text(
                    _password.isEmpty ? '------' : _password,
                    style: TextStyle(
                        fontSize: 15,
                        fontWeight: FontWeight.w700,
                        letterSpacing: 2,
                        color: _title),
                  ),
                ),
              ],
            ),
          ),
          InkWell(
            borderRadius: BorderRadius.circular(8),
            onTap: _load,
            child: Padding(
              padding: const EdgeInsets.all(6),
              child: Icon(Icons.refresh_rounded, size: 16, color: _sub),
            ),
          ),
        ],
      ),
    );
  }

  // --------------------------------------------------------------- وضعیت

  Widget _buildStatusRow() {
    final status = stateGlobal.svcStatus.value;
    final Color color;
    final String label;
    if (status == SvcStatus.ready) {
      color = const Color(0xFF1E9E6A);
      label = 'آمادهٔ دریافت اتصال';
    } else if (status == SvcStatus.connecting) {
      color = NrispBrand.orange;
      label = 'در حال آماده‌سازی';
    } else {
      color = const Color(0xFFD9534F);
      label = 'سرویس فعال نیست';
    }
    return Row(
      children: [
        Container(
          width: 8,
          height: 8,
          decoration: BoxDecoration(color: color, shape: BoxShape.circle),
        ),
        const SizedBox(width: 8),
        Expanded(
          child: Text(label,
              style: TextStyle(fontSize: 11.5, color: _title),
              overflow: TextOverflow.ellipsis),
        ),
      ],
    );
  }

  // ------------------------------------------------------------- تنظیمات

  Widget _buildSettingsButton() {
    return OutlinedButton(
      onPressed: DesktopTabPage.onAddSetting,
      style: OutlinedButton.styleFrom(
        padding: const EdgeInsets.symmetric(vertical: 11),
        backgroundColor: _isDark ? Colors.white10 : Colors.white,
        side: BorderSide(color: _isDark ? Colors.white24 : NrispBrand.line),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.tune_rounded, size: 15, color: _title),
          const SizedBox(width: 7),
          Text('تنظیمات',
              style: TextStyle(
                  fontSize: 12.5, color: _title, fontWeight: FontWeight.w600)),
        ],
      ),
    );
  }

  Widget _buildFooter() {
    return Column(
      children: [
        Text('nrisp.ac.ir',
            style: TextStyle(fontSize: 10, color: _sub, letterSpacing: 0.3)),
      ],
    );
  }
}
