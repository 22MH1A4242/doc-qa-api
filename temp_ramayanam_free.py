"""
================================================================
  🏹 RAMAYANAM SHORTS CREATOR — 100% FREE
  No API key needed! No paid tools!

  INSTALL (one time only):
  pip install gtts pillow numpy opencv-python pydub

  RUN:
  python ramayanam_free.py
================================================================
"""

import os, sys, math, textwrap, time, re, subprocess
from pathlib import Path
import numpy as np

# ── check packages ─────────────────────────────────────────────
def check():
    missing = []
    for imp,pkg in [("PIL","pillow"),("cv2","opencv-python"),
                    ("gtts","gtts"),("numpy","numpy")]:
        try: __import__(imp)
        except ImportError: missing.append(pkg)
    if missing:
        print(f"\n❌  Run this first:\n\n   pip install {' '.join(missing)}\n")
        sys.exit(1)
check()

from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
import cv2

# ── output folders ─────────────────────────────────────────────
OUTDIR = Path("ramayanam_output")
TMPDIR = Path("ramayanam_tmp")
OUTDIR.mkdir(exist_ok=True)
TMPDIR.mkdir(exist_ok=True)

# ── video settings ─────────────────────────────────────────────
W, H = 1080, 1920
FPS  = 30

# ══════════════════════════════════════════════════════════════
#  ALL 150 VIDEOS — PRE-WRITTEN SCRIPTS (no API needed!)
#  Day 1 = index 0-4, Day 2 = index 5-9, etc.
# ══════════════════════════════════════════════════════════════
ALL_VIDEOS = [

  # ── DAY 1 — BALA KANDA ──────────────────────────────────────
  { "day":1,"num":1,"duration":1,"theme":"divine",
    "title_en":"Rama's Divine Birth — 3D Ayodhya",
    "title_te":"రాముని జన్మ — అయోధ్య 3D దృశ్యం",
    "hashtags":"#Ramayanam #RamaBirth #TeluguShorts #రామాయణం #Shorts #BalaKanda",
    "scenes":[
      {"dur":8, "theme":"divine","head":"త్రేతాయుగం","overlay1":"TRETA YUGA","overlay2":"AYODHYA CITY",
       "vo_te":"త్రేతాయుగంలో అయోధ్య నగరంలో ఒక దివ్యమైన క్షణం వచ్చింది",
       "vo_en":"In the Treta Yuga, a divine moment arrived in Ayodhya"},
      {"dur":12,"theme":"golden","head":"దశరథుని కోరిక","overlay1":"KING DASHARATHA","overlay2":"PRAYED FOR SONS",
       "vo_te":"దశరథ మహారాజు పుత్రుల కోసం యజ్ఞం చేశాడు. అగ్నిదేవుడు పాయసం తెచ్చాడు",
       "vo_en":"King Dasharatha performed a sacred yagna. Agni deva brought divine payasam"},
      {"dur":15,"theme":"divine","head":"దివ్య జన్మ","overlay1":"DIVINE BIRTH","overlay2":"CHAITRA NAVAMI",
       "vo_te":"చైత్ర నవమి రోజున కౌసల్యాదేవి గర్భం నుండి నీలమేఘ శ్యాముడు జన్మించాడు",
       "vo_en":"On Chaitra Navami, the dark-complexioned divine child was born from Kaushalya"},
      {"dur":15,"theme":"golden","head":"దేవతల వర్షం","overlay1":"FLOWERS FROM","overlay2":"THE HEAVENS",
       "vo_te":"దేవతలు ఆకాశం నుండి పూలు కురిపించారు. శంఖాలు మ్రోగాయి. లోకమంతా సంతోషపడింది",
       "vo_en":"Gods showered flowers from heavens. Conch shells echoed. The world rejoiced"},
      {"dur":10,"theme":"divine","head":"జై శ్రీరామ్","overlay1":"JAI SHRI RAM","overlay2":"SUBSCRIBE NOW",
       "vo_te":"విష్ణువు స్వయంగా రాముడిగా అవతరించాడు. జై శ్రీరామ్! సబ్స్క్రైబ్ చేయండి",
       "vo_en":"Vishnu himself descended as Rama. Jai Shri Ram! Please subscribe"},
    ]},

  { "day":1,"num":2,"duration":3,"theme":"battle",
    "title_en":"Why Did God Take Birth as Rama?",
    "title_te":"భగవంతుడు రాముడిగా ఎందుకు జన్మించాడు?",
    "hashtags":"#WhyRama #Ramayanam #Ravana #Vishnu #TeluguShorts #రామాయణం #Shorts",
    "scenes":[
      {"dur":15,"theme":"battle","head":"రావణుని తపస్సు","overlay1":"RAVANA'S","overlay2":"10000 YEAR PENANCE",
       "vo_te":"రావణుడు 10 వేల సంవత్సరాలు తపస్సు చేశాడు. తన 9 తలలు నరుక్కుని హోమంలో వేశాడు",
       "vo_en":"Ravana performed penance for ten thousand years, offering his nine heads in the fire"},
      {"dur":20,"theme":"battle","head":"బ్రహ్మ వరం","overlay1":"BRAHMA GRANTS","overlay2":"POWERFUL BOON",
       "vo_te":"బ్రహ్మదేవుడు ప్రత్యక్షమయ్యాడు. రావణుడు వరం అడిగాడు — దేవతలెవ్వరూ చంపలేకుండా",
       "vo_en":"Brahma appeared and granted the boon — no god or demon could kill Ravana"},
      {"dur":20,"theme":"battle","head":"లోకాల హింస","overlay1":"RAVANA ATTACKS","overlay2":"ALL THREE WORLDS",
       "vo_te":"వరం పొందిన రావణుడు లోకాలన్నీ జయించాడు. దేవతలను హింసించాడు. ఋషులను కష్టపెట్టాడు",
       "vo_en":"With the boon, Ravana conquered all worlds, tormenting gods and sages alike"},
      {"dur":20,"theme":"divine","head":"దేవతల వేడుకోలు","overlay1":"GODS PRAY","overlay2":"TO VISHNU",
       "vo_te":"దేవతలందరూ వైకుంఠానికి వెళ్ళారు. విష్ణువు దగ్గర మొరపెట్టుకున్నారు. రక్షించమని వేడుకున్నారు",
       "vo_en":"All gods rushed to Vaikuntham and prayed before Vishnu to save them"},
      {"dur":20,"theme":"divine","head":"విష్ణువు మాట","overlay1":"VISHNU PROMISES","overlay2":"TO TAKE BIRTH",
       "vo_te":"విష్ణువు చిరునవ్వు నవ్వాడు — నేను మానవుడిగా జన్మించి రావణుని వధిస్తాను అని మాట ఇచ్చాడు",
       "vo_en":"Vishnu smiled and promised — I shall take birth as a human and slay Ravana"},
      {"dur":20,"theme":"golden","head":"అయోధ్య ఎంపిక","overlay1":"AYODHYA CHOSEN","overlay2":"BY VISHNU",
       "vo_te":"విష్ణువు అయోధ్యను ఎంచుకున్నాడు. దశరథుని ఇంట జన్మించాలని నిర్ణయించుకున్నాడు",
       "vo_en":"Vishnu chose Ayodhya and decided to be born in the house of Dasharatha"},
      {"dur":15,"theme":"golden","head":"పుత్రకామేష్టి","overlay1":"SACRED YAGNA","overlay2":"PERFORMED",
       "vo_te":"దశరథుడు పుత్రకామేష్టి యజ్ఞం చేయించాడు. అగ్నిదేవుడు పాయసంతో ప్రత్యక్షమయ్యాడు",
       "vo_en":"Dasharatha conducted the Putrakameshti yagna and Agni appeared with divine payasam"},
      {"dur":15,"theme":"divine","head":"4 పుత్రులు","overlay1":"FOUR PRINCES","overlay2":"BORN TO SAVE EARTH",
       "vo_te":"నలుగురు దివ్య పుత్రులు జన్మించారు. రాముడు, భరతుడు, లక్ష్మణుడు, శత్రుఘ్నుడు",
       "vo_en":"Four divine princes were born — Rama, Bharata, Lakshmana and Shatrughna"},
      {"dur":15,"theme":"divine","head":"లీలావతారం","overlay1":"NOT JUST A KING","overlay2":"GOD HIMSELF",
       "vo_te":"ఇది కేవలం ఒక రాజు పుట్టుక కాదు. ఇది సమస్త లోకాల రక్షణ కోసం దేవుని లీల",
       "vo_en":"This was not merely a king's birth. It was God's divine plan to save all worlds"},
      {"dur":15,"theme":"divine","head":"జై శ్రీరామ్","overlay1":"JAI SHRI RAM","overlay2":"LIKE AND SUBSCRIBE",
       "vo_te":"జై శ్రీరామ్! ఇలాంటి వీడియోలు ఇంకా చూడాలంటే సబ్స్క్రైబ్ చేయండి",
       "vo_en":"Jai Shri Ram! Subscribe for more such amazing Ramayanam videos"},
    ]},

  { "day":1,"num":3,"duration":1,"theme":"golden",
    "title_en":"Dasharatha's Putrakameshti Yagna 3D",
    "title_te":"దశరథుని పుత్రకామేష్టి యజ్ఞం — 3D",
    "hashtags":"#Putrakameshti #Dasharatha #Yagna #Ramayanam #TeluguShorts #Shorts #BalaKanda",
    "scenes":[
      {"dur":10,"theme":"emotional","head":"వారసుడు లేడు","overlay1":"NO HEIR","overlay2":"FOR AYODHYA",
       "vo_te":"దశరథ మహారాజుకు 60 సంవత్సరాలైనా ఒక్క కొడుకు లేడు. గుండె బరువెక్కింది",
       "vo_en":"King Dasharatha had no son even after 60 years. His heart was heavy with grief"},
      {"dur":12,"theme":"golden","head":"వశిష్ఠుని సలహా","overlay1":"SAGE VASISHTHA","overlay2":"ADVISES THE KING",
       "vo_te":"మహర్షి వశిష్ఠుడు సలహా ఇచ్చాడు — ఋష్యశృంగ మహర్షి చేత యజ్ఞం చేయించు",
       "vo_en":"Sage Vasishtha advised — get the Putrakameshti yagna performed by Rishyashringa"},
      {"dur":15,"theme":"golden","head":"యజ్ఞం జ్వాల","overlay1":"SACRED FIRE","overlay2":"BURNS FOR 12 DAYS",
       "vo_te":"12 రోజులు నిరంతరం యజ్ఞం జరిగింది. వేల మంది ఋషులు వేదమంత్రాలు చదివారు",
       "vo_en":"The yagna burned for 12 continuous days with thousands of sages chanting Vedas"},
      {"dur":13,"theme":"divine","head":"అగ్నిదేవుడు","overlay1":"AGNI DEVA","overlay2":"APPEARS FROM FIRE",
       "vo_te":"అగ్ని కుండం నుండి దివ్య పురుషుడు ప్రత్యక్షమయ్యాడు. చేతిలో బంగారు పాత్ర",
       "vo_en":"A divine being appeared from the sacred fire, holding a golden pot"},
      {"dur":10,"theme":"divine","head":"దివ్య పాయసం","overlay1":"DIVINE PAYASAM","overlay2":"GIFT FROM GODS",
       "vo_te":"ఈ పాయసం రాణులకు ఇవ్వండి — మీకు దివ్య పుత్రులు జన్మిస్తారు! జై శ్రీరామ్",
       "vo_en":"Give this payasam to your queens and divine sons shall be born. Jai Shri Ram!"},
    ]},

  { "day":1,"num":4,"duration":3,"theme":"golden",
    "title_en":"Ancient Ayodhya — 3D City Tour",
    "title_te":"పురాతన అయోధ్య నగరం — 3D పర్యటన",
    "hashtags":"#Ayodhya #AncientCity #Ramayanam #TeluguShorts #3DTour #Shorts #రామాయణం",
    "scenes":[
      {"dur":18,"theme":"golden","head":"అయోధ్య నగరం","overlay1":"AYODHYA","overlay2":"THE UNCONQUERABLE CITY",
       "vo_te":"సరయూ నది ఒడ్డున కోసల దేశంలో ప్రపంచంలోనే అత్యంత సుందరమైన నగరం — అయోధ్య",
       "vo_en":"On the banks of river Sarayu, in Kosala kingdom, stood the world's most beautiful city — Ayodhya"},
      {"dur":18,"theme":"golden","head":"వాల్మీకి వర్ణన","overlay1":"12 YOJANAS LONG","overlay2":"3 YOJANAS WIDE",
       "vo_te":"వాల్మీకి మహర్షి చెప్పారు — 12 యోజనాల పొడవు, 3 యోజనాల వెడల్పు, 7 అంతస్తుల ప్రాకారాలు",
       "vo_en":"Sage Valmiki described — 12 yojanas long, 3 wide, protected by 7-layered massive walls"},
      {"dur":20,"theme":"golden","head":"రాజభవనం","overlay1":"GOLDEN PALACE","overlay2":"OF DASHARATHA",
       "vo_te":"దశరథ మహారాజు రాజభవనం — వేల స్తంభాలు, బంగారు చెక్కడాలు, రత్నాల కిటికీలు",
       "vo_en":"Dasharatha's palace had thousands of pillars, golden carvings and jeweled windows"},
      {"dur":20,"theme":"golden","head":"నగర జీవితం","overlay1":"NO POOR PERSON","overlay2":"IN ALL OF AYODHYA",
       "vo_te":"అయోధ్యలో ఒక్క నిరుపేద మనిషి లేడు. ప్రతి ఇంట్లో ధాన్యం నిండి ఉండేది",
       "vo_en":"There was not a single poor person in Ayodhya. Every home was filled with grain"},
      {"dur":20,"theme":"ocean","head":"సరయూ నది","overlay1":"RIVER SARAYU","overlay2":"LIFE OF AYODHYA",
       "vo_te":"సరయూ నది అయోధ్యకు జీవనది. ఆమె ఒడ్డున ఘాట్లు, స్నానఘాట్లు, దేవాలయాలు",
       "vo_en":"River Sarayu was the lifeblood of Ayodhya, with ghats, bathing steps and temples"},
      {"dur":18,"theme":"golden","head":"రాజ మార్గాలు","overlay1":"WIDE STREETS","overlay2":"ALWAYS WATERED",
       "vo_te":"అయోధ్య వీధులు ఎప్పుడూ నీళ్ళు చల్లి శుభ్రంగా ఉంచేవారు. పూల అలంకరణలు",
       "vo_en":"Ayodhya's streets were always watered clean and decorated with flowers"},
      {"dur":18,"theme":"divine","head":"దేవాలయాలు","overlay1":"TEMPLES IN EVERY","overlay2":"STREET OF AYODHYA",
       "vo_te":"ప్రతి వీధిలో దేవాలయాలు ఉండేవి. ప్రతి గుడిలో దీపాలు వెలిగేవి",
       "vo_en":"Every street had temples and every temple had lamps burning through the night"},
      {"dur":18,"theme":"golden","head":"అజేయమైనది","overlay1":"AYODHYA MEANS","overlay2":"UNCONQUERABLE",
       "vo_te":"అయోధ్య అంటే అర్థమే జయించలేనిది. శత్రువులెవ్వరూ ఈ నగరాన్ని జయించలేకపోయారు",
       "vo_en":"Ayodhya means unconquerable. No enemy in history could ever defeat this great city"},
      {"dur":18,"theme":"divine","head":"విష్ణువు ఎంపిక","overlay1":"VISHNU CHOSE","overlay2":"THIS SACRED CITY",
       "vo_te":"ఇంత గొప్ప నగరంలోనే విష్ణువు అవతరించడానికి ఎంచుకున్నాడు. ఎంత అదృష్టం",
       "vo_en":"In this magnificent city, Vishnu chose to take birth. What great fortune"},
      {"dur":10,"theme":"golden","head":"జై శ్రీరామ్","overlay1":"JAI SHRI RAM","overlay2":"SUBSCRIBE FOR MORE",
       "vo_te":"అయోధ్య దర్శనం నచ్చిందా? కామెంట్లో చెప్పండి. సబ్స్క్రైబ్ చేయండి. జై శ్రీరామ్",
       "vo_en":"Liked the Ayodhya tour? Comment below. Subscribe for more. Jai Shri Ram"},
    ]},

  { "day":1,"num":5,"duration":1,"theme":"divine",
    "title_en":"4 Brothers — Rama Lakshmana Bharat Shatrughna",
    "title_te":"నలుగురు సోదరులు — రాముడు లక్ష్మణుడు భరతుడు శత్రుఘ్నుడు",
    "hashtags":"#4Brothers #Rama #Lakshmana #Bharata #Ramayanam #TeluguShorts #Shorts #BalaKanda",
    "scenes":[
      {"dur":8, "theme":"divine","head":"నలుగురు అవతారాలు","overlay1":"FOUR DIVINE","overlay2":"AVATARS BORN",
       "vo_te":"అయోధ్యలో నలుగురు రాజకుమారులు జన్మించారు. ఒక్కొక్కరూ దివ్యుల అవతారాలు",
       "vo_en":"Four divine princes were born in Ayodhya, each an incarnation of the divine"},
      {"dur":13,"theme":"divine","head":"రాముడు","overlay1":"RAMA — VISHNU","overlay2":"AVATAR OF GOD",
       "vo_te":"రాముడు — కౌసల్య తనయుడు. నీలమేఘ శ్యాముడు. విష్ణువు స్వయంగా అవతరించాడు",
       "vo_en":"Rama, son of Kaushalya, dark as a monsoon cloud. Vishnu himself incarnated"},
      {"dur":12,"theme":"ocean","head":"లక్ష్మణుడు","overlay1":"LAKSHMANA","overlay2":"ADI SESHA AVATAR",
       "vo_te":"లక్ష్మణుడు — సుమిత్ర తనయుడు. ఆదిశేషుని అవతారం. రాముని నీడలా జీవించాడు",
       "vo_en":"Lakshmana, son of Sumitra, avatar of Adishesha. He lived as Rama's very shadow"},
      {"dur":12,"theme":"golden","head":"భరతుడు","overlay1":"BHARATA","overlay2":"THE NOBLE SACRIFICE",
       "vo_te":"భరతుడు — కైకేయి తనయుడు. సుదర్శన చక్రం అవతారం. రాజ్యం వచ్చినా వదిలేసాడు",
       "vo_en":"Bharata, son of Kaikeyi, avatar of Sudarshana Chakra. He gave up the kingdom"},
      {"dur":15,"theme":"divine","head":"సంపూర్ణ విష్ణువు","overlay1":"FOUR TOGETHER","overlay2":"ONE COMPLETE VISHNU",
       "vo_te":"నలుగురూ కలిస్తే ఒక సంపూర్ణ విష్ణువు! ఇది రామాయణం యొక్క రహస్యం. జై శ్రీరామ్",
       "vo_en":"Together the four form one complete Vishnu. This is the secret of Ramayana. Jai Shri Ram"},
    ]},

  # ── DAY 2 — BALA KANDA continued ─────────────────────────
  { "day":2,"num":1,"duration":3,"theme":"battle",
    "title_en":"Vishwamitra Takes Young Rama to Forest",
    "title_te":"విశ్వామిత్రుడు బాల రాముని తీసుకుపోయాడు",
    "hashtags":"#Vishwamitra #YoungRama #Ramayanam #TeluguShorts #Shorts #BalaKanda #రామాయణం",
    "scenes":[
      {"dur":20,"theme":"divine","head":"విశ్వామిత్రుడు","overlay1":"SAGE VISHWAMITRA","overlay2":"ARRIVES IN AYODHYA",
       "vo_te":"ఒక రోజు బ్రహ్మర్షి విశ్వామిత్రుడు అయోధ్యకు వచ్చాడు. దశరథుని కొలువు కూటంలో",
       "vo_en":"One day the great sage Vishwamitra arrived at Ayodhya and entered Dasharatha's court"},
      {"dur":20,"theme":"battle","head":"రాక్షస బాధ","overlay1":"DEMONS DISTURB","overlay2":"SACRED YAGNA",
       "vo_te":"విశ్వామిత్రుడు చెప్పాడు — నా యజ్ఞాన్ని రాక్షసులు పాడుచేస్తున్నారు. రాముని ఇవ్వు",
       "vo_en":"Vishwamitra said — demons are destroying my yagna. Give me Rama to protect it"},
      {"dur":20,"theme":"emotional","head":"దశరథుని భయం","overlay1":"DASHARATHA","overlay2":"REFUSES IN FEAR",
       "vo_te":"దశరథుడు గాభరాపడ్డాడు — రాముడింకా చిన్నపిల్లాడు! నేను వస్తాను, వాడిని పంపడం వీలుకాదు",
       "vo_en":"Dasharatha panicked — Rama is just a child! I shall come instead, I cannot send him"},
      {"dur":20,"theme":"divine","head":"వశిష్ఠుని మాట","overlay1":"SAGE VASISHTHA","overlay2":"ASSURES THE KING",
       "vo_te":"వశిష్ఠుడు చెప్పాడు — మహారాజా, రాముడు సాధారణ బాలుడు కాదు. విశ్వామిత్రుడు రక్షిస్తాడు",
       "vo_en":"Vasishtha said — O King, Rama is no ordinary boy. Vishwamitra will protect him"},
      {"dur":18,"theme":"golden","head":"నిర్ణయం","overlay1":"RAMA LEAVES","overlay2":"WITH A SMILE",
       "vo_te":"రాముడు తండ్రి ముందు నమస్కరించాడు. చిరునవ్వుతో విశ్వామిత్రుని వెంట బయలుదేరాడు",
       "vo_en":"Rama bowed before his father and set off with Vishwamitra, smiling with no fear"},
      {"dur":18,"theme":"forest","head":"అడవి మార్గం","overlay1":"INTO THE FOREST","overlay2":"ON FOOT",
       "vo_te":"రాముడు, లక్ష్మణుడు విశ్వామిత్రుని వెంట అడవి బాటలో నడిచారు. విల్లు భుజాన వేసుకుని",
       "vo_en":"Rama and Lakshmana walked the forest path with Vishwamitra, bows on their shoulders"},
      {"dur":18,"theme":"battle","head":"తాటక వధ","overlay1":"TADAKA THE DEMON","overlay2":"RAMA'S FIRST BATTLE",
       "vo_te":"అడవిలో భయంకరమైన తాటక రాక్షసి అడ్డుపడింది. రాముడు మొదటి యుద్ధంలో ఆమెను వధించాడు",
       "vo_en":"The terrifying demon Tadaka blocked their path. Rama slew her in his very first battle"},
      {"dur":18,"theme":"divine","head":"దివ్యాస్త్రాలు","overlay1":"DIVINE WEAPONS","overlay2":"GIFTED TO RAMA",
       "vo_te":"విశ్వామిత్రుడు సంతోషపడ్డాడు. రాముడికి అనేక దివ్యాస్త్రాలు ఇచ్చాడు",
       "vo_en":"Vishwamitra was overjoyed and gifted Rama numerous divine weapons as reward"},
      {"dur":18,"theme":"golden","head":"యజ్ఞ రక్షణ","overlay1":"YAGNA PROTECTED","overlay2":"BY YOUNG RAMA",
       "vo_te":"రాముడు, లక్ష్మణుడు కలిసి యజ్ఞాన్ని రక్షించారు. విశ్వామిత్రుడు సంతోషంతో నిండిపోయాడు",
       "vo_en":"Rama and Lakshmana together protected the sacred yagna. Vishwamitra was filled with joy"},
      {"dur":8, "theme":"divine","head":"జై శ్రీరామ్","overlay1":"JAI SHRI RAM","overlay2":"LIKE AND SHARE",
       "vo_te":"రాముని బాల్యం ఇంతటి అద్భుతంగా ఉంది! జై శ్రీరామ్! సబ్స్క్రైబ్ చేయండి",
       "vo_en":"Rama's childhood was this wonderful! Jai Shri Ram! Please subscribe"},
    ]},

  { "day":2,"num":2,"duration":1,"theme":"battle",
    "title_en":"Tadaka Vadha — Rama's First Battle",
    "title_te":"తాటక వధ — రాముని మొదటి యుద్ధం",
    "hashtags":"#TadakaVadha #YoungRama #FirstBattle #Ramayanam #TeluguShorts #Shorts",
    "scenes":[
      {"dur":10,"theme":"forest","head":"తాటక అడవి","overlay1":"TADAKA'S FOREST","overlay2":"DARK AND CURSED",
       "vo_te":"తాటక అడవి చాలా భయంకరంగా ఉంది. అక్కడ పక్షులు కూడా ఉండేవి కావు",
       "vo_en":"Tadaka's forest was terrifying. Even birds dared not enter this cursed land"},
      {"dur":15,"theme":"battle","head":"తాటక దాడి","overlay1":"TADAKA ATTACKS","overlay2":"WITH FULL FURY",
       "vo_te":"భయంకరమైన తాటక పెద్ద అరుపుతో వచ్చింది. ఆమె శరీరం పర్వతంలా ఉంది",
       "vo_en":"The terrifying Tadaka came with a mighty roar. Her body was like a mountain"},
      {"dur":15,"theme":"battle","head":"రాముని బాణం","overlay1":"RAMA'S ARROW","overlay2":"NEVER MISSES",
       "vo_te":"రాముడు విల్లు ఎక్కుపెట్టాడు. ఒక్క బాణంతో తాటకను వధించాడు. విశ్వామిత్రుడు ఆశ్చర్యపోయాడు",
       "vo_en":"Rama drew his bow and with a single arrow slew Tadaka. Vishwamitra was amazed"},
      {"dur":20,"theme":"divine","head":"మొదటి విజయం","overlay1":"FIRST VICTORY","overlay2":"AT AGE 16",
       "vo_te":"16 సంవత్సరాల రాముడు మొదటి యుద్ధంలో విజయం సాధించాడు. ఇది విష్ణువు శక్తి",
       "vo_en":"16-year-old Rama won his first battle. This was the power of Vishnu himself"},
    ]},

  { "day":2,"num":3,"duration":1,"theme":"divine",
    "title_en":"Ahalya Moksha — Stone Becomes Woman",
    "title_te":"అహల్య మోక్షం — రాముని పాద స్పర్శ",
    "hashtags":"#Ahalya #AhalyaMoksha #Ramayanam #TeluguShorts #Shorts #BalaKanda",
    "scenes":[
      {"dur":12,"theme":"forest","head":"శిల అడవిలో","overlay1":"A STONE IN","overlay2":"THE FOREST",
       "vo_te":"అడవిలో ఒక పెద్ద రాయి ఉంది. విశ్వామిత్రుడు చెప్పాడు — రాముడా ఈ రాయికి నమస్కరించు",
       "vo_en":"In the forest lay a large stone. Vishwamitra said — Rama, bow to this stone"},
      {"dur":15,"theme":"emotional","head":"అహల్య శాపం","overlay1":"AHALYA CURSED","overlay2":"TO BECOME STONE",
       "vo_te":"ఆ రాయి గౌతమ ముని భార్య అహల్య. ఆమె తప్పుకు శాపంగా రాయిగా మారింది",
       "vo_en":"That stone was Ahalya, wife of sage Gautama. She had been cursed to become stone"},
      {"dur":15,"theme":"divine","head":"రాముని పాదం","overlay1":"RAMA'S HOLY FEET","overlay2":"TOUCH THE STONE",
       "vo_te":"రాముని పాదం ఆ రాయిని తాకింది. వెంటనే దివ్యమైన వెలుతురు వెలువడింది",
       "vo_en":"Rama's holy feet touched the stone. Immediately a divine light burst forth"},
      {"dur":18,"theme":"divine","head":"అహల్య లేచింది","overlay1":"AHALYA FREED","overlay2":"FROM THE CURSE",
       "vo_te":"అహల్య రాయి నుండి బయటకు వచ్చింది. రాముని పాదాలకు నమస్కరించింది. శాపం తీరింది",
       "vo_en":"Ahalya emerged from the stone and bowed at Rama's feet. The curse was lifted"},
    ]},

  { "day":2,"num":4,"duration":3,"theme":"golden",
    "title_en":"Sita Swayamvar — Rama Breaks Shiva's Bow",
    "title_te":"సీత స్వయంవరం — రాముడు శివుని విల్లు విరచాడు",
    "hashtags":"#SitaSwayamvar #RamaBreaksBow #Ramayanam #TeluguShorts #Shorts #BalaKanda",
    "scenes":[
      {"dur":18,"theme":"golden","head":"జనకుని సభ","overlay1":"KING JANAKA'S","overlay2":"GRAND COURT",
       "vo_te":"మిధిలానగరంలో రాజు జనకుడు స్వయంవరం ఏర్పాటు చేశాడు. ప్రపంచమంతా తెలిసింది",
       "vo_en":"King Janaka of Mithila arranged a great swayamvar. The news spread across the world"},
      {"dur":18,"theme":"divine","head":"సీత పరిచయం","overlay1":"PRINCESS SITA","overlay2":"DAUGHTER OF EARTH",
       "vo_te":"సీత — జనకుని కుమార్తె. భూమాత పుత్రి. ఆమె సౌందర్యం అసాధారణం",
       "vo_en":"Sita, daughter of Janaka and child of Mother Earth. Her beauty was beyond description"},
      {"dur":18,"theme":"golden","head":"శివుని విల్లు","overlay1":"SHIVA'S BOW","overlay2":"IMPOSSIBLE TO LIFT",
       "vo_te":"జనకుడు ప్రకటించాడు — ఈ శివుని విల్లు ఎవడు ఎక్కుపెడతాడో అతనికి సీతనిస్తాను",
       "vo_en":"Janaka declared — whoever strings Shiva's bow shall win Sita's hand in marriage"},
      {"dur":18,"theme":"battle","head":"రాజుల వైఫల్యం","overlay1":"100 KINGS FAIL","overlay2":"TO LIFT THE BOW",
       "vo_te":"వందల మంది రాజులు వచ్చారు. ఒక్కరూ విల్లు కదిలించలేకపోయారు. అందరూ నిరాశపడ్డారు",
       "vo_en":"Hundreds of kings came but none could even move the bow. All left in shame"},
      {"dur":18,"theme":"divine","head":"రాముడు లేచాడు","overlay1":"RAMA RISES","overlay2":"FROM HIS SEAT",
       "vo_te":"విశ్వామిత్రుడు సైగ చేశాడు. రాముడు నిదానంగా లేచాడు. సభ అంతా నిశ్శబ్దమైంది",
       "vo_en":"Vishwamitra gestured. Rama rose calmly. The entire court fell silent in anticipation"},
      {"dur":20,"theme":"golden","head":"విల్లు పట్టాడు","overlay1":"RAMA LIFTS","overlay2":"THE DIVINE BOW",
       "vo_te":"రాముడు విల్లు తాకాడు. అప్రయత్నంగా పైకి లేపాడు. సభ ఆశ్చర్యంతో చప్పట్లు కొట్టింది",
       "vo_en":"Rama touched the bow and lifted it effortlessly. The court erupted with amazement"},
      {"dur":20,"theme":"battle","head":"విల్లు విరిగింది","overlay1":"THE BOW SNAPS","overlay2":"WITH THUNDER",
       "vo_te":"రాముడు విల్లు ఎక్కుపెట్టాడు. పెద్ద శబ్దంతో విల్లు రెండుగా విరిగిపోయింది",
       "vo_en":"Rama strung the bow and with a thunderous crack it snapped into two pieces"},
      {"dur":18,"theme":"divine","head":"సీత వరమాల","overlay1":"SITA GARLANDS","overlay2":"HER RAMA",
       "vo_te":"సీత సంతోషంతో నిండిపోయింది. రాముని మెడలో వరమాల వేసింది. ఇరువురూ ఆనందపడ్డారు",
       "vo_en":"Sita was filled with joy and placed the wedding garland around Rama's neck"},
      {"dur":18,"theme":"golden","head":"పరశురాముని సవాలు","overlay1":"PARASHURAMA","overlay2":"CHALLENGES RAMA",
       "vo_te":"పరశురాముడు కోపంగా వచ్చాడు. రాముడు నిర్భయంగా అతని సవాలు స్వీకరించాడు",
       "vo_en":"Parashurama came in anger but Rama fearlessly accepted his challenge"},
      {"dur":12,"theme":"divine","head":"జై శ్రీరామ్","overlay1":"JAI SHRI RAM","overlay2":"SUBSCRIBE NOW",
       "vo_te":"రామ సీతల వివాహం సమస్త లోకాలను ఆనంద పరిచింది. జై శ్రీరామ్ సబ్స్క్రైబ్ చేయండి",
       "vo_en":"The marriage of Rama and Sita filled all worlds with joy. Jai Shri Ram subscribe"},
    ]},

  { "day":2,"num":5,"duration":1,"theme":"divine",
    "title_en":"Rama Sita Wedding — Grand Ceremony",
    "title_te":"రామ సీత వివాహం — భవ్యమైన వేడుక",
    "hashtags":"#RamaSitaWedding #Vivah #Ramayanam #TeluguShorts #Shorts #BalaKanda #రామాయణం",
    "scenes":[
      {"dur":12,"theme":"golden","head":"వివాహ వేడుక","overlay1":"GRAND WEDDING","overlay2":"IN MITHILA",
       "vo_te":"మిధిలా నగరం పూలతో అలంకరించబడింది. రామ సీత వివాహానికి లోకమంతా వచ్చింది",
       "vo_en":"Mithila was decorated with flowers. The whole world came for Rama and Sita's wedding"},
      {"dur":15,"theme":"divine","head":"సప్తపది","overlay1":"SEVEN STEPS","overlay2":"SACRED VOWS",
       "vo_te":"రాముడు సీత చేయి పట్టుకున్నాడు. అగ్ని చుట్టూ సప్తపది నడిచారు. ముహూర్తం శుభంగా ముగిసింది",
       "vo_en":"Rama held Sita's hand and they took the seven sacred steps around the holy fire"},
      {"dur":15,"theme":"golden","head":"దేవతల దీవెనలు","overlay1":"GODS SHOWER","overlay2":"DIVINE BLESSINGS",
       "vo_te":"దేవతలు ఆకాశం నుండి పూలు కురిపించారు. శుభాకాంక్షలు తెలిపారు. లోకమంతా సంతోషించింది",
       "vo_en":"Gods showered flowers from the sky, blessing the divine couple from above"},
      {"dur":18,"theme":"divine","head":"నిత్య బంధం","overlay1":"ETERNAL BOND","overlay2":"RAMA AND SITA",
       "vo_te":"రాముడు సీత — ఈ జంట అనాదిగా ముడిపడి ఉంది. ఇది లోకానికి ఆదర్శ దాంపత్యం. జై శ్రీరామ్",
       "vo_en":"Rama and Sita — eternally bound together. This is the ideal marriage for all worlds"},
    ]},
]

