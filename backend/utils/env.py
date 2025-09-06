def mask_middle(s: str) -> str:
    """
    中间打码(保持原长度):
    - 长度 <= 4: 全部 *
    - 其他: 前后各保留约 1/3（>=1），中间至少 2 位打码
      打码段使用重复 '**' 生成并截断，确保总长度不变
    """
    if not s:
        return s
    n = len(s)
    if n <= 4:
        return "*" * n

    base = max(1, n // 3)
    prefix_len = base
    suffix_len = base
    masked_len = n - prefix_len - suffix_len

    # 确保中间至少 2 位被打码
    if masked_len < 2:
        # 收缩前后保留长度
        available = n - 2  # 预留 2 位作为打码
        prefix_len = available // 2
        suffix_len = available - prefix_len
        masked_len = 2

    prefix = s[:prefix_len]
    suffix = s[-suffix_len:] if suffix_len > 0 else ""
    # 生成打码段（用 ** 重复并截断以适配长度）
    masked_section = ("**" * ((masked_len + 1) // 2))[:masked_len]
    return f"{prefix}{masked_section}{suffix}"
