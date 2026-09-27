"""Fail fast with an actionable message when the database is unreachable.

Django reports a bad DATABASE_URL as either a DNS failure ("[Errno -2] Name or
service not known") or an auth failure, buried in a long traceback from
`manage.py migrate`. On Render that surfaces as "No open ports detected",
which gives no hint that the database is the problem at all.

This runs before migrate in the container CMD so the real cause is the last
line in the log.
"""

import os
import socket
from urllib.parse import urlparse

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand, CommandError
from django.db import connections


class Command(BaseCommand):
    help = 'Verify DATABASE_URL is set and its host resolves, then open a connection.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-dns',
            action='store_true',
            help='Skip the DNS check (useful when running behind a proxy).',
        )

    def handle(self, *args, **options):
        is_production = (
            os.environ.get('RENDER', '').lower() == 'true'
            or settings.DEBUG is False
        )

        if not is_production and not options['skip_dns']:
            # Local development runs on SQLite by design; nothing to verify.
            self.stdout.write(self.style.WARNING('preflight: not production, skipping checks.'))
            return

        raw = os.environ.get('DATABASE_URL', '').strip()
        if not raw:
            raise CommandError(self._hint('DATABASE_URL is not set.'))

        parsed = urlparse(raw)
        if parsed.scheme not in ('postgres', 'postgresql', 'psql'):
            raise CommandError(self._hint(
                'DATABASE_URL must be a PostgreSQL URL, got scheme {!r}.'.format(parsed.scheme)
            ))

        if not parsed.hostname:
            raise CommandError(self._hint('DATABASE_URL has no host.'))

        if not options['skip_dns']:
            try:
                socket.getaddrinfo(parsed.hostname, parsed.port or 5432)
            except socket.gaierror as exc:
                raise CommandError(self._hint(
                    'Cannot resolve database host {!r} ({}). The host does not exist, '
                    'so the database is gone or the connection string is wrong.'
                    .format(parsed.hostname, exc)
                ))

        try:
            connection = connections['default']
            connection.ensure_connection()
        except Exception as exc:
            raise CommandError(self._hint(
                'Could not connect to {}:{} as user {!r} - {}: {}'
                .format(
                    parsed.hostname,
                    parsed.port or 5432,
                    parsed.username,
                    type(exc).__name__,
                    exc,
                )
            ))

        self.stdout.write(self.style.SUCCESS(
            'preflight: connected to {}:{}'.format(parsed.hostname, parsed.port or 5432)
        ))

    @staticmethod
    def _hint(problem):
        return (
            '\n\n'
            '================================================================\n'
            'DATABASE PREFLIGHT FAILED\n'
            '{}\n'.format(problem) +
            '\n'
            'Render web services use an ephemeral filesystem, so a broken\n'
            'database cannot be worked around by falling back to SQLite - every\n'
            'user and appointment would be lost on the next restart.\n'
            '\n'
            'Fix: set DATABASE_URL in Render under\n'
            '  Dashboard -> mobi-mama -> Environment -> DATABASE_URL\n'
            '\n'
            'It must be a live PostgreSQL connection string, for example\n'
            '  postgresql://USER:PASSWORD@HOST/neondb?sslmode=require\n'
            '\n'
            'A free Render Postgres expires after 30 days; an external host\n'
            'such as Neon does not expire. Re-check the dashboard value - a\n'
            'stale connection string to a deleted database is the usual cause.\n'
            '================================================================'
        )
