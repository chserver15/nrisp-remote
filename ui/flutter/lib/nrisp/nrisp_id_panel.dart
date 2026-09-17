// ---------------------------------------------------------------------------
// صفحهٔ اصلی اختصاصی — موسسه تحقیقات سیاست علمی کشور
// این پنل جای لوگو، شناسه، رمز و وضعیت سرویس را در صفحهٔ اصلی می‌گیرد و
// با زبان راست‌به‌چپ، رنگ‌های سازمانی و کارت‌های گرد طراحی شده است.
// ---------------------------------------------------------------------------

import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_hbb/common.dart';
import 'package:flutter_hbb/desktop/pages/desktop_tab_page.dart';
import 'package:flutter_hbb/models/platform_model.dart';
import 'package:flutter_hbb/models/state_model.dart';

/// نام نمایشی برنامه (فارسی)
const String nrispAppNameFa = 'دسترسی راه دور موسسه';

/// نام سازمان
const String nrispCompanyFa = 'موسسه تحقیقات سیاست علمی کشور';

/// نشانی سایت سازمان
const String nrispDomain = 'nrisp.ac.ir';

/// رنگ‌های سازمانی موسسه
class NrispBrand {
  static const Color blue = Color(0xFF0E3091);
  static const Color blueDeep = Color(0xFF0A2570);
  static const Color blueLight = Color(0xFF2C5AC4);
  static const Color orange = Color(0xFFE89B25);
  static const Color ink = Color(0xFF16222E);
  static const Color muted = Color(0xFF7A8A98);
  static const Color line = Color(0xFFE4EBF1);
  static const Color cardDark = Color(0xFF1B2430);
  static const Color softBlue = Color(0xFFEEF3FB);
  static const Color green = Color(0xFF1E9E6A);
  static const Color red = Color(0xFFD9534F);
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
    return Directionality(
      textDirection: TextDirection.rtl,
      child: Padding(
        padding: const EdgeInsets.fromLTRB(12, 14, 12, 16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            _hero(),
            const SizedBox(height: 14),
            _idCard(),
            const SizedBox(height: 10),
            _passwordCard(),
            const SizedBox(height: 12),
            _actionRow(),
            const SizedBox(height: 12),
            _hintCard(),
            const SizedBox(height: 16),
            _footer(),
          ],
        ),
      ),
    );
  }

  // ------------------------------------------------------------- سرصفحهٔ رنگی

  Widget _hero() {
    final status = stateGlobal.svcStatus.value;
    final Color dot;
    final String label;
    if (status == SvcStatus.ready) {
      dot = NrispBrand.green;
      label = 'آمادهٔ دریافت اتصال';
    } else if (status == SvcStatus.connecting) {
      dot = NrispBrand.orange;
      label = 'در حال آماده‌سازی';
    } else {
      dot = NrispBrand.red;
      label = 'سرویس فعال نیست';
    }
    return Container(
      padding: const EdgeInsets.fromLTRB(14, 14, 14, 13),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          begin: Alignment.topRight,
          end: Alignment.bottomLeft,
          colors: [NrispBrand.blueLight, NrispBrand.blue, NrispBrand.blueDeep],
        ),
        borderRadius: BorderRadius.circular(18),
        boxShadow: [
          BoxShadow(
            color: NrispBrand.blue.withOpacity(0.28),
            blurRadius: 18,
            offset: const Offset(0, 6),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                width: 46,
                height: 46,
                padding: const EdgeInsets.all(6),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(13),
                ),
                child: loadIcon(32),
              ),
              const SizedBox(width: 11),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      nrispAppNameFa,
                      style: TextStyle(
                        fontSize: 15,
                        fontWeight: FontWeight.w800,
                        color: Colors.white,
                        height: 1.35,
                      ),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                    const SizedBox(height: 3),
                    Text(
                      nrispCompanyFa,
                      style: const TextStyle(
                        fontSize: 10.5,
                        color: Color(0xFFD5E0F6),
                        height: 1.3,
                      ),
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.16),
              borderRadius: BorderRadius.circular(20),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Container(
                  width: 7,
                  height: 7,
                  decoration: BoxDecoration(color: dot, shape: BoxShape.circle),
                ),
                const SizedBox(width: 7),
                Text(
                  label,
                  style: const TextStyle(
                    fontSize: 11,
                    color: Colors.white,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  // ------------------------------------------------------------ کارت شناسه

  Widget _idCard() {
    return Container(
      padding: const EdgeInsets.fromLTRB(14, 12, 14, 12),
      decoration: BoxDecoration(
        color: _card,
        borderRadius: BorderRadius.circular(18),
        border: Border.all(color: _isDark ? Colors.white12 : NrispBrand.line),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(_isDark ? 0.30 : 0.05),
            blurRadius: 18,
            offset: const Offset(0, 5),
          ),
        ],
      ),
      child: Column(
        children: [
          Row(
            children: [
              Icon(Icons.badge_outlined, size: 15, color: NrispBrand.orange),
              const SizedBox(width: 6),
              Text(
                'شناسهٔ این دستگاه',
                style: TextStyle(fontSize: 11.5, color: _sub),
              ),
            ],
          ),
          const SizedBox(height: 8),
          FittedBox(
            fit: BoxFit.scaleDown,
            child: Text(
              _id.isEmpty ? '...' : _id,
              style: const TextStyle(
                fontSize: 26,
                fontWeight: FontWeight.w800,
                color: NrispBrand.blue,
                letterSpacing: 2.0,
                height: 1.2,
              ),
            ),
          ),
          const SizedBox(height: 9),
          _chip(
            icon: Icons.copy_rounded,
            text: 'کپی شناسه',
            onTap: () {
              if (_id.isEmpty) return;
              Clipboard.setData(ClipboardData(text: _id));
              showToast(translate('Copied'));
            },
            filled: true,
          ),
        ],
      ),
    );
  }

  // -------------------------------------------------------------- کارت رمز

  Widget _passwordCard() {
    return Container(
      padding: const EdgeInsets.fromLTRB(14, 12, 14, 12),
      decoration: BoxDecoration(
        color: _isDark ? Colors.white10 : NrispBrand.softBlue,
        borderRadius: BorderRadius.circular(18),
      ),
      child: Column(
        children: [
          Row(
            children: [
              Icon(Icons.lock_outline_rounded, size: 15, color: NrispBrand.orange),
              const SizedBox(width: 6),
              Text('رمز عبور یک‌بارمصرف',
                  style: TextStyle(fontSize: 11.5, color: _sub)),
            ],
          ),
          const SizedBox(height: 8),
          FittedBox(
            fit: BoxFit.scaleDown,
            child: Text(
              _password.isEmpty ? '------' : _password,
              style: TextStyle(
                fontSize: 22,
                fontWeight: FontWeight.w800,
                letterSpacing: 4,
                color: _title,
                height: 1.2,
              ),
            ),
          ),
          const SizedBox(height: 9),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              _chip(
                icon: Icons.copy_rounded,
                text: 'کپی رمز',
                onTap: () {
                  if (_password.isEmpty) return;
                  Clipboard.setData(ClipboardData(text: _password));
                  showToast(translate('Copied'));
                },
                filled: true,
              ),
              const SizedBox(width: 8),
              _chip(
                icon: Icons.refresh_rounded,
                text: 'رمز تازه',
                onTap: _load,
                filled: false,
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _chip({
    required IconData icon,
    required String text,
    required VoidCallback onTap,
    required bool filled,
  }) {
    final Color bg = filled
        ? (_isDark ? Colors.white12 : Colors.white)
        : (_isDark ? Colors.white10 : NrispBrand.blue);
    final Color fg = filled
        ? NrispBrand.blue
        : (_isDark ? Colors.white : Colors.white);
    return Material(
      color: Colors.transparent,
      child: InkWell(
        borderRadius: BorderRadius.circular(20),
        onTap: onTap,
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 13, vertical: 7),
          decoration: BoxDecoration(
            color: bg,
            borderRadius: BorderRadius.circular(20),
            border: Border.all(
              color: filled
                  ? (_isDark ? Colors.white24 : NrispBrand.line)
                  : Colors.transparent,
            ),
          ),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(icon, size: 14, color: fg),
              const SizedBox(width: 6),
              Text(
                text,
                style: TextStyle(
                  fontSize: 11.5,
                  color: fg,
                  fontWeight: FontWeight.w700,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  // ------------------------------------------------------------- دکمه‌های کار

  Widget _actionRow() {
    return Row(
      children: [
        Expanded(
          child: ElevatedButton(
            onPressed: () {
              final text = _password.isEmpty ? _id : '$_id  $_password';
              if (text.trim().isEmpty) return;
              Clipboard.setData(ClipboardData(text: text));
              showToast(translate('Copied'));
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: NrispBrand.orange,
              foregroundColor: Colors.white,
              elevation: 0,
              padding: const EdgeInsets.symmetric(vertical: 12),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(13),
              ),
            ),
            child: const Text(
              'ارسال شناسه و رمز',
              style: TextStyle(fontSize: 12.5, fontWeight: FontWeight.w700),
            ),
          ),
        ),
        const SizedBox(width: 9),
        Expanded(
          child: OutlinedButton(
            onPressed: DesktopTabPage.onAddSetting,
            style: OutlinedButton.styleFrom(
              padding: const EdgeInsets.symmetric(vertical: 12),
              backgroundColor: _isDark ? Colors.white10 : Colors.white,
              side: BorderSide(color: _isDark ? Colors.white24 : NrispBrand.line),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(13),
              ),
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(Icons.tune_rounded, size: 15, color: _title),
                const SizedBox(width: 6),
                Text(
                  'تنظیمات',
                  style: TextStyle(
                    fontSize: 12.5,
                    color: _title,
                    fontWeight: FontWeight.w700,
                  ),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  // ---------------------------------------------------------------- راهنما

  Widget _hintCard() {
    return Container(
      padding: const EdgeInsets.fromLTRB(13, 12, 13, 12),
      decoration: BoxDecoration(
        color: _isDark
            ? Colors.white.withOpacity(0.05)
            : NrispBrand.orange.withOpacity(0.10),
        borderRadius: BorderRadius.circular(14),
        border: Border.all(
          color: _isDark ? Colors.white12 : NrispBrand.orange.withOpacity(0.35),
        ),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Icon(Icons.support_agent_rounded,
              size: 17, color: NrispBrand.orange),
          const SizedBox(width: 8),
          Expanded(
            child: Text(
              'برای آنکه پشتیبانی موسسه به این رایانه متصل شود، '
              'شناسه و رمز بالا را برای ایشان بفرستید. برای اتصال شما به '
              'دستگاهی دیگر، شناسهٔ آن دستگاه را در کادر «کنترل دسکتاپ میزبان» وارد کنید.',
              style: TextStyle(fontSize: 11, color: _title, height: 1.65),
            ),
          ),
        ],
      ),
    );
  }

  Widget _footer() {
    return Column(
      children: [
        Text(
          nrispCompanyFa,
          textAlign: TextAlign.center,
          style: TextStyle(fontSize: 10.5, color: _sub, height: 1.5),
        ),
        const SizedBox(height: 2),
        Text(
          nrispDomain,
          style: const TextStyle(
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
