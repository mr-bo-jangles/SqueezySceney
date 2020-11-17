import logging
from pathlib import Path
from shutil import copyfile
from zipfile import ZipFile

import orjson
from copy import deepcopy
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Tuple, List, Any, Optional, Dict, IO

logger = logging.getLogger()


@dataclass
class Token:
    _id: str
    flags: Dict
    name: str
    displayName: int
    img: str
    tint: Optional[str]
    width: int
    height: int
    scale: Decimal
    x: int
    y: int
    elevation: int
    lockRotation: bool
    rotation: Decimal
    effects: List[Any]
    hidden: bool
    vision: bool
    dimSight: int
    brightSight: int
    dimLight: int
    brightLight: int
    sightAngle: int
    lightAngle: int
    lightAlpha: Decimal
    lightAnimation: Dict
    actorId: str
    actorLink: bool
    actorData: Dict
    disposition: int
    displayBars: int
    bar1: Dict
    bar2: Dict
    mirrorX: Optional[bool] = None
    mirrorY: Optional[bool] = None
    lightColor: Optional[str] = None


@dataclass
class Wall:
    _id: str
    flags: Dict
    c: List[int]
    move: int
    sense: int
    door: int
    ds: int
    dir: Optional[int] = 0


@dataclass
class Light:
    _id: str
    flags: Dict
    t: str
    x: int
    y: int
    hidden: bool
    rotation: Decimal
    dim: int
    bright: int
    angle: int
    darknessThreshold: int
    tintAlpha: Decimal
    lightAnimation: Dict
    tintColor: Optional[str] = ''


@dataclass
class Sound:
    __slots__ = ['_id', 'flags', 'path', 'repeat', 'volume', 'type', 'x', 'y', 'radius', 'easing']
    _id: str
    flags: Dict
    path: str
    repeat: bool
    volume: Decimal
    type: str
    x: int
    y: int
    radius: Decimal
    easing: bool


@dataclass
class Note:
    __slots__ = ['_id', 'flags', 'entryId', 'x', 'y', 'icon', 'iconSize', 'iconTint', 'text', 'fontFamily', 'fontSize',
                 'textAnchor', 'textColor']
    _id: str
    flags: Dict
    entryId: str
    x: int
    y: int
    icon: str
    iconSize: int
    iconTint: str
    text: str
    fontFamily: str
    fontSize: int
    textAnchor: int
    textColor: str


@dataclass
class Drawing:
    __slots__ = [
        '_id',
        'flags',
        'type',
        'author',
        'x',
        'y',
        'width',
        'height',
        'rotation',
        'z',
        'hidden',
        'locked',
        'points',
        'bezierFactor',
        'fillType',
        'fillColor',
        'fillAlpha',
        'strokeWidth',
        'strokeColor',
        'strokeAlpha',
        'texture',
        'text',
        'fontFamily',
        'fontSize',
        'textColor',
        'textAlpha',
    ]
    _id: str
    flags: Dict
    type: str
    author: str
    x: int
    y: int
    width: Decimal
    height: Decimal
    rotation: Decimal
    z: int
    hidden: bool
    locked: bool
    points: List[Any]
    bezierFactor: int
    fillType: int
    fillColor: str
    fillAlpha: Decimal
    strokeWidth: int
    strokeColor: str
    strokeAlpha: Decimal
    texture: str
    text: str
    fontFamily: str
    fontSize: int
    textColor: str
    textAlpha: Decimal