# ══════════════════════════════════════════════════════════════
#  COLOR THEMES
# ══════════════════════════════════════════════════════════════
THEMES = {
    "divine":   {"b1":(8,4,28),   "b2":(35,15,70),  "acc":(212,175,55),"txt":(245,235,200)},
    "battle":   {"b1":(30,3,3),   "b2":(90,15,5),   "acc":(220,60,30), "txt":(255,220,200)},
    "forest":   {"b1":(3,20,8),   "b2":(8,50,18),   "acc":(80,200,100),"txt":(220,255,220)},
    "emotional":{"b1":(15,5,30),  "b2":(45,20,65),  "acc":(200,100,220),"txt":(240,220,250)},
    "ocean":    {"b1":(3,12,35),  "b2":(8,35,80),   "acc":(40,180,220),"txt":(200,235,255)},
    "golden":   {"b1":(25,18,3),  "b2":(70,50,8),   "acc":(212,175,55),"txt":(255,245,210)},
}
GOLD=(212,175,55); WHITE=(255,255,255); SAFFRON=(255,149,0)

# ══════════════════════════════════════════════════════════════
#  FONT LOADER
# ══════════════════════════════════════════════════════════════
_FONT_CACHE = {}
def fnt(size):
    if size in _FONT_CACHE: return _FONT_CACHE[size]
    paths = [
        "C:/Windows/Fonts/arialbd.ttf","C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibrib.ttf","C:/Windows/Fonts/segoeui.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                f = ImageFont.truetype(p,size)
                _FONT_CACHE[size]=f
                return f
            except: pass
    f = ImageFont.load_default()
    _FONT_CACHE[size]=f
    return f

# ══════════════════════════════════════════════════════════════
#  FRAME DRAWING
# ══════════════════════════════════════════════════════════════
def make_frame(scene, fi, total_fi, global_pct):
    th = THEMES.get(scene.get("theme","divine"), THEMES["divine"])
    b1,b2 = th["b1"],th["b2"]

    # gradient bg
    arr = np.zeros((H,W,3),np.uint8)
    for y in range(H):
        t = y/H
        arr[y,:] = [int(b1[k]*(1-t)+b2[k]*t) for k in range(3)]

    # animated stars
    rng = np.random.default_rng(scene.get("id",1)*777+fi//8)
    for _ in range(50):
        px,py = int(rng.integers(0,W)),int(rng.integers(0,H))
        a = 0.15+0.35*abs(math.sin(fi*0.07+px*0.01))
        ov = arr.copy(); cv2.circle(ov,(px,py),2,th["acc"][::-1],-1)
        cv2.addWeighted(ov,a,arr,1-a,0,arr)

    # border
    g = th["acc"][::-1]
    cv2.rectangle(arr,(28,28),(W-28,H-28),g,1)
    cv2.rectangle(arr,(36,36),(W-36,H-36),g,1)
    for cx,cy in [(28,28),(W-28,28),(28,H-28),(W-28,H-28)]:
        cv2.circle(arr,(cx,cy),10,g,1); cv2.circle(arr,(cx,cy),2,g,-1)

    # progress bar
    bx = int((W-80)*global_pct)
    cv2.rectangle(arr,(40,46),(40+bx,54),th["acc"][::-1],-1)

    pil  = Image.fromarray(cv2.cvtColor(arr,cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil)
    acc  = th["acc"]; txt = th["txt"]

    def shadow_text(x,y,text,size,color,sh=(0,0,0),off=3):
        draw.text((x+off,y+off),text,font=fnt(size),fill=sh,anchor="mm")
        draw.text((x,y),         text,font=fnt(size),fill=color,anchor="mm")

    # emoji icon per theme
    icons={"divine":"✨","battle":"⚔","forest":"🌿","emotional":"💫","ocean":"🌊","golden":"👑"}
    shadow_text(W//2, H//2-400, icons.get(scene.get("theme","divine"),"✨"), 110, acc)

    # decorative line
    lw=320
    draw.rectangle([W//2-lw//2, H//2-280, W//2+lw//2, H//2-274], fill=acc)

    # heading
    head = scene.get("head","RAMAYANAM").upper()
    y = H//2-255
    for line in textwrap.wrap(head, 14):
        shadow_text(W//2, y, line, 72, acc); y+=88

    # overlay lines
    y2 = H//2+30
    for key,col in [("overlay1",WHITE),("overlay2",tuple(min(255,c+80) for c in acc))]:
        val = scene.get(key,"")
        if val:
            shadow_text(W//2, y2, val.upper(), 52, col); y2+=68

    # subtitle
    vo = scene.get("vo_en","")
    y3 = H-310
    for line in textwrap.wrap(vo, 30)[:3]:
        try:
            bb=fnt(38).getbbox(line); bw=bb[2]-bb[0]+36; bh=bb[3]-bb[1]+18
            pill=Image.new("RGBA",(bw,bh),(0,0,0,155))
            pil.paste(pill,(W//2-bw//2,y3-9),pill)
        except: pass
        shadow_text(W//2, y3+4, line, 38, SAFFRON, off=2); y3+=56

    # watermark
    shadow_text(W//2, H-55, "🏹 Ramayanam Telugu Shorts", 26, (180,155,90), off=1)
    # scene num
    draw.ellipse([W-95,70,W-55,110],outline=acc,width=2)
    shadow_text(W-75, 90, str(scene.get("id",1)), 26, acc, off=1)

    return cv2.cvtColor(np.array(pil),cv2.COLOR_RGB2BGR)

def make_intro(fi, total, ch_name):
    arr = np.zeros((H,W,3),np.uint8)
    for y in range(H):
        t=y/H; arr[y,:]=[int(8*(1-t)+35*t),int(4*(1-t)+15*t),int(28*(1-t)+70*t)]
    cv2.rectangle(arr,(28,28),(W-28,H-28),(212,175,55),1)
    pil=Image.fromarray(cv2.cvtColor(arr,cv2.COLOR_BGR2RGB))
    draw=ImageDraw.Draw(pil)
    fade=min(1.0,fi/20)
    def st(x,y,t,s,c):
        cc=tuple(int(v*fade) for v in c)
        draw.text((x+3,y+3),t,font=fnt(s),fill=(0,0,0),anchor="mm")
        draw.text((x,y),t,font=fnt(s),fill=cc,anchor="mm")
    st(W//2,H//2-180,"🏹",110,GOLD)
    st(W//2,H//2+20,ch_name.upper(),68,GOLD)
    st(W//2,H//2+130,"రామాయణం తెలుగు షార్ట్స్",44,WHITE)
    st(W//2,H-80,"Daily Ramayanam Shorts in Telugu",30,(180,155,90))
    return cv2.cvtColor(np.array(pil),cv2.COLOR_RGB2BGR)

def make_outro(fi, total):
    arr = np.zeros((H,W,3),np.uint8)
    for y in range(H):
        t=y/H; arr[y,:]=[int(25*(1-t)+70*t),int(18*(1-t)+50*t),int(3*(1-t)+8*t)]
    cv2.rectangle(arr,(28,28),(W-28,H-28),(212,175,55),1)
    pil=Image.fromarray(cv2.cvtColor(arr,cv2.COLOR_BGR2RGB))
    draw=ImageDraw.Draw(pil)
    def st(x,y,t,s,c):
        draw.text((x+2,y+2),t,font=fnt(s),fill=(0,0,0),anchor="mm")
        draw.text((x,y),t,font=fnt(s),fill=c,anchor="mm")
    st(W//2,H//2-220,"జై శ్రీరామ్! 🙏",68,GOLD)
    st(W//2,H//2-80,"👍  Like చేయండి",56,WHITE)
    st(W//2,H//2+40,"🔔  Subscribe చేయండి",56,SAFFRON)
    st(W//2,H//2+160,"🔗  Share చేయండి",56,WHITE)
    st(W//2,H-80,"🏹 Ramayanam Telugu Shorts",30,(180,155,90))
    return cv2.cvtColor(np.array(pil),cv2.COLOR_RGB2BGR)

# ══════════════════════════════════════════════════════════════
#  VIDEO RENDERER
# ══════════════════════════════════════════════════════════════
def render_video(video_data, slug):
    print("\n  🎬  Rendering video...")
    raw = TMPDIR/f"raw_{slug}.mp4"
    writer = cv2.VideoWriter(str(raw),cv2.VideoWriter_fourcc(*"mp4v"),FPS,(W,H))

    intro_f = 2*FPS; outro_f = 3*FPS
    scene_f = sum(s["dur"]*FPS for s in video_data["scenes"])
    total_f = intro_f+scene_f+outro_f
    done=0

    # INTRO
    for fi in range(intro_f):
        writer.write(make_intro(fi,intro_f,"Ramayanam Shorts"))
        done+=1; _bar(done,total_f,"Intro")

    # SCENES
    for idx,scene in enumerate(video_data["scenes"]):
        scene["id"]=idx+1
        nf=scene["dur"]*FPS
        for fi in range(nf):
            writer.write(make_frame(scene,fi,nf,done/total_f))
            done+=1; _bar(done,total_f,f"Scene {idx+1}")

    # OUTRO
    for fi in range(outro_f):
        writer.write(make_outro(fi,outro_f))
        done+=1; _bar(done,total_f,"Outro")

    writer.release()
    print(f"\n  ✓ Raw video done")
    return str(raw)

def _bar(d,t,lbl):
    p=int(d/t*100); b="█"*(p//5)+"░"*(20-p//5)
    print(f"  [{b}] {p:3d}%  {lbl}          ",end="\r")

# ══════════════════════════════════════════════════════════════
#  AUDIO + SRT
# ══════════════════════════════════════════════════════════════
def gen_audio(video_data, language, slug):
    print("\n\n  🎙️  Generating audio...")
    clips=[]
    for i,s in enumerate(video_data["scenes"],1):
        text = s["vo_te"] if language=="telugu" else s["vo_en"]
        lang = "te" if language=="telugu" else "en"
        try:
            p=TMPDIR/f"a_{slug}_{i:02d}.mp3"
            gTTS(text=text,lang=lang,slow=False).save(str(p))
            clips.append((str(p),s["dur"]))
            print(f"  ✓ Scene {i}",end="\r")
        except Exception as e:
            print(f"  ⚠ Scene {i} failed: {e}")
            clips.append((None,s["dur"]))

    # merge with pydub if available, else ffmpeg concat
    try:
        from pydub import AudioSegment
        out_audio = AudioSegment.silent(duration=2000)
        for path,dur in clips:
            ms=dur*1000
            if path and os.path.exists(path):
                seg=AudioSegment.from_mp3(path)
                seg=seg[:ms] if len(seg)>ms else seg+AudioSegment.silent(ms-len(seg))
            else:
                seg=AudioSegment.silent(duration=ms)
            out_audio+=seg
        out_audio+=AudioSegment.silent(duration=3000)
        out=TMPDIR/f"audio_{slug}.mp3"
        out_audio.export(str(out),format="mp3")
        print(f"\n  ✓ Audio merged")
        return str(out)
    except ImportError:
        # fallback: just use first clip
        if clips and clips[0][0]:
            print(f"\n  ✓ Using first audio clip (install pydub for full merge)")
            return clips[0][0]
        return None

def gen_srt(video_data, language, slug):
    path=OUTDIR/f"subtitles_{slug}.srt"
    lines=[]; t=2.0
    for i,s in enumerate(video_data["scenes"],1):
        text=s["vo_te"] if language=="telugu" else s["vo_en"]
        dur=s["dur"]
        wrapped="\n".join(textwrap.wrap(text,40))
        lines.append(f"{i}\n{_ts(t)} --> {_ts(t+dur)}\n{wrapped}\n")
        t+=dur
    path.write_text("\n".join(lines),encoding="utf-8")
    print(f"  ✓ Subtitles: {path.name}")
    return str(path)

def _ts(s):
    h=int(s//3600);m=int(s%3600//60);sec=s%60
    return f"{h:02d}:{m:02d}:{sec:06.3f}".replace(".",",")

# ══════════════════════════════════════════════════════════════
#  MERGE WITH FFMPEG
# ══════════════════════════════════════════════════════════════
def merge(video, audio, slug):
    if not audio or not os.path.exists(audio):
        import shutil
        out=OUTDIR/f"FINAL_{slug}.mp4"; shutil.copy(video,out); return str(out)
    out=OUTDIR/f"FINAL_{slug}.mp4"
    cmd=(f'ffmpeg -y -i "{video}" -i "{audio}" -c:v libx264 '
         f'-c:a aac -shortest -movflags +faststart "{out}" -loglevel error')
    print("  🔗  Merging video + audio...")
    ret=os.system(cmd)
    if ret==0 and out.exists():
        print(f"  ✓ Final: {out.name}"); return str(out)
    import shutil; out2=OUTDIR/f"FINAL_{slug}_no_audio.mp4"
    shutil.copy(video,out2); return str(out2)

# ══════════════════════════════════════════════════════════════
#  SAVE YOUTUBE META
# ══════════════════════════════════════════════════════════════
def save_meta(video_data, srt, final, slug):
    p=OUTDIR/f"youtube_{slug}.txt"
    p.write_text(f"""
{'='*55}
YOUTUBE UPLOAD — {video_data['title_te']}
{'='*55}

TITLE (Telugu): {video_data['title_te']}
TITLE (English): {video_data['title_en']}

DESCRIPTION:
రామాయణం తెలుగు షార్ట్స్ — ప్రతిరోజు కొత్త వీడియో!
{video_data['title_en']} — Full story in Telugu with subtitles.
Subscribe for daily Ramayanam shorts in Telugu! 🏹

{video_data['hashtags']}

UPLOAD STEPS:
[ ] Upload: {Path(final).name}
[ ] Paste Telugu title
[ ] Add subtitle file: {Path(srt).name}
[ ] Add to playlist by Kanda
[ ] Upload time: 7 AM or 9 PM IST
""",encoding="utf-8")
    print(f"  ✓ Meta: {p.name}")
    return str(p)

# ══════════════════════════════════════════════════════════════
#  MAIN MENU
# ══════════════════════════════════════════════════════════════
def main():
    print("\n"+"╔"+"═"*53+"╗")
    print("║  🏹  RAMAYANAM SHORTS — 100% FREE CREATOR     ║")
    print("║  No API key · No paid tools · Just run!        ║")
    print("╚"+"═"*53+"╝\n")

    # group by day
    days = {}
    for v in ALL_VIDEOS:
        days.setdefault(v["day"],[]).append(v)

    print("  Available days:\n")
    for d in sorted(days.keys()):
        vids=days[d]
        print(f"  Day {d} — {len(vids)} videos:")
        for v in vids:
            dur=f"{v['duration']}min"
            print(f"    {v['num']}. [{dur}] {v['title_en']}")
        print()

    mode = input("  Generate (A) All videos  (D) Specific day  (V) One video [A/D/V]: ").strip().upper()

    if mode=="D":
        d = int(input("  Which day? ").strip())
        selected = days.get(d,[])
    elif mode=="V":
        d   = int(input("  Which day? ").strip())
        num = int(input("  Which video number? ").strip())
        selected = [v for v in days.get(d,[]) if v["num"]==num]
    else:
        selected = ALL_VIDEOS

    lang = input("\n  Language? 1=Telugu  2=English  [Enter=Telugu]: ").strip()
    language = "english" if lang=="2" else "telugu"

    if not selected:
        print("  ❌  No videos found for that selection."); return

    print(f"\n  Generating {len(selected)} video(s) in {language}...\n")
    input("  Press Enter to start...")

    for i,vd in enumerate(selected,1):
        print(f"\n{'─'*55}")
        print(f"  Video {i}/{len(selected)}: {vd['title_en']}")
        print(f"{'─'*55}")
        slug = f"day{vd['day']}_{vd['num']}_{int(time.time())}"
        raw   = render_video(vd, slug)
        audio = gen_audio(vd, language, slug)
        srt   = gen_srt(vd, language, slug)
        final = merge(raw, audio, slug)
        save_meta(vd, srt, final, slug)

    print(f"""
{'='*55}
  ✅  ALL DONE!
{'='*55}
  📁  Output: ramayanam_output/
  🎬  Upload FINAL_*.mp4 to YouTube
  📝  Upload subtitles_*.srt in YouTube Studio
  📋  Copy title from youtube_*.txt

  Next video in 2 days — come back for Day 3+!
  🏹  Jai Shri Ram!
{'='*55}
""")

if __name__=="__main__":
    main()
