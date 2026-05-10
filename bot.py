import discord
from discord.ext import commands, tasks
from discord.ui import Button, View, Select
import json
import os
import asyncio
import aiohttp
import datetime
from PIL import Image, ImageDraw, ImageFont
import io
import requests
import re

# ─────────────────────────────────────────────
#  KONFIGURASI — Dibaca dari Environment Variables
# ─────────────────────────────────────────────
TOKEN                   = os.environ["TOKEN"]
OWNER_ID                = int(os.environ["OWNER_ID"])
SPAM_CHANNEL_ID         = int(os.environ["SPAM_CHANNEL_ID"])
TIKTOK_USERNAME         = os.environ["TIKTOK_USERNAME"]
TIKTOK_CHECK_CHANNEL_ID = int(os.environ["TIKTOK_CHECK_CHANNEL_ID"])
TICKET_CHANNEL_ID       = int(os.environ["TICKET_CHANNEL_ID"])   # ID channel #buat-laporan
VOICE_CATEGORY_ID       = int(os.environ["VOICE_CATEGORY_ID"])   # ID kategori Voice Zone

DATA_FILE        = "data.json"
LAST_TIKTOK_FILE = "last_tiktok.json"
YOUTUBE_FILE     = "youtube.json"
TICKET_FILE      = "tickets.json"
VERIF_FILE       = "verif.json"

# ─────────────────────────────────────────────
#  LEVEL CONFIG
# ─────────────────────────────────────────────
LEVEL_CONFIG = {
    1: {"name": "Bot",          "xp_required": 0,    "color": (108, 117, 125)},
    2: {"name": "Side Brother", "xp_required": 100,  "color": (23, 162, 184)},
    3: {"name": "Member",       "xp_required": 300,  "color": (40, 167, 69)},
    4: {"name": "Brother",      "xp_required": 700,  "color": (255, 193, 7)},
    5: {"name": "Big Brother",  "xp_required": 1500, "color": (220, 53, 69)},
}
XP_PER_MESSAGE = 10

# ─────────────────────────────────────────────
#  BOT INIT
# ─────────────────────────────────────────────
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# Simpan voice room aktif: {channel_id: owner_id}
active_voice_rooms = {}

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def is_admin(member: discord.Member):
    if member.id == OWNER_ID:
        return True
    return member.guild_permissions.administrator or member.guild_permissions.manage_guild

# ─────────────────────────────────────────────
#  DATA HELPERS
# ─────────────────────────────────────────────
def load_json(path):
    if not os.path.exists(path):
        return {}
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

# ─────────────────────────────────────────────
#  RANK CARD
# ─────────────────────────────────────────────
def create_rank_card(username, avatar_bytes, xp, level):
    W, H = 700, 200
    card = Image.new("RGBA", (W, H), (30, 30, 46))
    draw = ImageDraw.Draw(card)
    level_color = LEVEL_CONFIG[level]["color"]

    for i in range(W):
        alpha = int(80 * (i / W))
        draw.line([(i, 0), (i, H)], fill=(*level_color, alpha))

    try:
        avatar_img = Image.open(io.BytesIO(avatar_bytes)).resize((130, 130)).convert("RGBA")
        mask = Image.new("L", (130, 130), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, 130, 130), fill=255)
        avatar_img.putalpha(mask)
        card.paste(avatar_img, (30, 35), avatar_img)
    except Exception:
        draw.ellipse([30, 35, 160, 165], fill=(60, 60, 80))

    draw.ellipse([28, 33, 162, 167], outline=level_color, width=3)

    try:
        font_big   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
        font_med   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
    except Exception:
        font_big = font_med = font_small = ImageFont.load_default()

    draw.text((190, 30), username, fill=(255, 255, 255), font=font_big)
    draw.text((190, 70), f"Level {level}  ·  {LEVEL_CONFIG[level]['name']}", fill=level_color, font=font_med)

    next_xp = get_xp_for_next_level(level)
    if next_xp:
        xp_text  = f"XP: {xp} / {next_xp}"
        progress = min(xp / next_xp, 1.0)
    else:
        xp_text  = f"XP: {xp}  (MAX LEVEL)"
        progress = 1.0

    draw.text((190, 105), xp_text, fill=(200, 200, 220), font=font_small)

    bar_x, bar_y, bar_w, bar_h = 190, 135, 450, 20
    draw.rounded_rectangle([bar_x, bar_y, bar_x+bar_w, bar_y+bar_h], radius=10, fill=(50, 50, 70))
    fill_w = int(bar_w * progress)
    if fill_w > 0:
        draw.rounded_rectangle([bar_x, bar_y, bar_x+fill_w, bar_y+bar_h], radius=10, fill=level_color)

    label = f"{int(progress*100)}% menuju level berikutnya" if next_xp else "🏆 Level Tertinggi!"
    draw.text((bar_x, bar_y+bar_h+5), label, fill=(160, 160, 180), font=font_small)
    draw.text((W-170, H-22), "Asisten Lurah BFL", fill=(80, 80, 100), font=font_small)

    buf = io.BytesIO()
    card.save(buf, format="PNG")
    buf.seek(0)
    return buf

