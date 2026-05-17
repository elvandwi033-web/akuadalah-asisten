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
ADMIN_BANK_ID           = "483284166268420096"   # ID admin bank — sumber hadiah game

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
DAILY_FILE       = "daily.json"
HISTORY_FILE     = "history.json"
DUEL_FILE        = "duel.json"
ACTIVITY_FILE    = "activity.json"   # tracking aktivitas game harian untuk pajak

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

WELCOME_BONUS_FILE = "welcome_bonus.json"   # track siapa yg sudah dapat bonus
WELCOME_BONUS_AMOUNT = 15                   # 15 Bcash untuk pemain baru
FIRSTPLAY_BONUS_FILE = "firstplay.json"     # track siapa yg sudah dapat bonus first-play di #spam
FIRSTPLAY_BONUS_AMOUNT = 10                 # 10 Bcash tiap pertama coba main game di #spam

def load_welcome_bonus():
    return load_json(WELCOME_BONUS_FILE, default={})

def save_welcome_bonus(d):
    save_json(WELCOME_BONUS_FILE, d)

def load_firstplay():
    return load_json(FIRSTPLAY_BONUS_FILE, default={})

def save_firstplay(d):
    save_json(FIRSTPLAY_BONUS_FILE, d)

def give_firstplay_bonus(uid: str, display_name: str) -> int:
    """Beri bonus 10 Bcash saat user pertama kali mencoba game di #spam. Return jumlah bonus (0 jika sudah dapat)."""
    uid = str(uid)
    data = load_firstplay()
    if uid in data:
        return 0
    data[uid] = True
    save_firstplay(data)
    ensure_coins(uid)
    ensure_coins(ADMIN_BANK_ID)
    admin_bal = get_coins(ADMIN_BANK_ID)
    if admin_bal < FIRSTPLAY_BONUS_AMOUNT:
        return 0
    add_coins(ADMIN_BANK_ID, -FIRSTPLAY_BONUS_AMOUNT)
    add_coins(uid, FIRSTPLAY_BONUS_AMOUNT)
    mint_coins(FIRSTPLAY_BONUS_AMOUNT)
    log_history(uid, "🎮 Bonus pertama main game", +FIRSTPLAY_BONUS_AMOUNT)
    log_history(ADMIN_BANK_ID, f"🎮 Bonus firstplay → {display_name}", -FIRSTPLAY_BONUS_AMOUNT)
    return FIRSTPLAY_BONUS_AMOUNT

# ═══════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════
def is_admin(member) -> bool:
    """Cek apakah user adalah admin/owner. Aman dipakai di DM (discord.User) maupun server (discord.Member)."""
    if member.id == OWNER_ID:
        return True
    # Jika sudah discord.Member (di server), langsung cek permissions
    if isinstance(member, discord.Member):
        return member.guild_permissions.administrator or member.guild_permissions.manage_guild
    # discord.User (dari DM) → cari member object di semua guild yang bot ikuti
    for guild in bot.guilds:
        m = guild.get_member(member.id)
        if m and (m.guild_permissions.administrator or m.guild_permissions.manage_guild):
            return True
    return False

def is_game_channel(ctx) -> bool:
    """Cek apakah command dijalankan di channel game (SPAM_CHANNEL_ID). DM selalu ditolak."""
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
    daily_tax.start()
    # Start coin price auto-update
    try:
        auto_price_update.start()
    except Exception:
        pass
    # Pastikan saldo admin bank sudah ada (init 10000 jika belum)
    coins = load_coins()
    if ADMIN_BANK_ID not in coins:
        coins[ADMIN_BANK_ID] = 20000
        save_coins(coins)
        print(f"✅ Saldo admin bank diinisialisasi: 20,000 Bcash")

    # Inisialisasi harga Bcash jika belum ada
    import os as _os
    if not _os.path.exists(PRICE_FILE):
        init_price = _PRICE_FILE_DEFAULT.copy()
        save_price(init_price)
        print(f"✅ Harga Bcash diinisialisasi: Rp{_PRICE_INITIAL:,} / 100 Bcash")
    print(f"✅ Semua sistem aktif. Logged in as {bot.user}")

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

    # ── DM Handler ──
    if isinstance(message.channel, discord.DMChannel):
        # Cek apakah pengirim adalah admin/owner di salah satu guild
        sender_is_admin = message.author.id == OWNER_ID
        if not sender_is_admin:
            for g in bot.guilds:
                member_obj = g.get_member(message.author.id)
                if member_obj is None:
                    try:
                        member_obj = await g.fetch_member(message.author.id)
                    except Exception:
                        continue
                if member_obj and is_admin(member_obj):
                    sender_is_admin = True
                    break

        # Jika admin/owner → langsung proses command, skip verifikasi
        if sender_is_admin:
            await bot.process_commands(message)
            return

        # Bukan admin → cek apakah kirim attachment untuk verifikasi
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

        # Member biasa tanpa attachment → proses command (bisa !koin dll)
        await bot.process_commands(message)
        return

    # ── Welcome Bonus 15 Bcash untuk user baru di #spam ──
    if message.channel.id == SPAM_CHANNEL_ID:
        welcome_data = load_welcome_bonus()
        uid_str = str(message.author.id)
        if uid_str not in welcome_data:
            welcome_data[uid_str] = True
            save_welcome_bonus(welcome_data)
            ensure_coins(uid_str)
            ensure_coins(ADMIN_BANK_ID)
            admin_bal = get_coins(ADMIN_BANK_ID)
            if admin_bal >= WELCOME_BONUS_AMOUNT:
                add_coins(ADMIN_BANK_ID, -WELCOME_BONUS_AMOUNT)
                add_coins(uid_str, WELCOME_BONUS_AMOUNT)
                mint_coins(WELCOME_BONUS_AMOUNT)
                log_history(uid_str, "🎁 Welcome Bonus (pemain baru)", +WELCOME_BONUS_AMOUNT)
                log_history(ADMIN_BANK_ID, f"🎁 Welcome Bonus → {message.author.display_name}", -WELCOME_BONUS_AMOUNT)
                embed_welcome = discord.Embed(
                    title="🎉 Selamat Datang di BFL!",
                    description=(
                        f"Halo {message.author.mention}! Kamu dapat **{WELCOME_BONUS_AMOUNT} Bcash** sebagai hadiah pemain baru! 🪙\n\n"
                        f"Gunakan `!koin` untuk cek saldo, `!daily` untuk reward harian, dan `!help` untuk lihat semua command."
                    ),
                    color=discord.Color.gold()
                )
                embed_welcome.set_thumbnail(url=message.author.display_avatar.url)
                embed_welcome.set_footer(text="Asisten Lurah BFL • Welcome Bonus")
                await message.channel.send(embed=embed_welcome)

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
    if not is_game_channel(ctx):
        return await ctx.send(game_channel_msg(ctx), delete_after=8)
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
    if not is_game_channel(ctx):
        return await ctx.send(game_channel_msg(ctx), delete_after=8)
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
async def warn(ctx, member: discord.Member = None, *, alasan="Tidak ada alasan"):
    if not is_admin(ctx.author):
        return await ctx.send("❌ Kamu tidak punya izin untuk command ini.")
    if member is None:
        return await ctx.send("❌ Format: `!warn @user [alasan]`")
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
async def clearwarn(ctx, member: discord.Member = None):
    if not is_admin(ctx.author):
        return await ctx.send("❌ Kamu tidak punya izin untuk command ini.")
    if member is None:
        return await ctx.send("❌ Format: `!clearwarn @user`")
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
    if not is_game_channel(ctx):
        return await ctx.send(game_channel_msg(ctx), delete_after=8)
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
async def timeout_member(ctx, member: discord.Member = None, durasi: int = None, *, alasan="Tidak ada alasan"):
    if not is_admin(ctx.author):
        return await ctx.send("❌ Kamu tidak punya izin untuk command ini.")
    if member is None or durasi is None:
        return await ctx.send("❌ Format: `!timeout @user <menit> [alasan]`")
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
async def ban_member(ctx, member: discord.Member = None, *, alasan="Tidak ada alasan"):
    if not is_admin(ctx.author):
        return await ctx.send("❌ Kamu tidak punya izin untuk command ini.")
    if member is None:
        return await ctx.send("❌ Format: `!ban @user [alasan]`")
    await member.ban(reason=alasan)
    embed = discord.Embed(title="🔨 Member di-Ban", color=discord.Color.red())
    embed.add_field(name="Member", value=f"{member} ({member.id})", inline=False)
    embed.add_field(name="Alasan", value=alasan, inline=False)
    embed.set_footer(text=f"Oleh: {ctx.author}")
    await ctx.send(embed=embed)

@ban_member.error
async def ban_error(ctx, error): await ctx.send(f"❌ Error: {error}")

@bot.command(name="unban")
async def unban_member(ctx, user_id: int = None):
    if not is_admin(ctx.author):
        return await ctx.send("❌ Kamu tidak punya izin untuk command ini.")
    if user_id is None:
        return await ctx.send("❌ Format: `!unban <user_id>`")
    guild = ctx.guild
    if guild is None:
        # Coba cari dari bot guilds jika dari DM
        if bot.guilds:
            guild = bot.guilds[0]
        else:
            return await ctx.send("❌ Tidak ada server yang ditemukan.")

    user = await bot.fetch_user(user_id)
    await guild.unban(user)
    await ctx.send(f"✅ **{user}** berhasil di-unban.")

@bot.command(name="addrole")
async def add_role(ctx, member: discord.Member = None, *, role_name: str = None):
    if not is_admin(ctx.author):
        return await ctx.send("❌ Kamu tidak punya izin untuk command ini.")
    if member is None or role_name is None:
        return await ctx.send("❌ Format: `!addrole @user <nama_role>`")
    if ctx.guild is None:
        return await ctx.send("❌ Command ini harus dijalankan di server.")
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if not role:
        await ctx.send(f"❌ Role **{role_name}** tidak ditemukan.")
        return
    await member.add_roles(role)
    await ctx.send(f"✅ Role **{role_name}** → {member.mention}.")

@bot.command(name="removerole")
async def remove_role(ctx, member: discord.Member = None, *, role_name: str = None):
    if not is_admin(ctx.author):
        return await ctx.send("❌ Kamu tidak punya izin untuk command ini.")
    if member is None or role_name is None:
        return await ctx.send("❌ Format: `!removerole @user <nama_role>`")
    if ctx.guild is None:
        return await ctx.send("❌ Command ini harus dijalankan di server.")
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if not role:
        await ctx.send(f"❌ Role **{role_name}** tidak ditemukan.")
        return
    await member.remove_roles(role)
    await ctx.send(f"✅ Role **{role_name}** dihapus dari {member.mention}.")

@bot.command(name="clear", aliases=["purge","hapus"])
async def clear_messages(ctx, jumlah: int = 10):
    if not is_admin(ctx.author):
        return await ctx.send("❌ Kamu tidak punya izin untuk command ini.")
    if isinstance(ctx.channel, discord.DMChannel):
        return await ctx.send("❌ Command ini hanya bisa digunakan di server.")
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
#  COMMANDS — HELP
# ═══════════════════════════════════════════════════════
@bot.command(name="help")
async def help_cmd(ctx):
    embed = discord.Embed(
        title="📖 Asisten Lurah BFL — Command List",
        description="Prefix: `!` | Command game hanya di <#" + str(SPAM_CHANNEL_ID) + ">",
        color=discord.Color.blue()
    )
    embed.add_field(name="🏅 Level & XP (di #spam)",
        value=("`!rank [@user]` — Lihat rank card + banner kamu\n"
               "`!leaderboard` / `!lb` / `!top` — Top 10 XP server\n"
               "`!mybanner` — Info rarity & tema banner kamu\n"
               "📌 XP dapet dari chat, level naik otomatis!"), inline=False)
    embed.add_field(name="💰 Bcash System (di #spam)",
        value=("`!koin [@user]` — Cek saldo + nilai IDR Bcash kamu\n"
               "`!daily` / `!klaim` — Klaim reward harian (streak 1–7, max 7 Bcash)\n"
               "`!kirim @user <jumlah>` — Transfer Bcash ke member lain\n"
               "`!convertcoin <jumlah>` — Tukar Bcash ke IDR (min. **Rp50.000**), tarik ke DANA/OVO/ShopeePay\n"
               "`!deposit <jumlah>` — Request deposit Bcash\n"
               "`!price` — Cek harga Bcash + grafik + market sentiment\n"
               "💱 **Harga Bcash bergerak seperti crypto!** Dipengaruhi game, trading, dan sirkulasi"), inline=False)
    embed.add_field(name="🎰 Mini Games (di #spam)",
        value=("`!slot <bet>` — Mesin slot, taruhan Bcash (min. 1)\n"
               "`!coinflip <heads/tails> <1-10>` — Flip koin, tebak sisi yang benar!\n"
               "`!balapan <1/2> <1-15>` — 🏇 Balapan kuda! Pilih kuda & taruhan (ada animasi!)\n"
               "`!ball <1-15>` — ⚽ Tendang bola ke gawang! Chance masuk **42%**\n"
               "`!hunt` — 🏹 Berburu di hutan! Modal **2 Bcash**, hadiah 2–15 Bcash\n"
               "`!duel @user <jumlah>` — Tantang user duel Bcash (ketik `ya` untuk terima)\n"
               "`!trade <up/down> <5-10>` — Prediksi harga Bcash, hasil 1 menit\n"
               "📌 Peluang menang balapan: **45%** | Ball: **42%** | Hunt: **55%**\n"
               "🎮 **Bonus 10 Bcash** untuk pertama kali main game!"), inline=False)
    embed.add_field(name="📊 Statistik (di #spam)",
        value=("`!history [@user]` / `!riwayat` — Lihat 10 transaksi Bcash terakhir"), inline=False)
    embed.add_field(name="🛒 Market System (di #spam)",
        value=("`!market` / `!shop` / `!katalog` — Lihat semua item\n"
               "`!buy <item_id>` — Beli item (isi form pengiriman via DM)\n"
               "`!inventory` / `!inv` [@user] — Lihat barang yang dimiliki"), inline=False)
    embed.add_field(name="🎙️ Voice Room",
        value=("`!createroom [nama]` — Buat voice room pribadi\n"
               "📌 Room auto-hapus saat kosong, maks 10 orang"), inline=False)
    embed.add_field(name="💤 AFK",
        value=("`!afk [alasan]` — Set status AFK\n"
               "📌 Status hilang otomatis saat kamu kirim pesan"), inline=False)
    embed.set_footer(text="Asisten Lurah BFL • Gunakan !helpadmin untuk command admin")
    await ctx.send(embed=embed)

