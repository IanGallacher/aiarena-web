import io

import matplotlib.pyplot as plt
import pandas as pd
from django.db import connection, transaction

from aiarena.core.models import Bot, Season, MatchParticipation, SeasonParticipation, Match
from aiarena.core.models.season_bot_matchup_stats import SeasonBotMatchupStats


class StatsGenerator:

    @staticmethod
    def update_stats(bot: Bot):
        with transaction.atomic():
            current_season: Season = Season.get_current_season()
            sp: SeasonParticipation = bot.current_season_participation()
            sp.lock_me()
            sp.match_count = MatchParticipation.objects.filter(bot=bot,
                                                               match__result__isnull=False,
                                                               match__round__season=current_season).count()
            if sp.match_count != 0:
                sp.win_count = MatchParticipation.objects.filter(bot=bot, result='win',
                                                        match__round__season=current_season
                                                        ).count()
                sp.win_perc = sp.win_count / sp.match_count
                sp.loss_count = MatchParticipation.objects.filter(bot=bot, result='loss',
                                                                  match__round__season=current_season
                                                                  ).count()
                sp.loss_perc = sp.loss_count / sp.match_count
                sp.tie_count = MatchParticipation.objects.filter(bot=bot, result='tie',
                                                                  match__round__season=current_season
                                                                  ).count()
                sp.tie_perc = sp.tie_count / sp.match_count
                sp.crash_count = MatchParticipation.objects.filter(bot=bot, result='loss', result_cause__in=['crash',
                                                                                                  'timeout',
                                                                                                  'initialization_failure'],
                                                                   match__round__season=current_season
                                                                   ).count()
                sp.crash_perc = sp.crash_count / sp.match_count
                graph = StatsGenerator._generate_elo_graph(bot.id)
                if graph is not None:
                    sp.elo_graph.save('elo.png', graph)
            else:
                sp.win_count = 0
                sp.loss_count = 0
                sp.tie_count = 0
                sp.crash_count = 0
            sp.save()

            StatsGenerator._update_matchup_stats(sp)

    @staticmethod
    def _update_matchup_stats(sp: SeasonParticipation):
        for season_participation in SeasonParticipation.objects.exclude(bot=sp.bot):
            with connection.cursor() as cursor:
                matchup_stats = SeasonBotMatchupStats.objects.select_for_update()\
                    .get_or_create(bot=sp, opponent=season_participation)[0]

                cursor.execute("""
                select count(cm.id) as count
                from core_match cm
                inner join core_matchparticipation bot_p on cm.id = bot_p.match_id
                inner join core_matchparticipation opponent_p on cm.id = opponent_p.match_id
                inner join core_round cr on cm.round_id = cr.id
                inner join core_season cs on cr.season_id = cs.id
                where cs.id = %s -- make sure it's part of the current season
                and bot_p.bot_id = %s
                and opponent_p.bot_id = %s
                and bot_p.result is not null -- make sure it's a finished match wih a result
                """, [sp.season_id, sp.bot_id, season_participation.bot_id])
                row = cursor.fetchone()
                matchup_stats.match_count = row[0]

                if matchup_stats.match_count != 0:

                    cursor.execute("""
                    select count(cm.id) as count
                    from core_match cm
                    inner join core_matchparticipation bot_p on cm.id = bot_p.match_id
                    inner join core_matchparticipation opponent_p on cm.id = opponent_p.match_id
                    inner join core_round cr on cm.round_id = cr.id
                    inner join core_season cs on cr.season_id = cs.id
                    where cs.id = %s -- make sure it's part of the current season
                    and bot_p.bot_id = %s
                    and opponent_p.bot_id = %s
                    and bot_p.result = 'win'
                    """, [sp.season_id, sp.bot_id, season_participation.bot_id])
                    row = cursor.fetchone()
                    matchup_stats.win_count = row[0]
                    matchup_stats.win_perc = matchup_stats.win_count/matchup_stats.match_count

                    cursor.execute("""
                    select count(cm.id) as count
                    from core_match cm
                    inner join core_matchparticipation bot_p on cm.id = bot_p.match_id
                    inner join core_matchparticipation opponent_p on cm.id = opponent_p.match_id
                    inner join core_round cr on cm.round_id = cr.id
                    inner join core_season cs on cr.season_id = cs.id
                    where cs.id = %s -- make sure it's part of the current season
                    and bot_p.bot_id = %s
                    and opponent_p.bot_id = %s
                    and bot_p.result = 'loss'
                    """, [sp.season_id, sp.bot_id, season_participation.bot_id])
                    row = cursor.fetchone()
                    matchup_stats.loss_count = row[0]
                    matchup_stats.loss_perc = matchup_stats.loss_count/matchup_stats.match_count

                    cursor.execute("""
                    select count(cm.id) as count
                    from core_match cm
                    inner join core_matchparticipation bot_p on cm.id = bot_p.match_id
                    inner join core_matchparticipation opponent_p on cm.id = opponent_p.match_id
                    inner join core_round cr on cm.round_id = cr.id
                    inner join core_season cs on cr.season_id = cs.id
                    where cs.id = %s -- make sure it's part of the current season
                    and bot_p.bot_id = %s
                    and opponent_p.bot_id = %s
                    and bot_p.result = 'tie'
                    """, [sp.season_id, sp.bot_id, season_participation.bot_id])
                    row = cursor.fetchone()
                    matchup_stats.tie_count = row[0]
                    matchup_stats.tie_perc = matchup_stats.tie_count/matchup_stats.match_count

                    cursor.execute("""
                    select count(cm.id) as count
                    from core_match cm
                    inner join core_matchparticipation bot_p on cm.id = bot_p.match_id
                    inner join core_matchparticipation opponent_p on cm.id = opponent_p.match_id
                    inner join core_round cr on cm.round_id = cr.id
                    inner join core_season cs on cr.season_id = cs.id
                    where cs.id = %s -- make sure it's part of the current season
                    and bot_p.bot_id = %s
                    and opponent_p.bot_id = %s
                    and bot_p.result = 'crash'
                    """, [sp.season_id, sp.bot_id, season_participation.bot_id])
                    row = cursor.fetchone()
                    matchup_stats.crash_count = row[0]
                    matchup_stats.crash_perc = matchup_stats.crash_count/matchup_stats.match_count
                else:
                    matchup_stats.win_count = 0
                    matchup_stats.loss_count = 0
                    matchup_stats.tie_count = 0
                    matchup_stats.crash_count = 0

                matchup_stats.save()

    @staticmethod
    def _get_data(bot_id):
        with connection.cursor() as cursor:
            query = (f"""
                select distinct
                cb.name, 
                avg(cp.resultant_elo) as elo, 
                date(cr.created) as date 
                from core_matchparticipation cp
                    inner join core_result cr on cp.match_id = cr.match_id
                    left join core_bot cb on cp.bot_id = cb.id
                where resultant_elo is not null 
                    and bot_id = {bot_id} 
                group by date(cr.created) 
                order by cr.created
                """)
            cursor.execute(query)
            elo_over_time = pd.DataFrame(cursor.fetchall())
        return elo_over_time

    @staticmethod
    def _generate_plot_image(df):
        plot = io.BytesIO()
        ax = plt.gca()
        graph = df.plot(kind='line', x='Date', y='ELO', ax=ax, figsize=(12, 9), color=('#86c232'))
        graph.spines["top"].set_visible(False)
        graph.spines["right"].set_visible(False)
        graph.spines["left"].set_color('#86c232')
        graph.spines["bottom"].set_color('#86c232')
        graph.autoscale(enable=True, axis='x')
        graph.get_xaxis().tick_bottom()
        graph.get_yaxis().tick_left()

        plt.title('ELO over time', fontsize=20, color=('#86c232'))
        plt.xticks(rotation=60)
        ax.xaxis.label.set_color('#86c232')
        ax.tick_params(axis='x', colors='#86c232')
        ax.tick_params(axis='y', colors='#86c232')
        plt.tight_layout()  # Avoids savefig cutting off x-label
        plt.savefig(plot, format="png", transparent=True)
        plt.cla()  # Clears axis in preparation for new graph
        return plot

    @staticmethod
    def _generate_elo_graph(bot_id: int):
        df = StatsGenerator._get_data(bot_id)
        if not df.empty:
            df[1] = pd.to_numeric(df[1])
            df.columns = ['Name', 'ELO', 'Date']

            return StatsGenerator._generate_plot_image(df)
        else:
            return None
