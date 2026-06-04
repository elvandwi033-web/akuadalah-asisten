# ═══════════════════════════════════════════════════════
#  ADDON FITUR BARU — Paste SEBELUM baris bot.run(TOKEN)
#  Kompatibel dengan bot_fixed.py (Asisten Lurah BFL)
#
#  FITUR:
#  1. React to Get Role
#  2. Auto Mod Anti Spam
#  3. Welcome Card & Leave Channel
#  4. Custom Nickname
#  5. Polling Sistem
# ═══════════════════════════════════════════════════════

# ── FILE DATABASE BARU ──
REACT_ROLE_FILE  = "react_roles.json"
AUTOMOD_FILE     = "automod.json"
WELCOME_CFG_FILE = "welcome_config.json"
POLLS_FILE       = "polls.json"

def load_react_roles():   return load_json(REACT_ROLE_FILE, default={})
def save_react_roles(d):  save_json(REACT_ROLE_FILE, d)
def load_automod():       return load_json(AUTOMOD_FILE, default={"enabled": True, "threshold": 5, "interval": 5, "mute_duration": 60})
def save_automod(d):      save_json(AUTOMOD_FILE, d)
def load_welcome_cfg():   return load_json(WELCOME_CFG_FILE, default={"welcome_channel": None, "leave_channel": None})
def save_welcome_cfg(d):  save_json(WELCOME_CFG_FILE, d)
def load_polls():         return load_json(POLLS_FILE, default={})
def save_polls(d):        save_json(POLLS_FILE, d)

# ═══════════════════════════════════════════════════════
#  1. REACT TO GET ROLE
# ═══════════════════════════════════════════════════════
# Commands:
#   !addreactrole <#channel> <message_id> <emoji> <@role>  — tambah react role
#   !removereactrole <message_id> <emoji>                   — hapus react role
#   !listreactrole                                           — daftar react role aktif

@bot.command(name="addreactrole", aliases=["arr"])
@commands.has_permissions(manage_roles=True)
async def add_react_role(ctx, channel: discord.TextChannel, message_id: int, emoji: str, role: discord.Role):
    """Tambah react-to-get-role pada sebuah pesan."""
    try:
        msg = await channel.fetch_message(message_id)
    except Exception:
        return await ctx.send("❌ Pesan tidak ditemukan.", delete_after=8)

    if role >= ctx.guild.me.top_role:
        return await ctx.send("❌ Role terlalu tinggi, bot tidak bisa memberikan role ini.", delete_after=8)

    await msg.add_reaction(emoji)

    data = load_react_roles()
    key  = str(message_id)
    if key not in data:
        data[key] = {"channel_id": channel.id, "roles": {}}
    data[key]["roles"][emoji] = role.id
    save_react_roles(data)

    embed = discord.Embed(
        title="✅ React Role Ditambahkan",
        description=(
            f"**Pesan:** [Jump]({msg.jump_url})\n"
            f"**Emoji:** {emoji}\n"
            f"**Role:** {role.mention}"
        ),
        color=discord.Color.green()
    )
    embed.set_footer(text="Asisten Lurah BFL • React Role")
    await ctx.send(embed=embed)


@bot.command(name="removereactrole", aliases=["rrr"])
@commands.has_permissions(manage_roles=True)
async def remove_react_role(ctx, message_id: int, emoji: str):
    """Hapus react-role dari sebuah pesan."""
    data = load_react_roles()
    key  = str(message_id)
    if key not in data or emoji not in data[key].get("roles", {}):
        return await ctx.send("❌ React role tidak ditemukan.", delete_after=8)

    del data[key]["roles"][emoji]
    if not data[key]["roles"]:
        del data[key]
    save_react_roles(data)
    await ctx.send(f"✅ React role `{emoji}` dihapus dari pesan `{message_id}`.", delete_after=8)


@bot.command(name="listreactrole", aliases=["lrr"])
@commands.has_permissions(manage_roles=True)
async def list_react_role(ctx):
    """Tampilkan semua react role aktif."""
    data = load_react_roles()
    if not data:
        return await ctx.send("📭 Tidak ada react role aktif.", delete_after=8)

    embed = discord.Embed(title="📋 Daftar React Role Aktif", color=discord.Color.blurple())
    for msg_id, val in data.items():
        ch = bot.get_channel(val["channel_id"])
        ch_mention = ch.mention if ch else f"<#{val['channel_id']}>"
        lines = []
        for emoji, role_id in val["roles"].items():
            role = ctx.guild.get_role(role_id)
            lines.append(f"{emoji} → {role.mention if role else role_id}")
        embed.add_field(
            name=f"Pesan ID: {msg_id} (di {ch_mention})",
            value="\n".join(lines) or "—",
            inline=False
        )
    embed.set_footer(text="Asisten Lurah BFL • React Role")
    await ctx.send(embed=embed)


