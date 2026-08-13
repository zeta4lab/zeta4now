from __future__ import annotations

import ipaddress
import mimetypes
import re
import sys
import warnings
from datetime import datetime
from filecmp import cmp
from pathlib import Path
from typing import BinaryIO
from urllib.parse import unquote, urlsplit

import yaml
from markdown_it import MarkdownIt
from markdown_it.token import Token
from PIL import Image, UnidentifiedImageError

ARTICLE_PATH_RE = re.compile(
    r"^news/([^/]+)/(?:[1-9]\d{3})/(?:0[1-9]|1[0-2])/([^/]+)\.md$"
)
FRONTMATTER_RE = re.compile(r"\A---\r?\n([\s\S]*?)\r?\n---\r?\n")
ATTRIBUTION_TEXT_RE = re.compile(
    r"^사진:\s*(.*?)\s*·\s*출처:\s*(https://\S+)\s*·\s*라이선스:\s*(.*?)$",
    re.IGNORECASE,
)
BARE_EXTERNAL_URL_RE = re.compile(
    r"(?i)(?<![\w])(?:(?:(?:https?|ftp):)?//[^\s<]+|www\.[^\s<]+)"
)
BARE_EMAIL_RE = re.compile(
    r"(?i)(?<![\w.+-])[a-z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-z0-9.-]+\.[a-z]{2,}"
)
ALLOWED_IMAGE_EXTENSIONS = {".webp", ".jpg", ".jpeg", ".png"}
VIDEO_EXTENSIONS = {
    ".mkv",
    ".avi",
    ".mpeg",
    ".mpg",
    ".ogv",
    ".wmv",
    ".flv",
    ".vob",
    ".y4m",
    ".rm",
    ".rmvb",
    ".mxf",
    ".h264",
    ".264",
    ".avc",
    ".h265",
    ".265",
    ".hevc",
    ".m4v",
    ".mjpeg",
    ".mjpg",
}
SHARED_BMFF_EXTENSIONS = {".mp4", ".mov", ".3gp", ".3g2", ".f4v"}
SHARED_MPEG_TS_EXTENSIONS = {".ts", ".mts", ".m2ts"}
MAX_MARKDOWN_BYTES = 1_000_000
MAX_IMAGE_BYTES = 10_000_000
MAX_IMAGE_PIXELS = 20_000_000
MAX_IMAGE_DIMENSION = 8_000
MAX_VIDEO_SCAN_BYTES = 1_000_000
COMMONMARK = MarkdownIt("commonmark")
EBML_HEADER = b"\x1a\x45\xdf\xa3"
ASF_HEADER = b"\x30\x26\xb2\x75\x8e\x66\xcf\x11\xa6\xd9\x00\xaa\x00\x62\xce\x6c"
ASF_STREAM_PROPERTIES = (
    b"\x91\x07\xdc\xb7\xb7\xa9\xcf\x11\x8e\xe6\x00\xc0\x0c\x20\x53\x65"
)
ASF_VIDEO_MEDIA = b"\xc0\xef\x19\xbc\x4d\x5b\xcf\x11\xa8\xfd\x00\x80\x5f\x5c\x44\x2b"
AI_DISCLOSURES = {
    "이 글은 공개 출처를 바탕으로 AI가 자동 생성했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.",
    "이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.",
}


def contains_html(tokens: list[Token]) -> bool:
    return any(
        token.type in {"html_block", "html_inline"}
        or contains_html(token.children or [])
        for token in tokens
    )


def plain_alt(image: Token) -> str:
    return "".join(
        token.content
        for token in image.children or []
        if token.type in {"text", "text_special", "code_inline"}
    )


def image_destination_syntax(value: str) -> str | None:
    value = value.strip()
    if not value.startswith("![") or "\n" in value or "\r" in value:
        return None
    depth = 1
    escaped = False
    for index, character in enumerate(value[2:], 2):
        if escaped:
            escaped = False
            continue
        if character == "\\":
            escaped = True
        elif character == "[":
            depth += 1
        elif character == "]":
            depth -= 1
            if depth == 0:
                if (
                    index + 2 > len(value)
                    or value[index + 1] != "("
                    or not value.endswith(")")
                ):
                    return None
                return value[index + 2 : -1]
    return None


def raw_image_path(value: str) -> str:
    value = value.strip()
    if value.startswith("<"):
        escaped = False
        for index, character in enumerate(value[1:], 1):
            if character == ">" and not escaped:
                return value[: index + 1]
            escaped = character == "\\" and not escaped
            if character != "\\":
                escaped = False
        return value

    depth = 0
    escaped = False
    for index, character in enumerate(value):
        if escaped:
            escaped = False
            continue
        if character == "\\":
            escaped = True
        elif character == "(":
            depth += 1
        elif character == ")" and depth:
            depth -= 1
        elif character.isspace() and depth == 0:
            return value[:index]
    return value


