
known_ports = [
    {
        'name': '$HTTP_PORTS',
        'ports': [80, 8000, 8080]
    },
    {
        'name': '$SHELLCODE_PORTS',
        'ports': list(range(0, 79)) + list(range(81, 65535))
    },
    {
        'name': '$ORACLE_PORTS',
        'ports': list(range(1024,65535))
    },
    {
        'name': '$SSH_PORTS',
        'ports': [22]
    },
    {
        'name': '$FTP_PORTS',
        'ports': [21, 2100, 3535]
    },
    {
        'name': '$SIP_PORTS',
        'ports': [5060,5061]
    },
    {
        'name': '$FILE_DATA_PORTS',
        'ports': []
    },
    {
        'name': '$GTP_PORTS',
        'ports': [2123, 2152, 3386]
    },
    {
        'name': '$AIM_SERVERS',
        'ports': []
    },
]