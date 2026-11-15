---
name: msp-update
description: Update Pardis native MPP cumulative quantities from a reviewed shared data freeze; preserve formulas and schedule.
---
# Pardis MSP
Read ../../mappings/README.md, ../../history/decisions.json and ../../history/open-questions.json. This profile is not a generic %Complete import.
## گردش کار مشترک
۱. دریافت یک‌باره؛ inventory/hash؛ ثبت source_id، دوره واقعی هر شرکت، قرارداد/ساختمان و وضعیت تایید.
۲. کنترل پوشش، واحد، درصد، مخرج، duplicateقبض و تعارض منابع؛ null برای نامعلوم.
۳. فقط اختلاف‌های موثر را سوال کن؛ تصمیم قبلی را دوباره نپرس. تصمیم جدید supersedes داشته باشد.
۴. frozen dataset با accepted record IDs و SHA256 منابع،نگاشت،تصمیم‌ها بساز. برگ‌های دارای تعارض حفظ/مسدود با reason؛ incomplete را complete ننام.
۵. MSP،اکسل،گزارش مدیریتی باید یک freeze_id مشترک مصرف کنند؛ هیچ ماژول تصمیم مستقل درباره داده مشترک نگیرد.
۶. کنترل output،بازگشایی،اختلاف دوره،حفظ قالب/برنامه؛ انتشار همراه coverage و سوال‌های باز. هر اصلاح بعدی freeze تازه است.

Only Number5 leaf edits. Build plan with sourceSha256 and changes[{uid,name,old,new}], using msp-418.json after rechecking headers/identity. Enforce nonnegative deltas before calling helper (helper itself only rejects negative quantities, not decreases). Empty change set: verify and save dated copy separately; helper rejects empty plan. Preserve sidecars explicitly.
On Windows with licensed Project, use PowerShell5.1 `scripts/apply_quantity_plan.ps1 -Source <previous.mpp> -Plan <plan.json> -Output <new.mpp> -Audit <audit.json>`. Output and audit must not exist. Do not quit shared user applications. Native snapshots are authority; XML export is rounded and not formula-complete. Run ../../validation/validate.py for bundled regression; for new runs repeat its checks with new snapshots plus schedule/resource/baseline invariants. Do not call all resource and baseline objects fully verified by this helper.
Status: tested native mechanism and25Aban case, not an unattended universal importer. Full Excel-only replay of the earliest pair was not proven (28of76changed leaves covered); exact MPP replay was a separate regression.
