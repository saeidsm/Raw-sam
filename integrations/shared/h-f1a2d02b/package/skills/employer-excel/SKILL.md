---
name: employer-excel
description: Populate the Pardis employer workbook from the same reviewed data freeze as MSP, preserving template features and explicit data gaps.
---
# Employer Excel
Read ../../mappings/README.md and INPUTS.md at package root. Use ../../templates/employer-1405.07.28.xlsx as historical original and ../../examples/employer/after-1405.08.25.xlsx as latest preserved case. Do not treat cached template history as new observations.
## گردش کار مشترک
۱. دریافت یک‌باره؛ inventory/hash؛ ثبت source_id، دوره واقعی هر شرکت، قرارداد/ساختمان و وضعیت تایید.
۲. کنترل پوشش، واحد، درصد، مخرج، duplicateقبض و تعارض منابع؛ null برای نامعلوم.
۳. فقط اختلاف‌های موثر را سوال کن؛ تصمیم قبلی را دوباره نپرس. تصمیم جدید supersedes داشته باشد.
۴. frozen dataset با accepted record IDs و SHA256 منابع،نگاشت،تصمیم‌ها بساز. برگ‌های دارای تعارض حفظ/مسدود با reason؛ incomplete را complete ننام.
۵. MSP،اکسل،گزارش مدیریتی باید یک freeze_id مشترک مصرف کنند؛ هیچ ماژول تصمیم مستقل درباره داده مشترک نگیرد.
۶. کنترل output،بازگشایی،اختلاف دوره،حفظ قالب/برنامه؛ انتشار همراه coverage و سوال‌های باز. هر اصلاح بعدی freeze تازه است.

Exact cell inventory: ../../mappings/employer-cells.json. Summary UID mapping: employer-summary.json. The2258edit historical plan is in examples/evidence, plus staff-revision.json. New period requires new plan; never replay old values as current. Keep date cutoff separate from MSP status date.
Successful workflow used artifact-tool for cell authoring, then read-only extraction/verification of authored cells and native Excel COM application to a copy of the original. Full artifact export lost/failed unsupported native features and one export did not open in Excel; direct XML splicing also failed. These are not release paths. Preserve native workbook with Excel COM, CalculateFullRebuild, save/reopen, PDF export/visual check. Do not use openpyxl for saving templates; it discards extensions/charts. openpyxl here is read-only validation.
Staff revision is notes only; D8:I9 remain incomplete intentionally. Status: tested partial-data workbook, not fully complete or turnkey generalized adapter. Do not auto-fill delivery unknowns or nine-person daily attendance.