@dataclass
class Point:
    __slots__ = ['x', 'y']
    x: Decimal
    y: Decimal

    @staticmethod
    def _translate_point(origin: 'Point', point: 'Point', scale: Decimal) -> 'Point':
        translated_x = origin.x * (1 - scale) + point.x * scale
        translated_y = origin.y * (1 - scale) + point.y * scale
        return Point(x=translated_x, y=translated_y)

    def translate_point(self, origin: 'Point', scale: Decimal) -> 'Point':
        return self._translate_point(origin=origin, point=self, scale=scale)

    @staticmethod
    def get_point_from_token(token_data: 'Token') -> 'Point':
        return Point(x=Decimal(token_data.x), y=Decimal(token_data.y))

    @staticmethod
    def get_points_from_walls(wall_data) -> Tuple['Point', 'Point']:
        coords = wall_data.c
        return Point(x=coords[0], y=coords[1]), Point(x=coords[2], y=coords[3])

    @staticmethod
    def get_point_from_light(light_data) -> 'Point':
        x = light_data.x
        y = light_data.y
        return Point(x=Decimal(x), y=Decimal(y))

    @staticmethod
    def get_point_from_sound(sound_data) -> 'Point':
        x = sound_data.x
        y = sound_data.y
        return Point(x=Decimal(x), y=Decimal(y))

    @staticmethod
    def get_point_from_note(note_data) -> 'Point':
        x = note_data.x
        y = note_data.y
        return Point(x=Decimal(x), y=Decimal(y))

    @staticmethod
    def get_point_from_drawing(drawing_data) -> 'Point':
        x = drawing_data.x
        y = drawing_data.y
        return Point(x=Decimal(x), y=Decimal(y))

    @property
    def integer_x(self) -> int:
        return int(self.x.quantize(Decimal(1)))

    @property
    def integer_y(self) -> int:
        return int(self.y.quantize(Decimal(1)))