@bot.command(name="helpadmin", aliases=["adminhelp"])
async def help_admin_cmd(ctx):
    # Resolve author sebagai Member (bukan User) agar guild_permissions tersedia
    author = ctx.author
    if isinstance(ctx.channel, discord.DMChannel):
        # Cari member object di salah satu guild
        for g in bot.guilds:
            m = g.get_member(author.id)
            if m is None:
                try:
                    m = await g.fetch_member(author.id)
                except Exception:
                    continue
            if m:
                author = m
                break

    if not is_admin(author):
        if isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("❌ Kamu bukan admin.")
        else:
            await ctx.send("❌ Hanya admin yang bisa melihat command ini.", delete_after=5)
        return
    embed = discord.Embed(
        title="🛡️ Admin Command List — Asisten Lurah BFL",
        description="Semua command di bawah hanya untuk Admin/Owner\n📌 Command bertanda *(DM)* bisa dipakai di DM bot",
        color=discord.Color.red()
    )
    embed.add_field(name="⚠️ Moderasi Member",
        value=("`!warn @user [alasan]` — Beri peringatan (auto-kick di warn ke-3)\n"
               "`!warnlist @user` — Lihat semua warn milik user\n"
               "`!clearwarn @user` — Hapus semua warn user\n"
               "`!timeout @user <menit> [alasan]` — Timeout member\n"
               "`!ban @user [alasan]` — Ban member dari server\n"
               "`!unban <user_id>` — Unban member via ID\n"
               "`!clear [n]` / `!purge` / `!hapus` — Hapus n pesan (default 10)"), inline=False)
    embed.add_field(name="🎭 Role Management",
        value=("`!addrole @user <nama_role>` — Tambahkan role ke member\n"
               "`!removerole @user <nama_role>` — Hapus role dari member"), inline=False)
    embed.add_field(name="💰 Bcash & Market Admin",
        value=("`!givecoin @user <jumlah>` *(DM/server)* — Tambah Bcash ke user\n"
               "`!addkoin <jumlah>` *(DM/server)* — ➕ Tambah saldo admin bank langsung\n"
               "`!checkbalance @user` — Cek saldo Bcash user\n"
               "`!setprice <harga>` — Override harga Bcash (Rp1.000–Rp15.000 per 100)\n"
               "`!burncoin <jumlah>` *(DM/server)* — 🔥 Burn Bcash dari admin bank → supply turun → harga naik\n"
               "`!price` — Lihat harga & market sentiment\n"
               "`!supply` *(DM/server)* — Laporan sirkulasi: holder, nama akun, burn\n"
               "`!setspamchannel <channel_id>` *(DM)* — Ganti spam channel\n"
               "`!additem` *(DM)* — Tambah item market baru (step-by-step)\n"
               "`!deleteitem <item_id>` — Hapus item dari market\n"
               "`!listuser` — Daftar semua user dengan saldo > 1 Bcash\n"
               "`!rain <total> [jumlah_user]` — Sebar Bcash ke user aktif\n"
               "📌 WD minimum **Rp50.000** | Semua kekalahan game → masuk saldo admin\n"
               "🏛️ **Pajak otomatis 10%** setiap hari untuk user tidak aktif bermain"), inline=False)
    embed.add_field(name="🎉 Giveaway *(DM)*",
        value=("`!setgiveaway <channel_id>` — Buat giveaway baru\n"
               "📌 Bot tanya: durasi (`1h`, `30m`, `2d`) lalu nama hadiah\n"
               "📌 Auto undi pemenang & DM pemenang"), inline=False)
    embed.add_field(name="📢 Pengumuman & Quote *(DM)*",
        value=("`!pengumuman <channel_id> <pesan>` — Kirim pengumuman @everyone\n"
               "`!setquotechannel <channel_id>` — Set channel tujuan quote\n"
               "`!addquote <quote>` — Tambah quote baru ke database\n"
               "`!kirimquote [channel_id]` — Kirim quote random manual"), inline=False)
    embed.add_field(name="🎫 Ticket System",
        value=("`!setupticket` — Pasang panel ticket di TICKET_CHANNEL\n"
               "📌 Member klik tombol → buat ticket privat"), inline=False)
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
    """Selalu return int, pastikan uid string, handle format lama (int key)."""
    uid = str(uid)
    coins = load_coins()
    # Cek string key dulu, fallback ke int key (format lama)
    if uid in coins:
        return int(coins[uid])
    if int(uid) in coins:
        # Migrasi key int ke string
        val = int(coins[int(uid)])
        coins[uid] = val
        del coins[int(uid)]
        save_coins(coins)
        return val
    return 0

def add_coins(uid: str, amount: int) -> int:
    """Tambah/kurang coin, pastikan uid string, return saldo baru."""
    uid = str(uid)
    coins = load_coins()
    # Migrasi int key ke string key jika ada
    if int(uid) in coins and uid not in coins:
        coins[uid] = coins.pop(int(uid))
    current = int(coins.get(uid, 0))
    coins[uid] = max(0, current + amount)
    save_coins(coins)
    return coins[uid]

def ensure_coins(uid: str):
    uid = str(uid)
    coins = load_coins()
    # Migrasi int key ke string key jika ada
    if int(uid) in coins and uid not in coins:
        coins[uid] = coins.pop(int(uid))
        save_coins(coins)
        return
    if uid not in coins:
        coins[uid] = 0
        save_coins(coins)

def log_history(uid: str, label: str, amount: int):
    """Catat transaksi ke history.json. amount positif = masuk, negatif = keluar."""
    uid = str(uid)
    data = load_json(HISTORY_FILE, default={})
    if uid not in data:
        data[uid] = []
    entry = {
        "label":  label,
        "amount": amount,
        "time":   datetime.datetime.utcnow().strftime("%d/%m %H:%M")
    }
    data[uid].insert(0, entry)   # terbaru di atas
    data[uid] = data[uid][:30]   # simpan max 30 entri
    save_json(HISTORY_FILE, data)

@bot.command(name="koin", aliases=["coins", "coin", "bcash", "wallet"])
async def coins_balance(ctx, member: discord.Member = None):
    is_dm = isinstance(ctx.channel, discord.DMChannel)
    if not is_dm and not is_game_channel(ctx):
        return await ctx.send(game_channel_msg(ctx), delete_after=8)
    if is_dm:
        member = ctx.author
    else:
        member = member or ctx.author
    uid = str(member.id)
    ensure_coins(uid)
    balance = get_coins(uid)

    price_data = load_price()
    price     = price_data["price"]
    total_idr = int((balance / 100) * price)

    # Trend singkat
    hist = price_data.get("history", [price])
    if len(hist) >= 2:
        trend = "📈" if price >= hist[-2] else "📉"
    else:
        trend = "➡️"

    embed = discord.Embed(
        title=f"💰 Dompet Bcash — {member.display_name}",
        color=discord.Color.gold()
    )
    embed.add_field(
        name="💰 Saldo",
        value=f"**{balance:,} Bcash**",
        inline=True
    )
    embed.add_field(
        name="💵 Nilai IDR",
        value=f"**Rp{total_idr:,}**",
        inline=True
    )
    embed.add_field(
        name=f"{trend} Harga Bcash",
        value=f"**Rp{price:,}** / 100 Bcash",
        inline=False
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text="Asisten Lurah BFL • Bcash | !price untuk detail market")
    await ctx.send(embed=embed)

@bot.command(name="givecoin")
async def give_coin(ctx, target: str = None, amount: str = None):
    """Admin beri Bcash ke user. Bisa di server (mention) atau DM (user_id)."""
    if not is_admin(ctx.author):
        await ctx.send("❌ Hanya admin.", delete_after=5 if not isinstance(ctx.channel, discord.DMChannel) else None)
        return

    if not target or not amount or not amount.replace(".", "").replace(",", "").isdigit():
        await ctx.send("❌ Format: `!givecoin @user 100` atau `!givecoin <user_id> 100`")
        return

    amt = int(amount.replace(".", "").replace(",", ""))

    # Resolve member — bisa mention atau user_id (penting untuk DM)
    member = None
    # Coba parse sebagai user_id
    raw_id = target.strip("<@!>")
    if raw_id.isdigit():
        try:
            member = await bot.fetch_user(int(raw_id))
        except Exception:
            pass
    if not member:
        await ctx.send("❌ User tidak ditemukan. Gunakan mention `@user` atau ID numerik.")
        return

    uid = str(member.id)
    ensure_coins(uid)
    ensure_coins(ADMIN_BANK_ID)
    admin_bal = get_coins(ADMIN_BANK_ID)
    if admin_bal < amt:
        return await ctx.send(f"❌ Saldo admin bank tidak cukup! Saldo: **{admin_bal:,} Bcash**, butuh: **{amt:,} Bcash**.")

    add_coins(ADMIN_BANK_ID, -amt)
    new_balance = add_coins(uid, amt)
    mint_coins(amt)
    log_history(uid, "💝 Givecoin dari Admin", +amt)
    log_history(ADMIN_BANK_ID, f"💝 Givecoin → {member.display_name}", -amt)

    display = f"<@{member.id}>" if not isinstance(ctx.channel, discord.DMChannel) else f"**{member.display_name}**"
    await ctx.send(f"✅ **{amt:,} Bcash** diberikan ke {display}. Saldo sekarang: **{new_balance:,} Bcash**")

    # Notif DM ke penerima
    try:
        await member.send(f"💝 Kamu mendapat **{amt:,} Bcash** dari Admin!\nSaldo sekarang: **{new_balance:,} Bcash**")
    except Exception:
        pass

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

        await ctx.send("**2.** Ketik **harga dalam Bcash** (contoh: 500)")
        price_msg = await bot.wait_for("message", check=check, timeout=60)
        if not price_msg.content.strip().isdigit():
            await ctx.send("❌ Harga harus angka!")
            return
        price = int(price_msg.content.strip())

        await ctx.send("**3.** Ketik **deskripsi item** (bisa panjang)")
        desc_msg = await bot.wait_for("message", check=check, timeout=180)
        description = desc_msg.content.strip()[:500]

        await ctx.send("**4.** Ketik **jumlah stok** (contoh: `10`), atau ketik `unlimited` jika tidak terbatas.")
        stock_msg = await bot.wait_for("message", check=check, timeout=60)
        stock_raw = stock_msg.content.strip().lower()
        if stock_raw in ["unlimited", "infinite", "tak terbatas", "-1", "∞"]:
            stock = -1
        elif stock_raw.isdigit() and int(stock_raw) > 0:
            stock = int(stock_raw)
        else:
            await ctx.send("❌ Stok harus angka positif atau `unlimited`!")
            return

        await ctx.send("**5.** Kirim **foto katalog** (satu attachment gambar) sekarang.")
        
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
            "stock": stock,
            "added_by": str(ctx.author.id),
            "added_at": str(datetime.datetime.utcnow())
        }
        save_market(market)

        stock_str = "∞ Unlimited" if stock == -1 else str(stock)
        embed = discord.Embed(title="✅ Item Berhasil Ditambahkan!", color=discord.Color.green())
        embed.add_field(name="ID", value=f"`{item_id}`", inline=False)
        embed.add_field(name="Nama", value=name, inline=False)
        embed.add_field(name="Harga", value=f"{price} Bcash", inline=True)
        embed.add_field(name="Stok", value=stock_str, inline=True)
        embed.set_thumbnail(url=image_url)
        await ctx.send(embed=embed)

    except asyncio.TimeoutError:
        await ctx.send("⏰ Timeout. Ulangi dengan `!additem`.")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

