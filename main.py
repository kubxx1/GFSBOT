import discord
from discord.ext import commands
import os
import asyncio
from models import Team, Match
from simulation import SimulationEngine
from utils import parse_squad_text, generate_random_squad
from config import *
import json

# Database file
TEAMS_DB = "/app/data/teams.json"

# Pobieranie tokena bezpośrednio ze zmiennych środowiskowych (Railway)
TOKEN = os.getenv("DISCORD_TOKEN")

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# In-memory storage
teams = {}
sim_engine = SimulationEngine()

def save_teams():
    with open(TEAMS_DB, 'w', encoding='utf-8') as f:
        data = {name: team.to_dict() for name, team in teams.items()}
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_teams():
    global teams
    if os.path.exists(TEAMS_DB):
        try:
            with open(TEAMS_DB, 'r', encoding='utf-8') as f:
                data = json.load(f)
                teams = {name: Team.from_dict(team_data) for name, team_data in data.items()}
            print(f"Loaded {len(teams)} teams from {TEAMS_DB}")
        except Exception as e:
            print(f"Error loading teams: {e}")
            teams = {}

# Load teams on startup
load_teams()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="create_team", description="Stworz nowa druzyne z lista zawodnikow")
async def create_team(interaction: discord.Interaction, name: str, squad_text: str):
    players = parse_squad_text(squad_text)
    new_team = Team(name, players)
    teams[name] = new_team
    save_teams()
    
    summary = f"Drużyna **{name}** stworzona pomyślnie z {len(players)} zawodnikami.\n"
    summary += f"Średni OVR: {new_team.get_avg_ovr():.1f}"
    await interaction.response.send_message(summary)

@bot.tree.command(name="create_random_team", description="Stwórz losową drużynę do testów")
async def create_random_team(interaction: discord.Interaction, name: str):
    players = generate_random_squad()
    new_team = Team(name, players)
    teams[name] = new_team
    save_teams()
    await interaction.response.send_message(f"Losowa drużyna **{name}** stworzona (Średni OVR: {new_team.get_avg_ovr():.1f}).")

@bot.tree.command(name="delete_team", description="Usuń istniejącą drużynę")
async def delete_team(interaction: discord.Interaction, name: str):
    if name in teams:
        del teams[name]
        save_teams()
        await interaction.response.send_message(f"Drużyna **{name}** została usunięta.")
    else:
        await interaction.response.send_message(f"Nie znaleziono drużyny o nazwie **{name}**.", ephemeral=True)

@bot.tree.command(name="edit_team", description="Edytuj skład istniejącej drużyny")
async def edit_team(interaction: discord.Interaction, name: str, squad_text: str):
    if name in teams:
        players = parse_squad_text(squad_text)
        teams[name].players = players
        save_teams()
        summary = f"Skład drużyny **{name}** zaktualizowany ({len(players)} zawodników).\n"
        summary += f"Nowy średni OVR: {teams[name].get_avg_ovr():.1f}"
        await interaction.response.send_message(summary)
    else:
        await interaction.response.send_message(f"Nie znaleziono drużyny **{name}**. Użyj /create_team aby ją stworzyć.", ephemeral=True)

@bot.tree.command(name="list_teams", description="Pokaż listę wszystkich drużyn")
async def list_teams(interaction: discord.Interaction):
    if not teams:
        await interaction.response.send_message("Brak stworzonych drużyn.")
        return
    
    msg = "**Dostępne drużyny:**\n"
    for name, team in teams.items():
        msg += f"- {name} (OVR: {team.get_avg_ovr():.1f}, {len(team.players)} zawodników)\n"
    await interaction.response.send_message(msg)

@bot.tree.command(name="play_match", description="Rozpocznij mecz między dwiema drużynami")
async def play_match(interaction: discord.Interaction, home_team: str, away_team: str, mode: str = "live"):
    if home_team not in teams or away_team not in teams:
        await interaction.response.send_message("Jedna lub obie drużyny nie istnieją! Użyj najpierw /create_team.", ephemeral=True)
        return

    home = teams[home_team]
    away = teams[away_team]
    
    # Create match instance
    match = Match(home, away, mode=mode.lower())
    
    # Check for empty teams
    if not home.players or not away.players:
        await interaction.response.send_message("Jedna z drużyn nie ma zawodników! Nie można rozpocząć meczu.", ephemeral=True)
        return

    # Defer response to prevent "Application not responding" if something takes long
    await interaction.response.defer()
    
    await interaction.followup.send(f"⚽ **MECZ ROZPOCZĘTY!** ⚽\n{home.name} vs {away.name}\nTryb: {mode}")
    
    # Simulation Loop
    channel = interaction.channel
    if not channel:
        channel = interaction.user # Fallback

    try:
        while not match.is_finished():
            sim_engine.simulate_minute(match)
            
            # Wait for "live" feeling
            if mode.lower() == 'live':
                 # Find events for this minute
                 events_this_minute = [log for log in match.logs if log.startswith(f"{match.current_minute}'")]
                 for event in events_this_minute:
                     try:
                         await channel.send(event)
                     except Exception as e:
                         print(f"Error sending message: {e}")

                 await asyncio.sleep(LIVE_MATCH_UPDATE_INTERVAL)
            
        
        # Match Ended - Profesjonalna karta wyniku (Embed)
        embed = discord.Embed(
            title="🏟️  KONIEC MECZU!",
            description=f"Starcie pomiędzy **{home.name}** a **{away.name}** dobiegło końca!",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="Wynik", 
            value=f" {home.name} {match.home_team.score} : {match.away_team.score} {away.name}", 
            inline=False
        )
        
        # Dodajemy statystyki do pól pod spodem
        embed.add_field(name="Gole  (Dom) ⚽", value=f"{match.home_team.score}", inline=True)
        embed.add_field(name="Gole  (Wyjazd)⚽", value=f"{match.away_team.score}", inline=True)
        
        embed.set_footer(text="Symulacja zakończona pomyślnie ⚽ | GFS | Globalna Federacja Symulacji")
        
        await channel.send(embed=embed)
        
        # Man of the Match - Złota karta
        motm_player = calculate_motm(home, away)
        if motm_player:
            motm_embed = discord.Embed(
                title="🌟 ZAWODNIK MECZU (MOTM) 🌟",
                description=f"Najlepszy zawodnik dzisiejszego spotkania to **{motm_player.name}**!",
                color=discord.Color.gold() # Złoty kolor dla MVP
            )
            motm_embed.add_field(name="Pozycja", value=motm_player.position, inline=True)
            motm_embed.add_field(name="Ocena", value=f"⭐ {motm_player.rating:.1f}", inline=True)
            if motm_player.goals > 0:
                motm_embed.add_field(name="Bramki", value=f"⚽ {motm_player.goals}", inline=True)
            
            await channel.send(embed=motm_embed)
    except Exception as e:
        print(f"CRASH IN MATCH LOOP: {e}")
        await channel.send(f"🆘 **BŁĄD KRYTYCZNY:** Mecz został przerwany z powodu błędu silnika: `{e}`")

def calculate_motm(home_team, away_team):
    all_players = home_team.players + away_team.players
    if not all_players:
        return None
    
    # Sort by rating, then goals, then assists
    motm = max(all_players, key=lambda p: (p.rating, p.goals, p.assists))
    return motm

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("\n❌ BŁĄD: Brak tokena DISCORD_TOKEN!")
        print("Wejdź w Railway -> Variables -> Add Variable i dodaj DISCORD_TOKEN\n")
