from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Type

__NAMESPACE__ = "http://ns.editeur.org/onix/3.1/reference"


class Scope(Enum):
    ROW = "row"
    COL = "col"
    ROWGROUP = "rowgroup"
    COLGROUP = "colgroup"


class Shape(Enum):
    RECT = "rect"
    CIRCLE = "circle"
    POLY = "poly"
    DEFAULT = "default"


class Tframe(Enum):
    VOID = "void"
    ABOVE = "above"
    BELOW = "below"
    HSIDES = "hsides"
    LHS = "lhs"
    RHS = "rhs"
    VSIDES = "vsides"
    BOX = "box"
    BORDER = "border"


class Trules(Enum):
    NONE = "none"
    GROUPS = "groups"
    ROWS = "rows"
    COLS = "cols"
    ALL = "all"


class ADir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class AbbrDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class AcronymDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class AddressDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class AreaDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class AreaNohref(Enum):
    NOHREF = "nohref"


class BDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class BdoDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class BigDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class BlockquoteDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


@dataclass
class Br:
    class Meta:
        name = "br"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


class CaptionDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class CiteDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class CodeDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class ColAlign(Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    JUSTIFY = "justify"
    CHAR = "char"


class ColDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class ColValign(Enum):
    TOP = "top"
    MIDDLE = "middle"
    BOTTOM = "bottom"
    BASELINE = "baseline"


class ColgroupAlign(Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    JUSTIFY = "justify"
    CHAR = "char"


class ColgroupDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class ColgroupValign(Enum):
    TOP = "top"
    MIDDLE = "middle"
    BOTTOM = "bottom"
    BASELINE = "baseline"


class DdDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class DfnDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class DivDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class DlDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class DtDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class EmDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class H1Dir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class H2Dir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class H3Dir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class H4Dir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class H5Dir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class H6Dir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class HrDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class IDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class ImgDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class ImgIsmap(Enum):
    ISMAP = "ismap"


class KbdDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class LiDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class MapDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class OlDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class OlType(Enum):
    VALUE_1 = "1"
    A = "A"
    A_1 = "a"
    I = "I"
    I_1 = "i"


class PDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class PreDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class QDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class RbDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class RbcDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class RpDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class RtDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class RtcDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class RubyDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class SampDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class SmallDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class SpanDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class StrongDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class SubDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class SupDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class TableDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class TbodyAlign(Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    JUSTIFY = "justify"
    CHAR = "char"


class TbodyDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class TbodyValign(Enum):
    TOP = "top"
    MIDDLE = "middle"
    BOTTOM = "bottom"
    BASELINE = "baseline"


class TdAlign(Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    JUSTIFY = "justify"
    CHAR = "char"


class TdDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class TdValign(Enum):
    TOP = "top"
    MIDDLE = "middle"
    BOTTOM = "bottom"
    BASELINE = "baseline"


class TfootAlign(Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    JUSTIFY = "justify"
    CHAR = "char"


class TfootDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class TfootValign(Enum):
    TOP = "top"
    MIDDLE = "middle"
    BOTTOM = "bottom"
    BASELINE = "baseline"


class ThAlign(Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    JUSTIFY = "justify"
    CHAR = "char"


class ThDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class ThValign(Enum):
    TOP = "top"
    MIDDLE = "middle"
    BOTTOM = "bottom"
    BASELINE = "baseline"


class TheadAlign(Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    JUSTIFY = "justify"
    CHAR = "char"


class TheadDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class TheadValign(Enum):
    TOP = "top"
    MIDDLE = "middle"
    BOTTOM = "bottom"
    BASELINE = "baseline"


class TrAlign(Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    JUSTIFY = "justify"
    CHAR = "char"


class TrDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class TrValign(Enum):
    TOP = "top"
    MIDDLE = "middle"
    BOTTOM = "bottom"
    BASELINE = "baseline"


class TtDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class UlDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


class VarDir(Enum):
    LTR = "ltr"
    RTL = "rtl"


@dataclass
class Area:
    class Meta:
        name = "area"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[AreaDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    shape: Shape = field(
        default=Shape.RECT,
        metadata={
            "type": "Attribute",
        }
    )
    coords: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    nohref: Optional[AreaNohref] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    alt: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class Col:
    class Meta:
        name = "col"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[ColDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    span: str = field(
        default="1",
        metadata={
            "type": "Attribute",
        }
    )
    width: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    align: Optional[ColAlign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    char: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    charoff: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    valign: Optional[ColValign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Dl:
    class Meta:
        name = "dl"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    dt: List["Dt"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    dd: List["Dd"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[DlDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Hr:
    class Meta:
        name = "hr"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[HrDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Img:
    class Meta:
        name = "img"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[ImgDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    src: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    alt: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    longdesc: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    height: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    width: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    usemap: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    ismap: Optional[ImgIsmap] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Ol:
    class Meta:
        name = "ol"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    li: List["Li"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[OlDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    type_value: Optional[OlType] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
        }
    )
    start: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Rp:
    class Meta:
        name = "rp"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[RpDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    content: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        }
    )


@dataclass
class Ul:
    class Meta:
        name = "ul"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    li: List["Li"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[UlDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Colgroup:
    class Meta:
        name = "colgroup"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    col: List[Col] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[ColgroupDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    span: str = field(
        default="1",
        metadata={
            "type": "Attribute",
        }
    )
    width: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    align: Optional[ColgroupAlign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    char: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    charoff: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    valign: Optional[ColgroupValign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class RubyContent:
    class Meta:
        name = "ruby.content"

    content: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "a",
                    "type": Type["A"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "map",
                    "type": Type["Map"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "img",
                    "type": Img,
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "br",
                    "type": Br,
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "bdo",
                    "type": Type["Bdo"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "span",
                    "type": Type["Span"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "small",
                    "type": Type["Small"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "big",
                    "type": Type["Big"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "b",
                    "type": Type["B"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "i",
                    "type": Type["I"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "tt",
                    "type": Type["Tt"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "sup",
                    "type": Type["Sup"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "sub",
                    "type": Type["Sub"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "q",
                    "type": Type["Q"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "acronym",
                    "type": Type["Acronym"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "abbr",
                    "type": Type["Abbr"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "cite",
                    "type": Type["Cite"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "var",
                    "type": Type["Var"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "kbd",
                    "type": Type["Kbd"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "samp",
                    "type": Type["Samp"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "code",
                    "type": Type["Code"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "dfn",
                    "type": Type["Dfn"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "strong",
                    "type": Type["Strong"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "em",
                    "type": Type["Em"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
            ),
        }
    )


@dataclass
class Rb(RubyContent):
    class Meta:
        name = "rb"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[RbDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Rt(RubyContent):
    class Meta:
        name = "rt"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[RtDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    rbspan: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Rbc:
    class Meta:
        name = "rbc"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    rb: List[Rb] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[RbcDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Rtc:
    class Meta:
        name = "rtc"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    rt: List[Rt] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[RtcDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Ruby:
    class Meta:
        name = "ruby"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    rb: Optional[Rb] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    rt: List[Rt] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 2,
            "max_occurs": 2,
            "sequence": 1,
        }
    )
    rp: List[Rp] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 2,
            "max_occurs": 2,
            "sequence": 1,
        }
    )
    rbc: Optional[Rbc] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    rtc: List[Rtc] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
            "max_occurs": 2,
            "sequence": 2,
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[RubyDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class PreContent:
    class Meta:
        name = "pre.content"

    content: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "a",
                    "type": Type["A"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "br",
                    "type": Br,
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "span",
                    "type": Type["Span"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "bdo",
                    "type": Type["Bdo"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "map",
                    "type": Type["Map"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "tt",
                    "type": Type["Tt"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "i",
                    "type": Type["I"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "b",
                    "type": Type["B"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "sup",
                    "type": Type["Sup"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "sub",
                    "type": Type["Sub"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "q",
                    "type": Type["Q"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "acronym",
                    "type": Type["Acronym"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "abbr",
                    "type": Type["Abbr"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "cite",
                    "type": Type["Cite"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "var",
                    "type": Type["Var"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "kbd",
                    "type": Type["Kbd"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "samp",
                    "type": Type["Samp"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "code",
                    "type": Type["Code"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "dfn",
                    "type": Type["Dfn"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "strong",
                    "type": Type["Strong"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "em",
                    "type": Type["Em"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
            ),
        }
    )


@dataclass
class Pre(PreContent):
    class Meta:
        name = "pre"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[PreDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Block:
    table: List["Table"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://ns.editeur.org/onix/3.1/reference",
        }
    )
    p: List["P"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://ns.editeur.org/onix/3.1/reference",
        }
    )
    div: List["Div"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://ns.editeur.org/onix/3.1/reference",
        }
    )
    blockquote: List["Blockquote"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://ns.editeur.org/onix/3.1/reference",
        }
    )
    pre: List[Pre] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://ns.editeur.org/onix/3.1/reference",
        }
    )
    hr: List[Hr] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://ns.editeur.org/onix/3.1/reference",
        }
    )
    address: List["Address"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://ns.editeur.org/onix/3.1/reference",
        }
    )
    dl: List[Dl] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://ns.editeur.org/onix/3.1/reference",
        }
    )
    ol: List[Ol] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://ns.editeur.org/onix/3.1/reference",
        }
    )
    ul: List[Ul] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://ns.editeur.org/onix/3.1/reference",
        }
    )
    h6: List["H6"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://ns.editeur.org/onix/3.1/reference",
        }
    )
    h5: List["H5"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://ns.editeur.org/onix/3.1/reference",
        }
    )
    h4: List["H4"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://ns.editeur.org/onix/3.1/reference",
        }
    )
    h3: List["H3"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://ns.editeur.org/onix/3.1/reference",
        }
    )
    h2: List["H2"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://ns.editeur.org/onix/3.1/reference",
        }
    )
    h1: List["H1"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://ns.editeur.org/onix/3.1/reference",
        }
    )


@dataclass
class Blockquote(Block):
    class Meta:
        name = "blockquote"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[BlockquoteDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    cite: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Flow:
    content: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "table",
                    "type": Type["Table"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "p",
                    "type": Type["P"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "div",
                    "type": Type["Div"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "blockquote",
                    "type": Blockquote,
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "pre",
                    "type": Pre,
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "hr",
                    "type": Hr,
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "address",
                    "type": Type["Address"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "dl",
                    "type": Dl,
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "ol",
                    "type": Ol,
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "ul",
                    "type": Ul,
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "h6",
                    "type": Type["H6"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "h5",
                    "type": Type["H5"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "h4",
                    "type": Type["H4"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "h3",
                    "type": Type["H3"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "h2",
                    "type": Type["H2"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "h1",
                    "type": Type["H1"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "a",
                    "type": Type["A"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "sup",
                    "type": Type["Sup"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "sub",
                    "type": Type["Sub"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "q",
                    "type": Type["Q"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "acronym",
                    "type": Type["Acronym"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "abbr",
                    "type": Type["Abbr"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "cite",
                    "type": Type["Cite"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "var",
                    "type": Type["Var"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "kbd",
                    "type": Type["Kbd"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "samp",
                    "type": Type["Samp"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "code",
                    "type": Type["Code"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "dfn",
                    "type": Type["Dfn"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "strong",
                    "type": Type["Strong"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "em",
                    "type": Type["Em"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "small",
                    "type": Type["Small"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "big",
                    "type": Type["Big"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "b",
                    "type": Type["B"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "i",
                    "type": Type["I"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "tt",
                    "type": Type["Tt"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "map",
                    "type": Type["Map"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "img",
                    "type": Img,
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "br",
                    "type": Br,
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "bdo",
                    "type": Type["Bdo"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "span",
                    "type": Type["Span"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
            ),
        }
    )


@dataclass
class Dd(Flow):
    class Meta:
        name = "dd"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[DdDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Div(Flow):
    class Meta:
        name = "div"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[DivDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Li(Flow):
    class Meta:
        name = "li"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[LiDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Td(Flow):
    class Meta:
        name = "td"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[TdDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    abbr: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    axis: Optional[object] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    headers: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Attribute",
            "tokens": True,
        }
    )
    scope: Optional[Scope] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    rowspan: str = field(
        default="1",
        metadata={
            "type": "Attribute",
        }
    )
    colspan: str = field(
        default="1",
        metadata={
            "type": "Attribute",
        }
    )
    align: Optional[TdAlign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    char: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    charoff: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    valign: Optional[TdValign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Th(Flow):
    class Meta:
        name = "th"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[ThDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    abbr: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    axis: Optional[object] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    headers: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Attribute",
            "tokens": True,
        }
    )
    scope: Optional[Scope] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    rowspan: str = field(
        default="1",
        metadata={
            "type": "Attribute",
        }
    )
    colspan: str = field(
        default="1",
        metadata={
            "type": "Attribute",
        }
    )
    align: Optional[ThAlign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    char: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    charoff: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    valign: Optional[ThValign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Tr:
    class Meta:
        name = "tr"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    th: List[Th] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    td: List[Td] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[TrDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    align: Optional[TrAlign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    char: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    charoff: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    valign: Optional[TrValign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Tbody:
    class Meta:
        name = "tbody"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    tr: List[Tr] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[TbodyDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    align: Optional[TbodyAlign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    char: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    charoff: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    valign: Optional[TbodyValign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Tfoot:
    class Meta:
        name = "tfoot"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    tr: List[Tr] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[TfootDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    align: Optional[TfootAlign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    char: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    charoff: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    valign: Optional[TfootValign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Thead:
    class Meta:
        name = "thead"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    tr: List[Tr] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[TheadDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    align: Optional[TheadAlign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    char: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    charoff: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    valign: Optional[TheadValign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Table:
    class Meta:
        name = "table"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    caption: Optional["Caption"] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    col: List[Col] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    colgroup: List[Colgroup] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    thead: Optional[Thead] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    tfoot: Optional[Tfoot] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    tbody: List[Tbody] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    tr: List[Tr] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[TableDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    summary: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    width: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    border: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    frame: Optional[Tframe] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    rules: Optional[Trules] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    cellspacing: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    cellpadding: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Map:
    class Meta:
        name = "map"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    table: List[Table] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    p: List["P"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    div: List[Div] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    blockquote: List[Blockquote] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    pre: List[Pre] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    hr: List[Hr] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    address: List["Address"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    dl: List[Dl] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    ol: List[Ol] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    ul: List[Ul] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    h6: List["H6"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    h5: List["H5"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    h4: List["H4"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    h3: List["H3"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    h2: List["H2"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    h1: List["H1"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    area: List[Area] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[MapDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class AContent:
    class Meta:
        name = "a.content"

    content: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "map",
                    "type": Map,
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "img",
                    "type": Img,
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "br",
                    "type": Br,
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "bdo",
                    "type": Type["Bdo"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "span",
                    "type": Type["Span"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "small",
                    "type": Type["Small"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "big",
                    "type": Type["Big"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "b",
                    "type": Type["B"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "i",
                    "type": Type["I"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "tt",
                    "type": Type["Tt"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "sup",
                    "type": Type["Sup"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "sub",
                    "type": Type["Sub"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "q",
                    "type": Type["Q"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "acronym",
                    "type": Type["Acronym"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "abbr",
                    "type": Type["Abbr"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "cite",
                    "type": Type["Cite"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "var",
                    "type": Type["Var"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "kbd",
                    "type": Type["Kbd"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "samp",
                    "type": Type["Samp"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "code",
                    "type": Type["Code"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "dfn",
                    "type": Type["Dfn"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "strong",
                    "type": Type["Strong"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "em",
                    "type": Type["Em"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
            ),
        }
    )


@dataclass
class A(AContent):
    class Meta:
        name = "a"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[ADir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    charset: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    rel: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    rev: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    accesskey: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    shape: Shape = field(
        default=Shape.RECT,
        metadata={
            "type": "Attribute",
        }
    )
    coords: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    tabindex: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    onfocus: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    onblur: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Inline:
    content: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "a",
                    "type": A,
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "sup",
                    "type": Type["Sup"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "sub",
                    "type": Type["Sub"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "q",
                    "type": Type["Q"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "acronym",
                    "type": Type["Acronym"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "abbr",
                    "type": Type["Abbr"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "cite",
                    "type": Type["Cite"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "var",
                    "type": Type["Var"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "kbd",
                    "type": Type["Kbd"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "samp",
                    "type": Type["Samp"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "code",
                    "type": Type["Code"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "dfn",
                    "type": Type["Dfn"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "strong",
                    "type": Type["Strong"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "em",
                    "type": Type["Em"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "small",
                    "type": Type["Small"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "big",
                    "type": Type["Big"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "b",
                    "type": Type["B"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "i",
                    "type": Type["I"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "tt",
                    "type": Type["Tt"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "map",
                    "type": Map,
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "img",
                    "type": Img,
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "br",
                    "type": Br,
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "bdo",
                    "type": Type["Bdo"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
                {
                    "name": "span",
                    "type": Type["Span"],
                    "namespace": "http://ns.editeur.org/onix/3.1/reference",
                },
            ),
        }
    )


@dataclass
class Abbr(Inline):
    class Meta:
        name = "abbr"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[AbbrDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Acronym(Inline):
    class Meta:
        name = "acronym"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[AcronymDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Address(Inline):
    class Meta:
        name = "address"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[AddressDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class B(Inline):
    class Meta:
        name = "b"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[BDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Bdo(Inline):
    class Meta:
        name = "bdo"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[BdoDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class Big(Inline):
    class Meta:
        name = "big"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[BigDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Caption(Inline):
    class Meta:
        name = "caption"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[CaptionDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Cite(Inline):
    class Meta:
        name = "cite"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[CiteDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Code(Inline):
    class Meta:
        name = "code"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[CodeDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Dfn(Inline):
    class Meta:
        name = "dfn"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[DfnDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Dt(Inline):
    class Meta:
        name = "dt"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[DtDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Em(Inline):
    class Meta:
        name = "em"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[EmDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class H1(Inline):
    class Meta:
        name = "h1"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[H1Dir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class H2(Inline):
    class Meta:
        name = "h2"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[H2Dir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class H3(Inline):
    class Meta:
        name = "h3"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[H3Dir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class H4(Inline):
    class Meta:
        name = "h4"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[H4Dir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class H5(Inline):
    class Meta:
        name = "h5"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[H5Dir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class H6(Inline):
    class Meta:
        name = "h6"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[H6Dir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class I(Inline):
    class Meta:
        name = "i"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[IDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Kbd(Inline):
    class Meta:
        name = "kbd"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[KbdDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class P(Inline):
    class Meta:
        name = "p"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[PDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Q(Inline):
    class Meta:
        name = "q"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[QDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    cite: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Samp(Inline):
    class Meta:
        name = "samp"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[SampDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Small(Inline):
    class Meta:
        name = "small"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[SmallDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Span(Inline):
    class Meta:
        name = "span"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[SpanDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Strong(Inline):
    class Meta:
        name = "strong"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[StrongDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Sub(Inline):
    class Meta:
        name = "sub"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[SubDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Sup(Inline):
    class Meta:
        name = "sup"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[SupDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Tt(Inline):
    class Meta:
        name = "tt"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[TtDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Var(Inline):
    class Meta:
        name = "var"
        namespace = "http://ns.editeur.org/onix/3.1/reference"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dir: Optional[VarDir] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