@bot.command(name="market", aliases=["shop", "katalog"])
async def show_market(ctx):
    if not is_game_channel(ctx):
        return await ctx.send(game_channel_msg(ctx), delete_after=8)

    market = load_market()
    if not market:
        await ctx.send("🛒 Market masih kosong. Admin bisa tambah dengan `!additem` via DM.")
        return

    # Bagi item ke beberapa embed (max 25 field per embed Discord)
    items_list = list(market.items())
    chunks = [items_list[i:i+8] for i in range(0, len(items_list), 8)]

    for page_num, chunk in enumerate(chunks):
        embed = discord.Embed(
            title="🛒 KATALOG MARKET BFL",
            description="Gunakan `!buy <ID>` untuk membeli item",
            color=discord.Color.gold()
        )
        if len(chunks) > 1:
            embed.title = f"🛒 KATALOG MARKET BFL (Halaman {page_num+1}/{len(chunks)})"

        for item_id, item in chunk:
            stock = item.get("stock", -1)
            if stock == -1:
                stock_str = "✅ ∞"
            elif stock > 0:
                stock_str = f"✅ {stock}"
            else:
                stock_str = "❌ Habis"

            embed.add_field(
                name=f"🛍️ {item['name']}",
                value=(
                    f"💰 **{item['price']} Bcash**\n"
                    f"📦 Stok: {stock_str}\n"
                    f"📝 {item['description'][:80]}{'...' if len(item['description']) > 80 else ''}\n"
                    f"🆔 `{item_id}`"
                ),
                inline=True
            )

        # Gunakan thumbnail item pertama di chunk sebagai preview
        first_item = chunk[0][1]
        embed.set_thumbnail(url=first_item.get("image_url", ""))
        embed.set_footer(text=f"Total {len(items_list)} item | Asisten Lurah BFL")
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

    # Cek stok
    stock = item.get("stock", -1)
    if stock == 0:
        await ctx.send(f"❌ **{item['name']}** sudah habis stok!")
        return

    uid = str(ctx.author.id)
    ensure_coins(uid)
    balance = get_coins(uid)

    if balance < item["price"]:
        await ctx.send(f"❌ Bcash tidak cukup! Kamu punya **{balance:,} Bcash**, butuh **{item['price']:,} Bcash**.")
        return

    # Potong coin, masuk ke admin bank sebagai pendapatan market
    add_coins(uid, -item["price"])
    add_coins(ADMIN_BANK_ID, +item["price"])
    burn_coins(item["price"])   # burn untuk pengaruhi supply/harga
    log_history(ADMIN_BANK_ID, f"🛒 Pendapatan market: {item['name']} dari {ctx.author.display_name}", +item["price"])

    # Kurangi stok jika bukan unlimited
    if stock != -1:
        market[item_id]["stock"] = stock - 1
        save_market(market)

    # Notif di channel
    embed_ok = discord.Embed(title="🎉 Pembelian Berhasil!", color=discord.Color.green())
    embed_ok.add_field(name="Item", value=item["name"], inline=False)
    embed_ok.add_field(name="Harga", value=f"-{item['price']:,} Bcash", inline=True)
    embed_ok.set_thumbnail(url=item["image_url"])
    embed_ok.set_footer(text="Cek DM kamu untuk mengisi data pengiriman!")
    await ctx.send(embed=embed_ok)

    # Buka DM untuk isi form
    try:
        dm = await ctx.author.create_dm()

        def check_dm(m):
            return m.author.id == ctx.author.id and isinstance(m.channel, discord.DMChannel)

        await dm.send(
            f"📦 **Form Pembelian — {item['name']}**\n\n"
            f"Harga: **{item['price']:,} Bcash** ✅ Sudah dibayar\n\n"
            f"Isi data pengiriman kamu:\n\n**1.** Ketik **nama lengkap** kamu:"
        )

        try:
            nama_msg = await bot.wait_for("message", check=check_dm, timeout=180)
            nama = nama_msg.content.strip()[:100]

            await dm.send("**2.** Ketik **nomor HP / WhatsApp** kamu:")
            hp_msg = await bot.wait_for("message", check=check_dm, timeout=120)
            nomor_hp = hp_msg.content.strip()[:30]

            await dm.send("**3.** Ketik **alamat lengkap** pengiriman kamu:")
            alamat_msg = await bot.wait_for("message", check=check_dm, timeout=300)
            alamat = alamat_msg.content.strip()[:500]

            # Simpan order ke file orders
            orders = load_json("orders.json", default=[])
            order_entry = {
                "user_id": str(ctx.author.id),
                "username": ctx.author.display_name,
                "item_id": item_id,
                "item_name": item["name"],
                "price": item["price"],
                "nama": nama,
                "nomor_hp": nomor_hp,
                "alamat": alamat,
                "time": datetime.datetime.utcnow().strftime("%d/%m/%Y %H:%M"),
                "status": "pending"
            }
            orders.append(order_entry)
            save_json("orders.json", orders)

            # Konfirmasi ke pembeli
            konfirm = discord.Embed(
                title="✅ Data Pengiriman Tersimpan!",
                color=discord.Color.green()
            )
            konfirm.add_field(name="🛍️ Item", value=item["name"], inline=False)
            konfirm.add_field(name="👤 Nama", value=nama, inline=True)
            konfirm.add_field(name="📱 No. HP", value=nomor_hp, inline=True)
            konfirm.add_field(name="📍 Alamat", value=alamat, inline=False)
            konfirm.set_footer(text="Admin akan menghubungi kamu segera • Asisten Lurah BFL")
            await dm.send(embed=konfirm)

            # Kirim notif ke owner / admin
            try:
                owner = await bot.fetch_user(OWNER_ID)
                notif = discord.Embed(
                    title="🔔 Order Baru Masuk!",
                    color=discord.Color.orange()
                )
                notif.add_field(name="👤 Pembeli", value=f"{ctx.author.mention} (`{ctx.author.id}`)", inline=False)
                notif.add_field(name="🛍️ Item", value=f"{item['name']} (`{item_id}`)", inline=False)
                notif.add_field(name="💰 Harga", value=f"{item['price']:,} Bcash", inline=True)
                notif.add_field(name="📛 Nama", value=nama, inline=True)
                notif.add_field(name="📱 No. HP", value=nomor_hp, inline=True)
                notif.add_field(name="📍 Alamat", value=alamat, inline=False)
                notif.set_footer(text=f"Waktu: {order_entry['time']}")
                await owner.send(embed=notif)
            except Exception:
                pass

        except asyncio.TimeoutError:
            await dm.send(
                "⏰ Timeout mengisi form. Data pengirimanmu belum tersimpan.\n"
                "Hubungi admin secara manual untuk konfirmasi pembelian."
            )

    except discord.Forbidden:
        await ctx.send(
            f"⚠️ {ctx.author.mention} Pembelian berhasil tapi DM kamu tertutup!\n"
            "Buka DM bot dan hubungi admin untuk isi data pengiriman."
        )

@bot.command(name="inventory", aliases=["inv", "barang", "myitems"])
async def show_inventory(ctx, member: discord.Member = None):
    if not is_game_channel(ctx):
        return await ctx.send(game_channel_msg(ctx), delete_after=8)
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

@bot.command(name="deleteitem", aliases=["hapusitem", "removeitem"])
async def delete_market_item(ctx, item_id: str = None):
    """Admin hapus item dari market. Bisa di server maupun DM."""
    if not is_admin(ctx.author):
        await ctx.send("❌ Hanya admin yang bisa menghapus item.")
        return
    if not item_id:
        await ctx.send("❌ Format: `!deleteitem <item_id>`\nContoh: `!deleteitem item_1747320000`")
        return

    market = load_market()
    if item_id not in market:
        await ctx.send(f"❌ Item `{item_id}` tidak ditemukan di market.")
        return

    item_name = market[item_id]["name"]
    del market[item_id]
    save_market(market)

    embed = discord.Embed(
        title="🗑️ Item Dihapus dari Market",
        description=f"**{item_name}** (`{item_id}`) berhasil dihapus.",
        color=discord.Color.red()
    )
    embed.set_footer(text=f"Dihapus oleh {ctx.author}")
    await ctx.send(embed=embed)

@bot.command(name="listuser", aliases=["daftaruser", "richlist"])
async def list_user_coins(ctx):
    """Admin — tampilkan semua user yang punya lebih dari 1 Bcash. Bisa di server maupun DM."""
    if not is_admin(ctx.author):
        await ctx.send("❌ Hanya admin yang bisa melihat command ini.")
        return

    coins = load_coins()
    # Filter user dengan lebih dari 1 koin, urutkan dari terbanyak
    rich_users = [
        (uid, int(bal)) for uid, bal in coins.items()
        if str(uid) != ADMIN_BANK_ID and int(bal) > 1
    ]
    rich_users.sort(key=lambda x: x[1], reverse=True)

    if not rich_users:
        await ctx.send("📭 Tidak ada user dengan saldo lebih dari 1 Bcash.")
        return

    price_data = load_price()
    price = price_data.get("price", 10000)

    embed = discord.Embed(
        title="💰 Daftar User Bcash (> 1 Bcash)",
        description=f"Total: **{len(rich_users)} user** | Harga: Rp{price:,}/100",
        color=discord.Color.gold()
    )

    medals = ["🥇", "🥈", "🥉"]
    lines = []
    for i, (uid, bal) in enumerate(rich_users[:25]):  # max 25
        medal = medals[i] if i < 3 else f"`#{i+1}`"
        idr = int((bal / 100) * price)
        try:
            user = await bot.fetch_user(int(uid))
            name = user.display_name
        except Exception:
            name = f"User#{uid}"
        lines.append(f"{medal} **{name}** — {bal:,} Bcash (≈ Rp{idr:,})")

    # Potong jika terlalu panjang
    chunk_size = 10
    for chunk_start in range(0, len(lines), chunk_size):
        chunk = lines[chunk_start:chunk_start + chunk_size]
        field_name = f"Peringkat {chunk_start+1}–{chunk_start+len(chunk)}"
        embed.add_field(name=field_name, value="\n".join(chunk), inline=False)

    embed.set_footer(text=f"Asisten Lurah BFL • Hanya terlihat admin | Total user terdaftar: {len(coins)}")
    await ctx.send(embed=embed)


@bot.command(name="supply", aliases=["supplyinfo", "sirkulasi"])
async def supply_cmd(ctx):
    """Admin — lihat info sirkulasi: total supply beredar, daftar holder, total burn. Bisa di DM."""
    if not is_admin(ctx.author):
        await ctx.send("❌ Hanya admin yang bisa melihat command ini.")
        return

    price_data  = load_price()
    coins_data  = load_coins()
    history_data = load_json(HISTORY_FILE, default={})

    # ── Hitung total beredar (semua user kecuali admin bank) ──
    total_beredar = 0
    holder_list   = []
    for uid, bal in coins_data.items():
        if str(uid) == ADMIN_BANK_ID:
            continue
        b = int(bal)
        if b > 0:
            total_beredar += b
            holder_list.append((str(uid), b))

    holder_list.sort(key=lambda x: x[1], reverse=True)

    # ── Hitung total coin yang pernah di-burn dari history ──
    total_burned = 0
    for uid, entries in history_data.items():
        for e in entries:
            lbl = e.get("label", "")
            # burn terjadi saat: slot kalah, buy item, lotre, convert, trade lose, duel
            if any(kw in lbl.lower() for kw in ["slot bet", "beli", "tiket lotre", "convert", "trade taruhan", "duel", "burn"]):
                if e["amount"] < 0:
                    total_burned += abs(e["amount"])

    supply_in_price = price_data.get("supply", 0)
    admin_bal       = get_coins(ADMIN_BANK_ID)
    price           = price_data.get("price", _PRICE_INITIAL)

    # ── Embed utama ──
    embed = discord.Embed(
        title="📊 Laporan Sirkulasi Bcash",
        color=discord.Color.blurple(),
        timestamp=datetime.datetime.utcnow()
    )
    embed.add_field(name="💰 Saldo Admin Bank",    value=f"**{admin_bal:,} Bcash**",       inline=True)
    embed.add_field(name="🏦 Total Beredar (User)",value=f"**{total_beredar:,} Bcash**",    inline=True)
    embed.add_field(name="📦 Supply di Sistem",    value=f"**{supply_in_price:,} Bcash**",  inline=True)
    embed.add_field(name="🔥 Estimasi Total Burn", value=f"**{total_burned:,} Bcash**",     inline=True)
    embed.add_field(name="👥 Total Holder Aktif",  value=f"**{len(holder_list)} user**",    inline=True)
    embed.add_field(name="💱 Harga Saat Ini",      value=f"**Rp{price:,}** / 100 Bcash",   inline=True)

    # ── Top 10 holder ──
    if holder_list:
        lines = []
        medals = ["🥇","🥈","🥉"]
        for i, (uid, bal) in enumerate(holder_list[:10]):
            medal = medals[i] if i < 3 else f"`#{i+1}`"
            idr   = int((bal / 100) * price)
            try:
                user = await bot.fetch_user(int(uid))
                nama = user.display_name
            except Exception:
                nama = f"User#{uid}"
            lines.append(f"{medal} **{nama}** — {bal:,} Bcash ≈ Rp{idr:,}")
        embed.add_field(
            name=f"🏆 Top {min(10, len(holder_list))} Holder",
            value="\n".join(lines),
            inline=False
        )

    embed.set_footer(text=f"Asisten Lurah BFL • Admin Only | Supply naik → harga ↓, burn → harga ↑")
    await ctx.send(embed=embed)


# ═══════════════════════════════════════════════════════
PRICE_FILE  = "coin_price.json"

# ── Konstanta harga ───────────────────────────────────
# ══════════════════════════════════════════════════════════════════════
#  KONSTANTA MARKET
#  Hard cap: 100 Bcash = Rp15.000 (batas atas mutlak)
#  Floor   : 100 Bcash = Rp1.000  (batas bawah mutlak)
# ══════════════════════════════════════════════════════════════════════
_PRICE_INITIAL = 10000   # harga awal  : 100 Bcash = Rp10.000
_PRICE_CAP     = 15000   # batas atas  : 100 Bcash = Rp15.000 (HARD CAP)
_PRICE_FLOOR   = 1000    # batas bawah : 100 Bcash = Rp1.000
_SUPPLY_INIT   = 20000   # supply awal Bcash

# Persentase max gerak per tick (simulasi pasar bergejolak tapi terukur)
_TICK_MAX_PCT  = 0.045   # max ±4.5% per 2 menit

_PRICE_FILE_DEFAULT = {
    "price":    _PRICE_INITIAL,
    "supply":   _SUPPLY_INIT,
    "history":  [],
    "pressure": 0.0,   # akumulasi tekanan dari game (positif=naik, negatif=turun)
    "trend":    0,     # momentum: +1 uptrend, -1 downtrend, 0 netral
    "streak":   0,     # berapa tick berturut ke arah yang sama
}

def load_price():
    d = load_json(PRICE_FILE, default=_PRICE_FILE_DEFAULT.copy())
    for k, v in _PRICE_FILE_DEFAULT.items():
        d.setdefault(k, v)
    return d

def save_price(d):
    save_json(PRICE_FILE, d)

def coin_to_idr(coin_amount: int) -> int:
    return int((coin_amount / 100) * load_price()["price"])

# ── Trigger tekanan harga dari game ───────────────────
def price_trigger(pressure_delta: float, reason: str = ""):
    """Tambah tekanan dari aktivitas game. Diserap saat tick berikutnya."""
    data = load_price()
    data["pressure"] = data.get("pressure", 0.0) + pressure_delta
    save_price(data)
    print(f"[MARKET] {reason} | Δ={pressure_delta:+.1f} | acc={data['pressure']:+.1f}")