@bot.event
async def on_raw_reaction_add(payload):
    if payload.member and payload.member.bot:
        return
    data = load_react_roles()
    key  = str(payload.message_id)
    if key not in data:
        return
    emoji_str = str(payload.emoji)
    role_id   = data[key]["roles"].get(emoji_str)
    if not role_id:
        return
    guild = bot.get_guild(payload.guild_id)
    if not guild:
        return
    role = guild.get_role(role_id)
    if not role:
        return
    member = payload.member or guild.get_member(payload.user_id)
    if member and role not in member.roles:
        try:
            await member.add_roles(role, reason="React Role")
        except Exception:
            pass


@bot.event
async def on_raw_reaction_remove(payload):
    data = load_react_roles()
    key  = str(payload.message_id)
    if key not in data:
        return
    emoji_str = str(payload.emoji)
    role_id   = data[key]["roles"].get(emoji_str)
    if not role_id:
        return
    guild = bot.get_guild(payload.guild_id)
    if not guild:
        return
    role   = guild.get_role(role_id)
    member = guild.get_member(payload.user_id)
    if member and role and role in member.roles:
        try:
            await member.remove_roles(role, reason="React Role dicopot")
        except Exception:
            pass


# ═══════════════════════════════════════════════════════
#  2. AUTO MOD ANTI SPAM
# ═══════════════════════════════════════════════════════
# Commands:
#   !automod on/off          — aktifkan/nonaktifkan auto mod
#   !automod threshold <n>   — set batas pesan (default 5)
#   !automod interval <s>    — set interval detik (default 5)
#   !automod mute <s>        — set durasi mute dalam detik (default 60)
#   !automod status          — lihat pengaturan saat ini

_spam_tracker: dict[int, list[float]] = {}   # user_id -> [timestamps]

async def _mute_member(member: discord.Member, duration_seconds: int, reason: str):
    """Timeout member dengan durasi tertentu."""
    until = datetime.datetime.utcnow() + datetime.timedelta(seconds=duration_seconds)
    try:
        await member.timeout(until, reason=reason)
    except Exception:
        pass


