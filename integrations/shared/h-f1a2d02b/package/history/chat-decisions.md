# Extracted conversation evidence

Messages are identified by stable local keys; message timestamps/remote IDs were unavailable. Quotations marked as summaries must not be treated as verbatim.

## D-FRACTION
Type: user_explicit
Statement/excerpt: روش ما درصد پیشرفت اکسل × حجم کل MSP هست
Effect: Preserve Number9; use full precision actual fraction.
Supersedes: None

## D-DECREASE-OLD
Type: user_explicit
Statement/excerpt: هر دو کاهش طبق اکسل اعمال شود
Effect: Historical only; revoked.
Supersedes: None

## D-NONNEGATIVE
Type: user_explicit
Statement/excerpt: این دو مورد منفی رو به مقدار هفته قبل برگردون که اختلاف هیچ ردیفی منفی نباشه
Effect: UID528 retains11020; UID634 retains101000 then increases to103112 on25.
Supersedes: D-DECREASE-OLD

## D-TRANSFER
Type: user_explicit
Statement/excerpt: سمنت برد به پیمانکار مادر (سیوان) و کلمپ به آران سیج منتقل شده است
Effect: Execution transfer only; preserve project tasks and prior quantities.
Supersedes: None

## D-DATE17
Type: user_explicit
Statement/excerpt: ۱۷ آبان، طبق پیام من
Effect: Overrides18Aban filenames.
Supersedes: None

## D-DATE25
Type: user_explicit
Statement/excerpt: بله، ۲۵ آبان
Effect: Report cutoff; does not change native status date.
Supersedes: None

## D-PERIOD
Type: user_explicit
Statement/excerpt: اختلاف ۱۷ تا ۲۵ آبان
Effect: Period quantities from two MSP snapshots.
Supersedes: None

## D-PDF23
Type: user_explicit
Statement/excerpt: تاریخ گزارش 23 هست و داده ها بروز هستن
Effect: Duplicate agriculture PDF is current; needed crew is not attendance.
Supersedes: None

## D-STAFF
Type: user_explicit
Statement/excerpt: ثابت ها همیشه هستند؛ سعید و منتظریان شنبه تا سه‌شنبه معمولاً؛ صفاری شنبه‌ها
Effect: 5fixed+4variable; unknown fourth schedule and category split; no fabricated daily mean.
Supersedes: None

## D-EMPLOYER-SUPPLY
Type: user_qualified
Statement/excerpt: احتمالا به دلیل تامین کارفرمایی هست
Effect: Probable explanation, not confirmed procurement allocation.
Supersedes: None

## D-NORMALIZE
Type: calculation
Statement/excerpt: full precision fraction×Number9; reject inconsistent fractions
Effect: Calculation implementation, not a new user instruction.
Supersedes: None