# ── Engine harga — dipanggil tiap 2 menit ─────────────
def _calc_new_price(current: int, supply: int, pressure: float,
                    trend: int, streak: int) -> tuple:
    """
    Simulasi pasar palsu (fake market) yang terasa organik:

    Komponen:
    1. RANDOM WALK  — gerak acak ±_TICK_MAX_PCT (basis volatilitas)
    2. MOMENTUM     — jika naik beberapa tick berturut, ada bias lanjut naik (FOMO)
    3. REVERSAL     — semakin lama satu arah, makin besar peluang berbalik
    4. SUPPLY DRAG  — supply > _SUPPLY_INIT menekan harga turun perlahan
    5. GAME PRESSURE— tekanan akumulasi dari aktivitas game
    6. MEAN REVERT  — tarikan lemah kembali ke _PRICE_INITIAL agar tidak stuck ekstrem

    Hard cap/floor diterapkan di akhir.
    """
    # 1. Random walk
    rand_pct   = random.uniform(-_TICK_MAX_PCT, _TICK_MAX_PCT)
    rand_move  = rand_pct * current

    # 2. Momentum bias — makin panjang streak makin kuat tapi makin mungkin reverse
    momentum_strength = min(abs(streak), 4) * 0.005   # max +2% bias
    momentum_move = trend * momentum_strength * current

    # 3. Reversal probability — streak > 3 tick mulai ada peluang berbalik
    reversal_move = 0
    if abs(streak) >= 3:
        # makin panjang streak, makin besar counter-move
        rev_strength = min(abs(streak) - 2, 5) * 0.004
        # probabilitas reversal naik seiring streak
        rev_chance = min(0.15 * (abs(streak) - 2), 0.60)
        if random.random() < rev_chance:
            reversal_move = -trend * rev_strength * current

    # 4. Supply drag
    supply_ratio  = (supply - _SUPPLY_INIT) / max(_SUPPLY_INIT, 1)
    supply_move   = -supply_ratio * 50

    # 5. Game pressure (dikonsumsi 60% per tick, sisanya carry-over)
    pressure_move = pressure * 0.6

    # 6. Mean reversion — lemah, hanya aktif jika harga terlalu jauh dari tengah
    mid           = (_PRICE_CAP + _PRICE_FLOOR) / 2   # ~8.000
    distance_pct  = (current - mid) / mid
    revert_move   = -distance_pct * 0.008 * current

    raw = (current + rand_move + momentum_move + reversal_move
           + supply_move + pressure_move + revert_move)

    # Clamp ke [FLOOR, CAP]
    new_price = max(_PRICE_FLOOR, min(_PRICE_CAP, int(round(raw))))

    # Update momentum state
    delta = new_price - current
    if delta > 0:
        new_trend  = 1
        new_streak = streak + 1 if trend == 1 else 1
    elif delta < 0:
        new_trend  = -1
        new_streak = streak - 1 if trend == -1 else -1
    else:
        new_trend  = trend
        new_streak = 0

    return new_price, new_trend, new_streak

# ── Auto-tick setiap 2 menit ──────────────────────────
def market_tick() -> int:
    data     = load_price()
    pressure = data.get("pressure", 0.0)
    trend    = data.get("trend", 0)
    streak   = data.get("streak", 0)

    new_price, new_trend, new_streak = _calc_new_price(
        data["price"], data["supply"], pressure, trend, streak
    )

    data["price"]    = new_price
    data["pressure"] = pressure * 0.4   # sisa 40% carry-over ke tick berikutnya
    data["trend"]    = new_trend
    data["streak"]   = new_streak
    hist = data.get("history", [])
    hist.append(new_price)
    data["history"]  = hist[-144:]      # 144 titik ≈ 4.8 jam riwayat
    save_price(data)
    return new_price

@tasks.loop(seconds=10)
async def auto_price_update():
    market_tick()

def burn_coins(amount: int):
    """
    Bcash di-burn → supply turun → harga naik.
    (Burn terjadi saat: lotre, slot kalah, trade lose, convert, buy item, duel)
    Semakin banyak di-burn, semakin besar kenaikan harga.
    """
    data = load_price()
    data["supply"] = max(1, data["supply"] - amount)
    save_price(data)
    # Supply turun → bullish trigger (diperkuat: 0.02 per Bcash, min 1.0)
    pressure_delta = max(1.0, amount * 0.02)
    price_trigger(pressure_delta, f"burn {amount} Bcash")

def mint_coins(amount: int):
    """
    Bcash baru masuk sirkulasi → supply naik → harga turun.
    (Mint terjadi saat: admin givecoin, daily reward, mining reward, rain, welcome bonus)
    Semakin banyak dicetak, semakin besar tekanan turun harga.
    """
    data = load_price()
    data["supply"] = data["supply"] + amount
    save_price(data)
    # Supply naik → bearish trigger (diperkuat: -0.015 per Bcash, min -0.5)
    pressure_delta = min(-0.5, -amount * 0.015)
    price_trigger(pressure_delta, f"mint {amount} Bcash")

# ── Commands ──────────────────────────────────────────────
@bot.command(name="convertcoin")
async def convert_coin(ctx, amount: int = None):
    if not is_game_channel(ctx):
        return await ctx.send(game_channel_msg(ctx), delete_after=8)

    # Hitung minimum Bcash agar nilai IDR >= 50.000
    current_price = load_price()["price"]
    min_bcash = math.ceil(50000 / (current_price / 100))   # Bcash yang nilainya = Rp50.000

    if not amount:
        return await ctx.send(
            f"❌ Contoh: `!convertcoin {min_bcash}`\n"
            f"💡 Minimum WD: **Rp50.000** = **{min_bcash:,} Bcash** (harga saat ini Rp{current_price:,}/100)"
        )

    idr_preview = int((amount / 100) * current_price)
    if idr_preview < 50000:
        return await ctx.send(
            f"❌ Minimum penarikan **Rp50.000**!\n"
            f"Kamu mau convert **{amount:,} Bcash** = **Rp{idr_preview:,}** — belum cukup.\n"
            f"💡 Kamu butuh minimal **{min_bcash:,} Bcash** (≈ Rp50.000 saat ini)."
        )

    uid = str(ctx.author.id)
    ensure_coins(uid)
    bal = get_coins(uid)
    if bal < amount:
        return await ctx.send(f"❌ Coin tidak cukup! Saldo kamu: **{bal:,} Bcash**, butuh: **{amount:,} Bcash**.")

    idr = coin_to_idr(amount)

    # Potong coin, masuk ke admin bank, burn sisanya (untuk pengaruhi supply)
    add_coins(uid, -amount)
    add_coins(ADMIN_BANK_ID, +amount)   # kekalahan/convert → masuk admin bank
    burn_coins(amount)                   # tetap burn untuk pengaruhi harga
    price_trigger(+amount * 0.8, f"convert {amount} Bcash ke IDR")
    log_history(uid, f"💱 WD ke IDR (Rp{idr:,})", -amount)
    log_history(ADMIN_BANK_ID, f"💱 WD masuk dari {ctx.author.display_name}", +amount)

    await ctx.send(f"✅ Convert **{amount:,} Bcash** (≈ **Rp{idr:,}**) berhasil. Cek DM kamu untuk isi data penarikan!")

    # Buka DM untuk isi form penarikan
    try:
        dm = await ctx.author.create_dm()

        EWALLET_OPTIONS = {
            "1": "DANA",
            "2": "OVO",
            "3": "ShopeePay",
        }

        def check_dm(m):
            return m.author.id == ctx.author.id and isinstance(m.channel, discord.DMChannel)

        await dm.send(
            f"💱 **Form Penarikan Bcash**\n\n"
            f"💰 Jumlah: **{amount:,} Bcash**\n"
            f"💵 Nilai: **Rp{idr:,}**\n"
            f"📊 Harga saat convert: **Rp{current_price:,}** / 100 Bcash\n\n"
            f"Pilih **e-wallet** tujuan penarikan:\n"
            f"`1` — DANA\n"
            f"`2` — OVO\n"
            f"`3` — ShopeePay\n\n"
            f"Ketik angka pilihanmu (1/2/3):"
        )

        try:
            pilih_msg = await bot.wait_for("message", check=check_dm, timeout=60)
            pilihan = pilih_msg.content.strip()
            if pilihan not in EWALLET_OPTIONS:
                await dm.send("❌ Pilihan tidak valid. Penarikan dibatalkan. Ulangi dengan `!convertcoin`.")
                return
            ewallet = EWALLET_OPTIONS[pilihan]

            await dm.send(f"📱 Ketik **nomor {ewallet}** kamu (contoh: 0812xxxxxxxx):")
            nomor_msg = await bot.wait_for("message", check=check_dm, timeout=120)
            nomor = nomor_msg.content.strip()[:20]

            await dm.send(f"👤 Ketik **nama pemilik akun {ewallet}** (sesuai yang terdaftar):")
            nama_msg = await bot.wait_for("message", check=check_dm, timeout=120)
            nama_akun = nama_msg.content.strip()[:100]

            # Simpan withdrawal request
            withdrawals = load_json("withdrawals.json", default=[])
            entry = {
                "user_id": str(ctx.author.id),
                "username": ctx.author.display_name,
                "amount_bcash": amount,
                "amount_idr": idr,
                "price_at_convert": current_price,
                "ewallet": ewallet,
                "nomor": nomor,
                "nama_akun": nama_akun,
                "time": datetime.datetime.utcnow().strftime("%d/%m/%Y %H:%M"),
                "status": "pending"
            }
            withdrawals.append(entry)
            save_json("withdrawals.json", withdrawals)

            # Konfirmasi ke user
            konfirm = discord.Embed(
                title="✅ Request Penarikan Diterima!",
                color=discord.Color.green()
            )
            konfirm.add_field(name="💰 Jumlah", value=f"{amount:,} Bcash", inline=True)
            konfirm.add_field(name="💵 Nilai IDR", value=f"Rp{idr:,}", inline=True)
            konfirm.add_field(name="📲 E-Wallet", value=ewallet, inline=True)
            konfirm.add_field(name="📱 Nomor", value=nomor, inline=True)
            konfirm.add_field(name="👤 Nama Akun", value=nama_akun, inline=True)
            konfirm.set_footer(text="Admin akan memproses dalam 1×24 jam • Asisten Lurah BFL")
            await dm.send(embed=konfirm)

            # Notif ke owner/admin
            try:
                owner = await bot.fetch_user(OWNER_ID)
                notif = discord.Embed(
                    title="💸 Request Penarikan Baru!",
                    color=discord.Color.orange()
                )
                notif.add_field(name="👤 User", value=f"{ctx.author.mention} (`{ctx.author.id}`)", inline=False)
                notif.add_field(name="💰 Bcash", value=f"{amount:,} Bcash", inline=True)
                notif.add_field(name="💵 IDR", value=f"Rp{idr:,}", inline=True)
                notif.add_field(name="📲 E-Wallet", value=ewallet, inline=True)
                notif.add_field(name="📱 Nomor", value=nomor, inline=True)
                notif.add_field(name="👤 Nama Akun", value=nama_akun, inline=True)
                notif.set_footer(text=f"Waktu: {entry['time']} | Harga: Rp{current_price:,}/100 Bcash")
                await owner.send(embed=notif)
            except Exception:
                pass

        except asyncio.TimeoutError:
            await dm.send(
                "⏰ Timeout mengisi form penarikan.\n"
                "Bcash sudah dipotong. Hubungi admin secara manual untuk konfirmasi penarikan."
            )

    except discord.Forbidden:
        await ctx.send(
            f"⚠️ {ctx.author.mention} DM kamu tertutup! Buka DM bot dan hubungi admin "
            f"untuk konfirmasi penarikan **{amount:,} Bcash (Rp{idr:,})**."
        )

@bot.command(name="setprice")
async def setprice(ctx, new_price: int = None):
    """Admin set harga pasar langsung (override manual)."""
    if not is_admin(ctx.author):
        return await ctx.send("❌ Admin only.")
    if not new_price or new_price < _PRICE_FLOOR:
        return await ctx.send(f"❌ Contoh: `!setprice 10000` (Rp{_PRICE_FLOOR:,}–Rp{_PRICE_CAP:,})")
    data = load_price()
    new_price         = min(new_price, _PRICE_CAP)
    data["price"]     = new_price
    data["pressure"]  = 0.0
    data["trend"]     = 0
    data["streak"]    = 0
    save_price(data)
    await ctx.send(f"✅ Harga Bcash diset ke **Rp{new_price:,}** / 100 Bcash. Momentum direset.")

@bot.command(name="burncoin", aliases=["burn", "burnbcash"])
async def burncoin_cmd(ctx, amount: str = None):
    """
    Admin burn Bcash dari saldo admin bank sendiri → supply turun → harga naik.
    Bisa dipakai di server maupun DM.
    Format: !burncoin <jumlah>
    """
    if not is_admin(ctx.author):
        await ctx.send("❌ Hanya admin yang bisa burn coin.")
        return

    if not amount or not amount.replace(".", "").replace(",", "").isdigit():
        await ctx.send(
            "❌ Format: `!burncoin <jumlah>`\n"
            "Contoh: `!burncoin 500`\n\n"
            "🔥 Burn = hancurkan Bcash dari saldo admin bank → supply turun → **harga naik**!"
        )
        return

    amt = int(amount.replace(".", "").replace(",", ""))
    if amt < 1:
        return await ctx.send("❌ Jumlah burn minimal 1 Bcash.")

    ensure_coins(ADMIN_BANK_ID)
    admin_bal = get_coins(ADMIN_BANK_ID)
    if admin_bal < amt:
        return await ctx.send(
            f"❌ Saldo admin bank tidak cukup!\n"
            f"Saldo admin: **{admin_bal:,} Bcash** | Mau burn: **{amt:,} Bcash**"
        )

    price_before = load_price()["price"]

    # Kurangi saldo admin bank & burn
    add_coins(ADMIN_BANK_ID, -amt)
    burn_coins(amt)
    log_history(ADMIN_BANK_ID, f"🔥 Admin burn {amt:,} Bcash", -amt)

    price_after = load_price()["price"]
    admin_bal_after = get_coins(ADMIN_BANK_ID)

    embed = discord.Embed(
        title="🔥 COIN BURN BERHASIL",
        description=(
            f"**{amt:,} Bcash** berhasil di-burn oleh admin!\n\n"
            f"Supply berkurang → harga Bcash terdorong naik."
        ),
        color=discord.Color.orange()
    )
    embed.add_field(name="🔥 Jumlah Dibakar",    value=f"**{amt:,} Bcash**",              inline=True)
    embed.add_field(name="💰 Saldo Admin Sisa",   value=f"**{admin_bal_after:,} Bcash**",  inline=True)
    embed.add_field(name="📊 Harga Sebelum",      value=f"Rp{price_before:,}",             inline=True)
    embed.add_field(name="📈 Harga Sekarang",     value=f"Rp{price_after:,}",              inline=True)
    delta = price_after - price_before
    arrow = "📈" if delta >= 0 else "📉"
    embed.add_field(name=f"{arrow} Perubahan Harga", value=f"**{'+' if delta >= 0 else ''}{delta:,}**", inline=True)
    embed.set_footer(text=f"Dibakar oleh {ctx.author.display_name} • Asisten Lurah BFL")
    await ctx.send(embed=embed)