@bot.event
async def on_message_automod(message):
    """Dipanggil manual dari on_message — cek spam."""
    if message.author.bot or not message.guild:
        return

    cfg = load_automod()
    if not cfg.get("enabled", True):
        return

    threshold = cfg.get("threshold", 5)
    interval  = cfg.get("interval", 5)
    mute_dur  = cfg.get("mute_duration", 60)

    uid  = message.author.id
    now  = message.created_at.timestamp()

    if uid not in _spam_tracker:
        _spam_tracker[uid] = []

    # Hapus timestamp lama
    _spam_tracker[uid] = [t for t in _spam_tracker[uid] if now - t < interval]
    _spam_tracker[uid].append(now)

    if len(_spam_tracker[uid]) >= threshold:
        _spam_tracker[uid] = []   # reset tracker
        # Hapus pesan-pesan spam (ambil 10 terakhir dari channel)
        def is_spam(m):
            return m.author.id == uid

        try:
            deleted = await message.channel.purge(limit=20, check=is_spam)
        except Exception:
            deleted = []

        # Mute (timeout)
        if isinstance(message.author, discord.Member):
            await _mute_member(
                message.author,
                mute_dur,
                reason=f"Auto Mod: Spam ({threshold} pesan dalam {interval}s)"
            )

        menit = mute_dur // 60
        detik = mute_dur % 60
        dur_str = f"{menit}m {detik}s" if menit else f"{detik}s"

        embed = discord.Embed(
            title="🚫 Anti Spam Aktif!",
            description=(
                f"{message.author.mention} terdeteksi spam!\n\n"
                f"🗑️ **{len(deleted)} pesan** dihapus\n"
                f"⏳ Timeout selama **{dur_str}**"
            ),
            color=discord.Color.red(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_footer(text="Asisten Lurah BFL • Auto Mod")
        try:
            await message.channel.send(embed=embed, delete_after=10)
        except Exception:
            pass


@bot.command(name="automod")
@commands.has_permissions(manage_guild=True)
async def automod_cmd(ctx, subcommand: str = "status", value: str = None):
    """Kelola pengaturan Auto Mod anti spam."""
    cfg = load_automod()

    sub = subcommand.lower()

    if sub == "on":
        cfg["enabled"] = True
        save_automod(cfg)
        return await ctx.send("✅ Auto Mod **diaktifkan**.", delete_after=8)

    elif sub == "off":
        cfg["enabled"] = False
        save_automod(cfg)
        return await ctx.send("✅ Auto Mod **dinonaktifkan**.", delete_after=8)

    elif sub == "threshold":
        if not value or not value.isdigit():
            return await ctx.send("❌ Gunakan: `!automod threshold <angka>`", delete_after=8)
        cfg["threshold"] = max(2, int(value))
        save_automod(cfg)
        return await ctx.send(f"✅ Threshold spam diset ke **{cfg['threshold']} pesan**.", delete_after=8)

    elif sub == "interval":
        if not value or not value.isdigit():
            return await ctx.send("❌ Gunakan: `!automod interval <detik>`", delete_after=8)
        cfg["interval"] = max(1, int(value))
        save_automod(cfg)
        return await ctx.send(f"✅ Interval diset ke **{cfg['interval']} detik**.", delete_after=8)

    elif sub == "mute":
        if not value or not value.isdigit():
            return await ctx.send("❌ Gunakan: `!automod mute <detik>`", delete_after=8)
        cfg["mute_duration"] = max(10, int(value))
        save_automod(cfg)
        return await ctx.send(f"✅ Durasi mute diset ke **{cfg['mute_duration']} detik**.", delete_after=8)

    else:  # status
        status = "🟢 Aktif" if cfg.get("enabled", True) else "🔴 Nonaktif"
        embed  = discord.Embed(
            title="🛡️ Auto Mod Status",
            description=(
                f"**Status:** {status}\n"
                f"**Threshold:** {cfg.get('threshold', 5)} pesan\n"
                f"**Interval:** {cfg.get('interval', 5)} detik\n"
                f"**Durasi Mute:** {cfg.get('mute_duration', 60)} detik"
            ),
            color=discord.Color.orange()
        )
        embed.set_footer(text="Asisten Lurah BFL • Auto Mod")
        await ctx.send(embed=embed)


# ═══════════════════════════════════════════════════════
#  3. WELCOME CARD & LEAVE CHANNEL
# ═══════════════════════════════════════════════════════
# Commands:
#   !setwelcome <#channel>   — set channel welcome
#   !setleave <#channel>     — set channel leave
#   !welcometest             — test welcome card (hanya admin)
#   !leavetest               — test leave message (hanya admin)

def _generate_welcome_card(member: discord.Member, avatar_bytes: bytes) -> io.BytesIO:
    """Buat welcome card bergaya anime/clean dengan PIL."""
    W, H = 800, 250

    # Background gradient ungu-biru
    img  = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    for y in range(H):
        r = int(30  + (y / H) * 20)
        g = int(10  + (y / H) * 10)
        b = int(60  + (y / H) * 60)
        draw.line([(0, y), (W, y)], fill=(r, g, b, 255))

    # Ornamen garis dekoratif
    for i in range(0, W, 40):
        alpha_val = 15 + (i % 80)
        draw.line([(i, 0), (i - 60, H)], fill=(255, 255, 255, alpha_val), width=1)

    # Lingkaran avatar
    av_size = 150
    av_x, av_y = 50, (H - av_size) // 2

    # Ring warna emas
    ring_size = av_size + 10
    ring_x    = av_x - 5
    ring_y    = av_y - 5
    draw.ellipse([ring_x, ring_y, ring_x + ring_size, ring_y + ring_size],
                 outline=(255, 215, 0), width=4)

    # Avatar
    av_img = Image.open(io.BytesIO(avatar_bytes)).convert("RGBA").resize((av_size, av_size))
    mask   = Image.new("L", (av_size, av_size), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, av_size, av_size], fill=255)
    img.paste(av_img, (av_x, av_y), mask)

    # Teks
    try:
        font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34)
        font_med = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        font_sml = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except Exception:
        font_big = ImageFont.load_default()
        font_med = font_big
        font_sml = font_big

    tx = av_x + av_size + 30
    ty = H // 2 - 60

    draw.text((tx, ty),       "SELAMAT DATANG!",       font=font_med, fill=(255, 215, 0))
    draw.text((tx, ty + 35),  member.display_name,     font=font_big, fill=(255, 255, 255))
    draw.text((tx, ty + 80),  f"@{member.name}",       font=font_sml, fill=(180, 180, 210))
    draw.text((tx, ty + 105), f"Member ke-{member.guild.member_count} di {member.guild.name}",
              font=font_sml, fill=(150, 150, 180))

    buf = io.BytesIO()
    img.convert("RGB").save(buf, format="PNG")
    buf.seek(0)
    return buf


