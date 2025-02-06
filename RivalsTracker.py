import sys
import requests
import flet as ft
from flet.core.progress_bar import ProgressBar
from flet.core.textfield import TextField

name1 = "i'm jahames"
name2 = "Pandahero2007"
name3 = "Vasti0n"
name4 = 'Koloru'
name5 = 'Leprechaun5823'
name6 = 'Maddog923'

pName = name4

base = 'https://mrapi.org'


def get_uid(name):
    uid_url = base+'/api/player-id/'+ name
    r = requests.get(uid_url).json()
    
    try:
        return r['id']
    except:
        print(r)
        sys.exit(1)


def get_main(hero_stats):
    main = {
        'hero':'',
        'playtime': 0,
        'kda': 0,
        'id': 0
        }
    
    for i in hero_stats:
        playtime = 0
        if 'ranked' in hero_stats[i]:
            playtime += hero_stats[i]['ranked']['playtime']['raw']
        if 'unranked' in hero_stats[i]:
            playtime += hero_stats[i]['unranked']['playtime']['raw']
        
        if playtime > main['playtime']:
            main['playtime'] = playtime
            main['hero'] = hero_stats[i]['hero_name']
            try:
                main['kda'] = hero_stats[i]['ranked']['kda']
            except:
                main['kda'] = main['kda']
            main['id'] = i
    return main


def get_player_stats(UID):
    url = base+'/api/player/'+str(UID)
    r = requests.get(url)
    r.raise_for_status()
    return r.json()


def get_leaderboard(hero_id):
    leaderboard = requests.get(base + '/api/leaderboard/' + str(hero_id))
    leaderboard.raise_for_status()
    return leaderboard.json()


def main(page: ft.Page) -> None:
    page.title = "Rivals Comparison"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = 'light'

    def button_clicked(e):
        name = tb4.value
        text.value = 'Loading...'
        try:
            stats = get_player_stats(get_uid(name))

            p_main = get_main(stats['hero_stats'])
            leaderboard = get_leaderboard(p_main['id'])

            kda_l = []

            r = 100
            for i in range(100):
                pb.value = i / r
                page.update()
                try:
                    kda = float(
                        get_player_stats(leaderboard[i]['player_id'])['hero_stats'][p_main['id']]['ranked']['kda'])
                    kda_l.append(kda)
                except:
                    continue
            v = f"Average KDA of {p_main['hero']} in top 100: {str(round(sum(kda_l) / len(kda_l), 2))} | {name}'s KDA: {p_main['kda']}"
            print(v)
            text.value = v
            page.update()

            # with open('data/'+str(main['hero'])+'-leaderboard.json', 'w', encoding='utf-8') as f:
            #     json.dump(leaderboard, f, ensure_ascii=False, indent=4)

            # with open('data/'+str(name)+'-data.json', 'w', encoding='utf-8') as f:
            #     json.dump(rj, f, ensure_ascii=False, indent=4)

        except Exception as err:
            text.value = 'Failed to load data...' + str(err)


    text: ft.Text = ft.Text('Enter User',text_align=ft.TextAlign.CENTER,width=600)
    pb: ProgressBar = ProgressBar(width=600)
    tb4 = ft.TextField(label="User", hint_text="Enter Exact Username")
    b = ft.ElevatedButton(text="Submit", on_click=button_clicked)

    page.add(
        ft.Row(
            [ft.Column(
                [text, pb],
                alignment=ft.MainAxisAlignment.CENTER
            )],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Row(
            [ft.Column(
                [tb4,b],
                alignment=ft.MainAxisAlignment.CENTER
            )],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

if __name__ == '__main__':
    ft.app(target=main)
    
