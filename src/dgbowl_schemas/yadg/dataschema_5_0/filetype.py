from pydantic import BaseModel, Extra, Field, validator
from abc import ABC
from typing import Optional, Literal, Union
import tzlocal
import locale

from .stepdefaults import StepDefaults


class FileType(BaseModel, ABC, extra=Extra.forbid):
    """Template ABC for parser classes."""

    filetype: Optional[str]
    timezone: Optional[str]
    locale: Optional[str]
    encoding: Optional[str]

    @validator("timezone", always=True)
    @classmethod
    def timezone_resolve_localtime(cls, v):
        if v == "localtime":
            v = tzlocal.get_localzone_name()
        return v

    @validator("locale", always=True)
    @classmethod
    def locale_set_default(cls, v):
        if v == "getlocale":
            v = ".".join(locale.getlocale())
        return v


class NoFileType(FileType):
    filetype: Optional[None] = None


class Tomato_json(FileType):
    filetype: Literal["tomato.json"]


DummyFileTypes = Union[
    NoFileType,
    Tomato_json,
]


class Drycal_csv(FileType):
    filetype: Literal["drycal.csv"]


class Drycal_rtf(FileType):
    filetype: Literal["drycal.rtf"]


class Drycal_txt(FileType):
    filetype: Literal["drycal.txt"]


FlowDataFileTypes = Union[
    Drycal_csv,
    Drycal_rtf,
    Drycal_txt,
]


class EClab_mpr(FileType):
    filetype: Literal["eclab.mpr", "marda:biologic-mpr"]


class EClab_mpt(FileType):
    filetype: Literal["eclab.mpt", "marda:biologic-mpt"]
    encoding: str = "windows-1252"


ElectroChemFileTypes = Union[
    EClab_mpr,
    EClab_mpt,
    Tomato_json,
]


class EZChrom_asc(FileType):
    filetype: Literal["ezchrom.asc"]


class Fusion_json(FileType):
    filetype: Literal["fusion.json"]


class Fusion_zip(FileType):
    filetype: Literal["fusion.zip"]


class Fusion_csv(FileType):
    filetype: Literal["fusion.csv"]


class Agilent_ch(FileType):
    filetype: Literal["agilent.ch", "marda:agilent-ch"]


class Agilent_dx(FileType):
    filetype: Literal["agilent.dx", "marda:agilent-dx"]


class Agilent_csv(FileType):
    filetype: Literal["agilent.csv"]


class EmpaLC_csv(FileType):
    filetype: Literal["empalc.csv"]


class EmpaLC_xlsx(FileType):
    filetype: Literal["empalc.xlsx"]


ChromTraceFileTypes = Union[
    EZChrom_asc,
    Fusion_json,
    Fusion_zip,
    Agilent_ch,
    Agilent_dx,
    Agilent_csv,
]

ChromDataFileTypes = Union[
    Fusion_json,
    Fusion_zip,
    Fusion_csv,
    EmpaLC_csv,
    EmpaLC_xlsx,
]


class Quadstar_sac(FileType):
    filetype: Literal["quadstar.sac"]


MassTraceFileTypes = Quadstar_sac


class LabView_csv(FileType):
    filetype: Literal["labview.csv"]


QFTraceFileTypes = LabView_csv


class Phi_spe(FileType):
    filetype: Literal["phi.spe", "marda:phi-spe"]


XPSTraceFileTypes = Phi_spe


class Panalytical_xrdml(FileType):
    filetype: Literal["panalytical.xrdml", "marda:panalytical-xrdml"]


class Panalytical_xy(FileType):
    filetype: Literal["panalytical.xy"]


class Panalytical_csv(FileType):
    filetype: Literal["panalytical.csv"]


XRDTraceFileTypes = Union[
    Panalytical_xrdml,
    Panalytical_xy,
    Panalytical_csv,
]


class ExtractorFactory(BaseModel):
    extractor: Union[
        DummyFileTypes,
        FlowDataFileTypes,
        ElectroChemFileTypes,
        ChromDataFileTypes,
        ChromTraceFileTypes,
        MassTraceFileTypes,
        QFTraceFileTypes,
        XPSTraceFileTypes,
        XRDTraceFileTypes,
    ] = Field(..., discriminator="filetype")

    @validator("extractor", always=True)
    @classmethod
    def extractor_set_defaults(cls, v):
        defaults = StepDefaults()
        if v.timezone is None:
            v.timezone = defaults.timezone
        if v.locale is None:
            v.locale = defaults.locale

        return v
