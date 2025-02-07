# Define suspicious threshold for domain age (e.g., less than 180 days = 6 months)
suspicious_threshold_domain = 180

status_descriptions = {
    'clientHold': "Domain is on hold and not currently resolving.",
    'clientTransferProhibited': "Domain cannot be transferred to another registrar.",
    'addPeriod': "Domain is in the add grace period after registration.",
    'clientDeleteProhibited': "Domain cannot be deleted from the registrar.",
    'serverHold': "Domain is delisted from the DNS system, not resolving.",
    'serverTransferProhibited': "Domain cannot be transferred between servers."
}