def valid_https_url(value: str) -> bool:
    if re.search(r"%(?![0-9A-Fa-f]{2})", value) or any(
        character.isspace() for character in value
    ):
        return False
    try:
        parsed = urlsplit(value)
        _port = parsed.port
        hostname = parsed.hostname or ""
        if parsed.username is not None or parsed.password is not None:
            return False
        try:
            ipaddress.ip_address(hostname)
        except ValueError:
            ascii_hostname = hostname.encode("idna").decode("ascii")
            labels = ascii_hostname.rstrip(".").split(".")
            if not labels or any(
                not label
                or len(label) > 63
                or label.startswith("-")
                or label.endswith("-")
                or not re.fullmatch(r"[A-Za-z0-9-]+", label)
                for label in labels
            ):
                return False
    except (UnicodeError, ValueError):
        return False
    return parsed.scheme == "https" and bool(hostname)


def valid_article_link(value: str) -> bool:
    return value.startswith("#") or valid_https_url(value)


def has_invalid_bare_link(tokens: list[Token]) -> bool:
    for parent in tokens:
        link_depth = 0
        for token in parent.children or []:
            if token.type == "link_open":
                link_depth += 1
            elif token.type == "link_close":
                link_depth -= 1
            elif token.type == "text" and link_depth == 0:
                if BARE_EMAIL_RE.search(token.content):
                    return True
                for match in BARE_EXTERNAL_URL_RE.finditer(token.content):
                    if not valid_article_link(match.group(0).rstrip(".,;:!?)]}")):
                        return True
    return False


def attribution_after(tokens: list[Token], inline_index: int) -> re.Match[str] | None:
    expected = ("paragraph_close", "paragraph_open", "inline", "paragraph_close")
    following = tokens[inline_index + 1 : inline_index + 5]
    if (
        len(following) != len(expected)
        or tuple(token.type for token in following) != expected
    ):
        return None
    inline = tokens[inline_index]
    attribution = following[2]
    if attribution.level != inline.level:
        return None
    children = attribution.children or []
    if [child.type for child in children] != ["em_open", "text", "em_close"]:
        return None
    return ATTRIBUTION_TEXT_RE.fullmatch(children[1].content)


def article_images(markdown: str) -> list[tuple[str, str, str, bool]]:
    tokens = COMMONMARK.parse(markdown)
    if contains_html(tokens):
        raise ValueError("원시 HTML은 허용하지 않습니다")
    if any(
        token.type == "link_open"
        and not valid_article_link(str(token.attrGet("href") or ""))
        for parent in tokens
        for token in (parent.children or [])
    ):
        raise ValueError("링크는 문서 내부 앵커 또는 유효한 HTTPS URL이어야 합니다")
    if has_invalid_bare_link(tokens):
        raise ValueError(
            "bare 외부 URL과 이메일 주소는 허용하지 않으며 HTTPS 링크를 사용해야 합니다"
        )

    images: list[tuple[str, str, str, bool]] = []
    for index, token in enumerate(tokens):
        if token.type != "inline":
            continue
        children = token.children or []
        image_tokens = [child for child in children if child.type == "image"]
        if not image_tokens:
            continue
        visible_children = [
            child for child in children if child.type != "text" or child.content.strip()
        ]
        if len(image_tokens) != 1 or visible_children != image_tokens:
            raise ValueError("사진은 문단에서 단독으로 사용해야 합니다")
        syntax = image_destination_syntax(token.content)
        if syntax is None:
            raise ValueError("사진은 한 줄 inline Markdown 문법만 사용할 수 있습니다")
        alt = plain_alt(image_tokens[0]).strip()
        if not alt:
            raise ValueError("사진 대체 텍스트가 비어 있습니다")
        attribution = attribution_after(tokens, index)
        attribution_valid = bool(
            attribution
            and attribution.group(1).strip()
            and valid_https_url(attribution.group(2))
            and attribution.group(3).strip()
        )
        images.append(
            (
                alt,
                (image_tokens[0].attrGet("src") or "").strip(),
                raw_image_path(syntax),
                attribution_valid,
            )
        )
    return images


