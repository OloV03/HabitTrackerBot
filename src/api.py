from typing import List
from datetime import datetime
from connector import select, insert

class Api:

    @staticmethod
    def add_habit_to_user(user_id: int, habit_nm: str) -> None:
        # TODO: добавить проверку наличия записи о привычке
        query = f"""
        insert into habits.habit
            select nextval('habits.seq_habit_id'), '{habit_nm}', now();
        """
        insert(query=query)

        query = f"""
        insert into habits.habit_x_user
            select habit_id, {user_id}, now()
            from habits.habit
            where habit_nm = '{habit_nm}';
        """
        insert(query=query)

    @staticmethod
    def list_user_habits(user_id: int) -> List[tuple]:
        query = f"""
        select habit_id, habit_nm from habits.habit_x_user
        left join habits.habit using(habit_id)
        where user_id = {user_id};
        """
        habits_list = select(query=query)
        return habits_list

    @staticmethod
    def add_event(user_id: int, habit_id: int, event_ts: str = str(datetime.now()), comment: str = "") -> None:
        query = f"""
        insert into habits.event (row_id, habit_id, user_id, comment_txt, event_ts, changed_ts)
        values (nextval('habits.seq_event_row_id'), {habit_id}, {user_id}, '{comment}', '{event_ts}', now());
        """
        insert(query=query)
