import 'package:flutter/material.dart';

class PrivacyPolicyScreen extends StatelessWidget {
  const PrivacyPolicyScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Privacy Policy')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: const [
          _H('Introduction'),
          _P('This Privacy Policy explains how Depth Note collects, uses, and protects information when you use the handwriting and AI features.'),
          _P('This policy is provided by Bisan Idrees (Israel).'),
          _H('Data We Collect'),
          _LI([
            'Account data (email, user ID) via Firebase Authentication.',
            'Purchase status via RevenueCat (entitlements, not full receipts). We do not receive your full payment details.',
            'Crash and usage analytics via Firebase Crashlytics and Firebase Analytics (which may include device and app metadata).',
            'Content you submit to AI (e.g., prompts, questions, and images you choose to process). This may be sent to AI providers (such as Alibaba Cloud Qwen and DeepSeek) and to a language detection service (DetectLanguage) solely to fulfill your requests.',
            'Your notes and images: these are stored locally on your device unless you export or share them. We do not operate a cloud database for your personal note content.',
          ]),
          _H('How We Use Data'),
          _LI([
            'Authenticate users and provide subscription features.',
            'Process AI requests and return answers you ask for.',
            'Improve reliability, diagnose crashes, and prevent abuse.',
          ]),
          _H('Data Sharing'),
          _P('We share necessary data with service providers: Firebase (authentication, analytics, crash reporting), RevenueCat (purchase management), AI providers (such as Alibaba Cloud Qwen and DeepSeek), and DetectLanguage (when language detection is used). We do not sell personal information or share it for advertising purposes.'),
          _H('Legal Basis and Region-Specific Rights'),
          _P('Where applicable (e.g., EU/UK), we process data to perform the service you request, to fulfill subscriptions, and to improve the app. You may have rights to access, correct, or delete your data and to object or restrict certain processing.'),
          _H('User Controls'),
          _LI([
            'Delete account: In the app, go to Settings → Delete account to permanently remove your account and associated data we control.',
            'Manage subscription: Use the App Store or Play Store subscription settings. Deleting your account does not cancel your subscription.',
            'Export/Deletion requests: Contact us to request a data export or deletion for data held by our providers (subject to verification).'
          ]),
          _H('Children'),
          _P('This app is not directed to children under 13 (or the minimum age in your jurisdiction). Do not use the service if you are under the applicable minimum age.'),
          _H('Security'),
          _P('We use industry-standard security measures. No method is 100% secure.'),
          _H('Changes'),
          _P('We may update this policy. Material changes will be posted in-app and on our website. Continued use constitutes acceptance.'),
          _H('Contact'),
          _P('For privacy questions or requests, contact: Bisan Idrees (Israel) – gmaildepthnoteapp@gmail.com'),
        ],
      ),
    );
  }
}

class _H extends StatelessWidget {
  const _H(this.text);
  final String text;
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(top: 16, bottom: 8),
      child: Text(text,
          style: Theme.of(context)
              .textTheme
              .titleMedium
              ?.copyWith(fontWeight: FontWeight.bold)),
    );
  }
}

class _P extends StatelessWidget {
  const _P(this.text);
  final String text;
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Text(text),
    );
  }
}

class _LI extends StatelessWidget {
  const _LI(this.items);
  final List<String> items;
  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        for (final i in items)
          Padding(
            padding: const EdgeInsets.only(bottom: 6),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('• '),
                Expanded(child: Text(i)),
              ],
            ),
          ),
      ],
    );
  }
}
