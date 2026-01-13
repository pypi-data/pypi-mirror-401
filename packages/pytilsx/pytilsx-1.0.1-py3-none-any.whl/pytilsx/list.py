def sortbynum(nums:list | tuple):
    """Sorting a list by number from largest to smallest without inversion"""
    a = list(nums)
    n = len(a)
    if n <= 1:
        return a.copy()

    # separate negatives and non-negatives (store magnitudes for negatives)
    negs = []
    pos = []
    for x in a:
        xi = int(x)
        if xi < 0:
            negs.append(-xi)
        else:
            pos.append(xi)

    def _radix_nonneg(lst):
        if not lst:
            return []
        out = list(lst)          # buffer A
        buf = [0] * len(out)     # buffer B
        # find max to know number of bytes to process
        maxv = 0
        for v in out:
            if v > maxv:
                maxv = v
        if maxv == 0:
            return out
        shift = 0
        mask = 0xFF
        # Reuse counts allocation inside loop by recreating list (fast in CPython)
        while (maxv >> shift) != 0:
            counts = [0] * 256
            # count digits
            for v in out:
                counts[(v >> shift) & mask] += 1
            # prefix sums -> starting indices
            total = 0
            for i in range(256):
                c = counts[i]
                counts[i] = total
                total += c
            # scatter (stable)
            for v in out:
                idx = (v >> shift) & mask
                buf[counts[idx]] = v
                counts[idx] += 1
            # swap buffers
            out, buf = buf, out
            shift += 8
        return out

    sorted_pos = _radix_nonneg(pos)
    sorted_negs = _radix_nonneg(negs)

    # negatives: reverse order and reapply sign
    res = []
    for i in range(len(sorted_negs) - 1, -1, -1):
        res.append(-sorted_negs[i])
    res.extend(sorted_pos)
    return res

def sortbystrlen(_list:list, revers:bool = False):
    """Sorting a list item by its length from largest to smallest without inversion"""
    if _list == []:
        return []

    outlist = _list.copy()
    n = len(outlist)
    
    for i in range(n):
        for j in range(0, n - i - 1):
            if (not revers and len(outlist[j]) > len(outlist[j + 1])) or (revers and len(outlist[j]) < len(outlist[j + 1])):
                outlist[j], outlist[j + 1] = outlist[j + 1], outlist[j]
    
    return outlist