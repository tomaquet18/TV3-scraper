import requests
import json
from datetime import datetime, timedelta

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0",
}

channels_tv = [
    "tv3",
    "324",
    "sx3",
    "c33",
    "esport3",
]

channels_radio = [
    "cr",
    "ci",
    "cm",
    "ic",
]

class Program:
    def __init__(
        self,
        program_code: int,
        program_title: str,
        chapter: int,
        synopsis: str,
        start_time: datetime,
        end_time: datetime,
        duration: timedelta,
        target: str,
        highlighted_text: str,
        highlighted_image: str,
        hashtag: str,
        audio_description: bool,
        catalan_subtitles: bool,
        vo_subtitles: bool,
        rerun: bool,
    ):
        self.program_code = program_code
        self.program_title = program_title
        self.chapter = chapter
        self.synopsis = synopsis
        self.start_time = start_time
        self.end_time = end_time
        self.duration = duration
        self.target = target
        self.highlighted_text = highlighted_text
        self.highlighted_image = highlighted_image
        self.hashtag = hashtag
        self.audio_description = audio_description
        self.catalan_subtitles = catalan_subtitles
        self.vo_subtitles = vo_subtitles
        self.rerun = rerun

        self.dict = {
            "program_code": self.program_code,
            "program_title": self. program_title,
            "chapter": self.chapter,
            "synopsis": self.synopsis,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": self.duration,
            "target": self.target,
            "highlighted_text": self.highlighted_text,
            "highlighted_image": self.highlighted_image,
            "hashtag": self.hashtag,
            "audio_description": self.audio_description,
            "catalan_subtitles": self.catalan_subtitles,
            "vo_subtitles": self.vo_subtitles,
            "rerun": self.rerun,
        }

def get_program(channel, now_later):
    url = f"https://dinamics.ccma.cat/wsarafem/arafem/%20/{channel}/profile/noimage/geo/cat"

    response = requests.get(url, headers=headers)

    if not response.status_code == 200:
        return None
    response = response.json()

    program_data = response["canal"][now_later]

    if not program_data:
        return None
    program = Program(
        program_code=int(program_data["codi_programa"]),
        program_title=program_data["titol_programa"],
        chapter=int(program_data["capitol"]),
        synopsis=program_data["sinopsi"],
        start_time=datetime.fromisoformat(program_data["start_time"]),
        end_time=datetime.fromisoformat(program_data["end_time"]),
        duration=timedelta(hours=int(program_data["durada"].split(':')[0]),
                           minutes=int(program_data["durada"].split(':')[1]),
                           seconds=int(program_data["durada"].split(':')[2])),
        target=program_data["target"],
        highlighted_text=program_data["destacat_text"],
        highlighted_image=program_data["destacat_imatge"],
        hashtag=program_data["hashtag"],
        audio_description=True if program_data["audio_descripcio"] == "yes" else False,
        catalan_subtitles=True if program_data["subtitulat_catala"] == "yes" else False,
        vo_subtitles=True if program_data["subtitulat_vo"] == "yes" else False,
        rerun=True if program_data["reemissio"] == "yes" else False,
    )
    return program

def get_current_programs(tv=True, radio=True, channels=channels_tv + channels_radio, now=True, later=False):
    data = {}

    if tv and radio:
        tv_radio = ""
    elif tv and not radio:
        tv_radio = "tv"
    elif radio and not tv:
        tv_radio = "radio"
    
    now_later = []
    now_later_out = {"ara_fem": "now", "despres_fem": "later"}
    if now and later:
        now_later = ["ara_fem", "despres_fem"]
    elif not now and later:
        now_later = ["despres_fem"]
    elif not later and now:
        now_later = ["ara_fem"]

    for channel in channels:
        if channel in channels_tv and not tv:
            continue
        if channel in channels_radio and not radio:
            continue

        data[channel] = {}
        for anytime in now_later:
            program = get_program(channel, anytime)
            if program is not None:
                data[channel][now_later_out[anytime]] = program.dict
            else:
                data[channel][now_later_out[anytime]] = {}
    
    return data

print(json.dumps(get_current_programs(now=True, later=True), default=str))