def has_source_footer(markdown: str, require_disclosure: bool) -> bool:
    tokens = COMMONMARK.parse(markdown)
    source_headings = [
        token
        for index, token in enumerate(tokens)
        if token.type == "heading_open"
        and token.tag == "h2"
        and token.level == 0
        and index + 1 < len(tokens)
        and tokens[index + 1].type == "inline"
        and tokens[index + 1].content.strip() == "출처"
    ]
    if len(source_headings) != 1 or not source_headings[0].map:
        return False
    footer = (
        "".join(markdown.splitlines(keepends=True)[source_headings[0].map[1] :])
        .strip()
        .replace("\r\n", "\n")
        .replace("\r", "\n")
    )
    source_block, separator, disclosure = footer.partition("\n\n---\n\n")
    source_tokens = COMMONMARK.parse(source_block.strip())
    list_pairs = {
        "bullet_list_open": "bullet_list_close",
        "ordered_list_open": "ordered_list_close",
    }
    if not source_tokens or source_tokens[0].type not in list_pairs:
        return False
    if source_tokens[-1].type != list_pairs[source_tokens[0].type]:
        return False

    has_link = False
    index = 1
    while index < len(source_tokens) - 1:
        item = source_tokens[index : index + 5]
        if len(item) != 5 or [token.type for token in item] != [
            "list_item_open",
            "paragraph_open",
            "inline",
            "paragraph_close",
            "list_item_close",
        ]:
            return False
        if [token.level for token in item] != [1, 2, 3, 2, 1]:
            return False
        if any(
            child.type == "link_open"
            and valid_https_url(str(child.attrGet("href") or ""))
            for child in item[2].children or []
        ):
            has_link = True
        index += 5
    if index != len(source_tokens) - 1:
        return False
    if not has_link:
        return False
    if not separator:
        return not require_disclosure
    return disclosure.strip() in AI_DISCLOSURES


def relative_name(root: Path, candidate: Path) -> str:
    return candidate.relative_to(root).as_posix()


def has_annex_b_video(header: bytes) -> bool:
    starts = list(re.finditer(b"\x00\x00\x00\x01|\x00\x00\x01", header))
    h264_types: set[int] = set()
    hevc_types: set[int] = set()
    for index, match in enumerate(starts):
        payload_start = match.end()
        payload_end = (
            starts[index + 1].start() if index + 1 < len(starts) else len(header)
        )
        payload = header[payload_start:payload_end]
        if not payload:
            continue
        h264_types.add(payload[0] & 0x1F)
        if len(payload) >= 2:
            hevc_types.add((payload[0] >> 1) & 0x3F)
    coherent_h264 = {7, 8} <= h264_types and bool(h264_types & {1, 2, 3, 4, 5})
    coherent_hevc = {32, 33, 34} <= hevc_types and bool(hevc_types & set(range(32)))
    return coherent_h264 or coherent_hevc


def has_ogg_video(candidate: Path, offset: int = 0) -> bool:
    pending_packets: dict[int, bytearray] = {}
    identification_streams: set[int] = set()
    try:
        with candidate.open("rb") as stream:
            stream.seek(offset)
            while header := stream.read(27):
                if len(header) != 27 or not header.startswith(b"OggS"):
                    return False
                segment_table = stream.read(header[26])
                if len(segment_table) != header[26]:
                    return False
                body_size = sum(segment_table)
                body = stream.read(body_size)
                if len(body) != body_size:
                    return False
                serial = int.from_bytes(header[14:18], "little")
                continued = bool(header[5] & 0x01)
                beginning = bool(header[5] & 0x02)
                if beginning:
                    pending_packets[serial] = bytearray()
                    identification_streams.add(serial)
                elif continued != bool(pending_packets.get(serial)):
                    pending_packets.pop(serial, None)
                    identification_streams.discard(serial)

                packet = pending_packets.setdefault(serial, bytearray())
                body_offset = 0
                for segment_length in segment_table:
                    packet.extend(body[body_offset : body_offset + segment_length])
                    body_offset += segment_length
                    if segment_length == 255:
                        continue
                    if serial in identification_streams:
                        if packet.startswith((b"\x80theora", b"OVP80", b"BBCD")):
                            return True
                        identification_streams.remove(serial)
                    packet.clear()
    except OSError:
        return False
    return False


def leading_id3_size(header: bytes) -> int:
    if len(header) < 10 or not header.startswith(b"ID3"):
        return 0
    size_bytes = header[6:10]
    if any(value & 0x80 for value in size_bytes):
        return 0
    size = sum(value << shift for value, shift in zip(size_bytes, (21, 14, 7, 0)))
    return 10 + size + (10 if header[5] & 0x10 else 0)


