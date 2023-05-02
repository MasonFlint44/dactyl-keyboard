from math import pi
from typing import List, Literal, Optional, Tuple

from pydantic import BaseModel, Field

d2r = pi / 180
r2d = 180 / pi

EngineType = Literal["solid", "cadquery"]


class EngineConfig(BaseModel):
    engine: EngineType = Field(default="solid", alias="ENGINE")


SymmetryType = Literal["symmetric", "asymmetric"]
ColumnStyleType = Literal["standard", "orthographic", "fixed"]


class ShapeConfig(BaseModel):
    save_dir: str = "."
    config_name: str = "DM"
    overrides: str = ""
    save_name: str = ""
    logo_file: Optional[str] = None
    show_caps: bool = True
    show_pcbs: bool = Field(
        default=False,
        description="only runs if caps are shown, easist place to initially inject geometry",
    )
    nrows: int = Field(default=5, description="key rows")
    ncols: int = Field(default=6, description="key columns")
    alpha: float = Field(default=pi / 12.0, description="curvature of the columns")
    beta: float = Field(default=pi / 36.0, description="curvature of the rows")
    centercol: int = Field(
        default=3,
        description="controls left_right tilt / tenting (higher number is more tenting)",
    )
    centerrow_offset: int = Field(
        default=3, description="rows from max, controls front_back tilt"
    )
    tenting_angle: float = Field(
        default=pi / 12.0, description="more precise tenting control"
    )
    symmetry: SymmetryType = Field(
        default="symmetric",
        description="if it is a symmetric or asymmetric bui.  If asymmetric it doubles the generation time.",
    )
    column_style_gt5: ColumnStyleType = "orthographic"
    column_style: ColumnStyleType = "standard"
    thumb_offsets: List[int] = [6, -3, 7]
    full_last_rows: bool = False
    keyboard_z_offset: int = Field(
        default=11,
        description="controls overall height (original=9 with centercol=3 - use 16 for centercol=2)",
    )
    column_offsets: List[List[float]] = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 2.82, -4.5],
        [0, 0, 0],
        [0, -6, 5],  # REDUCED STAGGER
        [0, -6, 5],  # REDUCED STAGGER
        [0, -6, 5],  # NOT USED IN MOST FORMATS (7th column)
        [0, -6, 5],  # NOT USED IN MOST FORMATS (8th column)
        [0, -6, 5],  # NOT USED IN MOST FORMATS (9th column)
    ]
    screw_offsets: List[List[float]] = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]
    logo_offsets: List[float] = [-10, -10, -1]


ThumbStyleType = Literal[
    "DEFAULT", "MINI", "CARBONFET", "MINIDOX", "TRACKBALL_ORBYL", "TRACKBALL_CJ"
]


class ThumbConfig(BaseModel):
    thumb_style: ThumbStyleType = "TRACKBALL_ORBYL"
    default_1U_cluster: Optional[bool] = Field(
        default=True,
        description="only used with default, makes top right thumb cluster key 1U",
    )
    minidox_Usize: float = Field(
        default=1.6,
        description="Thumb key size.  May need slight oversizing, check w/ caps.  Additional spacing will be automatically added for larger keys.",
    )
    thumb_plate_tr_rotation: float = Field(
        default=0.0,
        description="Top right plate rotation tweaks as thumb cluster is crowded for hot swap, etc. - MUST be in 90 degree increments.",
        multiple_of=90.0,
    )
    thumb_plate_tl_rotation: float = Field(
        default=0.0,
        description="Top left plate rotation tweaks as thumb cluster is crowded for hot swap, etc. - MUST be in 90 degree increments.",
        multiple_of=90.0,
    )
    thumb_plate_mr_rotation: float = Field(
        default=0.0,
        description="Mid right plate rotation tweaks as thumb cluster is crowded for hot swap, etc. - MUST be in 90 degree increments.",
        multiple_of=90.0,
    )
    thumb_plate_ml_rotation: float = Field(
        default=0.0,
        description="Mid left plate rotation tweaks as thumb cluster is crowded for hot swap, etc. - MUST be in 90 degree increments.",
        multiple_of=90.0,
    )
    thumb_plate_br_rotation: float = Field(
        default=0.0,
        description="Bottom right plate rotation tweaks as thumb cluster is crowded for hot swap, etc. - MUST be in 90 degree increments.",
        multiple_of=90.0,
    )
    thumb_plate_bl_rotation: float = Field(
        default=0.0,
        description="Bottom left plate rotation tweaks as thumb cluster is crowded for hot swap, etc. - MUST be in 90 degree increments.",
        multiple_of=90.0,
    )


