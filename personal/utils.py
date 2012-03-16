import re

from django.core.validators import RegexValidator

class HostnameValidator(RegexValidator):
    regex = re.compile(ur'^(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?))$', re.IGNORECASE)