def has_mpeg_transport_stream(data: bytes) -> bool:
    video_stream_types = {
        0x01,  # MPEG-1 Video
        0x02,  # MPEG-2 Video
        0x10,  # MPEG-4 Visual
        0x1B,  # H.264/AVC
        0x24,  # H.265/HEVC
        0x25,  # HEVC temporal subset
        0x42,  # AVS
        0xD1,  # Dirac
        0xEA,  # VC-1
    }

    def section_from_payload(packet: bytes) -> tuple[int, bytes] | None:
        if len(packet) < 5 or packet[0] != 0x47 or packet[1] & 0x80:
            return None
        adaptation_control = (packet[3] >> 4) & 0x03
        if adaptation_control not in {1, 3}:
            return None
        payload_offset = 4
        if adaptation_control == 3:
            payload_offset += 1 + packet[4]
        if payload_offset >= 188:
            return None
        payload = packet[payload_offset:188]
        if packet[1] & 0x40:
            pointer = payload[0]
            payload = payload[1 + pointer :]
        if len(payload) < 3:
            return None
        section_length = ((payload[1] & 0x0F) << 8) | payload[2]
        section_end = 3 + section_length
        if section_length > 1021 or section_end > len(payload):
            return None
        pid = ((packet[1] & 0x1F) << 8) | packet[2]
        return pid, payload[:section_end]

    for packet_size in (188, 192, 204, 208):
        offset = data.find(b"\x47")
        while offset >= 0 and offset + packet_size * 4 + 4 <= len(data):
            valid = True
            for index in range(5):
                packet = offset + packet_size * index
                if data[packet] != 0x47 or data[packet + 1] & 0x80:
                    valid = False
                    break
                adaptation_control = (data[packet + 3] >> 4) & 0x03
                if adaptation_control == 0:
                    valid = False
                    break
                if adaptation_control in {2, 3} and data[packet + 4] > packet_size - 5:
                    valid = False
                    break
            if valid:
                pmt_pids: set[int] = set()
                sections: list[tuple[int, bytes]] = []
                packet_offset = offset
                while packet_offset + 188 <= len(data):
                    section = section_from_payload(
                        data[packet_offset : packet_offset + 188]
                    )
                    if section:
                        sections.append(section)
                        pid, payload = section
                        if pid == 0 and payload[0] == 0x00 and len(payload) >= 12:
                            entries_end = len(payload) - 4
                            for entry in range(8, entries_end - 3, 4):
                                program = int.from_bytes(
                                    payload[entry : entry + 2], "big"
                                )
                                if program:
                                    pmt_pids.add(
                                        ((payload[entry + 2] & 0x1F) << 8)
                                        | payload[entry + 3]
                                    )
                    packet_offset += packet_size
                for pid, payload in sections:
                    if pid not in pmt_pids or payload[0] != 0x02 or len(payload) < 16:
                        continue
                    program_info_length = ((payload[10] & 0x0F) << 8) | payload[11]
                    entry = 12 + program_info_length
                    entries_end = len(payload) - 4
                    while entry + 5 <= entries_end:
                        stream_type = payload[entry]
                        if stream_type in video_stream_types:
                            return True
                        info_length = ((payload[entry + 3] & 0x0F) << 8) | payload[
                            entry + 4
                        ]
                        entry += 5 + info_length
                return False
            offset = data.find(b"\x47", offset + 1)
    return False


def has_ebml_video_track(candidate: Path, start: int = 0) -> bool:
    def read_vint(
        stream: BinaryIO, offset: int, *, identifier: bool
    ) -> tuple[int, int] | None:
        stream.seek(offset)
        first_data = stream.read(1)
        if not first_data:
            return None
        first = first_data[0]
        marker = 0x80
        length = 1
        while length <= 8 and not first & marker:
            marker >>= 1
            length += 1
        remainder = stream.read(length - 1)
        if length > 8 or len(remainder) != length - 1:
            return None
        value = first if identifier else first & (marker - 1)
        for byte in remainder:
            value = (value << 8) | byte
        return value, length

    segment_id = 0x18538067
    tracks_id = 0x1654AE6B
    track_entry_id = 0xAE
    track_type_id = 0x83

    def scan(stream: BinaryIO, scan_start: int, end: int, context: int = 0) -> bool:
        offset = scan_start
        while offset < end:
            identifier = read_vint(stream, offset, identifier=True)
            if not identifier:
                return False
            element_id, id_length = identifier
            size_field = read_vint(stream, offset + id_length, identifier=False)
            if not size_field:
                return False
            size, size_length = size_field
            payload_start = offset + id_length + size_length
            payload_end = (
                end if size == (1 << (7 * size_length)) - 1 else payload_start + size
            )
            if payload_end > end:
                return False
            if (
                context == track_entry_id
                and element_id == track_type_id
                and 1 <= size <= 8
            ):
                stream.seek(payload_start)
                if int.from_bytes(stream.read(size), "big") == 1:
                    return True
            child_context = (
                element_id
                if element_id in {segment_id, tracks_id, track_entry_id}
                else 0
            )
            if child_context and scan(
                stream, payload_start, payload_end, child_context
            ):
                return True
            offset = payload_end
        return False

    try:
        with candidate.open("rb") as stream:
            return scan(stream, start, candidate.stat().st_size)
    except OSError:
        return False