class TrackballInWallConfig(BaseModel):
    trackball_in_wall: bool = Field(
        default=False,
        description="Separate trackball option, placing it in the OLED area",
    )
    tbiw_ball_center_row: float = Field(
        default=0.2, description="up from cornerrow instead of down from top"
    )
    tbiw_translational_offset: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    tbiw_rotation_offset: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    tbiw_left_wall_x_offset_override: float = 50.0
    tbiw_left_wall_z_offset_override: float = 0.0
    tbiw_left_wall_lower_y_offset: float = 0.0
    tbiw_left_wall_lower_z_offset: float = 0.0
    tbiw_oled_center_row: float = Field(
        default=0.75, description="offsets are from this position"
    )
    tbiw_oled_translation_offset: Tuple[float, float, float] = Field(
        default=(-3.5, 0, 1.5),
        description="# Z offset tweaks are expected depending on curvature and OLED mount choice.",
    )
    tbiw_oled_rotation_offset: Tuple[float, float, float] = (0, 0, 0)


class TrackballJsConfig(BaseModel):
    other_thumb: Optional[ThumbStyleType] = Field(
        default="DEFAULT",
        description="cluster used for second thumb unless ball_side == 'both'",
    )
    tbjs_key_diameter: int = 70
    tbjs_translation_offset: Tuple[int, int, int] = Field(
        default=(0, 0, 10), description="applied to the whole assy"
    )
    tbjs_rotation_offset: Tuple[int, int, int] = Field(
        default=(0, 0, 0), description="applied to the whole assy"
    )
    tbjs_key_translation_offsets: List[Tuple[float, float, float]] = Field(
        default=[
            (0.0, 0.0, -3.0 - 5),
            (0.0, 0.0, -3.0 - 5),
            (0.0, 0.0, -3.0 - 5),
            (0.0, 0.0, -3.0 - 5),
        ],
        description="Offsets are per key and are applied before rotating into place around the ball. X and Y act like Tangential and Radial around the ball",
    )
    tbjs_key_rotation_offsets: List[Tuple[float, float, float]] = Field(
        default=[
            (0.0, 0.0, 0.0),
            (0.0, 0.0, 0.0),
            (0.0, 0.0, 0.0),
            (0.0, 0.0, 0.0),
        ],
        description="Offsets are per key and are applied before rotating into place around the ball. X and Y act like Tangential and Radial around the ball",
    )


class TrackballCjConfig(BaseModel):
    tbcj_inner_diameter: int = 42
    tbcj_thickness: int = 2
    tbcj_outer_diameter: int = 53


BallSideType = Literal["left", "right", "both"]


class TrackballConfig(BaseModel):
    trackball_modular: bool = Field(
        default=False,
        description="May add removable trackball in subsequent releases, no current use.",
    )
    trackball_Usize: float = Field(
        default=1.5, description="size for inner key near trackball"
    )
    ball_side: BallSideType = "right"
    ball_diameter: float = 34.0
    ball_wall_thickness: int = Field(
        default=3,
        description="should not be changed unless the import models are changed.",
    )
    ball_gap: float = 1.0
    trackball_hole_diameter: float = 36.5
    trackball_hole_height: int = 40
    trackball_plate_thickness: int = 2
    trackball_plate_width: int = 2
    tb_socket_translation_offset: Tuple[int, int, float] = Field(
        default=(0, 0, 2.0),
        description="applied to the socket and sensor, large values will cause web/wall issues.",
    )
    tb_socket_rotation_offset: Tuple[int, int, int] = Field(
        default=(0, 0, 0),
        description="applied to the socket and sensor, large values will cause web/wall issues.",
    )
    tb_sensor_translation_offset: Tuple[int, int, int] = Field(
        default=(0, 0, 0),
        description="deviation from socket offsets, for fixing generated geometry issues",
    )
    tb_sensor_rotation_offset: Tuple[int, int, int] = Field(
        default=(0, 0, 0),
        description="deviation from socket offsets, for fixing generated geometry issues",
    )


