

birdsys = {
    "ik": {
        "controls": [
            "foot_s_ik_control",
            "polevectorLeg_s_control"
        ],
        "sys": [
            "leg_01_s_ik_sys",
            "leg_02_s_ik_sys",
            "leg_03_s_ik_sys",
            "poleRef_s_sys"
        ],
        "ikh": [
            "leg_s_ikh_sys"
        ]
    },
    "fk": {
        "controls": [
            "foot_s_fk_control",
            "lowerleg_s_fk_control",
            "upperleg_s_fk_control"
        ],
        "sys": {
            "leg_01_s_fk_sys",
            "leg_02_s_fk_sys",
            "leg_03_s_fk_sys",
            "polevectorLeg_s_fk_ref"
        }
    },
    "def": [
        "leg_01_s_def",
        "leg_02_s_def",
        "ankle_01_s_def"
    ],
    "attr": {
        "leg_s_attributesShape": {
            "FKIK": {"type": "float", "min": 0.0, "max": 1.0}
        },
    },
    "connections": {

    }
}