def has_asf_video_stream(candidate: Path, start: int = 0) -> bool:
    try:
        file_size = candidate.stat().st_size
        with candidate.open("rb") as stream:
            stream.seek(start)
            header = stream.read(30)
            if len(header) != 30 or header[:16] != ASF_HEADER:
                return False
            header_size = int.from_bytes(header[16:24], "little")
            object_count = int.from_bytes(header[24:28], "little")
            header_end = start + header_size
            if header_size < 30 or header_end > file_size or object_count > 10_000:
                return False
            offset = start + 30
            for _index in range(object_count):
                if offset + 24 > header_end:
                    return False
                stream.seek(offset)
                object_header = stream.read(24)
                object_size = int.from_bytes(object_header[16:24], "little")
                if object_size < 24 or offset + object_size > header_end:
                    return False
                if object_header[:16] == ASF_STREAM_PROPERTIES:
                    stream_type = stream.read(16)
                    if stream_type == ASF_VIDEO_MEDIA:
                        return True
                offset += object_size
    except OSError:
        return False
    return False


def has_exact_jpeg_container(payload: bytes) -> bool:
    if not payload.startswith(b"\xff\xd8"):
        return False
    offset = 2
    in_scan = False
    while offset < len(payload):
        if in_scan:
            marker_start = payload.find(b"\xff", offset)
            if marker_start < 0 or marker_start + 1 >= len(payload):
                return False
            marker_end = marker_start + 1
            while marker_end < len(payload) and payload[marker_end] == 0xFF:
                marker_end += 1
            if marker_end >= len(payload):
                return False
            marker = payload[marker_end]
            if marker == 0x00 or 0xD0 <= marker <= 0xD7:
                offset = marker_end + 1
                continue
            offset = marker_start
            in_scan = False
            continue

        if payload[offset] != 0xFF:
            return False
        marker_end = offset + 1
        while marker_end < len(payload) and payload[marker_end] == 0xFF:
            marker_end += 1
        if marker_end >= len(payload):
            return False
        marker = payload[marker_end]
        offset = marker_end + 1
        if marker == 0xD9:
            return offset == len(payload)
        if marker == 0x01 or marker == 0xD8 or 0xD0 <= marker <= 0xD7:
            continue
        if marker == 0x00 or offset + 2 > len(payload):
            return False
        segment_length = int.from_bytes(payload[offset : offset + 2], "big")
        if segment_length < 2 or offset + segment_length > len(payload):
            return False
        offset += segment_length
        if marker == 0xDA:
            in_scan = True
    return False


def has_video_iso_bmff_track(candidate: Path, start: int = 0) -> bool:
    containers = {b"moov", b"trak", b"mdia"}
    has_video = False

    def scan_boxes(stream: BinaryIO, offset: int, end: int, depth: int) -> bool:
        nonlocal has_video
        while offset + 8 <= end:
            stream.seek(offset)
            header = stream.read(16)
            if len(header) < 8:
                return False
            size = int.from_bytes(header[:4], "big")
            box_type = header[4:8]
            header_size = 8
            if size == 1:
                if len(header) < 16:
                    return False
                size = int.from_bytes(header[8:16], "big")
                header_size = 16
            elif size == 0:
                size = end - offset
            if size < header_size or offset + size > end:
                return False
            payload_start = offset + header_size
            if box_type == b"hdlr" and size >= header_size + 12:
                stream.seek(payload_start + 8)
                if stream.read(4) == b"vide":
                    has_video = True
            if (
                box_type in containers
                and depth < 4
                and scan_boxes(stream, payload_start, offset + size, depth + 1)
            ):
                has_video = True
            offset += size
        return has_video

    try:
        file_size = candidate.stat().st_size
        with candidate.open("rb") as stream:
            scan_boxes(stream, start, file_size, 0)
            return has_video
    except OSError:
        return False