@dataclass
class Scene:
    __slots__ = [
        "_id",
        "name",
        "folder",
        "sort",
        "flags",
        "description",
        "navigation",
        "nav_order",
        "nav_name",
        "active",
        "initial",
        "img",
        "thumb",
        "width",
        "height",
        "padding",
        "background_color",
        "tiles",
        "grid_type",
        "grid",
        "shift_x",
        "shift_y",
        "grid_color",
        "grid_alpha",
        "grid_distance",
        "grid_units",
        "tokens",
        "walls",
        "token_vision",
        "fog_exploration",
        "lights",
        "global_light",
        "global_light_threshold",
        "darkness",
        "playlist",
        "sounds",
        "templates",
        "journal",
        "notes",
        "weather",
        "drawings",
        "size"
    ]

    _id: str
    name: str
    folder: str
    sort: int
    flags: Dict
    description: str
    navigation: bool
    nav_order: int
    nav_name: str
    active: bool
    initial: Dict
    img: str
    thumb: str
    width: int
    height: int
    padding: int
    background_color: str
    tiles: List[Any]
    grid_type: int
    grid: int
    shift_x: int
    shift_y: int
    grid_color: str
    grid_alpha: float
    grid_distance: int
    grid_units: str
    tokens: List['Token']
    walls: List['Wall']
    token_vision: bool
    fog_exploration: bool
    lights: List['Light']
    global_light: bool
    global_light_threshold: Optional[float]
    darkness: float
    playlist: str
    sounds: List['Sound']
    templates: List[Any]
    journal: str
    notes: List['Note']
    weather: str
    drawings: List['Drawing']
    size: Optional[Any]

    @staticmethod
    def create(scene_data) -> 'Scene':
        return Scene(
            _id=scene_data.get('_id'),
            name=scene_data.get('name'),
            folder=scene_data.get('folder'),
            sort=scene_data.get('sort'),
            flags=scene_data.get('flags'),
            description=scene_data.get('description'),
            navigation=scene_data.get('navigation'),
            nav_order=scene_data.get('navOrder'),
            nav_name=scene_data.get('navName'),
            active=scene_data.get('active'),
            initial=scene_data.get('initial'),
            img=scene_data.get('img'),
            thumb=scene_data.get('thumb'),
            width=scene_data.get('width'),
            height=scene_data.get('height'),
            padding=scene_data.get('padding'),
            background_color=scene_data.get('backgroundColor'),
            tiles=scene_data.get('tiles'),
            grid_type=scene_data.get('gridType'),
            grid=scene_data.get('grid'),
            shift_x=scene_data.get('shiftX'),
            shift_y=scene_data.get('shiftY'),
            grid_color=scene_data.get('gridColor'),
            grid_alpha=scene_data.get('gridAlpha'),
            grid_distance=scene_data.get('gridDistance'),
            grid_units=scene_data.get('gridUnits'),
            tokens=[Token(**token) for token in scene_data.get('tokens', [])],
            walls=[Wall(**wall) for wall in scene_data.get('walls', [])],
            token_vision=scene_data.get('tokenVision'),
            fog_exploration=scene_data.get('fogExploration'),
            lights=[Light(**light) for light in scene_data.get('lights', [])],
            global_light=scene_data.get('globalLight'),
            global_light_threshold=scene_data.get('globalLightThreshold'),
            darkness=scene_data.get('darkness'),
            playlist=scene_data.get('playlist'),
            sounds=[Sound(**sound) for sound in scene_data.get('sounds', [])],
            templates=scene_data.get('templates'),
            journal=scene_data.get('journal'),
            notes=[Note(**note) for note in scene_data.get('notes', [])],
            weather=scene_data.get('weather'),
            drawings=[Drawing(**drawing) for drawing in scene_data.get('drawings', [])],
            size=scene_data.get('size'),
        )

    def get_origin(self) -> Point:
        x = Decimal(self.shift_x) * Decimal('0.5')
        y = Decimal(self.shift_y) * Decimal('0.5')
        return Point(x, y)

    def scale_scene(self, scale: Decimal):
        origin = self.get_origin()

        self._scale_tokens(origin=origin, scale=scale)
        self._scale_walls(origin=origin, scale=scale)
        self._scale_lights(origin=origin, scale=scale)
        self._scale_sounds(origin=origin, scale=scale)
        self._scale_notes(origin=origin, scale=scale)
        self._scale_drawings(origin=origin, scale=scale)

        self.width = int((self.width * scale).quantize(Decimal(1)))
        self.height = int((self.height * scale).quantize(Decimal(1)))
        self.grid = int((self.grid * scale).quantize(Decimal(1)))
        self.shift_x = int((self.shift_x * scale).quantize(Decimal(1)))
        self.shift_y = int((self.shift_y * scale).quantize(Decimal(1)))

    def _scale_tokens(self, origin: Point, scale: Decimal):
        resized_tokens = []
        for token in self.tokens:
            token_point = Point.get_point_from_token(token_data=token)
            scaled_token_point = token_point.translate_point(origin=origin, scale=scale)
            new_token = deepcopy(token)
            new_token.x = scaled_token_point.integer_x
            new_token.y = scaled_token_point.integer_y
            resized_tokens.append(new_token)
        self.tokens = resized_tokens

    def _scale_walls(self, origin: Point, scale: Decimal):
        resized_walls = []
        for wall in self.walls:
            wall_points = Point.get_points_from_walls(wall_data=wall)
            scaled_wall_points = []
            for wall_point in wall_points:
                scaled_wall_point = wall_point.translate_point(origin=origin, scale=scale)
                scaled_wall_points.extend([scaled_wall_point.integer_x, scaled_wall_point.integer_y])
            new_wall = deepcopy(wall)
            new_wall.c = scaled_wall_points
            resized_walls.append(new_wall)
        self.walls = resized_walls

    def _scale_lights(self, origin: Point, scale: Decimal):
        resized_lights = []
        for light in self.lights:
            light_point = Point.get_point_from_light(light_data=light)
            scaled_light_point = light_point.translate_point(origin=origin, scale=scale)
            new_light = deepcopy(light)
            new_light.x = scaled_light_point.integer_x
            new_light.y = scaled_light_point.integer_y
            resized_lights.append(new_light)
        self.lights = resized_lights

    def _scale_sounds(self, origin: Point, scale: Decimal):
        resized_sounds = []
        for sound in self.sounds:
            sound_point = Point.get_point_from_sound(sound_data=sound)
            scaled_sound_point = sound_point.translate_point(origin=origin, scale=scale)
            new_sound = deepcopy(sound)
            new_sound.x = scaled_sound_point.integer_x
            new_sound.y = scaled_sound_point.integer_y
            resized_sounds.append(new_sound)
        self.sounds = resized_sounds

    def _scale_notes(self, origin: Point, scale: Decimal):
        resized_notes = []
        for note in self.notes:
            note_point = Point.get_point_from_note(note_data=note)
            scaled_note_point = note_point.translate_point(origin=origin, scale=scale)
            new_note = deepcopy(note)
            new_note.x = scaled_note_point.integer_x
            new_note.y = scaled_note_point.integer_y
            resized_notes.append(new_note)
        self.notes = resized_notes

    def _scale_drawings(self, origin: Point, scale: Decimal):
        resized_drawings = []
        for drawing in self.drawings:
            drawing_point = Point.get_point_from_drawing(drawing_data=drawing)
            scaled_drawing_point = drawing_point.translate_point(origin=origin, scale=scale)
            new_drawing = deepcopy(drawing)
            new_drawing.x = scaled_drawing_point.integer_x
            new_drawing.y = scaled_drawing_point.integer_y
            resized_drawings.append(new_drawing)
        self.drawings = resized_drawings

    @staticmethod
    def from_json_string(json_string) -> 'Scene':
        return Scene.create(orjson.loads(json_string))

    def to_json(self):
        output_dict = dict(
            _id=self._id,
            name=self.name,
            folder=self.folder,
            sort=self.sort,
            flags=self.flags,
            description=self.description,
            navigation=self.description,
            navOrder=self.nav_order,
            navName=self.nav_name,
            active=self.active,
            initial=self.initial,
            img=self.img,
            thumb=self.thumb,
            width=self.width,
            height=self.height,
            padding=self.padding,
            backgroundColor=self.background_color,
            tiles=self.tiles,
            gridType=self.grid_type,
            grid=self.grid,
            shiftX=self.shift_x,
            shiftY=self.shift_y,
            gridColor=self.grid_color,
            gridAlpha=self.grid_alpha,
            gridDistance=self.grid_distance,
            gridUnits=self.grid_units,
            tokens=self.tokens,
            walls=self.walls,
            tokenVision=self.token_vision,
            fogExploration=self.fog_exploration,
            lights=self.lights,
            globalLight=self.global_light,
            globalLightThreshold=self.global_light_threshold,
            darkness=self.darkness,
            playlist=self.playlist,
            sounds=self.sounds,
            templates=self.templates,
            journal=self.journal,
            notes=self.notes,
            weather=self.weather,
            drawings=self.drawings,
            size=self.size
        )
        return orjson.dumps(output_dict).decode('utf-8')


@dataclass
class AdventureBundle:
    filename: Optional[str] = None
    scenes: Dict[str, Scene] = field(default_factory=dict)

    def perform_scaling(self, input_file: IO, output_file: IO, scale: Decimal):
        self.filename = input_file
        logger.warning(f'input_filename: {input_file.name}. output_filename: {output_file}. scale: {scale}')
        copyfile(input_file.name, output_file)
        with ZipFile(input_file) as input_zip_file, ZipFile(output_file, mode="w") as output_zip_file:
            file_list = input_zip_file.namelist()
            for compressed_item in file_list:
                compressed_item_path = Path(compressed_item)

                opened_file = input_zip_file.read(compressed_item)
                if compressed_item_path.match('scene/*.json'):
                    logger.warning(f'Processing {compressed_item_path}')
                    scene1 = Scene.from_json_string(json_string=opened_file)
                    self.scenes[compressed_item] = scene1
                else:
                    output_zip_file.writestr(compressed_item, opened_file)

            self.scale_scenes(scale=scale)
            for scene_filename, scene in self.scenes.items():
                output_zip_file.writestr(scene_filename, scene.to_json())

    def scale_scenes(self, scale: Decimal):
        for _, scene in self.scenes.items():
            scene.scale_scene(scale=scale)
