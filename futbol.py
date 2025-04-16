import pandas as pd
from datetime import datetime

# Cargar datasets
players = pd.read_csv("/Users/greta/Desktop/PORTFOLIO/futbol/players.csv")
appearances = pd.read_csv("/Users/greta/Desktop/PORTFOLIO/futbol/appearances.csv")
clubs = pd.read_csv("/Users/greta/Desktop/PORTFOLIO/futbol/clubs.csv")
competitions = pd.read_csv("/Users/greta/Desktop/PORTFOLIO/futbol/competitions.csv")

# Calcular edad
players["date_of_birth"] = pd.to_datetime(players["date_of_birth"], errors="coerce")
today = pd.to_datetime("today")
players["age"] = (today - players["date_of_birth"]).dt.days // 365

# Filtrar edad menor o igual a 21
players_sub21 = players[players["age"] <= 21]
players_sub21_ids = players_sub21["player_id"]

# TOP 10 países con más jugadores sub21
top_young = players_sub21["country_of_citizenship"].value_counts().head(10).reset_index()
top_young.columns = ["country", "number_of_u21_players"]
top_young.to_csv("top_young.csv", index=False)

# promedio de altura por pais
players["height_in_cm"] = pd.to_numeric(players["height_in_cm"], errors="coerce")
avg_height = players.groupby("country_of_citizenship")["height_in_cm"].mean().reset_index()
avg_height.columns = ["country", "avg_height_cm"]
avg_height.to_csv("avg_height.csv", index=False)

# Valor de mercado promedio por país (u21)
players["market_value_in_eur"] = pd.to_numeric(players["market_value_in_eur"], errors="coerce")
market_value = players_sub21.groupby("country_of_citizenship")["market_value_in_eur"].mean().reset_index()
market_value.columns = ["country", "avg_market_value_u21"]
market_value.to_csv("market_value.csv", index=False)

# minutos jugados por país (u211)
u21_minutes = appearances[appearances["player_id"].isin(players_sub21_ids)]
minutes_by_country = u21_minutes.merge(players[["player_id", "country_of_citizenship"]], on="player_id")
minutes_sum = minutes_by_country.groupby("country_of_citizenship")["minutes_played"].sum().reset_index()
minutes_sum.columns = ["country", "total_minutes_played_u21"]
minutes_sum.to_csv("minutes_played.csv", index=False)
# calcular edad promedio de jugadores sub21 por país
players["date_of_birth"] = pd.to_datetime(players["date_of_birth"], errors="coerce")
today = pd.to_datetime("today")
players["age"] = (today - players["date_of_birth"]).dt.days // 365

# filtro sub21
sub21_players = players[players["age"] <= 21]

# edad promedio por pais
avg_age_sub21 = sub21_players.groupby("country_of_citizenship")["age"].mean().sort_values()

# export
avg_age_sub21.to_frame(name="average_age").reset_index().rename(columns={"country_of_citizenship": "country"}).to_csv("avg_age_sub21.csv", index=False)

# Ligas
competition_name = {
    "IT1": "Serie A", 
    "ES1": "La Liga", 
    "FR1": "Ligue 1", 
    "GB1": "Premier League", 
    "L1": "Bundesliga",
    "NL1": "Eredivisie", 
    "BE1": "Pro League", 
    "PT1": "Primeira Liga",
    "GR1": "Super League Greece", 
    "UKR1": "Ukrainian Premier League",
    "RU1": "Russian Premier League", 
    "DK1": "Danish Superliga", 
    "PO1": "Primeira Liga", 
    "SC1": "Scottish Premiership", 
    "TR1": "Turkish Süper Lig", 
    # Si hace falta, agregamos ligas... 
}
players["league_name"] = players["current_club_domestic_competition_id"].map(competition_name)


