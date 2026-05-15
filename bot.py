<FILE file_path="/home/workdir/attachments/bot.py" size="125800 bytes">
import discord
from discord.ext import commands, tasks
from discord.ui import Button, View, Select
import json, os, asyncio, aiohttp, datetime, re, random, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io, requests, colorsys, pytz

# ═══════════════════════════════════════════════════════
#  KONFIGURASI
# ═══════════════════════════════════════════════════════
TOKEN                   = os.environ["TOKEN"]
OWNER_ID                = int(os.environ["OWNER_ID"])
SPAM_CHANNEL_ID         = int(os.environ["SPAM_CHANNEL_ID"])
TIKTOK_USERNAME         = os.environ["TIKTOK_USERNAME"]
TIKTOK_CHECK_CHANNEL_ID = int(os.environ["TIKTOK_CHECK_CHANNEL_ID"])
TICKET_CHANNEL_ID       = int(os.environ["TICKET_CHANNEL_ID"])
VOICE_CATEGORY_ID       = int(os.environ["VOICE_CATEGORY_ID"])

WIB = pytz.timezone("Asia/Jakarta")

# ═══════════════════════════════════════════════════════
#  FILE DATABASE
# ═══════════════════════════════════════════════════════
DATA_FILE        = "data.json"
LAST_TIKTOK_FILE = "last_tiktok.json"
YOUTUBE_FILE     = "youtube.json"
TICKET_FILE      = "tickets.json"
VERIF_FILE       = "verif.json"
WARN_FILE        = "warns.json"
GIVEAWAY_FILE    = "giveaways.json"
QUOTE_FILE       = "quotes.json"
SETTINGS_FILE    = "settings.json"
AFK_FILE         = "afk.json"
BANNER_FILE      = "banners.json"
CUSTOM_CMD_FILE  = "custom_commands.json"
COIN_FILE        = "coins.json"
MARKET_FILE      = "market.json"
INVENTORY_FILE   = "inventory.json"

# ═══════════════════════════════════════════════════════
#  LEVEL CONFIG
# ═══════════════════════════════════════════════════════
LEVEL_CONFIG = {
    1: {"name": "Bot",          "xp_required": 0,    "color": (108, 117, 125)},
    2: {"name": "Side Brother", "xp_required": 100,  "color": (23, 162, 184)},
    3: {"name": "Member",       "xp_required": 300,  "color": (40, 167, 69)},
    4: {"name": "Brother",      "xp_required": 700,  "color": (255, 193, 7)},
    5: {"name": "Big Brother",  "xp_required": 1500, "color": (220, 53, 69)},
}
XP_PER_MESSAGE = 10

# Banner rarity config per level range
BANNER_RARITY = {
    "Common":    {"levels": [1, 2],    "color": (150, 150, 150), "chance": 60},
    "Uncommon":  {"levels": [2, 3],    "color": (80, 200, 80),   "chance": 25},
    "Rare":      {"levels": [3, 4],    "color": (80, 120, 255),  "chance": 10},
    "Epic":      {"levels": [4, 5],    "color": (180, 80, 255),  "chance": 4},
    "Legendary": {"levels": [5, 5],    "color": (255, 200, 0),   "chance": 1},
}

# ═══════════════════════════════════════════════════════
#  QUOTES DATABASE (100 quotes)
# ═══════════════════════════════════════════════════════
DEFAULT_QUOTES = [
    "Jangan hitung hari, buat setiap hari diperhitungkan.",
    "Kesuksesan adalah jumlah dari usaha-usaha kecil yang diulang setiap hari.",
    "Jatuh tujuh kali, bangkit delapan kali.",
    "Mimpi tidak bekerja kecuali kamu bekerja.",
    "Setiap hari adalah kesempatan baru untuk menjadi lebih baik.",
    "Kegagalan adalah awal dari kesuksesan.",
    "Percayai prosesnya, hasil tidak pernah mengkhianati usaha.",
    "Jangan takut gagal, takutlah tidak pernah mencoba.",
    "Orang sukses melakukan apa yang orang malas hindari.",
    "Kamu lebih kuat dari yang kamu kira.",
    "Mulailah dari mana kamu berada, gunakan apa yang kamu punya.",
    "Satu langkah kecil hari ini lebih baik dari seribu rencana besok.",
    "Karakter terbentuk bukan saat hidup mudah, tapi saat menghadapi cobaan.",
    "Jangan bandingkan perjalananmu dengan orang lain.",
    "Waktu yang kamu nikmati adalah waktu yang tidak terbuang.",
    "Kesabaran adalah kunci dari segala keberhasilan.",
    "Berani bermimpi besar, tapi mulai dari langkah kecil.",
    "Hidup terlalu singkat untuk menyimpan dendam.",
    "Bersyukur adalah magnet untuk hal-hal baik.",
    "Versi terbaik dari dirimu sedang menunggumu di depan.",
    "Tidak ada jalan pintas menuju tempat yang layak dituju.",
    "Disiplin adalah jembatan antara tujuan dan pencapaian.",
    "Keberanian bukan ketiadaan rasa takut, tapi tetap melangkah meski takut.",
    "Hidup bukan tentang menemukan dirimu, tapi menciptakan dirimu.",
    "Setiap orang punya cerita, jangan nilai buku dari sampulnya.",
    "Yang kamu pikirkan, itulah yang akan menjadi kenyataanmu.",
    "Jangan menunggu sempurna, mulai saja dulu.",
    "Masa depan milik mereka yang percaya pada keindahan impian mereka.",
    "Ribuan mil dimulai dari satu langkah.",
    "Kebahagiaan bukan tujuan, melainkan cara menjalani hidup.",
    "Jadilah perubahan yang ingin kamu lihat di dunia.",
    "Jika kamu tidak bisa terbang, larilah. Jika tidak bisa lari, berjalanlah.",
    "Tidak ada yang impossible bagi mereka yang mau berusaha.",
    "Hidup adalah 10% apa yang terjadi padamu dan 90% bagaimana kamu meresponsnya.",
    "Orang hebat tidak lahir, mereka dibentuk.",
    "Kamu tidak perlu jadi hebat untuk memulai, tapi kamu perlu memulai untuk jadi hebat.",
    "Belajarlah dari kemarin, hiduplah untuk hari ini, berharaplah untuk esok.",
    "Jangan biarkan ketakutan masa lalu merusak kebahagiaan masa depan.",
    "Senyum adalah senjata paling murah namun paling efektif.",
    "Jadikan setiap momen berarti, karena waktu tidak bisa diputar kembali.",
    "Tekad yang kuat adalah kunci membuka pintu kesempatan.",
    "Kegagalan hanya berakhir saat kamu berhenti mencoba.",
    "Impian tanpa tindakan hanyalah angan-angan.",
    "Jadilah cahaya di tengah kegelapan.",
    "Kamu adalah arsitek dari takdirmu sendiri.",
    "Keberhasilan sejati adalah membantu orang lain berhasil.",
    "Jangan biarkan suara keraguan mengalahkan suara harapan.",
    "Kreativitas lahir dari keberanian untuk berbeda.",
    "Yang membedakan pemenang dan pecundang hanyalah kemauan.",
    "Hidup singkat, buat setiap detiknya layak dikenang.",
    "Kepercayaan diri adalah modal utama meraih sukses.",
    "Kamu tidak bisa kembali ke awal, tapi bisa mulai dari sini.",
    "Jadikan kritik sebagai bahan bakar, bukan racun.",
    "Setiap matahari terbit membawa kesempatan baru.",
    "Kesederhanaan adalah keanggunan sejati.",
    "Orang yang tidak pernah salah adalah orang yang tidak pernah mencoba.",
    "Pikiran positif menghasilkan energi positif.",
    "Jangan takut berbeda, jadilah unik.",
    "Kerendahan hati adalah mahkota orang yang bijak.",
    "Bertumbuh itu menyakitkan, tapi tidak bertumbuh lebih menyakitkan.",
    "Doa tanpa usaha adalah omong kosong, usaha tanpa doa adalah kesombongan.",
    "Yang kamu tanam hari ini akan kamu panen esok hari.",
    "Jadilah orang yang kamu butuhkan saat kamu kecil.",
    "Hidup bukan tentang menghindari badai, tapi belajar menari di tengah hujan.",
    "Keikhlasan adalah kunci ketenangan jiwa.",
    "Jangan takut bermimpi, takutlah tidak berani mewujudkannya.",
    "Setiap kesulitan pasti ada kemudahan.",
    "Waktu adalah investasi paling berharga.",
    "Jangan biarkan orang lain mendefinisikan siapa dirimu.",
    "Kamu bisa mengubah arah angin, tapi kamu bisa mengatur layarmu.",
    "Ribuan kegagalan adalah tangga menuju satu kesuksesan.",
    "Jadilah produktif, bukan sekedar sibuk.",
    "Hargai prosesnya, bukan hanya hasilnya.",
    "Diam bukan berarti lemah, kadang diam adalah strategi.",
    "Jangan tunda kebaikan, lakukan sekarang.",
    "Yang membuat kamu berbeda adalah kekuatanmu, bukan kelemahanmu.",
    "Kesehatan adalah investasi terbaik.",
    "Bukan tentang seberapa keras kamu jatuh, tapi seberapa cepat kamu bangkit.",
    "Jadikan pengalaman buruk sebagai pelajaran terbaik.",
    "Fokus pada apa yang bisa kamu kendalikan.",
    "Berikan yang terbaik, sisanya biarkan Tuhan yang mengurus.",
    "Keberanian adalah otot, semakin sering dilatih semakin kuat.",
    "Satu buku bisa mengubah hidupmu.",
    "Jangan remehkan kekuatan niat yang tulus.",
    "Setiap orang adalah guru, setiap tempat adalah sekolah.",
    "Hidup itu singkat, jangan habiskan untuk hal yang tidak bermakna.",
    "Kepedulianmu kepada orang lain adalah cerminan hatimu.",
    "Jadilah versi terbaik dirimu, bukan tiruan terbaik orang lain.",
    "Kamu tidak perlu izin siapapun untuk menjadi dirimu sendiri.",
    "Semangat pagi adalah bensin untuk hari yang produktif.",
    "Percayalah, semua akan indah pada waktunya.",
    "Jangan berhenti belajar karena hidup tidak pernah berhenti mengajar.",
    "Ketulusan hati adalah harta yang tidak ternilai.",
    "Jadikan hidupmu sebagai inspirasi, bukan sensasi.",
    "Yang penting bukan seberapa lama kamu hidup, tapi seberapa bermakna hidupmu.",
    "Teruslah berjalan meski jalannya terjal, karena pemandangan terbaik ada di puncak.",
    "Jangan biarkan masa lalu mencuri masa depanmu.",
    "Kamu adalah keajaiban yang sedang berjalan.",
]