def is_video_file(candidate: Path) -> bool:
    media_type, _encoding = mimetypes.guess_type(candidate.name)
    suffix = candidate.suffix.lower()
    if suffix in VIDEO_EXTENSIONS or bool(
        suffix not in SHARED_BMFF_EXTENSIONS | SHARED_MPEG_TS_EXTENSIONS | {".webm"}
        and media_type
        and media_type.startswith("video/")
    ):
        return True
    if candidate.is_symlink() or not candidate.is_file():
        return False
    if candidate.suffix.lower() in ALLOWED_IMAGE_EXTENSIONS and is_valid_image_file(
        candidate
    ):
        return False
    try:
        with candidate.open("rb") as stream:
            prefix = stream.read(10)
            scan_offset = leading_id3_size(prefix)
            stream.seek(scan_offset)
            header = stream.read(MAX_VIDEO_SCAN_BYTES + 416)
    except OSError:
        return False
    if header.startswith(b"OggS"):
        return has_ogg_video(candidate, scan_offset)
    if header.startswith(EBML_HEADER):
        return has_ebml_video_track(candidate, scan_offset)
    if header.startswith(ASF_HEADER):
        return has_asf_video_stream(candidate, scan_offset)
    return (
        has_video_iso_bmff_track(candidate, scan_offset)
        or (header.startswith(b"RIFF") and header[8:12] == b"AVI ")
        or header.startswith(
            (
                b"DKIF",
                b"FLV",
                b"YUV4MPEG2",
                b".RMF",
                b"\x00\x00\x01\xba",
                b"\x00\x00\x01\xb3",
                b"\x06\x0e\x2b\x34\x02\x05\x01\x01\x0d\x01\x02",
            )
        )
        or has_annex_b_video(header[:512])
        or has_mpeg_transport_stream(header)
    )


def is_valid_image_file(candidate: Path) -> bool:
    expected = {
        ".png": "PNG",
        ".jpg": "JPEG",
        ".jpeg": "JPEG",
        ".webp": "WEBP",
    }
    try:
        if candidate.stat().st_size > MAX_IMAGE_BYTES:
            return False
        payload = candidate.read_bytes()
        suffix = candidate.suffix.lower()
        if suffix == ".png":
            offset = 8
            if not payload.startswith(b"\x89PNG\r\n\x1a\n"):
                return False
            while offset + 12 <= len(payload):
                chunk_length = int.from_bytes(payload[offset : offset + 4], "big")
                chunk_type = payload[offset + 4 : offset + 8]
                offset += 12 + chunk_length
                if offset > len(payload):
                    return False
                if chunk_type == b"IEND":
                    if chunk_length != 0 or offset != len(payload):
                        return False
                    break
            else:
                return False
        elif suffix in {".jpg", ".jpeg"}:
            if not has_exact_jpeg_container(payload):
                return False
        elif suffix == ".webp":
            if (
                len(payload) < 12
                or payload[:4] != b"RIFF"
                or payload[8:12] != b"WEBP"
                or int.from_bytes(payload[4:8], "little") + 8 != len(payload)
            ):
                return False
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(candidate) as image:
                width, height = image.size
                if (
                    bool(getattr(image, "is_animated", False))
                    or int(getattr(image, "n_frames", 1)) != 1
                    or width > MAX_IMAGE_DIMENSION
                    or height > MAX_IMAGE_DIMENSION
                    or width * height > MAX_IMAGE_PIXELS
                ):
                    return False
                image.load()
                return image.format == expected.get(candidate.suffix.lower())
    except (
        OSError,
        UnidentifiedImageError,
        Image.DecompressionBombError,
        Image.DecompressionBombWarning,
    ):
        return False


