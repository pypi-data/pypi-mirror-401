"""Type definitions and enums for the Blendflare API."""

from enum import Enum
from typing import Dict, List, Optional


class Category(str, Enum):
    """Main asset categories."""

    ARCHITECTURE = "architecture"
    CHARACTER = "character"
    ACCESSORIES = "accessories"
    DECORATION = "decoration"
    INDUSTRIAL = "industrial"
    INTERIOR = "interior"
    MILITARY = "military"
    NATURE = "nature"
    # SCIENCE = "science"
    SPACE = "space"
    SPORT_HOBBY = "sport_hobby"
    TECHNOLOGY = "technology"
    TRANSPORT = "transport"
    NODE_GROUP = "node_group"
    MATERIALS = "materials"
    HDRIS = "hdris"
    BRUSHES = "brushes"
    DECALS = "decals"
    SCENES = "scenes"
    SIMULATIONS_VFX = "simulations_vfx"
    ANIMATION_RIGS = "animation_rigs"
    TEMPLATE_SETUPS = "template_setups"
    EDUCATIONAL = "educational"
    LIGHTING = "lighting"
    RESEARCH = "research"


class Subcategory(str, Enum):
    """Subcategories for assets."""

    # Accessories
    BAGS_CARRIERS = "bags_carriers"
    BELTS_STRAPS = "belts_straps"
    EYEWEAR = "eyewear"
    FASHION_ACCESSORIES = "fashion_accessories"
    FOOTWEAR = "footwear"
    GLOVES_HAND_ACCESSORIES = "gloves_hand_accessories"
    HAIR_ACCESSORIES = "hair_accessories"
    HEADWEAR = "headwear"
    JEWELRY = "jewelry"
    OTHER = "other"
    SCARVES_NECKWEAR = "scarves_neckwear"
    TECH_ACCESSORIES = "tech_accessories"

    # Animation Rigs
    ANIMAL_RIGS = "animal_rigs"
    ANIMATION_PRESETS = "animation_presets"
    CHARACTER_RIGS = "character_rigs"
    CONTROLLERS_UI = "controllers_ui"
    CREATURE_RIGS = "creature_rigs"
    FACIAL_RIGS = "facial_rigs"
    HAND_RIGS = "hand_rigs"
    IK_FK_SYSTEMS = "ik_fk_systems"
    MECHANICAL_RIGS = "mechanical_rigs"
    MOTION_CAPTURE = "motion_capture"
    TAIL_RIGS = "tail_rigs"
    VEHICLE_RIGS = "vehicle_rigs"
    WING_RIGS = "wing_rigs"

    # Architecture
    BALCONY_TERRACE = "balcony_terrace"
    BUILDING = "building"
    DOOR = "door"
    EXTERIOR_ELEMENT = "exterior_element"
    FENCE_RAILING = "fence_railing"
    FLOOR_COVERING = "floor_covering"
    FOUNDATION_STRUCTURAL_BASE = "foundation_structural_base"
    MOLDING_CARVING = "molding_carving"
    ROOF_ROOFING_ELEMENTS = "roof_roofing_elements"
    STAIRS = "stairs"
    STRUCTURE = "structure"
    WALL_PANEL = "wall_panel"
    WINDOW = "window"

    # Brushes
    ANIMAL_CREATURE = "animal_creature"
    ART = "art"
    CLOTHING = "clothing"
    DAMAGE = "damage"
    FABRIC_TEXTILE = "fabric_textile"
    GEOMETRIC = "geometric"
    HAIR_FUR = "hair_fur"
    HUMAN = "human"
    INDUSTRIAL = "industrial"
    NATURE = "nature"
    SCI_FI_TECH = "sci_fi_tech"

    # Character
    ANATOMY = "anatomy"
    ANIMAL = "animal"
    WOMAN_CLOTHING = "woman_clothing"
    MAN_CLOTHING = "man_clothing"
    FANTASY_RACES = "fantasy_races"
    HAIR_HAIRSTYLES = "hair_hairstyles"
    HUMANOIDS = "humanoids"
    MONSTER_CREATURE = "monster_creature"
    ROBOT = "robot"

    # Decals
    BLOOD = "blood"
    BULLET_HOLES = "bullet_holes"
    BURN_MARKS = "burn_marks"
    CRACKS_DAMAGE = "cracks_damage"
    DEBRIS = "debris"
    DECORATION = "decoration"
    DIRT_GRIME = "dirt_grime"
    FLOOR_MARKINGS = "floor_markings"
    FOLIAGE = "foliage"
    FOODS = "foods"
    GRAFFITI = "graffiti"
    IMPERFECTIONS = "imperfections"
    ORGANIC_PATTERNS = "organic_patterns"
    PAINT_CHIPPING = "paint_chipping"
    RUST_CORROSION = "rust_corrosion"
    SCRATCHES_SCUFFS = "scratches_scuffs"
    SIGNAGE = "signage"
    STAINS_SPILLS = "stains_spills"
    SYMBOLS_ICONS = "symbols_icons"
    TEXT_NUMBERS = "text_numbers"
    VEHICLE_MARKINGS = "vehicle_markings"
    WATER_MOISTURE = "water_moisture"
    WEAR_TEAR = "wear_tear"

    # Decoration
    BED_SHEET = "bed_sheet"
    BLANKET = "blanket"
    BOOK = "book"
    CANDLES_CANDLE_HOLDERS = "candles_candle_holders"
    CARPETS = "carpets"
    CLOCK_WATCH = "clock_watch"
    CURTAIN = "curtain"
    DECORATION_SET = "decoration_set"
    FABRICS = "fabrics"
    FIREPLACE = "fireplace"
    FOOD_DRINKS = "food_drinks"
    HOLIDAY_DECORATION = "holiday_decoration"
    MIRROR = "mirror"
    MONEY = "money"
    MUSICAL_INSTRUMENTS = "musical_instruments"
    PICTURE = "picture"
    PILLOW = "pillow"
    SCULPTURE = "sculpture"
    TEXTILE = "textile"
    TOYS_GAMES = "toys_games"
    TROPHY_AWARD = "trophy_award"
    VASE = "vase"

    # Educational
    BEGINNER_PROJECTS = "beginner_projects"
    CHALLENGE_PROJECTS = "challenge_projects"
    COURSE_MATERIALS = "course_materials"
    DOCUMENTATION = "documentation"
    LEARNING_KITS = "learning_kits"
    PRACTICE_SCENES = "practice_scenes"
    STUDY_REFERENCES = "study_references"
    TECHNIQUE_DEMONSTRATIONS = "technique_demonstrations"
    TUTORIAL_FILES = "tutorial_files"
    WORKFLOW_EXAMPLES = "workflow_examples"

    # HDRIs
    ABSTRACT = "abstract"
    ARCHITECTURAL = "architectural"
    CITYSCAPES = "cityscapes"
    FUTURISTIC_ENVIRONMENTS = "futuristic_environments"
    HOLIDAY = "holiday"
    INTERIORS = "interiors"
    LANDSCAPES = "landscapes"
    NIGHTTIME_ENVIRONMENTS = "nighttime_environments"
    PUBLIC = "public"
    RESIDENTIAL = "residential"
    RURAL = "rural"
    SPORTS = "sports"
    STUDIO = "studio"
    URBAN = "urban"
    WATER_ENVIRONMENTS = "water_environments"

    # Industrial
    CONTAINER = "container"
    EQUIPMENT = "equipment"
    MACHINERY = "machinery"
    PARTS = "parts"
    SIGN = "sign"
    TOOLS = "tools"

    # Interior
    ARMCHAIR = "armchair"
    BATHROOM_FURNITURE = "bathroom_furniture"
    BED = "bed"
    CABINETS = "cabinets"
    CHAIR = "chair"
    CONSOLE = "console"
    DRESSING_TABLE = "dressing_table"
    ENTERTAINMENT_CENTER = "entertainment_center"
    HOME_ACCESSORIES = "home_accessories"
    KIDS_FURNITURE = "kids_furniture"
    KITCHEN_FURNITURE = "kitchen_furniture"
    LIGHTS = "lights"
    OFFICE_FURNITURE = "office_furniture"
    OUTDOOR_FURNITURE = "outdoor_furniture"
    POUF = "pouf"
    RESTAURANT_BAR = "restaurant_bar"
    ROOM_DIVIDER_SCREEN = "room_divider_screen"
    SEATING_SET = "seating_set"
    SHELVING_BOOKCASE = "shelving_bookcase"
    SHOPPING_RETAIL = "shopping_retail"
    SIDEBOARD_DRAWERS_CHEST = "sideboard_drawers_chest"
    SOFA = "sofa"
    TABLE = "table"
    WARDROBE = "wardrobe"

    # Lighting
    CINEMATIC_LIGHTING = "cinematic_lighting"
    IES_PROFILES = "ies_profiles"
    LIGHT_RIGS = "light_rigs"
    NATURAL_LIGHTING = "natural_lighting"
    NEON_GLOWING = "neon_glowing"
    NIGHT_LIGHTING = "night_lighting"
    OUTDOOR_LIGHTING = "outdoor_lighting"
    PRODUCT_LIGHTING = "product_lighting"
    STUDIO_LIGHTING = "studio_lighting"
    VOLUMETRIC_LIGHTING = "volumetric_lighting"

    # Materials
    ASPHALT = "asphalt"
    BRICKS = "bricks"
    CARBON_FIBER = "carbon_fiber"
    CERAMIC = "ceramic"
    CONCRETE = "concrete"
    DIRT = "dirt"
    FABRIC = "fabric"
    FLOOR = "floor"
    FOAM = "foam"
    FOOD = "food"
    GLASS = "glass"
    GRASS = "grass"
    GROUND = "ground"
    ICE = "ice"
    LEATHER = "leather"
    LIQUID = "liquid"
    MARBLE = "marble"
    METAL = "metal"
    ORGANIC = "organic"
    ORNAMENTS = "ornaments"
    PAINT = "paint"
    PAPER = "paper"
    PAVING = "paving"
    PLASTER = "plaster"
    PLASTIC = "plastic"
    ROCK = "rock"
    ROOFING = "roofing"
    RUBBER = "rubber"
    RUST = "rust"
    SAND = "sand"
    SOIL = "soil"
    STONE = "stone"
    TECH = "tech"
    TERRAZZO = "terrazzo"
    TILES = "tiles"
    WAX = "wax"
    WOOD = "wood"

    # Military
    AIRCRAFT = "aircraft"
    VEHICLES = "vehicles"
    WATERCRAFT = "watercraft"
    WEAPONS = "weapons"
    EQUIPMENT_GEAR = "equipment_gear"
    ACCESSORIES_MILITARY = "accessories"
    FORTIFICATIONS = "fortifications"
    CAMPS_BASES = "camps_bases"
    PROPS = "props"
    ARMOR = "armor"
    CLOTHING_UNIFORMS = "clothing_uniforms"

    # Nature
    ATMOSPHERE = "atmosphere"
    FLOWERS = "flowers"
    FOLIAGE_BUSH = "foliage_bush"
    FUNGI_MUSHROOMS = "fungi_mushrooms"
    LANDSCAPE = "landscape"
    PLANT = "plant"
    ROCK_STONE_FORMATION = "rock_stone_formation"
    TREE = "tree"
    WATER_FEATURES = "water_features"

    # Node Groups
    COMPOSITING_NODES = "compositing_nodes"
    GEOMETRY_NODES = "geometry_nodes"
    PROCEDURAL_GENERATORS = "procedural_generators"
    SHADING_NODES = "shading_nodes"
    SIMULATION_NODES = "simulation_nodes"
    UTILITY_NODES = "utility_nodes"

    # Research
    ASTRONOMY_ASTROPHYSICS = "astronomy_astrophysics"
    BIOLOGY_MOLECULAR = "biology_molecular"
    BIOMEDICAL_MEDICAL = "biomedical_medical"
    CHEMISTRY_MATERIALS = "chemistry_materials"
    DATA_VISUALIZATION = "data_visualization"
    EARTH_SCIENCES_GEOLOGY = "earth_sciences_geology"
    MACHINE_LEARNING_AI = "machine_learning_ai"
    NEUROSCIENCE = "neuroscience"
    SCIENTIFIC_ILLUSTRATION = "scientific_illustration"
    SYNTHETIC_DATASETS = "synthetic_datasets"

    # Scenes
    ABSTRACT_SCENES = "abstract_scenes"
    ANIMATION_SCENES = "animation_scenes"
    COMPLETE_PROJECTS = "complete_projects"
    ENVIRONMENT_SCENES = "environment_scenes"
    EXTERIOR_SCENES = "exterior_scenes"
    GAME_ENVIRONMENTS = "game_environments"
    INTERIOR_SCENES = "interior_scenes"
    PRODUCT_SHOTS = "product_shots"
    REALISTIC_SCENES = "realistic_scenes"
    STYLIZED_SCENES = "stylized_scenes"

    # Simulations & VFX
    ATMOSPHERIC_EFFECTS = "atmospheric_effects"
    CLOTH_SIMULATIONS = "cloth_simulations"
    DESTRUCTION_BREAKING = "destruction_breaking"
    EXPLOSIONS = "explosions"
    FIRE_SMOKE = "fire_smoke"
    FLUID_SIMULATIONS = "fluid_simulations"
    MAGIC_ENERGY_EFFECTS = "magic_energy_effects"
    PARTICLE_SYSTEMS = "particle_systems"
    PHYSICS_SIMULATIONS = "physics_simulations"
    WEATHER_EFFECTS = "weather_effects"

    # Space
    PLANET = "planet"
    SATELLITE = "satellite"
    SPACECRAFT = "spacecraft"
    STATION = "station"
    SPACE_SUIT_EQUIPMENT = "space_suit_equipment"

    # Sport & Hobby
    FISHING = "fishing"
    GYM = "gym"
    HOBBY_ACCESSORIES = "hobby_accessories"
    MUSIC = "music"
    SPORT = "sport"

    # Technology
    AUDIO_DEVICES = "audio_devices"
    CABLES_CONNECTORS = "cables_connectors"
    COMPUTER = "computer"
    DEVICE = "device"
    DRONE = "drone"
    GAMING_HARDWARE = "gaming_hardware"
    HOME_APPLIANCE = "home_appliance"
    PHOTOGRAPHY = "photography"
    ROBOTICS = "robotics"
    SMART_HOME_DEVICES = "smart_home_devices"
    VIDEO_DEVICES = "video_devices"

    # Template Setups
    ARCHVIZ_TEMPLATES = "archviz_templates"
    CAMERA_RIGS = "camera_rigs"
    COMPOSITING_TEMPLATES = "compositing_templates"
    LIGHTING_SETUPS = "lighting_setups"
    PRODUCT_VISUALIZATION = "product_visualization"
    RENDER_SETUPS = "render_setups"
    SCENE_TEMPLATES = "scene_templates"
    SHADER_TEMPLATES = "shader_templates"
    STUDIO_SETUPS = "studio_setups"
    WORKFLOW_TEMPLATES = "workflow_templates"

    # Transport
    AGRICULTURAL_VEHICLE = "agricultural_vehicle"
    BICYCLE = "bicycle"
    CAR = "car"
    CONSTRUCTION_VEHICLE = "construction_vehicle"
    EMERGENCY = "emergency"
    HEAVY_VEHICLE = "heavy_vehicle"
    MOTOCYCLE = "motocycle"
    PUBLIC_TRANSPORT = "public_transport"
    RAILED_VEHICLE = "railed_vehicle"
    SMALL_ELECTRIC_VEHICLES = "small_electric_vehicles"
    TRAILER_CARAVAN = "trailer_caravan"
    VEHICLE_PARTS = "vehicle_parts"


