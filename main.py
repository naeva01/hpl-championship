import os

TEAM_FILE = "teams.txt"
MATCH_FILE = "matches.txt"

teams = {}
players = set()


def load_teams():
    if not os.path.exists(TEAM_FILE):
        return

    with open(TEAM_FILE, "r") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            data = line.split("|")

            if len(data) != 4:
                continue

            name = data[0]
            team_players = data[1].split(",") if data[1] else []

            teams[name] = {
                "players": team_players,
                "points": int(data[2]),
                "wins": int(data[3])
            }

            for player in team_players:
                if player:
                    players.add(player)


def save_teams():
    with open(TEAM_FILE, "w") as file:
        for name, team in teams.items():
            player_list = ",".join(team["players"])
            file.write(
                f"{name}|{player_list}|{team['points']}|{team['wins']}\n"
            )


def save_match(winner, loser):
    with open(MATCH_FILE, "a") as file:
        file.write(f"{winner} defeated {loser}\n")


def add_team():
    name = input("Enter hostel team name: ").strip().title()

    if name == "":
        print("Team name cannot be empty.")
        return

    if name in teams:
        print("This team already exists.")
        return

    teams[name] = {
        "players": [],
        "points": 0,
        "wins": 0
    }

    save_teams()
    print(name, "has been added.")


def add_player():
    if len(teams) == 0:
        print("Please add a team first.")
        return

    print("\nAvailable Teams:")
    for team in teams:
        print("-", team)

    team_name = input("Enter team name: ").strip().title()

    if team_name not in teams:
        print("Team not found.")
        return

    player_name = input("Enter player name: ").strip().title()

    if player_name == "":
        print("Player name cannot be empty.")
        return

    if player_name in players:
        print("This player is already registered.")
        return

    if len(teams[team_name]["players"]) == 11:
        print("This team already has 11 players.")
        return

    teams[team_name]["players"].append(player_name)
    players.add(player_name)

    save_teams()

    print(player_name, "has been added to", team_name)


def record_match():
    if len(teams) < 2:
        print("At least two teams are needed.")
        return

    print("\nTeams:")
    for team in teams:
        print("-", team)

    team1 = input("Enter first team: ").strip().title()
    team2 = input("Enter second team: ").strip().title()

    if team1 not in teams or team2 not in teams:
        print("One or both teams were not found.")
        return

    if team1 == team2:
        print("A team cannot play against itself.")
        return

    print("\nWho won?")
    print("1.", team1)
    print("2.", team2)

    choice = input("Enter 1 or 2: ")

    if choice == "1":
        winner = team1
        loser = team2
    elif choice == "2":
        winner = team2
        loser = team1
    else:
        print("Invalid choice.")
        return

    teams[winner]["points"] += 3
    teams[winner]["wins"] += 1

    save_teams()
    save_match(winner, loser)

    print(winner, "won the match.")
    print("3 points have been added.")


def show_points_table():
    if len(teams) == 0:
        print("No teams available.")
        return

    print("\n========== HPL POINTS TABLE ==========")

    sorted_teams = sorted(
        teams.items(),
        key=lambda item: item[1]["points"],
        reverse=True
    )

    print(f"{'Rank':<6}{'Team':<22}{'Players':<10}{'Wins':<8}{'Points'}")
    print("-" * 60)

    rank = 1

    for name, team in sorted_teams:
        print(
            f"{rank:<6}"
            f"{name:<22}"
            f"{len(team['players']):<10}"
            f"{team['wins']:<8}"
            f"{team['points']}"
        )
        rank += 1


def show_players():
    print("\nTotal unique players:", len(players))

    if len(players) == 0:
        print("No players registered yet.")
        return

    print("Players:")

    for player in sorted(players):
        print("-", player)


def declare_winner():
    if len(teams) == 0:
        print("No teams available.")
        return

    sorted_teams = sorted(
        teams.items(),
        key=lambda item: item[1]["points"],
        reverse=True
    )

    winner_name = sorted_teams[0][0]
    winner = sorted_teams[0][1]

    print("\n========== HPL CHAMPIONSHIP ==========")
    print("Champion:", winner_name)
    print("Points:", winner["points"])
    print("Wins:", winner["wins"])

    if winner["players"]:
        print("Players:", ", ".join(winner["players"]))
    else:
        print("Players: No players added")

    print("\nPrize:")

    if winner["points"] >= 9:
        print("Trophy + Rs. 5000 Cash + Free Mess for 1 Week")
    elif winner["points"] >= 6:
        print("Trophy + Rs. 3000 Cash")
    else:
        print("Trophy + Rs. 1000 Cash")

    if len(sorted_teams) > 1:
        runner_up = sorted_teams[1][0]
        print("\nRunner Up:", runner_up)
        print("Runner Up Prize: Rs. 1000 Cash")

    with open("winner.txt", "w") as file:
        file.write("HPL CHAMPION 2026: " + winner_name + "\n")
        file.write("Prize: Trophy + Cash\n")

    print("\nWinner information saved in winner.txt")


def main():
    load_teams()

    print("======================================")
    print("     HOSTEL PREMIER LEAGUE - HPL 2026")
    print("======================================")

    while True:
        print("\n1. Add Hostel Team")
        print("2. Add Player")
        print("3. Record Match")
        print("4. Show Points Table")
        print("5. Show All Players")
        print("6. Declare Winner")
        print("7. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_team()

        elif choice == "2":
            add_player()

        elif choice == "3":
            record_match()

        elif choice == "4":
            show_points_table()

        elif choice == "5":
            show_players()

        elif choice == "6":
            declare_winner()

        elif choice == "7":
            print("Thank you for using HPL.")
            break

        else:
            print("Please enter a number from 1 to 7.")


load_teams()
main()