@bot.event
async def on_member_join(member):
    cfg = load_welcome_cfg()
    ch_id = cfg.get("welcome_channel")
    if not ch_id:
        return
    channel = member.guild.get_channel(int(ch_id))
    if not channel:
        return

    # Download avatar
    try:
        av_bytes = await member.display_avatar.read()
    except Exception:
        av_bytes = None

    embed = discord.Embed(
        title="👋 Member Baru Bergabung!",
        description=(
            f"Halo {member.mention}, selamat datang di **{member.guild.name}**!\n\n"
            f"📌 Kamu adalah member ke **{member.guild.member_count}**\n"
            f"📅 Akun dibuat: <t:{int(member.created_at.timestamp())}:R>"
        ),
        color=discord.Color.from_rgb(80, 60, 180),
        timestamp=datetime.datetime.utcnow()
    )
    embed.set_footer(text="Asisten Lurah BFL • Welcome")

    if av_bytes:
        try:
            card_buf = await asyncio.get_event_loop().run_in_executor(
                None, _generate_welcome_card, member, av_bytes
            )
            file  = discord.File(card_buf, filename="welcome.png")
            embed.set_image(url="attachment://welcome.png")
            await channel.send(file=file, embed=embed)
            return
        except Exception:
            pass

    # Fallback tanpa card
    embed.set_thumbnail(url=member.display_avatar.url)
    await channel.send(embed=embed)


@bot.event
async def on_member_remove(member):
    cfg   = load_welcome_cfg()
    ch_id = cfg.get("leave_channel")
    if not ch_id:
        return
    channel = member.guild.get_channel(int(ch_id))
    if not channel:
        return

    embed = discord.Embed(
        title="👋 Member Keluar",
        description=(
            f"**{member.display_name}** (`{member.name}`) telah meninggalkan server.\n\n"
            f"👥 Sisa member: **{member.guild.member_count}**"
        ),
        color=discord.Color.from_rgb(180, 60, 60),
        timestamp=datetime.datetime.utcnow()
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text="Asisten Lurah BFL • Leave")
    await channel.send(embed=embed)


@bot.command(name="setwelcome")
@commands.has_permissions(manage_guild=True)
async def set_welcome_channel(ctx, channel: discord.TextChannel):
    cfg = load_welcome_cfg()
    cfg["welcome_channel"] = channel.id
    save_welcome_cfg(cfg)
    await ctx.send(f"✅ Welcome channel diset ke {channel.mention}.", delete_after=8)


@bot.command(name="setleave")
@commands.has_permissions(manage_guild=True)
async def set_leave_channel(ctx, channel: discord.TextChannel):
    cfg = load_welcome_cfg()
    cfg["leave_channel"] = channel.id
    save_welcome_cfg(cfg)
    await ctx.send(f"✅ Leave channel diset ke {channel.mention}.", delete_after=8)


@bot.command(name="welcometest")
@commands.has_permissions(manage_guild=True)
async def welcome_test(ctx):
    """Test tampilan welcome card."""
    await on_member_join(ctx.author)
    await ctx.send("✅ Welcome card terkirim (test).", delete_after=5)


@bot.command(name="leavetest")
@commands.has_permissions(manage_guild=True)
async def leave_test(ctx):
    """Test pesan leave."""
    await on_member_remove(ctx.author)
    await ctx.send("✅ Leave message terkirim (test).", delete_after=5)


# ═══════════════════════════════════════════════════════
#  4. CUSTOM NICKNAME
# ═══════════════════════════════════════════════════════
# Commands:
#   !nick <nickname baru>    — ganti nickname sendiri
#   !nick reset              — reset nickname ke nama asli
#   !setnick @user <nick>    — admin: ganti nick orang lain

