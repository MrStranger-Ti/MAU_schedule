from datetime import date
from typing import Callable, Any, Iterable
from zoneinfo import ZoneInfo

import pytest
from django.contrib.auth import get_user_model

from mau_auth.models import MauUser
from notes.models import Note

User: type[MauUser] = get_user_model()