class ExperimentalConfig(BaseModel):
    pinky_1_5U: bool = Field(
        default=False, description="LEAVE AS FALSE, CURRENTLY BROKEN"
    )
    first_1_5U_row: int = 0
    last_1_5U_row: int = 5
    # TODO: are below part of ShapeConfig instead?
    extra_width: float = Field(
        default=2.5, description="extra space between the base of keys - original=2"
    )
    extra_height: float = Field(default=1.0, description="original= 0.5")
    wall_z_offset: int = Field(
        default=15, description="length of the first downward_sloping part of the wall"
    )
    wall_x_offset: int = Field(
        default=5,
        description="offset in the x and/or y direction for the first downward_sloping part of the wall (negative)",
    )
    wall_y_offset: int = Field(
        default=6,
        description="offset in the x and/or y direction for the first downward_sloping part of the wall (negative)",
    )
    left_wall_x_offset: int = Field(
        default=12,
        description="specific values for the left side due to the minimal wall.",
    )
    left_wall_z_offset: int = Field(
        default=3,
        description="specific values for the left side due to the minimal wall.",
    )
    left_wall_lower_y_offset: int = Field(
        default=0, description="specific values for the lower left corner."
    )
    left_wall_lower_z_offset: int = 0
    wall_thickness: float = Field(
        default=4.5,
        description="wall thickness parameter used on upper/mid stage of the wall",
    )
    wall_base_y_thickness: float = Field(
        default=4.5, description="wall thickness at the lower stage"
    )
    wall_base_x_thickness: float = Field(
        default=4.5, description="wall thickness at the lower stage"
    )
    wall_base_back_thickness: float = Field(
        default=4.5,
        description="wall thickness at the lower stage specifically in back for interface",
    )


class FixedColumnStyleConfig(BaseModel):
    """
    Settings for column_style == fixed.
    The defaults roughly match Maltron settings.
    http://patentimages.storage.googleapis.com/EP0219944A2/imgf0002.png

    NOTE: THIS DOESN'T WORK QUITE LIKE I'D HOPED.
    """

    fixed_angles: List[float] = [d2r * 10, d2r * 10, 0, 0, 0, d2r * -15, d2r * -15]
    fixed_x: List[float] = Field(
        default=[], description="relative to the middle finger"
    )
    fixed_z: List[float] = Field(
        default=[], description="overrides the z portion of the column ofsets above"
    )
    fixed_tenting: float = 0


# PlateStyleType options:
# 'HOLE'        A square hole. Also useful for applying custom plate files.
# 'NUB'         Original side nubs.
# 'UNDERCUT'    Snap fit undercut. May require CLIP_THICKNESS and possibly
#                   CLIP_UNDERCUT tweaking and/or filing to get proper snap.
# 'NOTCH'       Snap fit undercut only near switch clip. May require CLIP_THICKNESS
#                   and possibly CLIP_UNDERCUT tweaking and/or filing to get proper snap.
# 'HS_NUB'      Hot swap underside with nubs.
# 'HS_UNDERCUT' Hot swap underside with undercut. Does not generate properly.
#                   Hot swap step needs to be modified.
# 'HS_NOTCH'    Hot swap underside with notch. Does not generate properly.
#                   Hot swap step needs to be modified.
PlateStyleType = Literal[
    "HOLE", "NUB", "UNDERCUT", "NOTCH", "HS_NUB", "HS_UNDERCUT", "HS_NOTCH"
]


class SwitchHoleConfig(BaseModel):
    plate_style: PlateStyleType = "NOTCH"
    hole_keyswitch_height: float = 14.0
    hole_keyswitch_width: float = 14.0
    nub_keyswitch_height: float = 14.4
    nub_keyswitch_width: float = 14.4
    undercut_keyswitch_height: float = 14.0
    undercut_keyswitch_width: float = 14.0
    notch_width: float = Field(
        default=5.0,
        description="If using notch, it is identical to undecut, but only locally by the switch clip",
    )
    sa_profile_key_height: float = 12.7
    sa_length: float = 18.5
    sa_double_length: float = 37.5
    plate_thickness: float = 4 + 1.1
    plate_rim: float = 1.5 + 0.5
    clip_thickness: float = 1.4
    clip_undercut: float = 1.0
    undercut_transition: float = Field(
        default=0.2,
        description="NOT FUNCTIONAL WITH OPENSCAD, ONLY WORKS WITH CADQUERY",
    )
    plate_file: Optional[str] = Field(
        default=None, description="Custom plate step file"
    )
    plate_offset: float = 0.0