@bot.command(name="nick")
@commands.guild_only()
async def change_nick(ctx, *, new_nick: str = None):
    """Ganti nickname sendiri di server ini."""
    member = ctx.author

    if new_nick is None or new_nick.lower() == "reset":
        try:
            await member.edit(nick=None, reason="Reset nickname sendiri")
            return await ctx.send(f"✅ {member.mention} Nickname direset ke nama asli.", delete_after=8)
        except discord.Forbidden:
            return await ctx.send("❌ Bot tidak punya izin mengubah nickname kamu.", delete_after=8)

    if len(new_nick) > 32:
        return await ctx.send("❌ Nickname maksimal 32 karakter.", delete_after=8)

    # Cek apakah user mencoba mengubah nick orang lain
    if not is_admin(member) and member.top_role >= ctx.guild.me.top_role:
        return await ctx.send("❌ Kamu tidak bisa mengubah nickname ini.", delete_after=8)

    try:
        old_nick = member.display_name
        await member.edit(nick=new_nick, reason=f"Custom nick oleh {member}")
        embed = discord.Embed(
            title="✏️ Nickname Diubah",
            description=f"**{old_nick}** → **{new_nick}**",
            color=discord.Color.blurple()
        )
        embed.set_footer(text="Asisten Lurah BFL • Custom Nick")
        await ctx.send(embed=embed, delete_after=10)
    except discord.Forbidden:
        await ctx.send("❌ Bot tidak punya izin mengubah nickname kamu.", delete_after=8)


@bot.command(name="setnick")
@commands.has_permissions(manage_nicknames=True)
@commands.guild_only()
async def set_nick_admin(ctx, member: discord.Member, *, new_nick: str = None):
    """Admin: atur nickname orang lain. Gunakan 'reset' untuk hapus nickname."""
    if new_nick is None or new_nick.lower() == "reset":
        try:
            await member.edit(nick=None, reason=f"Nick reset oleh {ctx.author}")
            return await ctx.send(f"✅ Nickname {member.mention} direset.", delete_after=8)
        except discord.Forbidden:
            return await ctx.send("❌ Bot tidak bisa mengubah nickname member ini.", delete_after=8)

    if len(new_nick) > 32:
        return await ctx.send("❌ Nickname maksimal 32 karakter.", delete_after=8)

    try:
        await member.edit(nick=new_nick, reason=f"Set nick oleh {ctx.author}")
        await ctx.send(f"✅ Nickname {member.mention} diubah ke **{new_nick}**.", delete_after=8)
    except discord.Forbidden:
        await ctx.send("❌ Bot tidak bisa mengubah nickname member ini.", delete_after=8)


# ═══════════════════════════════════════════════════════
#  5. POLLING SISTEM
# ═══════════════════════════════════════════════════════
# Commands:
#   !poll <durasi_menit> <pertanyaan> | <pilihan1> | <pilihan2> ...
#       Contoh: !poll 10 Warna favorit? | Merah | Biru | Hijau
#   !endpoll <poll_id>   — akhiri poll lebih cepat (admin/pembuat)
#   !pollresult <poll_id> — lihat hasil poll

NUMBER_EMOJIS = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]

class PollView(View):
    def __init__(self, poll_id: str, options: list[str]):
        super().__init__(timeout=None)
        self.poll_id = poll_id
        for i, opt in enumerate(options[:10]):
            btn = discord.ui.Button(
                label=f"{NUMBER_EMOJIS[i]} {opt[:60]}",
                style=discord.ButtonStyle.primary,
                custom_id=f"poll_{poll_id}_{i}"
            )
            btn.callback = self._make_callback(i)
            self.add_item(btn)

    def _make_callback(self, option_idx: int):
        async def callback(interaction: discord.Interaction):
            polls = load_polls()
            poll  = polls.get(self.poll_id)
            if not poll:
                return await interaction.response.send_message("❌ Poll tidak ditemukan.", ephemeral=True)
            if poll.get("ended"):
                return await interaction.response.send_message("❌ Poll sudah berakhir.", ephemeral=True)

            uid    = str(interaction.user.id)
            votes  = poll.setdefault("votes", {})
            prev   = votes.get(uid)

            if prev == option_idx:
                # Toggle: batal vote
                del votes[uid]
                msg = f"✅ Kamu membatalkan vote **{poll['options'][option_idx]}**."
            else:
                votes[uid] = option_idx
                msg = f"✅ Kamu memilih **{poll['options'][option_idx]}**!"

            save_polls(polls)

            # Update embed
            try:
                ch  = bot.get_channel(int(poll["channel_id"]))
                m   = await ch.fetch_message(int(poll["message_id"]))
                await m.edit(embed=_build_poll_embed(poll, self.poll_id))
            except Exception:
                pass

            await interaction.response.send_message(msg, ephemeral=True)
        return callback


