from dataclasses import dataclass
from enum import IntEnum
from typing import Optional, List


class EnumGroupType(IntEnum) :
    Translation = 0
    Transfer = 1
    Compression = 2


class EnumLanguage(IntEnum) :
    JpSc = 0
    ScTc = 1
    JpScTc = 2
    Sc = 3
    JpTc = 4
    Tc = 5
    Jp = 6
    Unspecified = 7
    Eng = 8
    EngSc = 9
    EngTc = 10
    EngScTc = 11


class EnumMediaType(IntEnum) :
    SingleEpisode = 0
    MultipleEpisode = 1
    Movie = 2
    Ova = 3


class EnumResolution(IntEnum) :
    R480p = 0
    R720p = 1
    R1080p = 2
    R2K = 3
    R4K = 4
    Unknown = 5


class EnumSubtitleType(IntEnum) :
    Embedded = 0
    Muxed = 1
    External = 2
    Unspecified = 3


@dataclass
class LocalizedTitle :
    language: str
    value: str


@dataclass
class ParseResult :
    origin_title: str
    title: str
    titles: List[LocalizedTitle]
    episode: Optional[float]
    version: int
    start_episode: Optional[int]
    end_episode: Optional[int]
    group: str
    group_type: EnumGroupType
    language: EnumLanguage
    subtitle_type: EnumSubtitleType
    resolution: EnumResolution
    source: str
    web_source: str
    media_type: EnumMediaType
    video_codec: str
    audio_codec: str
    color_bit_depth: int


def from_json(d: dict) -> ParseResult :
    # 处理 LocalizedTitle 列表
    raw_titles = d.get("Titles")
    parsed_titles = []
    if raw_titles :
        for t in raw_titles :
            parsed_titles.append(LocalizedTitle(
                language = t.get("Language", ""),
                value = t.get("Value", "")
            ))

    return ParseResult(
        origin_title = d.get("OriginTitle", ""),
        title = d.get("Title", ""),
        titles = parsed_titles,
        episode = d.get("Episode"),
        version = d.get("Version", 1),
        start_episode = d.get("StartEpisode"),  # 注意：C# JSON如果为null，get返回None
        end_episode = d.get("EndEpisode"),
        group = d.get("Group", ""),
        group_type = EnumGroupType(d.get("GroupType", 0)),
        language = EnumLanguage(d.get("Language", 7)),
        subtitle_type = EnumSubtitleType(d.get("SubtitleType", 3)),
        resolution = EnumResolution(d.get("Resolution", 5)),
        source = d.get("Source", "WebRip"),
        web_source = d.get("WebSource", ""),
        media_type = EnumMediaType(d.get("MediaType", 0)),
        video_codec = d.get("VideoCodec", ""),
        audio_codec = d.get("AudioCodec", ""),
        color_bit_depth = d.get("ColorBitDepth", -1)
    )