def validate_article(
    root: Path,
    article: Path,
    referenced_images: set[Path] | None = None,
    seen_slugs: dict[str, str] | None = None,
) -> list[str]:
    errors: list[str] = []
    name = relative_name(root, article)
    path_match = ARTICLE_PATH_RE.fullmatch(name)
    if not path_match:
        return [f"{name}: 기사 경로 계약을 따르지 않습니다"]
    if article.is_symlink():
        return [f"{name}: 기사 심볼릭 링크는 허용하지 않습니다"]
    if article.stat().st_size > MAX_MARKDOWN_BYTES:
        return [f"{name}: Markdown 크기가 {MAX_MARKDOWN_BYTES}바이트를 초과합니다"]

    try:
        markdown = article.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [f"{name}: Markdown은 UTF-8이어야 합니다"]
    frontmatter_match = FRONTMATTER_RE.match(markdown)
    try:
        metadata = (
            yaml.safe_load(frontmatter_match.group(1)) if frontmatter_match else {}
        )
    except yaml.YAMLError:
        metadata = {}
        errors.append(f"{name}: front matter YAML이 올바르지 않습니다")
    slug_value = metadata.get("slug") if isinstance(metadata, dict) else None
    slug = slug_value if isinstance(slug_value, str) else ""
    required_strings = ("title", "topic", "summary", "generated_by", "model")
    if not isinstance(metadata, dict):
        errors.append(f"{name}: front matter는 mapping이어야 합니다")
    else:
        for field in required_strings:
            if not isinstance(metadata.get(field), str) or not metadata[field].strip():
                errors.append(f"{name}: front matter {field} 값이 필요합니다")
        topic = metadata.get("topic")
        if isinstance(topic, str) and not re.fullmatch(
            r"[a-z0-9가-힣][a-z0-9가-힣_-]*", topic
        ):
            errors.append(f"{name}: front matter topic 형식이 올바르지 않습니다")
        if isinstance(topic, str) and topic != path_match.group(1):
            errors.append(
                f"{name}: front matter topic과 news 하위 디렉터리가 일치하지 않습니다"
            )
        published_at = metadata.get("published_at")
        try:
            published = (
                published_at
                if isinstance(published_at, datetime)
                else datetime.fromisoformat(published_at)
            )
            if published.tzinfo is None:
                raise ValueError
        except (TypeError, ValueError):
            errors.append(
                f"{name}: front matter published_at은 시간대가 있는 ISO 8601이어야 합니다"
            )
        tags = metadata.get("tags")
        if tags is not None and (
            not isinstance(tags, list)
            or any(not isinstance(tag, str) or not tag.strip() for tag in tags)
        ):
            errors.append(f"{name}: front matter tags는 문자열 목록이어야 합니다")
    if slug != path_match.group(2):
        errors.append(f"{name}: front matter slug와 파일명이 일치하지 않습니다")
    elif seen_slugs is not None:
        previous = seen_slugs.setdefault(slug, name)
        if previous != name:
            errors.append(f"{name}: slug가 {previous} 문서와 중복됩니다: {slug}")
    try:
        body = markdown[frontmatter_match.end() :] if frontmatter_match else markdown
        images = article_images(body)
    except ValueError as error:
        return [*errors, f"{name}: {error}"]
    require_disclosure = (
        isinstance(metadata, dict) and metadata.get("generated_by") != "manual"
    )
    if not has_source_footer(body, require_disclosure):
        errors.append(f"{name}: ## 출처 섹션에 최소 1개의 HTTPS 원문 링크가 필요합니다")

    for _alt, destination, raw_destination, attribution_valid in images:
        bracketed = raw_destination.startswith("<") and raw_destination.endswith(">")
        if (
            not bracketed and any(character.isspace() for character in raw_destination)
        ) or any(marker in destination for marker in ("?", "#")):
            errors.append(
                f"{name}: 사진 경로에 공백, 쿼리 또는 프래그먼트를 사용할 수 없습니다"
            )
            continue

        if re.search(r"%(?![0-9A-Fa-f]{2})", raw_destination) or re.search(
            r"%(?![0-9A-Fa-f]{2})", destination
        ):
            errors.append(f"{name}: 사진 경로의 percent encoding이 잘못됐습니다")
            continue
        try:
            decoded = unquote(destination, encoding="utf-8", errors="strict")
        except UnicodeDecodeError:
            errors.append(
                f"{name}: 사진 경로는 올바른 UTF-8 percent encoding을 사용해야 합니다"
            )
            continue
        if re.search(r"%(?![0-9A-Fa-f]{2})", decoded):
            errors.append(
                f"{name}: 정규화한 사진 경로의 percent encoding이 잘못됐습니다"
            )
            continue
        parts = decoded.split("/")
        if (
            len(parts) != 3
            or parts[:2] != [".", slug]
            or not parts[-1]
            or "\\" in decoded
            or "\0" in decoded
        ):
            errors.append(f"{name}: 사진 경로는 ./{slug}/<file> 형식이어야 합니다")
            continue
        image = article.parent / slug / parts[-1]
        if referenced_images is not None:
            referenced_images.add(image)
        if image.suffix.lower() not in ALLOWED_IMAGE_EXTENSIONS:
            errors.append(f"{name}: 사진 형식은 webp, jpg, jpeg 또는 png여야 합니다")
        elif not image.is_file() or image.is_symlink():
            errors.append(
                f"{name}: 참조한 사진 파일이 없거나 심볼릭 링크입니다: {decoded}"
            )
        elif not is_valid_image_file(image):
            errors.append(
                f"{relative_name(root, image)}: 확장자와 일치하는 유효한 사진 파일이 아닙니다"
            )
        if not attribution_valid:
            errors.append(
                f"{name}: 각 사진 바로 다음에 제작자·HTTPS 출처·라이선스를 표시해야 합니다"
            )

    return errors