def _build_poll_embed(poll: dict, poll_id: str) -> discord.Embed:
    options = poll["options"]
    votes   = poll.get("votes", {})
    total   = len(votes)

    # Hitung suara per opsi
    counts = [0] * len(options)
    for v in votes.values():
        if 0 <= v < len(options):
            counts[v] += 1

    lines = []
    for i, opt in enumerate(options):
        pct  = (counts[i] / total * 100) if total else 0
        bar  = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        lines.append(f"{NUMBER_EMOJIS[i]} **{opt}**\n`{bar}` {counts[i]} suara ({pct:.1f}%)")

    end_dt  = datetime.datetime.fromisoformat(poll["end_time"])
    sisa    = end_dt - datetime.datetime.utcnow()
    sisa_s  = max(0, int(sisa.total_seconds()))
    h, rem  = divmod(sisa_s, 3600)
    m, s    = divmod(rem, 60)
    sisa_str = f"{h}j {m}m {s}d" if sisa_s > 0 else "Selesai"

    ended = poll.get("ended", False)
    color = discord.Color.green() if not ended else discord.Color.greyple()

    embed = discord.Embed(
        title=f"📊 {'[SELESAI] ' if ended else ''}POLL — {poll['question']}",
        description="\n\n".join(lines),
        color=color,
        timestamp=datetime.datetime.utcnow()
    )
    embed.add_field(name="⏳ Sisa Waktu", value=sisa_str, inline=True)
    embed.add_field(name="🗳️ Total Vote", value=str(total), inline=True)
    embed.add_field(name="🆔 Poll ID", value=f"`{poll_id}`", inline=True)
    embed.set_footer(text="Asisten Lurah BFL • Polling Sistem")
    return embed


@bot.command(name="poll")
@commands.guild_only()
async def create_poll(ctx, duration: int, *, content: str):
    """Buat poll baru.
    Contoh: !poll 10 Warna favorit? | Merah | Biru | Hijau
    """
    if "|" not in content:
        return await ctx.send(
            "❌ Format salah!\nGunakan: `!poll <menit> <pertanyaan> | <opsi1> | <opsi2> ...`",
            delete_after=12
        )

    parts    = [p.strip() for p in content.split("|")]
    question = parts[0]
    options  = [p for p in parts[1:] if p]

    if len(options) < 2:
        return await ctx.send("❌ Minimal 2 pilihan.", delete_after=8)
    if len(options) > 10:
        return await ctx.send("❌ Maksimal 10 pilihan.", delete_after=8)
    if duration < 1 or duration > 1440:
        return await ctx.send("❌ Durasi 1–1440 menit.", delete_after=8)

    poll_id  = str(int(datetime.datetime.utcnow().timestamp()))
    end_time = (datetime.datetime.utcnow() + datetime.timedelta(minutes=duration)).isoformat()

    poll = {
        "question":   question,
        "options":    options,
        "votes":      {},
        "channel_id": ctx.channel.id,
        "message_id": None,
        "end_time":   end_time,
        "creator_id": ctx.author.id,
        "ended":      False,
    }

    view = PollView(poll_id, options)
    msg  = await ctx.send(embed=_build_poll_embed(poll, poll_id), view=view)

    poll["message_id"] = msg.id
    polls = load_polls()
    polls[poll_id] = poll
    save_polls(polls)

    await ctx.message.delete(delay=2)
    # Auto end setelah durasi
    asyncio.get_event_loop().create_task(_auto_end_poll(poll_id, duration * 60))


async def _auto_end_poll(poll_id: str, delay_seconds: float):
    await asyncio.sleep(delay_seconds)
    await _end_poll(poll_id)