@bot.command(name="price")
async def price_cmd(ctx):
    data  = load_price()
    price = data["price"]
    hist  = data.get("history", [price])
    if len(hist) >= 2:
        prev = hist[-2]
        if price > prev:   arrow = "📈"
        elif price < prev: arrow = "📉"
        else:              arrow = "➡️"
    else:
        arrow = "➡️"
    await ctx.send(f"{arrow} **Harga Bcash: Rp{price:,}** / 100 Bcash")

@bot.command(name="checkbalance")
async def checkbalance(ctx, target: str = None):
    """Admin cek saldo user. Bisa pakai @mention di server atau user_id di DM."""
    if not is_admin(ctx.author):
        return await ctx.send("❌ Admin only")
    if not target:
        return await ctx.send("Gunakan `!checkbalance @user` atau `!checkbalance <user_id>`")
    # Resolve user — support mention dan raw user_id
    raw_id = target.strip("<@!>")
    if not raw_id.isdigit():
        return await ctx.send("❌ Gunakan mention `@user` atau ID numerik.")
    try:
        user = await bot.fetch_user(int(raw_id))
    except Exception:
        return await ctx.send("❌ User tidak ditemukan.")
    bal = get_coins(str(user.id))
    price = load_price().get("price", 10000)
    idr   = int((bal / 100) * price)
    await ctx.send(
        f"💰 **{user.display_name}** (`{user.id}`)\n"
        f"Saldo: **{bal:,} Bcash** (≈ Rp{idr:,})"
    )

@bot.command(name="deposit")
async def deposit_cmd(ctx, amount:int=None):
    if not amount or amount < 100:
        return await ctx.send("❌ Minimum deposit 100 Bcash (Rp10.000)")
    price = load_price().get("price",10000)
    total = int((amount/100)*price)
    await ctx.author.send(f"📥 **Deposit Request**\nJumlah: **{amount} Bcash**\nTransfer: **Rp{total:,}**\nKirim bukti pembayaran ke admin untuk diproses.")

@bot.command(name="setspamchannel")
async def set_spam_channel(ctx, channel_id:int=None):
    global SPAM_CHANNEL_ID
    if not isinstance(ctx.channel, discord.DMChannel):
        return await ctx.send("DM only")
    if not is_admin(ctx.author):
        return await ctx.send("❌ Admin only")
    SPAM_CHANNEL_ID = channel_id
    await ctx.send(f"✅ Spam channel diubah ke {channel_id}")

@bot.command(name="slot")
async def slot_game(ctx, bet:int=None):
    if not is_game_channel(ctx):
        return await ctx.send(game_channel_msg(ctx), delete_after=8)
    if not bet or bet < 1:
        return await ctx.send("❌ Min bet 1 Bcash")
    uid = str(ctx.author.id)
    ensure_coins(uid)
    balance = get_coins(uid)
    if balance < bet:
        return await ctx.send(f"❌ Coin tidak cukup! Saldo kamu: **{balance:,} coin**, butuh: **{bet:,} coin**.")

    add_coins(uid, -bet)
    log_history(uid, f"🎰 Slot bet", -bet)
    mark_activity(uid)
    bonus = give_firstplay_bonus(uid, ctx.author.display_name)
    if bonus:
        await ctx.send(f"🎮 {ctx.author.mention} Selamat datang! Kamu dapat **+{bonus} Bcash** bonus pertama main game!", delete_after=10)

    roll = random.randint(1, 100)
    if roll <= 45:
        multi  = random.choice([1, 1.5, 2])
        reward = int(bet * multi)
        # Cek saldo admin bank
        ensure_coins(ADMIN_BANK_ID)
        admin_bal = get_coins(ADMIN_BANK_ID)
        if admin_bal < reward:
            # Admin bank tidak cukup → kembalikan bet user, batalkan
            add_coins(uid, bet)
            return await ctx.send("⚠️ Saldo admin bank tidak mencukupi saat ini. Bet dikembalikan.")
        add_coins(ADMIN_BANK_ID, -reward)
        add_coins(uid, reward)
        log_history(uid, f"🎰 Slot menang (x{multi})", +reward)
        log_history(ADMIN_BANK_ID, f"🎰 Bayar slot {ctx.author.display_name} (x{multi})", -reward)
        # 🪙 WIN: banyak Bcash masuk ke user dari admin → sedikit bearish (lebih banyak beredar)
        price_trigger(-bet * 0.4, f"slot WIN x{multi} bet={bet}")
        msg = f"🎰 JACKPOT! Menang **{reward} Bcash** (x{multi})"
    else:
        # Kalah: bet masuk ke admin bank, lalu burn untuk pengaruhi supply/harga
        add_coins(ADMIN_BANK_ID, +bet)
        burn_coins(bet)
        log_history(uid, "🎰 Slot kalah", -bet)
        log_history(ADMIN_BANK_ID, f"🎰 Pot masuk dari {ctx.author.display_name} (slot kalah)", +bet)
        # 🪙 LOSE: bet di-burn → supply turun → bullish
        price_trigger(+bet * 0.6, f"slot LOSE burn={bet}")
        msg = f"💀 Kalah **{bet} Bcash**"
    await ctx.send(msg)
    try:
        await ctx.author.send(f"💰 Saldo kamu sekarang: **{get_coins(uid):,} Bcash**")
    except Exception:
        pass

# ═══════════════════════════════════════════════════════
#  GAME — COIN FLIP (!coinflip)
# ═══════════════════════════════════════════════════════
_CF_HEADS_ART = (
    "```\n"
    "  ╭──────────╮\n"
    "  │  👑 HEADS │\n"
    "  │  D E P A N│\n"
    "  ╰──────────╯\n"
    "```"
)
_CF_TAILS_ART = (
    "```\n"
    "  ╭──────────╮\n"
    "  │  ✦ TAILS │\n"
    "  │ B E L A K │\n"
    "  ╰──────────╯\n"
    "```"
)

@bot.command(name="coinflip", aliases=["cf", "flip", "koinflip"])
async def coinflip_cmd(ctx, pilihan: str = None, bet: int = None):
    if not is_game_channel(ctx):
        return await ctx.send(game_channel_msg(ctx), delete_after=8)

    if not pilihan or not bet:
        embed_help = discord.Embed(
            title="🪙 Coin Flip — Cara Main",
            description=(
                "Tebak sisi koin yang keluar — **heads** (depan) atau **tails** (belakang)!\n\n"
                "**Format:** `!coinflip <heads/tails> <bet>`\n"
                "**Contoh:** `!coinflip heads 5`\n\n"
                "💰 Bet **min 1 — max 10 Bcash**\n"
                "🏆 Menang → dapat **2× bet** dari admin bank\n"
                "🔥 Kalah → bet **di-burn** (harga Bcash naik!)\n\n"
                "**Alias:** `!cf` · `!flip` · `!koinflip`"
            ),
            color=discord.Color.gold()
        )
        embed_help.set_footer(text="Asisten Lurah BFL • Coin Flip | 50/50 Fair Game")
        return await ctx.send(embed=embed_help)

    pilihan = pilihan.lower().strip()
    alias_heads = ["heads", "head", "h", "depan", "muka"]
    alias_tails = ["tails", "tail", "t", "belakang", "ekor"]

    if pilihan not in alias_heads + alias_tails:
        return await ctx.send(
            "❌ Pilihan tidak valid!\n"
            "Ketik `heads` / `h` / `depan`  atau  `tails` / `t` / `belakang`\n"
            "Contoh: `!coinflip heads 5`"
        )
    if bet < 1 or bet > 10:
        return await ctx.send("❌ Bet min **1 Bcash**, max **10 Bcash**.")

    uid = str(ctx.author.id)
    ensure_coins(uid)
    bal = get_coins(uid)
    if bal < bet:
        return await ctx.send(
            f"❌ Bcash tidak cukup!\n"
            f"Saldo kamu: **{bal:,} Bcash** | Butuh: **{bet:,} Bcash**"
        )

    add_coins(uid, -bet)
    log_history(uid, "🪙 Coinflip bet", -bet)
    mark_activity(uid)
    bonus = give_firstplay_bonus(uid, ctx.author.display_name)
    if bonus:
        await ctx.send(f"🎮 {ctx.author.mention} Selamat datang! Kamu dapat **+{bonus} Bcash** bonus pertama main game!", delete_after=10)

    pick_heads = pilihan in alias_heads
    pick_label = "👑 HEADS (Depan)" if pick_heads else "✦ TAILS (Belakang)"

    # ── Embed animasi ──
    spin_frames = [
        ("🟡", "Koin dilempar ke udara..."),
        ("🔄", "Koin berputar cepat..."),
        ("💫", "Terus berputar..."),
        ("🔄", "Melambat..."),
        ("⭕", "Hampir mendarat..."),
        ("🟡", "Koin mendarat! 🎯"),
    ]
    delays = [0.55, 0.45, 0.45, 0.5, 0.6, 0.75]

    embed_spin = discord.Embed(
        title="🪙 COIN FLIP",
        description=(
            f"**{ctx.author.display_name}** melempar koin!\n\n"
            f"**Pilihan:** {pick_label}\n"
            f"**Taruhan:** {bet:,} Bcash\n\n"
            f"🟡 *Siap-siap...*"
        ),
        color=discord.Color.yellow()
    )
    embed_spin.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
    embed_spin.set_footer(text="Asisten Lurah BFL • Coin Flip | 50/50 Fair Game")
    msg = await ctx.send(embed=embed_spin)

    for (icon, label), delay in zip(spin_frames, delays):
        await asyncio.sleep(delay)
        embed_spin.description = (
            f"**{ctx.author.display_name}** melempar koin!\n\n"
            f"**Pilihan:** {pick_label}\n"
            f"**Taruhan:** {bet:,} Bcash\n\n"
            f"{icon} *{label}*"
        )
        try:
            await msg.edit(embed=embed_spin)
        except Exception:
            pass

    await asyncio.sleep(0.7)

    # ── Hasil ──
    result_heads = random.random() < 0.5
    player_wins  = (pick_heads == result_heads)
    result_label = "👑 HEADS (Depan)" if result_heads else "✦ TAILS (Belakang)"
    result_art   = _CF_HEADS_ART if result_heads else _CF_TAILS_ART

    if player_wins:
        reward = bet * 2
        ensure_coins(ADMIN_BANK_ID)
        admin_bal = get_coins(ADMIN_BANK_ID)
        if admin_bal < reward:
            add_coins(uid, bet)   # kembalikan bet
            embed_err = discord.Embed(
                title="⚠️ Coin Flip Dibatalkan",
                description="Saldo admin bank tidak mencukupi. Bet dikembalikan.",
                color=discord.Color.orange()
            )
            return await msg.edit(embed=embed_err)

        add_coins(ADMIN_BANK_ID, -reward)
        add_coins(uid, reward)
        log_history(uid, "🪙 Coinflip WIN (×2)", +reward)
        log_history(ADMIN_BANK_ID, f"🪙 Bayar coinflip {ctx.author.display_name}", -reward)
        price_trigger(-bet * 0.5, f"coinflip WIN bet={bet}")
        new_bal = get_coins(uid)

        embed_result = discord.Embed(
            title="🎉 COIN FLIP — MENANG!",
            description=(
                f"{result_art}\n"
                f"**Hasil:** {result_label}\n"
                f"**Pilihanmu:** {pick_label} ✅\n\n"
                f"💰 **+{reward:,} Bcash** masuk ke dompetmu!\n"
                f"📊 Saldo sekarang: **{new_bal:,} Bcash**"
            ),
            color=discord.Color.green()
        )
        embed_result.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
        embed_result.set_footer(text="Asisten Lurah BFL • Coin Flip | 🏆 Selamat!")
        await msg.edit(embed=embed_result)

    else:
        # Kalah: bet masuk ke admin bank, burn untuk pengaruhi supply
        add_coins(ADMIN_BANK_ID, +bet)
        burn_coins(bet)
        log_history(uid, "🪙 Coinflip LOSE", -bet)
        log_history(ADMIN_BANK_ID, f"🪙 Pot masuk dari {ctx.author.display_name} (coinflip kalah)", +bet)
        price_trigger(+bet * 0.8, f"coinflip LOSE burn={bet}")
        new_bal = get_coins(uid)

        embed_result = discord.Embed(
            title="💀 COIN FLIP — KALAH!",
            description=(
                f"{result_art}\n"
                f"**Hasil:** {result_label}\n"
                f"**Pilihanmu:** {pick_label} ❌\n\n"
                f"🔥 **{bet:,} Bcash** di-burn → harga Bcash naik sedikit!\n"
                f"📊 Saldo sekarang: **{new_bal:,} Bcash**"
            ),
            color=discord.Color.red()
        )
        embed_result.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
        embed_result.set_footer(text="Asisten Lurah BFL • Coin Flip | Coba lagi!")
        await msg.edit(embed=embed_result)




# ═══════════════════════════════════════════════════════
#  ACTIVITY TRACKER — untuk sistem pajak
# ═══════════════════════════════════════════════════════
def load_activity():
    return load_json(ACTIVITY_FILE, default={})

def save_activity(d):
    save_json(ACTIVITY_FILE, d)

def mark_activity(uid: str):
    """Tandai user sudah main game hari ini (UTC)."""
    uid = str(uid)
    data = load_activity()
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    data[uid] = today
    save_activity(data)

# ═══════════════════════════════════════════════════════
#  ANTI-SPAM TRADE — lock per user
# ═══════════════════════════════════════════════════════
_active_trades: set = set()   # set of uid yang sedang open trade