# ─────────────────────────────────────────────
#  UI — VERIFIKASI VIEW
# ─────────────────────────────────────────────
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
        await interaction.response.send_message(
            f"Role **{self.chosen_role}** dipilih. Klik ACC untuk konfirmasi.", ephemeral=True
        )

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
            await interaction.response.send_message(
                f"❌ Role **{self.chosen_role}** tidak ada di server.", ephemeral=True
            )
            return

        await member.add_roles(role)

        try:
            await member.send(
                f"🎉 Verifikasi kamu **disetujui**!\n"
                f"Role **{self.chosen_role}** telah diberikan. Selamat bergabung!"
            )
        except Exception:
            pass

        await interaction.response.edit_message(
            content=f"✅ Role **{self.chosen_role}** diberikan ke **{member.display_name}**.",
            view=None
        )
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
                await member.send(
                    "❌ Verifikasi kamu **ditolak**.\n"
                    "Silakan coba lagi dengan bukti yang lebih jelas."
                )
            except Exception:
                pass

        name = member.display_name if member else str(self.applicant_id)
        await interaction.response.edit_message(
            content=f"❌ Verifikasi **{name}** ditolak.", view=None
        )
        verif = load_verif()
        verif.pop(str(self.applicant_id), None)
        save_verif(verif)

