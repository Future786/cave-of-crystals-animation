#!/usr/bin/env python3
"""
Master Configuration for 10 Viral Scientific Documentary Animations
Each video is calibrated for 60–75 seconds duration, 1080x1920 (9:16 vertical),
complete synchronized subtitles, procedural animations, and high-retention visual hooks.
"""

TOPICS = [
    # -------------------------------------------------------------
    # Topic 1: The Mariana Trench (Challenger Deep)
    # -------------------------------------------------------------
    {
        "id": "01_mariana_trench",
        "title": "The Mariana Trench: Challenger Deep",
        "tag": "PACIFIC OCEAN • 10,994M",
        "preset": "abyss",
        "tokens": {
            "top": "#0c2c3d",
            "bottom": "#03060a",
            "hl": "#00f2fe",
            "pill": "#0a1822"
        },
        "sentences": [
            {
                "text": "Eleven kilometers beneath the surface of the Pacific Ocean lies Challenger Deep, the deepest known chasm on Earth.",
                "caption_text": "11 kilometers beneath the Pacific,\nlies *Challenger Deep*, Earth's deepest chasm.",
                "shot": 0
            },
            {
                "text": "In nineteen sixty, two explorers descended for five hours inside the bathyscaphe Trieste, entering the midnight Hadal zone.",
                "caption_text": "In 1960, the *bathyscaphe Trieste*\ndescended 5 hours into the midnight Hadal zone.",
                "shot": 1
            },
            {
                "text": "If Mount Everest were placed at the trench floor, its highest peak would still be buried under more than two kilometers of water.",
                "caption_text": "If *Mount Everest* sat at the floor,\nits peak would be buried under 2,000m of water.",
                "shot": 2
            },
            {
                "text": "At this extreme depth, the hydrostatic water pressure exceeds one thousand and eighty atmospheres.",
                "caption_text": "At this extreme depth, water pressure\nexceeds *1,080 atmospheres*.",
                "shot": 3
            },
            {
                "text": "That is equivalent to eight metric tons of crushing force pressing down on every single square inch of surface.",
                "caption_text": "That equals *8 metric tons of force*\ncrushing down on every square inch.",
                "shot": 3
            },
            {
                "text": "Submarines require thick forged steel spheres just to keep from being instantly pulverized into scrap.",
                "caption_text": "Submersibles require thick forged titanium spheres\nto avoid being *instantly pulverized*.",
                "shot": 4
            },
            {
                "text": "Yet inside this pitch black freezing void, extraordinary biological life thrives in abundance.",
                "caption_text": "Yet inside this crushing black void,\n*extraordinary life thrives in abundance*.",
                "shot": 5
            },
            {
                "text": "The Mariana snailfish survives without scales or solid bones, using flexible cartilage and trimethylamine oxide cellular armor.",
                "caption_text": "The *Mariana Snailfish* survives with\nno bones, using flexible cellular armor.",
                "shot": 6
            },
            {
                "text": "Giant single celled xenophyophores grow to twenty centimeters wide, filter feeding on organic marine snow.",
                "caption_text": "Giant single-celled *xenophyophores*\ngrow to 20 cm wide in freezing silence.",
                "shot": 7
            },
            {
                "text": "Here, at the absolute edge of planetary physics, life did not surrender to the abyss. It conquered it.",
                "caption_text": "At the edge of planetary physics,\n*life conquered the abyss*.",
                "shot": 8
            }
        ]
    },

    # -------------------------------------------------------------
    # Topic 2: The Kola Superdeep Borehole
    # -------------------------------------------------------------
    {
        "id": "02_kola_borehole",
        "title": "The Kola Superdeep Borehole",
        "tag": "MURMANSK, ARCTIC • 12,262M",
        "preset": "magma",
        "tokens": {
            "top": "#24160f",
            "bottom": "#0d0704",
            "hl": "#ff9f1c",
            "pill": "#1c120c"
        },
        "sentences": [
            {
                "text": "In the frozen Arctic tundra of the Kola Peninsula, Soviet engineers spent twenty-four years drilling the deepest artificial hole on Earth.",
                "caption_text": "In the frozen Arctic tundra, engineers spent\n24 years drilling the *deepest hole on Earth*.",
                "shot": 0
            },
            {
                "text": "Reaching twelve thousand two hundred and sixty-two meters down, the drill penetrated more than seven miles into the continental crust.",
                "caption_text": "Reaching *12,262 meters down*,\nthe drill went 7 miles into Earth's crust.",
                "shot": 1
            },
            {
                "text": "At seven kilometers down, geologists expected dense dry granite, but instead found fractured rock saturated with boiling water.",
                "caption_text": "At 7 kilometers down, they found fractured rock\nsaturated with *boiling hydrothermal water*.",
                "shot": 2
            },
            {
                "text": "Trapped hydrogen gas boiled out of the mud in quantities that stunned the Soviet science academy.",
                "caption_text": "Trapped *hydrogen gas boiled out*\nin quantities that stunned geologists.",
                "shot": 2
            },
            {
                "text": "Even more astonishing, they discovered microscopic plankton fossils six kilometers deep, perfectly preserved in two billion year old rock.",
                "caption_text": "They found *microscopic plankton fossils*\npreserved in 2-billion-year-old rock.",
                "shot": 3
            },
            {
                "text": "By twelve kilometers, subterranean temperatures soared to one hundred and eighty degrees Celsius, turning rock into ductile plastic.",
                "caption_text": "Temperatures soared to *180°C*,\nturning ancient granite into soft plastic.",
                "shot": 4
            },
            {
                "text": "The rock behaved like putty, flowing back into the drill shaft and destroying cutting heads within minutes.",
                "caption_text": "The softened rock flowed like putty,\n*destroying drill bits within minutes*.",
                "shot": 5
            },
            {
                "text": "Sensational rumors claimed microphones recorded screaming souls, but the real telemetry revealed acoustic pressure waves of shifting tectonic stress.",
                "caption_text": "Urban legends claimed 'screaming souls',\nbut sensors recorded *tectonic acoustic stress*.",
                "shot": 6
            },
            {
                "text": "Today, that nine-inch portal into the underworld sits welded shut beneath a rusty steel cap, an abandoned gateway to the abyss.",
                "caption_text": "Today, that nine-inch portal sits\n*welded shut beneath a rusty steel cap*.",
                "shot": 7
            }
        ]
    },

    # -------------------------------------------------------------
    # Topic 3: The Bloop (Ocean Acoustic Anomaly)
    # -------------------------------------------------------------
    {
        "id": "03_the_bloop",
        "title": "The Bloop: Deep Ocean Acoustic Anomaly",
        "tag": "SOUTH PACIFIC • 50°S 100°W",
        "preset": "sonar",
        "tokens": {
            "top": "#03170e",
            "bottom": "#010804",
            "hl": "#00ff66",
            "pill": "#051f14"
        },
        "sentences": [
            {
                "text": "In the summer of nineteen ninety-seven, an underwater listening network picked up an anomaly that stunned marine acousticians.",
                "caption_text": "In the summer of 1997, hydrophones\npicked up *an unprecedented deep ocean anomaly*.",
                "shot": 0
            },
            {
                "text": "The US Navy had installed the SOSUS hydrophone array to track Soviet submarines through the deep sound channel.",
                "caption_text": "The Navy had installed the *SOSUS array*\nto track submarines through deep ocean channels.",
                "shot": 1
            },
            {
                "text": "Deep in the remote South Pacific, a thunderous ultra-low frequency sound echoed across more than five thousand kilometers of open water.",
                "caption_text": "Deep in the South Pacific, an ultra-low sound\nechoed across *5,000 kilometers* of water.",
                "shot": 2
            },
            {
                "text": "Named The Bloop, the signal rose rapidly in frequency over four and a half minutes and was detected by multiple listening stations.",
                "caption_text": "Named *The Bloop*, the signal rose for\n4.5 minutes across multiple stations.",
                "shot": 3
            },
            {
                "text": "Its acoustic profile closely resembled an organic biological vocalization, but it was several times louder than the largest blue whale.",
                "caption_text": "The acoustic profile looked biological,\nyet *several times louder than a Blue Whale*.",
                "shot": 4
            },
            {
                "text": "Biologists calculated that if an animal produced the sound, it would have to measure well over two hundred feet in length.",
                "caption_text": "If produced by a creature, it would have to\n*measure over 200 feet in length*.",
                "shot": 5
            },
            {
                "text": "Finally, in two thousand twelve, NOAA scientists identified the true culprit: an immense icequake caused by massive Antarctic icebergs cracking and calving.",
                "caption_text": "In 2012, NOAA cracked the case:\nan *immense Antarctic icequake* cracking glaciers.",
                "shot": 6
            },
            {
                "text": "The shearing of giant ice sheets generated acoustic shockwaves loud enough to shake the entire southern hemisphere.",
                "caption_text": "Shearing ice sheets generated shockwaves\n*loud enough to shake an ocean hemisphere*.",
                "shot": 6
            },
            {
                "text": "Yet eighty percent of our oceans remain unmapped and unmonitored. What else is singing in the dark?",
                "caption_text": "Yet 80% of our oceans remain unmapped.\n*What else is singing in the dark?*",
                "shot": 7
            }
        ]
    },

    # -------------------------------------------------------------
    # Topic 4: Lake Vostok (The Subglacial Time Capsule)
    # -------------------------------------------------------------
    {
        "id": "04_lake_vostok",
        "title": "Lake Vostok: Antarctica's Subglacial Time Capsule",
        "tag": "EAST ANTARCTICA • -89°C",
        "preset": "glacial",
        "tokens": {
            "top": "#0a2336",
            "bottom": "#030d15",
            "hl": "#00e5ff",
            "pill": "#082133"
        },
        "sentences": [
            {
                "text": "Four thousand meters beneath the East Antarctic ice sheet lies Lake Vostok, a subglacial liquid ocean sealed off from Earth for fifteen million years.",
                "caption_text": "4,000 meters beneath Antarctic ice lies\n*Lake Vostok*, sealed for 15 million years.",
                "shot": 0
            },
            {
                "text": "Covering fifteen thousand square kilometers, it is nearly the size of Lake Ontario, buried under four kilometers of crushing glacial ice.",
                "caption_text": "The lake is the size of *Lake Ontario*,\nburied under 4 km of solid glacial ice.",
                "shot": 1
            },
            {
                "text": "Despite sitting beneath the coldest surface on Earth at minus eighty-nine degrees, geothermal heat keeps its freshwater reservoir in a liquid state.",
                "caption_text": "Despite -89°C surface air, geothermal heat\nkeeps the freshwater lake in a *liquid state*.",
                "shot": 2
            },
            {
                "text": "The pressure here exceeds three hundred and fifty atmospheres, and the water is supersaturated with fifty times more oxygen than normal lakes.",
                "caption_text": "Pressure exceeds *350 atmospheres*,\nwith 50 times more oxygen than normal water.",
                "shot": 3
            },
            {
                "text": "For decades, Russian drillers bored through thousands of meters of ice cores, taking extreme precautions to avoid contaminating the virgin waters.",
                "caption_text": "Scientists drilled thousands of meters,\ntaking extreme care *not to contaminate the waters*.",
                "shot": 4
            },
            {
                "text": "They used a specialized freon and kerosene fluid column to balance the immense hydrostatic pressure of the overlying ice.",
                "caption_text": "A specialized fluid column balanced the\n*immense hydrostatic pressure* of the ice.",
                "shot": 4
            },
            {
                "text": "When the core reached accreted lake ice, genetic analysis revealed thousands of novel DNA sequences from ancient bacteria and fungi.",
                "caption_text": "Core samples revealed thousands of\n*novel DNA sequences* from ancient microbes.",
                "shot": 5
            },
            {
                "text": "These organisms have thrived in complete total darkness, nourished only by minerals from geothermal bedrock vents.",
                "caption_text": "These organisms thrived in total darkness,\n*feeding only on mineral bedrock vents*.",
                "shot": 6
            },
            {
                "text": "Lake Vostok is our closest terrestrial model for Jupiter's ice moon Europa. If life can survive here, life is everywhere in the cosmos.",
                "caption_text": "Lake Vostok proves life can survive here;\n*and perhaps on Jupiter's moon Europa*.",
                "shot": 7
            }
        ]
    },

    # -------------------------------------------------------------
    # Topic 5: The Door to Hell (Darvaza Gas Crater)
    # -------------------------------------------------------------
    {
        "id": "05_darvaza_crater",
        "title": "The Door to Hell: Darvaza Gas Crater",
        "tag": "KARAKUM DESERT, TURKMENISTAN",
        "preset": "inferno",
        "tokens": {
            "top": "#2d0902",
            "bottom": "#0c0200",
            "hl": "#ff9100",
            "pill": "#260b05"
        },
        "sentences": [
            {
                "text": "In the heart of the Karakum Desert in Turkmenistan, a giant flaming crater burns like an open portal into the underworld.",
                "caption_text": "In the heart of the Karakum Desert,\na giant *flaming crater* burns day and night.",
                "shot": 0
            },
            {
                "text": "Known as the Door to Hell, this fiery pit measures seventy meters across and thirty meters deep, burning incessantly since nineteen seventy-one.",
                "caption_text": "Known as the *Door to Hell*,\nthis 70m pit has burned non-stop since 1971.",
                "shot": 1
            },
            {
                "text": "It began when a Soviet drilling rig accidentally punctured a subterranean natural gas cavern, causing the ground to violently collapse.",
                "caption_text": "A Soviet drilling rig punctured a gas cavern,\ncausing the ground to *violently collapse*.",
                "shot": 2
            },
            {
                "text": "The entire drilling rig and camp plunged into the crater, miraculously without loss of life, but exposing a massive methane blowout.",
                "caption_text": "The rig fell into the sinkhole,\n*unleashing an uncontrollable methane blowout*.",
                "shot": 2
            },
            {
                "text": "To prevent toxic methane gas from poisoning nearby villages, engineers ignited the crater, estimating it would burn out in a few weeks.",
                "caption_text": "To stop poisonous fumes, engineers lit the gas,\n*expecting it to burn out in weeks*.",
                "shot": 3
            },
            {
                "text": "Over fifty years later, roaring flames still erupt from hundreds of pressurized vents, fed by vast untapped underground gas reserves.",
                "caption_text": "Over 50 years later, roaring flames\nstill erupt from *hundreds of pressurized vents*.",
                "shot": 4
            },
            {
                "text": "Temperatures at the bottom reach over four hundred degrees Celsius, visible at night for miles across the pitch black desert dunes.",
                "caption_text": "Temperatures reach *over 400°C*,\nglowing like a beacon across the desert.",
                "shot": 4
            },
            {
                "text": "In two thousand thirteen, explorer George Kourounis rappelled to the bottom wearing a heat-reflective suit, collecting soil samples from the inferno.",
                "caption_text": "In 2013, an explorer rappelled to the floor,\n*collecting samples inside the 400°C inferno*.",
                "shot": 5
            },
            {
                "text": "Astonishingly, scientists discovered rich colonies of extremophile bacteria living happily inside the burning high-temperature soil.",
                "caption_text": "Scientists discovered *extremophile bacteria*\nliving happily inside the burning soil.",
                "shot": 6
            }
        ]
    },

    # -------------------------------------------------------------
    # Topic 6: Tardigrades (The Indestructible Extremophile)
    # -------------------------------------------------------------
    {
        "id": "06_tardigrades",
        "title": "Tardigrades: The Indestructible Extremophile",
        "tag": "MICRO-METAZOA • 0.5MM",
        "preset": "microscope",
        "tokens": {
            "top": "#0a1e14",
            "bottom": "#020905",
            "hl": "#76ff03",
            "pill": "#091f14"
        },
        "sentences": [
            {
                "text": "Measuring less than half a millimeter long, tardigrades, or water bears, are the most indestructible animals on planet Earth.",
                "caption_text": "Measuring half a millimeter long,\n*Tardigrades* are Earth's most indestructible animals.",
                "shot": 0
            },
            {
                "text": "These microscopic eight-legged metazoans have survived all five mass extinction events over the past six hundred million years.",
                "caption_text": "They survived *all five mass extinction events*\nover 600 million years of Earth history.",
                "shot": 1
            },
            {
                "text": "When environmental conditions turn hostile, they enter cryptobiosis, expelling ninety-nine percent of the water from their bodies.",
                "caption_text": "In deadly conditions, they enter *cryptobiosis*,\nexpelling 99% of their body water.",
                "shot": 2
            },
            {
                "text": "In this dehydrated tun state, their metabolism slows to less than zero point zero one percent of normal, virtually stopping biological time.",
                "caption_text": "In this 'tun' state, their metabolism slows,\n*virtually stopping biological time*.",
                "shot": 3
            },
            {
                "text": "Special disordered proteins transform their cellular interior into a protective biological glass, locking vital organs in stasis.",
                "caption_text": "Proteins turn their cellular interior into\n*protective biological glass* in stasis.",
                "shot": 4
            },
            {
                "text": "Tardigrades have survived temperatures of minus two hundred and seventy-two degrees Celsius, boiling water at one hundred and fifty degrees, and the vacuum of open space.",
                "caption_text": "They survive *-272°C absolute zero*,\n150°C boiling heat, and the vacuum of space.",
                "shot": 5
            },
            {
                "text": "They withstand one thousand times more ionizing radiation than a human, repairing their shattered DNA with unique suppressor proteins.",
                "caption_text": "They survive *1,000x human lethal radiation*,\nrapidly repairing their shattered DNA.",
                "shot": 6
            },
            {
                "text": "A unique protein called Dsup binds to their chromatin like a molecular armor shield, deflecting hydroxyl free radicals.",
                "caption_text": "A protein called *Dsup* wraps around their DNA\nlike a bulletproof armor shield.",
                "shot": 6
            },
            {
                "text": "Add a single drop of water after thirty years of frozen sleep, and the water bear rehydrates, stands up, and walks away unharmed.",
                "caption_text": "Add a single drop of water after 30 years,\n*and they rehydrate and walk away unharmed*.",
                "shot": 7
            }
        ]
    },

    # -------------------------------------------------------------
    # Topic 7: The Wow! Signal (The 72-Second Cosmic Enigma)
    # -------------------------------------------------------------
    {
        "id": "07_wow_signal",
        "title": "The Wow! Signal: The 72-Second Cosmic Enigma",
        "tag": "BIG EAR OBSERVATORY • 1420 MHZ",
        "preset": "cosmos",
        "tokens": {
            "top": "#05020c",
            "bottom": "#010004",
            "hl": "#ffd700",
            "pill": "#14092b"
        },
        "sentences": [
            {
                "text": "On August fifteenth, nineteen seventy-seven, Ohio State University's Big Ear radio telescope was scanning the constellation Sagittarius.",
                "caption_text": "On August 15, 1977, the *Big Ear telescope*\nwas scanning the constellation Sagittarius.",
                "shot": 0
            },
            {
                "text": "The telescope had no moving parts, relying on Earth's rotation to sweep across the sky, observing any point for exactly seventy-two seconds.",
                "caption_text": "Earth's rotation swept the sky, giving\n*exactly 72 seconds* to observe any point.",
                "shot": 1
            },
            {
                "text": "Suddenly, the receiver picked up an intensely powerful narrowband radio spike thirty times stronger than deep space background noise.",
                "caption_text": "Suddenly, it picked up a powerful radio spike\n*30 times stronger* than deep space noise.",
                "shot": 2
            },
            {
                "text": "When astronomer Jerry Ehman reviewed the computer printout, he spotted the alphanumerical intensity sequence 6-E-Q-U-J-5.",
                "caption_text": "Astronomer Jerry Ehman spotted the sequence\n*6-E-Q-U-J-5* on the computer printout.",
                "shot": 3
            },
            {
                "text": "Stunned by its perfect bell curve and strength, he grabbed a red pen, circled the characters, and wrote the word Wow in the margin.",
                "caption_text": "Stunned by its strength, he circled the code\nin red ink and wrote *'Wow!' in the margin*.",
                "shot": 4
            },
            {
                "text": "The signal was broadcast precisely at fourteen twenty megahertz, the protected hydrogen line universally considered the cosmic beacon frequency.",
                "caption_text": "It transmitted at *1420 MHz*,\nthe sacred interstellar hydrogen line frequency.",
                "shot": 5
            },
            {
                "text": "It showed all the hallmarks of an artificial transmission from beyond our solar system, with no Doppler shift typical of orbiting satellites.",
                "caption_text": "It showed all the hallmarks of an\n*artificial interstellar transmission*.",
                "shot": 6
            },
            {
                "text": "Despite hundreds of follow up sweeps across forty-seven years, the signal never repeated. The universe returned to complete silence.",
                "caption_text": "Across 47 years of sweeps, it never repeated.\n*The cosmos returned to complete silence*.",
                "shot": 7
            }
        ]
    },

    # -------------------------------------------------------------
    # Topic 8: Chernobyl's Elephant's Foot (The Lethal Corium)
    # -------------------------------------------------------------
    {
        "id": "08_chernobyl_foot",
        "title": "Chernobyl's Elephant's Foot: The Lethal Corium",
        "tag": "REACTOR 4 BASEMENT • 10,000 R/HR",
        "preset": "radiation",
        "tokens": {
            "top": "#171908",
            "bottom": "#060702",
            "hl": "#ffd600",
            "pill": "#171807"
        },
        "sentences": [
            {
                "text": "In December nineteen eighty-six, cleanup workers exploring the dark flooded corridors beneath Chernobyl's destroyed Reactor Four made a chilling discovery.",
                "caption_text": "In December 1986, workers beneath Chernobyl's\nReactor 4 made *a chilling discovery*.",
                "shot": 0
            },
            {
                "text": "Resting against a concrete wall was a two-meter wrinkled mass of lethal radioactive corium, forever known as the Elephant's Foot.",
                "caption_text": "Resting against a wall was a 2-meter mass\nof corium, known as *The Elephant's Foot*.",
                "shot": 1
            },
            {
                "text": "During the meltdown, uranium fuel rods melted at two thousand degrees, combining with molten sand, concrete, and zirconium into radioactive lava.",
                "caption_text": "Uranium fuel melted at *2,000°C*,\nfusing with sand and concrete into nuclear lava.",
                "shot": 2
            },
            {
                "text": "It burned through the reinforced reactor floor, dripping down steam pipes before solidifying into a deadly dark mass.",
                "caption_text": "It burned through reinforced concrete floors\nbefore solidifying into *a deadly mass*.",
                "shot": 2
            },
            {
                "text": "When first discovered, its radiation was estimated at ten thousand roentgens per hour.",
                "caption_text": "Its radiation measured *10,000 roentgens/hr*,\na lethally toxic level.",
                "shot": 3
            },
            {
                "text": "Standing near it for just three hundred seconds would deliver a lethal human dose, destroying internal organs within forty-eight hours.",
                "caption_text": "Standing near it for *300 seconds*\nwould guarantee fatal radiation sickness.",
                "shot": 3
            },
            {
                "text": "Early photographs were captured by wheeling remote robotic cameras, and the gamma rays were so intense they degraded the film with white static snow.",
                "caption_text": "Gamma rays were so intense they destroyed\nfilm cameras with *swirling white static snow*.",
                "shot": 4
            },
            {
                "text": "Scientists even fired armor piercing rifle rounds at the mass just to break off small rock fragments for laboratory chemical analysis.",
                "caption_text": "Scientists fired *armor-piercing rifle rounds*\nto chip off samples for laboratory tests.",
                "shot": 5
            },
            {
                "text": "Today, even inside this radioactive sarcophagus, black radiotrophic fungi grow on the walls, using melanin pigment to harvest gamma radiation for energy.",
                "caption_text": "Today, *black radiotrophic fungi* grow there,\nusing melanin to feed on gamma radiation.",
                "shot": 6
            }
        ]
    },

    # -------------------------------------------------------------
    # Topic 9: The Devil's Kettle (The Disappearing Waterfall)
    # -------------------------------------------------------------
    {
        "id": "09_devils_kettle",
        "title": "The Devil's Kettle: The Disappearing Waterfall",
        "tag": "BRULE RIVER, MINNESOTA",
        "preset": "canyon",
        "tokens": {
            "top": "#181410",
            "bottom": "#060503",
            "hl": "#00e5ff",
            "pill": "#141916"
        },
        "sentences": [
            {
                "text": "In the dense pine forests along Minnesota's North Shore, the Brule River approaches a dramatic volcanic cliff called the Devil's Kettle.",
                "caption_text": "In Minnesota's pine forests, the Brule River\napproaches *The Devil's Kettle* waterfall.",
                "shot": 0
            },
            {
                "text": "Just before plunging over a fifty-foot rhyolite ledge, a massive rock outcrop cleanly splits the entire river into two halves.",
                "caption_text": "Before plunging over a 50-foot ledge,\na rock outcrop *splits the river into two halves*.",
                "shot": 1
            },
            {
                "text": "The eastern half tumbles normally down the canyon walls toward Lake Superior, but the western half drops straight into a giant circular geological pothole.",
                "caption_text": "The eastern half flows normally,\nbut the western half drops into *a giant pothole*.",
                "shot": 2
            },
            {
                "text": "For generations, the water appeared to vanish into the Earth with no visible exit point anywhere in the surrounding river system.",
                "caption_text": "For generations, the water seemed to\n*vanish into Earth* with no exit point.",
                "shot": 3
            },
            {
                "text": "Local legends claimed the pothole was a bottomless abyss leading directly into subterranean caverns connected to the mantle.",
                "caption_text": "Legends claimed the pothole was an abyss\n*leading to bottomless caverns deep underground*.",
                "shot": 3
            },
            {
                "text": "Curious hikers and researchers dumped fluorescent green dyes, ping-pong balls, and radio telemetry tags into the kettle, but nothing ever emerged.",
                "caption_text": "Researchers dumped dyes and trackers in,\n*yet nothing ever emerged downstream*.",
                "shot": 4
            },
            {
                "text": "In two thousand seventeen, Minnesota hydrologists solved the mystery by measuring water volume with acoustic Doppler flow meters.",
                "caption_text": "In 2017, hydrologists measured water volume\nusing *acoustic Doppler flow meters*.",
                "shot": 5
            },
            {
                "text": "The water was not vanishing into the mantle: it drains into an underground channel and surges back up into the riverbed directly beneath the plunge pool.",
                "caption_text": "The water didn't vanish: it re-surfaces\n*directly under the plunge pool downstream*.",
                "shot": 6
            },
            {
                "text": "The items thrown in had simply been pulverized by the violent recirculating vortex currents at the bottom of the kettle.",
                "caption_text": "Objects thrown inside were simply pulverized\n*by the violent swirling vortex currents*.",
                "shot": 7
            }
        ]
    },

    # -------------------------------------------------------------
    # Topic 10: The Silurian Hypothesis (Deep Time Civilizations)
    # -------------------------------------------------------------
    {
        "id": "10_silurian_hypothesis",
        "title": "The Silurian Hypothesis: Deep Time Civilizations",
        "tag": "GEOLOGICAL TIME • 55,000,000 BC",
        "preset": "strata",
        "tokens": {
            "top": "#241911",
            "bottom": "#0c0704",
            "hl": "#ffab40",
            "pill": "#1c1510"
        },
        "sentences": [
            {
                "text": "If an advanced industrial civilization existed on Earth fifty million years before humans, could we prove they were ever here?",
                "caption_text": "If an industrial species lived 50 million years ago,\n*could we prove they were ever here?*",
                "shot": 0
            },
            {
                "text": "This is the Silurian Hypothesis, a scientific thought experiment published by NASA climatologist Gavin Schmidt and astrophysicist Adam Frank.",
                "caption_text": "This is the *Silurian Hypothesis*,\na scientific study by NASA and astrophysics teams.",
                "shot": 1
            },
            {
                "text": "Humans have existed for only three hundred thousand years, less than zero point zero one percent of Earth's four point five billion year history.",
                "caption_text": "Humans have existed for 300,000 years,\n*less than 0.01%* of Earth's vast history.",
                "shot": 2
            },
            {
                "text": "Fifty-six million years ago, the Paleocene-Eocene Thermal Maximum saw global temperatures spike by eight degrees in a geological heartbeat.",
                "caption_text": "56 million years ago, temperatures spiked\n*by 8 degrees* in a sudden geological heartbeat.",
                "shot": 3
            },
            {
                "text": "Fossilization is extraordinarily rare: less than a tiny fraction of one percent of all ancient species are ever preserved in rock.",
                "caption_text": "Fossilization is extraordinarily rare:\n*less than 0.1%* of species ever become stone.",
                "shot": 4
            },
            {
                "text": "In just a few millennia, our cities, steel skyscrapers, concrete highways, and dams will weather, crumble, and erode into dust.",
                "caption_text": "In just a few thousand years, our cities\n*will weather and crumble into dust*.",
                "shot": 5
            },
            {
                "text": "The only immortal traces left in the geological strata would be synthetic plastics, anomalous carbon isotope spikes, and long-lived radioactive plutonium isotopes.",
                "caption_text": "The only immortal traces would be\n*plastics, carbon spikes, and radioactive isotopes*.",
                "shot": 6
            },
            {
                "text": "All traces of modern human civilization will eventually be compressed into a microscopic sedimentary rock layer less than two millimeters thick.",
                "caption_text": "Our entire civilization will condense\n*into a rock layer less than 2 millimeters thick*.",
                "shot": 7
            },
            {
                "text": "Looking into the abyss of deep time, civilizations rise, burn, and dissolve like a whisper in the rock layers of Earth.",
                "caption_text": "In the abyss of deep time, civilizations rise\n*and dissolve like a whisper in the stone*.",
                "shot": 8
            }
        ]
    }
]