@bot.command(name="trade")
async def trade_cmd(ctx, direction:str=None, amount:int=None):
    if not is_game_channel(ctx):
        return await ctx.send(game_channel_msg(ctx), delete_after=8)
    if direction not in ["up", "down", "naik", "turun"]:
        return await ctx.send("Gunakan `!trade up/down <5-10>` | Contoh: `!trade up 5`")
    if not amount or amount < 5 or amount > 10:
        return await ctx.send("❌ Jumlah taruhan min **5** dan max **10** Bcash.")
    uid = str(ctx.author.id)
    if uid in _active_trades:
        return await ctx.send(f"⚠️ {ctx.author.mention} Kamu masih punya trade aktif! Tunggu hasilnya dulu.")
    ensure_coins(uid)
    balance = get_coins(uid)
    if balance < amount:
        return await ctx.send(f"❌ Coin tidak cukup! Saldo kamu: **{balance:,} coin**, butuh: **{amount:,} Bcash**.")
    _active_trades.add(uid)
    mark_activity(uid)
    add_coins(uid, -amount)
    log_history(uid, "📈 Trade taruhan", -amount)
    start = load_price()["price"]
    await ctx.send(f"📈 Trade dimulai! Taruhan **{amount} Bcash** | Harga awal: **Rp{start:,}** | Hasil dalam 1 menit...")
    await asyncio.sleep(60)
    _active_trades.discard(uid)
    end = load_price()["price"]
    result_up = end > start
    pick_up = direction in ["up", "naik"]
    if result_up == pick_up:
        reward = amount * 2
        ensure_coins(ADMIN_BANK_ID)
        admin_bal = get_coins(ADMIN_BANK_ID)
        if admin_bal < reward:
            add_coins(uid, amount)
            return await ctx.send("⚠️ Saldo admin bank tidak mencukupi. Bet dikembalikan.")
        add_coins(ADMIN_BANK_ID, -reward)
        add_coins(uid, reward)
        log_history(uid, f"📈 Trade WIN (Rp{start:,}→{end:,})", +reward)
        log_history(ADMIN_BANK_ID, f"📈 Bayar trade {ctx.author.display_name}", -reward)
        price_trigger(-amount * 1.0, f"trade WIN amount={amount}")
        await ctx.send(f"✅ Trade **WIN**! Harga Rp{start:,} → Rp{end:,} | Reward: **{reward} Bcash**")
        try:
            await ctx.author.send(f"💰 Saldo kamu sekarang: **{get_coins(uid):,} Bcash**")
        except Exception:
            pass
    else:
        add_coins(ADMIN_BANK_ID, +amount)
        burn_coins(amount)
        log_history(uid, f"📈 Trade LOSE (Rp{start:,}→{end:,})", -amount)
        log_history(ADMIN_BANK_ID, f"📈 Pot masuk dari {ctx.author.display_name} (trade kalah)", +amount)
        price_trigger(+amount * 1.2, f"trade LOSE burn={amount}")
        await ctx.send(f"❌ Trade **LOSE**! Harga Rp{start:,} → Rp{end:,}")
        try:
            await ctx.author.send(f"💰 Saldo kamu sekarang: **{get_coins(uid):,} Bcash**")
        except Exception:
            pass

# ═══════════════════════════════════════════════════════
#  BALAPAN KUDA (!balapan)
# ═══════════════════════════════════════════════════════
_active_races: dict = {}   # channel_id → race info (agar 1 race per channel)

