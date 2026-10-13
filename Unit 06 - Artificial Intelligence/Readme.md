Analysis: Naive Bayes vs Keyword Rule for Spam Detection

The problem

Spam filtering decides whether an email is unwanted (spam) or legitimate (not spam). I compared two approaches: the Naive Bayes model from `spam_classifier.py`, which learns word patterns from labelled examples, and the fixed keyword rule from `emailClassifier.js`. I tested both on the same 20 handwritten emails (10 spam, 10 legitimate). The Naive Bayes model was trained on the script's 5 emails.

Results

Both approaches scored 60% accuracy. The keyword rule had precision 0.60 and recall 0.60: it missed 4 spam emails ("Claim your reward today", "Cheap meds…") and wrongly flagged 4 legitimate ones because "win" matched "Window" and "Winter", "cash" matched "cashier", and "selected" matched an interview invitation. Naive Bayes caught all 10 spam emails (recall 1.00) but flagged 8 of 10 legitimate emails as spam (precision 0.56). With only 5 training emails, three of them spam, it ignores unseen words and defaults towards spam. Its high recall comes mostly from over-flagging, not understanding.

Limitations

The training set is tiny, and the test set is small and written by me, not a public benchmark, so these numbers show the methods' behaviour, not their real-world accuracy. Neither method handles misspellings, context or evolving spam tactics. A real evaluation should use a dataset like UCI Spambase and report results on thousands of emails.

Ethical considerations

Blocking legitimate email has real costs: both methods wrongly flagged a job interview invitation. Spam filters should therefore be tuned to avoid false positives, and users should be able to review filtered mail. Training data can embed bias: models trained on narrow samples may unfairly flag writing styles, dialects, or non-native English, and may handle other languages poorly. Real email data also raises privacy and consent concerns, so training should use anonymised, consented or public corpora. Finally, a filter that silently deletes mail should never be the only safeguard.
