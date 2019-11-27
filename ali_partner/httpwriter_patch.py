from aiohttp import http_writer
from ali_partner.logger import logger


def _write_no_exception(self, chunk: bytes) -> None:
    try:
        self.original_write(chunk)
    except ConnectionResetError as exc:
        logger.debug('ConnectionResetError exception suppressed')


def patch_streamwriter():
    http_writer.StreamWriter.original_write = http_writer.StreamWriter._write
    http_writer.StreamWriter._write = _write_no_exception
    logger.warning('StreamWriter patched to suppress ConnectionResetError\'s')