@bot.command(name="balapan", aliases=["race", "kuda"])
async def balapan_cmd(ctx, pilihan: str = None, bet: int = None):
    if not is_game_channel(ctx):
        return await ctx.send(game_channel_msg(ctx), delete_after=8)

    if not pilihan or not bet:
        embed = discord.Embed(
            title="🏇 Balapan Kuda — Cara Main",
            description=(
                "Pilih kuda dan taruhkan Bcash kamu!\n\n"
                "**Format:** `!balapan <1/2> <bet>`\n"
                "**Contoh:** `!balapan 1 10`\n\n"
                "🐴 **Kuda 1** vs 🐎 **Kuda 2**\n"
                "💰 Bet **min 1 — max 15 Bcash**\n"
                "🎯 Menang → **×2 Bcash**\n"
                "⚡ Peluang menang: **45%** (apapun kuda yang dipilih)"
            ),
            color=discord.Color.orange()
        )
        embed.set_footer(text="Asisten Lurah BFL • Balapan Kuda")
        return await ctx.send(embed=embed)

    if pilihan not in ["1", "2"]:
        return await ctx.send("❌ Pilih kuda **1** atau **2**. Contoh: `!balapan 1 10`")
    if bet < 1 or bet > 15:
        return await ctx.send("❌ Bet min **1** dan max **15** Bcash.")

    uid = str(ctx.author.id)
    ensure_coins(uid)
    balance = get_coins(uid)
    if balance < bet:
        return await ctx.send(f"❌ Bcash tidak cukup! Saldo: **{balance:,}**, butuh: **{bet:,}**.")

    add_coins(uid, -bet)
    log_history(uid, f"🏇 Balapan Kuda bet kuda-{pilihan}", -bet)
    mark_activity(uid)

    # ── Tentukan hasil LEBIH DULU (45% user menang, 55% user kalah) ──
    user_won   = random.random() < 0.45
    # Kuda pemenang: jika user menang → kuda yang dipilih menang, jika kalah → kuda lawan
    winner_kuda = pilihan if user_won else ("2" if pilihan == "1" else "1")

    # ── Animasi balapan ──
    KUDA1, KUDA2 = "🐴", "🐎"
    FINISH = "🏁"
    TRACK  = 12   # panjang lintasan (karakter)

    pos1 = 0
    pos2 = 0

    def render(p1, p2):
        lane1 = " " * p1 + KUDA1 + "─" * (TRACK - p1)
        lane2 = " " * p2 + KUDA2 + "─" * (TRACK - p2)
        return (
            f"```\n"
            f"{FINISH} Lintasan Balapan BFL {FINISH}\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f" Kuda 1 ➜ {lane1}\n"
            f" Kuda 2 ➜ {lane2}\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"```"
        )

    embed_race = discord.Embed(
        title="🏇 BALAPAN DIMULAI!",
        description=render(pos1, pos2),
        color=discord.Color.orange()
    )
    embed_race.add_field(name="🎯 Pilihan Kamu", value=f"Kuda **{pilihan}**", inline=True)
    embed_race.add_field(name="💰 Taruhan", value=f"**{bet:,} Bcash**", inline=True)
    embed_race.set_footer(text="Asisten Lurah BFL • Balapan Kuda")
    msg = await ctx.send(embed=embed_race)

    # Animasi — 5 frame (kedua kuda bergerak acak, netral)
    for frame in range(5):
        await asyncio.sleep(1.2)
        pos1 = min(pos1 + random.randint(0, 3), TRACK - 1)
        pos2 = min(pos2 + random.randint(0, 3), TRACK - 1)
        embed_race.description = render(pos1, pos2)
        await msg.edit(embed=embed_race)

    # Frame terakhir — pemenang maju ke garis finish
    if winner_kuda == "1":
        pos1 = TRACK
    else:
        pos2 = TRACK

    # Frame terakhir — pemenang di garis finish
    embed_race.description = render(pos1, pos2)
    await msg.edit(embed=embed_race)
    await asyncio.sleep(0.8)

    # ── Hasil ──
    user_won = (pilihan == winner_kuda)
    kuda_icon = KUDA1 if winner_kuda == "1" else KUDA2

    if user_won:
        reward = bet * 2
        ensure_coins(ADMIN_BANK_ID)
        admin_bal = get_coins(ADMIN_BANK_ID)
        if admin_bal < reward:
            add_coins(uid, bet)
            embed_err = discord.Embed(
                title="⚠️ Balapan Dibatalkan",
                description="Saldo admin bank tidak mencukupi. Bet dikembalikan.",
                color=discord.Color.orange()
            )
            return await ctx.send(embed=embed_err)
        add_coins(ADMIN_BANK_ID, -reward)
        add_coins(uid, reward)
        log_history(uid, f"🏇 Balapan WIN kuda-{winner_kuda}", +reward)
        log_history(ADMIN_BANK_ID, f"🏇 Bayar balapan {ctx.author.display_name}", -reward)
        price_trigger(-bet * 0.5, f"balapan WIN bet={bet}")
        new_bal = get_coins(uid)
        embed_result = discord.Embed(
            title=f"🏆 {kuda_icon} KUDA {winner_kuda} MENANG!",
            description=(
                f"{ctx.author.mention} Tebakanmu **BENAR**!\n\n"
                f"💰 **+{reward:,} Bcash** masuk ke dompetmu!\n"
                f"📊 Saldo sekarang: **{new_bal:,} Bcash**"
            ),
            color=discord.Color.green()
        )
    else:
        add_coins(ADMIN_BANK_ID, +bet)
        burn_coins(bet)
        log_history(uid, f"🏇 Balapan LOSE kuda-{winner_kuda}", -bet)
        log_history(ADMIN_BANK_ID, f"🏇 Pot balapan dari {ctx.author.display_name}", +bet)
        price_trigger(+bet * 0.8, f"balapan LOSE burn={bet}")
        new_bal = get_coins(uid)
        embed_result = discord.Embed(
            title=f"💀 {kuda_icon} KUDA {winner_kuda} MENANG!",
            description=(
                f"{ctx.author.mention} Tebakanmu **SALAH**.\n\n"
                f"🔥 **{bet:,} Bcash** di-burn → harga Bcash naik!\n"
                f"📊 Saldo sekarang: **{new_bal:,} Bcash**"
            ),
            color=discord.Color.red()
        )

    embed_result.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
    embed_result.set_footer(text="Asisten Lurah BFL • Balapan Kuda")
    await ctx.send(embed=embed_result)



# ═══════════════════════════════════════════════════════
#  TRANSFER BCASH (!kirim)
# ═══════════════════════════════════════════════════════
@bot.command(name="kirim", aliases=["transfer", "send"])
async def kirim_bcash(ctx, target: discord.Member = None, amount: int = None):
    if not is_game_channel(ctx):
        return await ctx.send(game_channel_msg(ctx), delete_after=8)

    # Validasi input
    if not target or not amount:
        return await ctx.send(
            "❌ Format salah! Gunakan: `!kirim @user <jumlah>`\n"
            "Contoh: `!kirim @BFL 50`"
        )
    if target.bot:
        return await ctx.send("❌ Tidak bisa kirim Bcash ke bot.")
    if target.id == ctx.author.id:
        return await ctx.send("❌ Tidak bisa kirim Bcash ke diri sendiri.")
    if amount <= 0:
        return await ctx.send("❌ Jumlah harus lebih dari 0.")

    sender_uid = str(ctx.author.id)
    target_uid = str(target.id)

    ensure_coins(sender_uid)
    ensure_coins(target_uid)

    sender_bal = get_coins(sender_uid)
    if sender_bal < amount:
        return await ctx.send(
            f"❌ Bcash tidak cukup!\n"
            f"Saldo kamu: **{sender_bal:,} Bcash**, mau kirim: **{amount:,} Bcash**."
        )

    # Eksekusi transfer
    add_coins(sender_uid, -amount)
    add_coins(target_uid, +amount)
    log_history(sender_uid, f"💸 Kirim ke {target.display_name}", -amount)
    log_history(target_uid, f"💸 Terima dari {ctx.author.display_name}", +amount)
    sender_new = get_coins(sender_uid)
    target_new  = get_coins(target_uid)

    embed = discord.Embed(
        title="💸 Transfer Bcash Berhasil",
        color=discord.Color.green()
    )
    embed.add_field(name="Dari",   value=ctx.author.mention, inline=True)
    embed.add_field(name="Ke",     value=target.mention,     inline=True)
    embed.add_field(name="Jumlah", value=f"**{amount:,} Bcash**", inline=True)
    embed.add_field(name="Saldo kamu",       value=f"{sender_new:,} Bcash", inline=True)
    embed.add_field(name=f"Saldo {target.display_name}", value=f"{target_new:,} Bcash", inline=True)
    embed.set_footer(text="Asisten Lurah BFL • Bcash Transfer")
    await ctx.send(embed=embed)

    # Notifikasi DM ke penerima
    try:
        await target.send(
            f"💸 Kamu menerima **{amount:,} Bcash** dari **{ctx.author.display_name}**!\n"
            f"Saldo sekarang: **{target_new:,} Bcash**"
        )
    except discord.Forbidden:
        pass   # DM tertutup, skip saja


# ═══════════════════════════════════════════════════════
#  DAILY REWARD (!daily)
# ═══════════════════════════════════════════════════════
DAILY_REWARDS = {
    1: 1,   # Hari ke-1: 1 Bcash
    2: 1,
    3: 2,
    4: 3,
    5: 4,
    6: 5,
    7: 7,   # Hari ke-7 (streak penuh): 7 Bcash — bonus terbesar
}
DAILY_COOLDOWN_HOURS = 24

@bot.command(name="daily", aliases=["klaim", "claimdaily"])
async def daily_cmd(ctx):
    if not is_game_channel(ctx):
        return await ctx.send(game_channel_msg(ctx), delete_after=8)

    uid = str(ctx.author.id)
    ensure_coins(uid)

    daily_data = load_json(DAILY_FILE, default={})
    now        = datetime.datetime.utcnow()
    user_data  = daily_data.get(uid, {"last_claim": None, "streak": 0})

    last_claim_str = user_data.get("last_claim")
    streak         = user_data.get("streak", 0)

    if last_claim_str:
        last_claim = datetime.datetime.fromisoformat(last_claim_str)
        delta_hours = (now - last_claim).total_seconds() / 3600

        # Belum 24 jam → cooldown
        if delta_hours < DAILY_COOLDOWN_HOURS:
            sisa_detik = int((DAILY_COOLDOWN_HOURS * 3600) - (now - last_claim).total_seconds())
            h, r = divmod(sisa_detik, 3600)
            m, s = divmod(r, 60)
            return await ctx.send(
                f"⏳ Kamu sudah klaim hari ini!\n"
                f"Cooldown: **{h}j {m}m {s}d** lagi.\n"
                f"Streak saat ini: **{streak} hari** 🔥"
            )

        # Lebih dari 48 jam → streak reset
        if delta_hours >= 48:
            streak = 0

    # Hitung streak baru (maks 7 untuk reward tertinggi, lalu reset ke 1)
    streak = (streak % 7) + 1
    reward  = DAILY_REWARDS[streak]

    # Berikan Bcash dari admin bank
    ensure_coins(ADMIN_BANK_ID)
    admin_bal = get_coins(ADMIN_BANK_ID)
    if admin_bal < reward:
        return await ctx.send("⚠️ Saldo admin bank tidak mencukupi untuk daily reward saat ini.")
    add_coins(ADMIN_BANK_ID, -reward)
    add_coins(uid, reward)
    mint_coins(reward)   # daily reward → supply naik → sedikit bearish
    log_history(uid, f"🌅 Daily reward (streak {streak}/7)", +reward)
    log_history(ADMIN_BANK_ID, f"🌅 Daily reward → {ctx.author.display_name} streak {streak}", -reward)
    daily_data[uid] = {
        "last_claim": now.isoformat(),
        "streak":     streak,
    }
    save_json(DAILY_FILE, daily_data)

    new_bal = get_coins(uid)

    # Buat progress bar streak (7 kotak)
    bar = ""
    for i in range(1, 8):
        if i < streak:
            bar += "🟨"   # sudah lewat
        elif i == streak:
            bar += "⭐"   # hari ini
        else:
            bar += "⬜"   # belum

    # Pesan bonus hari ke-7
    if streak == 7:
        bonus_msg = "\n🎉 **STREAK SEMPURNA!** Kamu dapat bonus tertinggi minggu ini!"
    else:
        next_reward = DAILY_REWARDS[min(streak + 1, 7)]
        bonus_msg = f"\n➡️ Besok (hari ke-{streak + 1 if streak < 7 else 1}): **{next_reward} Bcash**"

    embed = discord.Embed(
        title="🌅 Daily Reward",
        description=f"{bar}",
        color=discord.Color.orange()
    )
    embed.add_field(name="🎁 Reward",    value=f"**+{reward} Bcash**",    inline=True)
    embed.add_field(name="🔥 Streak",    value=f"**{streak} / 7 hari**", inline=True)
    embed.add_field(name="💰 Saldo",     value=f"**{new_bal:,} Bcash**", inline=True)
    embed.add_field(
        name="📅 Jadwal Reward",
        value=(
            "Hari 1: 1 • Hari 2: 1 • Hari 3: 2\n"
            "Hari 4: 3 • Hari 5: 4 • Hari 6: 5\n"
            "⭐ **Hari 7: 7 Bcash** ⭐"
        ),
        inline=False
    )
    embed.set_thumbnail(url=ctx.author.display_avatar.url)
    embed.set_footer(text=f"Klaim lagi dalam 24 jam • Asisten Lurah BFL{bonus_msg}")
    await ctx.send(embed=embed)


# ═══════════════════════════════════════════════════════
#  RAIN BCASH (!rain) — Admin only
# ═══════════════════════════════════════════════════════
@bot.command(name="rain")
async def rain_bcash(ctx, total: int = None, max_users: int = 5):
    if not is_admin(ctx.author):
        return await ctx.send("❌ Hanya admin.", delete_after=5)
    if not total or total < 1:
        return await ctx.send(
            "❌ Format: `!rain <total_bcash> [jumlah_user]`\n"
            "Contoh: `!rain 100 5` → sebar 100 Bcash ke 5 user aktif di channel ini"
        )

    # Cek saldo admin bank cukup
    ensure_coins(ADMIN_BANK_ID)
    admin_bal = get_coins(ADMIN_BANK_ID)
    if admin_bal < total:
        return await ctx.send(f"❌ Saldo admin bank tidak cukup! Saldo: **{admin_bal:,} Bcash**, butuh: **{total:,} Bcash**.")

    # Scan 5 menit terakhir, hanya di channel tempat !rain diketik
    cutoff = datetime.datetime.utcnow() - datetime.timedelta(minutes=5)
    aktif = {}
    async for msg in ctx.channel.history(limit=200, after=cutoff):
        if (not msg.author.bot
                and msg.author.id != ctx.author.id
                and msg.author.id not in aktif):
            aktif[msg.author.id] = msg.author

    if not aktif:
        return await ctx.send(
            f"❌ Tidak ada user aktif dalam 5 menit terakhir di <#{ctx.channel.id}>."
        )

    pool     = list(aktif.values())
    winners  = random.sample(pool, min(max_users, len(pool)))
    per_user = total // len(winners)
    if per_user < 1:
        return await ctx.send(
            f"❌ Total terlalu kecil untuk dibagi ke {len(winners)} user. "
            f"Min **{len(winners)} Bcash**."
        )

    total_keluar = per_user * len(winners)
    # Potong saldo admin bank
    add_coins(ADMIN_BANK_ID, -total_keluar)
    log_history(ADMIN_BANK_ID, f"🌧️ Rain ke {len(winners)} user di #{ctx.channel.name}", -total_keluar)

    mention_list = []
    for w in winners:
        wuid = str(w.id)
        ensure_coins(wuid)
        add_coins(wuid, per_user)
        log_history(wuid, f"🌧️ Rain dari admin di #{ctx.channel.name}", +per_user)
        mention_list.append(w.mention)

    embed = discord.Embed(
        title="🌧️ RAIN BCASH!",
        description=f"Admin **{ctx.author.display_name}** menyebar Bcash di <#{ctx.channel.id}>!",
        color=discord.Color.blue()
    )
    embed.add_field(name="💰 Per User",    value=f"**{per_user:,} Bcash**",              inline=True)
    embed.add_field(name="👥 Penerima",    value=f"**{len(winners)} user**",              inline=True)
    embed.add_field(name="💸 Total Sebar", value=f"**{total_keluar:,} Bcash**",           inline=True)
    embed.add_field(name="🎉 Penerima",    value=" ".join(mention_list),                  inline=False)
    embed.set_footer(text=f"Aktif di #{ctx.channel.name} dalam 5 menit untuk kebagian rain berikutnya!")
    await ctx.send(embed=embed)


# ═══════════════════════════════════════════════════════
#  RIWAYAT TRANSAKSI (!history)
# ═══════════════════════════════════════════════════════
@bot.command(name="history", aliases=["riwayat", "log"])
async def history_cmd(ctx, member: discord.Member = None):
    if not is_game_channel(ctx):
        return await ctx.send(game_channel_msg(ctx), delete_after=8)

    if member and not is_admin(ctx.author):
        member = None

    target  = member or ctx.author
    uid     = str(target.id)
    data    = load_json(HISTORY_FILE, default={})
    entries = data.get(uid, [])

    if not entries:
        return await ctx.send(f"📭 Belum ada riwayat transaksi untuk **{target.display_name}**.")

    lines = []
    for e in entries[:10]:
        sign  = "+" if e["amount"] > 0 else ""
        arrow = "🟢" if e["amount"] > 0 else "🔴"
        lines.append(f"{arrow} `{e['time']}` {e['label']} **{sign}{e['amount']:,} Bcash**")

    embed = discord.Embed(
        title=f"📊 Riwayat Transaksi — {target.display_name}",
        description="\n".join(lines),
        color=discord.Color.blurple()
    )
    embed.set_thumbnail(url=target.display_avatar.url)
    embed.set_footer(text="Menampilkan 10 transaksi terakhir • Asisten Lurah BFL")
    await ctx.send(embed=embed)


# ═══════════════════════════════════════════════════════
#  DUEL BCASH (!duel)
# ═══════════════════════════════════════════════════════
_active_duels = set()

@bot.command(name="duel")
async def duel_cmd(ctx, target: discord.Member = None, amount: int = None):
    if not is_game_channel(ctx):
        return await ctx.send(game_channel_msg(ctx), delete_after=8)
    if not target or not amount:
        return await ctx.send("❌ Format: `!duel @user <jumlah>`\nContoh: `!duel @BFL 50`")
    if target.bot:
        return await ctx.send("❌ Tidak bisa duel dengan bot.")
    if target.id == ctx.author.id:
        return await ctx.send("❌ Tidak bisa duel dengan diri sendiri.")
    if amount < 1:
        return await ctx.send("❌ Jumlah taruhan min 1 Bcash.")

    ch_uid = str(ctx.author.id)
    tg_uid = str(target.id)

    if ch_uid in _active_duels or tg_uid in _active_duels:
        return await ctx.send("❌ Salah satu pemain sedang dalam duel aktif. Tunggu selesai.")

    ensure_coins(ch_uid); ensure_coins(tg_uid)
    ch_bal = get_coins(ch_uid)
    tg_bal = get_coins(tg_uid)

    if ch_bal < amount:
        return await ctx.send(f"❌ Bcash kamu tidak cukup! Saldo: **{ch_bal:,}**, butuh: **{amount:,}**.")
    if tg_bal < amount:
        return await ctx.send(f"❌ Bcash {target.display_name} tidak cukup! Saldo: **{tg_bal:,}**, butuh: **{amount:,}**.")

    _active_duels.add(ch_uid); _active_duels.add(tg_uid)
    await ctx.send(
        f"⚔️ {target.mention} kamu ditantang duel oleh {ctx.author.mention}!\n"
        f"Taruhan: **{amount:,} Bcash** | Ketik `ya` dalam 30 detik untuk menerima."
    )

    def check_accept(m):
        return (m.author.id == target.id and
                m.channel.id == ctx.channel.id and
                m.content.lower() in ["ya", "yes", "iya", "ok"])

    try:
        await bot.wait_for("message", check=check_accept, timeout=30)
    except asyncio.TimeoutError:
        _active_duels.discard(ch_uid); _active_duels.discard(tg_uid)
        return await ctx.send(f"⏰ {target.display_name} tidak merespons. Duel dibatalkan.")

    add_coins(ch_uid, -amount)
    add_coins(tg_uid, -amount)
    mark_activity(ch_uid)
    mark_activity(tg_uid)
    # Kedua bet masuk ke admin bank, lalu burn untuk pengaruhi supply/harga
    add_coins(ADMIN_BANK_ID, +amount)
    add_coins(ADMIN_BANK_ID, +amount)
    burn_coins(amount)
    burn_coins(amount)
    log_history(ADMIN_BANK_ID, f"⚔️ Pot duel dari {ctx.author.display_name} & {target.display_name}", +(amount * 2))

    anim_msg = await ctx.send("🪙 Lempar koin...")
    await asyncio.sleep(1)
    await anim_msg.edit(content="🪙 ~~Lempar koin...~~ ⚡ Menentukan pemenang...")
    await asyncio.sleep(1)

    winner, loser = random.choice([(ctx.author, target), (target, ctx.author)])
    w_uid = str(winner.id)
    l_uid = str(loser.id)

    # Hadiah pemenang dari admin bank
    hadiah = amount * 2
    ensure_coins(ADMIN_BANK_ID)
    admin_bal = get_coins(ADMIN_BANK_ID)
    if admin_bal >= hadiah:
        add_coins(ADMIN_BANK_ID, -hadiah)
        add_coins(w_uid, hadiah)
        log_history(ADMIN_BANK_ID, f"⚔️ Bayar duel pemenang {winner.display_name}", -hadiah)
    else:
        # Fallback: hadiah hanya dari pot yang ada (tanpa admin bank)
        add_coins(w_uid, hadiah)

    log_history(w_uid, f"⚔️ Duel menang vs {loser.display_name}",  +hadiah)
    log_history(l_uid, f"⚔️ Duel kalah vs {winner.display_name}", -amount)
    # 🪙 Duel: kedua bet di-burn → supply -2x amount → bullish
    # tapi pemenang dapat hadiah besar → sedikit bearish offset
    price_trigger(+amount * 0.8, f"duel result burn={amount*2}")
    _active_duels.discard(ch_uid); _active_duels.discard(tg_uid)

    embed = discord.Embed(title="⚔️ Hasil Duel!", color=discord.Color.gold())
    embed.add_field(name="🏆 Pemenang",     value=winner.mention,                inline=True)
    embed.add_field(name="💀 Kalah",        value=loser.mention,                 inline=True)
    embed.add_field(name="💰 Hadiah",       value=f"**{hadiah:,} Bcash**",       inline=True)

    embed.set_footer(text="Asisten Lurah BFL • Duel Bcash")
    await ctx.send(embed=embed)
    # Kirim saldo via DM ke masing-masing
    for _uid, _user in [(w_uid, winner), (l_uid, loser)]:
        try:
            await _user.send(f"💰 Saldo kamu sekarang: **{get_coins(_uid):,} Bcash**")
        except Exception:
            pass


# ═══════════════════════════════════════════════════════
#  PAJAK HARIAN — user tidak main game kena 10% per hari
# ═══════════════════════════════════════════════════════
@tasks.loop(hours=24)
async def daily_tax():
    """Jalankan setiap 24 jam. User yang tidak main game hari ini kena potongan pajak 10%."""
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    activity = load_activity()
    coins    = load_coins()
    taxed    = 0

    for uid, bal in list(coins.items()):
        if uid == ADMIN_BANK_ID:
            continue
        bal = int(bal)
        if bal <= 0:
            continue
        # Cek apakah user main game hari ini
        last_active = activity.get(str(uid))
        if last_active == today:
            continue   # sudah main → bebas pajak
        # Tidak main → potong 10%
        potongan = max(1, int(bal * 0.10))
        add_coins(str(uid), -potongan)
        add_coins(ADMIN_BANK_ID, +potongan)
        log_history(str(uid), "🏛️ Potongan pajak", -potongan)
        log_history(ADMIN_BANK_ID, f"🏛️ Pajak dari user {uid}", +potongan)
        taxed += 1

    print(f"[PAJAK] {today} — {taxed} user dikenai pajak 10%")

@daily_tax.before_loop
async def before_daily_tax():
    await bot.wait_until_ready()
    # Sinkronkan loop ke jam 00:00 UTC
    now = datetime.datetime.utcnow()
    next_midnight = (now + datetime.timedelta(days=1)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    await asyncio.sleep((next_midnight - now).total_seconds())

# ═══════════════════════════════════════════════════════
#  ADDKOIN — Admin tambah saldo admin bank
# ═══════════════════════════════════════════════════════
@bot.command(name="addkoin", aliases=["addbcash", "topupbank"])
async def addkoin_cmd(ctx, amount: str = None):
    """Admin tambah saldo admin bank langsung. Bisa di server atau DM."""
    if not is_admin(ctx.author):
        return await ctx.send("❌ Hanya admin.")
    if not amount or not amount.replace(".", "").replace(",", "").isdigit():
        return await ctx.send(
            "❌ Format: `!addkoin <jumlah>`\n"
            "Contoh: `!addkoin 5000`\n\n"
            "💡 Perintah ini langsung menambah saldo admin bank."
        )
    amt = int(amount.replace(".", "").replace(",", ""))
    if amt < 1:
        return await ctx.send("❌ Jumlah minimal 1 Bcash.")

    ensure_coins(ADMIN_BANK_ID)
    new_bal = add_coins(ADMIN_BANK_ID, amt)
    mint_coins(amt)
    log_history(ADMIN_BANK_ID, f"➕ Topup admin bank oleh {ctx.author.display_name}", +amt)

    embed = discord.Embed(
        title="✅ Saldo Admin Bank Ditambah",
        color=discord.Color.green()
    )
    embed.add_field(name="➕ Ditambahkan", value=f"**{amt:,} Bcash**",     inline=True)
    embed.add_field(name="💰 Saldo Baru",  value=f"**{new_bal:,} Bcash**", inline=True)
    embed.set_footer(text=f"Oleh {ctx.author.display_name} • Asisten Lurah BFL")
    await ctx.send(embed=embed)


# ═══════════════════════════════════════════════════════
#  GAME — TENDANG BOLA (!ball)
# ═══════════════════════════════════════════════════════

_BALL_KICK_FRAMES = [
    # Frame 1 — siap tendang
    ("```\n"
     "  ⚽         🧤[     ]\n"
     "  Bola: siap ditendang!\n"
     "```"),
    # Frame 2 — tendang!
    ("```\n"
     "  💥  ⚽→→→→ 🧤[     ]\n"
     "  Bola melayang...\n"
     "```"),
    # Frame 3 — meluncur
    ("```\n"
     "  💨       ⚽→ 🧤[     ]\n"
     "  Melesat deras!\n"
     "```"),
]