# ─────────────────────────────────────────────
#  UI — TICKET VIEW
# ─────────────────────────────────────────────
class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="📩 Buat Laporan / Diskusi", style=discord.ButtonStyle.primary, custom_id="buat_ticket")
    async def buat_ticket(self, interaction: discord.Interaction, button: Button):
        guild   = interaction.guild
        member  = interaction.user
        tickets = load_tickets()

        # Cek ticket aktif sebelum defer
        for tid, tdata in tickets.items():
            if tdata["user_id"] == member.id and tdata["status"] == "open":
                await interaction.response.send_message(
                    f"⚠️ Kamu sudah punya ticket aktif: <#{tid}>", ephemeral=True
                )
                return

        # Defer dulu agar Discord tidak timeout saat buat channel
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
                name=f"ticket-{member.display_name}",
                overwrites=overwrites,
                reason=f"Ticket oleh {member}"
            )

            tickets[str(ticket_channel.id)] = {
                "user_id": member.id,
                "status": "open",
                "created_at": str(datetime.datetime.utcnow())
            }
            save_tickets(tickets)

            embed = discord.Embed(
                title="📩 Ticket Dibuat",
                description=(
                    f"Halo {member.mention}! Ticket kamu telah dibuat.\n\n"
                    "Silakan jelaskan laporan atau pertanyaan kamu di sini.\n"
                    "Admin akan segera merespons.\n\n"
                    "Klik **Tutup Ticket** jika sudah selesai."
                ),
                color=discord.Color.blue(),
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_footer(text="Asisten Lurah BFL • Ticket System")
            await ticket_channel.send(
                content=f"{member.mention}",
                embed=embed,
                view=CloseTicketView(ticket_channel.id)
            )
            await interaction.followup.send(
                f"✅ Ticket dibuat: {ticket_channel.mention}", ephemeral=True
            )

        except discord.Forbidden:
            await interaction.followup.send(
                "❌ Bot tidak punya izin untuk membuat channel. Pastikan bot punya permission **Manage Channels**.",
                ephemeral=True
            )
        except Exception as e:
            await interaction.followup.send(
                f"❌ Terjadi error saat membuat ticket: `{e}`", ephemeral=True
            )

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
            await interaction.response.send_message("⚠️ Data ticket tidak ditemukan.", ephemeral=True)
            return
        if member.id != tdata["user_id"] and not is_admin(member):
            await interaction.response.send_message(
                "❌ Hanya pembuat ticket atau admin yang bisa menutup.", ephemeral=True
            )
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

# ─────────────────────────────────────────────
#  EVENTS
# ─────────────────────────────────────────────
@bot.event
async def on_ready():
    print(f"✅ {bot.user} online sebagai Asisten Lurah BFL!")
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="Desa BFL 🏘️")
    )
    # Register persistent views agar tombol tetap berfungsi setelah bot restart
    bot.add_view(TicketView())
    tickets = load_tickets()
    for channel_id, tdata in tickets.items():
        if tdata.get("status") == "open":
            bot.add_view(CloseTicketView(int(channel_id)))
    check_tiktok.start()
    print("✅ Semua sistem aktif.")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # ── Verifikasi via DM (foto masuk ke DM owner) ──
    if isinstance(message.channel, discord.DMChannel) and message.author.id != OWNER_ID:
        if message.attachments:
            verif = load_verif()
            uid   = str(message.author.id)
            if uid in verif:
                await message.channel.send("⏳ Verifikasi kamu sedang diproses. Mohon tunggu.")
                return

            verif[uid] = {"status": "pending"}
            save_verif(verif)

            owner = await bot.fetch_user(OWNER_ID)
            embed = discord.Embed(
                title="📋 Verifikasi Masuk",
                description=(
                    f"**User:** {message.author} (`{message.author.id}`)\n"
                    f"**Display Name:** {message.author.display_name}\n\n"
                    "Pilih role lalu klik ACC atau REJECT."
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
                await owner.send(embed=embed, files=files, view=VerifView(message.author.id, guild_id))
                await message.channel.send(
                    "✅ Bukti verifikasi telah dikirim ke admin. Tunggu konfirmasi ya!"
                )
            else:
                await message.channel.send("❌ Kamu harus bergabung ke server terlebih dahulu.")
            return

        # DM biasa — proses command jika ada
        await bot.process_commands(message)
        return

    # ── XP System (server) ──
    data = load_data()
    uid  = str(message.author.id)
    if uid not in data:
        data[uid] = {"xp": 0, "level": 1}
    old_level          = data[uid]["level"]
    data[uid]["xp"]   += XP_PER_MESSAGE
    new_level          = get_level(data[uid]["xp"])
    data[uid]["level"] = new_level
    save_data(data)
    if new_level > old_level:
        embed = discord.Embed(
            title="🎉 LEVEL UP!",
            description=(
                f"{message.author.mention} naik ke "
                f"**Level {new_level} — {LEVEL_CONFIG[new_level]['name']}**!"
            ),
            color=discord.Color.from_rgb(*LEVEL_CONFIG[new_level]["color"])
        )
        await message.channel.send(embed=embed)
    await bot.process_commands(message)

@bot.event
async def on_voice_state_update(member, before, after):
    """Auto-delete voice room saat kosong."""
    if before.channel and before.channel.id in active_voice_rooms:
        if len(before.channel.members) == 0:
            try:
                await before.channel.delete(reason="Voice room kosong, auto-delete.")
            except Exception:
                pass
            active_voice_rooms.pop(before.channel.id, None)

# ─────────────────────────────────────────────
#  COMMANDS — LEVEL
# ─────────────────────────────────────────────
@bot.command(name="rank")
async def rank(ctx, member: discord.Member = None):
    if ctx.author.id != OWNER_ID and ctx.channel.id != SPAM_CHANNEL_ID:
        await ctx.send(f"⚠️ Command ini hanya bisa digunakan di <#{SPAM_CHANNEL_ID}>!", delete_after=5)
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
    card_buf = create_rank_card(str(member.display_name), avatar_bytes, xp, level)
    await ctx.send(file=discord.File(fp=card_buf, filename="rank.png"))

@bot.command(name="leaderboard", aliases=["lb", "top"])
async def leaderboard(ctx):
    if ctx.author.id != OWNER_ID and ctx.channel.id != SPAM_CHANNEL_ID:
        await ctx.send(f"⚠️ Command ini hanya bisa digunakan di <#{SPAM_CHANNEL_ID}>!", delete_after=5)
        return
    data         = load_data()
    sorted_users = sorted(data.items(), key=lambda x: x[1]["xp"], reverse=True)[:10]
    medals       = ["🥇", "🥈", "🥉"]
    embed = discord.Embed(title="🏆 Leaderboard XP — Asisten Lurah BFL", color=discord.Color.gold())
    for i, (uid, info) in enumerate(sorted_users):
        try:
            user = await bot.fetch_user(int(uid))
            name = user.display_name
        except Exception:
            name = f"User#{uid}"
        lvl   = info["level"]
        medal = medals[i] if i < 3 else f"#{i+1}"
        embed.add_field(
            name=f"{medal} {name}",
            value=f"Level {lvl} ({LEVEL_CONFIG[lvl]['name']}) · {info['xp']} XP",
            inline=False
        )
    await ctx.send(embed=embed)

# ─────────────────────────────────────────────
#  COMMANDS — PENGUMUMAN (Owner via DM)
# ─────────────────────────────────────────────
@bot.command(name="pengumuman")
async def pengumuman(ctx, channel_id: int, *, pesan: str):
    if not isinstance(ctx.channel, discord.DMChannel):
        await ctx.send("⚠️ Command ini hanya bisa digunakan via DM bot.")
        return
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Kamu tidak punya izin.")
        return
    channel = bot.get_channel(channel_id)
    if not channel:
        await ctx.send("❌ Channel tidak ditemukan. Pastikan ID benar.")
        return
    embed = discord.Embed(
        title="📢 PENGUMUMAN",
        description=pesan,
        color=discord.Color.blue(),
        timestamp=datetime.datetime.utcnow()
    )
    embed.set_footer(text="Asisten Lurah BFL")
    await channel.send("@everyone", embed=embed)
    await ctx.send(f"✅ Pengumuman berhasil dikirim ke #{channel.name}!")

# ─────────────────────────────────────────────
#  COMMANDS — MODERASI
# ─────────────────────────────────────────────
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
async def timeout_error(ctx, error):
    await ctx.send(f"❌ Error: {error}")

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
async def ban_error(ctx, error):
    await ctx.send(f"❌ Error: {error}")

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
    await ctx.send(f"✅ Role **{role_name}** berhasil diberikan ke {member.mention}.")

@bot.command(name="removerole")
@commands.has_permissions(manage_roles=True)
async def remove_role(ctx, member: discord.Member, *, role_name: str):
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if not role:
        await ctx.send(f"❌ Role **{role_name}** tidak ditemukan.")
        return
    await member.remove_roles(role)
    await ctx.send(f"✅ Role **{role_name}** berhasil dihapus dari {member.mention}.")

@bot.command(name="clear", aliases=["purge", "hapus"])
@commands.has_permissions(manage_messages=True)
async def clear_messages(ctx, jumlah: int = 10):
    await ctx.channel.purge(limit=jumlah + 1)
    await ctx.send(f"✅ **{jumlah}** pesan berhasil dihapus.", delete_after=5)

@clear_messages.error
async def clear_error(ctx, error):
    await ctx.send(f"❌ Error: {error}")

# ─────────────────────────────────────────────
#  COMMANDS — TICKET SETUP
# ─────────────────────────────────────────────
@bot.command(name="setupticket")
async def setup_ticket(ctx):
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Hanya owner yang bisa setup ticket.", delete_after=5)
        return
    channel = bot.get_channel(TICKET_CHANNEL_ID)
    if not channel:
        await ctx.send("❌ Channel #buat-laporan tidak ditemukan. Cek TICKET_CHANNEL_ID.")
        return
    embed = discord.Embed(
        title="📩 Buat Laporan / Diskusi",
        description=(
            "Klik tombol di bawah untuk membuat ticket.\n\n"
            "Ticket akan membuat channel privat yang hanya bisa dilihat oleh kamu dan admin.\n"
            "Gunakan untuk laporan, pertanyaan, atau diskusi pribadi."
        ),
        color=discord.Color.blue()
    )
    embed.set_footer(text="Asisten Lurah BFL • Ticket System")
    await channel.send(embed=embed, view=TicketView())
    await ctx.send(f"✅ Ticket system dipasang di {channel.mention}!")

# ─────────────────────────────────────────────
#  COMMANDS — YOUTUBE DATABASE
# ─────────────────────────────────────────────
@bot.command(name="addyt")
async def add_youtube(ctx, nama: str, link: str):
    if not is_admin(ctx.author):
        await ctx.send("❌ Hanya admin yang bisa menambah link YouTube.", delete_after=5)
        return
    if "youtube.com" not in link and "youtu.be" not in link:
        await ctx.send("❌ Link harus berupa link YouTube yang valid.", delete_after=5)
        return
    yt = load_youtube()
    yt[nama] = link
    save_youtube(yt)
    await ctx.send(f"✅ **{nama}** berhasil ditambahkan ke database YouTube!")

@bot.command(name="removeyt")
async def remove_youtube(ctx, *, nama: str):
    if not is_admin(ctx.author):
        await ctx.send("❌ Hanya admin yang bisa menghapus link YouTube.", delete_after=5)
        return
    yt = load_youtube()
    if nama not in yt:
        await ctx.send(f"❌ **{nama}** tidak ditemukan.", delete_after=5)
        return
    del yt[nama]
    save_youtube(yt)
    await ctx.send(f"✅ **{nama}** berhasil dihapus dari database.")

@bot.command(name="youtube", aliases=["yt", "daftaryt"])
async def list_youtube(ctx):
    if ctx.author.id != OWNER_ID and ctx.channel.id != SPAM_CHANNEL_ID:
        await ctx.send(f"⚠️ Command ini hanya bisa digunakan di <#{SPAM_CHANNEL_ID}>!", delete_after=5)
        return
    yt = load_youtube()
    if not yt:
        await ctx.send("📭 Database YouTube masih kosong.")
        return
    embed = discord.Embed(title="🎬 Database YouTube — BFL", color=discord.Color.red())
    for nama, link in yt.items():
        embed.add_field(name=nama, value=link, inline=False)
    embed.set_footer(text="Asisten Lurah BFL • YouTube Database")
    await ctx.send(embed=embed)

# ─────────────────────────────────────────────
#  COMMANDS — VOICE ROOM
# ─────────────────────────────────────────────
@bot.command(name="createroom")
async def create_room(ctx, *, nama_room: str = None):
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.send("❌ Command ini hanya bisa digunakan di server.")
        return

    guild    = ctx.guild
    member   = ctx.author
    category = discord.utils.get(guild.categories, id=VOICE_CATEGORY_ID)

    if not category:
        await ctx.send("❌ Kategori Voice Zone tidak ditemukan. Cek VOICE_CATEGORY_ID.")
        return

    # Cek apakah sudah punya room aktif
    for ch_id, owner_id in list(active_voice_rooms.items()):
        if owner_id == member.id:
            ch = guild.get_channel(ch_id)
            if ch:
                await ctx.send(f"⚠️ Kamu sudah punya room aktif: **{ch.name}**", delete_after=10)
                return

    # Cek batas maksimal room
    current_rooms = [ch for ch in category.voice_channels if ch.id in active_voice_rooms]
    if len(current_rooms) >= 10:
        await ctx.send("⚠️ Maksimal 10 room aktif. Tunggu ada room yang kosong.", delete_after=10)
        return

    room_name = nama_room if nama_room else f"Room {member.display_name}"

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(connect=True, view_channel=True),
        member: discord.PermissionOverwrite(
            connect=True, manage_channels=True, mute_members=True, move_members=True
        ),
        guild.me: discord.PermissionOverwrite(connect=True, manage_channels=True),
    }

    voice_channel = await guild.create_voice_channel(
        name=room_name,
        category=category,
        overwrites=overwrites,
        user_limit=10,
        reason=f"Room dibuat oleh {member}"
    )
    active_voice_rooms[voice_channel.id] = member.id

    embed = discord.Embed(
        title="🎙️ Voice Room Dibuat!",
        description=(
            f"Room **{room_name}** telah dibuat di kategori **Voice Zone**.\n"
            "Room akan otomatis dihapus jika sudah kosong.\n"
            f"Kapasitas: **10 orang**"
        ),
        color=discord.Color.green()
    )
    embed.set_footer(text=f"Dibuat oleh {member.display_name}")
    await ctx.send(embed=embed)

# ─────────────────────────────────────────────
#  COMMANDS — VERIFIKASI
# ─────────────────────────────────────────────
@bot.command(name="verif")
async def verif_cmd(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.send(
            "📋 **Verifikasi BFL**\n\n"
            "Kirim foto bukti kamu di sini.\n"
            "Admin akan mereviu dan memberikan role: **Moderator**, **Stream**, atau **Clipper**."
        )
        return
    await ctx.send(
        f"{ctx.author.mention} Silakan kirim foto bukti ke **DM bot** ini!",
        delete_after=15
    )
    try:
        await ctx.author.send(
            "📋 **Verifikasi BFL**\n\n"
            "Kirim foto bukti kamu di sini.\n"
            "Admin akan mereviu dan memberikan role: **Moderator**, **Stream**, atau **Clipper**."
        )
    except discord.Forbidden:
        await ctx.send(
            f"❌ {ctx.author.mention} DM kamu tertutup. Buka DM dulu lalu coba lagi.",
            delete_after=10
        )

# ─────────────────────────────────────────────
#  COMMANDS — HELP
# ─────────────────────────────────────────────
@bot.command(name="help")
async def help_cmd(ctx):
    embed = discord.Embed(title="📖 Asisten Lurah BFL — Daftar Command", color=discord.Color.blue())
    embed.add_field(
        name="🏅 Level (di #spam)",
        value="`!rank [@user]`\n`!leaderboard`\n`!youtube`",
        inline=False
    )
    embed.add_field(
        name="🎬 YouTube (Admin only, semua channel)",
        value="`!addyt <nama> <link>`\n`!removeyt <nama>`",
        inline=False
    )
    embed.add_field(
        name="🎙️ Voice Room",
        value="`!createroom [nama]` — Buat room voice (maks 10 orang, auto-delete saat kosong)",
        inline=False
    )
    embed.add_field(
        name="📋 Verifikasi Mod/Stream/Clipper",
        value="`!verif` — Mulai verifikasi via DM bot",
        inline=False
    )
    embed.add_field(
        name="🔇 Moderasi",
        value="`!timeout @user <menit> [alasan]`\n`!ban @user [alasan]`\n`!unban <id>`\n`!clear [jumlah]`",
        inline=False
    )
    embed.add_field(
        name="🎭 Role",
        value="`!addrole @user <nama_role>`\n`!removerole @user <nama_role>`",
        inline=False
    )
    embed.add_field(
        name="📢 Pengumuman (Owner via DM bot)",
        value="`!pengumuman <channel_id> <pesan>`",
        inline=False
    )
    embed.add_field(
        name="⚙️ Setup (Owner only)",
        value="`!setupticket` — Pasang tombol ticket di #buat-laporan",
        inline=False
    )
    embed.set_footer(text="Asisten Lurah BFL • Desa BFL")
    await ctx.send(embed=embed)

# ─────────────────────────────────────────────
#  TIKTOK TRACKER
# ─────────────────────────────────────────────
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
            title=f"🎵 @{TIKTOK_USERNAME} baru saja posting di TikTok!",
            description=f"Lihat video terbaru sekarang 👇\n{tiktok_url}",
            color=discord.Color.from_rgb(254, 44, 85),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_footer(text="Asisten Lurah BFL • TikTok Tracker")
        await channel.send(embed=embed)
    except Exception as e:
        print(f"[TikTok Check Error] {e}")

@check_tiktok.before_loop
async def before_check():
    await bot.wait_until_ready()

# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
bot.run(TOKEN)