class BaseOledConfig(BaseModel):
    oled_mount_width: float = Field(
        default=12.5, description="width of OLED, plus clearance"
    )
    oled_mount_height: float = Field(..., description="length of screen")
    oled_mount_rim: float
    oled_mount_depth: float
    oled_mount_cut_depth: float = 20.0
    oled_mount_location_xyz: Tuple[float, float, float] = Field(
        ..., description="will be overwritten if oled_center_row is not None"
    )
    oled_mount_rotation_xyz: Tuple[float, float, float] = Field(
        ..., description="will be overwritten if oled_center_row is not None"
    )
    oled_left_wall_x_offset_override: float = 24.0
    oled_left_wall_z_offset_override: float = 0.0
    oled_left_wall_lower_y_offset: float = 12.0
    oled_left_wall_lower_z_offset: float = 5.0


class UndercutOledConfig(BaseOledConfig):
    oled_mount_width: float = Field(
        default=15.0, description="width of OLED, plus clearance"
    )
    oled_mount_height: float = Field(default=35.0, description="length of screen")
    oled_mount_rim: float = 3.0
    oled_mount_depth: float = 6.0
    oled_mount_location_xyz: Tuple[float, float, float] = Field(
        default=(-80.0, 20.0, 45.0),
        description="will be overwritten if oled_center_row is not None",
    )
    oled_mount_rotation_xyz: Tuple[float, float, float] = Field(
        default=(13.0, 0.0, -6.0),
        description="will be overwritten if oled_center_row is not None",
    )
    oled_left_wall_x_offset_override: float = 28.0
    oled_mount_undercut: float = 1.0
    oled_mount_undercut_thickness: float = 2.0


class SlidingOledConfig(BaseOledConfig):
    oled_mount_height: float = Field(default=25.0, description="length of screen")
    oled_mount_rim: float = 2.5
    oled_mount_depth: float = 8.0
    oled_mount_location_xyz: Tuple[float, float, float] = Field(
        default=(-78.0, 10.0, 41.0),
        description="will be overwritten if oled_center_row is not None",
    )
    oled_mount_rotation_xyz: Tuple[float, float, float] = Field(
        default=(6.0, 0.0, -3.0),
        description="will be overwritten if oled_center_row is not None",
    )
    oled_thickness: float = Field(
        default=4.2,
        description="thickness of OLED, plus clearance.  Must include components",
    )
    oled_edge_overlap_end: float = Field(
        default=6.5, description="length from end of viewable screen to end of PCB"
    )
    oled_edge_overlap_connector: float = Field(
        default=5.5,
        description="length from end of viewable screen to end of PCB on connection side.",
    )
    oled_edge_overlap_thickness: float = Field(
        default=2.5, description="thickness of material over edge of PCB"
    )
    oled_edge_overlap_clearance: float = Field(
        default=2.5,
        description="Clearance to insert PCB before laying down and sliding.",
    )
    oled_edge_chamfer: float = 2.0


class ClipOledConfig(BaseOledConfig):
    oled_mount_height: float = Field(default=39.0, description="length of screen")
    oled_mount_rim: float = 2.0
    oled_mount_depth: float = 7.0
    oled_mount_location_xyz: Tuple[float, float, float] = Field(
        default=(-78.0, 20.0, 42.0),
        description="will be overwritten if oled_center_row is not None",
    )
    oled_mount_rotation_xyz: Tuple[float, float, float] = Field(
        default=(12.0, 0.0, -6.0),
        description="will be overwritten if oled_center_row is not None",
    )
    oled_thickness: float = Field(
        default=4.2,
        description="thickness of OLED, plus clearance.  Must include components",
    )
    oled_mount_bezel_thickness: float = Field(
        default=3.5, description="z thickness of clip bezel"
    )
    oled_mount_bezel_chamfer: float = Field(
        default=2.0, description="depth of the 45 degree chamfer"
    )
    oled_mount_connector_hole: float = 6.0
    oled_screen_start_from_conn_end: float = 6.5
    oled_screen_length: float = 24.5
    oled_screen_width: float = 10.5
    oled_clip_thickness: float = 1.5
    oled_clip_width: float = 6.0
    oled_clip_overhang: float = 1.0
    oled_clip_extension: float = 5.0
    oled_clip_width_clearance: float = 0.5
    oled_clip_undercut: float = 0.5
    oled_clip_undercut_thickness: float = 2.5
    oled_clip_y_gap: float = 0.2
    oled_clip_z_gap: float = 0.2