_BALL_GOAL_FRAME = (
    "```\n"
    "  🥅  💥⚽  🙆 GOLAAAAAS!\n"
    "  Kiper tidak bisa menghentikan!\n"
    "```"
)

_BALL_SAVE_FRAME = (
    "```\n"
    "  🥅  🤾✋⚽  DITANGKAP!\n"
    "  Kiper berhasil blok!\n"
    "```"
)

@bot.command(name="ball", aliases=["tendang", "goal"])
async def ball_game(ctx, bet: int = None):
    if not is_game_channel(ctx):
        return await ctx.send(game_channel_msg(ctx), delete_after=8)

    if not bet or bet < 1:
        embed = discord.Embed(
            title="⚽ Tendang Bola — Cara Main",
            description=(
                "Tendang bola ke gawang yang dijaga kiper!\n\n"
                "**Format:** `!ball <bet>`\n"
                "**Contoh:** `!ball 10`\n\n"
                "⚽ Kamu menendang bola ke gawang\n"
                "🧤 Kiper berusaha menghalang\n"
                "🎯 **Chance masuk: 42%**\n"
                "💰 Bet **min 1 — max 15 Bcash**\n"
                "🏆 Menang → **×2 Bcash**"
            ),
            color=discord.Color.green()
        )
        embed.set_footer(text="Asisten Lurah BFL • Ball Game")
        return await ctx.send(embed=embed)

    if bet < 1 or bet > 15:
        return await ctx.send("❌ Bet min **1** dan max **15** Bcash.")

    uid = str(ctx.author.id)
    ensure_coins(uid)
    balance = get_coins(uid)
    if balance < bet:
        return await ctx.send(f"❌ Bcash tidak cukup! Saldo: **{balance:,}**, butuh: **{bet:,}**.")

    add_coins(uid, -bet)
    log_history(uid, f"⚽ Ball bet", -bet)
    mark_activity(uid)
    bonus = give_firstplay_bonus(uid, ctx.author.display_name)
    if bonus:
        await ctx.send(f"🎮 {ctx.author.mention} Selamat datang! Kamu dapat **+{bonus} Bcash** bonus pertama main game!", delete_after=10)

    # Tentukan hasil lebih dulu (42% gol, 58% ditangkap)
    user_gol = random.random() < 0.42

    # Animasi tendangan
    anim_msg = await ctx.send(_BALL_KICK_FRAMES[0])
    await asyncio.sleep(0.9)
    await anim_msg.edit(content=_BALL_KICK_FRAMES[1])
    await asyncio.sleep(0.9)
    await anim_msg.edit(content=_BALL_KICK_FRAMES[2])
    await asyncio.sleep(0.8)

    if user_gol:
        await anim_msg.edit(content=_BALL_GOAL_FRAME)
        await asyncio.sleep(0.5)

        reward = bet * 2
        ensure_coins(ADMIN_BANK_ID)
        admin_bal = get_coins(ADMIN_BANK_ID)
        if admin_bal < reward:
            add_coins(uid, bet)
            return await ctx.send("⚠️ Saldo admin bank tidak mencukupi. Bet dikembalikan.")

        add_coins(ADMIN_BANK_ID, -reward)
        add_coins(uid, reward)
        log_history(uid, "⚽ Ball GOL! (×2)", +reward)
        log_history(ADMIN_BANK_ID, f"⚽ Bayar ball {ctx.author.display_name} (gol)", -reward)
        price_trigger(-bet * 0.4, f"ball GOL bet={bet}")
        new_bal = get_coins(uid)

        embed = discord.Embed(
            title="⚽ GOOOOL! Bola Masuk!",
            description=(
                f"{ctx.author.mention} berhasil menjebol gawang! Kiper tak berdaya! 🎉\n\n"
                f"💰 **+{reward:,} Bcash** masuk ke dompetmu!\n"
                f"📊 Saldo sekarang: **{new_bal:,} Bcash**"
            ),
            color=discord.Color.green()
        )
        embed.set_footer(text="Asisten Lurah BFL • Ball Game | ⚽ GOL!")
    else:
        await anim_msg.edit(content=_BALL_SAVE_FRAME)
        await asyncio.sleep(0.5)

        add_coins(ADMIN_BANK_ID, +bet)
        burn_coins(bet)
        log_history(uid, "⚽ Ball ditangkap", -bet)
        log_history(ADMIN_BANK_ID, f"⚽ Pot masuk dari {ctx.author.display_name} (ball saved)", +bet)
        price_trigger(+bet * 0.6, f"ball SAVED burn={bet}")
        new_bal = get_coins(uid)

        embed = discord.Embed(
            title="🧤 DITANGKAP! Kiper Jago!",
            description=(
                f"{ctx.author.mention} Kiper terlalu tangguh, bola tertangkap! 😤\n\n"
                f"🔥 **{bet:,} Bcash** di-burn → harga Bcash naik sedikit!\n"
                f"📊 Saldo sekarang: **{new_bal:,} Bcash**"
            ),
            color=discord.Color.red()
        )
        embed.set_footer(text="Asisten Lurah BFL • Ball Game | Coba lagi!")

    await ctx.send(embed=embed)
    try:
        await ctx.author.send(f"⚽ Hasil ball: {'GOL! 🥅' if user_gol else 'Ditangkap 🧤'} | Saldo: **{get_coins(uid):,} Bcash**")
    except Exception:
        pass


# ═══════════════════════════════════════════════════════
#  GAME — BERBURU (!hunt)
# ═══════════════════════════════════════════════════════

_HUNT_FRAMES = [
    "```\n🌲🌲🌲🌲🌲🌲🌲🌲\n🏹 Kamu memasuki hutan...\n🌲🌲🌲🌲🌲🌲🌲🌲\n```",
    "```\n🌲🌲🌲🌲🌲🌲🌲🌲\n🏹💨 Membidik target...\n🌲🦌🌲🐗🌲🦊🌲🌲\n```",
    "```\n🌲🌲🌲🌲🌲🌲🌲🌲\n🏹💥 TEMBAK!\n🌲🌲🌲🌲🌲🌲🌲🌲\n```",
]

_HUNT_RESULTS = [
    # (min_reward, max_reward, chance_pct, label, emoji)
    (2,  5,  40, "Buruan Kecil",   "🐇"),   # kelinci/ayam hutan
    (5,  7,  10, "Buruan Sedang",  "🦌"),   # rusa
    (15, 15,  5, "JACKPOT BESAR",  "🐗"),   # babi hutan langka
]
# Kalah: 40% — hilang modal 2 Bcash

@bot.command(name="hunt", aliases=["buru", "berburu"])
async def hunt_game(ctx):
    if not is_game_channel(ctx):
        return await ctx.send(game_channel_msg(ctx), delete_after=8)

    HUNT_COST = 2
    uid = str(ctx.author.id)
    ensure_coins(uid)
    balance = get_coins(uid)

    if balance < HUNT_COST:
        return await ctx.send(
            f"❌ Modal berburu kurang! Butuh **{HUNT_COST} Bcash**, saldo kamu: **{balance:,} Bcash**."
        )

    add_coins(uid, -HUNT_COST)
    log_history(uid, "🏹 Hunt modal", -HUNT_COST)
    mark_activity(uid)
    bonus = give_firstplay_bonus(uid, ctx.author.display_name)
    if bonus:
        await ctx.send(f"🎮 {ctx.author.mention} Selamat datang! Kamu dapat **+{bonus} Bcash** bonus pertama main game!", delete_after=10)

    # Animasi masuk hutan
    anim_msg = await ctx.send(_HUNT_FRAMES[0])
    await asyncio.sleep(1.0)
    await anim_msg.edit(content=_HUNT_FRAMES[1])
    await asyncio.sleep(1.0)
    await anim_msg.edit(content=_HUNT_FRAMES[2])
    await asyncio.sleep(0.8)

    # Tentukan hasil dengan weighted random
    # Chance: 40% kecil, 10% sedang, 5% jackpot, 40% kalah → total 95% win + 5% bonus → 45% menang, 40% kalah, 5% jackpot, 10% sedang
    roll = random.randint(1, 100)

    if roll <= 5:
        # Jackpot babi hutan (5%)
        reward = 15
        result_label = "🐗 JACKPOT BESAR — Babi Hutan Langka!"
        embed_color = discord.Color.gold()
        result_icon = "🏆"
        won = True
    elif roll <= 15:
        # Buruan sedang rusa (10%)
        reward = random.randint(5, 7)
        result_label = "🦌 Buruan Sedang — Rusa!"
        embed_color = discord.Color.green()
        result_icon = "🎯"
        won = True
    elif roll <= 55:
        # Buruan kecil (40%)
        reward = random.randint(2, 5)
        result_label = "🐇 Buruan Kecil — Kelinci Hutan!"
        embed_color = discord.Color.blurple()
        result_icon = "✅"
        won = True
    else:
        # Kalah (40%) — modal hangus
        reward = 0
        result_label = "💨 Target Kabur! Kamu pulang dengan tangan kosong."
        embed_color = discord.Color.red()
        result_icon = "❌"
        won = False

    if won:
        ensure_coins(ADMIN_BANK_ID)
        admin_bal = get_coins(ADMIN_BANK_ID)
        if admin_bal < reward:
            add_coins(uid, HUNT_COST)
            return await ctx.send("⚠️ Saldo admin bank tidak mencukupi. Modal berburu dikembalikan.")

        add_coins(ADMIN_BANK_ID, -reward)
        add_coins(uid, reward)
        log_history(uid, f"🏹 Hunt WIN — {result_label}", +reward)
        log_history(ADMIN_BANK_ID, f"🏹 Bayar hunt {ctx.author.display_name}", -reward)
        price_trigger(-HUNT_COST * 0.3, f"hunt WIN reward={reward}")
        new_bal = get_coins(uid)

        embed = discord.Embed(
            title=f"{result_icon} Hasil Berburu!",
            description=(
                f"{result_label}\n\n"
                f"{ctx.author.mention} berhasil membawa pulang buruan!\n"
                f"💰 **+{reward:,} Bcash** masuk ke dompetmu!\n"
                f"📊 Saldo sekarang: **{new_bal:,} Bcash**"
            ),
            color=embed_color
        )
        embed.set_footer(text="Asisten Lurah BFL • Hunt Game | Selamat Berburu!")
    else:
        add_coins(ADMIN_BANK_ID, +HUNT_COST)
        burn_coins(HUNT_COST)
        log_history(uid, "🏹 Hunt — target kabur", -HUNT_COST)
        log_history(ADMIN_BANK_ID, f"🏹 Pot masuk dari {ctx.author.display_name} (hunt kalah)", +HUNT_COST)
        price_trigger(+HUNT_COST * 0.6, f"hunt LOSE burn={HUNT_COST}")
        new_bal = get_coins(uid)

        embed = discord.Embed(
            title="💨 Buruan Kabur!",
            description=(
                f"{result_label}\n\n"
                f"Modal **{HUNT_COST} Bcash** hangus.\n"
                f"📊 Saldo sekarang: **{new_bal:,} Bcash**"
            ),
            color=embed_color
        )
        embed.set_footer(text="Asisten Lurah BFL • Hunt Game | Coba lagi!")

    await ctx.send(embed=embed)
    try:
        result_txt = f"+{reward} Bcash 🎯" if won else f"-{HUNT_COST} Bcash 💨"
        await ctx.author.send(f"🏹 Hasil berburu: {result_txt} | Saldo: **{get_coins(uid):,} Bcash**")
    except Exception:
        pass


# ═══════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════
#  GLOBAL ERROR HANDLER
# ═══════════════════════════════════════════════════════
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if hasattr(ctx.command, "on_error"):
        return
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Kamu tidak punya izin untuk command ini.", delete_after=5)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Argumen `{error.param.name}` diperlukan.", delete_after=8)
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Argumen tidak valid.", delete_after=8)
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏳ Cooldown! Coba lagi dalam **{error.retry_after:.1f}** detik.", delete_after=5)
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("❌ Kamu tidak memenuhi syarat untuk command ini.", delete_after=5)
    else:
        print(f"[ERROR] Command '{ctx.command}' by {ctx.author}: {error}")

bot.run(TOKEN)