class Style(str, Enum):
    """Visual style of assets."""

    REALISTIC = "realistic"
    STYLIZED = "stylized"
    CARTOON = "cartoon"
    ANIME = "anime"
    PAINTERLY = "painterly"
    LINE_ART = "line_art"
    CLAY = "clay"
    CEL_SHADING = "cel_shading"
    ABSTRACT = "abstract"
    PIXELATED = "pixelated"
    OTHER = "other"


class RenderEngine(str, Enum):
    """Blender render engines."""

    CYCLES = "cycles"
    EEVEE = "eevee"
    WORKBENCH = "workbench"
    RENDERMAN = "renderman"
    VRAY = "vray"
    OCTANE = "octane"
    ARNOLD = "arnold"
    LUXCORE = "luxcore"


class MaterialType(str, Enum):
    """Material types."""

    PROCEDURAL = "procedural"
    TEXTURE_BASED = "texture_based"
    BOTH = "both"
    NA = "na"


class UVMapping(str, Enum):
    """UV mapping types."""

    NO_UV = "no_uv"
    OVERLAPPING = "overlapping"
    NON_OVERLAPPING = "non_overlapping"
    MIXED = "mixed"


class Feature(str, Enum):
    """Asset features."""

    PRINTABLE_3D = "3d_printable"
    ANIMATED = "animated"
    RIGGED = "rigged"
    SCANNED_3D = "3d_scanned"
    LOW_POLY = "low_poly"
    HIGH_POLY = "high_poly"
    GAME_READY = "game_ready"
    SCULPTING = "sculpting"
    GREASE_PENCIL = "grease_pencil"
    SYNTHETIC_DATA = "synthetic_data"


