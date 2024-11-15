from typing import List, Tuple
from datetime import datetime
from connector import select, insert

class Api:

    @staticmethod
    def habit_exist(habit_nm: str) -> bool:
        """
        Проверка наличия записи о привычке в БД

        Parameters
        ----------
        habit_nm : str
            Название привычки
        
        Returns
        -------
        bool
            True если запись есть в бд, иначе False
        """
        query = f"""
        select * from habits.habit
        where habit_nm = '{habit_nm}';
        """
        result = select(query=query)
        return len(result) > 0

    @staticmethod
    def add_habit_to_user(user_id: int, habit_nm: str) -> None:
        """
        Добавление пользователю привычки

        Parameters
        ----------
        user_id : int
            ID пользователя, которому добавляется привычка
        habit_nm : str
            Название привычки
        """

        if not Api.habit_exist(habit_nm=habit_nm):
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
    def list_user_habits(user_id: int) -> List[Tuple[int, str]]:
        """
        Список привычек пользователя

        Parameters
        ----------
        user_id : int
            ID пользователя
        """

        query = f"""
        select habit_id, habit_nm from habits.habit_x_user
        left join habits.habit using(habit_id)
        where user_id = {user_id};
        """
        habits_list = select(query=query)
        return habits_list

    @staticmethod
    def list_habits_names(user_id: int) -> List[str]:
        habits_list = Api.list_user_habits(user_id=user_id)

        return [i.habit_nm for i in habits_list]

    @staticmethod
    def add_event(user_id: int, habit_id: int, event_ts: str = str(datetime.now()), comment: str = "") -> None:
        """
        Добавление записи о выполнении привычки

        Parameters
        ----------
        user_id : int
            ID пользователя

        habit_id : int
            ID привычки

        event_ts : str
            Время события в виде строки (default=datetime.now())

        comment: str
            Комментарий к записи (default='')
        """
        
        query = f"""
        insert into habits.event (row_id, habit_id, user_id, comment_txt, event_ts, changed_ts)
        values (nextval('habits.seq_event_row_id'), {habit_id}, {user_id}, '{comment}', '{event_ts}', now() at time zone 'Europe/Moscow');
        """
        insert(query=query)

    @staticmethod
    def last_event(user_id: int, habit_id: int) -> str:
        """
        Последняя запись о выполнении привычки

        Parameters
        ----------
        user_id : int
            ID пользователя

        habit_id : int
            ID привычки
        """
        
        query = f"""
        select event_ts 
        from habits.event                             
        join habits.habit using (habit_id)
        where
            user_id = {user_id}
            and habit_id = '{habit_id}'
        order by event_ts desc
        limit 1;
        """

        result = select(query=query)
        return str(result[0].event_ts) if result else ""