def validate_repository(root: Path, base: Path | None = None) -> list[str]:
    errors: list[str] = []
    news = root / "news"
    if not news.is_dir() or news.is_symlink():
        return ["news 디렉터리가 없거나 심볼릭 링크입니다"]
    previously_published_images = (
        {
            existing.relative_to(base)
            for existing in (base / "news").rglob("*")
            if existing.is_file()
            and not existing.is_symlink()
            and existing.suffix.lower() in ALLOWED_IMAGE_EXTENSIONS
        }
        if base and (base / "news").is_dir()
        else set()
    )

    for candidate in root.rglob("*"):
        relative = candidate.relative_to(root)
        if ".git" in relative.parts:
            continue
        is_stored_file = candidate.is_file() or candidate.is_symlink()
        media_type, _encoding = mimetypes.guess_type(candidate.name)
        if is_stored_file and is_video_file(candidate):
            errors.append(f"{relative.as_posix()}: 동영상 파일은 저장할 수 없습니다")
        if (
            is_stored_file
            and media_type
            and media_type.startswith("image/")
            and candidate.suffix.lower() not in ALLOWED_IMAGE_EXTENSIONS
        ):
            errors.append(
                f"{relative.as_posix()}: 사진 형식은 webp, jpg, jpeg 또는 png여야 합니다"
            )
        if (
            is_stored_file
            and candidate.suffix.lower() in ALLOWED_IMAGE_EXTENSIONS
            and not is_valid_image_file(candidate)
        ):
            errors.append(
                f"{relative.as_posix()}: 확장자와 일치하는 유효한 정적 사진 파일이 아닙니다"
            )

    referenced_images: set[Path] = set()
    seen_slugs: dict[str, str] = {}
    for article in news.rglob("*"):
        if article.suffix.lower() != ".md":
            continue
        if article.is_file() and not article.is_symlink():
            errors.extend(
                validate_article(root, article, referenced_images, seen_slugs)
            )

    for candidate in news.rglob("*"):
        if candidate.is_symlink():
            errors.append(
                f"{relative_name(root, candidate)}: 심볼릭 링크는 허용하지 않습니다"
            )
            continue
        if not candidate.is_file():
            continue
        suffix = candidate.suffix.lower()
        if suffix == ".md" or is_video_file(candidate):
            continue
        elif suffix in ALLOWED_IMAGE_EXTENSIONS:
            media_parts = candidate.relative_to(news).parts
            if len(media_parts) != 5:
                errors.append(
                    f"{relative_name(root, candidate)}: 사진은 기사 slug와 같은 이름의 디렉터리 바로 아래에 저장해야 합니다"
                )
                continue
            if not is_valid_image_file(candidate):
                errors.append(
                    f"{relative_name(root, candidate)}: 확장자와 일치하는 유효한 사진 파일이 아닙니다"
                )
            article = candidate.parent.parent / f"{candidate.parent.name}.md"
            if not article.is_file():
                errors.append(
                    f"{relative_name(root, candidate)}: 대응하는 기사 파일이 없습니다"
                )
            elif (
                candidate not in referenced_images
                and candidate.relative_to(root) not in previously_published_images
            ):
                errors.append(
                    f"{relative_name(root, candidate)}: 대응하는 기사에서 참조하지 않은 사진입니다"
                )
        else:
            errors.append(
                f"{relative_name(root, candidate)}: 기사 미디어 디렉터리에는 webp, jpg, jpeg 또는 png만 저장할 수 있습니다"
            )

    return list(dict.fromkeys(errors))


def validate_immutable_media(base: Path, candidate: Path) -> list[str]:
    errors: list[str] = []
    base_news = base / "news"
    if not base_news.is_dir():
        return errors
    for existing in base_news.rglob("*"):
        if not existing.is_file() or existing.is_symlink():
            continue
        if existing.suffix.lower() not in ALLOWED_IMAGE_EXTENSIONS:
            continue
        relative = existing.relative_to(base)
        proposed = candidate / relative
        if not proposed.is_file() or proposed.is_symlink():
            errors.append(f"{relative.as_posix()}: 발행된 사진은 삭제할 수 없습니다")
        elif not cmp(existing, proposed, shallow=False):
            errors.append(
                f"{relative.as_posix()}: 발행된 사진은 같은 경로에서 덮어쓸 수 없습니다"
            )
    return errors


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve(strict=True)
    base = Path(sys.argv[2]).resolve(strict=True) if len(sys.argv) > 2 else None
    errors = validate_repository(root, base)
    if base:
        errors.extend(validate_immutable_media(base, root))
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("공개 콘텐츠 계약 검증을 통과했습니다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