class OledConfigs(BaseModel):
    undercut: UndercutOledConfig = Field(default=UndercutOledConfig(), alias="UNDERCUT")
    sliding: SlidingOledConfig = Field(default=SlidingOledConfig(), alias="SLIDING")
    clip: ClipOledConfig = Field(default=ClipOledConfig(), alias="CLIP")


# OledMountType options:
# Initial pass will be manual placement.  Can be used to create other mounts as well.
# 'NONE'        No OLED mount
# 'UNDERCUT'    Simple rectangle with undercut for clip in item
# 'SLIDING'     Features to slide the OLED in place and use a pin or block to secure from underneath.
# 'CLIP'        Features to set the OLED in a frame a snap a bezel down to hold it in place.
OledMountType = Literal["NONE", "UNDERCUT", "SLIDING", "CLIP"]
ScrewsOffsetType = Literal["INSIDE", "OUTSIDE", "ORIGINAL"]


class OledMountConfig(BaseModel):
    oled_mount_type: Optional[OledMountType] = "CLIP"
    oled_center_row: Optional[float] = Field(
        default=1.25,
        description="if not None, this will override the oled_mount_location_xyz and oled_mount_rotation_xyz settings",
    )
    oled_translation_offset: Tuple[int, int, int] = Field(
        default=(0, 0, 4),
        description="Z offset tweaks are expected depending on curvature and OLED mount choice.",
    )
    oled_rotation_offset: Tuple[int, int, int] = (0, 0, 0)
    oled_configurations: OledConfigs = OledConfigs()
    web_thickness: float = 4.0
    post_size: float = 0.1
    post_adj: int = 0
    screws_offset: ScrewsOffsetType = "INSIDE"
    screw_insert_height: float = 3.8
    screw_insert_bottom_radius: float = 5.31 / 2
    screw_insert_top_radius: float = 5.1 / 2
    wire_post_height: int = 7
    wire_post_overhang: float = 3.5
    wire_post_diameter: float = 2.6


# ControllerMountType options:
# RJ9_USB_WALL          Standard internal plate with RJ9 opening and square cutout for connection.
# USB_WALL              Standard internal plate with a square cutout for connection, no RJ9.
# RJ9_USB_TEENSY        Teensy holder
# USB_TEENSY            Teensy holder, no RJ9
# EXTERNAL              square cutout for a holder such as the one from lolligagger.
# BLACKPILL_EXTERNAL    larger square cutout for lolligagger type holder modified for the blackpill.
# NONE                  No openings in the back.
ControllerMountType = Literal[
    "RJ9_USB_WALL",
    "USB_WALL",
    "RJ9_USB_TEENSY",
    "USB_TEENSY",
    "EXTERNAL",
    "BLACKPILL_EXTERNAL",
    "NONE",
]


class ControllerMountConfig(BaseModel):
    controller_mount_type: ControllerMountType = "EXTERNAL"
    external_holder_height: float = 12.5
    external_holder_width: float = 28.75
    external_holder_xoffset: float = -5.0
    external_holder_yoffset: float = Field(
        default=-4.5,
        description="Tweak this value to get the right undercut for the tray engagement. Offset is from the top inner corner of the top inner key.",
    )
    blackpill_holder_width: Optional[float] = 32.0
    blackpill_holder_xoffset: Optional[float] = -6.5


class BottomPlateConfig(BaseModel):
    screw_hole_diameter: int = 2
    base_thickness: float = Field(
        default=3.0, description="thickness in the middle of the plate"
    )
    base_offset: float = Field(
        default=3.0,
        description="Both start flat/flush on the bottom.  This offsets the base up (if positive)",
    )
    base_rim_thickness: float = Field(
        default=5.0, description="thickness on the outer frame with screws"
    )
    screw_cbore_diameter: float = 4.0
    screw_cbore_depth: float = 2.0


class PlateHolesConfig(BaseModel):
    plate_holes: bool = False
    plate_holes_xy_offset: Tuple[float, float] = (0.0, 0.0)
    plate_holes_width: float = 14.3
    plate_holes_height: float = 14.3
    plate_holes_diameter: float = 1.7
    plate_holes_depth: float = 20.0


class PcbConfig(BaseModel):
    pcb_width: float = 18.0
    pcb_height: float = 18.0
    pcb_thickness: float = 1.5
    pcb_hole_diameter: int = 2
    pcb_hole_pattern_width: float = 14.3
    pcb_hole_pattern_height: float = 14.3
