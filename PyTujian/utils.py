def format_size(size: int) -> str:
    _size = size
    _unit = 'B'
    if _size > 1000:
        _size /= 1024
        _unit = 'KB'
    if _size > 1000:
        _size /= 1024
        _unit = 'MB'
    if _size > 1000:
        _size /= 1024
        _unit = 'GB'
    if _size > 1000:
        _size /= 1024
        _unit = 'TB'
    if _size > 1000:
        _size /= 1024
        _unit = 'PB'
    if _size > 1000:
        _size /= 1024
        _unit = 'EB'
    if _size > 1000:
        _size /= 1024
        _unit = 'ZB'
    if _size > 1000:
        _size /= 1024
        _unit = 'YB'
    if _size > 1000:
        _size /= 1024
        _unit = 'BB'
    return '%0.2f %s' % (_size, _unit)