# ═══════════════════════════════════════════════════════
#  BOT INIT
# ═══════════════════════════════════════════════════════
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)
active_voice_rooms = {}

# ═══════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════
def is_admin(member: discord.Member):
    if member.id == OWNER_ID:
        return True
    return member.guild_permissions.administrator or member.guild_permissions.manage_guild

def is_game_channel(ctx) -> bool:
    """Cek apakah command dijalankan di channel game yang diizinkan (SPAM_CHANNEL_ID) atau oleh owner."""
    if ctx.author.id == OWNER_ID:
        return True
    if isinstance(ctx.channel, discord.DMChannel):
        return False
    return ctx.channel.id == SPAM_CHANNEL_ID

def game_channel_msg(ctx):
    return f"⚠️ {ctx.author.mention} Command ini hanya bisa digunakan di <#{SPAM_CHANNEL_ID}>!"

def load_json(path, default=None):
    if default is None:
        default = {}
    if not os.path.exists(path):
        return default
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def load_data():         return load_json(DATA_FILE)
def save_data(d):        save_json(DATA_FILE, d)
def load_last_tiktok():  return load_json(LAST_TIKTOK_FILE)
def save_last_tiktok(d): save_json(LAST_TIKTOK_FILE, d)
def load_youtube():      return load_json(YOUTUBE_FILE)
def save_youtube(d):     save_json(YOUTUBE_FILE, d)
def load_tickets():      return load_json(TICKET_FILE)
def save_tickets(d):     save_json(TICKET_FILE, d)
def load_verif():        return load_json(VERIF_FILE)
def save_verif(d):       save_json(VERIF_FILE, d)
def load_warns():        return load_json(WARN_FILE)
def save_warns(d):       save_json(WARN_FILE, d)
def load_giveaways():    return load_json(GIVEAWAY_FILE)
def save_giveaways(d):   save_json(GIVEAWAY_FILE, d)
def load_settings():     return load_json(SETTINGS_FILE)
def save_settings(d):    save_json(SETTINGS_FILE, d)
def load_afk():          return load_json(AFK_FILE)
def save_afk(d):         save_json(AFK_FILE, d)
def load_banners():      return load_json(BANNER_FILE)
def save_banners(d):     save_json(BANNER_FILE, d)

def load_quotes():
    q = load_json(QUOTE_FILE, default=[])
    if not q:
        save_json(QUOTE_FILE, DEFAULT_QUOTES)
        return DEFAULT_QUOTES
    return q

def get_level(xp):
    current_level = 1
    for lvl in sorted(LEVEL_CONFIG.keys(), reverse=True):
        if xp >= LEVEL_CONFIG[lvl]["xp_required"]:
            current_level = lvl
            break
    return current_level

def get_xp_for_next_level(level):
    next_level = level + 1
    if next_level > max(LEVEL_CONFIG.keys()):
        return None
    return LEVEL_CONFIG[next_level]["xp_required"]

# ═══════════════════════════════════════════════════════
#  BANNER GENERATOR — Anime Style
# ═══════════════════════════════════════════════════════
RARITY_ORDER = ["Common", "Uncommon", "Rare", "Epic", "Legendary"]

def assign_banner(user_id: int, level: int) -> dict:
    """Tentukan rarity banner berdasarkan level, lalu generate seed unik per user."""
    banners = load_banners()
    uid = str(user_id)

    # Jika sudah punya banner dan belum level up, return yang ada
    if uid in banners:
        stored = banners[uid]
        current_rarity_idx = RARITY_ORDER.index(stored["rarity"])
        # Upgrade banner jika level naik ke threshold baru
        new_rarity = get_rarity_for_level(level)
        new_rarity_idx = RARITY_ORDER.index(new_rarity)
        if new_rarity_idx > current_rarity_idx:
            stored["rarity"] = new_rarity
            stored["rarity_color"] = BANNER_RARITY[new_rarity]["color"]
            banners[uid] = stored
            save_banners(banners)
        return banners[uid]

    # Banner baru — seed unik dari user_id
    rarity = get_rarity_for_level(level)
    seed = user_id % 1000  # 0-999 untuk variasi warna
    banners[uid] = {
        "rarity": rarity,
        "rarity_color": BANNER_RARITY[rarity]["color"],
        "seed": seed,
        "theme": seed % 8,  # 8 tema anime berbeda
    }
    save_banners(banners)
    return banners[uid]

def get_rarity_for_level(level: int) -> str:
    if level >= 5:
        return random.choices(
            ["Legendary", "Epic", "Rare"],
            weights=[20, 50, 30]
        )[0]
    elif level >= 4:
        return random.choices(
            ["Epic", "Rare", "Uncommon"],
            weights=[25, 45, 30]
        )[0]
    elif level >= 3:
        return random.choices(
            ["Rare", "Uncommon", "Common"],
            weights=[20, 50, 30]
        )[0]
    elif level >= 2:
        return random.choices(
            ["Uncommon", "Common"],
            weights=[35, 65]
        )[0]
    else:
        return "Common"

def draw_anime_banner(draw, W, H, theme: int, seed: int, rarity: str):
    """Generate banner anime-style berdasarkan tema dan seed."""
    random.seed(seed)
    rc = BANNER_RARITY[rarity]["color"]

    themes = {
        0: draw_theme_sakura,
        1: draw_theme_galaxy,
        2: draw_theme_cyber,
        3: draw_theme_ocean,
        4: draw_theme_fire,
        5: draw_theme_forest,
        6: draw_theme_moonlight,
        7: draw_theme_aurora,
    }
    fn = themes.get(theme % 8, draw_theme_galaxy)
    fn(draw, W, H, rc, seed)

