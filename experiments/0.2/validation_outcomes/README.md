# Validation outcomes

Validation outcomes may be acquired and hashed before scoring, but the outcome contents must remain sealed. A manifest or checksum is not the same as exposure of the validation file.

The outcome artifact can be released only after the prediction artifact has been frozen and checksummed, and a release-authorization record has been committed. Until then, `outcome_contents_available_to_scoring` must remain `false`.