class Simulation(str, Enum):
    """Physics simulation types."""

    FLUID = "fluid"
    SMOKE = "smoke"
    CLOTH = "cloth"
    SOFT_BODY = "soft_body"
    RIGID_BODY = "rigid_body"
    HAIR = "hair"


class NodeGroupType(str, Enum):
    """Node group types."""

    SHADING_NODES = "shading_nodes"
    GEOMETRY_NODES = "geometry_nodes"
    COMPOSITING_NODES = "compositing_nodes"


class Physics(str, Enum):
    """Physics features."""

    FORCE_FIELDS = "force_fields"
    RIGID_BODY_CONSTRAINTS = "rigid_body_constraints"
    COLLISION_OBJECTS = "collision_objects"


class GameEngine(str, Enum):
    """Game engine compatibility."""

    GODOT = "godot"
    UNITY = "unity"
    UNREAL_ENGINE = "unreal_engine"


class LicenseType(str, Enum):
    """Asset license types."""

    CC0 = "cc0"
    CC_BY = "cc_by"
    CC_BY_SA = "cc_by_sa"
    CC_BY_NC = "cc_by_nc"
    CC_BY_NC_SA = "cc_by_nc_sa"
    CUSTOM = "custom"
    ALL_RIGHTS_RESERVED = "all_rights_reserved"