# confederaciones
country_to_confed = {
    # CONMEBOL
    "Argentina": "CONMEBOL", "Brazil": "CONMEBOL", "Uruguay": "CONMEBOL",
    "Chile": "CONMEBOL", "Paraguay": "CONMEBOL", "Peru": "CONMEBOL",
    "Colombia": "CONMEBOL", "Ecuador": "CONMEBOL", "Venezuela": "CONMEBOL",
    "Bolivia": "CONMEBOL",

    # UEFA
    "Germany": "UEFA", "France": "UEFA", "Spain": "UEFA", "Italy": "UEFA",
    "England": "UEFA", "Netherlands": "UEFA", "Belgium": "UEFA",
    "Portugal": "UEFA", "Greece": "UEFA", "Turkey": "UEFA", "Ukraine": "UEFA",
    "Russia": "UEFA", "Denmark": "UEFA", "Scotland": "UEFA", "Sweden": "UEFA",
    "Norway": "UEFA", "Switzerland": "UEFA", "Poland": "UEFA", "Austria": "UEFA",
    "Croatia": "UEFA", "Czech Republic": "UEFA", "Serbia": "UEFA", "Finland": "UEFA",
    "Slovakia": "UEFA", "Slovenia": "UEFA", "Hungary": "UEFA", "Romania": "UEFA",
    "Bosnia-Herzegovina": "UEFA", "Georgia": "UEFA", "Armenia": "UEFA", "Albania": "UEFA",
    "North Macedonia": "UEFA", "Iceland": "UEFA", "Ireland": "UEFA", "Wales": "UEFA",
   

    # CONCACAF
    "Mexico": "CONCACAF", "United States": "CONCACAF", "Canada": "CONCACAF",
    "Costa Rica": "CONCACAF", "Honduras": "CONCACAF", "Panama": "CONCACAF",
    "Jamaica": "CONCACAF", "El Salvador": "CONCACAF", "Guatemala": "CONCACAF",
    "Trinidad and Tobago": "CONCACAF", "Haiti": "CONCACAF",

    # CAF
    "Senegal": "CAF", "Nigeria": "CAF", "Ghana": "CAF", "Ivory Coast": "CAF",
    "Cameroon": "CAF", "Egypt": "CAF", "Morocco": "CAF", "Algeria": "CAF",
    "Tunisia": "CAF", "South Africa": "CAF", "Mali": "CAF", "Burkina Faso": "CAF",
    "The Gambia": "CAF", "Gabon": "CAF", "Benin": "CAF", "Togo": "CAF", "Congo DR": "CAF",

    # AFC
    "Japan": "AFC", "South Korea": "AFC", "Australia": "AFC", "Iran": "AFC",
    "Saudi Arabia": "AFC", "Qatar": "AFC", "Uzbekistan": "AFC", "Iraq": "AFC",
    "United Arab Emirates": "AFC", "China": "AFC", "India": "AFC",

    # OFC
    "New Zealand": "OFC", "Fiji": "OFC"
}

players["confederation"] = players["country_of_citizenship"].map(country_to_confed)
players["confederation"].fillna("Other", inplace=True)

players.to_csv("players_con_confederation.csv", index=False)

import pandas as pd
from datetime import datetime

# Cargar datos
players = pd.read_csv("/Users/greta/Desktop/PORTFOLIO/futbol/players.csv")
appearances = pd.read_csv("/Users/greta/Desktop/PORTFOLIO/futbol/appearances.csv")

# Convertir fecha y calcular edad
players["date_of_birth"] = pd.to_datetime(players["date_of_birth"], errors="coerce")
today = pd.to_datetime("today")
players["age"] = (today - players["date_of_birth"]).dt.days // 365

# Filtrar sub21
u21 = players[players["age"] <= 21]

# Total minutos por jugador
minutos = appearances.groupby("player_id")["minutes_played"].sum().reset_index()

# Unir con los jugadores U21
ranking = u21.merge(minutos, on="player_id", how="left")

# Limpiar nulos
ranking["minutes_played"].fillna(0, inplace=True)
ranking["market_value_in_eur"].fillna(0, inplace=True)

# Normalizar valores
ranking["mv_norm"] = (ranking["market_value_in_eur"] - ranking["market_value_in_eur"].min()) / (ranking["market_value_in_eur"].max() - ranking["market_value_in_eur"].min())
ranking["mp_norm"] = (ranking["minutes_played"] - ranking["minutes_played"].min()) / (ranking["minutes_played"].max() - ranking["minutes_played"].min())

# Score combinado (ajustá pesos si querés)
ranking["score"] = 0.6 * ranking["mv_norm"] + 0.4 * ranking["mp_norm"]

# Top 10
top_u21 = ranking.sort_values("score", ascending=False).head(10)

# Seleccionar columnas útiles
top_u21_final = top_u21[[
    "name",
    "country_of_citizenship",
    "current_club_name",
    "age",
    "position",
    "minutes_played",
    "market_value_in_eur",
    "image_url"
]]

# Exportar a CSV
top_u21_final.to_csv("best_u21_players.csv", index=False)

print(top_u21_final)

# convertir fecha para filtrar U21
players["date_of_birth"] = pd.to_datetime(players["date_of_birth"], errors="coerce")
hoy = pd.to_datetime("today")
players["age"] = (hoy - players["date_of_birth"]).dt.days // 365

# filtro  solo jugadores U21
u21_players = players[players["age"] <= 21]

# minutos jugados — agrupando por jugador y club 
minutos = appearances.groupby(["player_id", "player_current_club_id"])["minutes_played"].sum().reset_index()

# merge con datos de jugadores U21 para eliminar dupes
u21_data = u21_players.merge(minutos, on="player_id", how="left")

# reemplazar NaN por 0 para eliminar jugadores sin minutos
u21_data["minutes_played"] = u21_data["minutes_played"].fillna(0)

# agrupar por club para totalizar minutos y market value únicos
resumen_clubes = u21_data.groupby("current_club_name").agg({
    "minutes_played": "sum",
    "market_value_in_eur": "sum",
    "player_id": "count"
}).rename(columns={"player_id": "u21_players_count"}).reset_index()

# Exportar a CSV 
resumen_clubes.to_csv("u21_club_summary.csv", index=False)

# filtro sub 21 para aplicar a todo el dashboard y exportar
df['u21_status'] = df['age'].apply(lambda x: 'U21' if x <= 21 else 'Not U21')
df.to_csv("players_with_u21_status.csv", index=False)