async def _end_poll(poll_id: str):
    polls = load_polls()
    poll  = polls.get(poll_id)
    if not poll or poll.get("ended"):
        return
    poll["ended"] = True
    save_polls(polls)

    try:
        ch  = bot.get_channel(int(poll["channel_id"]))
        msg = await ch.fetch_message(int(poll["message_id"]))
        await msg.edit(embed=_build_poll_embed(poll, poll_id), view=None)

        # Umumkan pemenang
        votes  = poll.get("votes", {})
        counts = [0] * len(poll["options"])
        for v in votes.values():
            if 0 <= v < len(counts):
                counts[v] += 1

        if any(counts):
            winner_idx = counts.index(max(counts))
            winner_opt = poll["options"][winner_idx]
            embed_win  = discord.Embed(
                title="🏆 Hasil Akhir Poll!",
                description=(
                    f"**{poll['question']}**\n\n"
                    f"🥇 Pemenang: **{winner_opt}** dengan **{counts[winner_idx]} suara**\n"
                    f"🗳️ Total vote: **{len(votes)}**"
                ),
                color=discord.Color.gold()
            )
            embed_win.set_footer(text="Asisten Lurah BFL • Polling Sistem")
            await ch.send(embed=embed_win)
    except Exception as e:
        print(f"[Poll] End error: {e}")


@bot.command(name="endpoll")
@commands.guild_only()
async def end_poll_cmd(ctx, poll_id: str):
    """Akhiri poll lebih awal (admin atau pembuat poll)."""
    polls = load_polls()
    poll  = polls.get(poll_id)
    if not poll:
        return await ctx.send("❌ Poll tidak ditemukan.", delete_after=8)
    if poll.get("ended"):
        return await ctx.send("❌ Poll sudah berakhir.", delete_after=8)
    if ctx.author.id != poll["creator_id"] and not is_admin(ctx.author):
        return await ctx.send("❌ Hanya pembuat poll atau admin.", delete_after=8)

    await _end_poll(poll_id)
    await ctx.send(f"✅ Poll `{poll_id}` diakhiri.", delete_after=8)


@bot.command(name="pollresult")
@commands.guild_only()
async def poll_result(ctx, poll_id: str):
    """Lihat hasil poll berdasarkan ID."""
    polls = load_polls()
    poll  = polls.get(poll_id)
    if not poll:
        return await ctx.send("❌ Poll tidak ditemukan.", delete_after=8)
    await ctx.send(embed=_build_poll_embed(poll, poll_id))


# ═══════════════════════════════════════════════════════
#  PATCH on_message — tambahkan automod hook
# ═══════════════════════════════════════════════════════
# Karena on_message sudah ada di bot_fixed.py, tambahkan
# baris ini SETELAH baris `if message.author.bot: return`
# di fungsi on_message yang ada:
#
#   await on_message_automod(message)
#
# Atau ganti fungsi on_message di bawah ini dan hapus yang lama:

# CATATAN: Jika kamu TIDAK mau menyentuh on_message lama,
# gunakan listener tambahan ini (discord.py mendukung multiple listener
# jika pakai bot.listen() — namun tidak bisa langsung override event yang sama).
# Cara paling aman: tambahkan 1 baris di dalam on_message yang sudah ada.


# ═══════════════════════════════════════════════════════
#  PATCH on_ready — register views baru
# ═══════════════════════════════════════════════════════
# Tambahkan baris ini di dalam on_ready() yang sudah ada,
# SETELAH baris yang sudah ada:
#
#   # Register PollView untuk poll yang belum selesai
#   polls = load_polls()
#   for pid, pw in polls.items():
#       if not pw.get("ended"):
#           bot.add_view(PollView(pid, pw["options"]))

# ═══════════════════════════════════════════════════════
#  RINGKASAN COMMAND BARU
# ═══════════════════════════════════════════════════════
# REACT ROLE:
#   !addreactrole #channel <msg_id> <emoji> @role
#   !removereactrole <msg_id> <emoji>
#   !listreactrole
#
# AUTO MOD:
#   !automod on/off/threshold/interval/mute/status
#
# WELCOME & LEAVE:
#   !setwelcome #channel
#   !setleave #channel
#   !welcometest
#   !leavetest
#
# CUSTOM NICK:
#   !nick <nickname>
#   !nick reset
#   !setnick @user <nickname>
#
# POLLING:
#   !poll <menit> <pertanyaan> | <opsi1> | <opsi2> ...
#   !endpoll <poll_id>
#   !pollresult <poll_id>