class LegalFlag(str, Enum):
    """Legal flags for assets."""

    FAN_ART = "fan_art"
    CONTAINS_NSFW = "contains_nsfw"
    TRADEMARKS = "trademarks"
    NO_AI_LICENSE = "no_ai_license"
    AI_GENERATED = "ai_generated"


class SortBy(str, Enum):
    """Sort fields for search results."""

    RELEVANCE = "relevance"
    NEWEST = "newest"
    OLDEST = "oldest"
    POPULAR = "popular"
    DOWNLOADS = "downloads"
    LIKES = "likes"
    VIEWS = "views"
    BOOKMARKS = "bookmarks"


class SortOrder(str, Enum):
    """Sort order for search results."""

    ASC = "asc"
    DESC = "desc"


# Category to Subcategory mapping
CATEGORY_SUBCATEGORIES: Dict[Category, List[Subcategory]] = {
    Category.ACCESSORIES: [
        Subcategory.BAGS_CARRIERS,
        Subcategory.BELTS_STRAPS,
        Subcategory.EYEWEAR,
        Subcategory.FASHION_ACCESSORIES,
        Subcategory.FOOTWEAR,
        Subcategory.GLOVES_HAND_ACCESSORIES,
        Subcategory.HAIR_ACCESSORIES,
        Subcategory.HEADWEAR,
        Subcategory.JEWELRY,
        Subcategory.OTHER,
        Subcategory.SCARVES_NECKWEAR,
        Subcategory.TECH_ACCESSORIES,
    ],
    Category.ANIMATION_RIGS: [
        Subcategory.ANIMAL_RIGS,
        Subcategory.ANIMATION_PRESETS,
        Subcategory.CHARACTER_RIGS,
        Subcategory.CONTROLLERS_UI,
        Subcategory.CREATURE_RIGS,
        Subcategory.FACIAL_RIGS,
        Subcategory.HAND_RIGS,
        Subcategory.IK_FK_SYSTEMS,
        Subcategory.MECHANICAL_RIGS,
        Subcategory.MOTION_CAPTURE,
        Subcategory.TAIL_RIGS,
        Subcategory.VEHICLE_RIGS,
        Subcategory.WING_RIGS,
    ],
    Category.ARCHITECTURE: [
        Subcategory.BALCONY_TERRACE,
        Subcategory.BUILDING,
        Subcategory.DOOR,
        Subcategory.EXTERIOR_ELEMENT,
        Subcategory.FENCE_RAILING,
        Subcategory.FLOOR_COVERING,
        Subcategory.FOUNDATION_STRUCTURAL_BASE,
        Subcategory.MOLDING_CARVING,
        Subcategory.ROOF_ROOFING_ELEMENTS,
        Subcategory.STAIRS,
        Subcategory.STRUCTURE,
        Subcategory.WALL_PANEL,
        Subcategory.WINDOW,
    ],
    Category.BRUSHES: [
        Subcategory.ANIMAL_CREATURE,
        Subcategory.ART,
        Subcategory.CLOTHING,
        Subcategory.DAMAGE,
        Subcategory.FABRIC_TEXTILE,
        Subcategory.GEOMETRIC,
        Subcategory.HAIR_FUR,
        Subcategory.HUMAN,
        Subcategory.INDUSTRIAL,
        Subcategory.NATURE,
        Subcategory.SCI_FI_TECH,
    ],
    Category.CHARACTER: [
        Subcategory.ANATOMY,
        Subcategory.ANIMAL,
        Subcategory.WOMAN_CLOTHING,
        Subcategory.MAN_CLOTHING,
        Subcategory.FANTASY_RACES,
        Subcategory.HAIR_HAIRSTYLES,
        Subcategory.HUMANOIDS,
        Subcategory.MONSTER_CREATURE,
        Subcategory.ROBOT,
    ],
    Category.DECALS: [
        Subcategory.BLOOD,
        Subcategory.BULLET_HOLES,
        Subcategory.BURN_MARKS,
        Subcategory.CRACKS_DAMAGE,
        Subcategory.DEBRIS,
        Subcategory.DECORATION,
        Subcategory.DIRT_GRIME,
        Subcategory.FLOOR_MARKINGS,
        Subcategory.FOLIAGE,
        Subcategory.FOODS,
        Subcategory.GRAFFITI,
        Subcategory.IMPERFECTIONS,
        Subcategory.ORGANIC_PATTERNS,
        Subcategory.PAINT_CHIPPING,
        Subcategory.RUST_CORROSION,
        Subcategory.SCRATCHES_SCUFFS,
        Subcategory.SIGNAGE,
        Subcategory.STAINS_SPILLS,
        Subcategory.SYMBOLS_ICONS,
        Subcategory.TEXT_NUMBERS,
        Subcategory.VEHICLE_MARKINGS,
        Subcategory.WATER_MOISTURE,
        Subcategory.WEAR_TEAR,
    ],
    Category.DECORATION: [
        Subcategory.BED_SHEET,
        Subcategory.BLANKET,
        Subcategory.BOOK,
        Subcategory.CANDLES_CANDLE_HOLDERS,
        Subcategory.CARPETS,
        Subcategory.CLOCK_WATCH,
        Subcategory.CURTAIN,
        Subcategory.DECORATION_SET,
        Subcategory.FABRICS,
        Subcategory.FIREPLACE,
        Subcategory.FOOD_DRINKS,
        Subcategory.HOLIDAY_DECORATION,
        Subcategory.MIRROR,
        Subcategory.MONEY,
        Subcategory.MUSICAL_INSTRUMENTS,
        Subcategory.PICTURE,
        Subcategory.PILLOW,
        Subcategory.SCULPTURE,
        Subcategory.TEXTILE,
        Subcategory.TOYS_GAMES,
        Subcategory.TROPHY_AWARD,
        Subcategory.VASE,
    ],
    Category.EDUCATIONAL: [
        Subcategory.BEGINNER_PROJECTS,
        Subcategory.CHALLENGE_PROJECTS,
        Subcategory.COURSE_MATERIALS,
        Subcategory.DOCUMENTATION,
        Subcategory.LEARNING_KITS,
        Subcategory.PRACTICE_SCENES,
        Subcategory.STUDY_REFERENCES,
        Subcategory.TECHNIQUE_DEMONSTRATIONS,
        Subcategory.TUTORIAL_FILES,
        Subcategory.WORKFLOW_EXAMPLES,
    ],
    Category.HDRIS: [
        Subcategory.ABSTRACT,
        Subcategory.ARCHITECTURAL,
        Subcategory.CITYSCAPES,
        Subcategory.FUTURISTIC_ENVIRONMENTS,
        Subcategory.HOLIDAY,
        Subcategory.INTERIORS,
        Subcategory.LANDSCAPES,
        Subcategory.NIGHTTIME_ENVIRONMENTS,
        Subcategory.PUBLIC,
        Subcategory.RESIDENTIAL,
        Subcategory.RURAL,
        Subcategory.SPORTS,
        Subcategory.STUDIO,
        Subcategory.URBAN,
        Subcategory.WATER_ENVIRONMENTS,
    ],
    Category.INDUSTRIAL: [
        Subcategory.CONTAINER,
        Subcategory.EQUIPMENT,
        Subcategory.MACHINERY,
        Subcategory.PARTS,
        Subcategory.SIGN,
        Subcategory.TOOLS,
    ],
    Category.INTERIOR: [
        Subcategory.ARMCHAIR,
        Subcategory.BATHROOM_FURNITURE,
        Subcategory.BED,
        Subcategory.CABINETS,
        Subcategory.CHAIR,
        Subcategory.CONSOLE,
        Subcategory.DRESSING_TABLE,
        Subcategory.ENTERTAINMENT_CENTER,
        Subcategory.HOME_ACCESSORIES,
        Subcategory.KIDS_FURNITURE,
        Subcategory.KITCHEN_FURNITURE,
        Subcategory.LIGHTS,
        Subcategory.OFFICE_FURNITURE,
        Subcategory.OUTDOOR_FURNITURE,
        Subcategory.POUF,
        Subcategory.RESTAURANT_BAR,
        Subcategory.ROOM_DIVIDER_SCREEN,
        Subcategory.SEATING_SET,
        Subcategory.SHELVING_BOOKCASE,
        Subcategory.SHOPPING_RETAIL,
        Subcategory.SIDEBOARD_DRAWERS_CHEST,
        Subcategory.SOFA,
        Subcategory.TABLE,
        Subcategory.WARDROBE,
    ],
    Category.LIGHTING: [
        Subcategory.CINEMATIC_LIGHTING,
        Subcategory.IES_PROFILES,
        Subcategory.LIGHT_RIGS,
        Subcategory.NATURAL_LIGHTING,
        Subcategory.NEON_GLOWING,
        Subcategory.NIGHT_LIGHTING,
        Subcategory.OUTDOOR_LIGHTING,
        Subcategory.PRODUCT_LIGHTING,
        Subcategory.STUDIO_LIGHTING,
        Subcategory.VOLUMETRIC_LIGHTING,
    ],
    Category.MATERIALS: [
        Subcategory.ASPHALT,
        Subcategory.BRICKS,
        Subcategory.CARBON_FIBER,
        Subcategory.CERAMIC,
        Subcategory.CONCRETE,
        Subcategory.DIRT,
        Subcategory.FABRIC,
        Subcategory.FLOOR,
        Subcategory.FOAM,
        Subcategory.FOOD,
        Subcategory.GLASS,
        Subcategory.GRASS,
        Subcategory.GROUND,
        Subcategory.ICE,
        Subcategory.LEATHER,
        Subcategory.LIQUID,
        Subcategory.MARBLE,
        Subcategory.METAL,
        Subcategory.ORGANIC,
        Subcategory.ORNAMENTS,
        Subcategory.PAINT,
        Subcategory.PAPER,
        Subcategory.PAVING,
        Subcategory.PLASTER,
        Subcategory.PLASTIC,
        Subcategory.ROCK,
        Subcategory.ROOFING,
        Subcategory.RUBBER,
        Subcategory.RUST,
        Subcategory.SAND,
        Subcategory.SOIL,
        Subcategory.STONE,
        Subcategory.TECH,
        Subcategory.TERRAZZO,
        Subcategory.TILES,
        Subcategory.WAX,
        Subcategory.WOOD,
    ],
    Category.MILITARY: [
        Subcategory.AIRCRAFT,
        Subcategory.VEHICLES,
        Subcategory.WATERCRAFT,
        Subcategory.WEAPONS,
        Subcategory.EQUIPMENT_GEAR,
        Subcategory.ACCESSORIES_MILITARY,
        Subcategory.FORTIFICATIONS,
        Subcategory.CAMPS_BASES,
        Subcategory.PROPS,
        Subcategory.ARMOR,
        Subcategory.CLOTHING_UNIFORMS,
    ],
    Category.NATURE: [
        Subcategory.ATMOSPHERE,
        Subcategory.FLOWERS,
        Subcategory.FOLIAGE_BUSH,
        Subcategory.FUNGI_MUSHROOMS,
        Subcategory.LANDSCAPE,
        Subcategory.PLANT,
        Subcategory.ROCK_STONE_FORMATION,
        Subcategory.TREE,
        Subcategory.WATER_FEATURES,
    ],
    Category.NODE_GROUP: [
        Subcategory.COMPOSITING_NODES,
        Subcategory.GEOMETRY_NODES,
        Subcategory.PROCEDURAL_GENERATORS,
        Subcategory.SHADING_NODES,
        Subcategory.SIMULATION_NODES,
        Subcategory.UTILITY_NODES,
    ],
    Category.RESEARCH: [
        Subcategory.ASTRONOMY_ASTROPHYSICS,
        Subcategory.BIOLOGY_MOLECULAR,
        Subcategory.BIOMEDICAL_MEDICAL,
        Subcategory.CHEMISTRY_MATERIALS,
        Subcategory.DATA_VISUALIZATION,
        Subcategory.EARTH_SCIENCES_GEOLOGY,
        Subcategory.MACHINE_LEARNING_AI,
        Subcategory.NEUROSCIENCE,
        Subcategory.SCIENTIFIC_ILLUSTRATION,
        Subcategory.SYNTHETIC_DATASETS,
    ],
    Category.SCENES: [
        Subcategory.ABSTRACT_SCENES,
        Subcategory.ANIMATION_SCENES,
        Subcategory.COMPLETE_PROJECTS,
        Subcategory.ENVIRONMENT_SCENES,
        Subcategory.EXTERIOR_SCENES,
        Subcategory.GAME_ENVIRONMENTS,
        Subcategory.INTERIOR_SCENES,
        Subcategory.PRODUCT_SHOTS,
        Subcategory.REALISTIC_SCENES,
        Subcategory.STYLIZED_SCENES,
    ],
    Category.SIMULATIONS_VFX: [
        Subcategory.ATMOSPHERIC_EFFECTS,
        Subcategory.CLOTH_SIMULATIONS,
        Subcategory.DESTRUCTION_BREAKING,
        Subcategory.EXPLOSIONS,
        Subcategory.FIRE_SMOKE,
        Subcategory.FLUID_SIMULATIONS,
        Subcategory.MAGIC_ENERGY_EFFECTS,
        Subcategory.PARTICLE_SYSTEMS,
        Subcategory.PHYSICS_SIMULATIONS,
        Subcategory.WEATHER_EFFECTS,
    ],
    Category.SPACE: [
        Subcategory.PLANET,
        Subcategory.SATELLITE,
        Subcategory.SPACECRAFT,
        Subcategory.STATION,
        Subcategory.SPACE_SUIT_EQUIPMENT,
    ],
    Category.SPORT_HOBBY: [
        Subcategory.FISHING,
        Subcategory.GYM,
        Subcategory.HOBBY_ACCESSORIES,
        Subcategory.MUSIC,
        Subcategory.SPORT,
    ],
    Category.TECHNOLOGY: [
        Subcategory.AUDIO_DEVICES,
        Subcategory.CABLES_CONNECTORS,
        Subcategory.COMPUTER,
        Subcategory.DEVICE,
        Subcategory.DRONE,
        Subcategory.GAMING_HARDWARE,
        Subcategory.HOME_APPLIANCE,
        Subcategory.PHOTOGRAPHY,
        Subcategory.ROBOTICS,
        Subcategory.SMART_HOME_DEVICES,
        Subcategory.VIDEO_DEVICES,
    ],
    Category.TEMPLATE_SETUPS: [
        Subcategory.ARCHVIZ_TEMPLATES,
        Subcategory.CAMERA_RIGS,
        Subcategory.COMPOSITING_TEMPLATES,
        Subcategory.LIGHTING_SETUPS,
        Subcategory.PRODUCT_VISUALIZATION,
        Subcategory.RENDER_SETUPS,
        Subcategory.SCENE_TEMPLATES,
        Subcategory.SHADER_TEMPLATES,
        Subcategory.STUDIO_SETUPS,
        Subcategory.WORKFLOW_TEMPLATES,
    ],
    Category.TRANSPORT: [
        Subcategory.AGRICULTURAL_VEHICLE,
        Subcategory.BICYCLE,
        Subcategory.CAR,
        Subcategory.CONSTRUCTION_VEHICLE,
        Subcategory.EMERGENCY,
        Subcategory.HEAVY_VEHICLE,
        Subcategory.MOTOCYCLE,
        Subcategory.PUBLIC_TRANSPORT,
        Subcategory.RAILED_VEHICLE,
        Subcategory.SMALL_ELECTRIC_VEHICLES,
        Subcategory.TRAILER_CARAVAN,
        Subcategory.VEHICLE_PARTS,
    ],
}


