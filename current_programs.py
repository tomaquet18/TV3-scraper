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

def get_program(channel):
    url = f"https://dinamics.ccma.cat/wsarafem/arafem/%20/{channel}/profile/noimage/geo/cat"

    response = requests.get(url, headers=headers)

    if not response.status_code == 200:
        return None
    response = response.json()

    ara_fem = response["canal"]["ara_fem"]

    if not ara_fem:
        return None
    program = Program(
        program_code=int(ara_fem["codi_programa"]),
        program_title=ara_fem["titol_programa"],
        chapter=int(ara_fem["capitol"]),
        synopsis=ara_fem["sinopsi"],
        start_time=datetime.fromisoformat(ara_fem["start_time"]),
        end_time=datetime.fromisoformat(ara_fem["end_time"]),
        duration=timedelta(hours=int(ara_fem["durada"].split(':')[0]),
                           minutes=int(ara_fem["durada"].split(':')[1]),
                           seconds=int(ara_fem["durada"].split(':')[2])),
        target=ara_fem["target"],
        highlighted_text=ara_fem["destacat_text"],
        highlighted_image=ara_fem["destacat_imatge"],
        hashtag=ara_fem["hashtag"],
        audio_description=ara_fem["audio_descripcio"],
        catalan_subtitles=ara_fem["subtitulat_catala"],
        vo_subtitles=ara_fem["subtitulat_vo"],
        rerun=ara_fem["reemissio"],
    )
    return program

def get_current_programs(tv=True, radio=True, channels=channels_tv + channels_radio):
    data = {}

    if tv and radio:
        tv_radio = ""
    elif tv and not radio:
        tv_radio = "tv"
    elif radio and not tv:
        tv_radio = "radio"
    
    for channel in channels:
        if channel in channels_tv and not tv:
            continue
        if channel in channels_radio and not radio:
            continue
        program = get_program(channel)
        if program is not None:
            data[channel] = program.dict
        else:
            data[channel] = {}
    
    return data

#print(json.dumps(get_current_programs(channels=["aa", "tv3"]), default=str))