def draw_theme_sakura(draw, W, H, rc, seed):
    random.seed(seed)
    # Gradient pink-putih
    for y in range(H):
        r = int(255 - (y/H)*60)
        g = int(180 - (y/H)*80)
        b = int(200 - (y/H)*50)
        draw.line([(0,y),(W,y)], fill=(r,g,b))
    # Bunga sakura
    for _ in range(18):
        x, y = random.randint(0,W), random.randint(0,H)
        size = random.randint(6,18)
        for petal in range(5):
            angle = petal * 72
            px = x + int(size * math.cos(math.radians(angle)))
            py = y + int(size * math.sin(math.radians(angle)))
            draw.ellipse([px-size//3, py-size//3, px+size//3, py+size//3],
                         fill=(255, 180+random.randint(-20,20), 200, 180))
    # Kelopak jatuh
    for _ in range(30):
        x,y = random.randint(0,W), random.randint(0,H)
        draw.ellipse([x,y,x+5,y+8], fill=(255,200,210))

def draw_theme_galaxy(draw, W, H, rc, seed):
    random.seed(seed)
    # Gradient gelap ungu-biru
    for y in range(H):
        r = int(10 + (y/H)*30)
        g = int(5 + (y/H)*20)
        b = int(40 + (y/H)*60)
        draw.line([(0,y),(W,y)], fill=(r,g,b))
    # Bintang
    for _ in range(80):
        x,y = random.randint(0,W), random.randint(0,H)
        s = random.choice([1,1,1,2,3])
        br = random.randint(180,255)
        draw.ellipse([x,y,x+s,y+s], fill=(br,br,br))
    # Nebula warna
    for _ in range(6):
        x,y = random.randint(0,W), random.randint(0,H)
        r2 = random.randint(30,80)
        col = (random.randint(80,180), random.randint(40,120), random.randint(150,255), 60)
        for dr in range(r2,0,-5):
            alpha = int(80*(1-dr/r2))
            draw.ellipse([x-dr,y-dr,x+dr,y+dr],
                         fill=(col[0],col[1],col[2]))

def draw_theme_cyber(draw, W, H, rc, seed):
    random.seed(seed)
    # Latar hitam
    draw.rectangle([0,0,W,H], fill=(5,5,15))
    # Grid
    for x in range(0,W,30):
        draw.line([(x,0),(x,H)], fill=(0,80,120,40), width=1)
    for y in range(0,H,20):
        draw.line([(0,y),(W,y)], fill=(0,80,120,40), width=1)
    # Garis neon
    for _ in range(8):
        x1,y1 = random.randint(0,W), random.randint(0,H)
        x2,y2 = random.randint(0,W), random.randint(0,H)
        col = random.choice([(0,255,200),(255,0,128),(0,180,255),(200,0,255)])
        draw.line([(x1,y1),(x2,y2)], fill=col, width=2)
    # Hexagon
    for _ in range(5):
        cx,cy = random.randint(20,W-20), random.randint(10,H-10)
        r2 = random.randint(15,35)
        pts = [(cx+int(r2*math.cos(math.radians(60*i))),
                cy+int(r2*math.sin(math.radians(60*i)))) for i in range(6)]
        draw.polygon(pts, outline=(0,255,200), fill=None)

def draw_theme_ocean(draw, W, H, rc, seed):
    random.seed(seed)
    for y in range(H):
        r = int(0 + (y/H)*20)
        g = int(80 + (y/H)*60)
        b = int(150 + (y/H)*80)
        draw.line([(0,y),(W,y)], fill=(r,g,b))
    # Gelombang
    for wave in range(5):
        pts = []
        offset = random.randint(0,30)
        for x in range(0,W+1,5):
            y2 = int(H*0.3 + wave*25 + 15*math.sin((x+offset*wave)/30))
            pts.append((x,y2))
        pts += [(W,H),(0,H)]
        alpha_col = (0,100+wave*15,180+wave*10)
        draw.polygon(pts, fill=alpha_col)
    # Gelembung
    for _ in range(20):
        x,y = random.randint(0,W), random.randint(0,H)
        r2 = random.randint(3,12)
        draw.ellipse([x-r2,y-r2,x+r2,y+r2], outline=(180,230,255), width=1)

def draw_theme_fire(draw, W, H, rc, seed):
    random.seed(seed)
    for y in range(H):
        r = min(255,int(150+(y/H)*100))
        g = int(50*(1-y/H))
        b = 0
        draw.line([(0,y),(W,y)], fill=(r,g,b))
    # Lidah api
    for _ in range(12):
        cx = random.randint(0,W)
        h2 = random.randint(H//4, H)
        w2 = random.randint(10,40)
        pts = [(cx-w2,H),(cx+w2,H),(cx+w2//3,H-h2),(cx-w2//3,H-h2)]
        col = random.choice([(255,200,0),(255,120,0),(255,60,0)])
        draw.polygon(pts, fill=col)
    # Percikan
    for _ in range(40):
        x,y = random.randint(0,W), random.randint(0,H)
        draw.ellipse([x,y,x+3,y+3], fill=(255,220,100))

def draw_theme_forest(draw, W, H, rc, seed):
    random.seed(seed)
    for y in range(H):
        r = int(20+(y/H)*30)
        g = int(60+(y/H)*80)
        b = int(20+(y/H)*20)
        draw.line([(0,y),(W,y)], fill=(r,g,b))
    # Pohon
    for _ in range(8):
        cx = random.randint(0,W)
        h2 = random.randint(40,H)
        w2 = random.randint(20,50)
        # Batang
        draw.rectangle([cx-5,H-h2//2,cx+5,H], fill=(80,50,20))
        # Daun
        for layer in range(3):
            lh = h2-layer*15
            lw = w2-layer*8
            pts = [(cx,H-h2-layer*20),(cx-lw,H-lh//2),(cx+lw,H-lh//2)]
            col = (random.randint(30,80),random.randint(120,180),random.randint(30,70))
            draw.polygon(pts, fill=col)
    # Kunang-kunang
    for _ in range(20):
        x,y = random.randint(0,W), random.randint(0,H//2)
        draw.ellipse([x,y,x+4,y+4], fill=(220,255,100))

def draw_theme_moonlight(draw, W, H, rc, seed):
    random.seed(seed)
    for y in range(H):
        r = int(10+(y/H)*20)
        g = int(10+(y/H)*20)
        b = int(40+(y/H)*60)
        draw.line([(0,y),(W,y)], fill=(r,g,b))
    # Bulan
    draw.ellipse([W-80,5,W-20,55], fill=(255,250,200))
    draw.ellipse([W-65,5,W-10,55], fill=(20,20,60))
    # Bintang
    for _ in range(60):
        x,y = random.randint(0,W), random.randint(0,H*2//3)
        s = random.choice([1,1,2])
        br = random.randint(150,255)
        draw.ellipse([x,y,x+s,y+s], fill=(br,br,br))
    # Pantulan di air
    for i in range(3):
        y2 = H-10-i*8
        draw.line([(W//2-30+i*5,y2),(W//2+30-i*5,y2)], fill=(255,250,150), width=2)

def draw_theme_aurora(draw, W, H, rc, seed):
    random.seed(seed)
    for y in range(H):
        r = int(5+(y/H)*15)
        g = int(10+(y/H)*30)
        b = int(30+(y/H)*50)
        draw.line([(0,y),(W,y)], fill=(r,g,b))
    # Aurora curtain
    colors = [(0,255,150),(0,200,255),(150,0,255),(255,100,200)]
    for i, col in enumerate(colors):
        for x in range(0,W,4):
            wave_h = int(H*0.5 + 40*math.sin((x/W*4*math.pi)+i))
            draw.line([(x,0),(x,wave_h)],
                      fill=(col[0],col[1],col[2]), width=3)
    # Bintang
    for _ in range(50):
        x,y = random.randint(0,W), random.randint(0,H//2)
        br = random.randint(150,255)
        draw.ellipse([x,y,x+2,y+2], fill=(br,br,br))

# ═══════════════════════════════════════════════════════
#  RANK CARD GENERATOR — Diperbaiki
# ═══════════════════════════════════════════════════════
def create_rank_card(username, avatar_bytes, xp, level, user_id):
    W, H = 760, 220
    card = Image.new("RGBA", (W, H), (0,0,0,255))
    draw = ImageDraw.Draw(card)

    # Banner
    banner_data = assign_banner(user_id, level)
    theme = banner_data.get("theme", 0)
    seed  = banner_data.get("seed", 0)
    rarity = banner_data.get("rarity", "Common")
    draw_anime_banner(draw, W, H, theme, seed, rarity)

    # Overlay gelap semi-transparan bawah
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    ov_draw = ImageDraw.Draw(overlay)
    ov_draw.rectangle([0, H//2, W, H], fill=(0,0,0,160))
    card = Image.alpha_composite(card, overlay)
    draw = ImageDraw.Draw(card)

    level_color = LEVEL_CONFIG[level]["color"]
    rc = BANNER_RARITY[rarity]["color"]

    # Avatar
    avatar_size = 110
    av_x, av_y = 20, H//2 - avatar_size//2
    try:
        av_img = Image.open(io.BytesIO(avatar_bytes)).resize((avatar_size, avatar_size)).convert("RGBA")
        mask = Image.new("L", (avatar_size, avatar_size), 0)
        ImageDraw.Draw(mask).ellipse((0,0,avatar_size,avatar_size), fill=255)
        av_img.putalpha(mask)
        # Border avatar
        border_size = avatar_size + 6
        border_img = Image.new("RGBA", (border_size, border_size), (0,0,0,0))
        ImageDraw.Draw(border_img).ellipse((0,0,border_size,border_size), fill=(*rc,255))
        card.paste(border_img, (av_x-3, av_y-3), border_img)
        card.paste(av_img, (av_x, av_y), av_img)
    except Exception:
        draw.ellipse([av_x,av_y,av_x+avatar_size,av_y+avatar_size], fill=(60,60,80))

    # Font
    try:
        font_name  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        font_level = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
        font_xp    = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
    except Exception:
        font_name = font_level = font_small = font_xp = ImageFont.load_default()

    tx = av_x + avatar_size + 18
    ty = H//2 - 10

    # Username
    draw.text((tx, ty - 50), username[:20], fill=(255,255,255), font=font_name)

    # Level badge
    badge_text = f"LV.{level}"
    badge_w = 60
    draw.rounded_rectangle([tx, ty-20, tx+badge_w, ty+4], radius=8, fill=(*level_color,220))
    draw.text((tx+8, ty-18), badge_text, fill=(255,255,255), font=font_level)

    # Level name
    draw.text((tx+badge_w+10, ty-18), LEVEL_CONFIG[level]['name'], fill=(*level_color,), font=font_level)

    # Rarity badge
    rarity_colors = {
        "Common": (150,150,150), "Uncommon": (80,200,80),
        "Rare": (80,120,255), "Epic": (180,80,255), "Legendary": (255,200,0)
    }
    rc2 = rarity_colors.get(rarity, (150,150,150))
    draw.rounded_rectangle([tx, ty+10, tx+100, ty+30], radius=6, fill=(*rc2,200))
    draw.text((tx+6, ty+12), f"✦ {rarity}", fill=(255,255,255), font=font_xp)

    # XP bar
    bar_x = tx
    bar_y = ty + 40
    bar_w = W - tx - 20
    bar_h = 16

    next_xp = get_xp_for_next_level(level)
    progress = min(xp / next_xp, 1.0) if next_xp else 1.0
    xp_text = f"{xp} / {next_xp} XP" if next_xp else f"{xp} XP  ✦ MAX"

    # Bar background
    draw.rounded_rectangle([bar_x, bar_y, bar_x+bar_w, bar_y+bar_h], radius=8, fill=(40,40,60))
    # Bar fill
    fill_w = max(int(bar_w * progress), 0)
    if fill_w > 0:
        # Gradient bar
        for i in range(fill_w):
            t = i / max(fill_w,1)
            r2 = int(level_color[0]*0.6 + level_color[0]*0.4*t)
            g2 = int(level_color[1]*0.6 + level_color[1]*0.4*t)
            b2 = int(level_color[2]*0.6 + level_color[2]*0.4*t)
            draw.line([(bar_x+i, bar_y+1),(bar_x+i, bar_y+bar_h-1)], fill=(r2,g2,b2))
        # Shine
        draw.rounded_rectangle([bar_x, bar_y, bar_x+fill_w, bar_y+bar_h//2], radius=6, fill=(255,255,255,40))

    # XP text di dalam bar
    draw.text((bar_x+5, bar_y+1), xp_text, fill=(220,220,220), font=font_xp)

    # Footer
    draw.text((W-160, H-20), "✦ Asisten Lurah BFL", fill=(200,200,200,180), font=font_xp)

    buf = io.BytesIO()
    card.save(buf, format="PNG")
    buf.seek(0)
    return buf

# ═══════════════════════════════════════════════════════
#  VERIF VIEW
# ═══════════════════════════════════════════════════════
class VerifView(View):
    def __init__(self, applicant_id: int, guild_id: int):
        super().__init__(timeout=None)
        self.applicant_id = applicant_id
        self.guild_id     = guild_id
        self.chosen_role  = None

    @discord.ui.select(
        placeholder="Pilih role yang akan diberikan...",
        options=[
            discord.SelectOption(label="Moderator", value="Moderator", emoji="🛡️"),
            discord.SelectOption(label="Stream",    value="Stream",    emoji="🎥"),
            discord.SelectOption(label="Clipper",   value="Clipper",   emoji="✂️"),
        ]
    )
    async def select_role(self, interaction: discord.Interaction, select: Select):
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("❌ Hanya owner.", ephemeral=True)
            return
        self.chosen_role = select.values[0]
        await interaction.response.send_message(f"Role **{self.chosen_role}** dipilih. Klik ACC.", ephemeral=True)

    @discord.ui.button(label="✅ ACC", style=discord.ButtonStyle.success)
    async def acc_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("❌ Hanya owner.", ephemeral=True)
            return
        if not self.chosen_role:
            await interaction.response.send_message("⚠️ Pilih role dulu.", ephemeral=True)
            return
        guild = bot.get_guild(self.guild_id)
        if not guild:
            await interaction.response.send_message("❌ Server tidak ditemukan.", ephemeral=True)
            return
        try:
            member = guild.get_member(self.applicant_id) or await guild.fetch_member(self.applicant_id)
        except Exception:
            await interaction.response.send_message("❌ Member tidak ditemukan.", ephemeral=True)
            return
        role = discord.utils.get(guild.roles, name=self.chosen_role)
        if not role:
            await interaction.response.send_message(f"❌ Role **{self.chosen_role}** tidak ada.", ephemeral=True)
            return
        await member.add_roles(role)
        try:
            await member.send(f"🎉 Verifikasi **disetujui**! Role **{self.chosen_role}** telah diberikan.")
        except Exception:
            pass
        await interaction.response.edit_message(
            content=f"✅ Role **{self.chosen_role}** → **{member.display_name}**.", view=None)
        verif = load_verif()
        verif.pop(str(self.applicant_id), None)
        save_verif(verif)

    @discord.ui.button(label="❌ REJECT", style=discord.ButtonStyle.danger)
    async def reject_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("❌ Hanya owner.", ephemeral=True)
            return
        guild  = bot.get_guild(self.guild_id)
        member = None
        if guild:
            try:
                member = guild.get_member(self.applicant_id) or await guild.fetch_member(self.applicant_id)
            except Exception:
                pass
        if member:
            try:
                await member.send("❌ Verifikasi **ditolak**. Coba lagi dengan bukti lebih jelas.")
            except Exception:
                pass
        name = member.display_name if member else str(self.applicant_id)
        await interaction.response.edit_message(content=f"❌ Verifikasi **{name}** ditolak.", view=None)
        verif = load_verif()
        verif.pop(str(self.applicant_id), None)
        save_verif(verif)

# ═══════════════════════════════════════════════════════
#  TICKET VIEW
# ═══════════════════════════════════════════════════════
class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="📩 Buat Laporan / Diskusi", style=discord.ButtonStyle.primary, custom_id="buat_ticket")
    async def buat_ticket(self, interaction: discord.Interaction, button: Button):
        guild   = interaction.guild
        member  = interaction.user
        tickets = load_tickets()

        for tid, tdata in tickets.items():
            if tdata["user_id"] == member.id and tdata["status"] == "open":
                await interaction.response.send_message(f"⚠️ Ticket aktif: <#{tid}>", ephemeral=True)
                return

        await interaction.response.defer(ephemeral=True)
        try:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            }
            for role in guild.roles:
                if role.permissions.administrator or role.permissions.manage_guild:
                    overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

            ticket_channel = await guild.create_text_channel(
                name=f"ticket-{member.display_name}", overwrites=overwrites,
                reason=f"Ticket oleh {member}"
            )
            tickets[str(ticket_channel.id)] = {
                "user_id": member.id, "status": "open",
                "created_at": str(datetime.datetime.utcnow())
            }
            save_tickets(tickets)

            embed = discord.Embed(
                title="📩 Ticket Dibuat",
                description=(
                    f"Halo {member.mention}!\n\n"
                    "Jelaskan laporan atau pertanyaan kamu.\n"
                    "Admin akan segera merespons.\n\n"
                    "Klik **Tutup Ticket** jika sudah selesai."
                ),
                color=discord.Color.blue(),
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_footer(text="Asisten Lurah BFL • Ticket System")
            await ticket_channel.send(content=f"{member.mention}", embed=embed,
                                       view=CloseTicketView(ticket_channel.id))
            await interaction.followup.send(f"✅ Ticket: {ticket_channel.mention}", ephemeral=True)
        except discord.Forbidden:
            await interaction.followup.send("❌ Bot tidak punya izin Manage Channels.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Error: `{e}`", ephemeral=True)

class CloseTicketView(View):
    def __init__(self, channel_id: int):
        super().__init__(timeout=None)
        self.channel_id = channel_id

    @discord.ui.button(label="🔒 Tutup Ticket", style=discord.ButtonStyle.danger, custom_id="tutup_ticket_v2")
    async def tutup_ticket(self, interaction: discord.Interaction, button: Button):
        member  = interaction.user
        tickets = load_tickets()
        tdata   = tickets.get(str(self.channel_id))
        if not tdata:
            await interaction.response.send_message("⚠️ Data tidak ditemukan.", ephemeral=True)
            return
        if member.id != tdata["user_id"] and not is_admin(member):
            await interaction.response.send_message("❌ Hanya pembuat ticket atau admin.", ephemeral=True)
            return
        await interaction.response.defer()
        await interaction.followup.send("🔒 Menutup ticket dalam 5 detik...")
        await asyncio.sleep(5)
        tickets[str(self.channel_id)]["status"] = "closed"
        save_tickets(tickets)
        channel = bot.get_channel(self.channel_id)
        if channel:
            try:
                await channel.delete(reason="Ticket ditutup")
            except Exception:
                pass

# ═══════════════════════════════════════════════════════
#  GIVEAWAY VIEW
# ═══════════════════════════════════════════════════════
class GiveawayView(View):
    def __init__(self, giveaway_id: str):
        super().__init__(timeout=None)
        self.giveaway_id = giveaway_id

    @discord.ui.button(label="🎉 Ikut Giveaway", style=discord.ButtonStyle.success,
                       custom_id="join_giveaway")
    async def join_giveaway(self, interaction: discord.Interaction, button: Button):
        giveaways = load_giveaways()
        gw = giveaways.get(self.giveaway_id)
        if not gw:
            await interaction.response.send_message("❌ Giveaway tidak ditemukan.", ephemeral=True)
            return
        if gw.get("ended"):
            await interaction.response.send_message("❌ Giveaway sudah berakhir.", ephemeral=True)
            return
        uid = str(interaction.user.id)
        if uid in gw["entries"]:
            # Toggle keluar
            gw["entries"].remove(uid)
            save_giveaways(giveaways)
            await interaction.response.send_message(
                "✅ Kamu keluar dari giveaway.", ephemeral=True)
        else:
            gw["entries"].append(uid)
            save_giveaways(giveaways)
            await interaction.response.send_message(
                f"🎉 Kamu sudah terdaftar! Total peserta: **{len(gw['entries'])}**", ephemeral=True)

        # Update embed
        try:
            ch = bot.get_channel(int(gw["channel_id"]))
            msg = await ch.fetch_message(int(gw["message_id"]))
            new_embed = build_giveaway_embed(gw)
            await msg.edit(embed=new_embed)
        except Exception:
            pass

def build_giveaway_embed(gw: dict) -> discord.Embed:
    end_dt = datetime.datetime.fromisoformat(gw["end_time"])
    now    = datetime.datetime.utcnow()
    sisa   = end_dt - now
    if sisa.total_seconds() > 0:
        h, rem = divmod(int(sisa.total_seconds()), 3600)
        m, s   = divmod(rem, 60)
        sisa_str = f"{h}j {m}m {s}d"
    else:
        sisa_str = "Selesai"

    embed = discord.Embed(
        title=f"🎉 GIVEAWAY — {gw['prize']}",
        description=(
            f"Klik tombol **🎉 Ikut Giveaway** untuk ikut!\n\n"
            f"👥 **Peserta:** {len(gw['entries'])} orang\n"
            f"⏰ **Berakhir dalam:** {sisa_str}\n"
            f"🏆 **Hadiah:** {gw['prize']}"
        ),
        color=discord.Color.gold(),
        timestamp=datetime.datetime.utcnow()
    )
    embed.set_footer(text="Asisten Lurah BFL • Giveaway System")
    return embed

# ═══════════════════════════════════════════════════════
#  EVENTS
# ═══════════════════════════════════════════════════════
@bot.event
async def on_ready():
    print(f"✅ {bot.user} online!")
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="Desa BFL 🏘️")
    )
    bot.add_view(TicketView())
    tickets = load_tickets()
    for channel_id, tdata in tickets.items():
        if tdata.get("status") == "open":
            bot.add_view(CloseTicketView(int(channel_id)))
    # Register giveaway views
    giveaways = load_giveaways()
    for gid, gw in giveaways.items():
        if not gw.get("ended"):
            bot.add_view(GiveawayView(gid))

    check_tiktok.start()
    check_giveaways.start()
    print("✅ Semua sistem aktif.")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # ── AFK check ──
    if not isinstance(message.channel, discord.DMChannel):
        afk_data = load_afk()
        uid = str(message.author.id)
        # Hapus AFK jika yang kirim pesan sendiri
        if uid in afk_data:
            del afk_data[uid]
            save_afk(afk_data)
            await message.channel.send(
                f"👋 {message.author.mention} selamat datang kembali! Status AFK dihapus.",
                delete_after=8
            )
        # Cek mention ke user AFK
        for mentioned in message.mentions:
            mid = str(mentioned.id)
            if mid in afk_data:
                alasan = afk_data[mid].get("reason", "Tidak ada alasan")
                await message.channel.send(
                    f"💤 **{mentioned.display_name}** sedang offline — {alasan}",
                    delete_after=10
                )

    # ── Verifikasi via DM ──
    if isinstance(message.channel, discord.DMChannel) and message.author.id != OWNER_ID:
        if message.attachments:
            verif = load_verif()
            uid   = str(message.author.id)
            if uid in verif:
                await message.channel.send("⏳ Verifikasi sedang diproses.")
                return
            verif[uid] = {"status": "pending"}
            save_verif(verif)
            owner = await bot.fetch_user(OWNER_ID)
            embed = discord.Embed(
                title="📋 Verifikasi Masuk",
                description=(
                    f"**User:** {message.author} (`{message.author.id}`)\n"
                    f"**Name:** {message.author.display_name}\n\n"
                    "Pilih role lalu ACC/REJECT."
                ),
                color=discord.Color.orange(),
                timestamp=datetime.datetime.utcnow()
            )
            guild_id = None
            for g in bot.guilds:
                if g.get_member(message.author.id):
                    guild_id = g.id
                    break
            files = [await att.to_file() for att in message.attachments
                     if att.content_type and att.content_type.startswith("image")]
            if guild_id:
                await owner.send(embed=embed, files=files,
                                 view=VerifView(message.author.id, guild_id))
                await message.channel.send("✅ Bukti dikirim ke admin. Tunggu konfirmasi!")
            else:
                await message.channel.send("❌ Bergabung ke server terlebih dahulu.")
            return
        await bot.process_commands(message)
        return

    # ── XP System ──
    data = load_data()
    uid  = str(message.author.id)
    if uid not in data:
        data[uid] = {"xp": 0, "level": 1}
    old_level        = data[uid]["level"]
    data[uid]["xp"] += XP_PER_MESSAGE
    new_level        = get_level(data[uid]["xp"])
    data[uid]["level"] = new_level
    save_data(data)
    if new_level > old_level:
        banner_data = assign_banner(message.author.id, new_level)
        embed = discord.Embed(
            title="🎉 LEVEL UP!",
            description=(
                f"{message.author.mention} naik ke **Level {new_level} — {LEVEL_CONFIG[new_level]['name']}**!\n"
                f"Banner diupgrade ke **{banner_data['rarity']}** ✦"
            ),
            color=discord.Color.from_rgb(*LEVEL_CONFIG[new_level]["color"])
        )
        await message.channel.send(embed=embed)
    await bot.process_commands(message)

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel and before.channel.id in active_voice_rooms:
        if len(before.channel.members) == 0:
            try:
                await before.channel.delete(reason="Voice room kosong.")
            except Exception:
                pass
            active_voice_rooms.pop(before.channel.id, None)

# ═══════════════════════════════════════════════════════
#  TASKS — GIVEAWAY CHECKER
# ═══════════════════════════════════════════════════════
@tasks.loop(seconds=30)
async def check_giveaways():
    giveaways = load_giveaways()
    changed   = False
    for gid, gw in giveaways.items():
        if gw.get("ended"):
            continue
        end_dt = datetime.datetime.fromisoformat(gw["end_time"])
        if datetime.datetime.utcnow() >= end_dt:
            gw["ended"] = True
            changed = True
            ch = bot.get_channel(int(gw["channel_id"]))
            if not ch:
                continue
            entries = gw.get("entries", [])
            if not entries:
                await ch.send(f"🎉 Giveaway **{gw['prize']}** berakhir — tidak ada peserta.")
                continue
            winner_id = int(random.choice(entries))
            try:
                winner = await bot.fetch_user(winner_id)
            except Exception:
                winner = None
            # Update embed
            try:
                msg = await ch.fetch_message(int(gw["message_id"]))
                embed = discord.Embed(
                    title=f"🏆 GIVEAWAY SELESAI — {gw['prize']}",
                    description=(
                        f"🎊 Pemenang: {winner.mention if winner else winner_id}\n"
                        f"👥 Total peserta: {len(entries)}"
                    ),
                    color=discord.Color.green()
                )
                embed.set_footer(text="Asisten Lurah BFL • Giveaway Selesai")
                await msg.edit(embed=embed, view=None)
            except Exception:
                pass
            # Announce
            await ch.send(
                f"🎊 Selamat {winner.mention if winner else winner_id}! "
                f"Kamu menang giveaway **{gw['prize']}**!"
            )
            # DM winner
            if winner:
                try:
                    dm_embed = discord.Embed(
                        title="🏆 Kamu Menang Giveaway!",
                        description=(
                            f"Selamat! Kamu memenangkan **{gw['prize']}**!\n\n"
                            f"👥 Total peserta: **{len(entries)}** orang\n"
                            "Hubungi admin untuk mengklaim hadiahmu."
                        ),
                        color=discord.Color.gold()
                    )
                    dm_embed.set_footer(text="Asisten Lurah BFL • Giveaway")
                    await winner.send(embed=dm_embed)
                except Exception:
                    pass
    if changed:
        save_giveaways(giveaways)

@check_giveaways.before_loop
async def before_check_giveaways():
    await bot.wait_until_ready()


# ═══════════════════════════════════════════════════════
#  TASKS — TIKTOK
# ═══════════════════════════════════════════════════════
@tasks.loop(minutes=5)
async def check_tiktok():
    channel = bot.get_channel(TIKTOK_CHECK_CHANNEL_ID)
    if not channel:
        return
    try:
        last_data = load_last_tiktok()
        url       = f"https://www.tiktok.com/@{TIKTOK_USERNAME}"
        headers   = {"User-Agent": "Mozilla/5.0"}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                html = await resp.text()
        matches = re.findall(r'"id":"(\d+)"', html)
        if not matches:
            return
        latest_id = matches[0]
        if last_data.get("last_id") == latest_id:
            return
        save_last_tiktok({"last_id": latest_id})
        tiktok_url = f"https://www.tiktok.com/@{TIKTOK_USERNAME}/video/{latest_id}"
        embed = discord.Embed(
            title=f"🎵 @{TIKTOK_USERNAME} baru posting di TikTok!",
            description=f"👇\n{tiktok_url}",
            color=discord.Color.from_rgb(254, 44, 85),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_footer(text="Asisten Lurah BFL • TikTok Tracker")
        await channel.send(embed=embed)
    except Exception as e:
        print(f"[TikTok] {e}")

@check_tiktok.before_loop
async def before_tiktok():
    await bot.wait_until_ready()

# ═══════════════════════════════════════════════════════
#  COMMANDS — RANK & LEADERBOARD
# ═══════════════════════════════════════════════════════
@bot.command(name="rank")
async def rank(ctx, member: discord.Member = None):
    if ctx.author.id != OWNER_ID and ctx.channel.id != SPAM_CHANNEL_ID:
        await ctx.send(f"⚠️ Hanya di <#{SPAM_CHANNEL_ID}>!", delete_after=5)
        return
    member = member or ctx.author
    data   = load_data()
    uid    = str(member.id)
    if uid not in data:
        data[uid] = {"xp": 0, "level": 1}
        save_data(data)
    xp    = data[uid]["xp"]
    level = data[uid]["level"]
    try:
        avatar_bytes = requests.get(member.display_avatar.url).content
    except Exception:
        avatar_bytes = b""
    card_buf = create_rank_card(str(member.display_name), avatar_bytes, xp, level, member.id)
    await ctx.send(file=discord.File(fp=card_buf, filename="rank.png"))

@bot.command(name="leaderboard", aliases=["lb", "top"])
async def leaderboard(ctx):
    if ctx.author.id != OWNER_ID and ctx.channel.id != SPAM_CHANNEL_ID:
        await ctx.send(f"⚠️ Hanya di <#{SPAM_CHANNEL_ID}>!", delete_after=5)
        return
    data         = load_data()
    sorted_users = sorted(data.items(), key=lambda x: x[1]["xp"], reverse=True)[:10]
    medals       = ["🥇","🥈","🥉"]
    embed = discord.Embed(title="🏆 Leaderboard XP — Asisten Lurah BFL", color=discord.Color.gold())
    for i, (uid, info) in enumerate(sorted_users):
        try:
            user = await bot.fetch_user(int(uid))
            name = user.display_name
        except Exception:
            name = f"User#{uid}"
        lvl   = info["level"]
        medal = medals[i] if i < 3 else f"#{i+1}"
        banners = load_banners()
        rarity  = banners.get(uid, {}).get("rarity", "Common")
        embed.add_field(
            name=f"{medal} {name}",
            value=f"Level {lvl} ({LEVEL_CONFIG[lvl]['name']}) · {info['xp']} XP · ✦ {rarity}",
            inline=False
        )
    await ctx.send(embed=embed)

# ═══════════════════════════════════════════════════════
#  COMMANDS — WARN
# ═══════════════════════════════════════════════════════
@bot.command(name="warn")
@commands.has_permissions(moderate_members=True)
async def warn(ctx, member: discord.Member, *, alasan="Tidak ada alasan"):
    if member.id == OWNER_ID:
        await ctx.send("❌ Tidak bisa warn owner.")
        return
    warns = load_warns()
    uid   = str(member.id)
    if uid not in warns:
        warns[uid] = []
    warns[uid].append({
        "alasan": alasan,
        "oleh": str(ctx.author.id),
        "waktu": str(datetime.datetime.utcnow())
    })
    total = len(warns[uid])
    save_warns(warns)

    embed = discord.Embed(
        title="⚠️ Peringatan Diberikan",
        color=discord.Color.orange()
    )
    embed.add_field(name="Member",  value=member.mention, inline=True)
    embed.add_field(name="Warn ke", value=f"**{total}/3**",  inline=True)
    embed.add_field(name="Alasan",  value=alasan, inline=False)
    embed.set_footer(text=f"Oleh: {ctx.author}")
    await ctx.send(embed=embed)

    # DM member
    try:
        await member.send(
            f"⚠️ Kamu mendapat peringatan di **{ctx.guild.name}**.\n"
            f"Alasan: **{alasan}**\n"
            f"Total warn: **{total}/3**"
        )
    except Exception:
        pass

    if total >= 3:
        await ctx.send(
            f"🚨 {member.mention} telah mendapat **3 peringatan** dan akan dikeluarkan dari server!"
        )
        try:
            await member.send(
                f"🚨 Kamu telah mendapat **3 peringatan** di **{ctx.guild.name}** "
                f"dan telah dikeluarkan dari server."
            )
        except Exception:
            pass
        await asyncio.sleep(2)
        await member.kick(reason="3x peringatan")
        # Reset warn
        warns[uid] = []
        save_warns(warns)

@warn.error
async def warn_error(ctx, error):
    await ctx.send(f"❌ Error: {error}")

@bot.command(name="warnlist")
async def warnlist(ctx, member: discord.Member):
    warns = load_warns()
    uid   = str(member.id)
    data  = warns.get(uid, [])
    if not data:
        await ctx.send(f"✅ {member.mention} tidak punya peringatan.")
        return
    embed = discord.Embed(title=f"⚠️ Daftar Warn — {member.display_name}",
                          color=discord.Color.orange())
    for i, w in enumerate(data, 1):
        embed.add_field(name=f"Warn #{i}", value=f"**Alasan:** {w['alasan']}", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="clearwarn")
@commands.has_permissions(moderate_members=True)
async def clearwarn(ctx, member: discord.Member):
    warns = load_warns()
    warns[str(member.id)] = []
    save_warns(warns)
    await ctx.send(f"✅ Semua warn {member.mention} telah dihapus.")

# ═══════════════════════════════════════════════════════
#  COMMANDS — AFK
# ═══════════════════════════════════════════════════════
@bot.command(name="afk")
async def afk(ctx, *, alasan="Tidak ada alasan"):
    if isinstance(ctx.channel, discord.DMChannel):
        return
    afk_data = load_afk()
    afk_data[str(ctx.author.id)] = {
        "reason": alasan,
        "since": str(datetime.datetime.utcnow())
    }
    save_afk(afk_data)
    await ctx.send(f"💤 {ctx.author.mention} sekarang **offline** — {alasan}", delete_after=10)

# ═══════════════════════════════════════════════════════
#  COMMANDS — GIVEAWAY (setup via DM)
# ═══════════════════════════════════════════════════════
@bot.command(name="setgiveaway")
async def set_giveaway(ctx, channel_id: int):
    if not isinstance(ctx.channel, discord.DMChannel):
        await ctx.send("⚠️ Command ini hanya via DM bot.")
        return
    if not is_admin(ctx.author) and ctx.author.id != OWNER_ID:
        await ctx.send("❌ Hanya admin yang bisa setup giveaway.")
        return
    ch = bot.get_channel(channel_id)
    if not ch:
        await ctx.send("❌ Channel tidak ditemukan.")
        return

    await ctx.send(f"✅ Channel giveaway: **#{ch.name}**\n\nBerapa lama giveaway berlangsung? (contoh: `1h`, `30m`, `2d`)")

    def check(m): return m.author.id == ctx.author.id and isinstance(m.channel, discord.DMChannel)

    try:
        dur_msg = await bot.wait_for("message", check=check, timeout=60)
        dur_str = dur_msg.content.strip().lower()
        seconds = parse_duration(dur_str)
        if not seconds:
            await ctx.send("❌ Format waktu salah. Contoh: `1h`, `30m`, `2d`")
            return

        await ctx.send("Apa hadiahnya? (ketik nama hadiah)")
        prize_msg = await bot.wait_for("message", check=check, timeout=60)
        prize = prize_msg.content.strip()

        # Buat giveaway
        end_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds)
        gid      = str(int(datetime.datetime.utcnow().timestamp()))
        gw_data  = {
            "channel_id": str(channel_id),
            "prize": prize,
            "end_time": end_time.isoformat(),
            "entries": [],
            "ended": False,
            "message_id": None
        }

        giveaways = load_giveaways()
        giveaways[gid] = gw_data
        save_giveaways(giveaways)

        embed = build_giveaway_embed(gw_data)
        view  = GiveawayView(gid)
        msg   = await ch.send(embed=embed, view=view)
        bot.add_view(view)

        giveaways[gid]["message_id"] = str(msg.id)
        save_giveaways(giveaways)

        await ctx.send(f"🎉 Giveaway **{prize}** berhasil dibuat di #{ch.name}!")

    except asyncio.TimeoutError:
        await ctx.send("⏰ Timeout. Ulangi command.")

def parse_duration(s: str) -> int:
    total = 0
    patterns = [("d", 86400), ("h", 3600), ("m", 60), ("s", 1)]
    for suffix, mult in patterns:
        match = re.search(r"(\d+)" + suffix, s)
        if match:
            total += int(match.group(1)) * mult
    return total if total > 0 else None

# ═══════════════════════════════════════════════════════
#  COMMANDS — QUOTE
# ═══════════════════════════════════════════════════════
@bot.command(name="setquotechannel")
async def set_quote_channel(ctx, channel_id: int):
    if not isinstance(ctx.channel, discord.DMChannel):
        await ctx.send("⚠️ Hanya via DM bot.")
        return
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Hanya owner.")
        return
    ch = bot.get_channel(channel_id)
    if not ch:
        await ctx.send("❌ Channel tidak ditemukan.")
        return
    settings = load_settings()
    settings["quote_channel_id"] = str(channel_id)
    save_settings(settings)
    await ctx.send(f"✅ Channel quote diset ke **#{ch.name}**. Gunakan `!kirimquote` untuk kirim manual.")

@bot.command(name="addquote")
async def add_quote(ctx, *, quote: str):
    if not isinstance(ctx.channel, discord.DMChannel):
        await ctx.send("⚠️ Hanya via DM bot.")
        return
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Hanya owner.")
        return
    quotes = load_quotes()
    quotes.append(quote)
    save_json(QUOTE_FILE, quotes)
    await ctx.send(f"✅ Quote ditambahkan! Total: **{len(quotes)}** quote.")

@bot.command(name="kirimquote")
async def kirim_quote_cmd(ctx, channel_id: int = None):
    """Kirim quote manual ke channel. Hanya owner via DM."""
    if not isinstance(ctx.channel, discord.DMChannel):
        await ctx.send("⚠️ Hanya via DM bot.")
        return
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Hanya owner.")
        return

    # Tentukan channel tujuan
    if channel_id:
        ch = bot.get_channel(channel_id)
    else:
        settings = load_settings()
        saved_id = settings.get("quote_channel_id")
        ch = bot.get_channel(int(saved_id)) if saved_id else None

    if not ch:
        await ctx.send("❌ Channel tidak ditemukan. Set dulu dengan `!setquotechannel <id>` atau sertakan ID channel: `!kirimquote <channel_id>`")
        return

    quotes = load_quotes()
    quote  = random.choice(quotes)
    embed  = discord.Embed(
        title="💬 Quote of the Day",
        description=f"*\"{quote}\"*",
        color=discord.Color.gold(),
        timestamp=datetime.datetime.utcnow()
    )
    embed.set_footer(text="Asisten Lurah BFL • Quote of the Day")
    await ch.send(embed=embed)
    await ctx.send(f"✅ Quote berhasil dikirim ke **#{ch.name}**!")

# ═══════════════════════════════════════════════════════
#  COMMANDS — BANNER INFO
# ═══════════════════════════════════════════════════════
@bot.command(name="mybanner")
async def my_banner(ctx):
    if ctx.author.id != OWNER_ID and ctx.channel.id != SPAM_CHANNEL_ID:
        await ctx.send(f"⚠️ Hanya di <#{SPAM_CHANNEL_ID}>!", delete_after=5)
        return
    data = load_data()
    uid  = str(ctx.author.id)
    if uid not in data:
        await ctx.send("❌ Kamu belum punya data XP. Kirim pesan dulu!")
        return
    level       = data[uid]["level"]
    banner_data = assign_banner(ctx.author.id, level)
    rarity      = banner_data["rarity"]
    theme_names = ["Sakura","Galaxy","Cyber","Ocean","Fire","Forest","Moonlight","Aurora"]
    theme_name  = theme_names[banner_data.get("theme",0) % 8]
    rarity_colors_hex = {
        "Common":"⬜","Uncommon":"🟩","Rare":"🟦","Epic":"🟪","Legendary":"🟨"
    }
    embed = discord.Embed(
        title="✦ Info Banner Kamu",
        description=(
            f"**Rarity:** {rarity_colors_hex.get(rarity,'✦')} **{rarity}**\n"
            f"**Tema:** {theme_name}\n"
            f"**Level saat ini:** {level} — {LEVEL_CONFIG[level]['name']}\n\n"
            "Gunakan `!rank` untuk melihat banner kamu!"
        ),
        color=discord.Color.from_rgb(*BANNER_RARITY[rarity]["color"])
    )
    embed.set_footer(text="Asisten Lurah BFL • Banner System")
    await ctx.send(embed=embed)

# ═══════════════════════════════════════════════════════
#  COMMANDS — PENGUMUMAN
# ═══════════════════════════════════════════════════════
@bot.command(name="pengumuman")
async def pengumuman(ctx, channel_id: int, *, pesan: str):
    if not isinstance(ctx.channel, discord.DMChannel):
        await ctx.send("⚠️ Hanya via DM bot.")
        return
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Tidak punya izin.")
        return
    channel = bot.get_channel(channel_id)
    if not channel:
        await ctx.send("❌ Channel tidak ditemukan.")
        return
    embed = discord.Embed(
        title="📢 PENGUMUMAN", description=pesan,
        color=discord.Color.blue(), timestamp=datetime.datetime.utcnow()
    )
    embed.set_footer(text="Asisten Lurah BFL")
    await channel.send("@everyone", embed=embed)
    await ctx.send(f"✅ Dikirim ke #{channel.name}!")

# ═══════════════════════════════════════════════════════
#  COMMANDS — MODERASI
# ═══════════════════════════════════════════════════════
@bot.command(name="timeout")
@commands.has_permissions(moderate_members=True)
async def timeout_member(ctx, member: discord.Member, durasi: int, *, alasan="Tidak ada alasan"):
    until = discord.utils.utcnow() + datetime.timedelta(minutes=durasi)
    await member.timeout(until, reason=alasan)
    embed = discord.Embed(title="⏱️ Member di-Timeout", color=discord.Color.orange())
    embed.add_field(name="Member", value=member.mention, inline=True)
    embed.add_field(name="Durasi", value=f"{durasi} menit", inline=True)
    embed.add_field(name="Alasan", value=alasan, inline=False)
    embed.set_footer(text=f"Oleh: {ctx.author}")
    await ctx.send(embed=embed)

@timeout_member.error
async def timeout_error(ctx, error): await ctx.send(f"❌ Error: {error}")

@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban_member(ctx, member: discord.Member, *, alasan="Tidak ada alasan"):
    await member.ban(reason=alasan)
    embed = discord.Embed(title="🔨 Member di-Ban", color=discord.Color.red())
    embed.add_field(name="Member", value=f"{member} ({member.id})", inline=False)
    embed.add_field(name="Alasan", value=alasan, inline=False)
    embed.set_footer(text=f"Oleh: {ctx.author}")
    await ctx.send(embed=embed)

@ban_member.error
async def ban_error(ctx, error): await ctx.send(f"❌ Error: {error}")

@bot.command(name="unban")
@commands.has_permissions(ban_members=True)
async def unban_member(ctx, user_id: int):
    user = await bot.fetch_user(user_id)
    await ctx.guild.unban(user)
    await ctx.send(f"✅ **{user}** berhasil di-unban.")

@bot.command(name="addrole")
@commands.has_permissions(manage_roles=True)
async def add_role(ctx, member: discord.Member, *, role_name: str):
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if not role:
        await ctx.send(f"❌ Role **{role_name}** tidak ditemukan.")
        return
    await member.add_roles(role)
    await ctx.send(f"✅ Role **{role_name}** → {member.mention}.")

@bot.command(name="removerole")
@commands.has_permissions(manage_roles=True)
async def remove_role(ctx, member: discord.Member, *, role_name: str):
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if not role:
        await ctx.send(f"❌ Role **{role_name}** tidak ditemukan.")
        return
    await member.remove_roles(role)
    await ctx.send(f"✅ Role **{role_name}** dihapus dari {member.mention}.")

@bot.command(name="clear", aliases=["purge","hapus"])
@commands.has_permissions(manage_messages=True)
async def clear_messages(ctx, jumlah: int = 10):
    await ctx.channel.purge(limit=jumlah+1)
    await ctx.send(f"✅ **{jumlah}** pesan dihapus.", delete_after=5)

@clear_messages.error
async def clear_error(ctx, error): await ctx.send(f"❌ Error: {error}")

# ═══════════════════════════════════════════════════════
#  COMMANDS — TICKET SETUP
# ═══════════════════════════════════════════════════════
@bot.command(name="setupticket")
async def setup_ticket(ctx):
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Hanya owner.", delete_after=5)
        return
    channel = bot.get_channel(TICKET_CHANNEL_ID)
    if not channel:
        await ctx.send("❌ Channel tidak ditemukan.")
        return
    embed = discord.Embed(
        title="📩 Buat Laporan / Diskusi",
        description=(
            "Klik tombol di bawah untuk membuat ticket.\n\n"
            "Channel privat akan dibuat, hanya kamu dan admin yang bisa melihatnya."
        ),
        color=discord.Color.blue()
    )
    embed.set_footer(text="Asisten Lurah BFL • Ticket System")
    await channel.send(embed=embed, view=TicketView())
    await ctx.send(f"✅ Ticket system dipasang di {channel.mention}!")

# ═══════════════════════════════════════════════════════
#  COMMANDS — YOUTUBE DATABASE
# ═══════════════════════════════════════════════════════
@bot.command(name="addyt")
async def add_youtube(ctx, nama: str, link: str):
    if not is_admin(ctx.author):
        await ctx.send("❌ Hanya admin.", delete_after=5)
        return
    if "youtube.com" not in link and "youtu.be" not in link:
        await ctx.send("❌ Link harus berupa link YouTube.", delete_after=5)
        return
    yt = load_youtube()
    yt[nama] = link
    save_youtube(yt)
    await ctx.send(f"✅ **{nama}** ditambahkan!")

@bot.command(name="removeyt")
async def remove_youtube(ctx, *, nama: str):
    if not is_admin(ctx.author):
        await ctx.send("❌ Hanya admin.", delete_after=5)
        return
    yt = load_youtube()
    if nama not in yt:
        await ctx.send(f"❌ **{nama}** tidak ditemukan.", delete_after=5)
        return
    del yt[nama]
    save_youtube(yt)
    await ctx.send(f"✅ **{nama}** dihapus.")

@bot.command(name="youtube", aliases=["yt","daftaryt"])
async def list_youtube(ctx):
    if ctx.author.id != OWNER_ID and ctx.channel.id != SPAM_CHANNEL_ID:
        await ctx.send(f"⚠️ Hanya di <#{SPAM_CHANNEL_ID}>!", delete_after=5)
        return
    yt = load_youtube()
    if not yt:
        await ctx.send("📭 Database YouTube kosong.")
        return
    embed = discord.Embed(title="🎬 Database YouTube — BFL", color=discord.Color.red())
    for nama, link in yt.items():
        embed.add_field(name=nama, value=link, inline=False)
    embed.set_footer(text="Asisten Lurah BFL • YouTube Database")
    await ctx.send(embed=embed)

# ═══════════════════════════════════════════════════════
#  COMMANDS — VOICE ROOM
# ═══════════════════════════════════════════════════════
@bot.command(name="createroom")
async def create_room(ctx, *, nama_room: str = None):
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.send("❌ Hanya di server.")
        return
    guild    = ctx.guild
    member   = ctx.author
    category = discord.utils.get(guild.categories, id=VOICE_CATEGORY_ID)
    if not category:
        await ctx.send("❌ Kategori Voice Zone tidak ditemukan.")
        return
    for ch_id, owner_id in list(active_voice_rooms.items()):
        if owner_id == member.id:
            ch = guild.get_channel(ch_id)
            if ch:
                await ctx.send(f"⚠️ Kamu sudah punya room: **{ch.name}**", delete_after=10)
                return
    current_rooms = [ch for ch in category.voice_channels if ch.id in active_voice_rooms]
    if len(current_rooms) >= 10:
        await ctx.send("⚠️ Maks 10 room aktif.", delete_after=10)
        return
    room_name = nama_room if nama_room else f"Room {member.display_name}"
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(connect=True, view_channel=True),
        member: discord.PermissionOverwrite(connect=True, manage_channels=True,
                                            mute_members=True, move_members=True),
        guild.me: discord.PermissionOverwrite(connect=True, manage_channels=True),
    }
    vc = await guild.create_voice_channel(
        name=room_name, category=category, overwrites=overwrites,
        user_limit=10, reason=f"Room oleh {member}"
    )
    active_voice_rooms[vc.id] = member.id
    embed = discord.Embed(
        title="🎙️ Voice Room Dibuat!",
        description=f"Room **{room_name}** aktif di **Voice Zone**.\nAuto-hapus saat kosong. Kapasitas: **10 orang**.",
        color=discord.Color.green()
    )
    embed.set_footer(text=f"Dibuat oleh {member.display_name}")
    await ctx.send(embed=embed)

# ═══════════════════════════════════════════════════════
#  COMMANDS — VERIFIKASI
# ═══════════════════════════════════════════════════════
@bot.command(name="verif")
async def verif_cmd(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.send(
            "📋 **Verifikasi BFL**\n\nKirim foto bukti kamu di sini.\n"
            "Admin akan memberikan role: **Moderator**, **Stream**, atau **Clipper**."
        )
        return
    await ctx.send(f"{ctx.author.mention} Kirim foto bukti ke **DM bot**!", delete_after=15)
    try:
        await ctx.author.send(
            "📋 **Verifikasi BFL**\n\nKirim foto bukti kamu di sini.\n"
            "Admin akan memberikan role: **Moderator**, **Stream**, atau **Clipper**."
        )
    except discord.Forbidden:
        await ctx.send(f"❌ {ctx.author.mention} Buka DM dulu.", delete_after=10)

# ═══════════════════════════════════════════════════════
#  COMMANDS — HELP
# ═══════════════════════════════════════════════════════
@bot.command(name="help")
async def help_cmd(ctx):
    embed = discord.Embed(title="📖 Asisten Lurah BFL — Command List", color=discord.Color.blue())
    embed.add_field(name="🏅 Level & Banner (di #spam)",
        value="`!rank [@user]`\n`!leaderboard`\n`!mybanner`", inline=False)
    embed.add_field(name="🪙 Coin System",
        value="`!koin [@user]` — Cek saldo coin\n`!givecoin @user <jumlah>` — Admin beri coin\n💱 **100 Coin = Rp 10.000**\nTukar coin ke IDR via `!convertcoin` (min. 100 coin)", inline=False)
    embed.add_field(name="🛒 Market System",
        value="`!market` / `!shop` — Lihat katalog\n`!buy <item_id>` — Beli barang\n`!inventory` / `!inv` — Lihat barang kamu\n`!additem` — Admin tambah item (via DM)", inline=False)
    embed.add_field(name="🎙️ Voice Room",
        value="`!createroom [nama]`", inline=False)
    embed.add_field(name="📋 Verifikasi",
        value="`!verif` — Mulai verifikasi via DM", inline=False)
    embed.add_field(name="💤 AFK",
        value="`!afk [alasan]` — Set status offline", inline=False)
    embed.add_field(name="🎬 YouTube",
        value="`!youtube` — Lihat daftar video", inline=False)
    embed.set_footer(text="Asisten Lurah BFL • Gunakan !helpadmin untuk command admin")
    await ctx.send(embed=embed)

@bot.command(name="helpadmin")
async def help_admin_cmd(ctx):
    if not is_admin(ctx.author):
        await ctx.send("❌ Hanya admin yang bisa melihat command ini.", delete_after=5)
        return
    embed = discord.Embed(title="🛡️ Admin Command List — Asisten Lurah BFL", color=discord.Color.red())
    embed.add_field(name="⚠️ Moderasi Member",
        value="`!warn @user [alasan]` — Beri peringatan (auto-kick di 3x)\n`!warnlist @user` — Lihat daftar warn\n`!clearwarn @user` — Hapus semua warn\n`!timeout @user <menit> [alasan]` — Timeout\n`!ban @user [alasan]` — Ban member\n`!unban <user_id>` — Unban member\n`!clear [n]` — Hapus n pesan", inline=False)
    embed.add_field(name="🎭 Role Management",
        value="`!addrole @user <nama_role>` — Tambah role\n`!removerole @user <nama_role>` — Hapus role", inline=False)
    embed.add_field(name="🪙 Coin Admin",
        value="`!givecoin @user <jumlah>` — Tambah coin", inline=False)
    embed.add_field(name="🛒 Market Admin",
        value="`!additem` (via DM bot) — Tambah item + foto katalog", inline=False)
    embed.add_field(name="🎬 YouTube Database",
        value="`!addyt <nama> <link>` — Tambah video\n`!removeyt <nama>` — Hapus video", inline=False)
    embed.add_field(name="🎉 Giveaway (via DM bot)",
        value="`!setgiveaway <channel_id>` — Buat giveaway baru", inline=False)
    embed.add_field(name="📢 Pengumuman & Quote (via DM bot)",
        value="`!pengumuman <channel_id> <pesan>` — Kirim pengumuman\n`!setquotechannel <channel_id>` — Set channel quote\n`!addquote <quote>` — Tambah quote baru\n`!kirimquote [channel_id]` — Kirim quote manual", inline=False)
    embed.add_field(name="🎫 Ticket System",
        value="`!setupticket` — Pasang panel ticket di channel", inline=False)
    embed.set_footer(text="Asisten Lurah BFL • Hanya terlihat oleh Admin/Owner")
    await ctx.send(embed=embed)

# ═══════════════════════════════════════════════════════
#  COIN SYSTEM (menggantikan BFcash)
# ═══════════════════════════════════════════════════════
def load_coins():
    return load_json(COIN_FILE, default={})

def save_coins(d):
    save_json(COIN_FILE, d)

def get_coins(uid: str) -> int:
    coins = load_coins()
    return coins.get(uid, 0)

def add_coins(uid: str, amount: int) -> int:
    coins = load_coins()
    current = coins.get(uid, 0)
    coins[uid] = max(0, current + amount)
    save_coins(coins)
    return coins[uid]

def ensure_coins(uid: str):
    coins = load_coins()
    if uid not in coins:
        coins[uid] = 0
        save_coins(coins)

@bot.command(name="koin", aliases=["coins", "coin", "saldo"])
async def coins_balance(ctx, member: discord.Member = None):
    if ctx.author.id != OWNER_ID and ctx.channel.id != SPAM_CHANNEL_ID:
        await ctx.send(f"⚠️ Hanya di <#{SPAM_CHANNEL_ID}>!", delete_after=5)
        return
    member = member or ctx.author
    uid = str(member.id)
    ensure_coins(uid)
    balance = get_coins(uid)
    embed = discord.Embed(title=f"🪙 Dompet Coin — {member.display_name}", color=discord.Color.gold())
    embed.add_field(name="🪙 Saldo", value=f"{balance:,} Coin", inline=True)
    embed.add_field(name="💱 Nilai IDR", value="100 Coin = Rp 10.000", inline=True)
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text="Asisten Lurah BFL • Coin System")
    await ctx.send(embed=embed)

@bot.command(name="givecoin")
async def give_coin(ctx, member: discord.Member = None, amount: str = None):
    if not is_admin(ctx.author):
        await ctx.send("❌ Hanya admin.", delete_after=5)
        return
    if not member or not amount or not amount.replace(".", "").replace(",", "").isdigit():
        await ctx.send("❌ Contoh: `!givecoin @user 100`")
        return
    amt = int(amount.replace(".", "").replace(",", ""))
    uid = str(member.id)
    ensure_coins(uid)
    new_balance = add_coins(uid, amt)
    await ctx.send(f"✅ **{amt:,} Coin** diberikan ke {member.mention}. Saldo sekarang: **{new_balance:,} Coin**")

# ═══════════════════════════════════════════════════════
#  MARKET SYSTEM
# ═══════════════════════════════════════════════════════
def load_market():
    return load_json(MARKET_FILE, default={})

def save_market(d):
    save_json(MARKET_FILE, d)

def load_inventory():
    return load_json(INVENTORY_FILE, default={})

def save_inventory(d):
    save_json(INVENTORY_FILE, d)

@bot.command(name="additem", aliases=["addmarket"])
async def add_market_item(ctx):
    """Admin setup item market via DM (nama, harga, deskripsi, foto katalog)"""
    if not isinstance(ctx.channel, discord.DMChannel):
        await ctx.send("⚠️ Command ini hanya via DM bot.", delete_after=5)
        return
    if not is_admin(ctx.author) and ctx.author.id != OWNER_ID:
        await ctx.send("❌ Hanya admin yang boleh setup market.", delete_after=5)
        return

    await ctx.send("🛒 **Setup Item Market Baru**\n\n**1.** Ketik **nama item** (contoh: Kaos BFL Premium)")
    
    def check(m): 
        return m.author.id == ctx.author.id and isinstance(m.channel, discord.DMChannel)

    try:
        # Nama
        name_msg = await bot.wait_for("message", check=check, timeout=180)
        name = name_msg.content.strip()[:100]

        await ctx.send("**2.** Ketik **harga dalam Coin** (contoh: 500)")
        price_msg = await bot.wait_for("message", check=check, timeout=60)
        if not price_msg.content.strip().isdigit():
            await ctx.send("❌ Harga harus angka!")
            return
        price = int(price_msg.content.strip())

        await ctx.send("**3.** Ketik **deskripsi item** (bisa panjang)")
        desc_msg = await bot.wait_for("message", check=check, timeout=180)
        description = desc_msg.content.strip()[:500]

        await ctx.send("**4.** Kirim **foto katalog** (satu attachment gambar) sekarang.")
        
        def check_photo(m):
            return (m.author.id == ctx.author.id and 
                    isinstance(m.channel, discord.DMChannel) and 
                    m.attachments and 
                    m.attachments[0].content_type.startswith("image"))
        
        photo_msg = await bot.wait_for("message", check=check_photo, timeout=300)
        image_url = photo_msg.attachments[0].url

        # Simpan ke market
        market = load_market()
        item_id = f"item_{int(datetime.datetime.utcnow().timestamp())}"
        market[item_id] = {
            "name": name,
            "price": price,
            "description": description,
            "image_url": image_url,
            "added_by": str(ctx.author.id),
            "added_at": str(datetime.datetime.utcnow())
        }
        save_market(market)

        embed = discord.Embed(title="✅ Item Berhasil Ditambahkan!", color=discord.Color.green())
        embed.add_field(name="ID", value=f"`{item_id}`", inline=False)
        embed.add_field(name="Nama", value=name, inline=False)
        embed.add_field(name="Harga", value=f"{price} Coin", inline=True)
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)

    except asyncio.TimeoutError:
        await ctx.send("⏰ Timeout. Ulangi dengan `!additem`.")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

@bot.command(name="market", aliases=["shop", "katalog"])
async def show_market(ctx):
    if ctx.author.id != OWNER_ID and ctx.channel.id != SPAM_CHANNEL_ID:
        await ctx.send(f"⚠️ Hanya di <#{SPAM_CHANNEL_ID}>!", delete_after=5)
        return

    market = load_market()
    if not market:
        await ctx.send("🛒 Market masih kosong. Admin bisa tambah dengan `!additem` via DM.")
        return

    await ctx.send("🛒 **KATALOG MARKET BFL**")
    for item_id, item in market.items():
        embed = discord.Embed(
            title=f"🛍️ {item['name']}",
            description=item["description"],
            color=discord.Color.gold()
        )
        embed.add_field(name="ID", value=f"`{item_id}`", inline=True)
        embed.add_field(name="💰 Harga", value=f"**{item['price']} Coin**", inline=True)
        embed.set_image(url=item["image_url"])
        embed.set_footer(text="Gunakan !buy <ID> untuk membeli")
        await ctx.send(embed=embed)

@bot.command(name="buy")
async def buy_item(ctx, item_id: str = None):
    if not is_game_channel(ctx):
        await ctx.send(game_channel_msg(ctx), delete_after=8)
        return
    if not item_id:
        await ctx.send("❌ Gunakan `!buy <item_id>` (contoh: `!buy item_1747320000`)")
        return

    market = load_market()
    if item_id not in market:
        await ctx.send("❌ Item ID tidak ditemukan di market.")
        return

    item = market[item_id]
    uid = str(ctx.author.id)
    ensure_coins(uid)
    balance = get_coins(uid)

    if balance < item["price"]:
        await ctx.send(f"❌ Coin tidak cukup! Kamu punya **{balance} Coin**, butuh **{item['price']} Coin**.")
        return

    # Potong coin
    add_coins(uid, -item["price"])

    # Tambah ke inventory
    inventory = load_inventory()
    if uid not in inventory:
        inventory[uid] = []
    inventory[uid].append({
        "item_id": item_id,
        "name": item["name"],
        "price": item["price"],
        "bought_at": str(datetime.datetime.utcnow())
    })
    save_inventory(inventory)

    embed = discord.Embed(title="🎉 Pembelian Berhasil!", color=discord.Color.green())
    embed.add_field(name="Item", value=item["name"], inline=False)
    embed.add_field(name="Harga", value=f"-{item['price']} Coin", inline=True)
    embed.add_field(name="Saldo tersisa", value=f"{get_coins(uid)} Coin", inline=True)
    embed.set_image(url=item["image_url"])
    await ctx.send(embed=embed)

    try:
        await ctx.author.send(f"✅ Kamu berhasil membeli **{item['name']}**!\nItem sudah masuk ke inventory kamu.")
    except:
        pass

@bot.command(name="inventory", aliases=["inv", "barang", "myitems"])
async def show_inventory(ctx, member: discord.Member = None):
    if ctx.author.id != OWNER_ID and ctx.channel.id != SPAM_CHANNEL_ID:
        await ctx.send(f"⚠️ Hanya di <#{SPAM_CHANNEL_ID}>!", delete_after=5)
        return
    member = member or ctx.author
    uid = str(member.id)
    inventory = load_inventory().get(uid, [])
    if not inventory:
        await ctx.send(f"🛍️ {member.mention} belum punya barang di inventory.")
        return

    embed = discord.Embed(title=f"🛍️ Inventory — {member.display_name}", color=discord.Color.purple())
    for item in inventory[-10:]:  # tampilkan 10 terakhir
        embed.add_field(
            name=item["name"],
            value=f"ID: `{item['item_id']}` • Dibeli: {item['bought_at'][:10]}",
            inline=False
        )
    embed.set_footer(text=f"Total item: {len(inventory)}")
    await ctx.send(embed=embed)

# ═══════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════
bot.run(TOKEN)
</FILE>