# Helper functions for type conversions
def join_enum_values(values: List[Enum]) -> str:
    """Join multiple enum values with + separator."""
    return "+".join(v.value for v in values)


def parse_tags(tags: List[str]) -> str:
    """Parse list of tags into API format."""
    return "+".join(tags)


def get_subcategories(category: Category) -> List[Subcategory]:
    """Get all subcategories for a given category.

    Args:
        category: The category to get subcategories for

    Returns:
        List of Subcategory enums for the given category.
        Returns empty list if category has no subcategories.

    Example:
        >>> from blendflare import Category, get_subcategories
        >>>
        >>> # Get all architecture subcategories
        >>> arch_subs = get_subcategories(Category.ARCHITECTURE)
        >>> for sub in arch_subs:
        ...     print(sub.value)
        balcony_terrace
        building
        door
        ...

        >>> # Use in UI to populate dropdown
        >>> category = Category.TRANSPORT
        >>> available_subcategories = get_subcategories(category)
        >>> # Now you can create a dynamic dropdown in your Blender addon
    """
    return CATEGORY_SUBCATEGORIES.get(category, [])


def get_subcategory_names(category: Category) -> List[str]:
    """Get all subcategory names (string values) for a given category.

    Args:
        category: The category to get subcategory names for

    Returns:
        List of subcategory string values for the given category.
        Returns empty list if category has no subcategories.

    Example:
        >>> from blendflare import Category, get_subcategory_names
        >>>
        >>> # Get subcategory names for HDRIS
        >>> hdri_subs = get_subcategory_names(Category.HDRIS)
        >>> print(hdri_subs)
        ['abstract', 'architectural', 'cityscapes', ...]

        >>> # Useful for creating EnumProperty items in Blender
        >>> items = [(s, s.replace('_', ' ').title(), '') for s in get_subcategory_names(Category.TRANSPORT)]
    """
    return [sub.value for sub in get_subcategories(category)]